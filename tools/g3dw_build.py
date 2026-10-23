"""Consolidated recovery: native ownership/compositing, never source-art resampling.

New namespace only. Historical plans, sources and runtime checkpoints are read-only.
Generated panels are source plates; binary seam masks select their native pixels.
"""
from pathlib import Path
import copy, hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/gate3/recovery-world-v1';O=R/'public/assets/gate3/recovery-world';D=R/'docs/gate3-recovery-world'
O.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load_world(m):
 w,h=m['size'];im=Image.new('RGBA',(w,h));walk=np.zeros((h,w),np.uint8)
 for c in m['chunks']:
  x,y,cw,ch=[c[k]for k in ['x','y','width','height']]
  im.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+ch,x:x+cw]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(ch,cw)
 return im,walk
def mincut(cost):
 """One native-pixel-wide monotonic minimum-cost seam; no alpha blending."""
 h,w=cost.shape;acc=cost.astype(np.float32).copy();back=np.zeros((h,w),np.int8)
 for y in range(1,h):
  prev=acc[y-1];choices=np.stack([np.r_[np.inf,prev[:-1]],prev,np.r_[prev[1:],np.inf]])
  choice=np.argmin(choices,axis=0);back[y]=choice-1;acc[y]+=choices[choice,np.arange(w)]
 path=np.empty(h,np.int32);path[-1]=np.argmin(acc[-1])
 for y in range(h-2,-1,-1):path[y]=path[y+1]+back[y+1,path[y+1]]
 return path
m=read('public/assets/gate3/recovery-pilots/manifest.json');ground,walk=load_world(m);old=ground.copy();oldwalk=walk.copy();W,H=m['size']
p=read('assets-src/gate3/production-plan-v3.1-restored.json')['plan'];registry=read('assets-src/gate3/recovery-world-v1/panel-registry.json')
covered=np.zeros((H,W),bool);records=[]
for q in registry['protectedGround']:
 px,py,pw,ph=q['rect'];covered[py:py+ph,px:px+pw]=True
# Native rowwise quilting; 1px binary ownership edges avoid all blend/resampling haze.
order=['northwest','palacecourt','academywest','northeast','thresholdwest','thresholdeast','urbanwest','urbanse','harborwest','harboreast','rail','jejunorth','jejusouth']
for name in order:
 x,y,w,h=registry['regions'][name];path=S/(name+'-authored.png');plate=Image.open(path).convert('RGBA');assert plate.size==(w,h),(name,plate.size)
 prev=np.array(ground.crop((x,y,x+w,y+h)));a=np.array(plate);cv=covered[y:y+h,x:x+w];mask=np.ones((h,w),bool)
 cost=np.abs(prev[:,:,:3].astype(np.float32)-a[:,:,:3]).mean(axis=2)+1
 # Only use rectangular overlap bands present for >=90% of their orthogonal axis.
 left=0
 while left<w-1 and cv[:,left].mean()>.9:left+=1
 top=0
 while top<h-1 and cv[top,:].mean()>.9:top+=1
 if 2<=left<w-4:
  seam=mincut(cost[:,:left]);mask &= np.arange(w)[None,:]>=seam[:,None]
 if 2<=top<h-4:
  seam=mincut(cost[:top,:].T);mask &= np.arange(h)[:,None]>=seam[None,:]
 # A90%-covered overlap band can include a small new tail. Those never inherit
 # the rejected baseline: every genuinely uncovered pixel must use the new plate.
 mask |= ~cv
 # Locked original scene grounds/floor always win; no masked replacement of their pixels.
 for protected in registry['protectedGround']:
  bx,by,bw,bh=protected['rect'];lx=max(0,bx-x);ly=max(0,by-y);rx=min(w,bx+bw-x);ry=min(h,by+bh-y)
  if lx<rx and ly<ry:mask[ly:ry,lx:rx]=False
 maskim=Image.fromarray(mask.astype('uint8')*255);maskim.save(S/(name+'-ownership.png'),optimize=True);ground.paste(plate,(x,y),maskim);covered[y:y+h,x:x+w]|=mask
 records.append({'region':name,'source':str(path.relative_to(R)),'sha256':sha(path),'origin':[x,y],'ownedPixels':int(mask.sum()),'mask':str((S/(name+'-ownership.png')).relative_to(R)),'nativeScale':1,'resampling':'NONE','seam':'binary native min-cost pixel ownership; no feather blending'})

