"""Versioned native zoning ownership. Old sources/manifests remain read-only."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import uniform_filter,distance_transform_edt
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/zoned-world-v1';O=R/'public/assets/gate3/zoned-world';D=R/'docs/gate3-zoned-world'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def world(m):
 im=Image.new('RGBA',m['size']);walk=np.zeros((m['size'][1],m['size'][0]),np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];im.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
 return im,walk
def mincut(a):
 h,w=a.shape;v=a.astype(np.float32).copy();back=np.zeros((h,w),np.int8)
 for y in range(1,h):
  prev=v[y-1];c=np.stack([np.r_[np.inf,prev[:-1]],prev,np.r_[prev[1:],np.inf]]);b=np.argmin(c,axis=0);back[y]=b-1;v[y]+=c[b,np.arange(w)]
 path=np.empty(h,np.int32);path[-1]=np.argmin(v[-1])
 for y in range(h-2,-1,-1):path[y]=path[y+1]+back[y+1,path[y+1]]
 return path
reg=read('assets-src/gate3/zoned-world-v1/land-use-registry.json');m=read('public/assets/gate3/recovery-world/manifest.json');ground,walk=world(m);original=ground.copy();oldwalk=walk.copy();W,H=m['size'];records=[]
# One shared pre-existing native ocean material under authored coastal continuations.
# Scope is water only: no generic landscape/ground tile, tint, blur or resampling.
a=np.array(original);blue=(a[:,:,0]<a[:,:,2]*.65)&(a[:,:,1]>a[:,:,2]*.6)&(a[:,:,2]>70)
waterDensity=uniform_filter(blue.astype(np.float32),size=49,mode='nearest')>.55
shoreDistance=distance_transform_edt(waterDensity)
waterMask=(shoreDistance>24)&blue
waterMask[3200:4736,3180:4204]=False
water=Image.open(R/'public/assets/gate2/c/ground.png').convert('RGBA').crop((0,0,128,128));wa=np.array(water)
sea=Image.fromarray(wa[(np.arange(H)[:,None]-3200)%128,(np.arange(W)[None,:]-3180)%128])
wm=Image.fromarray(waterMask.astype('uint8')*255);wm.save(S/'shared-offshore-ownership.png',optimize=True);ground.paste(sea,(0,0),wm)
# Full accepted native park receiver terrain is protected, in addition to original A/C/floor.
locks=reg['protectedGround']+[{'rect':[416,2760,1536,580],'source':'BASELINE_ACCEPTED_NAMSAN'}]
# Protected actual road registers: no source pixel drift in markings/crosswalks.
roadRects=[[1970,2110,160,1770],[470,2626,1482,128],[2144,2626,130,128],[390,3744,2510,92]]
for name in ['heritageeast','urbanwest','transit','amusement','harborwest','harboreast','railcoast','jejunorth','jejusouth','cityhinge']:
 if name not in reg['regions']or not(S/(name+'-authored.png')).exists():continue
 x,y,w,h=reg['regions'][name];plate=Image.open(S/(name+'-authored.png')).convert('RGBA');assert plate.size==(w,h),(name,plate.size)
 # Native binary depth-contour ownership in water: gradually interleave complete
 # source texels across offshore transition, never alpha-filter source artwork.
 dist=shoreDistance[y:y+h,x:x+w];yy,xx=np.indices((h,w),dtype=np.uint32)
 noise=(((xx+np.uint32(x))*np.uint32(73856093))^((yy+np.uint32(y))*np.uint32(19349663)))
 noise=(noise^(noise>>np.uint32(13)))*np.uint32(1274126177)
 threshold=(noise%np.uint32(65536))/65536.0
 ownership=np.clip((240-dist)/180,0,1);ownership=ownership*ownership*(3-2*ownership)
 mask=threshold<ownership;prev=np.array(ground.crop((x,y,x+w,y+h)));new=np.array(plate)
 # Outer cuts choose native matching pixels in a narrow shared-context band;
 # no opacity feather, RGB blending, stretch, resampling or synthetic sharpening.
 cost=np.abs(prev[:,:,:3].astype(np.float32)-new[:,:,:3]).mean(2)+1;band=32
 left=mincut(cost[:,:band]);right=w-band+mincut(cost[:,-band:]);top=mincut(cost[:band,:].T);bottom=h-band+mincut(cost[-band:,:].T)
 mask&=(np.arange(w)[None,:]>=left[:,None])&(np.arange(w)[None,:]<=right[:,None])&(np.arange(h)[:,None]>=top[None,:])&(np.arange(h)[:,None]<=bottom[None,:])
 if name.startswith('jeju'):
  waterOnly=waterDensity[y:y+h,x:x+w].copy()
  for bx,by,bw,bh in [[3120,3440,60,170],[3120,3950,60,140]]:
   lx=max(0,bx-x);ly=max(0,by-y);rx=min(w,bx+bw-x);ry=min(h,by+bh-y)
   if lx<rx and ly<ry:waterOnly[ly:ry,lx:rx]=True
  mask&=waterOnly
 # All water editing is OUTSIDE the entire canonical Jeju rectangle.
 # Preserve actual original road/marking geometry across independently authored ground.
 for q in locks+[{'rect':v}for v in roadRects]:
  bx,by,bw,bh=q['rect'];lx=max(0,bx-x);ly=max(0,by-y);rx=min(w,bx+bw-x);ry=min(h,by+bh-y)
  if lx<rx and ly<ry:mask[ly:ry,lx:rx]=False
 # Namsan north-west quarter and Maru contact are never included in city/harbor edits.
 if name=='harborwest':mask[:60,:]=False
 im=Image.fromarray(mask.astype('uint8')*255);im.save(S/(name+'-ownership.png'),optimize=True);ground.paste(plate,(x,y),im)
 records.append({'id':name,'source':str((S/(name+'-authored.png')).relative_to(R)),'sha256':sha(S/(name+'-authored.png')),'rect':[x,y,w,h],'mask':str((S/(name+'-ownership.png')).relative_to(R)),'nativeScale':1,'resampling':'NONE','ownedPixels':int(mask.sum())})
# Local station-frontage road continuation WEST to the existing avenue.
# This is not the rejected platform paving connector, not a new reservation,
# and never owns any approved forecourt/source pixels or new collision geometry.
streetSource=S/'station-street-approach-authored.png'
if streetSource.exists():
 street=Image.open(streetSource).convert('RGBA');sm=Image.new('L',street.size)
 ImageDraw.Draw(sm).rectangle((466,438,609,533),fill=255)
 sm.save(S/'station-street-approach-ownership.png',optimize=True);ground.paste(street,(1664,2304),sm)
 records.append({'id':'station-frontage-west-street-continuation','source':str(streetSource.relative_to(R)),'sha256':sha(streetSource),'worldRect':[2130,2742,144,96],'mask':str((S/'station-street-approach-ownership.png').relative_to(R)),'nativeScale':1,'resampling':'NONE','canonicalFloorChangedPixels':0,'masterplanChange':False,'platformConnector':False,'collisionChanges':0,'purpose':'Finish existing frontage roadway into existing avenue through unprotected public-space margin, with swept curb and pedestrian edge. Not a new protected route or land allocation.'})

# Match canonical Jeju boundary texels exactly in the EXTERNAL open-water apron.
# Native reflection is used for water texels only (no island/foam/bridge/land),
# then a binary ownership transition returns to the shared offshore material.
# Source PNG and ALL1024x1536 canonical pixels remain unchanged; no stretching,
# interpolation, color adjustment, invented land or architecture duplication.
j=Image.open(R/'public/assets/gate2/c/ground.png').convert('RGBA');ja=np.array(j)
yy,xx=np.indices((H,W),dtype=np.int16);sx=xx-3180;sy=yy-3200
outside=(sx<0)|(sx>=1024)|(sy<0)|(sy>=1536)
ex=np.maximum(np.maximum(-sx,sx-1023),0);ey=np.maximum(np.maximum(-sy,sy-1535),0);ed=np.maximum(ex,ey)
rx=np.where(sx<0,-sx-1,np.where(sx>=1024,2047-sx,sx));ry=np.where(sy<0,-sy-1,np.where(sy>=1536,3071-sy,sy));rx=np.clip(rx,0,1023);ry=np.clip(ry,0,1535)
donor=ja[ry,rx];a=np.array(ground)
cb=(a[:,:,0]<a[:,:,2]*.65)&(a[:,:,1]>a[:,:,2]*.6)&(a[:,:,2]>70)
db=(donor[:,:,0]<donor[:,:,2]*.65)&(donor[:,:,1]>donor[:,:,2]*.6)&(donor[:,:,2]>70)
weight=np.clip((180-ed)/148,0,1);weight=weight*weight*(3-2*weight)
hashNoise=(((xx.astype(np.uint32))*np.uint32(73856093))^((yy.astype(np.uint32))*np.uint32(19349663)))
hashNoise=(hashNoise^(hashNoise>>np.uint32(13)))*np.uint32(1274126177)
eMask=outside&(ed<180)&cb&db&((hashNoise%np.uint32(65536))/65536.0<weight)
a[eMask]=donor[eMask];ground=Image.fromarray(a)
Image.fromarray(eMask.astype('uint8')*255).save(S/'jeju-external-water-ownership.png',optimize=True)

# Narrow constructed western city seawall on existing land, not new quay land.
wallSource=S/'west-quay-edge-authored.png'
if wallSource.exists():
 wall=Image.open(wallSource).convert('RGBA');oldpart=np.array(ground.crop((0,1740,1536,2764)));newpart=np.array(wall)
 cost=np.abs(oldpart[:,:,[0,1,2]].astype(np.float32)-newpart[:,:,[0,1,2]]).mean(2)+1
 left=96+mincut(cost[:,96:150]);wallMask=(np.arange(1536)[None,:]>=left[:,None])&(np.arange(1536)[None,:]<196)
 wi=Image.fromarray(wallMask.astype('uint8')*255);wi.save(S/'west-quay-edge-ownership.png',optimize=True);ground.paste(wall,(0,1740),wi)
 records.append({'id':'western-city-constructed-seawall','source':str(wallSource.relative_to(R)),'sha256':sha(wallSource),'worldRect':[96,1740,100,1024],'supportRect':[160,1740,30,1024],'mask':str((S/'west-quay-edge-ownership.png').relative_to(R)),'nativeScale':1,'resampling':'NONE','landAllocated':0,'purpose':'Low native granite/basalt seawall defines existing straight engineered city coast; only native water/shadow/foam on seaward side. Maru20px nonpublic gap outside this y-range remains unchanged.'})

# Remove only new noncanonical landscape trees obstructing urban/service/transit/quay space.
remove=['recovery-world/planted-tree-'+str(i).zfill(2)for i in [12,13,14,15,16,20,24]]
objects=copy.deepcopy(m['objects']);removed=[o for o in objects if o['id']in remove];objects=[o for o in objects if o['id']not in remove]
base,basewalk=world(read('public/assets/gate3/registration-working-v3/manifest.json'))
for o in removed:
 cx=o['x']+o['width']//2;cy=o['sortY'];walk[cy-6:cy+8,cx-11:cx+12]=basewalk[cy-6:cy+8,cx-11:cx+12]
# Explicit low-bed contact ownership in visible commercial service/transit space.
# These native base footprints are outside protected facade/contact/floor/island
# envelopes and outside every approved public-path width. Do not use foliage alpha
# as a collider or silently force a route through a garden bed.
environmentContacts=[
 {'id':'western-city-quay-wall','rect':[160,1740,30,1024]},
 {'id':'west-service-low-bed','rect':[172,1950,80,205]},
 {'id':'west-retail-alley-low-bed','rect':[424,2100,38,380]},
 {'id':'retail-east-alley-low-bed','rect':[1790,2310,110,160]},
 {'id':'transit-avenue-low-bed','rect':[2150,2130,60,470]}
]
plan=read('assets-src/gate3/production-plan-v3.1-restored.json')['plan']
routes=Image.new('L',(W,H));rd=ImageDraw.Draw(routes)
for path in plan['paths']:rd.line([tuple(v)for v in path['points']],fill=255,width=path['width'],joint='curve')
routePixels=np.array(routes)>0
for contact in environmentContacts:
 x,y,w,h=contact['rect'];assert not np.any(routePixels[y:y+h,x:x+w]),contact
 assert not any(x<o['x']+o['width']and x+w>o['x']and y<o['y']+o['height']and y+h>o['y']for o in objects if o['id'].startswith(('registration/','a/','c/'))),contact
 walk[y:y+h,x:x+w]=0
 contact['publicRouteOverlapPixels']=0;contact['ownership']='Native low planter-base footprint, not foliage overhang; source art unchanged'

# Verify every protected source/art ownership region including native park remains exact.
protected=[]
for q in locks:
 x,y,w,h=q['rect'];a=ground.crop((x,y,x+w,y+h));b=original.crop((x,y,x+w,y+h));assert a.tobytes()==b.tobytes(),q
 protected.append({'source':q['source'],'rect':q['rect'],'pixelExact':True})
assert not np.any(walk[2626:2755,2950:2958]);chunks=[];changed=[];maskchanged=[]
for c0 in m['chunks']:
 c=copy.deepcopy(c0);x,y,w,h=[c[k]for k in ['x','y','width','height']];part=ground.crop((x,y,x+w,y+h));prior=original.crop((x,y,x+w,y+h))
 if part.tobytes()!=prior.tobytes():
  out=O/(c['id']+'.png');part.save(out,optimize=True);c.update(image=str(out.relative_to(R/'public')),sha256=sha(out));changed.append(c['id'])
 if np.any(walk[y:y+h,x:x+w]!=oldwalk[y:y+h,x:x+w]):
  out=O/(c['id']+'.bin');out.write_bytes(walk[y:y+h,x:x+w].tobytes());c.update(mask=str(out.relative_to(R/'public')),maskSha256=sha(out));maskchanged.append(c['id'])
 chunks.append(c)
review=copy.deepcopy(m);review.update(id='zoned-world',chunks=chunks,objects=objects,artStatus='ZONED ENVIRONMENT CORRECTION CANDIDATE / HUMAN ART AND SPATIAL REVIEW PENDING / BAKERY UNPLACED / P1S OPEN')
for o in objects:assert o==next(v for v in m['objects']if v['id']==o['id'])
extraEntries={'urban-service-west':[330,2300],'urban-service-east':[1780,2440],'urban-density':[1780,2190],'station-amusement':[2598.5,2760],'rail-coast':[2970,2680],'jeju-bridge':[3300,3560],'ocean-transition':[3300,3560]}
extraFrames={'urban-service-west':[640,2280],'urban-service-east':[1840,2260],'urban-density':[1184,1930],'station-amusement':[2598,2810],'rail-coast':[3340,2350],'jeju-bridge':[3180,3520],'ocean-transition':[3540,3100]}
review['reviewEntries'].update(extraEntries);review['nativeFrames'].update(extraFrames)
# Same framing/entries as prior world, supporting exact before-after evidence.
O.mkdir(exist_ok=True);overview=ground.copy()
for o in sorted(objects,key=lambda o:o['sortY']):overview.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
overview.save(D/'world-native-composite.png',optimize=True);overview.thumbnail((870,973),Image.Resampling.NEAREST);overview.save(O/'overview.png',optimize=True);review['overview']='assets/gate3/zoned-world/overview.png';write(O/'manifest.json',review)
before=copy.deepcopy(m);before['id']='zoned-before';before['reviewEntries'].update(extraEntries);before['nativeFrames'].update(extraFrames);write(R/'public/assets/gate3/zoned-before/manifest.json',before)
write(S/'integration-provenance.json',{'baseline':'public/assets/gate3/recovery-world/manifest.json','authority':'docs/current/G3D_ZONING_CORRECTION.md','registry':'assets-src/gate3/zoned-world-v1/land-use-registry.json','panels':records,'protectedRegions':protected,'protectedRoadRects':roadRects,'changedGroundChunks':changed,'unchangedGroundChunks':[c['id']for c in chunks if c['id']not in changed],'changedMaskChunks':maskchanged,'removedUrbanTrees':removed,'removedTreeReason':'Open commercial service alleys, transit sightlines and quay public space. Native tree sources retained; only their explicitly registered foot contacts restored from protected baseline.','newEnvironmentContacts':environmentContacts,'collisionChangedPixels':int(np.count_nonzero(walk!=oldwalk)),'remainingObjectRegistration':'EXACT','logicalSolids':'UNCHANGED','externalJejuWaterApron':{'mask':'assets-src/gate3/zoned-world-v1/jeju-external-water-ownership.png','source':'public/assets/gate2/c/ground.png','transform':'Native1:1 reflected open-water texels OUTSIDE canonical rectangle only; no land/foam/bridge donor pixels and no RGB filtering. Exact edge phase, binary transition32-180px to shared ocean.','protectedIslandPixelsChanged':0},'sharedWater':{'source':'public/assets/gate2/c/ground.png','nativeSourceRect':[0,0,128,128],'phase':[3180,3200],'mask':'assets-src/gate3/zoned-world-v1/shared-offshore-ownership.png','transition':'Native binary source-texel ownership over60-240px physical offshore-depth band; no RGB blending or antialiasing. Stable world-coordinate dither, not rectangular cutoff.','purpose':'Retain existing approved native wave surface as single offshore material; authored coast ownership follows actual shoreline distance, never panel rectangles. No landscape tile shortcut; original Jeju excluded in full.'},'sourceResampling':'NONE','planningAmendments':[],'station8pxStrip':'UNCHANGED/CLOSED','bakery':'Required/unplaced. W0 rejected, Q1 unallocated.','physicalDevices':'NOT TESTED','artAcceptance':'PENDING HUMAN'})
print('Zoned build',len(records),'plates;',len(changed),'affected ground chunks;',len(chunks)-len(changed),'reused;',len(removed),'purpose-based tree removals')
