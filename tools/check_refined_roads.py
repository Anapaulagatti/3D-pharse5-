"""Product-level street clearance against exported authored solids; no art generation."""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/world-refinement'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((S/'outdoor-bundle.json').read_text());plan=json.loads((R/'docs/world-refinement/compact-layout.json').read_text());solids=b['collision']['solids'];fail=[];count=0
for road in plan['roads']:
 for a,z in zip(road['points'],road['points'][1:]):
  dx=z[0]-a[0];dy=z[1]-a[1];length=math.hypot(dx,dy);nx=-dy/length;ny=dx/length
  for i in range(math.ceil(length/8)+1):
   t=min(1,i*8/length);x=a[0]+dx*t;y=a[1]+dy*t
   for side in [-1,0,1]:
    offset=side*(road['width']/2-10);px=x+nx*offset;py=y+ny*offset;count+=1
    for angle in range(0,360,45):
     xx=px+8*math.cos(math.radians(angle));yy=py+4*math.sin(math.radians(angle))
     collision=next((r for r in solids if r['x']<=xx<=r['x']+r['w']and r['y']<=yy<=r['y']+r['h']),None)
     if collision:
      if not any(f['road']==road['id']and f['reason']==collision['reason']for f in fail):fail.append({'road':road['id'],'point':[round(px,2),round(py,2)],'reason':collision['reason']})
      break
report={'status':'FAIL'if fail else'PASS','method':'All planned public path segments sampled every8px, centre and both clear-width shoulders, with actual8x4elliptical actor feet against every authored solid. Independent route intent vs collider placement, not a mirror test of rendering.','sampledPositions':count,'failures':fail,'bundleSha256':sha(S/'outdoor-bundle.json'),'layoutSha256':sha(R/'docs/world-refinement/compact-layout.json')}
out=R/'docs/world-refinement/quality/road-clearance.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not fail
