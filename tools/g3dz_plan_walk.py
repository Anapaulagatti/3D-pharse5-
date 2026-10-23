from pathlib import Path
import json,heapq,math
import numpy as np
from scipy.ndimage import label,binary_erosion
R=Path(__file__).resolve().parents[1];m=json.loads((R/'public/assets/gate3/zoned-world/manifest.json').read_text());W,H=m['size'];a=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];a[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
G=4;a=binary_erosion(a>127,iterations=10).astype("uint8")*255;small=a.reshape(H//G,G,W//G,G).min(axis=(1,3))>127;labs,n=label(small);start=(2048//G,1930//G);component=labs[start[1],start[0]];assert component
h,w=small.shape

def snap(pt):
 x,y=[round(v/G)for v in pt];opts=[]
 for dy in range(-18,19):
  for dx in range(-18,19):
   xx,yy=x+dx,y+dy
   if 0<=xx<w and 0<=yy<h and labs[yy,xx]==component:opts.append(((xx*G-pt[0])**2+(yy*G-pt[1])**2,(xx,yy)))
 assert opts,pt
 return min(opts)[1]
def path(s,t):
 heap=[(0,0,s)];cost={s:0};parent={}
 while heap:
  _,g,u=heapq.heappop(heap)
  if u==t:break
  if g!=cost[u]:continue
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   v=(u[0]+dx,u[1]+dy)
   if not (0<=v[0]<w and 0<=v[1]<h and small[v[1],v[0]]):continue
   ng=g+1
   if ng<cost.get(v,1e20):cost[v]=ng;parent[v]=u;heapq.heappush(heap,(ng+abs(v[0]-t[0])+abs(v[1]-t[1]),ng,v))
 else:raise ValueError((s,t))
 result=[t]
 while result[-1]!=s:result.append(parent[result[-1]])
 result.reverse();out=[result[0]];last=None
 for i in range(1,len(result)):
  direction=(result[i][0]-result[i-1][0],result[i][1]-result[i-1][1])
  if last is not None and direction!=last:out.append(result[i-1])
  last=direction
 out.append(result[-1]);return [[x*G+2,y*G+2]for x,y in out],(len(result)-1)*G
sequence=[('palace',[2048,990]),('archive',[2320,1110]),('culture',[2610,1550]),('academy',[800,1500]),('retail',[1128,2690]),('station',[2598,2760]),('amusement',[2440,3260]),('namsan',[1460,3260]),('maru',[326,3380]),('market',[1440,3740]),('market-entry',[910,3680]),('ferry',[2900,3480]),('ferry-entry',[2560,3760]),('jeju-arrival',[3500,3610]),('oreum',[3730,3335]),('orchard',[3960,4080]),('house',[3590,4390])];legs=[]
for name,pt in sequence:
 t=snap(pt);points,length=path(start,t);legs.append({'id':name,'requestedTarget':pt,'reachedGridTarget':list(points[-1]),'points':points,'lengthPx':length,'minimumRunSeconds':length/100});start=t
out={'grid':G,'method':'Offline A* over10px eroded actual masks, conservative min4x4 samples; driver clearance only, not full Juni body; real movement must validate','legs':legs,'totalLengthPx':sum(x['lengthPx']for x in legs)};(R/'docs/gate3-zoned-world/walk-plan.json').write_text(json.dumps(out,indent=2)+'\n');print('Planned',len(legs),'legs;',out['totalLengthPx'],'pixels;',sum(len(l['points'])for l in legs),'waypoints')
