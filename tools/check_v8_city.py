"""Stored V8 preservation/route/collision checks. Never generates assets or calls Forge."""
from pathlib import Path
import json,math,hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v8-city';Q=R/'docs/v8-city/quality';Q.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text())
proof=read(S/'preservation.json')
for path,want in proof['gitBlobs'].items():
 data=(R/path).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==want,('Prior approved source changed',path)
b=read(S/'map/outdoor-bundle.json');old=read(R/'assets-src/v7-world/map/outdoor-bundle.json');now={o['id']:o for o in b['objects']};north=[o for o in old['objects']if o['y']<2240]
for o in north:assert all(now[o['id']][k]==o[k]for k in ['prop','x','y','sortY','scale']),o['id']
a=Image.open(S/'map/ground-native.png').convert('RGB');oldground=Image.open(R/'assets-src/v7-world/map/ground-native.png').convert('RGB');assert a.size==(4352,5312);assert ImageChops.difference(a.crop((0,0,4352,2240)),oldground.crop((0,0,4352,2240))).getbbox()is None
for k,p in b['props'].items():assert hashlib.sha256((S/'map'/p['image']).read_bytes()).hexdigest()==p['sha256'],k
for o in b['objects']:assert o['scale']==1,o['id']
t=read(R/'public/review/v8-city/world/plaza.json');solids=b['collision']['solids'];actual=next(l for l in t['layers']if l['name']=='Collision')['objects'];assert [[q[k]for k in ['x','y','width','height']]for q in actual]==[[q[k]for k in ['x','y','w','h']]for q in solids]
fails=[];samples=0
for route in read(S/'routes.json'):
 for a,c in zip(route['points'],route['points'][1:]):
  dx,dy=c[0]-a[0],c[1]-a[1];dist=math.hypot(dx,dy)
  if not dist:continue
  steps=max(1,math.ceil(dist/4));off=max(0,route['clearWidth']/2-8)
  for step in range(steps+1):
   for side in [-off,0,off]:
    t=step/steps;x=a[0]+dx*t-dy/dist*side;y=a[1]+dy*t+dx/dist*side;samples+=1
    hit=next((q for q in solids if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']),None)
    if hit:fails.append({'route':route['id'],'point':[round(x,2),round(y,2)],'reason':hit['reason']})
r={'status':'FAIL'if fails else'PASS','protectedPriorFiles':len(proof['gitBlobs']),'protectedNorthObjects':len(north),'northGroundAbove2240Exact':True,'nativeProps':len(b['props']),'placements':len(b['objects']),'solids':len(solids),'routes':len(read(S/'routes.json')),'strictFootShoulderSamples':samples,'failures':fails,'actorHalfFeet':[8,4],'sourceTiledCollisionExact':True}
(Q/'preservation-navigation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({**r,'failures':fails[:12]}));assert not fails,('Blocked routes',len(fails))
