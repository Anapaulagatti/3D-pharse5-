from pathlib import Path
import numpy as np,sys,json,heapq,hashlib
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[2]
f=np.load(R/'.cache/phase3bd-farm-path-floor.npy');G=4
# Body-aware masks are already anchor fields; retain 3px extra driver margin.
digest=hashlib.sha256(f.tobytes()).hexdigest()
cache=R/('.cache/phase3bd-path-'+digest+'.npy')
if cache.exists():small=np.load(cache)
else:
 d=distance_transform_edt(f);small=d[2::G,2::G]>=3;np.save(cache,small)
h,w=small.shape
s0=tuple(map(float,sys.argv[1:3]));t0=tuple(map(float,sys.argv[3:5]));radius=float(sys.argv[5]) if len(sys.argv)>5 else 10
s=(round((s0[0]-2)/G),round((s0[1]-2)/G));candidates=[]
for dy in range(-3,4):
 for dx in range(-3,4):
  x,y=s[0]+dx,s[1]+dy
  if 0<=x<w and 0<=y<h and small[y,x]:candidates.append(((x*G+2-s0[0])**2+(y*G+2-s0[1])**2,(x,y)))
if not candidates:raise ValueError('start not on walkable field '+str(s0))
s=min(candidates)[1];heap=[(0,0,s)];cost={s:0};parent={};end=None
while heap:
 _,g,u=heapq.heappop(heap)
 if g!=cost[u]:continue
 if (u[0]*G+2-t0[0])**2+(u[1]*G+2-t0[1])**2<=radius**2:end=u;break
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  v=(u[0]+dx,u[1]+dy)
  if not (0<=v[0]<w and 0<=v[1]<h and small[v[1],v[0]]):continue
  ng=g+1
  if ng<cost.get(v,1e20):
   cost[v]=ng;parent[v]=u;heur=max(0,abs(v[0]*G+2-t0[0])+abs(v[1]*G+2-t0[1])-radius)/G;heapq.heappush(heap,(ng+heur,ng,v))
if end is None:raise ValueError('No route '+str(t0))
r=[end]
while r[-1]!=s:r.append(parent[r[-1]])
r.reverse();out=[r[0]];direction=None
for i in range(1,len(r)):
 nd=(r[i][0]-r[i-1][0],r[i][1]-r[i-1][1])
 if direction is not None and nd!=direction:out.append(r[i-1])
 direction=nd
out.append(r[-1]);print(json.dumps({'points':[[x*G+2,y*G+2]for x,y in out],'length':(len(r)-1)*G,'target':t0,'radius':radius}))
