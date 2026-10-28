"""Independent read-only conservative29x9 native contact on canonical masks/solids."""
from pathlib import Path
import json,math,numpy as np
from scipy.ndimage import minimum_filter1d
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());w,h=m['size'];field=np.zeros((h,w),np.uint8)
for c in m['chunks']:field[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(c['height'],c['width'])
for o in m['logicalSolids']:
 x,y,ww,hh=o['rect'];field[math.floor(y):math.ceil(y+hh),math.floor(x):math.ceil(x+ww)]=0
clear=minimum_filter1d(minimum_filter1d(field,size=29,axis=1,mode='constant'),size=9,axis=0,mode='constant')>127
regs=json.loads((R/'assets-src/npcs/phase3a-final-six/definitions.json').read_text())['npcs'];critical=json.loads((R/'docs/phase3a/navigation-qa.json').read_text())['criticalReservedAreas'];rows=[]
def overlap(a,b):return a[0]<b[0]+b[2]and a[0]+a[2]>b[0]and a[1]<b[1]+b[3]and a[1]+a[3]>b[1]
for n in regs:
 tests=0;hits=[]
 for a,b in list(zip(n['route'],n['route'][1:]+n['route'][:1]))+[(n['spawn'],n['reviewSpawn'])]:
  length=max(1,math.ceil(math.dist(a,b)))
  for i in range(length+1):
   x=a[0]+(b[0]-a[0])*i/length;y=a[1]+(b[1]-a[1])*i/length;assert clear[round(y),round(x)],(n['id'],x,y,'blocked native contact');tests+=1
 # Reservations apply to patrol positions; a player approach is allowed to cross public arrival space.
 for a,b in zip(n['route'],n['route'][1:]+n['route'][:1]):
  length=max(1,math.ceil(math.dist(a,b)))
  for i in range(length+1):
   x=a[0]+(b[0]-a[0])*i/length;y=a[1]+(b[1]-a[1])*i/length
   for id,rect in critical.items():
    if overlap([x-14,y-4,28,8],rect):hits.append(id)
 assert not hits,(n['id'],hits)
 rows.append({'id':n['id'],'sampledContactPositions':tests,'nativeContact':[29,9],'patrolCriticalOverlaps':hits,'groundAndLogicalSolids':'PASS','approach':'PASS','route':n['route']})
(D/'navigation-qa.json').write_text(json.dumps({'status':'PASS scoped six historical art-candidate routes','npcs':6,'rows':rows,'worldSource':'Unmodified canonical masks and logicalSolids','worldEdits':[],'station8pxStrip':'UNCHANGED; no platform-transfer fix claimed','historical6':'Six source-gated art candidates only; verified historical content remains BLOCKED','bakery':'Unplaced planning decision untouched'},indent=2)+'\n');print('PASS6 complete conservative patrols/approaches and protected entrance/reservation checks')
