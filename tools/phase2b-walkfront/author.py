"""Walk-front-only native own-material hotfix. No other clip/export may be written."""
from pathlib import Path
import sys,json,io,subprocess,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';O=R/'assets-src/characters/phase2b-walkfront';sys.path.insert(0,str(R/'tools/phase1b'));from animate import bone,translate
IDS=['ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo'];T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']['walk-front'];BASE=json.loads((D/'before.json').read_text())['commit']
# Native tracing of Juni's knees and elbow arcs; original frame order retained.
K=[[[43,78],[49,84]],[[45,83],[50,76]],[[44,84],[50,73]],[[44,74],[49,84]],[[43,78],[49,84]],[[45,84],[51,76]],[[44,84],[50,75]],[[43,77],[49,84]]]
E=[[[33,61],[61,59]],[[33,63],[62,60]],[[33,62],[61,61]],[[34,58],[62,63]],[[33,60],[61,60]],[[34,63],[62,60]],[[33,63],[61,62]],[[34,61],[61,60]]]
HIPX=[0,0,0,1,0,1,1,0]
def segment(im,mask):
 a=np.array(im);a[~mask]=0;return Image.fromarray(a)
def connected(mask, predicate):
 seen=np.zeros(mask.shape,bool);regions=[]
 for y,x in zip(*np.where(mask)):
  if seen[y,x]:continue
  todo=[(y,x)];seen[y,x]=True;reg=[]
  while todo:
   yy,xx=todo.pop();reg.append((yy,xx))
   for y2,x2 in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
    if 0<=y2<112 and 0<=x2<96 and mask[y2,x2]and not seen[y2,x2]:seen[y2,x2]=True;todo.append((y2,x2))
  if predicate(reg):regions.append(reg)
 assert regions
 reg=max(regions,key=len);result=np.zeros(mask.shape,bool)
 for y,x in reg:result[y,x]=True
 return result

def parts(root):
 native=Image.open(root/'native/front.png').convert('RGBA');a=np.array(native);yy,xx=np.indices(a.shape[:2]);c=json.loads((root/'rig.json').read_text())['front'];p={'body':Image.open(root/'layers/front/body.png').convert('RGBA')}
 for side,left in [('L',True),('R',False)]:
  half=xx<48 if left else xx>=48
  legmask=connected(half&(yy>=68)&(a[:,:,3]>0),lambda reg:max(y for y,x in reg)>=97)
  for name,lo,hi in [('thigh',68,84),('shin',80,95),('shoe',92,112)]:p[side+name]=segment(native,legmask&(yy>=lo)&(yy<hi))
  # Own full sleeve silhouette replaces the inherited narrow Haneul polygon.
  outer=((xx<=40)&((yy<60)|(xx<=38))&((yy<65)|(xx<=36)))if left else((xx>=56)&((yy<60)|(xx>=58))&((yy<65)|(xx>=60)))
  armmask=connected(outer&(yy>=47)&(yy<77)&(a[:,:,3]>0),lambda reg:any(abs(x-c['arms'][side][2][0])<=4 and abs(y-c['arms'][side][2][1])<=3 for y,x in reg))
  p[side+'upperarm']=segment(native,armmask&(yy<64));p[side+'forearm']=segment(native,armmask&(yy>=60))
 return p,c

def torso(im,dx,dy,hip):
 out=Image.new('RGBA',(96,112));a=np.array(im)
 for y in range(112):
  t=max(0,min(1,(y-47)/24));shift=round(dx+(hip-dx)*t);row=Image.fromarray(a[y:y+1]);out.alpha_composite(row,(shift,y+dy))
 return out

def shoe(im,sole,lift,side):
 q=im.crop(im.getbbox());w,h=q.size
 # Front contact projects the toe toward camera; lifted heels foreshorten.
 ratio=.82 if lift<=2 else .72;vh=1 if lift<=2 else .58 if lift<9 else .45
 q=q.resize((max(5,round(w*ratio)),max(3,round(h*vh))),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(96,112));out.alpha_composite(q,(round(sole[0]-(q.width-1)/2),round(sole[1]-q.height+1)));return out

