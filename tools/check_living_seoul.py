"""Offline integrity/navigation/export/preservation gate; no optional tool or generation."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];S=R/'assets-src/living-seoul'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
proof=read(S/'preserved-baseline.json')
assert proof['west_ground_equal'] and proof['west_objects_equal']
for p in proof['preserved']:assert sha(R/p['path'])==p['sha256'],p['path']
route=read(S/'image-route.json');assert len(route['calls'])==3 and route['paid_api_requests']==0
for path,h in route['hashes'].items():assert sha(S/path)==h,path
checks=[]
for name in ['outdoor','room']:
    b=read(S/f'{name}-bundle.json');D=R/f'public/review/living-seoul/{name}'
    for key,p in b['props'].items():
        assert sha(S/p['image'])==p['sha256']==sha(D/f'{key}.png'),key
        im=Image.open(S/p['image']).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<={0,255}
        assert im.getbbox() and im.getbbox()[0]>0 and im.getbbox()[1]>0
        assert im.getbbox()[2]<im.width and im.getbbox()[3]<im.height
    nav=read(S/name/'linked-navigation/nav-report.json');assert nav['status']=='pass' and not nav['problems']
    assert nav['inputs'][0]['sha256']==sha(S/f'{name}-bundle.json')
    for i in nav['inputs']:assert sha(S/name/'linked-navigation'/i['path'])==i['sha256'],i['path']
    assert all(c['status']=='pass' for c in nav['checks']),nav['checks']
    exported=read(S/name/'tiled/map.embedded.tmj');runtime=read(D/'plaza.json')
    a=[o for l in exported['layers'] if l['name']=='collision' for o in l['objects'] if o['type']=='solid']
    z=next(l for l in runtime['layers'] if l['name']=='Collision')['objects']
    assert z[:len(a)]==a
    assert read(S/f'{name}-world.json')['mapSha256']==sha(D/'plaza.json')
    for l in runtime['layers']:
        if l['type']=='tilelayer':assert l==next(e for e in exported['layers'] if e['name']==l['name'])
    checks.append({'map':name,'targets':len(nav['targets']),'tiledSolids':len(a),'props':len(b['objects']),'linkedNavigation':'pass'})
assert ImageChops.difference(Image.open(S/'room-base.png'),Image.open(R/'public/review/living-seoul/room/room-base.png')).getbbox(alpha_only=False) is None
print(json.dumps({'status':'PASS','preservedFiles':len(proof['preserved']),'maps':checks,'notProven':['Visual appeal or artistic approval','Physical mobile FPS','All later districts/NPCs are still planned, not delivered']}))
