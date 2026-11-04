from pathlib import Path
import json,hashlib,numpy as np
R=Path.cwd();D=R/'docs/phase3bd-final-quality';before=np.load('.cache/phase3bd-farm-path-floor.npy');after=before.copy();after[1094:1378,520:554]=True
m=json.load(open('public/assets/gate3/palace-cleanup-world/manifest.json'))
for s in m.get('logicalSolids',[]):
 x,y,w,h=s['rect'];after[int(np.ceil(y)):int(np.ceil(y+h)),int(np.ceil(x)):int(np.ceil(x+w))]=False
np.save('.cache/phase3bd-final-quality-floor.npy',after)
report={'beforeSHA256':hashlib.sha256(before.tobytes()).hexdigest(),'afterSHA256':hashlib.sha256(after.tobytes()).hexdigest(),'actualReproduction':'HANOK_BEFORE_QA.json: W blocked at(534.0768,1376.9996)','runtimeBlocker':'WorldCache canonical per-pixel anchor mask, not Arcade/Matter; nativeContact guard currently covers bridge approachrect[2980,3380,600,300], not this hanok. No actor collider offset or camera root cause found.','rootCause':'west-hanok repaint kept all old collision cells exact; legacy reservation still marks visible side paving as blocked atx474.. while new image shows pathx~490..580','newAnchorCorridor':[520,1094,34,284],'physicalFootBounds':[-27,-4,24,-1],'edgeSafetyPx':3,'visibleStoneX':[490,580],'newOpenedCells':int((after&~before).sum()),'closedCells':int((before&~after).sum()),'outsideROIChanges':int(np.any(after!=before)and np.count_nonzero((after!=before)&~np.pad(np.ones((284,34),bool),((1094,after.shape[0]-1378),(520,after.shape[1]-554))))),'artChanges':0,'maskFilesChanged':0,'sampleSemantics':[{'point':[x,y],'before':bool(before[y,x]),'after':bool(after[y,x])}for x,y in [(534,1370),(534,1200),(534,1096),(600,1200),(640,1200),(495,1200),(574,1200)]]}
(D/'HANOK_COLLISION_DIAGNOSIS.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
