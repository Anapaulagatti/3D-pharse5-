"""Plan input waypoints from the final collision grid; never change runtime positions."""
import json,heapq
import numpy as np
from scipy.ndimage import minimum_filter
from pathlib import Path
G=json.loads(Path('.cache/v10-production/navigation-final-2/nav-grid.json').read_text());grid=G['moves'];cols=G['cols'];cell=G['cell']
safe=minimum_filter(np.array([[v!='#' for v in row]for row in grid],dtype=np.uint8),size=13,mode='constant')
def route(a,b):
 start=(int(a[0]/cell),int(a[1]/cell));goal=(int(b[0]/cell),int(b[1]/cell));q=[(0,0,start)];cost={start:0};parent={}
 while q:
  _,c,p=heapq.heappop(q)
  if c!=cost[p]:continue
  if p==goal:break
  x,y=p;bits=int(grid[y][x],16)if grid[y][x]!='#'else 0
  for dx,dy,bit in [(1,0,1),(0,1,2),(-1,0,4),(0,-1,8)]:
   if not bits&bit:continue
   n=(x+dx,y+dy);nc=c+1
   if not safe[n[1],n[0]]:continue
   if nc<cost.get(n,1e20):cost[n]=nc;parent[n]=p;heapq.heappush(q,(nc+abs(n[0]-goal[0])+abs(n[1]-goal[1]),nc,n))
 assert goal in cost,(a,b)
 path=[goal]
 while path[-1]!=start:path.append(parent[path[-1]])
 path.reverse();points=[path[0]]
 for i in range(1,len(path)-1):
  if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):points.append(path[i])
 points.append(path[-1]);return [[(x+.5)*cell,(y+.5)*cell]for x,y in points]
# Includes each district; no QA placement, only a legitimate ferry transfer between land masses.
groups=[[[2176,832],[2176,2400],[2256,2816],[3776,2832],[3200,3072],[2512,3312],[736,3040],[616,4072],[952,4080],[800,4168],[3064,3952],[3776,4096],[3968,4560]],[[3296,5216],[2800,5384],[3288,5568],[3520,5568],[3296,5056]]]
out=[]
for group in groups:
 out.append([dict(destination=b,points=route(a,b)[1:])for a,b in zip(group,group[1:])])
Path('docs/v10-production/walkthrough-routes.json').write_text(json.dumps(out,indent=2)+'\n');print('Planned',sum(len(x['points'])for g in out for x in g),'input waypoints')
