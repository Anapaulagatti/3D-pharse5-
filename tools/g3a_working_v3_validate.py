"""Accepted plan diff, exact source protection, route and support clearance validation."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib,subprocess
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-controlled-finalization'
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
working=read('assets-src/gate3/production-plan-v3-working.json');plan=working['plan'];base=read('assets-src/gate25/world-plan-v1.json');m=read('public/assets/gate3/registration-working-v3/manifest.json');old=read('public/assets/gate3/registration-review/manifest.json');W,H=m['size']
def arrays(manifest):
 a=np.zeros((H,W),np.uint8);g=Image.new('RGBA',(W,H))
 for c in manifest['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];raw=(R/'public'/c['mask']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['maskSha256'];a[y:y+h,x:x+w]=np.frombuffer(raw,np.uint8).reshape(h,w);im=Image.open(R/'public'/c['image']).convert('RGBA');g.paste(im,(x,y));assert hashlib.sha256((R/'public'/c['image']).read_bytes()).hexdigest()==c['sha256']
 return a,g
walk,ground=arrays(m);before,beforeGround=arrays(old)
def point(manifest,field,x,y):
 if any(x>=s['rect'][0]and y>=s['rect'][1]and x<s['rect'][0]+s['rect'][2]and y<s['rect'][1]+s['rect'][3]for s in manifest.get('logicalSolids',[])):return False
 return bool(0<=x<W and 0<=y<H and field[math.floor(y+.5),math.floor(x+.5)]>127)
def check(name,points):
 bad=[];length=0;oldBad=0;newBad=0;count=0
 for a,b in zip(points,points[1:]):
  dist=math.dist(a,b);length+=dist
  for i in range(math.ceil(dist)+1):
   t=i/max(1,math.ceil(dist));x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t;ok=point(m,walk,x,y);was=point(old,before,x,y);count+=1
   if not was:oldBad+=1
   if not ok:
    bad.append([round(x,3),round(y,3)])
    if was:newBad+=1
 return {'id':name,'points':points,'lengthPx':round(length,3),'walkSeconds':round(length/60,3),'runSeconds':round(length/100,3),'status':'PASS'if not bad else'FAIL_CENTRELINE','failedSamples':len(bad),'examples':bad[:8],'previousComparisonFailedSamples':oldBad,'newlyBlockedVersusComparison':newBad,'sampleCount':count}
selected=[('maru-front',[[700,3140],[700,3380],[326,3380],[326,3343]]),('namsan-west-loop',[[950,3280],[700,3140],[700,2920],[750,2800]]),('station-threshold',[[2598.5,2760],[2598.5,2610]]),('platform-full-length-clearance',[[2980,2749],[2980,2350]]),('platform-protected-public-path',[[2980,2690],[2970,2530]]),('canopy-opening-approach',[[2980,2550],[2960,2550],[2960,2530]]),('amusement-main-access',[[2048,3260],[2440,3260],[2440,3200]]),('main-avenue-south',[[2048,3260],[2048,3790]]),('island-arrival-main',[[2048,3480],[2900,3480],[3160,3480]])]
routes=[check(n,p)for n,p in selected];allpaths=[check(p['id'],p['points'])for p in plan['paths']]
field=walk>127
for solid in m['logicalSolids']:
 x,y,w,h=solid['rect'];field[max(0,math.ceil(y)):min(H,math.ceil(y+h)),max(0,math.ceil(x)):min(W,math.ceil(x+w))]=False
for route,record in zip(plan['paths'],allpaths):
 if not record['failedSamples']:continue
 points=route['points'];r=route['width']//2+2;x0=max(0,min(p[0]for p in points)-r);y0=max(0,min(p[1]for p in points)-r);x1=min(W,max(p[0]for p in points)+r+1);y1=min(H,max(p[1]for p in points)+r+1)
 ribbon=Image.new('L',(x1-x0,y1-y0));ImageDraw.Draw(ribbon).line([(x-x0,y-y0)for x,y in points],fill=255,width=route['width'],joint='curve');components,_=label(field[y0:y1,x0:x1]&(np.array(ribbon)>0))
 ids=[int(components[y-y0,x-x0])for x,y in points];record['withinReservedCorridorConnectivity']='PASS_FOOT_CENTRE_FIELD'if ids[0]>0 and all(i==ids[0]for i in ids)else'FAIL_OR_BLOCKED_WAYPOINT';record['corridorCaveat']='4-connected field inside unchanged reserved width, all exact planned waypoints; not a guarantee of full visual clearance or a new route amendment.'
# No protected native heritage visual or physical overwrite by accepted retail projections.
def intersection(a,b):
 x,y=max(a[0],b[0]),max(a[1],b[1]);r,z=min(a[0]+a[2],b[0]+b[2]),min(a[1]+a[3],b[1]+b[3]);return[x,y,r-x,z-y]if r>x and z>y else None
heritage=[b for b in base['buildings']if b['kind']=='heritage'];hits=[]
for e in plan['registrationEasements']:
 for b in heritage:
  for kind in ['contact','visualEnvelope']:
   hit=intersection(e[kind],b['rect'])
   if hit:hits.append({'retail':e['id'],'heritage':b['id'],'type':kind,'overlap':hit})
 assert not intersection(e['visualEnvelope'],[640,650,1536,1024])
assert not hits
retailPathHits=[]
for e in plan['registrationEasements']:
 x,y,w,h=e['visualEnvelope']
 for path in plan['paths']:
  canvas=Image.new('L',(w,h));ImageDraw.Draw(canvas).line([(px-x,py-y)for px,py in path['points']],fill=255,width=path['width'],joint='curve')
  n=int((np.array(canvas)>0).sum())
  if n:retailPathHits.append({'retail':e['id'],'path':path['id'],'overlapPixels':n})
assert not retailPathHits,retailPathHits
sourceWalk=np.array(Image.open(R/'public/assets/gate2/district-planter-repair/walk.png').convert('L'));assert np.all(sourceWalk[713:842,3176:3184]==0);assert np.array_equal(walk[2626:2755,2950:2958],before[2626:2755,2950:2958])
# Preserve all historical planned buildings except the expressly accepted cafe width and new Maru.
assert plan['land']==base['land'];assert plan['station']==base['station'];assert plan['railKeepouts']==base['railKeepouts'];assert plan['overpasses']==base['overpasses']
for b in base['buildings']:
 if b['id']in ['tower','carousel','wheel','ferry']:
  x,y,w,h=b['rect'];assert np.array_equal(np.array(ground.crop((x,y,x+w,y+h))),np.array(beforeGround.crop((x,y,x+w,y+h)))),b['id']
 n=next(x for x in plan['buildings']if x['id']==b['id'])
 if b['id']!='cafe':assert n==b,b['id']
for p in base['paths']:
 n=next(x for x in plan['paths']if x['id']==p['id'])
 if p['id']!='tower-approach':assert n==p,p['id']
 else:assert n['points'][:4]==p['points'][:4]
for x,y,w,h in [[640,650,1536,1024],[3180,3200,1024,1536]]:assert np.array_equal(np.array(ground.crop((x,y,x+w,y+h))),np.array(beforeGround.crop((x,y,x+w,y+h))))
assert np.array_equal(walk[2603:2813,2274:2958],before[2603:2813,2274:2958]);assert np.array_equal(np.array(ground.crop((2274,2603,2958,2813))),np.array(beforeGround.crop((2274,2603,2958,2813))))
for id in ['registration/station','registration/station-planter-left','registration/station-planter-right']:
 assert next(o for o in old['objects']if o['id']==id)==next(o for o in m['objects']if o['id']==id)
assert next(s for s in m['logicalSolids']if s['id']=='station')['rect']==[2322.5,2380,555,210]
assert not any('bakery'in o['id']for o in m['objects']);assert plan['contentAllocations'][0]['requiredWorldContent'];assert plan['contentAllocations'][0]['allocation'].startswith('DEFERRED')
# Frozen approved source hashes and historical files, including the accepted forecourt.
locks=read('docs/gate3a/protected-assets.json')['sha256']|read('assets-src/gate3/approved-station-forecourt.json')['sha256']
for n,h in locks.items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
protectedDirs=['assets-src/gate25','assets-src/world-gate1','assets-src/gate3/forecourt-restoration','public/assets/gate3/world','public/assets/gate3/registration','public/assets/gate3/registration-refined','public/assets/gate3/registration-forecourt','public/assets/gate3/registration-review','public/assets/juni']
assert not subprocess.check_output(['git','diff','b72dc6f','--']+protectedDirs,cwd=R).strip()
# Native source remains exact outside the explicitly local railing ownership detail.
src=np.array(Image.open(R/'public/assets/gate3/registration/station-platform-canopy.png').convert('RGBA'));composite=Image.new('RGBA',(74,436))
for o in sorted(m['objects'],key=lambda o:o['sortY']):
 if o['id'].startswith('station-platform/')and o['id']!='station-platform/opening-connector':composite.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x']-2884,o['y']-2213))
a=np.array(composite);different=np.any(a!=src,2);allowed=np.zeros((436,74),bool);allowed[282:316,29:74]=True;assert not np.any(different&~allowed)
# Fixed platform: verify width49 sprite has no physical support footprint at each route point.
supports=[s for s in m['logicalSolids']if s['id'].startswith('platform-')];supportClear=[]
for x,y in [(2980,y)for y in range(2350,2691)]+[(2970,2530)]:
 for s in supports:
  r=s['rect'];assert not intersection([x-24.5,y-1,49,2],r),(x,y,s)
for s in supports:supportClear.append({'id':s['id'],'physicalBase':s['rect'],'runtimeGuardRadius':25,'stationBodyColliderChanged':False})
write(D/'route-validation.json',{'selectedRoutes':routes,'fullApprovedPathCentrelineAudit':allpaths,'retailPhysicalOrVisualHeritageHits':hits,'retailVisualEnvelopePublicRouteHits':retailPathHits,'inheritedStationTransferGuard':{'sourceMaskRect':[3176,713,8,129],'worldMaskRect':[2950,2626,8,129],'allClosed':True,'unchanged':True,'localProduction':'BLOCKED / collision-ownership decision required'},'protectedRoutesRecordExactExceptAcceptedWesternLoop':True,'platformReservationsExact':True,'landAllocationExact':True,'bakeryActiveAllocation':None,'publicExclusions':plan['publicExclusions'],'method':'<=1px continuous logical + actual chunk-mask checks, exact endpoints. Centreline failures and inherited limitations disclosed separately from corridor routing.','supportFootprints':supportClear,'nativeDetailChangedPixels':int(different.sum()),'nativeDetailAllowedSourceBox':[29,282,74,316]})
write(D/'protected-assets.json',{'status':'PASS','sha256':locks,'historicalDirectoriesUnchanged':protectedDirs,'canonicalForecourtGroundAndMaskExact':True,'protectedStationObjectsAndColliderExact':True,'historicalHeritageAndJejuSceneGroundExact':True,'bakeryNativeAssetUnchanged':True,'originalPlatformReservationExact':True})
print('Selected:',[(r['id'],r['status'],r['examples'][:1])for r in routes]);print('Full path failures:',[(r['id'],r['failedSamples'],r['newlyBlockedVersusComparison'])for r in allpaths if r['failedSamples']])
