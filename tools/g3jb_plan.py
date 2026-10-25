"""Exact native all-pose clearance and original-control waypoint plans, BOTH crossings."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,heapq
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/jeju-bridges-v1';D=R/'docs/gate3-jeju-bridges';m=json.loads((R/'public/assets/gate3/jeju-bridges-world/manifest.json').read_text());f=np.zeros((4864,4352),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
valid=np.array(Image.open(S/'all-pose-supported-centres.png'))>0;safe=(f>0)&valid;dist=distance_transform_edt(safe)
def route(a,b):
 a=tuple(a);b=tuple(b);q=[(0,0,(*a,4))];cost={(*a,4):0};parent={};end=None
 while q:
  _,g,u=heapq.heappop(q)
  if cost[u]!=g:continue
  if u[:2]==b:end=u;break
  for k,(dx,dy)in enumerate([(5,0),(-5,0),(0,5),(0,-5)]):
   x,y=u[0]+dx,u[1]+dy
   if not(2980<x<3620 and 3380<y<4140):continue
   pts=[(u[0]+dx*t//5,u[1]+dy*t//5)for t in range(1,6)]
   if not all(safe[yy,xx]for xx,yy in pts):continue
   v=(x,y,k);ng=g+5+(12 if u[2]!=k and u[2]!=4 else 0)+10/(dist[y,x]+1)
   if ng<cost.get(v,1e20):cost[v]=ng;parent[v]=u;heapq.heappush(q,(ng+abs(x-b[0])+abs(y-b[1]),ng,v))
 assert end is not None,('NO SAFE ROUTE',a,b)
 p=[end]
 while p[-1]in parent:p.append(parent[p[-1]])
 p.reverse();out=[p[0][:2]]
 for i in range(1,len(p)-1):
  if p[i][2]!=p[i+1][2]:out.append(p[i][:2])
 out.append(p[-1][:2]);return [list(p)for p in out]
legs=[];report={}
for k,start,checks in [('A',[3010,3460],[[3110,3460],[3300,3555],[3350,3570],[3530,3640]]),('B',[3030,3920],[[3120,3975],[3300,4020],[3570,4060]])]:
 points=[start]
 for t in checks:points+=route(points[-1],t)[1:]
 report[k]={'start':start,'end':checks[-1],'mandatoryStops':checks,'safeNativeRoute':points,'minimumUniversalPoseMarginPx':min(float(dist[y,x])for x,y in points),'geometryOnly':'NOT actual gameplay PASS'}
 for run,direction in [(False,'out'),(False,'return'),(True,'out'),(True,'return')]:
  p=points if direction=='out'else list(reversed(points));leg={'id':f'bridge-{k.lower()}-'+('run'if run else'walk')+'-'+direction,'bridge':k,'points':p,'scene':'jeju-bridges-world','entry':'bridge-'+k.lower()+'-full','sceneResetBefore':not run and direction=='out','running':run,'gridTarget':p[-1]};legs.append(leg)
json.dump({'method':'Planned routes only. Actual WASD/Shift/joystick executes every leg; distinct review spawn permitted once per crossing, never within traversal. All120 native poses support union54px wide/7px high, not sprite box.','legs':legs},open(D/'walk-plan.json','w'),indent=2);json.dump(report,open(D/'geometric-clearance.json','w'),indent=2)
print([(l['id'],len(l['points']))for l in legs])
