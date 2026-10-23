from pathlib import Path
import json,hashlib,math,subprocess
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,label
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery-world';S=R/'assets-src/gate3/recovery-world-v1'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
m=read('public/assets/gate3/recovery-world/manifest.json');before=read('public/assets/gate3/recovery-pilots/manifest.json');W,H=m['size'];ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
lock=read('assets-src/gate3/recovery-world-v1/protected-lock.json');bad=[p for p,h in lock['sha256'].items()if sha(R/p)!=h];hashreport={'registry':'assets-src/gate3/recovery-world-v1/protected-lock.json','checked':len(lock['sha256']),'changed':bad,'status':'FAIL'if bad else'PASS'};write(D/'protected-hashes.json',hashreport)
frozen_refs=read('assets-src/gate3/recovery/baseline-lock.json')['historicalRefs'].splitlines();current_refs=subprocess.check_output(['git','show-ref','--tags'],cwd=R,text=True).splitlines();hashreport['historicalTagsUnchanged']=all(line in current_refs for line in frozen_refs);hashreport['canonicalForecourtTag']=subprocess.check_output(['git','rev-parse','checkpoint/g3a-station-forecourt-approved-20261023'],cwd=R,text=True).strip();assert hashreport['canonicalForecourtTag']=='5d441efa1c8b0816ae1dcade4162dc06bf441b3b';write(D/'protected-hashes.json',hashreport)
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
nav={'method':'Actual runtime .bin field, every planned centerline sampled at <=1px, 4-connected components and conservative49px-diameter clearance. Geometry-only travel times, actual videos reported separately. No route amendments.','routes':routes,'targets':targets,'station8pxStripClosed':bool(not np.any(walk[2626:2755,2950:2958])),'bakery':'Required / unplaced / W0 rejected / Q1 unallocated','publicNetworkAcceptance':'FAIL while inherited route/49px-clearance findings remain','physicalDevices':'NOT TESTED'};write(D/'navigation-report.json',nav)

# Exact projected alpha intersection, rather than bbox-only artwork conflict diagnosis.
def opaque_overlap(o,rect):
 x,y,w,h=rect;lx=max(x,o['x']);ly=max(y,o['y']);rx=min(x+w,o['x']+o['width']);ry=min(y+h,o['y']+o['height'])
 if lx>=rx or ly>=ry:return 0
 a=np.array(Image.open(R/'public'/o['image']).convert('RGBA').getchannel('A').crop((lx-o['x'],ly-o['y'],rx-o['x'],ry-o['y'])))
 return int((a>32).sum())
projection=[]
for key,rect in [('tower',(470,2626,1482,128)),('carousel',(2274,2196,766,667)),('wheel',(2274,2196,766,667))]:
 o=next(o for o in m['objects']if o['id']=='recovery-world/'+key);count=opaque_overlap(o,rect);projection.append({'id':key,'nativeEnvelope':[o[k]for k in ['x','y','width','height']],'protectedRoot':o['sortY'],'comparisonRect':list(rect),'opaqueOverlapPixels':count,'stationFacadePixels':opaque_overlap(o,(2313,2196,645,453))if key!='tower'else None,'canonicalFloorPixels':opaque_overlap(o,(2274,2603,684,210))if key!='tower'else None,'lowerRoadContinuationPixels':opaque_overlap(o,(2274,2813,684,50))if key!='tower'else None,'status':'FAIL_PROJECTION_OR_HUMAN_OCCLUSION_DECISION_OPEN'if count else'PASS_SELECTED_PROJECTION','policy':'Complete native silhouette, no tip crop/downscale, protected root/reservation unchanged. Visual projection is not a ground/support collision; residual road occlusion remains explicitly reviewable.'})
write(D/'projection-report.json',projection)

# Protected object texture/registration/pivot/solids invariant; authorized retail alpha policy is explicit.
protected_objects=[]
for ob in before['objects']:
 if ob['id'].startswith('production/')or ob['id'].startswith('recovery/'):continue
 new=next(o for o in m['objects']if o['id']==ob['id']);keys=['image','x','y','width','height','sortY','sourceAnchor','sourcePivot'];changed=[k for k in keys if ob.get(k)!=new.get(k)];protected_objects.append({'id':ob['id'],'registrationAndTexture':'FAIL'if changed else'PASS','changed':changed,'foregroundAlpha':[ob['alphaSoftening'],new['alphaSoftening']]})
assert before.get('logicalSolids')==m.get('logicalSolids');assert all(isinstance(o['x'],int)and isinstance(o['y'],int)for o in m['objects'])
core={name:subprocess.check_output(['git','show',lock['baselineCommit']+':src/gate3/'+name],cwd=R)==(R/'src/gate3'/name).read_bytes()for name in ['NativeTexture.ts','PixelGrid.ts','FoundationCamera.ts','Registration.ts','WorldCache.ts','ResourcePool.ts']}
readback=[]
capture=D/'native-captures.json'
if capture.exists():
 shots=json.loads(capture.read_text())
 for row in shots['rows']:
  if '-after-native'not in row['name']:continue
  sx,sy=row['audit']['camera']['scroll'];actual=Image.open(D/(row['name']+'.png')).convert('RGB');view=ground.crop((sx,sy,sx+1280,sy+900));expected=Image.alpha_composite(Image.new('RGBA',view.size,'#33494a'),view).convert('RGB');eligible=Image.new('L',actual.size,255);d=ImageDraw.Draw(eligible)
  for ob in m['objects']:d.rectangle((ob['x']-sx,ob['y']-sy,ob['x']+ob['width']-sx-1,ob['y']+ob['height']-sy-1),fill=0)
  px,py=row['state']['x'],row['state']['y'];d.rectangle((px-sx-60,py-sy-130,px-sx+60,py-sy+10),fill=0)
  mask=(np.array(eligible)>0)&(np.array(view)[:,:,3]==255);diff=np.any(np.array(actual)!=np.array(expected),axis=2);count=int((mask&diff).sum());readback.append({'frame':row['name'],'opaqueGroundPixels':int(mask.sum()),'mismatched':count,'status':'FAIL'if count else'PASS','integerCamera':all(v==int(v)for v in row['audit']['camera']['scroll']),'samplingScaleNative':all(l.get('scale')==[1,1]and l.get('scaleMode')==1 for l in row['audit']['layers'])})
qa={'protectedHashes':hashreport,'protectedObjectRegistration':protected_objects,'protectedLogicalSolids':'UNCHANGED','integerNativePlacement':'PASS','rendererCoreUnchanged':core,'pixelReadback':readback,'station8pxStrip':'UNCHANGED/CLOSED; no transfer acceptance','retailVisibility':'Native facade preserved; authorized foreground alpha0.35 when behind. See actual Phaser occlusion evidence.','artAcceptance':'PENDING HUMAN / not established by technical checks','fullWorldCompleteness':'PARTIAL while required Bakery and P1s remain','hardwareWebGLPerformance':'NOT TESTED on physical GPU','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED'};write(D/'technical-qa.json',qa)
print('Protected hashes:',hashreport['status'],hashreport['checked'],'; planned failures:',sum(bool(r['blockedCenterSamples'])for r in routes),'; projection:',projection)
