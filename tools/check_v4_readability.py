"""Offline V4 saved-art safety; never generates or calls Forge/network."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v4-readability';P=S/'map';OLD=R/'assets-src/modern-streets/map';Q=R/'docs/v4-readability/quality'
def read(p):return json.loads(p.read_text())
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
proof=read(S/'preservation.json')
for name,h in proof['files'].items():assert sha(R/name)==h,('Protected prior file changed',name)
b=read(P/'outdoor-bundle.json');old=read(OLD/'outdoor-bundle.json');runtime=R/'public/review/v4-readability/world';world=read(P/'world.json');t=read(runtime/'plaza.json')
assert b['collision']['solids'][:621]==old['collision']['solids']
for key in ['spawns','portals','anchors','interactions','world','camera']:assert b[key]==old[key],key
assert b['objects'][:406]==old['objects']
for k,a in old['props'].items():
 assert (P/b['props'][k]['image']).resolve()==(OLD/a['image']).resolve()
 assert sha(P/b['props'][k]['image'])==a['sha256']==b['props'][k]['sha256']
for k,a in b['props'].items():assert (runtime/f'{k}.png').read_bytes()==(P/a['image']).read_bytes()
assert sha(runtime/'plaza.json')==world['mapSha256']and(runtime/'tiles.png').read_bytes()==(P/'tiles.png').read_bytes()
actual=sorted((o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects']);expected=sorted((o['x'],o['y'],o['w'],o['h'])for o in b['collision']['solids']);assert actual==expected
for name in ['land-mask.png','forest-mask.png','walk-mask.png']:assert(P/name).read_bytes()==(OLD/name).read_bytes()
before=Image.open(OLD/'ground-native.png').convert('RGB');after=Image.open(P/'ground-native.png').convert('RGB');assert before.size==after.size==(4352,4800)
for box in [(0,0,4352,2240),(0,3648,4352,4800)]:assert ImageChops.difference(before.crop(box),after.crop(box)).getbbox()is None
assert read(R/'assets-src/juni-animation/runtime.json')['frameCount']==144
for name in ['world','room']:assert read(S/f'{name}-navigation/nav-report.json')['status']=='pass'
new=b['objects'][406:];boundaries=read(S/'boundaries.json')['placements'];assert len(new)==len(boundaries)==len(b['collision']['solids'])-621
for o,p in zip(new,boundaries):assert o['x']==p['x']and o['y']==p['y']and p['collider']in b['collision']['solids']
for r in read(S/'prop-recipes.json'):
 im=Image.open(S/'props'/('v4-'+r['id']+'.png')).convert('RGBA');assert {a[3]for a in im.get_flattened_data()}<={0,255}
assert (S/'palette/palette.json').read_bytes()==(R/'assets-src/v3-final/palette/palette.json').read_bytes()
receipt=read(S/'image-route.json');assert len(receipt)==1 and receipt[0]['paidProviderRequests']==0 and sha(S/receipt[0]['raw'])==receipt[0]['sha256']
routes=read(S/'routes.json');bad=[];samples=0
for route in routes:
 for a,z in zip(route['points'],route['points'][1:]):
  dx,dy=z[0]-a[0],z[1]-a[1];dist=math.hypot(dx,dy)
  if not dist:continue
  for i in range(math.ceil(dist/8)+1):
   f=min(1,i*8/dist)
   for off in [-(route['clearWidth']/2-8),0,route['clearWidth']/2-8]:
    x=a[0]+dx*f-dy/dist*off;y=a[1]+dy*f+dx/dist*off;samples+=1
    hit=[q for q in b['collision']['solids']if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']]
    if hit:bad.append({'route':route['id'],'point':[round(x,2),round(y,2)],'reason':hit[0].get('reason')})
report={'status':'PASS'if not bad else'FAIL','sourceBundleSha256':sha(P/'outdoor-bundle.json'),'routes':len(routes),'samples':samples,'failures':bad,'newBoundaries':len(new),'allOriginal406PlacementsAnd621CollidersPreserved':True,'northernAndJejuChangedPixels':0,'priorProtectedFiles':len(proof['files']),'method':'All original44routes plus new park loop, actual8x4feet+shoulders/8pxsampling; exact old621+new boundary feet match Tiled runtime. No tolerance changes.'};Q.mkdir(parents=True,exist_ok=True);(Q/'route-clearance.json').write_text(json.dumps(report,indent=2)+'\n');assert not bad,json.dumps(bad[:25]);print(json.dumps({k:v for k,v in report.items()if k!='failures'}))
