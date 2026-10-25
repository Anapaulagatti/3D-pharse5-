from pathlib import Path
import json,hashlib,math,subprocess
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,label
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-jeju-bridges';S=R/'assets-src/gate3/alignment-v1'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
m=read('public/assets/gate3/jeju-bridges-world/manifest.json');before=read('public/assets/gate3/reconciled-world/manifest.json');W,H=m['size'];ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
plan=read('assets-src/gate3/production-plan-v3.1-restored.json')['plan'];dist=distance_transform_edt(walk>0);components,n=label(walk>0);sx,sy=m['spawn'];component=int(components[int(sy),int(sx)]);routes=[]
for q in plan['paths']:
 pts=[];length=0
 for a,b in zip(q['points'],q['points'][1:]):
  length+=math.dist(a,b)
  for t in np.linspace(0,1,int(math.dist(a,b))+1):
   x,y=np.rint(np.array(a)*(1-t)+np.array(b)*t).astype(int);pts.append((int(x),int(y)))
 bad=[v for v in pts if not walk[v[1],v[0]]];body=[v for v in pts if dist[v[1],v[0]]<24.5]
 routes.append({'id':q['id'],'lengthPx':round(length,1),'walkSecondsAt60px':round(length/60,1),'runSecondsAt100px':round(length/100,1),'sampleCount':len(pts),'blockedCenterSamples':len(bad),'firstBlocked':bad[:8],'body49pxClearanceFailures':len(body),'minimumCenterClearance':round(min(float(dist[y,x])for x,y in pts),2),'status':'FAIL'if bad else'PASS_CENTER_ONLY','fullBody':'FAIL_OR_NOT_CERTIFIED'if body else'PASS_CONSERVATIVE_RADIUS24_5'})
targets=[]
for key,(x,y)in m['reviewEntries'].items():
 x,y=int(x),int(y);targets.append({'id':key,'point':[x,y],'footConnected':bool(components[y,x]>0 and components[y,x]==component),'clearanceToSolidPx':round(float(dist[y,x]),2)})
nav={'method':'Actual runtime .bin field, every planned centerline sampled at <=1px, 4-connected components and conservative49px-diameter clearance. Diagnostic radius24.5 is conservative and is NOT the native directional ground-contact guard used on the bridge. Geometry-only travel times; actual movement/body readback reported separately. No route amendments.','routes':routes,'targets':targets,'station8pxStripClosed':bool(not np.any(walk[2626:2755,2950:2958])),'bakery':'Required / unplaced / W0 rejected / Q1 unallocated','publicNetworkAcceptance':'FAIL while inherited route/49px-clearance findings remain','physicalDevices':'NOT TESTED'};write(D/'navigation-report.json',nav)
