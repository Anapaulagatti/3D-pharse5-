from pathlib import Path
import json, numpy as np
from scipy.ndimage import label, binary_erosion
from collections import deque
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a';report=[];routes={}
for kind in ['world','district']:
 p=json.loads((R/f'public/assets/gate3/{kind}/manifest.json').read_text());W,H=p['size'];mask=np.zeros((H,W),np.uint8)
 for c in p['chunks']:
  x,y,w,h=[c[k] for k in ['x','y','width','height']];mask[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
 # 8px lattice, cardinal traversal; every segment verified at 1px before path is accepted.
 step=8;grid=binary_erosion(mask>127,iterations=4)[::step,::step]; labels,n=label(grid)
 def snap(pt):
  x,y=pt;near=[]
  for iy in range(max(0,int(y)//step-3),min(grid.shape[0],int(y)//step+4)):
   for ix in range(max(0,int(x)//step-3),min(grid.shape[1],int(x)//step+4)):
    if grid[iy,ix]:near.append(((ix*step-x)**2+(iy*step-y)**2,(ix,iy)))
  return min(near)[1] if near else None
 def path(a,b):
  start=snap(a);goal=snap(b)
  if not start or not goal:return None
  q=deque([start]);prev={start:None}
  while q:
   x,y=q.popleft()
   if (x,y)==goal:break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    xx,yy=x+dx,y+dy
    if 0<=xx<grid.shape[1] and 0<=yy<grid.shape[0] and grid[yy,xx] and (xx,yy) not in prev:
     # Ensure not jumping across a narrow wall absent from lattice samples.
     if any(mask[y*step+dy*k,x*step+dx*k]<=127 for k in range(1,step+1)):continue
     prev[(xx,yy)]=(x,y);q.append((xx,yy))
  if goal not in prev:return None
  route=[];cur=goal
  while cur is not None:route.append([cur[0]*step,cur[1]*step]);cur=prev[cur]
  route.reverse();compressed=[route[0]]
  for i in range(1,len(route)-1):
   a,b,c=route[i-1:i+2]
   if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):compressed.append(b)
  compressed.append(route[-1]);return compressed
 tests=[('north-to-spine',[1740,1440],[2048,1900]),('bridge-to-house',[3120,3480],[3590,4410]),('oreum-to-house',[3730,3335],[3590,4410]),('mainland-ferry',[2048,1900],[2560,4100])] if kind=='world' else [('district-crossings',[1200,780],[2824,857])]
 for name,a,b in tests:
  route=path(a,b);distance=sum(abs(q[0]-r[0])+abs(q[1]-r[1]) for q,r in zip(route or [],(route or [])[1:]))
  report.append(dict(scene=kind,id=name,status='PASS' if route else 'FAIL',start=a,goal=b,gridStep=8,distancePx=distance if route else None,walkSeconds=distance/60 if route else None,runSeconds=distance/100 if route else None,validation='Static collision path: cardinal 8px search with4px safety clearance for input steering, each segment checked every1px. Not proof of actual input traversal or final artwork.'))
  if route:routes[name]=route
(D/'route-audit.json').write_text(json.dumps(report,indent=2)+'\n');(D/'route-points.json').write_text(json.dumps(routes,indent=2)+'\n');print(json.dumps(report,indent=2))
