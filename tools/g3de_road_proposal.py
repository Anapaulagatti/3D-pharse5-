"""ISOLATED PROPOSAL ONLY: never changes main candidate or canonical source."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';O=R/'public/assets/gate3/residual-road-proposal';O.mkdir(exist_ok=True);m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text());p=copy.deepcopy(m);p['id']='residual-road-proposal';p['artStatus']='PROPOSAL ONLY / NOT ADOPTED / protected canonical asphalt native-restoration exception requires human approval';g=Image.new('RGBA',m['size'])
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
old=g.copy();src=Image.open(R/'assets-src/gate2/originals/station.png').convert('RGBA');material=Image.new('RGBA',(684,58));material.paste(src.crop((820,1010,1160,1068)),(0,0));material.paste(src.crop((850,1020,1194,1078)),(340,0));material.save(S/'road-proposal-native-material.png')
box=(2274,2755,2958,2813);a=np.array(g.crop(box));r,gg,b=[a[:,:,i].astype(float)for i in range(3)];mask=(r<130)&(gg<140)&(b<150)&(abs(r-gg)<20)&(b>r*.8);mask&=~((gg>r*1.1)&(gg>b*1.1));mask=np.array(mask);imask=Image.fromarray(mask.astype('uint8')*255);g.paste(material,(2274,2755),imask);imask.save(S/'road-proposal-only-mask.png')
for c in p['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];a=g.crop((x,y,x+w,y+h))
 if a.tobytes()!=old.crop((x,y,x+w,y+h)).tobytes():
  path=O/(c['id']+'.png');a.save(path);c['image']=str(path.relative_to(R/'public'));c['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
# Paving/curb/tactile and marks outside explicit asphalt mask remain exact.
assert np.array_equal(np.array(g.crop((2274,2603,2958,2755))),np.array(old.crop((2274,2603,2958,2755))))
a=np.array(g.crop(box));b=np.array(old.crop(box));assert np.array_equal(a[~mask],b[~mask])
over=g.copy()
for o in sorted(p['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');p['overview']='assets/gate3/residual-road-proposal/overview.png';(O/'manifest.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(S/'road-proposal-only.json').write_text(json.dumps({'status':'PROPOSAL ONLY / NOT ADOPTED IN MAIN','protectedRoadRect':[2274,2755,684,58],'changedAsphaltPixels':int(mask.sum()),'nativeSource':'assets-src/gate2/originals/station.png','samples':[[820,1010,340,58],[850,1020,344,58]],'canonicalPNG':'UNCHANGED','mainCandidate':'UNCHANGED','unchanged':'Forecourt paving/curb/tactile/crosswalk/lane markings/foliage outside mask, all architecture/props/registration/collision','requires':'Explicit human exception for derived native protected-road material restoration; not permission for geometry or world expansion','scope':'Historical baked source softness/material phase only; no renderer sharpening/recolor/filter/upscale.'},indent=2)+'\n')
print('Isolated protected-road proposal prepared:',int(mask.sum()),'asphalt pixels; main unchanged')
