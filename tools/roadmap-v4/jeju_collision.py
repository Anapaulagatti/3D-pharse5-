"""Owner V4 P0-5: local anchor-mask continuation on EXISTING painted bridge-to-island paving. No art writes."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path.cwd();D=R/'docs/roadmap-v4';m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());old={r['id']:r['mask']for r in json.loads((R/'src/gate3/phase3bc-collision.json').read_text())['chunks']};W,H=m['size'];patch=Image.new('L',(W,H));d=ImageDraw.Draw(patch)
# Existing approved island-side horizontal paving, not roof/orchard/cliff. Source house-direct-approach translated by3180,3200.
points=[(3568,4063),(3615,4060),(3650,4065),(3690,4070),(3720,4065)];d.line(points,fill=255,width=24,joint='curve')
for x,y in points:d.ellipse((x-12,y-12,x+12,y+12),fill=255)
# Keep this bounded to the existing island-side deck; protected support/water below4079 are excluded.
pa=np.asarray(patch).copy();pa[:4045]=0;pa[4079:]=0;pa[:,:3568]=0;pa[:,3734:]=0
rows=[]
for c in m['chunks']:
 x,y,w,h=c['x'],c['y'],c['width'],c['height'];roi=pa[y:y+h,x:x+w]>0
 if not roi.any():continue
 name=old.get(c['id'],c['mask']);raw=(R/'public'/name).read_bytes();before=np.frombuffer(raw,np.uint8).reshape(h,w);after=before.copy();after[roi]=255
 if np.array_equal(before,after):continue
 out='assets/roadmap-v4/collision/'+c['id']+'.bin';(R/'public'/out).write_bytes(after.tobytes());changed=after!=before;assert not np.any(changed&~roi)
 rows.append(dict(id=c['id'],originalMask=name,originalSHA256=hashlib.sha256(raw).hexdigest(),mask=out,sha256=hashlib.sha256(after.tobytes()).hexdigest(),openedCells=int(changed.sum()),closedCells=0,outsideROICells=0))
q={'schemaVersion':1,'authority':'Owner V4 2026-11-10 P0-5 exact redpath; original art/bridge/house and mask sources immutable','rootCause':'Original island-side anchor field rejects part of already painted horizontal paving between approved bridgeB end and house-direct-approach. Baseline actual WASD stops x3606.9668,y4059.9424; first candidate outward traversal exposed the remaining3580..3583 edge gap at(3580.47,4064.75). Corridor now overlaps old deck floor at3568,4063. Earlier coarsecurve target crossed insidehouse; correctedsourcecanonicalcurve itself traverses, junctionstillblocks.','ROI':[3568,4045,166,34],'anchorCorridorWidth':24,'points':points,'sourceRoute':'public/assets/gate2/c/scene.json house-direct-approach; sourceoffset[3180,3200]','chunks':rows,'artFilesChanged':0,'originalMaskFilesChanged':0,'physicalNativeContactChanged':False,'protectedLogicalSolidsChanged':False}
(R/'src/gate3/v4-collision.json').write_text(json.dumps(q,indent=2)+'\n');(D/'JEJU_COLLISION_AMENDMENT.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
