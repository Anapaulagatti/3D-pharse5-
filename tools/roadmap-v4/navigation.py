"""Independent conservative QA route guide from actual canonical masks and amendments, never a runtime collider."""
from pathlib import Path
import json,numpy as np,hashlib,subprocess
R=Path.cwd();m=json.load(open('public/assets/gate3/palace-cleanup-world/manifest.json'));w,h=m['size'];a=np.zeros((h,w),bool);over={}
for n in ['src/gate3/phase3bc-collision.json','src/gate3/v4-collision.json']:
 for c in json.load(open(n))['chunks']:over[c['id']]=c['mask']
for c in m['chunks']:
 x,y,cw,ch=[c[k]for k in ['x','y','width','height']];a[y:y+ch,x:x+cw]=np.frombuffer((R/'public'/over.get(c['id'],c['mask'])).read_bytes(),np.uint8).reshape(ch,cw)>127
for x,y,cw,ch in [[700,2593,35,12],[1112,2593,33,12],[1402,2593,33,12],[310,3333,33,11],[455,2350,30,130],[520,1094,34,284]]:a[y:y+ch,x:x+cw]=True
for s in m.get('logicalSolids',[]):
 x,y,cw,ch=s['rect'];a[int(np.ceil(y)):int(np.ceil(y+ch)),int(np.ceil(x)):int(np.ceil(x+cw))]=False
spec=m['contactCollision'];x,y,cw,ch=spec['rect'];p=np.frombuffer((R/'public'/spec['physical']).read_bytes(),np.uint8).reshape(ch,cw)>0;pad=64;pp=np.pad(p,pad,constant_values=True);valid=np.ones_like(p);offsets={(dx+sx,dy+sy)for key,pts in spec['footprints'].items()if key.startswith('run-')for dx,dy in pts for sx in [-2,0,2]for sy in [-2,0,2]}
for dx,dy in offsets:valid&=pp[pad+dy:pad+dy+ch,pad+dx:pad+dx+cw]
a[y:y+ch,x:x+cw]&=valid
(R/'.cache').mkdir(exist_ok=True);np.save('.cache/roadmap-v4-nav.npy',a);source=(R/'tools/roadmap-v2/nav_path.py').read_text().replace('.cache/roadmap-v2-nav.npy','.cache/roadmap-v4-nav.npy');(R/'tools/roadmap-v4/nav_path.py').write_text(source);(R/'docs/roadmap-v4/NAV_GUIDE.json').write_text(json.dumps({'testGuideOnly':True,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'walkable':int(a.sum()),'source':'Canonical masks +exact authorized amendments +native foot guard. Real keyboard traversal still mandatory.'},indent=2)+'\n');print('V4 independent guide',a.shape)
