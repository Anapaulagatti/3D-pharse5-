"""Validate actual Tiled objects, PNG grid/palettes, frame rects, provenance."""
from pathlib import Path
from PIL import Image
import json,hashlib,collections,os
R=Path(__file__).resolve().parents[1]; src=R/'assets-src';out=R/os.environ.get('PIXEL_REPORT_DIR','quality-reports/pixel-v3.1');out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((src/'manifest.json').read_text());m=json.loads((R/'public/assets/plaza.json').read_text());assert m==json.loads((src/'plaza.tmj').read_text());assert m['tilewidth']==m['tileheight']==32 and m['orientation']=='orthogonal'
assert len({l['name'] for l in m['layers']})==4
for l in m['layers']:
 if l['type']=='tilelayer':assert len(l['data'])==m['width']*m['height'] and all(isinstance(v,int) and 0<=v<=16 for v in l['data'])
solids=m['layers'][2]['objects'];assert all(o['type']=='solid' and o['width']>0 and o['height']>0 for o in solids)
sx,sy=json.loads((src/'layout.json').read_text())['spawn'];assert not any(o['x']<=sx<=o['x']+o['width'] and o['y']<=sy<=o['y']+o['height'] for o in solids)
# Flood-fill reachable tile centres with actual authoring collision footprints.
w,h=m['width'],m['height'];blocked=lambda x,y:any(o['x']-8<=x<=o['x']+o['width']+8 and o['y']-5<=y<=o['y']+o['height']+5 for o in solids)
queue=collections.deque([(12,11)]);seen={(12,11)}
while queue:
 x,y=queue.popleft()
 for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 1<=nx<w-1 and 1<=ny<h and (nx,ny) not in seen and not blocked(nx*32+16,ny*32+16):seen.add((nx,ny));queue.append((nx,ny))
assert (13,10) in seen and (12,17) in seen,'NPC/bridge route inaccessible'
for a in manifest['assets']:
 f=R/a['path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256'];assert a['provenance']=='ORIGINAL_CODE_AUTHORED' and a['license']=='MIT'
checks=[]
for style in 'ABC':
 d=R/'public/assets'/style;atlas=Image.open(d/'avatar.png').convert('RGBA');j=json.loads((d/'avatar.json').read_text());assert len(j['frames'])==48
 for name,meta in j['frames'].items():
  f=meta['frame'];assert f['w']==48 and f['h']==64 and not meta['trimmed'];x,y=f['x'],f['y'];assert x>=2 and y>=2 and x+48<atlas.width and y+64<atlas.height
  im=atlas.crop((x,y,x+48,y+64));pixels=list(im.get_flattened_data());assert set(v[3] for v in pixels)<={0,255};assert all(v==(0,0,0,0) for v in pixels if v[3]==0)
  assert list(atlas.crop((x-2,y-2,x+50,y)).get_flattened_data())==[(0,0,0,0)]*104
  assert im.tobytes()==Image.open(src/style/(name+'.png')).convert('RGBA').tobytes()
 for dr in ['up','down','left','right']:
  hashes={hashlib.sha256(Image.open(src/style/f'walk-{dr}-{n}.png').tobytes()).hexdigest() for n in range(6)};assert len(hashes)>=4,'Imperceptible gait'
 for p in (src/style).glob('*.png'):
  im=Image.open(p);assert im.mode=='P';assert len(im.getcolors() or [])<=33
 checks.append({'style':style,'frames':48,'walk_distinct_min':4,'palette_limit':32,'binary_alpha':True,'atlas_source_match':True,'gutter':2})
report={'status':'PASS','map_layers':4,'collision_objects':len(solids),'reachable_tiles':len(seen),'styles':checks,'assets_hash_verified':len(manifest['assets']),'important_limit':'Geometric/source QA; visual approval is separate.'};(out/'asset-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
