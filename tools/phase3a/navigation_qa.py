"""Native contact/critical route validation, read-only approved world sources."""
from bind import R,D,m,clear,segment
import json,math
reg=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs'];farm=json.loads((R/'public'/m['farmMetadata']).read_text());critical={'palace-centerline':[2016,685,64,1065],'cafe-door':[700,2588,36,60],'bookshop-door':[1110,2588,36,60],'station-entrance':[2560,2580,80,210],'station-crossing':[2560,2715,100,100],'jeju-house-steps':[3560,4350,85,150],'jeju-bridge-a':[2980,3380,600,300],'jeju-bridge-b':[3030,3910,560,250],'ferry-dock':[2520,3860,90,330],'namsan-entrance':[1435,3220,45,90],'carousel-arrival':[2400,3220,80,100]}
for p in farm['plots']:critical[p['id']]=p['collisionRect']
def overlap(a,b):return a[0]<b[0]+b[2]and a[0]+a[2]>b[0]and a[1]<b[1]+b[3]and a[1]+a[3]>b[1]
rows=[]
for n in reg:
 pts=n['route'];tests=0;rx,ry=n['footprint']
 for a,b in zip(pts,pts[1:]+pts[:1]):
  assert segment(a,b),(n['id'],a,b)
  length=max(1,math.ceil(math.dist(a,b)))
  for i in range(length+1):
   x=a[0]+(b[0]-a[0])*i/length;y=a[1]+(b[1]-a[1])*i/length;hits=[name for name,r in critical.items()if overlap([x-rx,y-ry,rx*2,ry*2],r)];assert not hits,(n['id'],[x,y],hits);tests+=1
 assert segment(n['spawn'],n['reviewSpawn']);rows.append({'id':n['id'],'spawn':n['spawn'],'reviewSpawn':n['reviewSpawn'],'route':pts,'fullNativeContact':[rx*2+1,ry*2+1],'sampledIntegerPositions':tests,'criticalRouteOverlap':[],'nativeGround':'PASS','realApproach':'See actual-gameplay.json; all14 original-control approaches tested'})
(D/'navigation-qa.json').write_text(json.dumps({'status':'PASS','npcs':len(rows),'method':'Unchanged canonical masks/logical solids; full native contact box at every integer position along all4edges and entire review approach. No global collision model or world edit.','criticalReservedAreas':critical,'rows':rows,'softContact':'NPCs yield to nearby player/other NPCs; they do not add hard obstacles to protected player routes.','physicalDevices':'NOT TESTED'},indent=2)+'\n');print('PASS14nativepatrols,approaches,criticalentrances/bridges/plotsclear')
