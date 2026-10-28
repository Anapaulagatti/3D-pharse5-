"""Bake illustrated own-layer rigs with accepted Juni landmarks; no primary art drawing."""
from pathlib import Path
import json,math,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion';D=R/'docs/phase3a-npc-expansion';sys.path.insert(0,str(R/'tools/phase1b'));from animate import bone,translate,ik
# Import the original pure affine helpers under a disambiguated module name when run as a script.
T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
K={
'front':[[[43,78],[49,84]],[[45,83],[50,76]],[[44,84],[50,73]],[[44,74],[49,84]],[[43,78],[49,84]],[[45,84],[51,76]],[[44,84],[50,75]],[[43,77],[49,84]]],
'back':[[[44,76],[53,84]],[[44,77],[54,85]],[[43,85],[54,77]],[[45,82],[52,85]],[[43,76],[53,84]],[[44,84],[55,77]],[[45,76],[54,84]],[[43,85],[54,77]]]}
def own_shoe(q,target,lift=0):
 b=q.getbbox();q=q.crop(b)
 # Preserve this actor's native shoe pixels at every phase; scaling lifted shoes broke ankle joins.
 out=Image.new('RGBA',(96,112));out.alpha_composite(q,(math.floor(target[0]-(q.width-1)/2+.5),math.floor(target[1]-q.height+1+.5)));return out

def forward(parts,c,d,i,action):
 pose=T['walk-'+d][i];walking=action=='walk';dx=pose['bodyDeltaX']if walking else 0;dy=pose['bodyDeltaY']if walking else(-1 if action=='idle'and i else 0);legs=[];arms=[];out=Image.new('RGBA',(96,112));record=[]
 for j,side in enumerate(['L','R']):
  h,k,a=c['joints'][side];bb=parts[side+'shoe'].getbbox();rest=[(bb[0]+bb[2]-1)/2,bb[3]-1];offset=h[0]-[44,52][j]
  groundOffset=99-max(v[1]for v in pose['soleScreenLR']);sole=[pose['soleScreenLR'][j][0]+offset,pose['soleScreenLR'][j][1]+groundOffset]if walking else rest;hip=[h[0]+dx,h[1]+dy];knee=[K[d][i][j][0]+offset,round((hip[1]+sole[1]-3)/2+max(-2,min(2,(K[d][i][j][1]-80)*.25)))]if walking else[k[0],k[1]+dy];ankle=[sole[0],sole[1]-3];leg=Image.new('RGBA',(96,112));bone(leg,parts[side+'thigh'],h,k,hip,knee);bone(leg,parts[side+'shin'],k,a,knee,ankle);leg.alpha_composite(own_shoe(parts[side+'shoe'],sole,99-sole[1]if walking else 0));legs.append((sole[1],leg));record.append({'side':side,'hip':hip,'knee':knee,'sole':sole})
 for _,leg in sorted(legs,key=lambda r:r[0]):out.alpha_composite(leg)
 translate(out,parts['body'],dx,dy)
 for j,side in enumerate(['L','R']):
  a,b,w=c['arms'][side];shoulder=[a[0]+dx,a[1]+dy];wrist=[pose['handScreenLR'][j][0],pose['handScreenLR'][j][1]]if walking else[w[0],w[1]+dy]
  if action=='greet'and side=='R':wrist=[65+round(math.sin(i*math.tau/8)*2),45+round(math.cos(i*math.tau/8))]
  if action=='activity':
   wrist=[46 if side=='L'else 56,62+round(math.sin(i*math.tau/8))]
  if action=='activity':wrist[0]+=round(math.cos(i*math.tau/8))
  elbow=[round((shoulder[0]+wrist[0])/2)+(-2 if side=='L'else 2),round((shoulder[1]+wrist[1])/2)+2];arm=Image.new('RGBA',(96,112));bone(arm,parts[side+'upperarm'],a,b,shoulder,elbow);bone(arm,parts[side+'forearm'],b,w,elbow,wrist);arms.append((side,arm));record[j]['wrist']=wrist
 for side,arm in arms:out.alpha_composite(arm)
 if d=='back'and action=='activity':translate(out,parts['body'],dx,dy)
 return out,record

