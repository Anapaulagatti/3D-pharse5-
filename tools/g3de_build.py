"""Residual-only native derived ownership. Geometry/source originals are read-only."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,label,distance_transform_edt
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';O=R/'public/assets/gate3/residual-world';D=R/'docs/gate3-residual'
def rd(p):return json.loads((R/p).read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=rd('public/assets/gate3/aligned-world/manifest.json');p=copy.deepcopy(m);p['id']='residual-world';p['artStatus']='RESIDUAL CORRECTION CANDIDATE / NOT HUMAN APPROVED';W,H=m['size'];g=Image.new('RGBA',(W,H));field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
old=g.copy();records=[]
def obj(id):return next(o for o in p['objects']if o['id']==id)
def save(n,im):
 path=O/(n+'.png');im.save(path);return str(path.relative_to(R/'public'))
def poly(size,points):
 im=Image.new('L',size);ImageDraw.Draw(im).polygon(points,fill=255);return np.array(im)>0
# Actual original static native composition is used only for foreground extraction.
static=old.copy()
for ob in sorted(m['objects'],key=lambda ob:ob['sortY']):static.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
# Palace: source corner balustrade leaked into a timber bay when the old derived
# front phase was corrected. Remove ONLY this misplaced duplicate, not central rails.
ob=obj('alignment/palace-native-front');im=Image.open(R/'public'/ob['image']).convert('RGBA');a=np.array(im);native=a.copy();yy,xx=np.indices(a.shape[:2]);rr,gg,bb=[a[:,:,k].astype(float)for k in range(3)];roi=(xx>=124)&(xx<161)&(yy<89);stone=roi&(rr>70)&(abs(rr-gg)<65)&(rr<gg*1.4)&(gg>bb*.95)
# Exact native timber/lattice donor from another source bay in this SAME derived front.
for y,x in zip(*np.where(stone)):a[y,x]=native[y,37+(x-124)]
im=Image.fromarray(a);ob['image']=save('palace-front-corner-ownership',im);Image.fromarray(stone.astype('uint8')*255).save(S/'palace-corner-retirement-mask.png');records.append({'id':'palace-corner-ownership','worldOrigin':[1510,590],'mask':'palace-corner-retirement-mask.png','nativeDonor':'aligned-world/palace-native-front.png at37+(x-124),sameY','reason':'Retire misplaced source-side return balustrade intruding into timber lattice bay. Central stone stair/rail details, axis2048, threshold685 and roof fixed. No hall shift.'})
# Fine stair-foot apron. Authoring is selected only inside ground material; no stairs
# or rail/stone architectural pixels are selected.
if(S/'palace-apron-authored.png').exists():
 ed=Image.open(S/'palace-apron-authored.png').convert('RGBA');box=(1830,750,2260,835);patch=ed.crop((box[0]-1280,box[1]-120,box[2]-1280,box[3]-120));mask=Image.new('L',patch.size)
 # Follow actual stone-course/joint boundaries, not an arbitrary image rectangle.
 pts=[(0,12),(14,12),(14,0),(416,0),(416,12),(429,12),(429,65),(405,65),(405,84),(20,84),(20,65),(0,65)];ImageDraw.Draw(mask).polygon(pts,fill=255);g.paste(patch,(1830,750),mask);mask.save(S/'palace-apron-ground-mask.png');records.append({'id':'palace-apron','worldRect':[1830,750,430,85],'source':'palace-apron-authored.png','mask':'palace-apron-ground-mask.png','preserved':'Original stair treads/central rail pixels y<750, doorway/roof/architecture unchanged. Native1x no RGB interpolation.'})
# Retail: the wide cafe edge strip contains original source background, not a
# structural side facade. Its genuine hanging plants above the parapet remain.
for name in ['cafe','bookshop','learning']:
 ob=obj('registration/'+name);im=Image.open(R/'public'/ob['image']).convert('RGBA');a=np.array(im);before=a[:,:,3].copy();yy,xx=np.indices(before.shape)
 rgb=a[:,:,:3].astype(float);rr,gg,bb=[rgb[:,:,k]for k in range(3)]
 green=(gg>=rr*.98)&(gg>bb*1.4)&(gg>35);petal=(rr>225)&(gg>215)&(bb>150)&(gg>rr*.94)&(bb>gg*.72)
 if name=='cafe':
  cut=(xx<38)&(yy>=190)
  # Preserve the original attached balcony flowers, hanging lamp and entrance pot.
  attached=(yy>=270)&(yy<389)&(green|petal)&(xx>=12)
  lamp=poly(im.size,[(26,389),(32,399),(33,417),(38,424),(38,466),(21,464),(13,444),(18,415),(22,411)])
  entranceFoliage=(yy>=515)&(yy<580)&(xx>=10)&(green|petal)
  entrancePot=poly(im.size,[(18,568),(38,568),(38,600),(20,600)])
  cut&=~(attached|lamp|entranceFoliage|entrancePot)
 elif name=='bookshop':
  # The old permissive green matte included warm paving/background tree tips.
  flowerSupport=distance_transform_edt(~(petal&(yy>=32)&(yy<85)))<9
  keep=(green|petal)&flowerSupport
  cut=(yy<56)&~keep
 else:
  flowerSupport=distance_transform_edt(~(petal&(yy>=42)&(yy<90)))<9
  keep=(green|petal)&flowerSupport
  cut=(yy<58)&~keep
  # This isolated upward tree limb came from the background, not the terrace bed.
  cut|=(yy<60)&(xx>=95)&(xx<190)
  cut[(xx>=198)&(xx<256)&(yy>=50)]=False # genuine HVAC upper cap
 a[cut,3]=0;ob['image']=save(name+'-owned',Image.fromarray(a));Image.fromarray((before!=a[:,:,3]).astype('uint8')*255).save(S/(name+'-alpha-retirement.png'));records.append({'id':name+'-edge','source':'public/assets/gate3/aligned-world/'+name+'-derived.png','mask':name+'-alpha-retirement.png','RGB':'EXACT','facadeGuards':'Native cafe structural facade localX>=38 below190, attached original balcony flowers/lamp/entrance pot and all RGB exact. Prior wide guard included nonarchitectural left background strip; explicit alpha retirement only there. Bookshop>=2150/learning>=2140 RGBA exact. Roof geometry fixed.'})
# Station potted tree: native existing pixels become an independent foreground
# owner. Only the clipped crown receives NEW pixels. Pot/trunk/contact shadow exact.
bx,by,bw,bh=2820,2490,176,208;tree=static.crop((bx,by,bx+bw,by+bh));ta=np.array(tree);r,gg,b=[ta[:,:,k].astype(float)for k in range(3)];yy,xx=np.indices((bh,bw));wx=xx+bx;wy=yy+by
crownShape=poly((bw,bh),[(57,30),(88,14),(117,11),(138,25),(138,138),(116,138),(104,120),(68,116),(40,121),(13,108),(5,78),(22,63),(50,53)])
green=(gg>=r*.92)&(gg>b*1.4)&(b<125)&(gg>35);crown=crownShape&green
# Small brown branch detail only within the true native crown, never paving.
branch=crownShape&(r>gg*1.15)&(gg>b*1.15)&(gg<125)&(distance_transform_edt(~crown)<3);owned=crown|branch
trunkShape=poly((bw,bh),[(73,105),(95,117),(124,104),(127,114),(108,134),(109,166),(92,169),(84,142)])
trunk=trunkShape&(r>gg*1.12)&(gg>b*1.15)&(r>40);owned|=trunk
pot=poly((bw,bh),[(69,167),(70,160),(77,153),(93,150),(117,150),(130,156),(136,166),(134,193),(123,202),(106,206),(84,203),(73,196),(69,188)])
owned|=pot
# Never absorb corrected rectangular planter pixels or its independent shadow.
owned[(wy>=2607)&(wx<2880)]=False
nativeOwned=owned.copy();ta[:,:,3]=np.where(owned,255,0)
# Complete only the missing natural foliage outside the historical source edge.
if(S/'station-tree-authored.png').exists():
 ed=np.array(Image.open(S/'station-tree-authored.png').convert('RGBA').crop((bx-1920,by-1920,bx-1920+bw,by-1920+bh)));er,eg,eb=[ed[:,:,k].astype(float)for k in range(3)];new=(wx>=2958)&(wx<2990)&(wy>=2500)&(wy<2630)&(eg>=er*.92)&(eg>eb*1.4)&(eb<125)&(eg>35);ta[new]=ed[new];ta[new,3]=255
else:new=np.zeros(owned.shape,bool)
Image.fromarray(nativeOwned.astype('uint8')*255).save(S/'station-tree-native-ownership.png');Image.fromarray((nativeOwned&(wx<2958)).astype('uint8')*255).save(S/'station-tree-preserved-native-mask.png');Image.fromarray(new.astype('uint8')*255).save(S/'station-tree-crown-completion-mask.png')
# Retire the old source copies from facade, canopy and canonical ground underneath
# the opaque true native tree owner. All STATIC approved pixels remain exact.
for id in ['registration/station','registration/station-platform-canopy']:
 ob=obj(id);im=Image.open(R/'public'/ob['image']).convert('RGBA');ar=np.array(im);x1=max(bx,ob['x']);y1=max(by,ob['y']);x2=min(bx+bw,ob['x']+ob['width']);y2=min(by+bh,ob['y']+ob['height'])
 if x1<x2 and y1<y2:
  sm=nativeOwned[y1-by:y2-by,x1-bx:x2-bx];part=ar[y1-ob['y']:y2-ob['y'],x1-ob['x']:x2-ob['x']];part[sm,3]=0
 if id=='registration/station':
  # The old resized source floor was still above canonical restored paving.
  ar[407:,:,3]=0
  # Canopy and background belong to their independent owners, not the building.
  ar[:,571:,3]=0
  # Retain genuine roof/side-attached greenery that projects past the station
  # contact silhouette; foliage is not a reason to keep its baked paving plate.
  originalAlpha=np.array(im)[:,:,3];rgb=ar[:,:,:3].astype(float);r0,g0,b0=[rgb[:,:,k]for k in range(3)];leaves=(g0>=r0*.92)&(g0>b0*1.4)&(b0<125)&(g0>35);petals=(r0>225)&(g0>215)&(b0>145)&(g0>r0*.94);attached=leaves|(petals&(distance_transform_edt(~leaves)<3));yy0,xx0=np.indices(ar.shape[:2]);attached&=(xx0>=571)&(xx0<611)&(yy0>=40)&(yy0<304);ar[attached,3]=originalAlpha[attached]
  # Cropped distant greenery above the rear HVAC is not roof-attached vegetation.
  ar[0:16,60:88,3]=0
  ar[0:30,153:459,3]=0
 else:
  # Exact original roof/post/sign/railing, retire obsolete ground/background only.
  keep=poly(im.size,[(0,18),(40,18),(73,95),(73,178),(57,178),(57,265),(73,265),(73,296),(0,296),(0,274),(12,274),(12,181),(23,181),(23,139),(0,139)])
  keep[0:18]=False;ar[~keep,3]=0
 ob['image']=save('station-facade-owned'if id=='registration/station'else'canopy-owned',Image.fromarray(ar));Image.fromarray(ar[:,:,3]).save(S/('station-owned-alpha.png'if id=='registration/station'else'canopy-owned-alpha.png'))
# Minimal hidden native floor under the retired tree prop, not a repaint of actual
# approved visible paving. Original canonical file and visible static art stay exact.
under=old.crop((bx,by,bx+bw,by+bh));ua=np.array(under);donor=np.array(old.crop((2570,2640,2634,2704)));ua[nativeOwned]=donor[yy[nativeOwned]%64,xx[nativeOwned]%64];g.paste(Image.fromarray(ua),(bx,by),Image.fromarray(nativeOwned.astype('uint8')*255))
p['objects'].append({'id':'residual/station-potted-tree','image':save('station-potted-tree',Image.fromarray(ta)),'x':bx,'y':by,'width':bw,'height':bh,'sortY':2696,'alphaSoftening':.35,'bytes':bw*bh*4})
records.append({'id':'station-tree-ownership','nativeWorldRect':[bx,by,bw,bh],'nativeSource':'Baseline exact static composite / original pot,trunk,crown RGB','newPixelsMask':'station-tree-crown-completion-mask.png','nativeRetirementMask':'station-tree-native-ownership.png','nativePreservationMask':'station-tree-preserved-native-mask.png','priority':'New completion owns pixels at/after2958; preserved native tree source ends2957 inclusive. Retirement mask can include that one border column, outside the original frame.','source':'station-tree-authored.png only outside2958','canonicalPolicy':'Original canonical file immutable. Only old baked tree pixels retire under exact native foreground; actual pavement/tactile/curb/independent shadows and visible static tree unchanged. No unrelated overlay bush.'})
# Southern shore: same large native ocean family and SAME global phase as existing
# offshore water. Retire the old rectangular nearshore water plate, preserve shore
# structure, original foam, promenades, ferry, piers and mainland footprint.
box=(0,3840,3180,4280);region=np.array(g.crop(box));r,gg,b=[region[:,:,k].astype(float)for k in range(3)];blue=(b>r*1.35)&(gg>r*1.2)&(b>45);foam=(r>150)&(gg>r*.94)&(b>r*.94);structure=~(blue|foam);labs,_=label(structure);sizes=np.bincount(labs.ravel());shore=(labs>0)&(sizes[labs]>=20);protected=binary_dilation(shore,iterations=4)|binary_dilation(foam,iterations=2);mask=blue&~protected
plate=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/ocean-authored.png').convert('RGBA'));ys,xs=np.indices(region.shape[:2]);surface=plate[(ys+3840-3200)%1024,(xs-3180)%1536];actual=mask&np.any(region!=surface,axis=2);g.paste(Image.fromarray(surface),(0,3840),Image.fromarray(mask.astype('uint8')*255));Image.fromarray(actual.astype('uint8')*255).save(S/'southern-shared-water-mask.png')
records.append({'id':'southern-water-family','worldRect':[0,3840,3180,440],'source':'assets-src/gate3/reconciliation-v1/ocean-authored.png','nativePhase':[3180,3200],'pixelsChanged':int(actual.sum()),'mask':'southern-shared-water-mask.png','policy':'One existing1536x1024 ocean family, native texels only, no image filters/reflecting/blur or new terrain. Actual shore/foam+4px rock contact protected. No promenade/mainland/pier/ferry change.'})
# Bounded bridge bay water source-edge correction. The abutments, original foam,
# original island land/architecture and existing bridge foreground stay exact.
if(S/'bridge-water-authored.png').exists():
 box=(2816,3072,4352,4096);cur=np.array(g.crop(box));ed=np.array(Image.open(S/'bridge-water-authored.png').convert('RGBA'));r,gg,b=[cur[:,:,k].astype(float)for k in range(3)];er,eg,eb=[ed[:,:,k].astype(float)for k in range(3)]
 water=(b>r*1.45)&(gg>r*1.3)&(b>70);newWater=(eb>er*1.4)&(eg>er*1.25)&(eb>70);foam=(r>150)&(gg>r*.94)&(b>r*.94)
 land=~(water|foam);labs,_=label(land);sizes=np.bincount(labs.ravel());guard=binary_dilation((labs>0)&(sizes[labs]>=20),iterations=5)|binary_dilation(foam,iterations=2)
 shape=poly((1536,1024),[(280,108),(320,88),(500,88),(624,210),(624,475),(584,668),(420,668),(280,550)])
 mask=shape&water&newWater&~guard
 kp=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0
 # Only the original authorized outer-water exception inside canonical C.
 x1=max(2816,3180);y1=max(3072,3200);x2=min(4352,4204);y2=min(4096,4736)
 mask[y1-3072:y2-3072,x1-2816:x2-2816]&=~kp[y1-3200:y2-3200,x1-3180:x2-3180]
 g.paste(Image.fromarray(ed),(2816,3072),Image.fromarray(mask.astype('uint8')*255));Image.fromarray(mask.astype('uint8')*255).save(S/'bridge-bay-water-ownership.png');records.append({'id':'bridge-bay-water','source':'bridge-water-authored.png','origin':[2816,3072],'mask':'bridge-bay-water-ownership.png','pixels':int(mask.sum()),'protection':'Original structures/foam/land+5px contact retained; canonical C source immutable, its prior protected land/nearshore semantic mask wins. Only authorized outer-water family is derived. No structural endpoints or proportions changed.'})
from g3de_ocean_wrap import apply_wrap
g,waterRecord=apply_wrap(g,R,S);records.append(waterRecord)
changed=[]
for c in p['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];part=g.crop((x,y,x+w,y+h))
 if part.tobytes()!=old.crop((x,y,x+w,y+h)).tobytes():
  out=O/(c['id']+'.png');part.save(out);c.update(image=str(out.relative_to(R/'public')),sha256=sha(out));changed.append(c['id'])
# No approved collision/geometry changes in main candidate.
frames={'coast-west':[750,3970],'coast-middle':[2048,3970],'coast-east':[2940,3980],'station-tree':[2940,2590],'archive-corridor':[2580,1020]};entries={'coast-west':[1000,3860],'coast-middle':[2048,3860],'coast-east':[2900,3830],'station-tree':[2598.5,2760],'station-right':[2598.5,2760],'archive-corridor':[2580,1110],'palace-east':[2580,1030]};p['nativeFrames'].update(frames);p['reviewEntries'].update(entries)
wr(O/'manifest.json',p);B=R/'public/assets/gate3/residual-before';B.mkdir(exist_ok=True);before=copy.deepcopy(m);before.update(id='residual-before',nativeFrames=p['nativeFrames'],reviewEntries=p['reviewEntries']);wr(B/'manifest.json',before)
over=g.copy()
for ob in sorted(p['objects'],key=lambda ob:ob['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
for n,box in [('palace',(1280,120,2816,1144)),('station',(1920,1920,3456,2944)),('retail',(320,1600,1856,2624)),('bridge',(2816,3072,4352,4096)),('coast-west',(0,3840,1536,4864)),('coast-middle',(1280,3840,2816,4864)),('coast-east',(2560,3840,4096,4864))]:over.crop(box).save(S/(n+'-after-context.png'))
# Static canonical material guard excluding authorized ownership changes outside
# floor and new crown beyond2958. Save exact diagnostics, never infer art approval.
canon=(2274,2603,2958,2813);beforeCanon=np.array(static.crop(canon));afterCanon=np.array(over.crop(canon));diff=np.any(beforeCanon!=afterCanon,axis=2);Image.fromarray(diff.astype('uint8')*255).save(S/'canonical-static-change-diagnostic.png')
over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');p['overview']='assets/gate3/residual-world/overview.png';wr(O/'manifest.json',p)
wr(S/'integration-provenance.json',{'baseline':'9827761 / visual aligned-world','records':records,'groundChunksChanged':changed,'mainFieldChunksChanged':[],'logicalSolids':'EXACT','protectedPlans':'EXACT','sourceArtwork':'IMMUTABLE','canonicalStaticDiffPixels':int(diff.sum()),'canonicalNativeSource':'IMMUTABLE','roadCandidate':'Separate only, not adopted','archive88px':'Separate only, not adopted','bridgeGeometry':'Unchanged; native stop/turn all-pose clearance proposal separate','sixReviewerImages':'NOT PROVIDED / requested','artAcceptance':'PENDING HUMAN'})
print('Residual candidate:',len(changed),'ground chunks; no collision changes; canonical static differences',int(diff.sum()))
