"""Protected-wall amendment is ONLY a separately named playable comparison."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';O=R/'public/assets/gate3/residual-gate-proposal';O.mkdir(exist_ok=True);m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text());p=copy.deepcopy(m);p['id']='residual-gate-proposal';p['artStatus']='PROPOSAL ONLY / NOT ADOPTED /88px secondary opening needs explicit protected-wall approval';ob=next(o for o in p['objects']if o['id']=='reconciliation/palace-south-east');im=Image.open(R/'public'/ob['image']).convert('RGBA');a=np.array(im);a[:,2536-ob['x']:2624-ob['x'],3]=0;path=O/'south-wall-proposed-opening.png';Image.fromarray(a).save(path);ob['image']=str(path.relative_to(R/'public'))
for c in p['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];a=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w).copy();x1=max(x,2536);x2=min(x+w,2624);y1=max(y,1040);y2=min(y+h,1065)
 if x1<x2 and y1<y2:
  a[y1-y:y2-y,x1-x:x2-x]=255;out=O/(c['id']+'.bin');a.tofile(out);c['mask']=str(out.relative_to(R/'public'));c['maskSha256']=hashlib.sha256(out.read_bytes()).hexdigest()
p['reviewEntries']['archive-gate-proposal']=[2580,1110];p['nativeFrames']['archive-gate-proposal']=[2580,1020];g=Image.new('RGBA',p['size'])
for c in p['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
for o in sorted(p['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
g.thumbnail((870,973),Image.Resampling.NEAREST);g.save(O/'overview.png');p['overview']='assets/gate3/residual-gate-proposal/overview.png';(O/'manifest.json').write_text(json.dumps(p,indent=2)+'\n');(S/'archive-secondary-gate-proposal.json').write_text(json.dumps({'status':'PROPOSAL ONLY / NOT ADOPTED','supportOpening':[2536,1040,88,25],'roofProjectionRemoval':[2536,1016,88,49],'axisX':2580,'protectedWallFile':'UNCHANGED','liveMainField':'UNCHANGED','visualTreatment':'Unroofed88px secondary pedestrian opening. Native wall/paving retained, no invented tall gate in the20px archive setback. Fine end-cap detailing needs review if planning amendment is accepted.','scope':'Only one wall texture alpha gap and88x25 local collision change in explicit proposal scene; no other geometry or masterplan change.'},indent=2)+'\n');print('Archive88px proposal separated; approved wall/main collision unchanged')
