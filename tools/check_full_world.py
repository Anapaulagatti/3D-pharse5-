"""Offline release guard: saved assets only, never invokes Forge, generation or network."""
from pathlib import Path
from PIL import Image
import hashlib,json,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/full-world'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proof=read(S/'preservation.json')
for p,h in proof['files'].items():assert sha(R/p)==h,('Approved prior source/art/test/lock changed',p)
receipts=read(S/'image-route.json');assert len(receipts)==6
for row in receipts:assert sha(S/row['raw'])==row['sha256']and row['paidProviderRequests']==0 and (S/row['prompt']).exists()
palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in read(R/'assets-src/seoul-production/palette/palette.json')['colors']}
props=list((S/'props').glob('*.png'));assert len(props)==32
for p in props+list((S/'terrain-native').glob('*.png')):
 im=Image.open(p).convert('RGBA');values=set(im.get_flattened_data());assert {q[3]for q in values}<={0,255},p;assert {q[:3]for q in values if q[3]}<=palette,p
b=read(S/'map/outdoor-bundle.json');w=read(S/'map/world.json');runtime=R/'public/review/full-world/world';t=read(runtime/'plaza.json')
assert [b['world']['width'],b['world']['height']]==[4352,4800]
assert len(b['objects'])==len(w['objects'])and len({o['id']for o in b['objects']})==len(b['objects'])
assert sha(runtime/'plaza.json')==w['mapSha256']
for key,p in b['props'].items():assert sha(S/'map'/p['image'])==p['sha256']and (runtime/f'{key}.png').read_bytes()==(S/'map'/p['image']).read_bytes(),key
actual=[(o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects']]
expected=[(o['x'],o['y'],o['w'],o['h'])for o in b['collision']['solids']];assert sorted(actual)==sorted(expected),'Phaser/Forge collision mismatch'
assert max(Image.open(S/'map/tiles.png').size)<=4096
for zone,path,dx,dy in [('heritage','north',1024,0),('namsan','park',0,2240)]:
 old=read(R/f'assets-src/living-korea/{path}/outdoor-bundle.json')
 for o in old['objects']:
  current=next(q for q in b['objects']if q['id']==f'{zone}-{o["id"]}');assert current['prop']==o['prop']and current['x']==o['x']+dx and current['y']==o['y']+dy and current['scale']==o['scale']
for name in ['world','room']:assert read(S/f'linked-{name}/nav-report.json')['status']=='pass'
roads=read(R/'docs/full-world/quality/road-clearance.json');assert roads['status']=='PASS'and not roads['failures']and roads['sourceBundleSha256']==sha(S/'map/outdoor-bundle.json')
for a in b['spawns']:
 x,y=a['x'],a['y'];assert not any(x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']for q in b['collision']['solids']),a
 assert all(math.hypot(x-q['circle'][0],y-q['circle'][1])>q['circle'][2]for q in b['portals']),('Arrival within trigger',a)
assert read(R/'assets-src/juni-animation/runtime.json')['frameCount']==144
print(json.dumps({'status':'PASS','protectedPriorFiles':len(proof['files']),'originalHostCalls':6,'paidProviderRoutes':0,'newFinishedPropComponents':len(props),'terrainSwatches':4,'world':[4352,4800],'props':len(b['objects']),'exactRuntimeColliders':len(actual),'publicPathSamples':roads['samples'],'retainedJuniFrames':144,'limits':['Numeric/source checks are not user visual approval','Raw Forge diagnostic failures/skips/boat-prop foot warning and inherited Juni motion warnings remain recorded','Physical mobile/Safari performance unmeasured']},ensure_ascii=False))
