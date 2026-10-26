"""Offline six-character motion-only repair. Never exports an approved identity.
Rigid head/torso and own garment/foot pixels; no runtime/controller modification.
"""
from pathlib import Path
import sys,json,math,hashlib,subprocess,io
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2b';O=R/'assets-src/characters/phase2b-motion';D=R/'docs/phase2b-motion'
sys.path.insert(0,str(R/'tools/phase1b'));from animate import bone,translate,ik
IDS=['sori','jiwon','nari','taeyang','yuna','hyunwoo']
T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
K={
'walk-front':[[[44,80],[50,84]],[[44,84],[55,80]],[[44,85],[56,77]],[[44,78],[50,84]],[[43,80],[50,84]],[[45,85],[56,79]],[[44,84],[55,79]],[[44,80],[50,84]]],
'walk-back':[[[44,76],[53,84]],[[44,77],[54,85]],[[43,85],[54,77]],[[45,82],[52,85]],[[43,76],[53,84]],[[44,84],[55,77]],[[45,76],[54,84]],[[43,85],[54,77]]],
'run-front':[[[47,80],[50,85]],[[44,88],[55,81]],[[47,78],[50,83]],[[48,73],[52,76]],[[43,84],[55,79]],[[46,82],[52,88]],[[46,79],[52,83]],[[46,76],[53,77]]],
'run-back':[[[44,79],[53,84]],[[44,80],[54,84]],[[44,77],[52,83]],[[45,74],[54,77]],[[44,79],[52,84]],[[44,85],[54,77]],[[44,75],[53,82]],[[43,75],[53,77]]],
}
def own_lower(id,d):
 im=Image.open(S/id/'native'/f'{d}.png').convert('RGBA');a=np.array(im);out={}
 # Foot-connected half-body segmentation preserves the whole own shoe/cuff.
 for side,left in [('L',True),('R',False)]:
  mask=a[:,:,3]>0;mask[:68]=False;mask[:,48 if left else 0:96 if left else 48]=False
  seen=np.zeros(mask.shape,bool);regions=[]
  for y,x in zip(*np.where(mask)):
   if seen[y,x]:continue
   stack=[(y,x)];seen[y,x]=True;region=[]
   while stack:
    yy,xx=stack.pop();region.append((yy,xx))
    for y2,x2 in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
     if 0<=y2<112 and 0<=x2<96 and mask[y2,x2]and not seen[y2,x2]:seen[y2,x2]=True;stack.append((y2,x2))
   if max(q[0]for q in region)>=97:regions.append(region)
  assert regions,(id,d,side)
  region=max(regions,key=len);leg=np.zeros_like(a)
  for y,x in region:leg[y,x]=a[y,x]
  for name,lo,hi in [('thigh',68,84),('shin',80,95),('shoe',92,112)]:
   q=leg.copy();q[:lo]=0;q[hi:]=0;out[side+name]=Image.fromarray(q)
 return out

def foot(im,target,view,lift,side,mode=None):
 """Native authored shoe projection: stance/toe, trailing heel or rear sole.
 Own footwear pixels supply palette/material; no new character master.
 """
 bb=im.getbbox();q=im.crop(bb);w,h=q.size
 if (view=='front'and lift>3)or(view=='back'and mode=='heel'):
  # A trailing foot exposes a small heel, not the flat planted toe billboard.
  q=q.resize((max(4,round(w*.62)),max(4,round(h*.62))),Image.Resampling.NEAREST)
 elif view=='back'and mode=='sole':
  # Rear swing exposes the underside. Recover outsole colors from own shoe.
  rgb=np.array(q);colors=rgb[rgb[:,:,3]>0][:,:3];luma=colors.mean(1);dark=tuple(int(v)for v in colors[np.argmin(luma)]);mid=tuple(int(v)for v in np.median(colors,axis=0));light=tuple(min(255,round(v*1.13))for v in mid)
  nw=max(5,round(w*.72));nh=7;sole=Image.new('RGBA',(nw,nh));dr=ImageDraw.Draw(sole);poly=[(2,0),(nw-3,0),(nw-1,2),(nw-1,nh-3),(nw-3,nh-1),(2,nh-1),(0,nh-3),(0,2)];dr.polygon(poly,fill=(*mid,255),outline=(*dark,255))
  dr.line((2,1,nw-3,1),fill=(*light,255));dr.rounded_rectangle((2,3,nw-3,nh-3),radius=1,fill=(*tuple(round(.65*v)for v in mid),255))
  q=sole
 # No interpolation, blur, global sharpening or runtime rescale.
 out=Image.new('RGBA',(96,112));out.alpha_composite(q,(round(target[0]-(q.width-1)/2),round(target[1]-q.height+1)));return out

