"""Offline saved-art integrity, original preservation and boundary/collision release guard."""
from pathlib import Path
from PIL import Image
import hashlib,json
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
