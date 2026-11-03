"""Read canonical native masks, including logical station footprint and native-contact guard.
No artwork rewrite. Reports connected components and practical anchor clearance separately.
"""
from pathlib import Path
import json, numpy as np
from scipy.ndimage import label, distance_transform_edt, binary_erosion
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd';P=R/'public'
m=json.loads((P/'assets/gate3/palace-cleanup-world/manifest.json').read_text());amend=json.loads((R/'src/gate3/phase3bc-collision.json').read_text());changes={c['id']:c['mask']for c in amend['chunks']}
for c in m['chunks']:c['mask']=changes.get(c['id'],c['mask'])
w,h=m['size'];floor=np.zeros((h,w),bool)
for c in m['chunks']:
 a=np.frombuffer((P/c['mask']).read_bytes(),np.uint8).reshape(c['height'],c['width'])>127
 floor[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']]=a
for s in m.get('logicalSolids',[]):
 x,y,rw,rh=s['rect'];floor[int(np.ceil(y)):int(np.ceil(y+rh)),int(np.ceil(x)):int(np.ceil(x+rw))]=False
# Ground mask is an anchor field, not a sprite-bounds box. Additional foot support is local.
if 'contactCollision' in m:
 spec=m['contactCollision']; x,y,cw,ch=spec['rect']; contact=np.frombuffer((P/spec['physical']).read_bytes(),np.uint8).reshape(ch,cw)>0
 allowed=np.ones_like(contact)
 offsets=set(tuple(p) for v in spec['footprints'].values() for p in v)
 # Union all walk/run directions produces conservative diagnostic, runtime uses actual direction.
 for dx,dy in offsets:
  shifted=np.ones_like(contact); sy0=max(0,dy);sy1=min(ch,ch+dy);sx0=max(0,dx);sx1=min(cw,cw+dx)
  shifted[sy0-dy:sy1-dy,sx0-dx:sx1-dx]=contact[sy0:sy1,sx0:sx1];allowed &= shifted
 floor[y:y+ch,x:x+cw] &= allowed
before=floor.copy()
repairs=[(700,2593,35,12),(1112,2593,33,12),(1402,2593,33,12),(310,3333,33,11)]
for x,y,rw,rh in repairs: floor[y:y+rh,x:x+rw]=True
labels,n=label(floor);counts=np.bincount(labels.ravel());main=int(np.argmax(counts[1:])+1)
distance=distance_transform_edt(floor)
points={**m['reviewEntries'],**{t['id']:[t['x'],t['y']] for t in m['targets']}}
for p in json.loads((P/'assets/gate3/final-world/farm-plots.json').read_text())['plots']:points[p['id']]=p['interactionAnchor']
for x in [3900,3930,3960]:points[f'quest-orchard-{x}']=[x,4080 if x>3900 else 4070]
report=[]
for name,(x,y) in points.items():
 x,y=round(x),round(y); component=int(labels[y,x]);report.append({'id':name,'point':[x,y],'walkable':bool(floor[y,x]),'component':component,'mainConnected':component==main,'anchorClearancePx':round(float(distance[y,x]),2),'status':'PASS' if component==main and distance[y,x]>=8 else 'WARN_NARROW' if component==main else 'FAIL_UNREACHABLE'})
rgba=np.zeros((h,w,3),np.uint8);rgba[floor]=[65,112,83];rgba[labels==main]=[120,180,137];rgba[floor&(distance<8)]=[225,170,60]
img=Image.fromarray(rgba);draw=ImageDraw.Draw(img)
for p in report:
 x,y=p['point'];draw.ellipse((x-5,y-5,x+5,y+5),fill='white' if p['mainConnected'] else 'red')
img.save(D/'COLLISION_NATIVE.png')
np.save(R/'.cache/phase3bd-floor.npy',floor)
(D/'NAVIGATION_AUDIT.json').write_text(json.dumps({'method':'All native anchor masks + logical solids + conservative all-direction local native foot support. Runtime is direction-specific. 8px radial anchor margin is diagnostic, not a new 96px sprite body. No generic dilation opens water/buildings.','size':[w,h],'components':n,'mainPixels':int(counts[main]),'collisionOnlyOpenedCells':int((floor&~before).sum()),'repairs':[list(r) for r in repairs],'points':report},indent=2)+'\n')
print('Native anchor audit',len(report),'points',n,'components');print('\n'.join(str(p) for p in report if p['status']!='PASS'))