def front(id,key,i,parts,c,blend=1):
 pose=T[key][i];d=key.split('-')[1];dx=round(pose['bodyDeltaX']*blend);dy=round(pose['bodyDeltaY']*blend);out=Image.new('RGBA',(96,112));legs=[];record=[]
 for j,side in enumerate(['L','R']):
  h,k,a=c['joints'][side];offset=h[0]-[45,53][j];sole=[pose['soleScreenLR'][j][0]+offset,pose['soleScreenLR'][j][1]];hip=[h[0]+dx,h[1]+dy];knee=[K[key][i][j][0]+offset,K[key][i][j][1]]
  # Interpolate joint targets at start/stop; never dissolve whole images.
  bb=parts[side+'shoe'].getbbox();rest=[round((bb[0]+bb[2]-1)/2),bb[3]-1];sole=[round(rest[n]+blend*(sole[n]-rest[n]))for n in range(2)];knee=[round(k[n]+blend*(knee[n]-k[n]))for n in range(2)]
  bb=parts[side+'shoe'].getbbox();ankle=[sole[0],sole[1]-max(2,bb[3]-1-a[1])];lift=98-sole[1];legs.append((sole[1],side,h,k,a,hip,knee,ankle,sole,lift));record.append({'side':side,'hip':hip,'knee':knee,'ankle':ankle,'sole':sole,'lift':lift})
 for _,side,h,k,a,hip,knee,ankle,sole,lift in sorted(legs):
  bone(out,parts[side+'thigh'],h,k,hip,knee);bone(out,parts[side+'shin'],k,a,knee,ankle);out.alpha_composite(foot(parts[side+'shoe'],sole,d,lift,side,([['heel','flat'],['heel','flat'],['sole','heel'],['sole','flat'],['heel','flat'],['flat','heel'],['heel','flat'],['sole','heel']][i][0 if side=='L'else 1]if key=='walk-back'else [['heel','flat'],['heel','flat'],['heel','flat'],['heel','sole'],['heel','flat'],['flat','heel'],['heel','flat'],['heel','sole']][i][0 if side=='L'else 1]if key=='run-back'else None)))
 # Arms belong behind/in front of the torso according to their observed depth.
 arms=[]
 for j,side in enumerate(['L','R']):
  a,b,w=c['arms'][side];hand=[round(w[n]+([2,-2][j]if n==0 else 0)+blend*(pose['handScreenLR'][j][n]-w[n]-([2,-2][j]if n==0 else 0)))for n in range(2)];shoulder=[a[0]+dx,a[1]+dy];elbow=[round((shoulder[0]+hand[0])/2)+(-3 if side=='L'else 3),round((shoulder[1]+hand[1])/2)+2];arm=Image.new('RGBA',(96,112));bone(arm,parts[side+'upperarm'],a,b,shoulder,elbow);bone(arm,parts[side+'forearm'],b,w,elbow,hand);arms.append((hand[1]-dy,side,arm))
 translate(out,parts['body'],dx,dy)
 for _,side,arm in sorted(arms):out.alpha_composite(arm)
 return out,record

def profile(id,phase,action,parts,c,amount=1):
 out=Image.new('RGBA',(96,112));run=action=='run';stride=64 if run else 44;A=stride/4;bob=round(-abs(math.sin(phase*math.tau))*(2 if run else 1)*amount);records=[]
 for side,offset in [('L',.5),('R',0)]:
  p=(phase+offset)%1
  if p<=.5:x=A-stride*p;lift=0
  else:
   u=(p-.5)*2;x=(-A)*(2*u**3-3*u**2+1)+A*(-2*u**3+3*u**2)+(-stride/2)*(u**3-2*u**2+u)+(-stride/2)*(u**3-u**2);lift=math.sin(math.pi*u)*(10 if run else 6)
  x*=amount;lift*=amount
  h,k,a=c['joints'][side];hip=[48+(0 if side=='R'else 1),70+bob];ankle=[48+round(x),c['groundY'][side]-round(lift)];knee=ik(hip,ankle,math.dist(h,k),math.dist(k,a),-1)
  bone(out,parts[side+'thigh'],h,k,hip,knee);bone(out,parts[side+'shin'],k,a,knee,ankle);translate(out,parts[side+'shoe'],ankle[0]-a[0],ankle[1]-a[1]);records.append({'side':side,'phase':p,'planted':p<=.5,'hip':hip,'knee':knee,'ankle':ankle,'groundRelativeX':x,'lift':lift})
 translate(out,parts['body'],0,bob)
 if 'Rforearm'in parts:
  a,b,w=c['arms']['R'];x=records[1]['groundRelativeX'];swing=-x/A;elbow=[b[0]+round(swing*(2 if run else 1)),b[1]+bob-round(abs(swing))];hand=[w[0]+round(swing*(8 if run else 5)),w[1]+bob-round(abs(swing)*2)];bone(out,parts['Rforearm'],b,w,elbow,hand)
 return out,records

