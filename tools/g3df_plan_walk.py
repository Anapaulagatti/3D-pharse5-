from pathlib import Path
import json,heapq,math
import numpy as np
from scipy.ndimage import minimum_filter,binary_erosion,distance_transform_edt
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-alignment';m=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text());W,H=m['size'];field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
sp=m['contactCollision'];ox,oy,w,h=sp['rect'];physical=np.fromfile(R/'public'/sp['physical'],np.uint8).reshape(h,w);valid={};bounds=[ox,oy,ox+w,oy+h]
for direction in ['left','right','front','back']:
 a=np.ones((h,w),bool)
 for dx,dy in sp['footprints']['walk-'+direction]:
  shifted=np.ones((h,w),bool);x1=max(0,-dx);x2=min(w,w-dx);y1=max(0,-dy);y2=min(h,h-dy);shifted[y1:y2,x1:x2]=physical[y1+dy:y2+dy,x1+dx:x2+dx]>0;a&=shifted
 valid[direction]=a
start=(2048,1090);legs=[]
def add(id,points,requested=None):
 global start
 if points[0]!=list(start):points=[list(start)]+points
 for x,y in points:assert field[y,x],(id,x,y)
 legs.append({'id':id,'requestedTarget':requested or points[-1],'reachedGridTarget':points[-1],'points':points,'lengthPx':sum(math.dist(a,b)for a,b in zip(points,points[1:]))});start=tuple(points[-1])
def astar(s,t,local=False):
 G=1 if local else 4
 x0,y0,x1,y1=(2980,3380,3740,3880)if local else(0,0,W,H)
 # Native guard tested at every1px of each step, not just endpoint connectivity.
 def allowed(x,y,d):
  if not(x0<=x<x1 and y0<=y<y1)or not field[y,x]:return False
  return not(ox<=x<ox+w and oy<=y<oy+h)or valid[d][y-oy,x-ox]
 def snap(pt):
  x,y=pt;out=[]
  for dy in range(-12,13):
   for dx in range(-12,13):
    xx=round((x+dx)/G)*G;yy=round((y+dy)/G)*G
    if x0<=xx<x1 and y0<=yy<y1 and field[yy,xx]:out.append(((xx-x)**2+(yy-y)**2,(xx,yy)))
  return min(out)[1]
 s=snap(s);t=snap(t);heap=[(0,0,s)];cost={s:0};parent={};arrived={s:None}
 while heap:
  _,g,u=heapq.heappop(heap)
  if u==t:break
  if g!=cost[u]:continue
  for dx,dy,d in [(G,0,'right'),(-G,0,'left'),(0,G,'front'),(0,-G,'back')]:
   v=(u[0]+dx,u[1]+dy)
   if not all(allowed(round(u[0]+dx*k/G),round(u[1]+dy*k/G),d)for k in range(G+1)):continue
   ng=g+G+(6 if local and arrived[u] is not None and arrived[u]!=d else 0)
   if ng<cost.get(v,1e20):cost[v]=ng;parent[v]=u;arrived[v]=d;heapq.heappush(heap,(ng+abs(v[0]-t[0])+abs(v[1]-t[1]),ng,v))
 else:raise ValueError(('No real native-contact route',s,t,local))
 path=[t]
 while path[-1]!=s:path.append(parent[path[-1]])
 path.reverse();out=[list(path[0])];last=None
 for i in range(1,len(path)):
  d=(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])
  if last is not None and d!=last:out.append(list(path[i-1]))
  last=d
 out.append(list(path[-1]));return out
add('palace-entrance',[[2048,1090],[2048,810],[2048,685]])
add('archive-entrance',[[2048,685],[2048,1030],[2580,1030],[2580,923]])
add('palace-exit',[[2580,923],[2580,1030],[2048,1030],[2048,1090]])
add('station-approach',astar(start,(2598,2630)))
add('station-public-threshold',[list(start),[2598,2630],[2598,2610]])
add('station-exit',[list(start),[2598,2760]])
add('mainland-landing',astar(start,(3130,3460)))
add('complete-bridge-to-jeju',astar(start,(3530,3640),True),[3500,3610])
(D/'walk-plan.json').write_text(json.dumps({'method':'Actual current fields and atlas-derived directional contact guards. Palace/archive use exact measured entrances. Complete bridge route constrained to the upper bridge ROI, not alternative island connectivity. All motion later validated via real controls.','legs':legs,'totalLengthPx':sum(l['lengthPx']for l in legs)},indent=2)+'\n')
print('Planned',len(legs),'legs;',round(sum(l['lengthPx']for l in legs)),'pixels;',len(legs[-1]['points']),'bridge turns')
