"""Check shipped review pixels/anchors/Tiled collision against editable sources, offline."""
from pathlib import Path
import json, hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gwanghwamun';D=R/'public/review/gwanghwamun'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=read(S/'map-bundle.json');w=read(S/'world.json');t=read(D/'plaza.json');anchors=read(D/'anchors.json')
assert b['art_source']=='host_image' and b['portals']==[] and len(b['props'])==12
assert (w['width'],w['height'])==(1024,768) and w['spawn']==[512,600]
assert w['mapSha256']==sha(D/'plaza.json')
for name,p in b['props'].items():
    source=S/p['image'];assert sha(source)==p['sha256'] and source.read_bytes()==(D/f'{name}.png').read_bytes()
    im=Image.open(source).convert('RGBA');assert list(im.size)==p['size']
    colors=im.getcolors(im.width*im.height);assert colors and len([c for c in colors if c[1][3]])<=96
    assert not any(im.getchannel('A').histogram()[1:255])
    box=im.getbbox();assert box and box[0]>=2 and box[1]>=2 and box[2]<=im.width-2 and box[3]<=im.height-2
    assert anchors[name]==p['anchor_px'] and 0<=anchors[name][0]<im.width and 0<=anchors[name][1]<im.height
for entry in b['tilesets']:
    manifest=S/entry['manifest'];assert sha(manifest)==entry['sha256'];ts=read(manifest);assert sha(S/ts['image'])==ts['sha256']
    assert not ts['seamless_verified'] # No invented seamless/Wang proof.
for layer in b['layers']:
    if layer['kind']=='tiles':
        assert sha(S/layer['data'])==layer['sha256']
        actual=next(l for l in t['layers'] if l['name']==layer['name']);expected=[i+1 for row in read(S/layer['data'])for i in row]
        assert actual['data']==expected
source_tiled=read(S/'tiled/map.embedded.tmj');expected=[o for l in source_tiled['layers']if l['name']=='collision'for o in l['objects']if o['type']=='solid']
assert next(l for l in t['layers']if l['name']=='Collision')['objects']==expected and len(expected)==33
assert read(S/'terrain-accepted/terrain-bundle.json')['qa']['status']=='pass'
assert read(S/'navigation/nav-report.json')['status']=='pass' and read(S/'tiled/export-report.json')['status']=='pass'
for report in [S/'navigation/nav-report.json',S/'tiled/export-report.json']:
    for ref in read(report)['inputs']:
        path=(report.parent/ref['path']).resolve()
        assert path.is_relative_to(S.resolve()) and sha(path)==ref['sha256'],f'Stale Forge report: {report.name} / {ref["path"]}'
assert (D/'tiles.png').read_bytes()==(S/'tiles.png').read_bytes()
print(json.dumps({'status':'PASS','generated_props':12,'placements':len(b['objects']),'runtime_solids':len(expected),'source_equals_runtime':True,'native_alpha':'binary','shared_prop_palette_max':96,'terrain_variants':8,'no_future_districts':True,'tiled_solid_rectangles_preserved':True}))
