"""Residual source/ownership/native QA. Technical preservation never grants art approval."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';D=R/'docs/gate3-residual'
def rd(p):return json.loads((R/p).read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=rd('public/assets/gate3/residual-world/manifest.json');old=rd('public/assets/gate3/aligned-world/manifest.json');W,H=m['size']
def world(mm):
 g=Image.new('RGBA',(W,H));f=np.zeros((H,W),np.uint8)
 for c in mm['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];im=Image.open(R/'public'/c['image']);assert im.size==(w,h);g.paste(im,(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
 return g,f
def static(mm,g):
 im=g.copy()
 for o in sorted(mm['objects'],key=lambda o:o['sortY']):im.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 return im
g,f=world(m);og,of=world(old);assert np.array_equal(f,of);assert m['logicalSolids']==old['logicalSolids'];assert m['contactCollision']==old['contactCollision'];assert not f[2626:2755,2950:2958].any()
lock=rd('assets-src/gate3/residual-v1/baseline-lock.json');bad=[p for p,h in lock['sources'].items()if sha(R/p)!=h];assert not bad,bad
library=rd('assets-src/gate3/recovery-world-v1/protected-lock.json');delta=[p for p,h in library['sha256'].items()if sha(R/p)!=h];assert delta==['src/gate3/PixelAudit.ts'],delta
refs=rd('assets-src/gate3/recovery/baseline-lock.json')['historicalRefs'].splitlines();now=subprocess.check_output(['git','show-ref','--tags'],cwd=R,text=True).splitlines();assert all(r in now for r in refs)
protected={'alignmentBaselineFiles':len(lock['sources']),'changedAlignmentFiles':bad,'libraryEntries':len(library['sha256']),'exactLibraryEntries':len(library['sha256'])-len(delta),'readOnlyCodeException':{'path':'src/gate3/PixelAudit.ts','change':'Opt-in exact POST_RENDER stop/turn pose observation; no frame/position/physics/camera override'},'allProtectedArtOriginals':'EXACT','historicalTagsUnchanged':True,'canonicalForecourtTag':subprocess.check_output(['git','rev-parse','checkpoint/g3a-station-forecourt-approved-20261023'],cwd=R,text=True).strip()};assert protected['canonicalForecourtTag']=='5d441efa1c8b0816ae1dcade4162dc06bf441b3b';wr(D/'protected-hashes.json',protected)
# Both approved plans remain byte exact at previous review baseline.
for p in ['assets-src/world-gate1/plan.json','assets-src/gate3/production-plan-v3.1-restored.json']:
 assert subprocess.check_output(['git','show','9827761:'+p],cwd=R)==(R/p).read_bytes(),p
core={n:subprocess.check_output(['git','show','9827761:src/gate3/'+n],cwd=R)==(R/'src/gate3'/n).read_bytes()for n in ['NativeTexture.ts','PixelGrid.ts','FoundationCamera.ts','Registration.ts','WorldCache.ts','ResourcePool.ts']};assert all(core.values())
objects=[];geometryKeys=['x','y','width','height','sortY','sourceAnchor','sourcePivot','alphaSoftening']
for before in old['objects']:
 after=next(o for o in m['objects']if o['id']==before['id']);changed=[k for k in geometryKeys if before.get(k)!=after.get(k)];assert not changed,(before['id'],changed);objects.append({'id':before['id'],'registrationDepthPivot':'EXACT','textureChange':after['image']!=before['image'],'before':before['image'],'after':after['image']})
facades=[]
for name,top,xGuard in [('cafe',2180,38),('bookshop',2150,0),('learning',2140,0)]:
 a=next(o for o in m['objects']if o['id']=='registration/'+name);b=next(o for o in old['objects']if o['id']==a['id']);aa=np.array(Image.open(R/'public'/a['image']).convert('RGBA'));bb=np.array(Image.open(R/'public'/b['image']).convert('RGBA'));assert np.array_equal(aa[:,:,:3],bb[:,:,:3]);sy=top-a['y'];assert np.array_equal(aa[sy:,xGuard:],bb[sy:,xGuard:]);facades.append({'id':name,'allRGB':'EXACT','structuralFacadeRGBA':'EXACT','worldGuard':[a['x']+xGuard,top,a['width']-xGuard,a['height']-sy],'exception':'Cafe prior full-width guard included nonarchitectural left background. Explicit alpha retirement there; real attached lamp/flowers/pot retained.'if name=='cafe'else'Upper alpha only, geometry fixed'})
# Actual source tree RGB/pot/trunk unchanged at exactly the old world registration.
ob=next(o for o in m['objects']if o['id']=='residual/station-potted-tree');tree=np.array(Image.open(R/'public'/ob['image']).convert('RGBA'));owned=np.array(Image.open(S/'station-tree-native-ownership.png'))>0;new=np.array(Image.open(S/'station-tree-crown-completion-mask.png'))>0;beforeStatic=static(old,og);afterStatic=static(m,g);source=np.array(beforeStatic.crop((ob['x'],ob['y'],ob['x']+ob['width'],ob['y']+ob['height'])));nativePreserved=owned&(np.indices(owned.shape)[1]+ob['x']<2958);Image.fromarray(nativePreserved.astype('uint8')*255).save(S/'station-tree-preserved-native-mask.png');assert np.array_equal(tree[:,:,:3][nativePreserved],source[:,:,:3][nativePreserved]);assert set(np.unique(tree[:,:,3]))<={0,255};assert not np.any(new&nativePreserved);assert not np.any((new&owned)&(np.indices(owned.shape)[1]+ob['x']<2958))
ys,xs=np.where(new);crownBox=[int(xs.min()+ob['x']),int(ys.min()+ob['y']),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)];assert crownBox[0]>=2958 and crownBox[0]+crownBox[2]<=2990
canon=(2274,2603,2958,2813);assert beforeStatic.crop(canon).tobytes()==afterStatic.crop(canon).tobytes();rawChange=np.any(np.array(g.crop(canon))!=np.array(og.crop(canon)),axis=2);allowed=np.zeros(rawChange.shape,bool);x1=max(2274,ob['x']);y1=max(2603,ob['y']);x2=min(2958,ob['x']+ob['width']);y2=min(2813,ob['y']+ob['height']);allowed[y1-2603:y2-2603,x1-2274:x2-2274]=owned[y1-ob['y']:y2-ob['y'],x1-ob['x']:x2-ob['x']];assert not np.any(rawChange&~allowed)
station=next(o for o in m['objects']if o['id']=='registration/station');original=np.array(Image.open(R/'public/assets/gate3/registration/station.png').convert('RGBA'));actual=np.array(Image.open(R/'public'/station['image']).convert('RGBA'));assert np.array_equal(actual[:,:,:3],original[:,:,:3]);assert station['sourcePivot']==[.5,0]
for x,y,w,h in [(88,16,65,40),(480,24,70,44)]:assert np.array_equal(actual[y:y+h,x:x+w],original[y:y+h,x:x+w]),'HVAC'
# Preserve the actual native canopy metal roof and protected post/sign geometry.
canopy=next(o for o in m['objects']if o['id']=='registration/station-platform-canopy');co=np.array(Image.open(R/'public/assets/gate3/registration/station-platform-canopy.png').convert('RGBA'));cn=np.array(Image.open(R/'public'/canopy['image']).convert('RGBA'));assert np.array_equal(co[:,:,:3],cn[:,:,:3]);rp=Image.new('L',(74,436));ImageDraw.Draw(rp).polygon([(0,26),(27,26),(73,126),(73,177),(24,177),(24,135),(0,119)],fill=255);r,gc,b=[co[:,:,k].astype(float)for k in range(3)];roof=(np.array(rp)>0)&(co[:,:,3]>0)&(b>=r*.95)&(gc>=r*.9);assert np.array_equal(co[roof],cn[roof]),'Protected native metal roof';assert np.array_equal(co[178:288,39:57],cn[178:288,39:57]),'Protected native canopy post/sign'
# Ground and scene-source ownership changes have exact native masks.
change=np.any(np.array(g)!=np.array(og),axis=2);Image.fromarray(change.astype('uint8')*255).save(S/'ground-change-mask.png')
# Canonical Jeju protected land/nearshore: only authorized outer-water exception may differ.
keep=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0;ca=np.array(g.crop((3180,3200,4204,4736)));cb=np.array(og.crop((3180,3200,4204,4736)));assert np.array_equal(ca[keep],cb[keep]);
# The repaired material consists ONLY of exact original native texels.
waterSource=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/ocean-authored.png').convert('RGBA'));waterNew=np.array(Image.open(S/'ocean-native-wrap-repaired.png').convert('RGBA'));maps=np.load(S/'ocean-native-origin-map.npz')['sourceYX'];assert np.array_equal(waterNew,waterSource[maps[:,:,0],maps[:,:,1]])
# Main palace successful registration/door/roof and central stair details unchanged.
for id in ['alignment/palace-portal','recovery-world/palace-roof']:
 a=next(o for o in m['objects']if o['id']==id);b=next(o for o in old['objects']if o['id']==id);assert a==b
front=next(o for o in m['objects']if o['id']=='alignment/palace-native-front');a=np.array(Image.open(R/'public'/front['image']));b=np.array(Image.open(R/'public/assets/gate3/aligned-world/palace-native-front.png'));mask=np.array(Image.open(S/'palace-corner-retirement-mask.png'))>0;assert np.array_equal(a[~mask],b[~mask]);assert np.array_equal(a[:,440:670],b[:,440:670]),'Central stair rails/steps'
# Real snapshots,20 matching native views plus isolated proposals. Actual foreground
# overlays are excluded from GROUND readback, not falsely counted as texture errors.
shots=rd('docs/gate3-residual/native-captures.json');pairs=[];reads=[]
for row in shots['rows']:
 if row['scene']!='residual-world':continue
 before=next(r for r in shots['rows']if r['entry']==row['entry']and r['scene']=='residual-before');assert row['audit']['camera']['scroll']==before['audit']['camera']['scroll'];assert row['audit']['camera']['zoom']==1;pairs.append({'entry':row['entry'],'sameCamera':True,'sameReviewPosition':[row['state']['x'],row['state']['y']]==[before['state']['x'],before['state']['y']]})
 sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(row['name']+'.png')).convert('RGB');v=g.crop((sx,sy,sx+im.width,sy+im.height));expect=Image.alpha_composite(Image.new('RGBA',v.size,'#33494a'),v).convert('RGB');eligible=Image.new('L',v.size,255);dr=ImageDraw.Draw(eligible)
 for o in m['objects']:dr.rectangle((o['x']-sx,o['y']-sy,o['x']+o['width']-sx-1,o['y']+o['height']-sy-1),fill=0)
 x,y=row['state']['x'],row['state']['y'];dr.rectangle((x-sx-60,y-sy-130,x-sx+60,y-sy+15),fill=0);mask=(np.array(eligible)>0)&(np.array(v)[:,:,3]==255);diff=int((mask&np.any(np.array(im)!=np.array(expect),axis=2)).sum());assert diff==0,row['name'];layers=row['audit']['layers'];assert all(l['scaleMode']==1 and l['scale']==[1,1]for l in layers);assert all(int(x)==x for x in row['audit']['camera']['scroll']);reads.append({'entry':row['entry'],'eligiblePixels':int(mask.sum()),'mismatched':diff,'integerCamera':True,'nearestAndNativeScale':True})
assert len(pairs)==20 and not shots['errors'];
# In-engine canonical frontage comparison, excluding only the actual animated Juni.
row=next(r for r in shots['rows']if r['entry']=='station-front'and r['scene']=='residual-world');bef=next(r for r in shots['rows']if r['entry']=='station-front'and r['scene']=='residual-before');sx,sy=row['audit']['camera']['scroll'];box=(2274-sx,2603-sy,2958-sx,2813-sy);a=np.array(Image.open(D/(row['name']+'.png')).convert('RGB').crop(box));b=np.array(Image.open(D/(bef['name']+'.png')).convert('RGB').crop(box));allowed=np.ones(a.shape[:2],bool)
for r in [row,bef]:
 x,y=r['state']['x'],r['state']['y'];x1=max(0,round(x)-60-2274);x2=min(684,round(x)+60-2274);y1=max(0,round(y)-130-2603);y2=min(210,round(y)+15-2603);allowed[y1:y2,x1:x2]=False
assert not np.any(allowed&np.any(a!=b,axis=2)),'Actual native canonical preservation'
# Proposed changes exist only in their named namespaces.
gate=rd('public/assets/gate3/residual-gate-proposal/manifest.json');gg,gf=world(gate);gateDiff=gf!=f;assert int(gateDiff.sum())==88*25;assert gg.tobytes()==g.tobytes();assert np.all(gf[1040:1065,2536:2624]);assert not np.any(f[1040:1065,2536:2624]);
road=rd('public/assets/gate3/residual-road-proposal/manifest.json');rg,rf=world(road);assert np.array_equal(rf,f);rc=np.any(np.array(rg)!=np.array(g),axis=2);outside=rc.copy();outside[2755:2813,2274:2958]=False;assert not outside.any()
bridge=rd('public/assets/gate3/residual-bridge-proposal/manifest.json');bg,bf=world(bridge);assert np.array_equal(bf,f)and bg.tobytes()==g.tobytes();
qa={'baseline':'9827761','clientDate':'2026-10-25 Asia/Saigon','protected':protected,'sixCoreRendererModules':core,'mainGeometryCollision':'EXACT / no masterplan or field changes','nativePairs':pairs,'nativeGroundReadback':reads,'canonicalForecourt':{'originalFile':'EXACT','staticVisibleArtwork':'PIXEL EXACT','actualPhaserComparison':'PIXEL EXACT excluding animated Juni','derivedRawGroundException':'Only old baked tree pixels retire under exact same native foreground. Actual paving/tactile/curb/shadows outside mask exact.','rawTreeOwnershipPixels':int(rawChange.sum())},'stationTree':{'oldPotTrunkCrownRGB':'EXACT at original world positions','newCrownRect':crownBox,'newCrownPixels':int(new.sum()),'alpha':'BINARY / no resampling halos','depthRoot':2696,'sourcePivot':'Original0.5 station policy unchanged'},'canopyNativeGuards':{'allRGB':'EXACT','actualMetalRoofRGBA':'EXACT','postSignGuard':[39,178,18,110],'postSignRGBA':'EXACT','originalDepthPivotAndLocation':'UNCHANGED'},'sourceGuards':facades,'protectedObjectRegistration':objects,'palaceAxisAndThreshold':'UNCHANGED2048 /685; central rails/stairs/portal/roof exact','mainStation8pxStrip':'CLOSED / not solved','gateProposal':{'status':'NOT ADOPTED','opening':[2536,1040,88,25],'hypotheticalCollisionChangedPixels':int(gateDiff.sum())},'roadProposal':{'status':'NOT ADOPTED','rect':[2274,2755,684,58],'collisionChanged':False},'bridgeProposal':{'status':'TECHNICAL OVERLAY ONLY / not artwork or live geometry','mainCollisionAndGround':'UNCHANGED','clearance':'See measured shoulder proposal and actual stop/turn reports, no locomotion-only body PASS'},'sixReviewerScreenshots':'NOT PROVIDED / requested; annotation validation NOT TESTED','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED','artAcceptance':'PENDING HUMAN / no build/test self-approval'}
wr(D/'technical-qa.json',qa);wr(D/'asset-provenance.json',{'sourceInputs':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(S.iterdir())if p.is_file()],'runtimeFiles':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for ns in ['residual-world','residual-before','residual-road-proposal','residual-gate-proposal','residual-bridge-proposal'] for p in sorted((R/'public/assets/gate3'/ns).iterdir())if p.is_file()],'authoring':'Built-in host image tool only for bounded apron/crown/bridge-water masks. No paid external API/integration. Exact prompts and original host outputs retained.','originals':'IMMUTABLE','artAcceptance':'PENDING HUMAN'})
print('Technical native audit:',len(pairs),'pairs;',sum(r['eligiblePixels']for r in reads),'ground pixels EXACT; canonical actual Phaser frontage preserved; art review pending')