# Preserve accepted fine-material pilots where full native source ownership is already established.
for name,origin,box in [('south',(416,1960),(416,1960,1952,2760)),('namsan',(416,2470),(416,2760,1952,3340))]:
 src=R/'assets-src/gate3/recovery'/(name+'-ground-derived.png');im=Image.open(src).convert('RGBA');x,y=origin;bx,by,rx,ry=box
 ground.paste(im.crop((bx-x,by-y,rx-x,ry-y)),(bx,by))
 records.append({'retainedAcceptedPilotMaterial':name,'source':str(src.relative_to(R)),'origin':[x,y],'ownershipRect':list(box),'nativeScale':1})

objects=copy.deepcopy(m['objects']);removed=[]
# Finish the remote north-east headland using one native donor from the newly
# authored eastern garden (no architecture). This is one registered landscape
# component, not the rejected periodically stamped material atlas.
head=Image.open(S/'northeast-authored.png').convert('RGBA').crop((1136,0,1536,512));ground.paste(head,(2800,80));covered[80:592,2800:3200]=True
records.append({'nativeLandscapeContinuation':'north-east headland','source':'assets-src/gate3/recovery-world-v1/northeast-authored.png','sourceRect':[1136,0,400,512],'worldRect':[2800,80,400,512],'scale':1,'resampling':'NONE','reuse':'One native existing authored landscape component; not a periodic tile fill. No architecture or land allocation.'})
# Native harbor planks continue the already reserved jetty, at their original scale.
jetty=Image.open(S/'harboreast-authored.png').convert('RGBA').crop((832,968,960,1024))
for yy in [4000,4056,4112]:
 hh=min(56,4160-yy);ground.paste(jetty.crop((0,0,128,hh)),(2496,yy));covered[yy:yy+hh,2496:2624]=True
records.append({'nativeMaterialContinuation':'reserved boarding jetty','source':'assets-src/gate3/recovery-world-v1/harboreast-authored.png','sourceRect':[832,968,128,56],'worldRect':[2496,4000,128,160],'scale':1,'resampling':'NONE','geometry':'Existing128px jetty reservation unchanged; source wooden-plank component reused at native pitch. No ferry gameplay.'})
road_source=S/'station-road-join-authored.png'
road=Image.open(road_source).convert('RGBA');road_mask=Image.new('L',road.size);ImageDraw.Draw(road_mask).rectangle((610,509,1293,558),fill=255);road_mask.save(S/'station-road-ownership.png',optimize=True)
ground.paste(road,(1664,2304),road_mask)
records.append({'localizedJoin':'station lower road / curb / tactile landing','source':str(road_source.relative_to(R)),'sha256':sha(road_source),'sourceRect':[610,509,684,50],'worldRect':[2274,2813,684,50],'mask':str((S/'station-road-ownership.png').relative_to(R)),'resampling':'NONE','protectedFloor':'UNCHANGED; ownership begins exactly below canonical floor','notPlatformConnector':True})
# Unify deep open water so independently authored regional plates cannot leave
# rectangular color panels. This is the APPROVED Jeju128px fine-wave component,
# not the rejected232–248px landscape atlas. Preserve every authored shoreline
# within160px of planned land and ALL original Jeju pixels without exception.
land_geometry=Image.new('L',(W,H));ld=ImageDraw.Draw(land_geometry)
for lx,ly,lw,lh in p['land']:ld.rectangle((lx,ly,lx+lw-1,ly+lh-1),fill=255)
deep=distance_transform_edt(np.array(land_geometry)==0)>160
deep[3200:4736,3180:4204]=False
water_source=R/'public/assets/gate2/c/ground.png';water=Image.open(water_source).convert('RGBA').crop((0,0,128,128));wa=np.array(water)
sea=Image.fromarray(wa[(np.arange(H)[:,None]-3200)%128,(np.arange(W)[None,:]-3180)%128]);sea_mask=Image.fromarray(deep.astype('uint8')*255);sea_mask.save(S/'deep-water-ownership.png',optimize=True);ground.paste(sea,(0,0),sea_mask)
records.append({'sharedNativeSurface':'deep open water','source':'public/assets/gate2/c/ground.png','sourceSha256':sha(water_source),'sourceRect':[0,0,128,128],'phaseAnchor':[3180,3200],'ownershipMask':'assets-src/gate3/recovery-world-v1/deep-water-ownership.png','ownedPixels':int(deep.sum()),'resampling':'NONE','protectedJeju':'ENTIRE original1024x1536 region excluded','shoreline':'Authored coast within160px of planned land retained','policy':'Approved fine-wave water reuse only; no rejected material-atlas tiles, color filtering, new land or shoreline movement.'})
for ob in list(objects):
 if ob['id'].startswith('production/tree-') or ob['id'] in ['recovery/tower','production/carousel','production/wheel','production/market','production/ferry']:
  objects.remove(ob);removed.append(ob['id'])
