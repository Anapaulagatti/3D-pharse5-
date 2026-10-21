"""Offline stored-output checks; no authoring, network or optional Forge requirement."""
import ast
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v10-city';P=R/'public/assets/v10-city'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
    protection=read(R/'assets-src/protected-north/protection.json')
    for file,key in [('ground-native.png','groundSha256'),('land-mask.png','landMaskSha256'),('district.json','layoutSha256')]:
        assert sha(R/'assets-src/protected-north'/file)==protection[key],file
    for path,want in read(R/'assets-src/protected-north/shared-system-protection.json').items():assert sha(R/path)==want,path
    for path,want in read(S/'protected-files.json').items():assert sha(R/path)==want,path
    for f in ['tools/v10_plan.py','tools/v10_build.py']:
        source=(R/f).read_text();ast.parse(source)
        assert all(s not in source for s in ['v9-world','v8-city','v7-world','v6-world']),f
    north=read(R/'assets-src/protected-north/district.json');b=read(S/'map/bundle.json');byid={o['id']:o for o in b['objects']}
    for o in north['objects']:
        for key in ['prop','x','y','sortY','scale','anchor_px']:assert byid[o['id']][key]==o[key],(o['id'],key)
    assert b['collision']['solids'][:len(north['solids'])]==north['solids']
    original=Image.open(R/'assets-src/protected-north/ground-native.png').convert('RGB');ground=Image.open(S/'map/ground-native.png').convert('RGB')
    assert ImageChops.difference(original,ground.crop((0,0,4352,2240))).getbbox() is None
    atlas=Image.open(P/'tiles.png').convert('RGB');tm=read(P/'plaza.json');w,h=read(S/'plan/city.json')['world'];restored=Image.new('RGB',(w,h))
    for i,gid in enumerate(tm['layers'][0]['data']):
        tile=gid-1;x=(tile%128)*32;y=(tile//128)*32
        restored.paste(atlas.crop((x,y,x+32,y+32)),((i%(w//32))*32,(i//(w//32))*32))
    assert ImageChops.difference(restored,ground).getbbox() is None,'Tiled runtime readback differs'
    col=tm['layers'][2]['objects'];assert [[o[k]for k in ['x','y','width','height']]for o in col]==[[o[k]for k in ['x','y','w','h']]for o in b['collision']['solids']]
    assert sha(P/'tiles.png')==sha(S/'map/tiles.png')
    for kind,spec in b['props'].items():assert sha(P/(kind+'.png'))==sha(S/'map'/spec['image']),kind
    for src in (R/'src').rglob('*.ts'):assert 'assets-src/v9-world' not in src.read_text(),src
    nav=read(S/'qa/nav-report.json');assert nav['status']=='pass'
    assert read(S/'qa/provenance.json')['bundleSha256']==sha(S/'map/bundle-hashed.json'),'Navigation proof stale'
    result=dict(status='PASS',northObjects=len(north['objects']),northSolids=len(north['solids']),protectedFiles=len(read(S/'protected-files.json')),northGroundExact=True,runtimeTiledReadbackExact=True,runtimeCollidersExact=True,noLegacySouthernRuntimeImports=True)
    print(json.dumps(result));return result
if __name__=='__main__':validate()
