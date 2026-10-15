"""Export current actor source atlases and fixed-canvas runtime textures, no world edits."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib,shutil
from avatar_art import A,D,L,W,H,P,draw,composite
R=Path(__file__).resolve().parents[1];S=R/'assets-src/actors';O=R/'public-unified/assets/actors';CACHE=R/'.cache/actor-frames';S.mkdir(exist_ok=True,parents=True);O.mkdir(exist_ok=True,parents=True)
DURATIONS={'idle':[1800,70,70,450,450,1800],'wave':[80,80,100,120,130,110,100,140],'celebrate':[100,80,60,70,100,90,70,90,100,150],'pose':[100,100,150,350,150,150],'think':[100,100,120,150,500,150,120,140],'start':[40,40,40],'stop':[40,50,60],'turn':[40,40,40]}
def atlas_bundle(actor,actions,layers,render,master):
 src=S/actor;out=O/actor;src.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 keys=[f'{a}-{dr}-{i}' for dr in D for a,n in actions.items() for i in range(n)];cols=12;size=(cols*52,math.ceil(len(keys)/cols)*72);sheets={k:Image.new('RGBA',size) for k in layers};frames={}
 for idx,key in enumerate(keys):
  parts=render(key);x=(idx%cols)*52+2;y=(idx//cols)*72+2
  frames[key]={'frame':{'x':x,'y':y,'w':W,'h':H},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':W,'h':H},'sourceSize':{'w':W,'h':H}}
  for layer in layers:sheets[layer].alpha_composite(parts[layer],(x,y))
  # Temporary per-frame work/Forge inputs live outside tracked source tree.
  p=CACHE/actor/key.split('-')[0]/key.split('-')[1];p.mkdir(parents=True,exist_ok=True);master(key).save(p/(key.split('-')[-1].zfill(2)+'.png'))
 for k,im in sheets.items():im.save(src/(k+'.png'));im.save(out/(k+'.png'))
 atlas={'frames':frames,'meta':{'app':'Korean Arena native fixed-registration pipeline','size':{'w':size[0],'h':size[1]},'scale':'1'}}
 for p in [src/'atlas.json',out/'atlas.json']:p.write_text(json.dumps(atlas,separators=(',',':'))+'\n')
 for dr in D:master(f'idle-{dr}-0').save(src/f'master-{dr}.png')
 manifest={'id':actor,'art_source':'code','disclosure':'code-drawn, no image model','frame':[W,H],'anchor':[24,64],'visible_idle_height':54,'actions':actions,'directions':D,'layers':layers,'frames':len(keys),'durations_ms':DURATIONS,'locomotion':{'walk':{'stride_world':26.6666667,'speed_ref':60},'run':{'stride_world':44,'speed_ref':100}},'files':[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.iterdir()) if p.is_file()]}
 (src/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return manifest
if __name__=='__main__':
 m=atlas_bundle('hero',A,L,draw,composite)
 (S/'palette.json').write_text(json.dumps(list(P.values()),indent=2)+'\n')
 from guest_art import guest,N
 for actor in ['sejong','jang','saimdang','yi']:atlas_bundle(actor,N,['sprite'],lambda k,actor=actor:{'sprite':guest(actor,k)},lambda k,actor=actor:guest(actor,k))
 print('Hero exported',m['frames'],'registered frames x',len(L),'layers; source48x68 includes motion padding only.')