for ob in objects:
 if ob['id'] in ['registration/cafe','registration/bookshop','registration/learning','registration/convenience']:
  ob['alphaSoftening']=.35

# Explicit candidate registry is separate from all protected registrations.
placements=read('assets-src/gate3/recovery-world-v1/native-assets.json')
for ob in placements['objects']:
 objects.append(ob)

# Remove obsolete prototype tree-foot solids, leaving protected original collision untouched.
_,basewalk=load_world(read('public/assets/gate3/registration-working-v3/manifest.json'))
for ob in m['objects']:
 if ob['id'].startswith('production/tree-'):
  cx=ob['x']+ob['width']//2;cy=ob['sortY'];walk[cy-8:cy+10,cx-13:cx+14]=basewalk[cy-8:cy+10,cx-13:cx+14]
for rect in placements.get('newFeet',[]):
 x,y,w,h=rect;walk[y:y+h,x:x+w]=0

# Integration-only ownership repair: the old market placeholder extended80px beyond
# its unchanged contact/root3660. Open only the104px entrance approach on existing land.
market_approach=[858,3660,104,80]
walk[3660:3740,858:962]=255
# Two loose market-counter feet project by<=20px into existing non-route plaza.
# Register those PROP contacts separately; building reservation remains780px.
market_ob=next(o for o in objects if o['id']=='recovery-world/market');ma=np.array(Image.open(R/'public'/market_ob['image']).getchannel('A'));my,mx=np.indices(ma.shape)
counter=(ma>200)&(my>=ma.shape[0]-18)&((mx+market_ob['x']<520)|(mx+market_ob['x']>=1300))
route_mask=Image.new('L',(W,H));route_draw=ImageDraw.Draw(route_mask)
for path in p['paths']:route_draw.line([tuple(v)for v in path['points']],fill=255,width=path['width'],joint='curve')
cy,cx=np.where(counter);wy=cy+market_ob['y'];wx=cx+market_ob['x'];assert not np.any(np.array(route_mask)[wy,wx])
walk[wy,wx]=0
Image.fromarray(counter.astype('uint8')*255).save(S/'market-counter-contact-mask.png',optimize=True)

# Native station floor and original historical/island source images must remain byte-exact.
protected=[]
for q in registry['protectedGround']:
 x,y,w,h=q['rect'];im=Image.open(R/q['source']).convert('RGBA');assert im.size==(w,h)
 assert ground.crop((x,y,x+w,y+h)).tobytes()==im.tobytes(),q['source']
 protected.append({'source':q['source'],'sha256':sha(R/q['source']),'nativeGroundExact':True,'rect':q['rect']})

chunks=[]
for c0 in m['chunks']:
 c=copy.deepcopy(c0);x,y,w,h=[c[k]for k in ['x','y','width','height']];im=ground.crop((x,y,x+w,y+h));wm=walk[y:y+h,x:x+w]
 out=O/(c['id']+'.png');im.save(out,optimize=True);bm=O/(c['id']+'.bin');bm.write_bytes(wm.tobytes());c.update(image=str(out.relative_to(R/'public')),mask=str(bm.relative_to(R/'public')),sha256=sha(out),maskSha256=sha(bm));chunks.append(c)

