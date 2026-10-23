from pathlib import Path
from PIL import Image
from scipy.ndimage import binary_erosion
from collections import deque
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-corrections';p=json.loads((R/'public/assets/gate3/registration/manifest.json').read_text());W,H=p['size'];walk=np.zeros((H,W),np.uint8)
for c in p['chunks']:
 x,y,w,h=[c[k] for k in ['x','y','width','height']];walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
grid=binary_erosion(walk>127,iterations=3)[::4,::4]
def route(start,end):
 def snap(pt):
  x,y=pt;pts=[]
  for yy in range(max(0,int(y)//4-4),min(grid.shape[0],int(y)//4+5)):
   for xx in range(max(0,int(x)//4-4),min(grid.shape[1],int(x)//4+5)):
    if grid[yy,xx]:pts.append(((xx*4-x)**2+(yy*4-y)**2,(xx,yy)))
  return min(pts)[1] if pts else None
 a,b=snap(start),snap(end)
 if a is None or b is None:return None
 q=deque([a]);prev={a:None}
 while q:
  x,y=q.popleft()
  if (x,y)==b:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   xx,yy=x+dx,y+dy
   if 0<=xx<grid.shape[1] and 0<=yy<grid.shape[0] and grid[yy,xx] and (xx,yy) not in prev:
    if any(walk[y*4+dy*k,x*4+dx*k]<=127 for k in range(1,5)):continue
    prev[xx,yy]=(x,y);q.append((xx,yy))
 if b not in prev:return None
 pts=[];cur=b
 while cur is not None:pts.append([cur[0]*4,cur[1]*4]);cur=prev[cur]
 pts.reverse();result=[pts[0]]
 for i in range(1,len(pts)-1):
  a,b,c=pts[i-1:i+2]
  if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):result.append(b)
 result.append(pts[-1]);return result
cases=[('station-threshold',[2598.5,2760],[2598.5,2610]),('bakery-entry',[1814,3900],[1814,3840]),('retail-to-station',[1128,2690],[2598.5,2760]),('waterfront-bypass',[2048,3300],[1814,3900]),('bakery-to-bridge',[1814,3900],[3120,3480]),('convenience-entry',[368,3220],[428,3133])]
rows=[];routes={}
for name,a,b in cases:
 pts=route(a,b);distance=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(pts or [],(pts or [])[1:]));rows.append(dict(id=name,start=a,goal=b,status='PASS' if pts else 'FAIL',lengthPx=distance,walkSeconds=distance/60,method='4px cardinal BFS with3px safety inset; each segment verified at1px; not exhaustive navigation acceptance'))
 if pts:routes[name]=pts
inv=json.loads((R/'docs/gate3a/protected-assets.json').read_text());changed=[k for k,v in inv['sha256'].items() if hashlib.sha256((R/k).read_bytes()).hexdigest()!=v];assert not changed,changed
(D/'static-validation.json').write_text(json.dumps({'routes':rows,'protectedFiles':len(inv['sha256']),'protectedSha256':'PASS','stationAnchor':[2238.5,2180],'stationLogicalCollider':[2322.5,2380,555,210],'masterplanSha256':hashlib.sha256((R/'assets-src/gate25/world-plan-v1.json').read_bytes()).hexdigest()},indent=2)+'\n');(D/'route-points.json').write_text(json.dumps(routes,indent=2)+'\n');print(rows)
