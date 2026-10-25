"""Surgical masked derivation only. All historical runtime/source files are read-only."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,label
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/final-surgical-v1';D=R/'docs/gate3-final';O=R/'public/assets/gate3/final-world';N=R/'public/assets/gate3/final-station-candidate'
def rd(p):return json.loads((R/p).read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def polygon(size,pts):
 a=Image.new('L',size);ImageDraw.Draw(a).polygon(pts,fill=255);return np.array(a)>0
def cut(cost):
 h,w=cost.shape;a=cost.astype(float).copy();back=np.zeros((h,w),np.int8)
 for y in range(1,h):
  q=np.stack([np.r_[np.inf,a[y-1,:-1]],a[y-1],np.r_[a[y-1,1:],np.inf]]);v=np.argmin(q,axis=0);a[y]+=q[v,np.arange(w)];back[y]=v-1
 out=np.empty(h,int);out[-1]=a[-1].argmin()
 for y in range(h-2,-1,-1):out[y]=out[y+1]+back[y+1,out[y+1]]
 return out
m=rd('public/assets/gate3/final-before/manifest.json');p=copy.deepcopy(m);p['id']='final-world';W,H=m['size'];g=Image.new('RGBA',(W,H));field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
old=g.copy();oldfield=field.copy();records=[];masks={}
def install(id,rect,patch,mask):
 x,y,w,h=rect;assert patch.size==(w,h);assert mask.shape==(h,w)
 assert all(isinstance(v,int)for v in rect)
 g.paste(patch,(x,y),Image.fromarray(mask.astype('uint8')*255));out=S/(id+'-mask.png');Image.fromarray(mask.astype('uint8')*255).save(out);masks[id]={'rect':rect,'mask':str(out.relative_to(R))};records.append({'id':id,'worldRect':rect,'mask':str(out.relative_to(R)),'pixelsSelected':int(mask.sum()),'sampling':'EXACT INTEGER TEXELS / no image resampling'})
# One local farm plate, not a world atlas. Min-error cuts only around its envelope.
rect=[300,230,760,570];x,y,w,h=rect;farm=Image.open(S/'farm-authored.png').convert('RGBA');assert farm.size==(1536,1024);patch=farm.crop((x-160,y-80,x-160+w,y-80+h));a=np.array(patch);prev=np.array(g.crop((x,y,x+w,y+h)));cost=np.abs(a[:,:,:3].astype(float)-prev[:,:,:3]).mean(2);mask=np.ones((h,w),bool)
band=40;left=cut(cost[:,:band]);right=cut(cost[:,-band:]);top=cut(cost[:band,:].T);bottom=cut(cost[-band:,:].T);yy,xx=np.indices((h,w));mask&=(xx>=left[:,None])&(xx<w-band+right[:,None])&(yy>=top[None,:])&(yy<h-band+bottom[None,:]);mask&=polygon((w,h),[(22,0),(700,0),(759,50),(759,450),(700,520),(600,555),(200,569),(45,530),(0,400),(0,70)])
mask &= ~polygon((w,h),[(715,66),(732,60),(759,66),(759,135),(735,135),(715,115)]) # Retire the authored jar that exceeded the envelope; no half prop installed.
mask &= (yy+y>=290) # Preserve original northern woodland; never select a sliced authored tree trunk.
# Old approved border pines remain native foreground owners. The one central
# obsolete tree lies completely within the authorized farm envelope and retires.
removed=[o for o in p['objects']if o['id']=='recovery-world/planted-tree-01'];assert len(removed)==1;p['objects']=[o for o in p['objects']if o not in removed]
install('farm-ground',rect,patch,mask)
# Path floor opens ONLY inside the farm and below the outer fence. Cultivated
# interiors stay non-public; exact180x128 metadata reservations are not collisions.
nav=polygon((w,h),[(35,115),(720,115),(720,500),(570,540),(150,540),(120,569),(0,569),(0,135)])
field[y:y+h,x:x+w][nav]=255
plots=[]
for row,py in enumerate([330,518]):
 for col,px in enumerate([380,600,825]):
  id=f'NW-FARM-{row*3+col+1:02d}';soil=[px+14,py+17,140,88];sx,sy,sw,sh=soil;field[sy:sy+sh,sx:sx+sw]=0
  plots.append({'id':id,'worldRect':[px,py,180,128],'cropDisplayRect':soil,'cropDisplayAnchor':[sx+sw//2,sy+sh//2],'interactionAnchor':[px+90,py+151],'state':'planted','futureStates':['empty','planted','ready'],'navigation':'Cultivated interior non-public; native stone/earth aisles public; no farming logic implemented','collisionRect':soil,'source':'farm-authored.png at native phase160,80','sourceRect':[px-160,py-80,180,128]})
wr(S/'farm-plots.json',{'schema':'korean-arena/farm-spatial-readiness/1','worldEnvelope':rect,'plots':plots,'systemsImplemented':[],'sourceScale':1,'note':'180x128 consistent logical plot reservations, native150-class soil beds with small organic border variation. Actual physical interior140x88; no crop timers/inventory/economy/quest.'});wr(D/'FARM_PLOTS.json',rd('assets-src/gate3/final-surgical-v1/farm-plots.json'));p['farmMetadata']='assets/gate3/final-world/farm-plots.json';wr(O/'farm-plots.json',rd('assets-src/gate3/final-surgical-v1/farm-plots.json'))
# Actual missing roof corner, native continuation of the SAME source house.
rect=[550,880,170,260];x,y,w,h=rect;patch=Image.open(S/'house-court-authored.png').convert('RGBA').crop((x-320,y-650,x-320+w,y-650+h));mask=polygon((w,h),[(0,60),(25,20),(95,0),(169,0),(169,250),(95,259),(32,222),(0,170)])
# Match the retained roof via a native minimum-error40px ownership strip, while
# preserving all source facade/doors and the roof to the east of720.
a=np.array(patch);prev=np.array(g.crop((x,y,x+w,y+h)));cost=np.abs(a[:,:,:3].astype(float)-prev[:,:,:3]).mean(2);seam=cut(cost[:,-40:]);yy,xx=np.indices((h,w));mask&=xx<w-40+seam[:,None];install('house-roof-corner',rect,patch,mask)
# Roof projections over the unchanged western path have their own foreground
# ownership, so Juni does not paint on top of the new eave during a real walk.
rgb=np.array(patch).astype(float);r0,g0,b0=[rgb[:,:,k]for k in range(3)];blue=(b0>=g0*.85)&(g0>=r0*.85)&(b0>35);near=binary_dilation(blue,iterations=12);wood=(r0>g0*1.10)&(g0>b0*1.1);rmask=mask&(blue|(near&wood));rf=np.array(patch);rf[:,:,3]=np.where(rmask,255,0);Image.fromarray(rf).save(O/'house-west-roof.png');p['objects'].append({'id':'surgical/house-west-roof','image':'assets/gate3/final-world/house-west-roof.png','x':x,'y':y,'width':w,'height':h,'sortY':1360,'alphaSoftening':.35,'bytes':w*h*4})

# The garden's western return is a very narrow ground/foreground split; source
# pine/bench/fence RGB outside it remain exact, with original object registration.
rect=[605,1410,90,264];x,y,w,h=rect;patch=Image.open(S/'courtyard-authored.png').convert('RGBA').crop((x-320,y-650,x-320+w,y-650+h));mask=polygon((w,h),[(20,0),(80,0),(89,40),(89,263),(0,263),(0,180),(18,150)])
# Native east join, no opacity feathering.
a=np.array(patch);prev=np.array(g.crop((x,y,x+w,y+h)));seam=cut(np.abs(a[:,:,:3].astype(float)-prev[:,:,:3]).mean(2)[:,-20:]);yy,xx=np.indices((h,w));mask&=xx<w-20+seam[:,None];install('courtyard-west-return',rect,patch,mask)
ob=next(o for o in p['objects']if o['id']=='a/foreground-pine');im=Image.open(R/'public'/ob['image']).convert('RGBA');ar=np.array(im);part=mask[:,640-x:695-x];ar[:,:part.shape[1],3][part]=0;Image.fromarray(ar).save(O/'courtyard-pine-owned.png');ob['image']='assets/gate3/final-world/courtyard-pine-owned.png'
fg=np.array(patch);fmask=mask&polygon((w,h),[(20,0),(80,0),(89,100),(89,263),(0,263),(0,180),(18,150)]);fg[:,:,3]=np.where(fmask,255,0);Image.fromarray(fg).save(O/'courtyard-west-foreground.png');p['objects'].append({'id':'surgical/courtyard-west-return','image':'assets/gate3/final-world/courtyard-west-foreground.png','x':x,'y':y,'width':w,'height':h,'sortY':1650.05,'alphaSoftening':.35,'bytes':w*h*4})
# Small new stone-corner support only, at its ground contact rather than full
# painted height. Existing public lane center580 stays open. No plan relocation.
field[1652:1674,610:635]=0
# Southern promenade road: actual source-family discontinuity occurs at1664,
# NOT the provisional overview-center guess2048. Asphalt only; curbs/markings fixed.
rect=[1510,3768,200,94];x,y,w,h=rect;cur=np.array(g.crop((x,y,x+w,y+h)));donor=np.array(old.crop((1730,3768,1930,3862)));r0,g0,b0=[cur[:,:,k].astype(float)for k in range(3)];r1,g1,b1=[donor[:,:,k].astype(float)for k in range(3)];mask=(r0<125)&(g0<125)&(b0<125)&(abs(r0-g0)<24)&(r1<125)&(g1<125)&(b1<125)&(abs(r1-g1)<24);yy,xx=np.indices((h,w));mask&=(xx<164)&(yy>=10)&(yy<88);seam=cut(np.abs(cur[:,:,:3].astype(float)-donor[:,:,:3]).mean(2)[:,:45]);mask&=xx>=seam[:,None];install('southern-asphalt-phase',rect,Image.fromarray(donor),mask)
# Tiny landing-water ownership seam only: integer native original Jeju water
# donor, no foam/land/bridge/global ocean edits. Original protected bitmap wins.
rect=[3090,3430,160,160];x,y,w,h=rect;cur=np.array(g.crop((x,y,x+w,y+h)));donor=np.array(old.crop((x+64,y,x+64+w,y+h)));r0,g0,b0=[cur[:,:,k].astype(float)for k in range(3)];r1,g1,b1=[donor[:,:,k].astype(float)for k in range(3)];water=(b0>r0*1.45)&(g0>r0*1.3)&(b0>70);newwater=(b1>r1*1.45)&(g1>r1*1.3)&(b1>70);foam=(r0>150)&(g0>r0*.94)&(b0>r0*.94);guard=binary_dilation(~water,iterations=3)|binary_dilation(foam,iterations=3);yy,xx=np.indices((h,w));mask=water&newwater&~guard&(xx>=65)&(xx<110)&(yy<95)
kp=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0
for ly in range(h):
 for lx in range(w):
  wx,wy=x+lx,y+ly
  if 3180<=wx<4204 and 3200<=wy<4736 and kp[wy-3200,wx-3180]:mask[ly,lx]=False
# A binary wavy material boundary follows existing native wave cost rather than a
# rectangular source edge; no new coast structure or bridge support is invented.
seam=cut(np.abs(cur[:,:,:3].astype(float)-donor[:,:,:3]).mean(2)[:,65:85]);mask&=xx>=65+seam[:,None];install('mainland-landing-water',rect,Image.fromarray(donor),mask)
# Per-scene sparse output, exact1:1 chunk bytes only where selected pixels differ.
def publish(q,ground,walk,out):
 out.mkdir(exist_ok=True);changed=[];changedfield=[]
 for c in q['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];part=ground.crop((x,y,x+w,y+h));partfield=walk[y:y+h,x:x+w]
  if part.tobytes()!=Image.open(R/'public'/c['image']).convert('RGBA').tobytes():
   fp=out/(c['id']+'.png');part.save(fp);c.update(image=str(fp.relative_to(R/'public')),sha256=sha(fp));changed.append(c['id'])
  if not np.array_equal(partfield,np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)):
   fp=out/(c['id']+'.bin');fp.write_bytes(partfield.tobytes());c['mask']=str(fp.relative_to(R/'public'));changedfield.append(c['id'])
 over=ground.copy()
 for ob in sorted(q['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
 over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(out/'overview.png');q['overview']=str((out/'overview.png').relative_to(R/'public'));wr(out/'manifest.json',q);return changed,changedfield
changed,cf=publish(p,g,field,O)
# Controlled station replacement candidate: the main scene RETAINS old station.
# Underlying source ground is already free of architectural RGB; retire only the
# residual old-side tactile fragments and narrow obsolete foundation above2603.
n=copy.deepcopy(p);n['id']='final-station-candidate';ng=g.copy();n['objects']=[o for o in n['objects']if o['id']!='registration/station'];newgroundmask=np.zeros((575,742),bool)
for rect in [[2313,2590,571,13],[2884,2490,74,113]]:
 x,y,w,h=rect;cur=np.array(ng.crop((x,y,x+w,y+h)));don=np.array(old.crop((x,y-180,x+w,y-180+h)));ms=np.ones((h,w),bool);ng.paste(Image.fromarray(don),(x,y),Image.fromarray(ms.astype('uint8')*255));newgroundmask[y-2140:y-2140+h,x-2274:x-2274+w]=ms
Image.fromarray(newgroundmask.astype('uint8')*255).save(S/'station-underlying-retirement-mask.png')
# New source is not scaled. Native integer translation(-19,-15) aligns its door
# center and stone foot to approved forecourt. Logical source anchor unchanged.
source=Image.open(S/'station-authored.png').convert('RGBA');A=np.array(source);shape=polygon(source.size,[(474,288),(914,288),(914,322),(949,322),(949,390),(979,475),(979,698),(894,698),(894,676),(528,676),(528,698),(414,698),(414,552),(383,552),(383,472),(414,472),(414,350),(474,350)])
# Keep real attached flower/HVAC edges, not any of the surrounding pavement.
# Hand-authored binary geometric ownership, alpha never interpolated.
shape[np.indices(shape.shape)[0]>=698]=False
A[:,:,3]=np.where(shape,255,0);srcbox=(380,276,980,699);asset=Image.fromarray(A).crop(srcbox);asset.save(S/'station-independent-complete.png');arr=np.array(asset);yy,xx=np.indices(arr.shape[:2]);roof=(yy<115)&(arr[:,:,3]>0);elevated=(yy>=115)&(yy<260)&(arr[:,:,3]>0);body=(yy>=260)&(arr[:,:,3]>0)
base=[2281,2181];parts=[]
for name,ms,depth in [('roof',roof,2590),('upper',elevated,2590),('facade',body,2590)]:
 ar=arr.copy();ar[:,:,3]=np.where(ms,255,0);fp=N/('station-'+name+'.png');Image.fromarray(ar).save(fp);ob={'id':'surgical/station-'+name,'image':str(fp.relative_to(R/'public')),'x':base[0],'y':base[1],'width':asset.width,'height':asset.height,'sortY':depth,'alphaSoftening':1,'sourceAnchor':[2313.5,2196],'sourcePivot':[32.5,15],'bytes':asset.width*asset.height*4};n['objects'].append(ob);parts.append(ob)
# Retain original canopy, independent planters, native crown, original contact
# shadows and physical transfer strip. No new paving connector.
stationChanges,stationFields=publish(n,ng,field,N)
stage=copy.deepcopy(n);stage['id']='final-station-ground';stage['objects']=[o for o in stage['objects']if not o['id'].startswith('surgical/station-')];stageO=R/'public/assets/gate3/final-station-ground';publish(stage,ng,field,stageO)
wr(S/'integration-provenance.json',{'baseline':'aad3b3c / residual-world','records':records,'masks':masks,'groundChunksChanged':changed,'fieldChunksChanged':cf,'newGardenCollisionFoot':{'rect':[610,1652,25,22],'reason':'New stone-corner support foot only; existing western lane580 stays open'},'removedFarmTree':removed,'oldStationMainScene':'RETAINED EXACT','newStationDecision':'PENDING / isolated candidate; not force-adopted','stationCandidateChunks':stationChanges,'stationCandidateFieldChunks':stationFields,'stationSourceTranslation':[-19,-15],'stationArchitectureOrigin':base,'stationSourceAnchor':[2313.5,2196],'stationSourcePivot':[32.5,15],'stationRasterOriginEquation':'[2313.5-32.5,2196-15]=[2281,2181]','entrance':'Existing public target2598,2610 and logical solids unchanged; source door center translated from697 to678=contextworld2598','architectureLayers':parts,'groundStage':'final-station-ground / old station active instance removed, no new architecture; canonical forecourt/canopy/props remain','protectedStationForecourt':'Ground y>=2603 unmodified in station candidate','islandLanding':'Inspected / unchanged: canonical basalt, foam, posts and path currently coherent; no protected-source repaint','minorPalaceRetail':'Inspected / unchanged: no new objective defect requiring another edit','scope':'Explicit masks only; no global water/source atlas rebuild','artAcceptance':'PENDING HUMAN'})
print('Surgical:',changed,'field:',cf,'station candidate',stationChanges,'main original station retained')