def frame(p,c,i):
 pose=T[i];dx,dy=pose['bodyDeltaX'],pose['bodyDeltaY'];out=Image.new('RGBA',(96,112));records=[];arms=[];legs=[]
 for j,side in enumerate(['L','R']):
  h,k,a=c['joints'][side];off=h[0]-[44,52][j];sole=[pose['soleScreenLR'][j][0]+off,pose['soleScreenLR'][j][1]];hip=[h[0]+HIPX[i],h[1]+dy];knee=[K[i][j][0]+off,K[i][j][1]];ankle=[sole[0],sole[1]-3];lift=98-sole[1];leg=Image.new('RGBA',(96,112));bone(leg,p[side+'thigh'],h,k,hip,knee);bone(leg,p[side+'shin'],k,a,knee,ankle);leg.alpha_composite(shoe(p[side+'shoe'],sole,lift,side));legs.append((sole[1],leg));records.append({'side':side,'hip':hip,'knee':knee,'sole':sole,'lift':lift})
  a,b,w=c['arms'][side];shoulder=[a[0]+dx,a[1]+dy];elbow=E[i][j];hand=pose['handScreenLR'][j];arm=Image.new('RGBA',(96,112));bone(arm,p[side+'upperarm'],a,b,shoulder,elbow);bone(arm,p[side+'forearm'],b,w,elbow,hand);arms.append((hand[1],arm));records[-1].update({'shoulder':shoulder,'elbow':elbow,'hand':hand})
 for _,arm in sorted(arms,key=lambda a:a[0])[:1]:out.alpha_composite(arm)
 for _,leg in sorted(legs,key=lambda a:a[0]):out.alpha_composite(leg)
 out.alpha_composite(torso(p['body'],dx,dy,HIPX[i]))
 out.alpha_composite(max(arms,key=lambda a:a[0])[1])
 # Far arm outside the torso remains visible, while its central pixels obey occlusion.
 return out,records

def build(id):
 assert id in IDS;phase='phase2a'if id in ['ara','doyun']else'phase2b';root=R/f'assets-src/characters/{phase}/{id}';p,c=parts(root);dest=O/id;dest.mkdir(parents=True,exist_ok=True)
 for name,im in p.items():im.save(dest/(name+'.png'))
 stem=f'public/assets/characters/{id}/atlas';atlas=Image.open(io.BytesIO(subprocess.check_output(['git','show',BASE+':'+stem+'.png']))).convert('RGBA');meta=json.loads((R/(stem+'.json')).read_text())['frames'];records=[]
 for i in range(8):
  im,land=frame(p,c,i);assert set(np.unique(np.array(im)[:,:,3]))<={0,255};key=f'walk-front-{i}';f=meta[key]['frame'];atlas.paste(im,(f['x'],f['y']));im.save(root/'frames'/f'{key}.png');records.append({'frame':key,'landmarks':land,'juniReference':key})
 atlas.save(R/(stem+'.png'));(dest/'guide.json').write_text(json.dumps({'id':id,'poses':records,'before':BASE,'policy':'Only8 walk-front cells; own native art, observed Juni rhythm/contact/elbows, torso differential1px. No timing/engine edit.'},indent=2)+'\n')
 # Native1:1 source review, immutable Juni / before / candidate at matching phase.
 ja=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');jm=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',BASE+':'+stem+'.png']))).convert('RGBA');board=Image.new('RGBA',(768,420),(28,30,38));dr=ImageDraw.Draw(board);gifs=[]
 for row,(name,a,m)in enumerate([('Juni',ja,jm),('BEFORE',old,meta),('CANDIDATE',atlas,meta)]):
  dr.text((4,row*140+2),f'{id} {name} | source-only native1:1',fill='white')
  for i in range(8):
   f=m[f'walk-front-{i}']['frame'];q=a.crop((f['x'],f['y'],f['x']+96,f['y']+112));board.alpha_composite(q,(96*i,row*140+18))
 board.save(D/f'{id}-front-source-native.png');board.resize((1536,840),Image.Resampling.NEAREST).save(D/f'{id}-front-source-2x.png')
 for i in range(8):
  q=Image.new('RGBA',(288,140),(28,30,38));dr=ImageDraw.Draw(q)
  for col,(label,a,m)in enumerate([('Juni',ja,jm),('Before',old,meta),('After',atlas,meta)]):
   dr.text((col*96+3,2),label,fill='white');f=m[f'walk-front-{i}']['frame'];q.alpha_composite(a.crop((f['x'],f['y'],f['x']+96,f['y']+112)),(col*96,18))
  gifs.append(q.convert('RGB').resize((576,280),Image.Resampling.NEAREST))
 gifs[0].save(D/f'{id}-front-source-review.gif',save_all=True,append_images=gifs[1:],duration=92,loop=0,disposal=2)
 print(id,'8 walk-front cells only',flush=True)
if __name__=='__main__':build(sys.argv[1])
