"""Offline validation of saved V6 map, relocation and strict physical route clearance."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v6-restructure';P=S/'map';Q=R/'docs/v6-restructure/quality'
def read(p):return json.loads(p.read_text())
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
proof=read(S/'preservation.json')
for name,h in proof['files'].items():assert sha(R/name)==h,('Prior protected file changed',name)
b=read(P/'outdoor-bundle.json');old=read(R/'assets-src/v4-readability/map/outdoor-bundle.json');runtime=R/'public/review/v6-restructure/world';world=read(P/'world.json');t=read(runtime/'plaza.json')
assert b['world']['width']==4352 and b['world']['height']==5312
assert len(read(S/'relocations.json')['placements'])>75
assert read(R/'assets-src/juni-animation/runtime.json')['frameCount']==144
for o in old['objects']:
 if o['y']<2240:
  a=next(a for a in b['objects']if a['id']==o['id']);assert all(a[k]==o[k]for k in ['x','y','sortY','prop','scale','anchor_px'])
for k,p in b['props'].items():assert sha(P/p['image'])==p['sha256']and(runtime/f'{k}.png').read_bytes()==(P/p['image']).read_bytes()
assert sha(runtime/'plaza.json')==world['mapSha256']and(runtime/'tiles.png').read_bytes()==(P/'tiles.png').read_bytes()
actual=sorted((o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects']);expected=sorted((o['x'],o['y'],o['w'],o['h'])for o in b['collision']['solids']);assert actual==expected
before=Image.open(R/'assets-src/v4-readability/map/ground-native.png').convert('RGB');after=Image.open(P/'ground-native.png').convert('RGB');assert after.size==(4352,5312)
assert ImageChops.difference(before.crop((0,0,4352,2240)),after.crop((0,0,4352,2240))).getbbox()is None
for name,source in [('world',P/'outdoor-bundle.json'),('room',S/'room-bundle.json')]:
 nav=read(S/f'{name}-navigation/nav-report.json')
 assert nav['status']=='pass'and not nav['problems']and not nav.get('unreachablePockets'),name
 assert nav['inputs'][0]['sha256']==sha(source),('Stale nav report',name)
audit=read(P/'composed/audit.json')
assert not any(c['status']=='fail'for c in audit['checks'])
assert next(c for c in audit['checks']if c['id']=='actors_visible')['status']=='pass'
travel=read(S/'travel.json')
for portal in b['portals']:
 if portal['id'].startswith('ferry-'):
  target=travel['mainlandTrigger']if portal['id']=='ferry-jeju'else travel['islandTrigger']
  assert portal['circle'][:2]==target
for o in read(S/'relocations.json')['placements']:
 actual=next(a for a in b['objects']if a['id']==o['id'])
 assert [actual['x'],actual['y']]==o['after']and o['after']!=o['before']
routes=read(S/'routes.json');bad=[];samples=0
for r in routes:
 for a,z in zip(r['points'],r['points'][1:]):
  dx,dy=z[0]-a[0],z[1]-a[1];dist=math.hypot(dx,dy)
  if not dist:continue
  for i in range(math.ceil(dist/8)+1):
   f=min(1,i*8/dist)
   for off in [-(r['clearWidth']/2-8),0,r['clearWidth']/2-8]:
    x=a[0]+dx*f-dy/dist*off;y=a[1]+dy*f+dx/dist*off;samples+=1
    hit=[q for q in b['collision']['solids']if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']]
    if hit:bad.append({'route':r['id'],'point':[round(x,2),round(y,2)],'reason':hit[0].get('reason')})
report={'status':'PASS'if not bad else'FAIL','sourceBundleSha256':sha(P/'outdoor-bundle.json'),'routes':len(routes),'samples':samples,'failures':bad,'priorProtectedFiles':len(proof['files']),'method':'Actual8x4feet+shoulders at8pxsampling; exact runtimeTiled rectangles; native northern pixels/Juni/original artwork protected; no tolerance changes.'};Q.mkdir(parents=True,exist_ok=True);(Q/'route-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
assert not bad,json.dumps(bad[:12]);print(json.dumps({k:v for k,v in report.items()if k!='failures'}))
