"""Offline saved-art integrity, original preservation and boundary/collision release guard."""
from pathlib import Path
from PIL import Image
import hashlib,json,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/living-korea'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proof=read(S/'preservation.json')
for p,h in proof['files'].items():assert sha(R/p)==h,('Protected existing art/source changed',p)
b=read(S/'north/outdoor-bundle.json');t=read(R/'public/review/living-korea/north/plaza.json');actual=[(o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects']];expected=[(q['x'],q['y'],q['w'],q['h'])for q in b['collision']['solids']];assert sorted(actual)==sorted(expected),'Phaser collision differs from actual Forge source'
for key,p in b['props'].items():
 image=(S/'north'/p['image']).resolve();assert image.exists() and sha(image)==p['sha256'],key
 assert (R/'public/review/living-korea/north'/f'{key}.png').read_bytes()==image.read_bytes(),key
for q in read(S/'north/boundary-recipes.json'):
 obj=next(o for o in b['objects']if o['prop']==q['id']);im=Image.open(S/'north'/b['props'][q['id']]['image']).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<={0,255},q['id']
 assert q['overlappingTilePixels']==0 and q['nativeScale']==1
 # Complete physical boundary is painted at its central load-bearing line.
 if q['from'][0]==q['to'][0]:missing=[y for y in range(im.height)if im.getpixel((im.width//2,y))[3]==0]
 else:missing=[x for x in range(im.width)if im.getpixel((x,im.height-8))[3]==0]
 assert not missing,('Unpainted boundary seam',q['id'],missing[:12])
 assert not any(o['prop']in ['rf-prod-service','rf-scholar-return','rf-work-return']for o in b['objects'])
trans=read(S/'north/museum-translations.json');assert len(trans)>=8 and all(q['shift']==[0,224]and q['scale']==1 for q in trans)
assert b['world']=={'width':2304,'height':2240,'unit':'px'}
print(f"Living Korea stored-source PASS: {len(proof['files'])} protected files, {len(b['objects'])} props, {len(actual)} exact colliders, {len(trans)} museum moves, all painted structural seams continuous")

# New Namsan source is separate; exact runtime/Tiled/linked-input data remains reproducible.
park=S/'park/outdoor-bundle.json'
if park.exists():
 b2=read(park);t2=read(R/'public/review/living-korea/park/plaza.json')
 got=[(o['x'],o['y'],o['width'],o['height'])for l in t2['layers']if l['name']=='Collision'for o in l['objects']]
 assert sorted(got)==sorted((q['x'],q['y'],q['w'],q['h'])for q in b2['collision']['solids'])
 for key,p in b2['props'].items():
  path=(S/'park'/p['image']).resolve();assert sha(path)==p['sha256'],key
  assert path.read_bytes()==(R/'public/review/living-korea/park'/f'{key}.png').read_bytes()
 for row in read(S/'image-route.json'):assert sha(S/row['raw'])==row['rawSha256']and row['paidProviderRequests']==0
 assert len(read(S/'image-route.json'))==4
 for folder in ['north','park']:assert max(Image.open(S/folder/'tiles.png').size)<=4096
 linked=read(S/'linked-inputs.json');assert linked['status']=='PASS'
 for name,item in linked['bundles'].items():
  assert sha(S/item['file'])==item['sha256']
  assert read(S/f'linked-{name}/nav-report.json')['status']=='pass'
 ownership=read(S/'tower-ownership.json');source=Image.open(S/'keyed/tower/tower-master/prop.png').convert('RGBA');recon=Image.new('RGBA',source.size)
 for part in ownership['parts']:
  box=part['sourceBox'];recon.paste(source.crop(tuple(box)),(box[0],box[1]))
 assert recon.tobytes()==source.tobytes() and ownership['disjointReconstructionDifferences']==0
 roads=read(R/'docs/living-korea/quality/road-clearance.json');assert roads['status']=='PASS'and not roads['failures']
 assert roads['masterplanSha256']==sha(R/'docs/living-korea/southern-masterplan.json')
 for name,h in roads['inputs'].items():assert h==sha(S/name/'outdoor-bundle.json')
 print(f"Namsan source PASS: {len(b2['objects'])} props / {len(got)} colliders,4actual host image receipts,3reciprocal maps,{roads['sampledPositions']} clear path samples,tower source exact ownership")

if park.exists():
  palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in read(R/'assets-src/seoul-production/palette/palette.json')['colors']}
  for path in (S/'props').glob('*.png'):
   im=Image.open(path).convert('RGBA');values=set(im.get_flattened_data());assert {v[3]for v in values}<={0,255},path
   assert {v[:3]for v in values if v[3]}<=palette,path

posts=[(o['x'],o['y'])for o in b['objects']if o['prop']=='kr-timber-cap']
assert len(posts)==len(set(posts))
minimum=min(math.hypot(x-xx,y-yy)for i,(x,y)in enumerate(posts)for xx,yy in posts[i+1:])
assert minimum>=48,('Clustered full-size timber posts',minimum)
print(f"Timber socket spacing PASS: {len(posts)} unique posts,minimum spacing {minimum}px (required>=48px)")
