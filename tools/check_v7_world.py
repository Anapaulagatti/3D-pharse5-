"""V7 offline preservation, native pixels, physical width and real map consistency.
Stored PNG/data validation only: stdlib/Pillow; never generates artwork.
"""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v7-world'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proof=read(S/'preservation.json')
for path,want in proof['gitBlobs'].items():
 data=(R/path).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==want,('Approved baseline file changed',path)
b=read(S/'map/outdoor-bundle.json');old=read(R/'assets-src/v6-restructure/map/outdoor-bundle.json')
assert b['size']==old['size'] if 'size'in b else True
for o in b['objects']:
 assert o['scale']==1,('Approved native prop rescaled',o['id'])
for key,p in b['props'].items():
 assert sha((S/'map'/p['image']).resolve())==p['sha256'],key
oldnorth={o['id']:o for o in old['objects']if o['y']<2240}
new={o['id']:o for o in b['objects']}
for key,o in oldnorth.items():
 assert [new[key][k]for k in ['prop','x','y','sortY','scale']]==[o[k]for k in ['prop','x','y','sortY','scale']],key
before=Image.open(R/'assets-src/v6-restructure/map/ground-native.png').convert('RGB');after=Image.open(S/'map/ground-native.png').convert('RGB')
assert after.size==before.size==(4352,5312)
assert ImageChops.difference(before.crop((0,0,4352,1920)),after.crop((0,0,4352,1920))).getbbox()is None,'Protected heritage ground changed'
tiled=read(R/'public/review/v7-world/world/plaza.json');actual=next(l for l in tiled['layers']if l['name']=='Collision')['objects']
assert [[q[k]for k in ['x','y','width','height']]for q in actual]==[[q[k]for k in ['x','y','w','h']]for q in b['collision']['solids']],'Runtime/source collision mismatch'
solids=b['collision']['solids'];samples=0;fails=[]
for route in read(S/'routes.json'):
 for a,c in zip(route['points'],route['points'][1:]):
  dx,dy=c[0]-a[0],c[1]-a[1];dist=math.hypot(dx,dy)
  if not dist:continue
  steps=max(1,math.ceil(dist/4));off=max(0,route['clearWidth']/2-8)
  for step in range(steps+1):
   for side in [-off,0,off]:
    t=step/steps;x=a[0]+dx*t-dy/dist*side;y=a[1]+dy*t+dx/dist*side;samples+=1
    hit=next((q for q in solids if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']),None)
    if hit:fails.append({'route':route['id'],'point':[x,y],'reason':hit['reason']})
(R/'.cache/v7-world/strict-shoulder-diagnostics.json').parent.mkdir(parents=True,exist_ok=True)
(R/'.cache/v7-world/strict-shoulder-diagnostics.json').write_text(json.dumps({'samples':samples,'failures':fails},indent=2)+'\n')
assert not fails,('Blocked physical route/shoulder',len(fails),fails[:12])
navs={}
for name in ['world','room']:
 j=read(S/f'{name}-navigation/nav-report.json');assert j['status']=='pass',[(c['id'],c['status'],c['value'])for c in j['checks']if c['status']!='pass'];navs[name]=j
report={'status':'PASS','baseline':proof['baseline'],'protectedFiles':len(proof['gitBlobs']),'protectedNorthObjects':len(oldnorth),'heritageGroundAbove1920Exact':True,'approvedNativePropKinds':len(b['props']),'placements':len(b['objects']),'solids':len(solids),'routes':len(read(S/'routes.json')),'strictFootAndShoulderSamples':samples,'actorHalfFeet':[8,4],'noScaledApprovedArt':True,'sourceRuntimeCollisionExact':True}
out=R/'docs/v7-world/quality/preservation-navigation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
