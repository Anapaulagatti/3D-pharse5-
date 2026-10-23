from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import label,distance_transform_edt
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-world';m=json.loads((R/'public/assets/gate3/production/manifest.json').read_text());W,H=m['size'];walk=np.zeros((H,W),np.uint8);ground=Image.new('RGBA',(W,H))
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];raw=(R/'public'/c['mask']).read_bytes();assert len(raw)==w*h;assert hashlib.sha256(raw).hexdigest()==c['maskSha256'];im=Image.open(R/'public'/c['image']).convert('RGBA');assert im.size==(w,h);ground.paste(im,(x,y));walk[y:y+h,x:x+w]=np.frombuffer(raw,np.uint8).reshape(h,w)
locks=json.loads((R/'docs/g3a-controlled-finalization/protected-assets.json').read_text())['sha256'];assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in locks.items())
frozen=json.loads((R/'assets-src/gate3/full-world/foundation-lock.json').read_text());assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in frozen['sha256'].items())
for line in frozen['historicalTagRefs'].splitlines():
 h,ref=line.split();assert subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()==h
exact=[]
for path,origin in [('public/assets/gate2/a/ground.png',(640,650)),('public/assets/gate2/c/ground.png',(3180,3200)),('assets-src/gate3/forecourt-restoration/restored-ground.png',(2274,2603))]:
 im=Image.open(R/path).convert('RGBA');x,y=origin;assert im.tobytes()==ground.crop((x,y,x+im.width,y+im.height)).tobytes();exact.append(path)
assert all(all(isinstance(o[k],int)for k in ['x','y','width','height'])for o in m['objects']);assert not any(o['id'].startswith('station-platform/')for o in m['objects'])
regions,n=label(walk>127);sx,sy=map(round,m['spawn']);component=int(regions[sy,sx]);assert component>0
rows=[]
for t in m['targets']:
 x,y=round(t['x']),round(t['y']);radius=60;local=regions[max(0,y-radius):min(H,y+radius+1),max(0,x-radius):min(W,x+radius+1)];yy,xx=np.where(local==component);dist=(xx+max(0,x-radius)-x)**2+(yy+max(0,y-radius)-y)**2
 nearest=None
 if len(dist):i=int(dist.argmin());nearest=[int(xx[i]+max(0,x-radius)),int(yy[i]+max(0,y-radius))]
 rows.append({'id':t['id'],'label':t['label'],'point':[x,y],'exactPointWalkable':bool(walk[y,x]>127),'exactPointInSpawnComponent':int(regions[y,x])==component,'nearbyReachablePoint':nearest,'nearbyDistancePx':float(np.sqrt(dist.min()))if len(dist)else None,'status':'CONNECTED_FOOT_POINT'if int(regions[y,x])==component else'FAIL_EXACT_TARGET / NEARBY_ONLY'if nearest else'FAIL_DISCONNECTED','fullJuniClearance':'NOT CERTIFIED / runtime uses foot-point sampling'})
plan=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan'];routes=[]
for p in plan['paths']:
 bad=[];total=0;length=0
 for a,b in zip(p['points'],p['points'][1:]):
  d=np.linalg.norm(np.subtract(b,a));length+=d
  for t in np.linspace(0,1,max(2,int(np.ceil(d))+1)):
   x,y=np.round(np.array(a)+(np.array(b)-a)*t).astype(int);total+=1
   if walk[y,x]<128:bad.append([int(x),int(y)])
 routes.append({'id':p['id'],'lengthPx':round(length,1),'walkSeconds':round(length/60,1),'runSeconds':round(length/100,1),'blockedSamples':len(bad),'sampleCount':total,'firstBlocked':bad[:5],'status':'PASS_CENTRELINE_ONLY'if not bad else'FAIL_CENTRELINE','note':'Geometric time at unchanged speed, excludes stops; connectivity does not certify full-body clearance.'})
(D/'navigation-report.json').write_text(json.dumps({'components':n,'spawnComponent':component,'targets':rows,'plannedRoutes':routes,'station8pxStripUnchanged':bool(np.all(walk[2626:2755,2950:2958]==0)),'ferryOperational':False,'bakeryPlaced':False,'fullNetworkAcceptance':'FAIL / see individual inherited target and centreline issues'},ensure_ascii=False,indent=2)+'\n')
(D/'protected-assets.json').write_text(json.dumps({'status':'PASS','verified':len(locks),'approvedGroundRegionsPixelExact':exact,'frozenPlanAndManifestExact':True,'allFrozenHistoricalRefsExact':True,'rejectedConnectorInactive':True,'nativeScale':1,'resampling':'NONE','sha256':locks},indent=2)+'\n')
print('PASS',len(locks),'protected assets;',sum(t['status']=='CONNECTED_FOOT_POINT'for t in rows),'/',len(rows),'exact foot targets connected;',sum(r['blockedSamples']>0 for r in routes),'planned centreline findings')
