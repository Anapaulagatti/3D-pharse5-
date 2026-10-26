"""Offline authored PNG-layer animation; runtime remains the accepted controller.
Layer masks and joint keys are editable production sources, never generated gameplay bones.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase1b';D=R/'docs/phase1b'
def layer(im,poly):
 m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([tuple(x)for x in poly],fill=255);a=np.array(im);a[:,:,3]=np.minimum(a[:,:,3],np.array(m));return Image.fromarray(a)
def bone(out,im,a,b,c,d):
 # Inverse affine maps the authored segment onto an explicitly keyed projected bone.
 ax,ay=a;bx,by=b;cx,cy=c;dx,dy=d;ux,uy=bx-ax,by-ay;vx,vy=dx-cx,dy-cy
 l=math.hypot(ux,uy);n=math.hypot(vx,vy)
 if n<.1:return
 # Perpendicular width stays native; longitudinal projection changes only limb pose.
 A=np.array([[vx/n,-vy/n],[vy/n,vx/n]])@np.diag([n/l,1])@np.array([[ux/l,uy/l],[-uy/l,ux/l]])
 inv=np.linalg.inv(A);off=np.array([ax,ay])-inv@np.array([cx,cy]);mat=(*inv[0],off[0],*inv[1],off[1])
 out.alpha_composite(im.transform(out.size,Image.Transform.AFFINE,mat,resample=Image.Resampling.NEAREST))
def translate(out,im,x,y):out.alpha_composite(im,(round(x),round(y)))
def render_front(parts,config,phase,action='walk'):
 out=Image.new('RGBA',(96,112));r=action=='run';t=phase*math.tau;s=math.sin(t);bob=round(-abs(math.sin(t))* (2 if r else 1));steps=[]
 if action=='idle':bob=-round((1-math.cos(t))/2)
 for side,offset in [('L',0),('R',math.pi)]:
  h,k,a=config['joints'][side];q=t+offset;v=math.cos(q);lift=max(0,-math.sin(q));amp=5 if r else 3
  ankle=[a[0]+config.get('footInsets',{}).get(side,0),round(a[1]+v*amp-amp)]
  knee=[k[0]+round(math.sin(q)*1.5),round((h[1]+bob+ankle[1])/2)]
  if action in ['idle','wave']:ankle=[a[0]+config.get('footInsets',{}).get(side,0),a[1]];knee=[k[0],k[1]+bob]
  steps.append((ankle[1],side,h,k,a,ankle,knee))
 # Higher/back foot first; genuine opposite-leg phases, never whole-portrait motion.
 for _,side,h,k,a,ankle,knee in sorted(steps):
  hip=[h[0],h[1]+bob];bone(out,parts[side+'thigh'],h,k,hip,knee);bone(out,parts[side+'shin'],k,a,knee,ankle);translate(out,parts[side+'shoe'],ankle[0]-a[0],ankle[1]-a[1])
 translate(out,parts['body'],0,bob)
 for side,offset in [('L',0),('R',math.pi)]:
  a,b,c=config['arms'][side];q=t+offset;v=math.cos(q);shoulder=[a[0],a[1]+bob]
  elbow=[b[0]+round((-1 if side=='L'else 1)*(-1+abs(v))),b[1]+bob+round(v*1.5)]
  wrist=[c[0]+round((2 if side=='L'else -2)),c[1]+bob+round(v*(5 if r else 3))]
  if action=='idle':elbow=[b[0],b[1]+bob];wrist=[c[0]+(2 if side=='L'else -2),c[1]+bob]
  if action=='wave'and side=='R':elbow=[a[0]+7,a[1]+2];wrist=[a[0]+8+round(math.sin(t)*3),a[1]-9]
  if action=='celebrate':
   sign=-1 if side=='L'else 1;elbow=[a[0]+sign*7,a[1]-4];wrist=[a[0]+sign*(10+round(math.sin(t))),a[1]-15+round(math.cos(t)*2)]
  bone(out,parts[side+'upperarm'],a,b,shoulder,elbow)
  bone(out,parts[side+'forearm'],b,c,elbow,wrist)
 return out

def pilot(id):
 p=S/id;cfg=json.loads((p/'rig.json').read_text());im=Image.open(p/'native/front.png').convert('RGBA');parts={name:layer(im,poly)for name,poly in cfg['front']['masks'].items()};o=p/'layers/front';o.mkdir(parents=True,exist_ok=True)
 for name,q in parts.items():q.save(o/f'{name}.png')
 frames=[render_front(parts,cfg['front'],i/8)for i in range(8)];out=p/'pilot';out.mkdir(exist_ok=True);board=Image.new('RGBA',(768,112))
 for i,q in enumerate(frames):q.save(out/f'walk-front-{i}.png');board.alpha_composite(q,(i*96,0))
 board.save(out/'walk-front-native.png');bg=Image.new('RGBA',board.size,(30,28,38,255));bg.alpha_composite(board);bg.resize((1536,224),Image.Resampling.NEAREST).save(out/'walk-front-2x.png')
 previews=[]
 for q in frames:
  bg=Image.new('RGBA',q.size,(30,28,38,255));bg.alpha_composite(q);previews.append(bg.resize((384,448),Image.Resampling.NEAREST).convert('RGB'))
 previews[0].save(out/'walk-front-review.gif',save_all=True,append_images=previews[1:],duration=92,loop=0)
 hashes=[hashlib.sha256(q.tobytes()).hexdigest()for q in frames];report={'character':id,'frames':8,'uniquePixelFrames':len(set(hashes)),'frameHashes':hashes,'cell':[96,112],'anchor':[48,100],'method':'independently authored image layers, keyed opposite-limb pose interpolation, offline nearest-neighbor bake','technical':'PASS'if len(set(hashes))==8 else'FAIL','visual':'PENDING native and animated review; not registry-unlocked','contactPhases':[0,4],'halfCyclePixelChanges':[int(np.any(np.array(frames[i])!=np.array(frames[i+4]),2).sum())for i in range(4)]};(out/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

def ik(hip,foot,l1,l2,sign):
 dx,dy=foot[0]-hip[0],foot[1]-hip[1];dist=max(.1,min(math.hypot(dx,dy),l1+l2-.1));base=math.atan2(dy,dx);angle=math.acos(max(-1,min(1,(l1*l1+dist*dist-l2*l2)/(2*l1*dist))));a=base+sign*angle;return [round(hip[0]+math.cos(a)*l1),round(hip[1]+math.sin(a)*l1)]
def render_side(parts,cfg,phase,action='walk'):
 out=Image.new('RGBA',(96,112));t=phase*math.tau;r=action=='run';sign=cfg['facing'];bob=round(-abs(math.sin(t))*(2 if r else 1));layers=[]
 if action=='idle':bob=-round((1-math.cos(t))/2)
 for side,offset in [('L',0),('R',math.pi)]:
  h,k,a=cfg['joints'][side];q=t+offset;foot=[cfg['groundX']+round(math.cos(q)*cfg['strideAmplitude']['run'if r else'walk']),cfg['groundY'][side]-round(max(0,math.sin(q))*(10 if r else 5))-(round(abs(math.sin(t))*3)if r else 0)];hip=[h[0],h[1]+bob]
  if action=='idle':foot=[cfg['groundX'],cfg['groundY'][side]]
  knee=ik(hip,foot,math.dist(h,k),math.dist(k,a),-sign)
  layers.append((side,hip,knee,foot,h,k,a))
 # Far leg and arm, torso, near leg and arm keep correct profile ownership.
 for side,hip,knee,foot,h,k,a in layers:
  bone(out,parts[side+'thigh'],h,k,hip,knee);bone(out,parts[side+'shin'],k,a,knee,foot);translate(out,parts[side+'shoe'],foot[0]-a[0],foot[1]-a[1])
 translate(out,parts['body'],0,bob)
 for side in ['L','R']:
  if side+'forearm'not in parts:continue
  a,b,c=cfg['arms'][side];w=math.cos(t+(0 if side=='L'else math.pi));elbow=[b[0],b[1]+bob];wrist=[c[0]+round(w*(7 if r else 4)),c[1]+bob-round(abs(w)*2)]
  if action=='idle':wrist=[c[0],c[1]+bob]
  bone(out,parts[side+'forearm'],b,c,elbow,wrist)
 return out

def complete(id):
 p=S/id;cfg=json.loads((p/'rig.json').read_text());frames={};clips={};stats=[]
 for direction in ['front','back','left','right']:
  conf=cfg[direction];im=Image.open(p/'native'/f'{direction}.png').convert('RGBA')
  for patch in conf.get('clothRecovery',[]):
   src,dst=patch['source'],patch['target'];piece=im.crop(tuple(src));im.alpha_composite(piece,tuple(dst))
  parts={name:layer(im,poly)for name,poly in conf['masks'].items()}
  # Forearms use original unpatched authored pixels.
  original=Image.open(p/'native'/f'{direction}.png').convert('RGBA')
  for name in parts:
   if 'arm'in name:parts[name]=layer(original,conf['masks'][name])
  parts['body']=layer(original,conf['masks']['body'])
  o=p/'layers'/direction;o.mkdir(parents=True,exist_ok=True)
  for name,q in list(parts.items()):
   if direction in ['left','right']and name in ['Lthigh','Lshin','Lshoe']:
    a=np.array(q);a[:,:,:3]=np.rint(a[:,:,:3].astype(float)*.68).astype('uint8');q=Image.fromarray(a);parts[name]=q
   q.save(o/f'{name}.png')
  renderer=render_front if direction in ['front','back']else render_side
  def add(action,seq,durations,loop):
   names=[]
   for i,q in enumerate(seq):
    n=f'{action}-{direction}-{i}';frames[n]=q;names.append(n)
   clips[f'{action}-{direction}']={'frames':names,'durationsMs':durations,'loop':loop}
  for action in ['walk','run']:
   seq=[renderer(parts,conf,i/8,action)for i in range(8)];add(action,seq,[92 if action=='walk'else 80]*8,True)
  # Rest pose lowers outstretched master arms through the same authored limb joints.
  idle=[renderer(parts,conf,q,'idle')for q in [0,.5]]
  add('idle',idle,[600,600],True)
  for action,phases in [('start',[.25,.18,.08]),('stop',[.08,.18,.25])]:add(action,[renderer(parts,conf,q,'walk')for q in phases],[55]*3,False)
  if direction=='front':
   for action in ['wave','celebrate']:add(action,[render_front(parts,conf,i/8,action)for i in range(8)],[100]*8,False)
 # Direction changes explicitly reuse independently authored directional poses.
 for source in ['front','back','left','right']:
  for target in ['front','back','left','right']:
   if source==target:continue
   opposite={('front','back'),('back','front'),('left','right'),('right','left')}
   dirs=[source]+(['right'if source in ['front','back']else'front']if(source,target)in opposite else[])+[target]
   clips[f'turn-{source}-{target}']={'frames':[f'idle-{d}-0'for d in dirs],'durationsMs':[45]*len(dirs),'loop':False}
 # Clips/frames stay explicit sources; atlases have no trimming or arbitrary pivots.
 native=p/'frames';native.mkdir(exist_ok=True)
 for old in native.glob('*.png'):
  if old.stem not in frames:old.unlink()
 for n,q in frames.items():q.save(native/f'{n}.png')
 cols=12;rows=math.ceil(len(frames)/cols);atlas=Image.new('RGBA',(cols*96,rows*112));data={}
 for i,(n,q)in enumerate(frames.items()):
  x,y=i%cols*96,i//cols*112;atlas.alpha_composite(q,(x,y));data[n]={'frame':{'x':x,'y':y,'w':96,'h':112},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':96,'h':112},'sourceSize':{'w':96,'h':112}}
 out=R/'public/assets/characters'/id;out.mkdir(exist_ok=True,parents=True);atlas.save(out/'atlas.png');(out/'atlas.json').write_text(json.dumps({'frames':data,'meta':{'app':'Korean Arena Phase1B offline authored layers','image':'atlas.png','format':'RGBA8888','size':{'w':atlas.width,'h':atlas.height},'scale':'1'}},indent=2)+'\n');frames['idle-front-0'].save(out/'preview-native.png');(p/'clips.json').write_text(json.dumps(clips,indent=2)+'\n')
 for clip,row in clips.items():
  seq=[frames[n]for n in row['frames']];unique=len({hashlib.sha256(q.tobytes()).hexdigest()for q in seq});boxes=[q.getbbox()for q in seq];alpha=set(np.unique(np.array(q)[:,:,3]).tolist()[0]for q in seq)
  if clip.startswith(('walk-','run-')):assert unique==8,(id,clip,unique)
  assert all(b and b[0]>0 and b[1]>0 and b[2]<96 and b[3]<112 for b in boxes),(id,clip,boxes)
  stats.append({'clip':clip,'frames':len(seq),'uniquePixelFrames':unique,'bounds':boxes})
 (p/'pack-qa.json').write_text(json.dumps({'id':id,'frameCount':len(frames),'native':[96,112],'anchor':[48,100],'clips':stats,'authorship':'host-image directional source; explicit offline PNG-layer rig and pose keys; no runtime skeletal renderer','humanArtApproval':'PENDING'},indent=2)+'\n')
 print(id,len(frames),'frames',len(clips),'clips')

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('character',choices=['haneul','bomi','minjun'])
 parser.add_argument('--pilot',action='store_true')
 args=parser.parse_args()
 (pilot if args.pilot else complete)(args.character)
