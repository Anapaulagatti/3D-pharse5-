"""Reconcile shared ownership and approved geometry; historical sources are read-only."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy.ndimage import uniform_filter,distance_transform_edt,label,binary_dilation
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/reconciliation-v1';O=R/'public/assets/gate3/reconciled-world';D=R/'docs/gate3-reconciliation'
def rd(p):return json.loads((R/p).read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def world(m):
 g=Image.new('RGBA',m['size']);a=np.zeros((m['size'][1],m['size'][0]),np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));a[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
 return g,a
m=rd('public/assets/gate3/zoned-world/manifest.json');reg=rd('assets-src/gate3/reconciliation-v1/registry.json');plan=rd('assets-src/gate3/production-plan-v3.1-restored.json')['plan'];g,a=world(m);old=g.copy();oldfield=a.copy();W,H=m['size'];records=[];objects=copy.deepcopy(m['objects'])
def maskrect(mask,worldrect,origin,fill):
 x,y,w,h=worldrect;ox,oy=origin;ImageDraw.Draw(mask).rectangle((x-ox,y-oy,x+w-ox-1,y+h-oy-1),fill=fill)
# Canonical Jeju land/foam/architecture preservation: semantic offshore exception only.
c=Image.open(R/'public/assets/gate2/c/ground.png').convert('RGBA');ca=np.array(c);nw=(ca[:,:,0]>=ca[:,:,2]*.65)|(ca[:,:,1]<=ca[:,:,2]*.6)|(ca[:,:,2]<70)
lab,n=label(nw);sizes=np.bincount(lab.ravel());keep=(lab>0)&(sizes[lab]>=36);keep=binary_dilation(keep,iterations=18)
# Conservative main island/nearshore envelope plus bridge/piers; water beyond it is editable.
semantic=Image.new('L',c.size);sd=ImageDraw.Draw(semantic)
sd.polygon([(130,110),(280,30),(780,0),(1000,100),(1023,280),(1023,540),(970,740),(1023,820),(1023,1100),(970,1160),(1000,1250),(950,1340),(830,1460),(620,1470),(450,1440),(260,1400),(80,1330),(30,1260),(30,1140),(100,1020),(40,940),(0,920),(0,780),(80,780),(100,650),(0,630),(0,450),(130,450),(130,400),(280,430),(320,360),(170,320),(100,250),(100,170)],fill=255)
sd.polygon([(0,320),(120,340),(320,390),(350,430),(220,440),(110,420),(0,440)],fill=255)
keep|=np.array(semantic)>0
# Entire interior source is protected; only original outer160px water band can be excepted.
yy,xx=np.indices((1536,1024));edge=np.minimum.reduce([xx,1023-xx,yy,1535-yy]);keep|=edge>=160
Image.fromarray(keep.astype('uint8')*255).save(S/'jeju-protected-land-nearshore.png',optimize=True)
waterException=~keep;Image.fromarray(waterException.astype('uint8')*255).save(S/'jeju-water-boundary-exception.png',optimize=True)
# One clean authored offshore family; no mirrored source donors or duplicated rocks/trees.
b=np.array(old);blue=(b[:,:,0]<b[:,:,2]*.65)&(b[:,:,1]>b[:,:,2]*.6)&(b[:,:,2]>70);waterDensity=uniform_filter(blue.astype(np.float32),49)>.55;depth=distance_transform_edt(waterDensity)
yw,xw=np.indices((H,W),dtype=np.int16);noise=(((xw.astype(np.uint32))*73856093)^((yw.astype(np.uint32))*19349663));noise=(noise^(noise>>13))*np.uint32(1274126177);noise=(noise%65536)/65536
sea=ca[0:128,0:128];shallow=ca[240:304,70:134]
baseSea=sea[(yw-3200)%128,(xw-3180)%128];nearSea=shallow[(yw-3200)%64,(xw-3180)%64]
oceanPlate=np.array(Image.open(S/'ocean-authored.png').convert('RGBA'));pixels=oceanPlate[(yw-3200)%1024,(xw-3180)%1536];ocean=Image.fromarray(pixels);land=Image.new('L',(W,H));ld=ImageDraw.Draw(land)
for lx,ly,lw,lh in plan['land']:ld.rectangle((lx,ly,lx+lw-1,ly+lh-1),fill=255)
landDistance=distance_transform_edt(np.array(land)==0);plannedSea=landDistance>80
oldReflection=np.array(Image.open(R/'assets-src/gate3/zoned-world-v1/jeju-external-water-ownership.png'))>0
# Preserve actual structural shoreline connected to approved land, not a rectangular
# distance cutoff. Detached reflected rock/wave fragments remain ocean-owned.
structural=(b[:,:,0]>=b[:,:,2]*.8)&(b[:,:,0]>=b[:,:,1]*.6)&(b[:,:,2]<170)
sl,sn=label(binary_dilation(structural,iterations=2));anchored=np.unique(sl[(np.array(land)>0)&structural]);anchored=anchored[anchored>0]
shoreStructure=np.isin(sl,anchored)&structural;physicalDistance=distance_transform_edt(~shoreStructure)
oldFoam=(b[:,:,0]>160)&(b[:,:,1]>=b[:,:,0]*.96)&(b[:,:,2]>=b[:,:,0]*.98)
shorePhysical=binary_dilation(shoreStructure,iterations=5)|binary_dilation(oldFoam&(physicalDistance<64),iterations=3)
Image.fromarray(shorePhysical.astype('uint8')*255).save(S/'physical-shore-preservation.png',optimize=True)
wm=(plannedSea|oldReflection|waterDensity)&~shorePhysical;wm[3180:3200,3180:4204]=True;wm[3200:4736,3180:4204]=waterException&(noise[3200:4736,3180:4204]<np.clip((160-edge)/80,0,1))
g.paste(ocean,(0,0),Image.fromarray(wm.astype('uint8')*255));Image.fromarray(wm.astype('uint8')*255).save(S/'shared-ocean-ownership.png',optimize=True)
# Derive station facade ownership separately from top background and central baked floor.
station=next(o for o in objects if o['id']=='registration/station');si=Image.open(R/'public'/station['image']).convert('RGBA');sa=np.array(si);retire=Image.new('L',si.size);dd=ImageDraw.Draw(retire)
dd.rectangle((160,0,459,18),fill=255);dd.polygon([(0,0),(77,0),(77,11),(40,39),(0,109)],fill=255);dd.rectangle((120,407,492,452),fill=255)
ret=np.array(retire)>0;sa[ret,3]=0;Image.fromarray(sa).save(O/'station-facade-derived.png',optimize=True);retire.save(S/'station-background-retirement.png',optimize=True)
station['image']='assets/gate3/reconciled-world/station-facade-derived.png'
assert np.array_equal(sa[~ret],np.array(si)[~ret]);assert np.array_equal(sa[:,:,:3],np.array(si)[:,:,:3])
# Shared environment panels, with architecture/floor/road ownership winning over generated context.
for name in ['palacewest','palaceeast','commercial','station']:
 x,y,w,h=reg['regions'][name];plate=Image.open(S/(name+'-authored.png')).convert('RGBA');assert plate.size==(w,h)
 mask=Image.new('L',(w,h),255)
 # Keep a narrow original-context rim; surfaces are reviewed at native scale.
 md=ImageDraw.Draw(mask);md.rectangle((0,0,w-1,h-1),outline=0,width=8)
 if name.startswith('palace'):
  # Do not repaint approved A gardens wholesale. Only explicit reconciliation corridors
  # and non-protected upper/eastern surrounds are editable inside the old image frame.
  maskrect(mask,[640,650,1536,1024],(x,y),0)
  for q in [[1060,650,90,390],[1110,985,720,100],[1830,790,430,340]]:maskrect(mask,q,(x,y),255)
  # Native wall-family sprites below own these bands; no duplicate generated roof courses.
  maskrect(mask,[1000,150,2200,105],(x,y),0)
  for q in reg['architecturePreservation']:maskrect(mask,q['rect'],(x,y),0)
 if name=='commercial':
  for q in [[1790,2310,110,160],[2150,2130,60,470]]:maskrect(mask,q,(x,y),0)
 if name.startswith('water'):
  arr=np.array(mask)>0;arr&=waterDensity[y:y+h,x:x+w];arr&=np.array(plate)[:,:,0]<np.array(plate)[:,:,2]*.65
  # Never reinstall reflected/ghost rocks from old context in deep open sea.
  arr&=~plannedSea[y:y+h,x:x+w]
  # Nearshore source context is preserved; no authored land/bridge pixels are ever installed.
  near=(depth[y:y+h,x:x+w]<240);weight=np.clip((300-depth[y:y+h,x:x+w])/150,0,1);arr&=(noise[y:y+h,x:x+w]<weight)|near
  mask=Image.fromarray(arr.astype('uint8')*255)
 # Canonical floor and original shared streets stay exact, not repainted to hide joins.
 for q in [[2274,2603,684,210],[1970,2110,160,1770],[470,2626,1482,128],[390,3744,2510,92]]:maskrect(mask,q,(x,y),0)
 # Jeju source exception is constrained by an explicit protected semantic mask.
 ma=np.array(mask);lx=max(x,3180);ly=max(y,3200);rx=min(x+w,4204);ry=min(y+h,4736)
 if lx<rx and ly<ry:
  sub=ma[ly-y:ry-y,lx-x:rx-x];kp=keep[ly-3200:ry-3200,lx-3180:rx-3180];sub[kp]=0
  if name.startswith('water'):
   edgepart=edge[ly-3200:ry-3200,lx-3180:rx-3180];weight=np.clip((160-edgepart)/80,0,1)
   pa=np.array(plate)[ly-y:ry-y,lx-x:rx-x];eligible=(~kp)&(pa[:,:,0]<pa[:,:,2]*.65)&(noise[ly:ry,lx:rx]<weight)
   sub[eligible]=255
 mask=Image.fromarray(ma);mask.save(S/(name+'-ownership.png'),optimize=True);g.paste(plate,(x,y),mask);records.append({'id':name,'source':str((S/(name+'-authored.png')).relative_to(R)),'rect':[x,y,w,h],'mask':str((S/(name+'-ownership.png')).relative_to(R)),'nativeScale':1,'resampling':'NONE'})
# Shared water owns ocean pixels AFTER all regional ground panels, too.
# Otherwise source-panel context silently overwrites the ocean and exposes its frame.
g.paste(ocean,(0,0),Image.fromarray(wm.astype('uint8')*255))
# Complete only native foam next to physically connected shore structures.
# No authored rock/land/tree or detached ghost-water context is installed.
for foamName in ['station','waternorth','watersouth']:
 fx,fy,fw,fh=reg['regions'][foamName];foamSource=Image.open(S/(foamName+'-authored.png')).convert('RGBA');fp=np.array(foamSource);current=np.array(g.crop((fx,fy,fx+fw,fy+fh)))
 white=(fp[:,:,0]>160)&(fp[:,:,1]>=fp[:,:,0]*.96)&(fp[:,:,2]>=fp[:,:,0]*.98)
 cb=(current[:,:,0]<current[:,:,2]*.65)&(current[:,:,2]>70);cf=(current[:,:,0]>160)&(current[:,:,1]>=current[:,:,0]*.96)&(current[:,:,2]>=current[:,:,0]*.98)
 foamMask=white&(cb|cf)&(landDistance[fy:fy+fh,fx:fx+fw]>8)&(physicalDistance[fy:fy+fh,fx:fx+fw]<64)
 lx=max(fx,3180);ly=max(fy,3200);rx=min(fx+fw,4204);ry=min(fy+fh,4736)
 if lx<rx and ly<ry:foamMask[ly-fy:ry-fy,lx-fx:rx-fx]=False
 fm=Image.fromarray(foamMask.astype('uint8')*255);fm.save(S/(foamName+'-shore-foam-ownership.png'),optimize=True);g.paste(foamSource,(fx,fy),fm)
gc=np.array(g.crop((3180,3200,4204,4736)));oc=np.array(old.crop((3180,3200,4204,4736)));gc[keep]=oc[keep];g.paste(Image.fromarray(gc),(3180,3200))
# Full approved south opening/court, no surviving old gate post or garden intrusions.
court=Image.open(R/'assets-src/gate3/zoned-world-v1/urbanwest-authored.png').convert('RGBA').crop((740,470,1170,810));g.paste(court,(1830,790));g.paste(court.crop((0,110,20,340)),(1810,900));court.save(S/'ceremonial-native-paving.png',optimize=True);records.append({'id':'ceremonial-court','worldRect':[1830,790,430,275],'source':'assets-src/gate3/zoned-world-v1/urbanwest-authored.png','sourceRect':[740,470,430,340],'trialRejected':'court-authored.png introduced forbidden new piers; not installed','retiredLeftPierFringe':[1810,900,20,230],'policy':'Explicit reversible terrain ownership inside old A, not source PNG mutation. Architectural pixels above790 and west pavilion outside court preserved.'})
# Source-preserving gate piers re-registered to the APPROVED south opening ends.
sourceA=Image.open(R/'public/assets/gate2/a/ground.png').convert('RGBA')
pierSpecs=[('left',(1170,260,1250,445),[(42,17),(48,19),(49,27),(56,30),(61,38),(75,42),(77,49),(71,55),(62,58),(63,89),(66,90),(66,156),(70,158),(70,173),(29,173),(29,158),(30,156),(30,91),(36,90),(36,61),(27,58),(21,56),(20,49),(25,43),(29,41),(34,33),(38,31),(39,24)],(1760,892)),('right',(1380,260,1490,450),[(44,16),(49,18),(50,27),(55,33),(59,40),(72,43),(73,50),(67,55),(60,58),(61,88),(63,91),(63,157),(67,159),(67,175),(27,175),(27,159),(29,156),(29,92),(34,89),(34,60),(23,57),(18,52),(18,44),(26,41),(29,34),(37,30),(40,24)],(2233,890))]
for name,box,points,(x,y)in pierSpecs:
 im=sourceA.crop(box);alpha=Image.new('L',im.size);ImageDraw.Draw(alpha).polygon(points,fill=255);alpha=alpha.filter(ImageFilter.MaxFilter(5));im.putalpha(alpha);im.save(O/('gate-pier-'+name+'.png'),optimize=True);alpha.save(S/('gate-pier-'+name+'-mask.png'),optimize=True)
 objects.append({'id':'reconciliation/gate-pier-'+name,'image':'assets/gate3/reconciled-world/gate-pier-'+name+'.png','x':x,'y':y,'width':im.width,'height':im.height,'sortY':1065,'alphaSoftening':.35,'bytes':im.width*im.height*4})
 records.append({'id':'gate-pier-'+name,'source':'public/assets/gate2/a/ground.png','sourceRect':list(box),'worldOrigin':[x,y],'supportPlane':'Original Gate1 south wall ends; native RGB copied exactly, new mask/registration explicit. No scale/architecture repaint.'})
# One reusable native wall family, ground support planes registered from approved plan.
wallSource=Image.open(S/'palacewest-authored.png').convert('RGBA');horizontal=Image.open(S/'palaceeast-authored.png').convert('RGBA').crop((20,65,1220,114));vertical=Image.open(S/'palaceeast-authored.png').convert('RGBA').crop((1210,140,1246,840))
# Dedicated wall-side paving owns retired source courses; no old roof tips,
# duplicated foundations or generated garden gate remnants remain under new walls.
apron=Image.open(S/'ceremonial-native-paving.png').convert('RGBA')
for ax,ay,aw,ah in [[1070,170,73,870],[2874,170,69,870],[1110,127,1830,73],[1110,985,720,80],[2260,985,680,80]]:
 for py in range(0,ah,apron.height):
  for px in range(0,aw,apron.width):
   cw=min(apron.width,aw-px);ch=min(apron.height,ah-py);g.paste(apron.crop((0,0,cw,ch)),(ax+px,ay+py))

# Protected baked architecture always wins over wall-side terrain retirement.
for protected in reg['architecturePreservation']:
 px,py,pw,ph=protected['rect'];g.paste(old.crop((px,py,px+pw,py+ph)),(px,py))
wallRecords=[]
for boundary in reg['approvedBoundaries']:
 bid=boundary['id'];x,y,w,h=boundary['rect']
 if w>h:
  im=Image.new('RGBA',(w,horizontal.height));pos=0
  while pos<w:
   k=min(horizontal.width,w-pos);im.paste(horizontal.crop((0,0,k,horizontal.height)),(pos,0));pos+=k
  oy=y+h-im.height;out=O/(bid+'.png');im.save(out,optimize=True);objects.append({'id':'reconciliation/'+bid,'image':str(out.relative_to(R/'public')),'x':x,'y':oy,'width':w,'height':im.height,'sortY':y+h,'alphaSoftening':.35,'bytes':w*im.height*4})
 else:
  for pos in range(0,h,128):
   k=min(128,h-pos);off=pos%vertical.height
   im=vertical.crop((0,off,vertical.width,min(off+k,vertical.height)))
   if im.height<k:im2=Image.new('RGBA',(im.width,k));im2.paste(im,(0,0));im2.paste(vertical.crop((0,0,im.width,k-im.height)),(0,im.height));im=im2
   ox=x-3;out=O/(bid+'-'+str(pos)+'.png');im.save(out,optimize=True);objects.append({'id':'reconciliation/'+bid+'-'+str(pos),'image':str(out.relative_to(R/'public')),'x':ox,'y':y+pos,'width':im.width,'height':k,'sortY':y+pos+k,'alphaSoftening':.35,'bytes':im.width*k*4})
 a[y:y+h,x:x+w]=0;wallRecords.append({'id':bid,'supportRect':boundary['rect'],'nativeSourceFamily':'palaceeast horizontal49px / support last25px / palaceeast vertical36px native course / support offset3px / native roof overhang3px','resampling':'NONE','visualProjection':'Roof courses may project above/left of ground support. No footprint inferred from roof bbox.'})
# Restore only documented ceremonial public ownership, never blindly clear native scenery.
a[790:1130,1830:2260]=255
# Restore original northern support rectangles; do not clear collision to fake
# reachability of a protected painted facade that does not fit its approved slot.
for building in reg['northernBuildings']:
 x,y,w,h=building['rect'];a[y:y+h,x:x+w]=0
# Preserve all modern colliders and the inherited platform strip.
for solid in m['logicalSolids']:
 x,y,w,h=solid['rect'];a[int(y):int(y+h),int(x):int(x+w)]=oldfield[int(y):int(y+h),int(x):int(x+w)]
assert not np.any(a[2626:2755,2950:2958]);assert np.array_equal(np.array(g.crop((2274,2603,2958,2813))),np.array(old.crop((2274,2603,2958,2813))))
assert np.array_equal(np.array(g.crop((3180,3200,4204,4736)))[keep],np.array(old.crop((3180,3200,4204,4736)))[keep])
chunks=[];changed=[];maskchanged=[]
for c0 in m['chunks']:
 c0=copy.deepcopy(c0);x,y,w,h=[c0[k]for k in ['x','y','width','height']];part=g.crop((x,y,x+w,y+h))
 if part.tobytes()!=old.crop((x,y,x+w,y+h)).tobytes():
  out=O/(c0['id']+'.png');part.save(out,optimize=True);c0.update(image=str(out.relative_to(R/'public')),sha256=sha(out));changed.append(c0['id'])
 if not np.array_equal(a[y:y+h,x:x+w],oldfield[y:y+h,x:x+w]):
  out=O/(c0['id']+'.bin');out.write_bytes(a[y:y+h,x:x+w].tobytes());c0.update(mask=str(out.relative_to(R/'public')),maskSha256=sha(out));maskchanged.append(c0['id'])
 chunks.append(c0)
review=copy.deepcopy(m);review.update(id='reconciled-world',chunks=chunks,objects=objects,artStatus='SPATIAL/SHARED-OWNERSHIP RECONCILIATION CANDIDATE / HUMAN REVIEW PENDING / PROTECTED ART CONFLICTS OPEN')
entries={'palace-compound':[2048,1090],'palace-court':[2048,990],'palace-west':[1740,1090],'palace-east':[2320,1110],'station-precinct':[2598.5,2760],'station-rear':[2680,2100],'station-left':[2260,2530],'station-right':[2970,2680],'station-forecourt':[2598.5,2760],'station-amusement':[2440,3260],'modern':[1128,2690],'jeju-bridge':[3300,3560],'jeju-offshore':[3300,3560],'jeju-south':[3590,4390]}
frames={'palace-compound':[2020,720],'palace-court':[2048,920],'palace-west':[1500,900],'palace-east':[2650,900],'station-precinct':[2680,2480],'station-rear':[2598,2110],'station-left':[2260,2440],'station-right':[3040,2440],'station-forecourt':[2598,2630],'station-amusement':[2598,2810],'modern':[1184,2410],'jeju-bridge':[3180,3520],'jeju-offshore':[3690,3180],'jeju-south':[3690,4270]}
review['reviewEntries'].update(entries);review['nativeFrames'].update(frames)
over=g.copy()
for o in sorted(objects,key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
over.save(D/'world-native-composite.png',optimize=True);over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png',optimize=True);review['overview']='assets/gate3/reconciled-world/overview.png';wr(O/'manifest.json',review)
before=copy.deepcopy(m);before.update(id='reconciled-before',reviewEntries=review['reviewEntries'],nativeFrames=review['nativeFrames']);wr(R/'public/assets/gate3/reconciled-before/manifest.json',before)
wr(S/'integration-provenance.json',{'baseline':reg['baselineManifest'],'sources':records,'walls':wallRecords,'changedGroundChunks':changed,'changedMaskChunks':maskchanged,'stationDerived':{'source':'public/assets/gate3/registration/station.png','retirementMask':'assets-src/gate3/reconciliation-v1/station-background-retirement.png','nativeRGBExact':True,'facadeAlphaExactOutsideExplicitBackground':True,'registrationPivotUnchanged':True,'floor':'EXACT / independent canonical owner'},'jejuException':{'mask':'assets-src/gate3/reconciliation-v1/jeju-water-boundary-exception.png','protectedLandMask':'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png','protectedPixelsExact':True,'sourcePNGUnchanged':True,'authorized':'Explicit reversible water-boundary exception in latest directive','changedSourceFramePixels':int(np.any(np.array(g.crop((3180,3200,4204,4736)))!=np.array(old.crop((3180,3200,4204,4736))),axis=2).sum()),'reflectionDonors':'NONE / retired prior reflection system','nativeWaterFamily':{'source':'assets-src/gate3/reconciliation-v1/ocean-authored.png','nativeExtent':[1536,1024],'transform':'Integer native translation/phase only, no reflection or RGB filtering','trialPolicy':'Final revision selects the clean1536x1024 authored offshore family at native1:1 rather than visibly repeating128px samples. Contextual waternorth/watersouth RGB with ghost fragments remains rejected; only physical-shore foam recovered. Canonical Jeju nearshore is protected.','externalSourceEdgeCleanup':[3180,3180,1024,20]}},'collisionOwnership':'Approved northern building supports/wall supports and430px ceremonial south opening/court reclaimed. Modern colliders, native Jeju field and station8px strip unchanged.','protectedArchitecture':'All original building registrations unchanged; Gate1 gate-pier correction explicitly source-preserving','planningAmendments':[],'artAcceptance':'PENDING HUMAN / plinth/cropped-source conflicts remain'})
print('Reconciled candidate built:',len(changed),'ground chunks;',len(maskchanged),'field chunks;',len(objects),'objects')
