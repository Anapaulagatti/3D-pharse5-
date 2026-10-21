"""Road-only A* walkthrough authoring. No movement hooks, clocks or teleport calls."""
from city_geometry import *
from PIL import ImageChops
from scipy.ndimage import distance_transform_edt
import numpy as np,heapq,itertools
b=json.loads((SOURCE/'map/bundle.json').read_text());mask=route_mask(PLAN['roads']);d=ImageDraw.Draw(mask);d.line((2176,832,2176,2240),fill=255,width=112)
for path in (SOURCE/'layers').glob('court-*.png'):mask=ImageChops.lighter(mask,Image.open(path))
mask=ImageChops.lighter(mask,Image.open(SOURCE/'layers/civic-square.png'));allowed=np.array(mask)[::8,::8]>127;clearance=distance_transform_edt(allowed)
for s in b['collision']['solids']:
 if s['shape']!='rect':raise ValueError('Declare non-rect source collision explicitly')
 x0=max(0,math.ceil((s['x']-18)/8));y0=max(0,math.ceil((s['y']-14)/8));x1=min(W//8-1,math.floor((s['x']+s['w']+18)/8));y1=min(H//8-1,math.floor((s['y']+s['h']+14)/8));allowed[y0:y1+1,x0:x1+1]=False
rows,cols=allowed.shape

def snap(p):
 xx,yy=[round(v/8)for v in p];candidates=[]
 for y in range(max(0,yy-6),min(rows,yy+7)):
  for x in range(max(0,xx-6),min(cols,xx+7)):
   if allowed[y,x]:candidates.append((math.dist([x*8,y*8],p),(x,y)))
 if not candidates:raise ValueError(('No nearby public walk point',p))
 dist,point=min(candidates);assert dist<=32,(p,dist);return point

def route(start,end):
 a=snap(start);z=snap(end);q=[(0,0,a)];best={a:0};prev={};counter=itertools.count();visited=set()
 while q:
  _,__,node=heapq.heappop(q)
  if node in visited:continue
  visited.add(node)
  if node==z:break
  x,y=node
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
   nx,ny=x+dx,y+dy
   if not(0<=nx<cols and 0<=ny<rows and allowed[ny,nx]):continue
   if dx and dy and(not allowed[y,nx]or not allowed[ny,x]):continue
   cost=best[node]+math.hypot(dx,dy)*(1+.6/max(1,clearance[ny,nx]));n=(nx,ny)
   if cost>=best.get(n,1e99):continue
   best[n]=cost;prev[n]=node;heapq.heappush(q,(cost+math.dist(n,z),next(counter),n))
 else:raise ValueError(('No road-only route',start,end))
 points=[z]
 while points[-1]!=a:points.append(prev[points[-1]])
 points.reverse()
 def visible(a,z):
  steps=max(1,math.ceil(math.dist(a,z)*4))
  for i in range(steps+1):
   x=round(a[0]+(z[0]-a[0])*i/steps);y=round(a[1]+(z[1]-a[1])*i/steps)
   if not allowed[y,x]:return False
  return True
 # Preserve necessary corners. Skip only segments whose entire public surface is proven clear.
 compressed=[points[0]];i=1
 while i<len(points):
  far=i
  for j in range(i+1,len(points)):
   if not visible(compressed[-1],points[j]):break
   far=j
  compressed.append(points[far]);i=far+1
 return [[x*8,y*8]for x,y in compressed]


tour=[('heritage-gateway',[2176,2240],None),('grocery',[1280,2784],'interact'),('bookshop',[1648,2784],None),('community-classroom',[2016,2784],'interact'),('gateway-reading-house',[2544,2784],None),('bakery',[1280,3280],'interact'),('public-service',[800,3280],None),('civic-meeting',[2176,3056],'celebrate'),('station',[1376,3960],'interact'),('design-gallery',[2192,3968],'interact'),('transit-stop',[2224,3648],None),('namsan-entrance',[2992,3152],None),('tower',[3520,2904],'interact'),('east-scenic-loop',[4000,3144],None),('park-pavilion',[3704,3272],None),('south-scenic-loop',[3152,3304],None),('visitor-information',[3872,3744],'interact'),('observation-wheel',[3136,3920],'wave'),('carousel',[3840,4216],'celebrate'),('discovery-hall',[3776,4536],'interact'),('east-waterfront-gateway',[4032,4560],None),('leisure-main-gate',[3216,4592],None),('coastal-lookout',[1392,4256],None),('coastal-cafe',[672,4256],'interact'),('mainland-boarding',PLAN['travel']['mainlandTrigger'],'ferry'),('jeju-village',[1296,5904],'interact'),('jeju-nature',[1856,5872],'interact'),('basalt-discovery',PLAN['travel']['discovery'],'discovery'),('oreum',[1280,5584],'interact'),('cliff-lookout',[672,5744],'interact'),('jeju-return-boarding',PLAN['travel']['islandTrigger'],'ferry')]
start=[2176,832];segments=[]
for id,point,action in tour:
 points=route(start,point);segments.append({'id':id,'requested':point,'points':points,'action':action});start=PLAN['travel']['islandArrival']if id=='mainland-boarding'else PLAN['travel']['mainlandArrival']if id=='jeju-return-boarding'else points[-1]
length=round(sum(sum(math.dist(a,z)for a,z in zip(s['points'],s['points'][1:]))for s in segments));write(SOURCE/'plan/walkthrough.json',{'method':'Road/court-only8px A*, actual18×14px safety envelope (more conservative than Juni8×4px) and current source solids. Input driver only; no runtime movement hooks.','sourceBundleSha256':sha(SOURCE/'map/bundle.json'),'visits':segments,'lengthPx':length,'nominalRunSeconds':round(length/100)});print('Planned public-route tour:',len(segments),'visits,',length,'px;',round(length/100),'nominal run seconds before natural pauses')
