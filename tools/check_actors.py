"""Validate every current actor source/runtime frame, palette, padding and authored motion."""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
from avatar_art import draw,composite
from guest_art import guest
R=Path(__file__).resolve().parents[1];S=R/'assets-src/actors';O=R/'public-unified/assets/actors';reports=[]
for actor in ['hero','sejong','jang','saimdang','yi']:
 m=json.loads((S/actor/'manifest.json').read_text());f=json.loads((S/actor/'atlas.json').read_text())['frames'];assert len(f)==m['frames'];assert m['frame']==[48,68] and m['anchor']==[24,64]
 for r in m['files']:assert hashlib.sha256((O/actor/r['path']).read_bytes()).hexdigest()==r['sha256'];assert (S/actor/r['path']).read_bytes()==(O/actor/r['path']).read_bytes()
 sheets={k:Image.open(S/actor/(k+'.png')).convert('RGBA') for k in m['layers']}
 for k,im in sheets.items():assert set(im.getchannel('A').get_flattened_data())<={0,255};assert len(set(im.get_flattened_data()))<=65,(actor,k,'palette')
 for key,info in f.items():
  b=info['frame'];x,y=b['x'],b['y'];expected=draw(key) if actor=='hero' else {'sprite':guest(actor,key)}
  for k,im in sheets.items():
   actual=im.crop((x,y,x+48,y+68));assert actual.tobytes()==expected[k].tobytes(),(actor,key,k,'source regeneration equality')
   edge=actual.getchannel('A');assert not any(edge.crop(z).getbbox() for z in [(0,0,48,1),(0,67,48,68),(0,0,1,68),(47,0,48,68)]),(actor,key,k,'clipped actor')
   g=im.crop((x-2,y-2,x+50,y+70)).getchannel('A');assert not any(g.crop(z).getbbox() for z in [(0,0,52,2),(0,70,52,72),(0,0,2,72),(50,0,52,72)]),(actor,key,k,'gutter')
 for dr in m['directions']:
  if actor=='hero':
   w=[composite(f'walk-{dr}-{i}').tobytes() for i in range(12)];r=[composite(f'run-{dr}-{i}').tobytes() for i in range(12)];assert len(set(w))>=10 and len(set(r))>=10;assert sum(a!=b for a,b in zip(w,r))>=10
  else:
   w=[guest(actor,f'walk-{dr}-{i}').tobytes() for i in range(12)];assert len(set(w))>=8,(actor,dr,'walk phases')
 if actor!='hero':assert guest(actor,'idle-down-0').crop((10,24,38,38)).tobytes()!=guest(actor,'wave-down-0').crop((10,24,38,38)).tobytes(),(actor,'neutral and happy face')
 reports.append({'actor':actor,'frames':len(f),'layers':len(sheets),'source_equals_runtime_and_regeneration':True,'binary_alpha':True,'max64colors_per_layer':True,'no_frame_clipping':True})
q=R/'.cache/current-qa';q.mkdir(parents=True,exist_ok=True);(q/'actors.json').write_text(json.dumps({'status':'PASS','actors':reports,'art_source':'code-drawn, no image model','limitation':'Not user visual approval or hardware FPS certification.'},indent=2)+'\n');print(json.dumps(reports))
