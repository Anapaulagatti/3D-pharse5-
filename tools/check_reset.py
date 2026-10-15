"""Reset asset/collision/pixel contracts; aesthetic approval is a separate gate."""
from pathlib import Path
from PIL import Image
import os,json,hashlib,collections
R=Path(__file__).resolve().parents[1];S=R/'assets-src/reset-v2';O=R/'public-reset/assets/reset-v2';Q=R/os.environ.get('PIXEL_REPORT_DIR','quality-reports/pixel-reset-v2');Q.mkdir(parents=True,exist_ok=True)
manifest=json.loads((S/'manifest.json').read_text());worlds=json.loads((S/'worlds.json').read_text());maps=[];avatar_hashes=[];checks=[]
for r in manifest['files']:
 p=R/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
for k,w in worlds.items():
 d=O/k;m=json.loads((d/'plaza.json').read_text());assert m==json.loads((S/k/'plaza.tmj').read_text());assert m['tilewidth']==32 and m['tileheight']==32 and len(m['layers'])==4
 for l in m['layers']:
  if l['type']=='tilelayer':assert len(l['data'])==30*24 and all(0<=v<=32 for v in l['data'])
 solids=m['layers'][2]['objects'];assert len(solids)==w['collisionCount']
 x,y=w['spawn'];assert not any(o['x']<=x<=o['x']+o['width'] and o['y']<=y<=o['y']+o['height'] for o in solids)
 # Native-grid flood fill must connect spawn with the NPC vicinity and exits.
 def blocked(x,y):return any(o['x']-8<=x<=o['x']+o['width']+8 and o['y']-4<=y<=o['y']+o['height']+4 for o in solids)
 start=(round(x/8),round(y/8));seen={start};q=collections.deque([start])
 while q:
  x,y=q.popleft()
  for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 4<=nx<116 and 4<=ny<92 and (nx,ny) not in seen and not blocked(nx*8,ny*8):seen.add((nx,ny));q.append((nx,ny))
 assert any(abs(x*8-w['npc'][0])+abs(y*8-w['npc'][1])<45 for x,y in seen),('NPC blocked',k)
 assert len(seen)>1000,(k,len(seen))
 atlas=Image.open(d/'avatar.png').convert('RGBA');frames=json.loads((d/'avatar.json').read_text())['frames'];assert len(frames)==72
 for name,t in frames.items():
  f=t['frame'];assert (f['w'],f['h'])==(48,64) and not t['trimmed'];xx,yy=f['x'],f['y'];im=atlas.crop((xx,yy,xx+48,yy+64));source=Image.open(S/k/(name+'.png')).convert('RGBA');assert im.tobytes()==source.tobytes();assert set(im.getchannel('A').get_flattened_data())<={0,255}
  assert all(v==(0,0,0,0) for v in atlas.crop((xx-2,yy-2,xx+50,yy)).get_flattened_data())
 for dr in ['down','up','left','right']:
  variants={hashlib.sha256(Image.open(S/k/f'walk-{dr}-{f}.png').tobytes()).hexdigest() for f in range(8)};assert len(variants)>=6,(k,dr,len(variants))
 idle=Image.open(S/k/'idle-down-0.png').convert('RGBA');bbox=idle.getchannel('A').getbbox();assert bbox[3]-bbox[1]>=60 and bbox[2]-bbox[0]>=30,(k,bbox)
 for name in ['house','tree1','tree2','feature','kiosk','decor']:
  im=Image.open(d/(name+'.png')).convert('RGBA');assert len(set(im.get_flattened_data()))<=129
  assert im.getchannel('A').getextrema()==(0,255)
 maps.append(w['mapSha256']);avatar_hashes.append(hashlib.sha256(atlas.tobytes()).hexdigest());checks.append({'style':k,'objects':len(w['objects']),'colliders':len(solids),'reachable_8px_nodes':len(seen),'frames':72,'walk_distinct_min':6,'idle_bbox':bbox,'idle_css_height_at2x':(bbox[3]-bbox[1])*2,'ground_hash':hashlib.sha256((d/'tiles.png').read_bytes()).hexdigest()})
assert len(set(maps))==3 and len(set(avatar_hashes))==3
report={'status':'PASS','styles':checks,'files_verified':len(manifest['files']),'maps_independent':True,'source_masters_untouched':True,'important_limit':'Unique hashes/data do not substitute for human style differentiation/readability approval.'};(Q/'reset-asset-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
