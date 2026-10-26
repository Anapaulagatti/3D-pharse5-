"""Versioned authoring of NEW Phase2A identities; never writes approved base assets."""
from pathlib import Path
import sys,json,math,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2a';D=R/'docs/phase2a';D.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'tools/phase1b'))
from animate import bone,translate,layer
T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
def prepare(id):
 spec=importlib.util.spec_from_file_location('p1b_prepare',R/'tools/phase1b/prepare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.S=S;m.prepare(id)
def rig(id):
 cfg=json.loads((R/'assets-src/characters/phase1b/haneul/rig.json').read_text())
 for d in ['front','back']:
  for side in ['L','R']:
   a,b,w=cfg[d]['arms'][side];b[1]=62;w[1]=72
   poly=cfg[d]['masks'][side+'forearm'];cfg[d]['masks'][side+'forearm']=[[x,y-4]for x,y in poly]
   cfg[d]['masks'][side+'upperarm']=[[x,min(y,65)]for x,y in cfg[d]['masks'][side+'upperarm']]
 for d in ['left','right']:
  im=Image.open(S/id/'native'/f'{d}.png').convert('RGBA')
  for side in ['L','R']:
   shoe=layer(im,cfg[d]['masks'][side+'shoe']);bb=shoe.getbbox();a=cfg[d]['joints'][side][2];cfg[d]['groundY'][side]=a[1]+99-(bb[3]-1)
 (S/id/'rig.json').write_text(json.dumps(cfg,indent=2)+'\n')
def front(parts,c,pose):
 out=Image.new('RGBA',(96,112));dx=pose.get('bodyDeltaX',0);dy=pose['bodyDeltaY'];steps=[]
 for side,sole in zip(['L','R'],pose['soleScreenLR']):
  h,k,a=c['joints'][side];box=parts[side+'shoe'].getbbox();sole0=[round((box[0]+box[2]-1)/2),box[3]-1];delta=[sole[0]-sole0[0],sole[1]-sole0[1]];ankle=[a[0]+delta[0],a[1]+delta[1]];hip=[h[0]+dx,h[1]+dy];knee=[round((hip[0]+ankle[0])/2)+(-1 if side=='L'else 1),round((hip[1]+ankle[1])/2)];steps.append((sole[1],side,h,k,a,hip,knee,ankle,delta))
 for _,side,h,k,a,hip,knee,ankle,delta in sorted(steps):
  bone(out,parts[side+'thigh'],h,k,hip,knee);bone(out,parts[side+'shin'],k,a,knee,ankle);translate(out,parts[side+'shoe'],*delta)
 translate(out,parts['body'],dx,dy)
 for side,hand in zip(['L','R'],pose['handScreenLR']):
  a,b,w=c['arms'][side];shoulder=[a[0]+dx,a[1]+dy];elbow=[round((shoulder[0]+hand[0])/2)+(-3 if side=='L'else 3),round((shoulder[1]+hand[1])/2)+2];bone(out,parts[side+'upperarm'],a,b,shoulder,elbow);bone(out,parts[side+'forearm'],b,w,elbow,hand)
 return out

def finish(id):
 import animate
 animate.S=S;animate.D=D
 animate.complete(id)
 p=S/id;cfg=json.loads((p/'rig.json').read_text());pub=R/'public/assets/characters'/id;atlas=Image.open(pub/'atlas.png').convert('RGBA');meta=json.loads((pub/'atlas.json').read_text())['frames']
 for key,poses in T.items():
  d=key.split('-')[1];parts={q.stem:Image.open(q).convert('RGBA')for q in(p/'layers'/d).glob('*.png')}
  for pose in poses:
   name=f'{key}-{pose["frame"]}';im=front(parts,cfg[d],pose);im.save(p/'frames'/f'{name}.png');f=meta[name]['frame'];atlas.paste(im,(f['x'],f['y']))
 atlas.save(pub/'atlas.png')
 frames={q.stem:Image.open(q).convert('RGBA')for q in(p/'frames').glob('*.png')};clips=json.loads((p/'clips.json').read_text());rows=[]
 for key,clip in clips.items():
  seq=[frames[n]for n in clip['frames']];unique=len({im.tobytes()for im in seq});assert not key.startswith(('walk-','run-'))or unique==8
  for im in seq:
   bb=im.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112,(id,key,bb);assert set(np.unique(np.array(im)[:,:,3]))<={0,255}
  rows.append({'clip':key,'count':len(seq),'distinct':unique,'bounds':[im.getbbox()for im in seq]})
 (p/'pack-qa.json').write_text(json.dumps({'id':id,'frameCount':len(frames),'native':[96,112],'anchor':[48,100],'clips':rows,'authoritative':'Final corrected pose pack; not pre-retarget intermediate statistics','humanArtApproval':'PENDING'},indent=2)+'\n')
 (p/'native-validation.json').write_text(json.dumps({'id':id,'frameCount':len(frames),'clips':rows,'native':[96,112],'anchor':[48,100],'JuniFrontBackTemplate':'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json','sourceArtwork':'host_image; independent identity turnaround, not generated animation sheet','animation':'Existing validated own-PNG-layer workflow, explicit Juni landmarks for front/back, native contact IK for profiles; no runtime skeleton','humanArtApproval':'PENDING'},indent=2)+'\n')
 for action in ['walk','run']:
  board=Image.new('RGBA',(768,528),(29,28,36,255));draw=ImageDraw.Draw(board)
  for row,d in enumerate(['front','back','left','right']):
   for i in range(8):board.alpha_composite(frames[f'{action}-{d}-{i}'],(i*96,row*132+20));draw.text((i*96+2,row*132+3),f'{action}-{d}-{i}',fill='white')
  board.save(D/f'{id}-{action}-native.png');board.resize((1536,1056),Image.Resampling.NEAREST).save(D/f'{id}-{action}-review-2x.png')
  seq=[]
  for i in range(8):
   q=Image.new('RGBA',(384,132),(29,28,36,255));dr=ImageDraw.Draw(q)
   for col,d in enumerate(['front','back','left','right']):q.alpha_composite(frames[f'{action}-{d}-{i}'],(col*96,20));dr.text((col*96+2,3),d,fill='white')
   seq.append(q.resize((768,264),Image.Resampling.NEAREST))
  seq[0].save(D/f'{id}-{action}-motion.png',save_all=True,append_images=seq[1:],duration=92 if action=='walk'else 80,loop=0,disposal=0,blend=0)
 print(id,'final112 frames;8 directions x8 distinct gait poses; native checks PASS')
if __name__=='__main__':
 id=sys.argv[1];assert id in ['ara','doyun'];prepare(id);rig(id);finish(id)
