"""Collision ownership only: broaden visible bridge deck lanes. No source art/mask replacement."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'public';O=P/'assets/gate3/phase3bc-collision';O.mkdir(exist_ok=True)
m=json.loads((P/'assets/gate3/palace-cleanup-world/manifest.json').read_text());w,h=m['size'];patch=Image.new('L',(w,h));dr=ImageDraw.Draw(patch)
lanes=[{'id':'bridge-a-visible-east-deck','points':[[3390,3589],[3445,3609],[3491,3629],[3530,3640]],'width':21}, {'id':'bridge-b-visible-deck','points':[[3030,3923],[3053,3947],[3126,3974],[3199,4001],[3283,4017],[3370,4030],[3456,4044],[3542,4058],[3580,4059]],'width':21}]
for lane in lanes:dr.line([tuple(p)for p in lane['points']],fill=255,width=lane['width'],joint='curve')
a=np.array(patch)>0;changes=[]
for c in m['chunks']:
 x,y,cw,ch=[c[k]for k in ['x','y','width','height']];sub=a[y:y+ch,x:x+cw]
 if not sub.any():continue
 old=np.frombuffer((P/c['mask']).read_bytes(),np.uint8).reshape(ch,cw);new=old.copy();new[sub]=255
 if np.array_equal(old,new):continue
 path=O/(c['id']+'.bin');path.write_bytes(new.tobytes());changes.append({'id':c['id'],'originalMask':c['mask'],'originalSHA256':hashlib.sha256(old.tobytes()).hexdigest(),'mask':str(path.relative_to(P)),'sha256':hashlib.sha256(new.tobytes()).hexdigest(),'openedCells':int(((new>127)&(old<=127)).sum())})
record={'schemaVersion':1,'authority':'Phase3BC explicit local collision correction; source pixels, supports, old masks and world coordinates immutable','method':'21px native lane on visually inspected existing stone deck. No new paving, water crossing, pier/rail opening or bridge relocation. Main renderer dependencies/logical solids retained. Actual controls required.','lanes':lanes,'chunks':changes}
(R/'src/gate3/phase3bc-collision.json').write_text(json.dumps(record,indent=2)+'\n');(R/'docs/phase3bc/COLLISION_AMENDMENTS.json').write_text(json.dumps(record,indent=2)+'\n');print('Derived masks',len(changes),'new floor',sum(c['openedCells']for c in changes))
