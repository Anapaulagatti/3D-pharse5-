"""Offline stored-asset/geometry/export verification; NEVER generate or require Forge."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/seoul-production';D=R/'public/review/seoul-production'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=j(S/'outdoor-bundle.json');z=j(R/'docs/urban-zoning/zoning-plan.json');proof=j(S/'geometry-proof.json')
assert b['world']['width']==4096 and b['world']['height']==1728 and z['world']==[4096,3072]
assert proof['masterplanSha256']==sha(R/'docs/urban-zoning/zoning-plan.json')
for building in z['buildings']:
 if building['id'] in ['academy','workshop','museum']:
  for mass in building['masses']:
   assert any([s['x'],s['y'],s['w'],s['h']]==mass['bounds']for s in b['collision']['solids'])
for layer in b['layers']:
 if 'data' in layer:assert sha(S/layer['data'])==layer['sha256']
for ts in b['tilesets']:assert sha(S/ts['manifest'])==ts['sha256']
assert j(S/'tileset.json')['sha256']==sha(S/'tiles.png')
assert j(S/'world.json')['mapSha256']==sha(D/'plaza.json')
for name,p in b['props'].items():assert sha(S/p['image'])==sha(D/f'{name}.png')
assert sha(S/'tiles.png')==sha(D/'tiles.png')
palette=set()
for item in j(S/'props.json'):
 im=Image.open(S/item['image']).convert('RGBA');alpha=im.getchannel('A');hist=alpha.histogram();assert sum(hist[1:255])==0;assert sha(S/item['image'])==item['sha256'];assert alpha.crop((0,0,im.width,1)).getextrema()[1]==0 and alpha.crop((0,im.height-1,im.width,im.height)).getextrema()[1]==0 and alpha.crop((0,0,1,im.height)).getextrema()[1]==0 and alpha.crop((im.width-1,0,im.width,im.height)).getextrema()[1]==0;palette.update(rgb[:3]for count,rgb in im.getcolors(im.width*im.height) if rgb[3])
assert len(palette)<=192
for npc in z['npcs']:
 x,y=npc['point']
 if y<1728:
  for r in b['collision']['solids']:
   assert not (r['x']-8<=x<=r['x']+r['w']+8 and r['y']-4<=y<=r['y']+r['h']+4),(npc['id'],r)
for row in j(S/'image-route.json')['actualImageCalls']:assert sha(S/row['source'])==row['sourceSha256']
for name in ['outdoor','room']:
 report=j(S/f'{name}-linked-navigation/nav-report.json');assert report['status']=='pass';assert not any(c['status']=='fail'for c in report['checks'])
 for inp in report['inputs']:assert sha((S/f'{name}-linked-navigation'/inp['path']).resolve())==inp['sha256']
t=j(D/'plaza.json');export=j(S/'tiled/map.embedded.tmj');original=next(l for l in export['layers']if l['name']=='collision');runtime=next(l for l in t['layers']if l['name']=='Collision');assert runtime['objects']==[o for o in original['objects']if o['type']=='solid']
# Tile layers read back exactly from actual Tiled export.
for layer in [l for l in t['layers']if l['type']=='tilelayer']:assert layer==next(l for l in export['layers']if l['name']==layer['name'])
assert j(S/'preservation.json')['files']
for p in j(S/'preservation.json')['files']:assert sha(R/p['path'])==p['sha256'],p['path']
print(json.dumps({'status':'PASS','nativeGeneratedProps':len(j(S/'props.json')),'placements':len(b['objects']),'runtimeSolids':len(runtime['objects']),'paletteColors':len(palette),'linkedNavigation':['outdoor:pass','room:pass'],'preservedFiles':len(j(S/'preservation.json')['files']),'limits':['Numeric checks are not art approval','Southern world and NPC production await Stage B approval','Composition edge-canopy clipping WARN retained; not all art QA pass']}))
