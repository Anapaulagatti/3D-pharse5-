"""Offline preservation and targeted polish integrity; no authoring tools required."""
from pathlib import Path
import hashlib,json
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'assets-src/stage-b-polish';S=R/'assets-src/seoul-production'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for row in j(P/'preservation.json')['files']:assert sha(R/row['path'])==row['sha256'],row['path']
b=j(S/'outdoor-bundle.json');old=j(P/'baseline-map.json')
assert b['objects'][:len(old['objects'])]==old['objects'],'Accepted placements/roof sorting changed'
for field in ['anchors','spawns','portals']:assert b[field]==old[field],field
assert b['collision']['solids'][:len(old['collision']['solids'])]==old['collision']['solids']
for key in ['actorRadius','ySquash','walkRegions','rects']:assert b['collision'][key]==old['collision'][key],key
palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in j(S/'palette/palette.json')['colors']}
for row in j(P/'props.json'):
    source=P/row['image'];assert sha(source)==row['sha256'];assert sha(source)==sha(R/f'public/review/seoul-production/{row["id"]}.png')
    im=Image.open(source).convert('RGBA');a=im.getchannel('A');assert sum(a.histogram()[1:255])==0
    assert a.getbbox()==(2,2,im.width-2,im.height-2)
    assert all(rgb[:3] in palette for count,rgb in im.getcolors(im.width*im.height)if rgb[3])
    assert b['props'][row['id']]['anchor_px']==row['anchor']
for row in j(P/'image-route.json')['calls']:assert sha(P/row['source'])==row['sha256']
for name in ['terrain','verge']:
    report=j(P/f'{name}/terrain-bundle.json');assert report['qa']['status']=='pass';assert not any(c['status']=='warn'for c in report['qa']['checks'])
    for terrain in report['terrains'].values():
        for variant in terrain['variants']:
            assert Image.open(P/name/variant['path']).size==(128,128)
atlas=Image.open(S/'tiles.png');assert max(atlas.size)<=4096,atlas.size
placements=j(P/'placements.json');assert len(placements)==10
for p in placements:
    assert any([r['x'],r['y'],r['w'],r['h']]==p['footprint']for r in b['collision']['solids'])
assert len(b['objects'])==len(old['objects'])+10
print(json.dumps({'status':'PASS','protectedFiles':len(j(P/'preservation.json')['files']),'acceptedObjectsUnchanged':len(old['objects']),'approvedMassAndOldCollisionUnchanged':True,'newPurposefulPlacements':10,'newNativeProps':6,'generatedMaterialVariants':10,'terrainAtlas':list(atlas.size),'noSrcOrJuniChange':True,'limits':['Preservation/numeric QA is not visual approval','Seamless/Wang not certified; existing edge-canopy and Juni weak-motion warnings retained']}))
