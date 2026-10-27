"""Conservative plan from unchanged canonical collision for real-input integration evidence."""
from bind import *
from scipy.ndimage import distance_transform_edt
# Overlay the existing physical guard in analysis only, then erode for player contact.
spec=m['contactCollision'];x,y,ww,hh=spec['rect'];physical=np.fromfile(R/'public'/spec['physical'],np.uint8).reshape(hh,ww)>0
padX=40;padY=12;padded=np.pad(physical,((padY,padY),(padX,padX)),constant_values=True);guard=np.ones_like(physical)
for dx,dy in set(tuple(p)for key,pts in spec['footprints'].items()if key.startswith('walk-')for p in pts):guard&=padded[padY+dy:padY+dy+hh,padX+dx:padX+dx+ww]
safe=field>127;safe[y:y+hh,x:x+ww]&=guard
clearance=distance_transform_edt(safe)
STEP=2
def path(start,end):
 a=tuple(round(v/STEP)for v in start);b=tuple(round(v/STEP)for v in end);assert safe[a[1]*STEP,a[0]*STEP]and safe[b[1]*STEP,b[0]*STEP],(start,end);todo=[(0,a)];cost={a:0};prev={};closed=set()
 while todo:
  _,u=heapq.heappop(todo)
  if u in closed:continue
  closed.add(u)
  if u==b:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   v=(u[0]+dx,u[1]+dy)
   if not(0<=v[0]*STEP<w and 0<=v[1]*STEP<h)or not safe[v[1]*STEP,v[0]*STEP]:continue
   if not all(safe[u[1]*STEP+dy*i,u[0]*STEP+dx*i]for i in range(STEP+1)):continue
   c=cost[u]+1+40/(clearance[v[1]*STEP,v[0]*STEP]+1)**2
   if c<cost.get(v,10**9):cost[v]=c;prev[v]=u;heapq.heappush(todo,(c+abs(v[0]-b[0])+abs(v[1]-b[1]),v))
 assert b in cost,(start,end,'unreachable');seq=[b]
 while seq[-1]!=a:seq.append(prev[seq[-1]])
 seq=seq[::-1];out=[seq[0]]
 for i in range(1,len(seq)-1):
  if(seq[i][0]-seq[i-1][0],seq[i][1]-seq[i-1][1])!=(seq[i+1][0]-seq[i][0],seq[i+1][1]-seq[i][1]):out.append(seq[i])
 out.append(seq[-1]);return [[x*STEP,y*STEP]for x,y in out]
# Start on mainland ferry public approach, cross approved northern bridgeA, visit house and orchard.
anchors=[[3010,3460],[2990,3490],[3812,4072],[3668,4396]];out=[]
for a,b in zip(anchors,anchors[1:]):
 seq=path(a,b);out+=seq if not out else seq[1:]
raw=out[:]
def clearLine(a,b):
 n=max(1,math.ceil(math.dist(a,b)));return all(clearance[round(a[1]+(b[1]-a[1])*i/n),round(a[0]+(b[0]-a[0])*i/n)]>=2 for i in range(n+1))
smooth=[out[0]];i=0
while i<len(out)-1:
 found=False
 for j in range(len(out)-1,i,-1):
  a=out[i];b=out[j]
  for elbow in [[b[0],a[1]],[a[0],b[1]]]:
   if clearLine(a,elbow)and clearLine(elbow,b):
    if elbow!=smooth[-1]:smooth.append(elbow)
    if b!=smooth[-1]:smooth.append(b)
    i=j;found=True;break
  if found:break
 if not found:
  i+=1;smooth.append(out[i])
out=smooth
length=sum(math.dist(a,b)for a,b in zip(out,out[1:]));(D/'cross-zone-route.json').write_text(json.dumps({'policy':'Canonical player walkable-point masks/logical solids plus existing local bridge physical guard only; no map edits. A* is offline QA planning,not a new runtime world model. Real player input follows these exact axis segments.','anchors':anchors,'waypoints':[[a,b,.4 if clearance[b,a]<3 else 1.7]for a,b in out],'distancePixels':length,'nominalWalkSeconds':length/60,'rawGridCorners':len(raw),'clearancePolicy':'Weighted A* plus verified axis-aligned shortcuts; every original native guard/mask point respected; minimum2px plan clearance; original control fine alignment only','bridge':'Approved northern Jeju bridgeA; mainland promenade → cultural house → orchard approach'},indent=2)+'\n');print('PASScross-zone plan',len(out),'corners',length,'px')
