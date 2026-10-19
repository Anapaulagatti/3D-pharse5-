"""Offline saved-art/road-release guard; never invokes Forge, generation or the network."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/modern-streets';OLD=R/'assets-src/v3-final/map';P=S/'map';Q=R/'docs/modern-streets/quality'
def read(p):return json.loads(p.read_text())
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
proof=read(S/'preservation.json')
for name,h in proof['files'].items():assert sha(R/name)==h,('Protected prior file changed',name)
b=read(P/'outdoor-bundle.json');old=read(OLD/'outdoor-bundle.json');world=read(P/'world.json');runtime=R/'public/review/modern-streets/world';t=read(runtime/'plaza.json')
assert b['collision']==old['collision']and len(b['collision']['solids'])==621
assert b['spawns']==old['spawns']and b['portals']==old['portals']and b['anchors']==old['anchors']and b['interactions']==old['interactions']
assert len(b['objects'])==len(old['objects'])==406
for a,z in zip(b['objects'],old['objects']):
 assert {k:v for k,v in a.items()if k!='occluder'}=={k:v for k,v in z.items()if k!='occluder'}
 ac=a.get('occluder',{});zc=z.get('occluder',{});assert {k:v for k,v in ac.items()if k!='source'}=={k:v for k,v in zc.items()if k!='source'}
 if zc.get('source'):assert (P/ac['source']).resolve()==(OLD/zc['source']).resolve()
for k,a in b['props'].items():
 assert (P/a['image']).resolve()==(OLD/old['props'][k]['image']).resolve()
 assert sha(P/a['image'])==a['sha256']==old['props'][k]['sha256']
 assert (runtime/f'{k}.png').read_bytes()==(P/a['image']).read_bytes()
assert sha(runtime/'plaza.json')==world['mapSha256']and (runtime/'tiles.png').read_bytes()==(P/'tiles.png').read_bytes()
actual=sorted((o['x'],o['y'],o['width'],o['height'])for l in t['layers']if l['name']=='Collision'for o in l['objects'])
expected=sorted((o['x'],o['y'],o['w'],o['h'])for o in b['collision']['solids']);assert actual==expected
for name in ['land-mask.png','forest-mask.png','walk-mask.png']:assert (P/name).read_bytes()==(OLD/name).read_bytes()
before=Image.open(OLD/'ground-native.png').convert('RGB');after=Image.open(P/'ground-native.png').convert('RGB');assert before.size==after.size==(4352,4800)
assert ImageChops.difference(before.crop((0,0,4352,2240)),after.crop((0,0,4352,2240))).getbbox()is None
assert ImageChops.difference(before.crop((0,3648,4352,4800)),after.crop((0,3648,4352,4800))).getbbox()is None
assert ImageChops.difference(before.convert('RGB'),after.convert('RGB')).getbbox()is not None
receipt=read(S/'image-route.json');assert len(receipt)==1 and receipt[0]['paidProviderRequests']==0 and sha(S/receipt[0]['raw'])==receipt[0]['sha256']
palette={tuple(bytes.fromhex(c['hex'].lstrip('#')))for c in read(S/'palette/palette.json')['colors']}
assert (S/'palette/palette.json').read_bytes()==(R/'assets-src/v3-final/palette/palette.json').read_bytes()
for p in list((S/'overlays').glob('*.png'))+list((S/'terrain').glob('*.png')):
 im=Image.open(p).convert('RGBA');values=set(im.get_flattened_data());assert {v[3]for v in values}<={0,255}and {v[:3]for v in values if v[3]}<=palette
assert read(R/'assets-src/juni-animation/runtime.json')['frameCount']==144
for name in ['world','room']:assert read(S/f'{name}-navigation/nav-report.json')['status']=='pass'
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
report={'status':'PASS'if not bad else'FAIL','sourceBundleSha256':sha(P/'outdoor-bundle.json'),'routes':len(routes),'samples':samples,'failures':bad,'method':'Original24routes plus20new cardinal street centrelines and actual shoulders at8pxsteps with8x4actor feet. Exact unchanged621runtime colliders, no tolerance weakening.','allApprovedPlacementsAndCollisionPreserved':True,'northernGroundChangedPixels':0,'JejuGroundChangedPixels':0,'priorProtectedFiles':len(proof['files'])}
Q.mkdir(parents=True,exist_ok=True);(Q/'road-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
assert not bad,json.dumps(bad[:30],ensure_ascii=False)
print(json.dumps({k:v for k,v in report.items()if k!='failures'}))
