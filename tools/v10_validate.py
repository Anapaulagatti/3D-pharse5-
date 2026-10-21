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
    for f in ['tools/v10_plan.py','tools/v10_final_build.py','tools/v10_surfaces.py','tools/v10_prepare_art.py']:
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
    assert sha(S/'plan/city.json')=='808ca4aa56be22afb11b35f30cbe557a5a5915dce272af0e9465257032233cc0','Approved plan changed'
    finish=read(S/'pixel-finish.json');assert len(finish['images'])==60
    for row in finish['images']:
        assert sha(S/row['image'])==row['sha256'],row['image']
        im=Image.open(S/row['image']).convert('RGBA');assert set(im.getchannel('A').get_flattened_data()) <= {0,255}
    provenance=read(S/'art-provenance.json')
    for row in provenance.values():
        assert row['art_source']=='host_image'
        if 'originalSha256' in row:assert sha(S/row['original'])==row['originalSha256']
    generations=read(S/'generation-manifest.json');assert len(generations)==10
    for item in generations:
        assert sha(S/item['original'])==item['sha256']
        assert sha(S/item['prompt'])==item['promptSha256']
    for row in provenance.values():
        if 'source' in row:assert row['source'] in provenance and provenance[row['source']]['art_source']=='host_image'
    plan=read(S/'plan/city.json')
    for lot in plan['plots']:
        obj=byid[lot['id']];x,y,w,h=lot['rect']
        assert (obj['x'],obj['y'])==(x+w/2,y+h),(lot['id'],'approved placement')
        assert sha(P/('v10-'+lot['id']+'.png'))==sha(S/'native'/(lot['id']+'.png'))
    assert not list(P.glob('v10-gray-*.png')),'Graybox artwork remains live'
    nav=read(S/'qa/nav-report.json');assert nav['status']=='pass'
    assert read(S/'qa/provenance.json')['bundleSha256']==sha(S/'map/bundle-hashed.json'),'Navigation proof stale'
    result=dict(status='PASS',northObjects=len(north['objects']),northSolids=len(north['solids']),protectedFiles=len(read(S/'protected-files.json')),northGroundExact=True,runtimeTiledReadbackExact=True,runtimeCollidersExact=True,noLegacySouthernRuntimeImports=True)
    print(json.dumps(result));return result
if __name__=='__main__':validate()
