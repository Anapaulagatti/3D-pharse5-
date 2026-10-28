"""Read-only QA walking route, not an amendment to world plans or NPC patrols."""
from pathlib import Path
import runpy,heapq,json
R=Path(__file__).resolve().parents[2];ctx=runpy.run_path(str(Path(__file__).with_name('navigation_qa.py')));clear=ctx['clear'];grid=clear[2::4,::4];start=(1128//4,(2690-2)//4);goal=(2464//4,(2690-2)//4);assert grid[start[1],start[0]]and grid[goal[1],goal[0]]
q=[(0,0,start)];g={start:0};prev={};found=False
while q:
 _,cost,p=heapq.heappop(q)
 if cost!=g[p]:continue
 if p==goal:found=True;break
 for dx,dy in[(1,0),(-1,0),(0,1),(0,-1)]:
  n=p[0]+dx,p[1]+dy
  if not(0<=n[0]<grid.shape[1]and 0<=n[1]<grid.shape[0])or not grid[n[1],n[0]]:continue
  c=cost+1
  if c<g.get(n,10**12):g[n]=c;prev[n]=p;heapq.heappush(q,(c+abs(n[0]-goal[0])+abs(n[1]-goal[1]),c,n))
assert found;path=[goal]
while path[-1]!=start:path.append(prev[path[-1]])
path.reverse();points=[path[0]]
for i in range(1,len(path)-1):
 if(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):points.append(path[i])
points.append(path[-1]);world=[[x*4,y*4+2]for x,y in points];out={'world':'palace-cleanup-world','start':world[0],'goal':world[-1],'waypoints':world,'pixels':(len(path)-1)*4,'method':'A* conservative29x9 contact on existing masks/logicalSolids; QA driver only, no world/NPC route edits'};(R/'docs/phase3a-npc-expansion/urban-traversal-plan.json').write_text(json.dumps(out,indent=2)+'\n');print(len(world),'corners',out['pixels'],'pixels per one-way path')