def profile(parts,c,d,i,action):
 sign=c['facing'];phase=i/8;walking=action=='walk';dy=-round(abs(math.sin(phase*math.tau)))if walking else(-1 if action=='idle'and i else 0);legs={};arms={};record=[]
 for side,offset in [('L',.5),('R',0)]:
  p=(phase+offset)%1;x=0;lift=0
  if walking:
   if p<=.5:x=11-44*p
   else:
    u=(p-.5)*2;x=-11*(2*u**3-3*u**2+1)+11*(-2*u**3+3*u**2)-22*(u**3-2*u**2+u)-22*(u**3-u**2);lift=math.sin(math.pi*u)*6
  h,k,a=c['joints'][side];bb=parts[side+'shoe'].getbbox();sole=[48+sign*x,99-round(lift)]if walking else[(bb[0]+bb[2]-1)/2,bb[3]-1];hip=[h[0],h[1]+dy];ankle=[sole[0],sole[1]-3];knee=ik(hip,ankle,math.dist(h,k),math.dist(k,a),-sign)if walking else[k[0],k[1]+dy];q=Image.new('RGBA',(96,112));bone(q,parts[side+'thigh'],h,k,hip,knee);bone(q,parts[side+'shin'],k,a,knee,ankle);q.alpha_composite(own_shoe(parts[side+'shoe'],sole));legs[side]=q;record.append({'side':side,'phase':p,'planted':walking and p<=.5,'sole':sole,'hip':hip,'knee':knee,'groundRelativeX':x,'lift':lift})
  a,b,w=c['arms'][side];swing=-x/11 if walking else 0;shoulder=[a[0],a[1]+dy];wrist=[w[0]+round(sign*swing*5),w[1]+dy-round(abs(swing))]
  if action=='greet'and side=='R':wrist=[48+sign*(14+round(math.sin(phase*math.tau)*2)),45+round(math.cos(phase*math.tau))]
  if action=='activity':wrist=[48+sign*(7 if side=='R'else 3),61+round(math.sin(phase*math.tau))]
  if action=='activity':wrist[0]+=round(math.cos(phase*math.tau))
  elbow=[round((shoulder[0]+wrist[0])/2),round((shoulder[1]+wrist[1])/2)+2];arm=Image.new('RGBA',(96,112));bone(arm,parts[side+'upperarm'],a,b,shoulder,elbow);bone(arm,parts[side+'forearm'],b,w,elbow,wrist);arms[side]=arm;record[-1]['wrist']=wrist
 out=Image.new('RGBA',(96,112));out.alpha_composite(legs['L']);out.alpha_composite(arms['L']);out.alpha_composite(legs['R']);translate(out,parts['body'],0,dy);out.alpha_composite(arms['R']);return out,record

def build(id,export=False):
 p=S/id;cfg=json.loads((p/'rig.json').read_text());frames={};poses=[]
 for d,c in cfg['views'].items():
  c['identity']=id;parts={q.stem:Image.open(q).convert('RGBA')for q in(p/'layers'/d).glob('*.png')}
  for action,count in [('idle',2),('walk',8),('greet',8),('activity',8)]:
   for i in range(count):
    name=f'{action}-{d}-{i}';im,land=(forward if d in ['front','back']else profile)(parts,c,d,i,action);
    if action=='activity'and d!='back'and(p/'activity-prop-native.png').exists():
     prop=Image.open(p/'activity-prop-native.png').convert('RGBA');anchor=[prop.width//2,prop.height-1];wrist=land[1]['wrist'];im.alpha_composite(prop,(round(wrist[0]-anchor[0]),round(wrist[1]-anchor[1])))
    frames[name]=im;poses.append({'frame':name,'landmarks':land})
 (p/'frames').mkdir(exist_ok=True)
 for n,q in frames.items():q.save(p/'frames'/f'{n}.png')
 (p/'pose-keys.json').write_text(json.dumps({'reference':'Approved Juni same-index numerical front/back landmarks, own-body knee retarget and a whole-pose grounded-sole offset for NEW NPCs only; approved44pxprofile Hermite. No player/pilot RGB copied; all four own source views independently illustrated','poses':poses},indent=2)+'\n')
 sheet=Image.new('RGBA',(768,528),(29,27,36,255));dr=ImageDraw.Draw(sheet)
 for row,d in enumerate(['front','back','left','right']):
  dr.text((2,row*132+2),f'{id} walk-{d} OWN illustrated layers',fill='white')
  for i in range(8):sheet.alpha_composite(frames[f'walk-{d}-{i}'],(i*96,row*132+20))
 sheet.convert('RGB').save(D/f'{id}-walk-native.png');sheet.resize((1536,1056),Image.Resampling.NEAREST).convert('RGB').save(D/f'{id}-walk-review-2x.png')
 seq=[]
 for i in range(8):
  q=Image.new('RGBA',(384,132),(29,27,36,255));dr=ImageDraw.Draw(q)
  for j,d in enumerate(['front','back','left','right']):q.alpha_composite(frames[f'walk-{d}-{i}'],(j*96,20));dr.text((j*96,2),d,fill='white')
  seq.append(q.resize((768,264),Image.Resampling.NEAREST))
 seq[0].save(D/f'{id}-walk-motion.webp',save_all=True,append_images=seq[1:],duration=140,loop=0,lossless=True)
 meta=json.loads((R/f'public/assets/npcs/phase3a/npc-{id}/atlas.json').read_text());assert set(frames)==set(meta['frames']);atlas=Image.new('RGBA',(768,1456))
 for n,q in frames.items():
  f=meta['frames'][n]['frame'];atlas.paste(q,(f['x'],f['y']));bb=q.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112,(id,n,bb)
 atlas.save(p/'candidate-atlas.png');frames['idle-front-0'].save(p/'candidate-preview-native.png')
 if export:
  import shutil
  for src,dst in [('candidate-atlas.png','atlas.png'),('candidate-preview-native.png','preview-native.png')]:shutil.copyfile(p/src,R/f'public/assets/npcs/phase3a/npc-{id}/{dst}')
 print(id,len(frames),'own-illustrated native cells;export',export)
if __name__=='__main__':
 for id in [v for v in sys.argv[1:]if v!='--export']:build(id,'--export'in sys.argv)
