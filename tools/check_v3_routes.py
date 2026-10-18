"""Authored road intent against exact exported rectangle collision/8x4actor feet."""
from v3_final_art import *
import math
b=json.loads((S/'map/outdoor-bundle.json').read_text());routes=json.loads((S/'routes.json').read_text());solids=b['collision']['solids'];bad=[];samples=0
for route in routes:
 points=route['points'];shoulder=route['clearWidth']/2-8
 for a,z in zip(points,points[1:]):
  dx,dy=z[0]-a[0],z[1]-a[1];distance=math.hypot(dx,dy)
  if not distance:continue
  for i in range(math.ceil(distance/8)+1):
   t=min(1,i*8/distance)
   for offset in [-shoulder,0,shoulder]:
    x=a[0]+dx*t-dy/distance*offset;y=a[1]+dy*t+dx/distance*offset;samples+=1
    hit=[q for q in solids if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']]
    if hit:bad.append({'route':route['id'],'point':[round(x,2),round(y,2)],'reason':hit[0].get('reason')})
q=R/'docs/v3-final/quality';q.mkdir(exist_ok=True);write(q/'road-clearance.json',{'status':'PASS'if not bad else'FAIL','samples':samples,'routes':len(routes),'failures':bad,'sourceBundleSha256':sha(S/'map/outdoor-bundle.json'),'method':'Every8pxcenter and actual road shoulders with8x4actor feet; exact exported solids. No collision tolerance widened.'});print('Samples',samples,'failures',len(bad));print(json.dumps(bad[:25],ensure_ascii=False))
if bad:raise SystemExit(1)