def build(id):
 assert id in IDS
 cfg=json.loads((S/id/'rig.json').read_text());outdir=O/id;outdir.mkdir(parents=True,exist_ok=True);frames={};audit=[]
 for d in ['front','back','right']:
  parts={p.stem:Image.open(p).convert('RGBA')for p in(S/id/'layers'/d).glob('*.png')}
  if d in ['front','back']:parts.update(own_lower(id,d))
  layers=outdir/'layers'/d;layers.mkdir(parents=True,exist_ok=True)
  for n,im in parts.items():im.save(layers/f'{n}.png')
  for action in ['walk','run']:
   for i in range(8):
    key=action+'-'+d;im,land=front(id,key,i,parts,cfg[d])if d!='right'else profile(id,i/8,action,parts,cfg[d]);name=key+'-'+str(i);frames[name]=im;audit.append({'frame':name,'landmarks':land,'juniReference':f'{key}-{i}'})
  # Existing3-frame timings/clip graph stay intact. Native pose targets settle
  # to the unchanged idle image; right starts advance swing->contact->stance.
  for action,weights in [('start',[.25,.7,1]),('stop',[.75,.35,0])]:
   for i,weight in enumerate(weights):
    if action=='stop'and i==2:
     im=Image.open(S/id/'frames'/f'idle-{d}-0.png').convert('RGBA');land={'settlesToUnchangedIdle':True}
    elif d=='right':im,land=profile(id,[.875,0,.125][i]if action=='start'else .25,'walk',parts,cfg[d],weight)
    else:im,land=front(id,'walk-'+d,1 if action=='start'and i==2 else 0,parts,cfg[d],weight)
    frames[f'{action}-{d}-{i}']=im;audit.append({'frame':f'{action}-{d}-{i}','landmarks':land})
 for key in ['walk-front','walk-back','walk-right','run-front','run-back','run-right']:
  assert len({frames[f'{key}-{i}'].tobytes()for i in range(8)})==8,(id,key)
 pub=R/f'public/assets/characters/{id}';before=json.loads((D/'before-manifest.json').read_text())['commit'];atlas=Image.open(io.BytesIO(subprocess.check_output(['git','show',before+':'+str((pub/'atlas.png').relative_to(R))]))).convert('RGBA');meta=json.loads((pub/'atlas.json').read_text())['frames'];changes=[]
 for name,im in frames.items():
  bb=im.getbbox();assert bb and bb[0]>=1 and bb[1]>=1 and bb[2]<96 and bb[3]<112,(id,name,bb)
  assert set(np.unique(np.array(im)[:,:,3]))<={0,255}
  f=meta[name]['frame'];old=atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112));changes.append({'frame':name,'beforeRGBA':hashlib.sha256(old.tobytes()).hexdigest(),'afterRGBA':hashlib.sha256(im.tobytes()).hexdigest(),'changedPixels':int(np.any(np.array(old)!=np.array(im),2).sum())});atlas.paste(im,(f['x'],f['y']));im.save(S/id/'frames'/f'{name}.png')
 atlas.save(pub/'atlas.png');(outdir/'motion-guide.json').write_text(json.dumps({'id':id,'frameRegistration':[96,112,48,100],'source':'Own preserved native materials; Juni poses and contact progression supply motion landmarks, not color pixels','poses':audit,'changes':changes},indent=2)+'\n')
 for action in ['walk','run']:
  board=Image.new('RGBA',(768,396),(28,30,38,255));dr=ImageDraw.Draw(board)
  for row,d in enumerate(['front','back','right']):
   for i in range(8):board.alpha_composite(frames[f'{action}-{d}-{i}'],(i*96,row*132+20));dr.text((i*96+2,row*132+3),f'{d} {i}',fill='white')
  board.save(D/f'{id}-{action}-candidate-native.png');board.resize((1536,792),Image.Resampling.NEAREST).save(D/f'{id}-{action}-candidate-2x.png')
 print(id,'motion cells replaced',len(frames))
if __name__=='__main__':build(sys.argv[1])
