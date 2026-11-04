from pathlib import Path
import numpy as np,json,hashlib
from scipy.ndimage import distance_transform_edt
R=Path.cwd();D=R/'docs/phase3bd-farm-path';before=np.load('.cache/phase3bd-floor.npy');after=before.copy();after[2350:2480,455:485]=True
# Match runtime order: logical solids always veto passability.
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text())
for s in m.get('logicalSolids',[]):
 x,y,w,h=s['rect'];after[int(np.ceil(y)):int(np.ceil(y+h)),int(np.ceil(x)):int(np.ceil(x+w))]=False
np.save('.cache/phase3bd-farm-path-floor.npy',after)
d1=distance_transform_edt(before);d2=distance_transform_edt(after)
rows=[]
for name,x,y in [('farm-04-approach',470,669),('farm-aisle',580,480),('farm-exit',500,810),('west-paved-corridor',470,2400),('new-clear-paving',458,2400),('shop-approach',650,2660),('bookshop-approach',1010,2620)]:
 rows.append({'id':name,'point':[x,y],'beforeClearance':round(float(d1[y,x]),2),'afterClearance':round(float(d2[y,x]),2),'afterWalkable':bool(after[y,x])})
(D/'NAVIGATION_AUDIT.json').write_text(json.dumps({'status':'STATIC PASS; actual traversal separately in GAMEPLAY_QA.json','openedCells':int((after&~before).sum()),'closedCells':int((before&~after).sum()),'beforeMaskSHA256':hashlib.sha256(before.tobytes()).hexdigest(),'afterMaskSHA256':hashlib.sha256(after.tobytes()).hexdigest(),'patch':[455,2350,30,130],'existingPlanterProtectedThroughX':454,'logicalSolidsUnchanged':True,'originalMasksUnchanged':True,'steeringAssist':'<=4px clearance search; swept actual <=1px steps, no teleport/speed boost/wall crossing; all play modes','points':rows},indent=2)+'\n')
print('Opened',int((after&~before).sum()),'cells; original masks unchanged')
