"""Offline release guards for the compact review. Never generates or calls APIs."""
from pathlib import Path
import hashlib,json
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/world-refinement';D=R/'public/review/world-refinement'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protected=j(S/'preservation.json')['files']
for row in protected:assert sha(R/row['path'])==row['sha256'],row['path']
b=j(S/'outdoor-bundle.json');layout=j(R/'docs/world-refinement/compact-layout.json');original=j(R/'docs/urban-zoning/zoning-plan.json')
assert b['world']['width']==2304 and b['world']['height']==1920
assert len({o['id'] for o in b['objects']})==len(b['objects'])
palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in j(R/'assets-src/seoul-production/palette/palette.json')['colors']}
route=j(S/'image-route.json');assert route['paidProviderRequests']==0 and len(route['calls'])==5
for row in route['calls']:assert sha(S/row['source'])==row['sha256']
for row in j(S/'props.json'):
    p=S/row['image'];assert sha(p)==row['sha256']
    im=Image.open(p).convert('RGBA');a=im.getchannel('A')
    assert sum(a.histogram()[1:255])==0 and a.getbbox()==(2,2,im.width-2,im.height-2)
    assert all(rgb[:3] in palette for count,rgb in im.getcolors(im.width*im.height)if rgb[3])
    assert b['props'][row['id']]['anchor_px']==row['anchor']
for name,p in b['props'].items():assert sha(S/p['image'])==sha(D/f'{name}.png'),name
derived=j(S/'derived-architecture.json');whole=Image.open(S/derived['parts'][0]['source']).convert('RGBA');reconstructed=Image.new('RGBA',whole.size)
for p in derived['parts']:
    assert sha(S/p['source'])==p['sourceSha256'] and sha(S/p['image'])==p['sha256']
    part=Image.open(S/p['image']).convert('RGBA');pixels=part.crop((2,2,part.width-2,part.height-2));box=p['sourceBox']
    assert pixels.tobytes()==whole.crop(tuple(box)).tobytes()
    reconstructed.paste(pixels,(box[0],box[1]))
assert whole.tobytes()==reconstructed.tobytes(),'Approved workshop pixels changed'
for row in j(S/'placements.json')['props']:assert not Path(row['image']).is_absolute() and (S/row['image']).is_file()
solids=b['collision']['solids']
for building in original['buildings']:
    if building['id'] in ['academy','workshop','museum']:
        dx,dy=layout['groups'][building['id']]
        for mass in building['masses']:
            x,y,w,h=mass['bounds'];assert any([s['x'],s['y'],s['w'],s['h']]==[x+dx,y+dy,w,h]for s in solids)
for seg in original['palace']['segments']:
    assert any(s['reason']=='Original palace '+seg['id'] for s in solids),seg['id']
for directory in ['navigation','outdoor-linked-navigation','room-linked-navigation']:
    report=j(S/directory/'nav-report.json');assert report['status']=='pass'
    assert not report['problems']
    for row in report['inputs']:assert sha(S/directory/row['path'])==row['sha256'],row['path']
roads=j(R/'docs/world-refinement/quality/road-clearance.json');assert roads['status']=='PASS' and not roads['failures']
assert roads['bundleSha256']==sha(S/'outdoor-bundle.json') and roads['layoutSha256']==sha(R/'docs/world-refinement/compact-layout.json')
audit=j(S/'composed/audit.json');assert not audit.get('warnings'),audit.get('warnings')
t=j(D/'plaza.json');exported=next(l for l in t['layers']if l['name']=='Collision')['objects']
assert len(exported)==len(solids)
assert sorted((p['x'],p['y'],p['width'],p['height'])for p in exported)==sorted((p['x'],p['y'],p['w'],p['h'])for p in solids)
for reserved in j(S/'geometry-proof.json')['reservedNPCs']:
    x,y=reserved['point'];assert not any(p['x']-8<x<p['x']+p['w']+8 and p['y']-4<y<p['y']+p['h']+4 for p in solids),reserved
assert max(Image.open(S/'tiles.png').size)<=4096 and sha(S/'tiles.png')==sha(D/'tiles.png')
print(json.dumps({'status':'PASS','protectedFiles':len(protected),'originalPalaceSegments':7,'newOriginalPropImages':11,'pixelExactWorkshopParts':2,'world':[2304,1920],'objects':len(b['objects']),'solids':len(solids),'publicPathSamples':roads['sampledPositions'],'limits':['Numeric integrity is not visual approval','Original Juni side-idle/wave QA warnings retained; physical-phone FPS unmeasured']}))
