from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b';H=D/'history/pre-opposing-profile';ids=['sori','jiwon','nari','taeyang','yuna','hyunwoo'];rows=[];board=Image.new('RGBA',(768,792),(29,28,36,255));dr=ImageDraw.Draw(board)
for row,id in enumerate(ids):
 root=R/f'assets-src/characters/phase2b/{id}';cfg=json.loads((root/'rig.json').read_text());old=Image.open(H/id/'atlas.png').convert('RGBA');meta=json.loads((H/id/'atlas.json').read_text())['frames'];outside=0;changed=0;frontback=0;phase=[]
 for name,f in meta.items():
  r=f['frame'];a=np.array(old.crop((r['x'],r['y'],r['x']+96,r['y']+112)));b=np.array(Image.open(root/'frames'/f'{name}.png').convert('RGBA'));delta=np.any(a!=b,2)
  if '-left-'not in name and '-right-'not in name:frontback+=int(delta.sum())
  else:
   forbidden=delta.copy();forbidden[58:82,30:68]=False;outside+=int(forbidden.sum());changed+=int(delta.sum())
 assert frontback==0 and outside==0
 for view in ['left','right']:
  for action,amp in [('walk',4),('run',7)]:
   for i in range(8):
    t=i*math.tau/8+math.pi;foot=round(math.cos(t)*cfg[view]['strideAmplitude'][action]);hand=round(-math.cos(t)*amp);assert foot*hand<=0
    phase.append({'view':view,'action':action,'frame':i,'nearFootXAboutStrideCenter':foot,'nearWristXAboutRest':hand,'opposesOrPassing':True})
 for col,name in enumerate(['walk-left-0','walk-left-4','run-right-0','run-right-4']):
  r=meta[name]['frame'];a=old.crop((r['x'],r['y'],r['x']+96,r['y']+112));b=Image.open(root/'frames'/f'{name}.png');x=192*col;y=row*132;board.alpha_composite(a,(x,y+20));board.alpha_composite(b,(x+96,y+20));dr.text((x+2,y+3),id+' '+name+' old/new',fill='white')
 rows.append({'id':id,'changedProfilePixels':changed,'changedPixelsOutsideForearmEnvelope':outside,'frontBackChangedPixels':frontback,'profilePhases':phase,'beforeAtlasSHA256':hashlib.sha256((H/id/'atlas.png').read_bytes()).hexdigest(),'finalAtlasSHA256':hashlib.sha256((R/f'public/assets/characters/{id}/atlas.png').read_bytes()).hexdigest()})
board.save(D/'profile-forearm-before-after-source-native.png');board.resize((1536,1584),Image.Resampling.NEAREST).save(D/'profile-forearm-before-after-source-review-2x.png');(D/'profile-arm-correction.json').write_text(json.dumps({'method':'Before/after source-frame comparison from archived pre-correction atlases, no existing approved identity changes. Signed native near-foot/near-wrist targets are opposite; profile limb interpolation only, not runtime rescaling. Every actual gait also captured in Phaser.','sourceOnlyComparison':True,'rows':rows},indent=2)+'\n');print('Six new profile forearm corrections:0 front/back or outside-owned-region changes')
