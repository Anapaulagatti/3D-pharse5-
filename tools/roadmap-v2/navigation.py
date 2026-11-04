from pathlib import Path
import json,numpy as np,hashlib
R=Path.cwd();a=np.load('.cache/phase3bd-final-quality-floor.npy').copy();m=json.load(open('public/assets/gate3/palace-cleanup-world/manifest.json'));spec=m['contactCollision'];x,y,w,h=spec['rect'];p=np.frombuffer((R/'public'/spec['physical']).read_bytes(),dtype=np.uint8).reshape(h,w)>0
# Exact union of accepted native run footprints, plus2pxguide safety. This is test routing only, never an altered game collider.
offsets={(dx+sx,dy+sy)for key,pts in spec['footprints'].items()if key.startswith('run-')for dx,dy in pts for sx in [-2,0,2]for sy in [-2,0,2]};pad=64;pp=np.pad(p,pad,constant_values=True);valid=np.ones_like(p)
for dx,dy in offsets:valid&=pp[pad+dy:pad+dy+h,pad+dx:pad+dx+w]
a[y:y+h,x:x+w]&=valid
np.save('.cache/roadmap-v2-nav.npy',a)
Path('docs/roadmap-v2/NAV_GUIDE.json').write_text(json.dumps({'status':'GUIDE ONLY; actual control traces required','footprints':'Accepted run union +2px guide safety, source runtime unchanged','floorSHA256':hashlib.sha256(a.tobytes()).hexdigest(),'contactRect':spec['rect']},indent=2)+'\n')
p=Path('tools/phase3bd-final-quality/path.py').read_text().replace('.cache/phase3bd-final-quality-floor.npy','.cache/roadmap-v2-nav.npy');Path('tools/roadmap-v2/nav_path.py').write_text(p)
