"""Offline V3 release guard. Reads saved originals/exports; never generates or calls Forge/network."""
from pathlib import Path
from PIL import Image
import hashlib,json,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v3-final'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proof=read(S/'preservation.json')
for p,h in proof['files'].items():assert sha(R/p)==h,('Protected source/art/test/lock changed',p)
receipts=read(S/'image-route.json');assert len(receipts)==7
for row in receipts:assert sha(S/row['raw'])==row['sha256'] and row['paidProviderRequests']==0 and (S/row['prompt']).exists()
base=read(R/'assets-src/seoul-production/palette/palette.json')['colors'];colors=read(S/'palette/palette.json')['colors'];assert [q['hex'] for q in colors[:len(base)]]==[q['hex']for q in base]
palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in colors};props=list((S/'props').glob('*.png'));assert len(props)==32
for p in props+list((S/'terrain').glob('*.png'))+list((S/'prop-layers').glob('*.png')):
 im=Image.open(p).convert('RGBA');values=set(im.get_flattened_data());assert {q[3]for q in values}<={0,255},p;assert {q[:3]for q in values if q[3]}<=palette,p
 if p.parent.name=='props':
  bb=im.getbbox();assert bb and bb[0]>=2 and bb[1]>=2 and bb[2]<=im.width-2 and bb[3]<=im.height-2,('Native clipped prop',p)
b=read(S/'map/outdoor-bundle.json');w=read(S/'map/world.json');runtime=R/'public/review/v3-final/world';t=read(runtime/'plaza.json');assert [b['world']['width'],b['world']['height']]==[4352,4800]
assert len(b['objects'])==len(w['objects']) and len(b['objects'])>286 and len({o['id']for o in b['objects']})==len(b['objects'])
assert sha(runtime/'plaza.json')==w['mapSha256']
for key,p in b['props'].items():assert sha(S/'map'/p['image'])==p['sha256'] and (runtime/f'{key}.png').read_bytes()==(S/'map'/p['image']).read_bytes(),key
actual=[(o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects']];expected=[(o['x'],o['y'],o['w'],o['h'])for o in b['collision']['solids']];assert sorted(actual)==sorted(expected),'Phaser/Forge collision mismatch'
assert max(Image.open(S/'map/tiles.png').size)<=4096
assert (runtime/'tiles.png').read_bytes()==(S/'map/tiles.png').read_bytes()
assert all((S/'map'/q['manifest']).resolve().parent==(S/'map').resolve()for q in b['tilesets'])
assert all((S/'map'/q['data']).resolve().parent==(S/'map/layers').resolve()for q in b['layers']if q.get('kind')=='tiles')
assert (runtime/'minimap.png').is_file()and (runtime/'rf-prod-doors.png').is_file()
assert (S/'map/tiled/map.embedded.tmj').is_file()
for name in ['world','room']:assert read(S/f'{name}-navigation/nav-report.json')['status']=='pass'
roads=read(R/'docs/v3-final/quality/road-clearance.json');assert roads['status']=='PASS' and not roads['failures'] and roads['sourceBundleSha256']==sha(S/'map/outdoor-bundle.json')
for a in b['spawns']:
 x,y=a['x'],a['y'];assert not any(x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']for q in b['collision']['solids']),a
 assert all(math.hypot(x-q['circle'][0],y-q['circle'][1])>q['circle'][2]for q in b['portals']),('Arrival within trigger',a)
assert read(R/'assets-src/juni-animation/runtime.json')['frameCount']==144
print(json.dumps({'status':'PASS','protectedPriorFiles':len(proof['files']),'originalHostCalls':7,'paidProviderRoutes':0,'finishedPropComponents':len(props),'terrainSwatches':9,'world':[4352,4800],'props':len(b['objects']),'exactRuntimeColliders':len(actual),'publicPathSamples':roads['samples'],'retainedJuniFrames':144,'limits':['Source checks are not user visual approval','Raw extraction/terrain failures and inherited Juni warnings remain recorded','Physical mobile/Safari performance unmeasured']},ensure_ascii=False))
