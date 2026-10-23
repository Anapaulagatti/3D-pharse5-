"""Restore rejected platform visuals without reverting accepted Working V3 amendments."""
from pathlib import Path
import json,subprocess,copy,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-platform-restoration';D.mkdir(exist_ok=True)
def write(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def historic(p):return json.loads(subprocess.check_output(['git','show','5afd77a:'+p],cwd=R))
path='public/assets/gate3/registration-working-v3/manifest.json';m=historic(path);before=json.loads((R/'public/assets/gate3/registration-review/manifest.json').read_text());old=copy.deepcopy(m)
m['objects']=[o for o in m['objects'] if not o['id'].startswith('station-platform/')]+[copy.deepcopy(next(o for o in before['objects'] if o['id']=='registration/station-platform-canopy'))]
W,H=m['size'];a=np.zeros((H,W),np.uint8);b=a.copy()
for manifest,target in [(m,a),(before,b)]:
 for c in manifest['chunks']:
  x,y,w,h=[c[k] for k in ['x','y','width','height']];target[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
for x,y,w,h in [[2929,2389,11,9],[2928,2489,11,6],[2913,2524,7,6]]:a[y-25:y+h+26,x-25:x+w+26]=b[y-25:y+h+26,x-25:x+w+26]
changed=[]
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];raw=a[y:y+h,x:x+w].tobytes()
 if raw!=(R/'public'/c['mask']).read_bytes():
  ref=next(z for z in before['chunks'] if z['id']==c['id']);assert raw==(R/'public'/ref['mask']).read_bytes();c['mask']=ref['mask'];c['maskSha256']=hashlib.sha256(raw).hexdigest();changed.append(c['id'])
m['logicalSolids']=[s for s in m['logicalSolids']if not s['id'].startswith('platform-')]
m['artStatus']='Original station-platform artwork RESTORED; accepted Maru/Namsan/retail unchanged; station transfer BLOCKED; G3-B BLOCKED'
m['workingPlan']='assets-src/gate3/production-plan-v3.1-restored.json'
# Rebuild only derived review overview; no ground image or approved art writes.
ground=Image.new('RGBA',(W,H))
for c in m['chunks']:ground.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
for o in sorted(m['objects'],key=lambda z:z['sortY']):ground.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
ground.thumbnail((870,973),Image.Resampling.NEAREST);out=R/'public/assets/gate3/registration-platform-restored';out.mkdir(exist_ok=True);ground.save(out/'overview.png',optimize=True);m['overview']='assets/gate3/registration-platform-restored/overview.png';write(R/path,m)
p=historic('assets-src/gate3/production-plan-v3-working.json');q=copy.deepcopy(p);q['version']='G3-A WORKING V3.1 / original platform appearance restored';q['stationEngineeringCandidate']={'status':'VISUAL MODIFICATION REJECTED / ORIGINAL ART RESTORED / COLLISION PROPOSAL ONLY','platformReservationUnchanged':[2920,2350,100,400],'remainingTransferConflict':p['stationEngineeringCandidate']['remainingTransferConflict'],'detail':'Original unsplit canopy and scenery retained exactly; no connector, rail redraw or independent support-mask additions active. Nonvisual ownership correction requires review and real movement validation.'};write(R/m['workingPlan'],q)
assert p['plan']==q['plan'] and p['registrations']==q['registrations']
assert np.array_equal(a[2603:2813,2274:2958],b[2603:2813,2274:2958])
assert np.all(a[2626:2755,2950:2958]==0)
write(D/'restoration-diff.json',{'baseline':'5afd77a','removedObjects':[o['id']for o in old['objects']if o['id'].startswith('station-platform/')],'restoredObject':next(o for o in m['objects']if o['id']=='registration/station-platform-canopy'),'revertedSupportMaskChunks':changed,'groundChunkImagesUnchanged':all(c['image']==d['image']for c,d in zip(m['chunks'],old['chunks'])),'acceptedPlanExact':p['plan']==q['plan'],'acceptedRegistrationsExact':p['registrations']==q['registrations'],'forecourtMaskExact':True,'legacyStripStillBlocked':True,'newCollisionOpeningApplied':False})
print('Restored original appearance; accepted plan exact; mask rollback:',changed)