entries={'palace':[2048,990],'academy':[800,1500],'archive':[2560,1110],'culture':[2610,1550],'transition':[2048,1930],'retail':[1128,2690],'bookshop-occlusion':[1128,2250],'station':[2598.5,2760],'platform':[2970,2680],'namsan':[1200,3260],'maru':[326,3380],'amusement':[2440,3260],'market':[1440,3740],'waterfront':[2048,3790],'ferry':[2900,3480],'jeju-arrival':[3300,3560],'jeju-oreum':[3730,3335],'jeju-culture':[3680,4430]}
frames={'palace':[2048,630],'academy':[1050,1280],'archive':[2500,1050],'culture':[2560,1330],'transition':[2048,1900],'retail':[1184,2410],'bookshop-occlusion':[1184,2410],'station':[2598,2460],'platform':[3100,2460],'namsan':[1184,2940],'maru':[620,3110],'amusement':[2600,3020],'market':[1050,3550],'waterfront':[2200,3820],'ferry':[2640,3550],'jeju-arrival':[3520,3540],'jeju-oreum':[3690,3460],'jeju-culture':[3690,4270]}
review=copy.deepcopy(m);review.update(id='recovery-world',chunks=chunks,objects=objects,artStatus='CONSOLIDATED RECOVERY CANDIDATE / HUMAN ART REVIEW PENDING / BAKERY UNPLACED / P1 ISSUES OPEN',reviewEntries=entries,nativeFrames=frames,spawn=[1128,2690]);review['stops']=[{'id':key,'label':key.replace('-',' '),'x':frames[key][0],'y':frames[key][1],'zoom':.5,'travelMs':1800,'holdMs':2300}for key in ['palace','archive','transition','retail','station','namsan','amusement','market','ferry','jeju-culture']]
over=ground.copy()
for ob in sorted(objects,key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
over.save(D/'world-native-composite.png',optimize=True);over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png',optimize=True);review['overview']='assets/gate3/recovery-world/overview.png';write(O/'manifest.json',review)
before=copy.deepcopy(m);before.update(id='recovery-world-before',reviewEntries=entries,nativeFrames=frames,spawn=review['spawn']);B=R/'public/assets/gate3/recovery-world-before';B.mkdir(exist_ok=True);write(B/'manifest.json',before)
write(S/'integration-provenance.json',{'authority':'docs/current/G3D_WORLD_RECOVERY_AUTHORIZATION.md','generator':'tools/g3dw_build.py','fullWorldPass':True,'finalArtAcceptance':False,'masterplanModified':False,'protectedGround':protected,'panels':records,'removedRejectedPrototypeObjects':removed,'addedObjects':placements,'retailOcclusion':'Original facade textures/colliders unchanged; runtime foreground alpha0.35 only while Juni stands behind facade, otherwise1.0.','nativeScale':1,'resampling':'NONE','stationCanopy':'Original BEFORE source/pivot and blocking8px strip unchanged; no visual connector','bakery':'Required / unplaced. W0 rejected, Q1 not allocated.','collisionChangedPixels':int(np.count_nonzero(walk!=oldwalk))})
write(S/'collision-ownership-amendments.json',{'masterplanChange':False,'approvedRoutesAndReservations':'UNCHANGED','repairs':[{'id':'market-native-front-approach','rect':market_approach,'reason':'Remove obsolete80px placeholder margin beyond fixed contact/root3660. Native104px entrance approach to existing public paving at3740, on existing land. No facade/collider/route relocation.'}],'loosePropFeet':{'id':'market-outer-counter-feet','mask':'assets-src/gate3/recovery-world-v1/market-counter-contact-mask.png','source':market_ob['image'],'origin':[market_ob['x'],market_ob['y']],'pixels':int(counter.sum()),'protectedRouteOverlapPixels':0,'policy':'Native opaque bottom18px of two loose side counters only, outside unchanged780px hall reservation on existing non-route public-space land. Not an expansion of building contact or quay land.'},'protectedStation8pxStrip':'UNCHANGED/CLOSED','protectedHistoricalAndJejuFields':'UNCHANGED'})
print('Built consolidated candidate:',len(chunks),'native chunks;',len(objects),'foregrounds')
land=Image.new('L',(W,H));ld=ImageDraw.Draw(land)
for x,y,w,h in p['land']:ld.rectangle((x,y,x+w-1,y+h-1),fill=255)
land=np.array(land)>0
Image.fromarray(covered.astype('uint8')*255).save(S/'material-coverage.png',optimize=True)
write(D/'material-coverage.json',{'method':'Native authored/protected material ownership union against unchanged planned land, not a quality/acceptance score.','plannedLandPixels':int(land.sum()),'coveredPlannedLandPixels':int((land&covered).sum()),'uncoveredPlannedLandPixels':int((land&~covered).sum()),'mask':'assets-src/gate3/recovery-world-v1/material-coverage.png','allWorldDestinationsComplete':False,'bakery':'Required/unplaced','artAcceptance':'PENDING HUMAN'})
