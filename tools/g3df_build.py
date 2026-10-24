"""Five-area derived candidate. Canonical sources/plans/checkpoints are read-only."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,label,distance_transform_edt,uniform_filter
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/alignment-v1';O=R/'public/assets/gate3/aligned-world';D=R/'docs/gate3-alignment'
def rd(p):return json.loads((R/p).read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=rd('public/assets/gate3/reconciled-world/manifest.json');p=copy.deepcopy(m);p['id']='aligned-world';p['artStatus']='FIVE-AREA DERIVED CORRECTION CANDIDATE / HUMAN APPROVAL PENDING';W,H=m['size'];g=Image.new('RGBA',(W,H));field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
old=g.copy();oldfield=field.copy();records=[]
def obj(id):return next(o for o in p['objects']if o['id']==id)
def saveimage(name,im):
 out=O/(name+'.png');im.save(out);return str(out.relative_to(R/'public'))
# Native retail: recover attached rooftop leaves above historical crop, remove paving/background.
src=Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGBA')
retail=[('cafe',(35,155,450,756),[(40,240),(435,239),(450,268),(450,756),(35,756),(35,340),(63,285),(66,260)],[(45,170,175,315),(300,250,405,330)]),('bookshop',(450,190,780,756),[(466,251),(480,247),(750,246),(780,274),(780,756),(450,756),(450,292)],[(477,218,770,300)]),('learning',(780,155,1080,756),[(798,217),(1025,214),(1070,244),(1080,268),(1080,756),(780,756),(780,263)],[(795,180,1035,265)])]
for name,box,poly,plants in retail:
 o=obj('registration/'+name);sx,sy,ex,ey=box;dx,dy={'cafe':(475,1835),'bookshop':(530,1835),'learning':(530,1835)}[name];im=src.crop(box);mask=Image.new('L',im.size);dr=ImageDraw.Draw(mask);dr.polygon([(x-sx,y-sy)for x,y in poly],fill=255)
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,bg,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2];green=(bg>r*.88)&(bg>b*1.15)&(bg>45);flowers=(r>135)&(bg>105)&(b<bg*.85);vegetation=binary_dilation(green,iterations=1)&(green|flowers)
 mm=np.array(mask)>0
 for x,y,x2,y2 in plants:
  roi=np.zeros(mm.shape,bool);roi[max(0,y-sy):min(im.height,y2-sy),max(0,x-sx):min(im.width,x2-sx)]=True
  petal=(r>210)&(bg>190)&(b>120)&(b<bg*.9)&(r<bg*1.3)&(uniform_filter(green.astype(float),5)>.25)
  supported=distance_transform_edt(~petal)<12
  mm|=roi&vegetation&supported
 # Native chimney top recovered; protected facade body unchanged in world coordinates.
 if name=='cafe':
  chimney=Image.new('L',im.size);ImageDraw.Draw(chimney).polygon([(390-sx,205-sy),(399-sx,202-sy),(409-sx,206-sy),(411-sx,211-sy),(407-sx,219-sy),(407-sx,246-sy),(390-sx,246-sy),(390-sx,219-sy),(386-sx,212-sy)],fill=255);mm|=np.array(chimney)>0
 # Separate the rounded attached flower crown from the tree behind it.
 if name=='cafe':
  yy,xx=np.indices(mm.shape);wx=xx+sx;wy=yy+sy;crown=((wx-105)/70)**2+((wy-233)/53)**2<=1;zone=(wx<185)&(wy<238);mm[zone]&=crown[zone]
 # Keep the facade-connected silhouette; retire detached source-background fragments.
 labs,_=label(mm);anchor=labs[im.height-20,im.width//2];mm&=labs==anchor
 a[:,:,3]=np.where(mm,a[:,:,3],0);im=Image.fromarray(a);mask=Image.fromarray(mm.astype('uint8')*255);mask.save(S/(name+'-ownership.png'));o.update(image=saveimage(name+'-derived',im),x=sx+dx,y=sy+dy,width=im.width,height=im.height,bytes=im.width*im.height*4)
 records.append({'id':name,'source':'assets-src/gate25-station-planters/final-clean-ground.png','sourceRect':list(box),'translation':[dx,dy],'mask':name+'-ownership.png','policy':'Native crop expansion and architectural alpha; source RGB and facade world registration exact. No resize or RGB filters.'})
# Station: own architecture/attached roof gardens; discard only obsolete background.
o=obj('registration/station');original=Image.open(R/'public/assets/gate3/registration/station.png').convert('RGBA');aa=np.array(original);alpha=aa[:,:,3].copy();ret=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/station-background-retirement.png'))>0;alpha[ret]=0
# Rear railing begins localY30; the29px above central span is unrelated paving/trees.
alpha[0:30,160:459]=0
# Separate side background paving, retaining green hanging roof garden silhouette.
colour=aa[:,:,:3].astype(float);green=(colour[:,:,1]>colour[:,:,0]*.88)&(colour[:,:,1]>colour[:,:,2]*1.15)&(colour[:,:,1]>40);whitegold=(colour[:,:,0]>140)&(colour[:,:,1]>115)&(colour[:,:,2]<colour[:,:,1]*.9);leaf=binary_dilation(green,iterations=1)&(green|whitegold)
corner=Image.new('L',original.size);ImageDraw.Draw(corner).polygon([(0,0),(77,0),(77,11),(40,39),(0,109)],fill=255);alpha[(np.array(corner)>0)&~leaf]=0
alpha[(np.array(corner)>0)&leaf]=np.array(original)[:,:,3][(np.array(corner)>0)&leaf]
# Frame of original facade/roof stays untouched. Existing canonical floor owns retired bottom.
aa[:,:,3]=alpha;# Roof gardens follow the measured sloping terrace edge; trees behind it are background.
# Recovering whole connected green components pulled background trees into the sprite.
Y,X=np.indices(alpha.shape)
left=(X<160)&(Y>=np.where(X<88,140-X*1.5,np.where(X<135,18,35)))
right=(X>=459)&(X<570)&(Y>=18+(X-459)*1.1)
upper=(Y<40)
aa[:,:,3][upper]=0
keepLeaf=leaf&(left|right)&upper;aa[:,:,3][keepLeaf]=np.array(original)[:,:,3][keepLeaf]
# Original HVAC/rear railing are protected solid architecture, not color-keyed plants.
for bx,by,bw,bh in [(88,16,65,40),(480,24,70,44)]:aa[by:by+bh,bx:bx+bw]=np.array(original)[by:by+bh,bx:bx+bw]
aa[30:40,151:480]=np.array(original)[30:40,151:480]
out=Image.fromarray(aa);o.update(image=saveimage('station-derived',out));Image.fromarray(np.array(out)[:,:,3]).save(S/'station-owned-alpha-original-frame.png')
records.append({'id':'station','source':'public/assets/gate3/registration/station.png','sourceRGB':'EXACT','originalFrameWorld':[2313,2196,645,453],'expandedFrameWorld':[2313,2196,645,453],'sourceAnchorAndPivot':'UNCHANGED; original frame and architectural pixels remain fixed','canonicalFloor':'UNCHANGED','roofCore':'UNCHANGED / backdrop alpha retired only'})
# Main hall native front is reassembled at one support plane, stair/door axis measured from original.
a=Image.open(R/'public/assets/gate2/a/ground.png').convert('RGBA');front=Image.new('RGBA',(1010,140));front.paste(a.crop((870,0,1536,140)),(0,0));front.paste(a.crop((1145,0,1489,140)),(666,0));# Retire only contaminated side-plinth pixels; keep the complete central stair block.
# One native carved foundation course, not repeated stairs or stacked foundations.
flat=a.crop((1380,65,1440,100))
for x0,x1 in [(0,324),(500,1010)]:
 for xx in range(x0,x1,60):front.paste(flat.crop((0,0,min(60,x1-xx),35)),(xx,65))
 clear=Image.new('RGBA',(x1-x0,40));front.paste(clear,(x0,100))
front=Image.fromarray(np.roll(np.array(front),127,axis=1))
# Recover exactly the20px upper timber course, no resizing; original roof stays at protected registration.
upper=Image.fromarray(np.roll(np.array(Image.open(R/'public/assets/gate3/recovery-world/palace-upper-timber.png').convert('RGBA')),127,axis=1)).crop((0,40,1010,60));body=Image.new('RGBA',(1010,160));body.paste(upper,(0,0));body.paste(front,(0,20))
# Retire only old baked facade on derived ground; no second foundation.
paving=Image.open(R/'assets-src/gate3/reconciliation-v1/ceremonial-native-paving.png').convert('RGBA')
for x in range(1510,2520,430):g.paste(paving.crop((0,0,min(430,2520-x),140)),(x,650))
p['objects']=[o for o in p['objects']if o['id']not in ['recovery-world/palace-upper-timber','recovery-world/palace-right-continuation']]
roof=obj('recovery-world/palace-roof');roof['sortY']=684
# Authored doorway patch is applied only inside its tiny explicit portal mask.
if (S/'palace-door-authored.png').exists():
 edit=Image.open(S/'palace-door-authored.png').convert('RGBA');patch=edit.crop((1994-1280,592-120,2106-1280,686-120))
 p['objects'].append({'id':'alignment/palace-portal','image':saveimage('palace-portal',patch),'x':1992,'y':592,'width':112,'height':94,'sortY':685,'alphaSoftening':1,'bytes':112*94*4})
 # One native pixel owner per architectural layer; no async equal-depth tie.
 ba=np.array(body);ba[2:96,482:594,3]=0;body=Image.fromarray(ba)
 ri=Image.open(R/'public'/roof['image']).convert('RGBA');ra=np.array(ri);ra[592-roof['y']:min(686-roof['y'],ri.height),1992-roof['x']:2104-roof['x'],3]=0;roof['image']=saveimage('palace-roof-portal-derived',Image.fromarray(ra))
 # Last12px of roof eave remains original; door lies behind it, foreground depth is measured threshold.
p['objects'].append({'id':'alignment/palace-native-front','image':saveimage('palace-native-front',body),'x':1510,'y':590,'width':1010,'height':160,'sortY':683,'alphaSoftening':.35,'bytes':1010*160*4})
# Explicit palace entrance aperture, not a moved support reservation. Actual threshold685, landing750.
field[685:810,2014:2083]=255
# Measured archive door source(320,310) ->world(2580,923), native stairs to1020.
# Its20px front corridor is tight;17px foot-depth fits with3px total margin.
field[1020:1040,2259:2910]=255
field[923:1020,2544:2617]=255
records.append({'id':'palace-main-front','doorSourceCenterX':1281,'oldDoorWorldX':1921,'correctedDoorWorldX':2048,'nativeFacadePhaseTranslation':127,'thresholdWorld':[2048,685],'paintedPlinthBottom':750,'approvedSupport':[1510,290,1050,460],'doorAperture':[2014,677,69,133],'portalDerivedRect':[1992,592,112,94],'sourcePortalTranslation':[-2,0],'clearDoorOpening':[2010,600,76,85],'depthPolicy':'Facade683, roof684, portal685; Juni at threshold685 draws at685.1. No async equal-depth ties. Original roof remains exact outside112x18 portal/eave ownership exception, source PNG immutable. Stairs behind Juni on ascent; support/root unchanged.','originalSources':'IMMUTABLE','noHallWorldRelocation':True})
# Separate eastern native steps from the facade: static RGB stays identical,
# while Juni stands in front of the actual923 threshold rather than behind a407px poster.
archive=obj('production/archive');ai=Image.open(R/'public'/archive['image']).convert('RGBA')
# Only central walking steps become ground. Side lanterns/gardens retain foreground ownership.
stair=ai.crop((277,310,373,407));g.alpha_composite(stair,(archive['x']+277,archive['y']+310))
tail=ai.crop((0,310,601,407));ta=np.array(tail);ta[:,277:373,3]=0;tail=Image.fromarray(ta)
p['objects'].append({'id':'alignment/archive-front-details','image':saveimage('archive-front-details',tail),'x':archive['x'],'y':archive['y']+310,'width':601,'height':97,'sortY':1020,'alphaSoftening':1,'bytes':601*97*4})
archive.update(image=saveimage('archive-upper',ai.crop((0,0,601,310))),height=310,sortY=923,bytes=601*310*4)
records.append({'id':'archive-layer-ownership','nativeSource':'public/assets/gate3/production-assets/archive.png','upperSourceRect':[0,0,601,310],'stairsSourceRect':[0,310,601,407],'registration':'UNCHANGED / static sourceRGB exact','threshold':[2580,923],'sideClearance':'Reserve-to-wall150px; painted low-platform envelope reaches about2858, leaving52px. Roof edge2861 leaves46px to eave2907. These are distinct projections, not automatic footprint acceptance.','frontGroundClearance':20,'proposal':'Retain current artwork/geometry in main; secondary88px gate proposal requires approval; no relocation or wall change applied.'})
# The protected west pavilion roof projects over the royal hall's left background.
# Preserve that native silhouette as foreground; never erase it with the retired hall ground.
pav=a.crop((680,35,1110,185));pm=Image.new('L',pav.size);ImageDraw.Draw(pm).polygon([(7,91),(52,66),(74,20),(83,13),(94,20),(96,33),(136,44),(239,48),(278,34),(282,25),(289,24),(294,35),(294,46),(316,65),(335,78),(366,86),(366,95),(350,110),(332,131),(294,145),(197,149),(99,143),(32,125),(8,108)],fill=255);pav.putalpha(pm)
# Ground pixels below the opaque extracted roof are retired to the native court material.
pad=Image.new('RGBA',pav.size)
for ty in range(0,pad.height,paving.height):
 for tx in range(0,pad.width,paving.width):pad.paste(paving.crop((0,0,min(paving.width,pad.width-tx),min(paving.height,pad.height-ty))),(tx,ty))
g.paste(pad,(1320,685),pm);p['objects'].append({'id':'alignment/west-pavilion-roof','image':saveimage('west-pavilion-roof',pav),'x':1320,'y':685,'width':430,'height':150,'sortY':1040,'alphaSoftening':.35,'bytes':430*150*4});pm.save(S/'west-pavilion-roof-ownership.png')
records.append({'id':'west-pavilion-roof','source':'public/assets/gate2/a/ground.png','sourceRect':[680,35,430,150],'worldOrigin':[1320,685],'policy':'Native RGB/placement exact; roof foreground restored above derived royal hall, old ground copy retired. No historical building move.'})
# Exact bridge deck and mainland access surfaces, physically observed in native source.
physical=Image.new('L',(W,H));pd=ImageDraw.Draw(physical);deck=[(3055,3460),(3147,3460),(3188,3527),(3205,3545),(3250,3552),(3300,3562),(3350,3574),(3400,3587),(3450,3603),(3505,3617),(3515,3655),(3450,3648),(3400,3630),(3350,3615),(3300,3602),(3250,3591),(3205,3579),(3170,3568),(3143,3522),(3055,3522)];pd.polygon(deck,fill=255)
# This is local collision ownership over visible deck, not new bridge land/endpoints.
# The timber landing is part of the real surface, not the old broad mainland rectangle.
pd.rectangle((3035,3380,3150,3522),fill=255)
physical.save(S/'bridge-physical-deck.png');pa=np.array(physical)>0
from scipy.ndimage import binary_erosion
#49x17 conservative ground contact: exact physical deck eroded by footprint, no double erosion.
from scipy.ndimage import minimum_filter
XX=np.indices(pa.shape,sparse=True)[1]
physicalUnion=pa|((oldfield>0)&((XX<3035)|(XX>3480)))
# Native mooring-post base footprints, measured from original timber landing.
postFeet=[[3080,3430,11,4],[3080,3446,11,4],[3080,3465,12,4],[3080,3488,11,4],[3080,3514,11,4],[3150,3548,22,5],[3190,3574,24,5],[3306,3601,25,5],[3217,3551,8,4],[3255,3558,8,4],[3287,3565,8,4],[3324,3566,22,5]]
for px,py,pw,ph in postFeet:physicalUnion[py:py+ph,px:px+pw]=False
field[3380:3605,3035:3180]=0
field[pa]=255
# Native atlas contact points: lowest4 opaque rows, projected to original ground anchor.
atlas=rd('public/assets/juni/juni.json')['frames'];sheet=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');footprints={}
for action in ['walk','run']:
 for direction in ['front','back','left','right']:
  points=set()
  for name,fr in atlas.items():
   if not (name.startswith(action+'-'+direction+'-')or name.startswith('idle-'+direction+'-')):continue
   f=fr['frame'];al=np.array(sheet.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])))[:,:,3];ys,xs=np.where(al>0);bottom=int(ys.max());ys,xs=np.where((al>0)&(np.indices(al.shape)[0]>=bottom-3));points.update((int(x-48),int(y-bottom-1))for x,y in zip(xs,ys))
  footprints[action+'-'+direction]=sorted(points)
rect=[2980,3380,600,300];cx,cy,cw,ch=rect;physicalUnion[cy:cy+ch,cx:cx+cw].astype('uint8').tofile(O/'bridge-physical.bin');p['contactCollision']={'physical':'assets/gate3/aligned-world/bridge-physical.bin','rect':rect,'footprints':footprints}
wr(S/'native-foot-contact.json',{'method':'Original atlas96x112 anchor48,100; lowest4 opaque rows per frame, raised feet projected onto unchanged ground anchor. Union across gait and idle poses, per direction. Full sprite appearance and original animation remain unchanged. This is ground contact, not a full-body artistic/occlusion PASS.','spec':p['contactCollision']})
Image.fromarray(physicalUnion.astype('uint8')*255).save(S/'bridge-ground-union.png')
# Reclaim obsolete centre-point padding only on public station entrance floor.
field[2610:2700,2534:2658]=255
# Protected platform8px strip is NEVER cleared.
field[2626:2755,2950:2958]=oldfield[2626:2755,2950:2958]
# Bounded authorized bridge-abutment derived artwork, core bridge/source PNG unchanged.
bridgeEdits=[('bridge-mainland',[(3134,3478),(3191,3485),(3220,3541),(3225,3652),(3154,3652),(3125,3550)]),('bridge-island',[(3315,3548),(3400,3568),(3483,3598),(3497,3646),(3398,3665),(3315,3638)])]
if (S/'bridge-authored.png').exists():
 ed=Image.open(S/'bridge-authored.png').convert('RGBA')
 for name,poly in bridgeEdits:
  mask=Image.new('L',ed.size);ImageDraw.Draw(mask).polygon([(x-2816,y-3072)for x,y in poly],fill=255);g.paste(ed,(2816,3072),mask);mask.save(S/(name+'-repair-mask.png'));records.append({'id':name,'source':'bridge-authored.png','worldOrigin':[2816,3072],'mask':name+'-repair-mask.png','policy':'Authorized bounded derived abutment ownership; originalJeju PNG/internal architecture/paths immutable, endpoint registrations unchanged'})
# One bounded water family around the bridge source-frame seam. Land/basalt/foam
# context is semantically separated; canonical Jeju PNG and internal scenery stay immutable.
ed=Image.open(S/'bridge-authored.png').convert('RGBA');current=np.array(g.crop((2816,3072,4352,4096)));auth=np.array(ed);rr,gg,bb=[current[:,:,k].astype(float)for k in range(3)];ar,ag,ab=[auth[:,:,k].astype(float)for k in range(3)]
blue=(rr<bb*.65)&(gg>bb*.6)&(bb>70);foam=(rr>190)&(gg>rr*.95)&(bb>rr*.98);newBlue=(ar<ab*.65)&(ag>ab*.6)&(ab>70);newFoam=(ar>190)&(ag>ar*.95)&(ab>ar*.98)
landLabels,_=label(~(blue|foam));sizes=np.bincount(landLabels.ravel());protected=binary_dilation((landLabels>0)&(sizes[landLabels]>=24),iterations=3)
yy,xx=np.indices(blue.shape);wx=xx+2816;wy=yy+3072;bay=((wx-3240)/160)**2+((wy-3520)/215)**2<1
wm=bay&(blue|foam)&(newBlue|newFoam)&~protected;waterMask=Image.fromarray(wm.astype('uint8')*255);g.paste(ed,(2816,3072),waterMask);waterMask.save(S/'bridge-water-ownership.png')
records.append({'id':'bridge-water-continuity','source':'bridge-authored.png','worldOrigin':[2816,3072],'mask':'bridge-water-ownership.png','pixels':int(wm.sum()),'scope':'Bounded bridge bay only; original basalt/land components plus3px contact rim protected. No new rocks/trees, mirror donors, RGB interpolation, blur or image resampling. Canonical PNG unchanged.'})
# Centre-point routes must follow the visible timber/paving, not the old stone sea wall.
# Classification changes navigation ownership only; no RGB filtering or artwork recoloring.
from scipy.ndimage import binary_closing
pix=np.array(g);rgb=pix[:,:,:3].astype(float);r,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
floor=(r>100)&(gg>70)&(r>=gg*.99)&(r>bb*1.12);floor=binary_closing(floor,structure=np.ones((3,3),bool))
field[pa]=0;field[pa&(floor|(np.indices(pa.shape,sparse=True)[1]>=3205))]=255
for px,py,pw,ph in postFeet:field[py:py+ph,px:px+pw]=0
Image.fromarray((pa&floor).astype('uint8')*255).save(S/'bridge-centre-surface.png')
# Bounded canopy completion: existing canopy stays exact. No new platform connection.
if (S/'station-canopy-authored.png').exists():
 ed=Image.open(S/'station-canopy-authored.png').convert('RGBA');box=(2946,2244,3028,2518);patch=ed.crop((box[0]-1920,box[1]-1920,box[2]-1920,box[3]-1920));mask=Image.new('L',patch.size);ImageDraw.Draw(mask).polygon([(12,0),(28,18),(82,150),(82,255),(40,274),(12,170)],fill=255);arr=np.array(patch);rgb=arr[:,:,:3].astype(float);nativeMetal=(rgb[:,:,2]>=rgb[:,:,0]*.95)&(rgb[:,:,1]>=rgb[:,:,0]*.9);mm=(np.array(mask)>0)&nativeMetal;mm[:,:12]=False;mm[2390-box[1]:,:]=False
 from scipy.ndimage import label
 labs,_=label(mm);anch=np.unique(labs[:,12:17]);anch=anch[anch>0];mm&=np.isin(labs,anch);mask=Image.fromarray(mm.astype('uint8')*255);patch.putalpha(mask);p['objects'].append({'id':'alignment/canopy-terminal','image':saveimage('canopy-terminal',patch),'x':box[0],'y':box[1],'width':patch.width,'height':patch.height,'sortY':2649,'alphaSoftening':.65,'bytes':patch.width*patch.height*4});mask.save(S/'canopy-completion-mask.png');records.append({'id':'canopy-terminal','worldBox':list(box),'source':'station-canopy-authored.png','policy':'Native roof terminal/fascia cap cantilevered from original supports. Generated extra ground post rejected as outside protected support reservation; not installed. Original canopy/source and collision unchanged. No90x36 connector or platform transfer claim.'})
# Near bridge rails/posts must occlude Juni naturally; they cannot stay baked under her.
# Reassign existing native pixels, then retire their ground copies. No new props or RGB.
bx,by,bw,bh=3135,3490,220,180;bridgeSource=g.crop((bx,by,bx+bw,by+bh)).convert('RGBA');bs=np.array(bridgeSource);owned=np.zeros((bh,bw),bool);newBridgeObjects=[]
yy,xx=np.indices((bh,bw));wx=xx+bx;wy=yy+by;rgb=bs[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
for i,(x,y,w,h,root)in enumerate([(3144,3514,30,110,3553),(3186,3538,35,110,3579),(3303,3564,37,100,3606)]):
 roi=(wx>=x)&(wx<x+w)&(wy>=y)&(wy<y+h);gray=(abs(rr-gg)<22)&(abs(gg-bb)<30)&(rr<245)
 mask=roi&gray&~owned
 # Retain one connected physical stone support, not isolated mortar specks.
 labs,_=label(mask);sizes=np.bincount(labs.ravel());sizes[0]=0
 if len(sizes)>1:mask=labs==int(sizes.argmax())
 name='bridge-near-stone-'+str(i);im=bridgeSource.crop((x-bx,y-by,x-bx+w,y-by+h));ma=mask[y-by:y-by+h,x-bx:x-bx+w];im.putalpha(Image.fromarray(ma.astype('uint8')*255));newBridgeObjects.append({'id':'alignment/'+name,'image':saveimage(name,im),'x':x,'y':y,'width':w,'height':h,'sortY':root,'alphaSoftening':1,'bytes':w*h*4});Image.fromarray(ma.astype('uint8')*255).save(S/(name+'-ownership.png'));owned|=mask
nearBand=(wx>=3205)&(wx<=3320)&(wy>=3550+(wx-3205)*.225)&(wy<=3588+(wx-3205)*.225)
wood=(rr>55)&(rr<225)&(rr>gg*1.3)&(gg>bb*1.2);mask=nearBand&wood&~owned
im=bridgeSource.copy();im.putalpha(Image.fromarray(mask.astype('uint8')*255));newBridgeObjects.append({'id':'alignment/bridge-near-wood','image':saveimage('bridge-near-wood',im),'x':bx,'y':by,'width':bw,'height':bh,'sortY':3607,'alphaSoftening':1,'bytes':bw*bh*4});owned|=mask;Image.fromarray(mask.astype('uint8')*255).save(S/'bridge-near-wood-ownership.png')
# Retired source pixels are hidden by the exact, opaque original foreground pixels.
donor=bs[67:75,105:121];under=bs.copy();under[owned]=donor[yy[owned]%8,xx[owned]%16];g.paste(Image.fromarray(under),(bx,by));p['objects'].extend(newBridgeObjects)
proof=g.crop((bx,by,bx+bw,by+bh))
for ob in sorted(newBridgeObjects,key=lambda ob:ob['sortY']):proof.alpha_composite(Image.open(R/'public'/ob['image']),(ob['x']-bx,ob['y']-by))
assert np.array_equal(np.array(proof),bs),'Bridge static pixel ownership regression'
records.append({'id':'bridge-near-foreground','nativeSource':'Current corrected bridge pixels at unchanged world registration','sourceRect':[bx,by,bw,bh],'maskPixelCount':int(owned.sum()),'staticCompositeExact':True,'purpose':'Correct near-railing/post occlusion. Old baked copies retired; one pixel owner. No source recoloring or extra props.'})
# Continue the station drop-off asphalt to the actual avenue junction, not to its
# original illustration edge. Native original1254px source samples, no scaling/filter.
# Existing curb, lane marks, crosswalk and canonical forecourt/road stay exact.
from scipy.ndimage import binary_erosion
x,y,w,h=2130,2670,144,143;roadSource=Image.open(S/'asphalt-native-continuation.png').convert('RGBA');region=np.array(g.crop((x-3,y-3,x+w+3,y+h+3))).astype(float);r0,g0,b0=region[:,:,0],region[:,:,1],region[:,:,2]
road=(r0<110)&(g0<115)&(b0<125)&(abs(r0-g0)<20)&(b0>=r0*.9);road=binary_erosion(road,iterations=1)[3:3+h,3:3+w];rm=Image.fromarray(road.astype('uint8')*255);g.paste(roadSource,(x,y),rm);rm.save(S/'station-asphalt-continuation-mask.png')
records.append({'id':'station-asphalt-continuation','worldRect':[x,y,w,h],'source':'assets-src/gate2/originals/station.png','nativeSamples':[[850,1010,144,76],[870,1020,144,67]],'mask':'station-asphalt-continuation-mask.png','policy':'Only existing unprotected spur asphalt inside lane/curb edges. No source recolor, blur, resampling, repeating tile or road-geometry change. Canonical road/curb/crosswalk unchanged. Source softness remaining inside protected road is separate.'})
# Canonical station ground wins, unconditionally.
g.paste(old.crop((2274,2603,2958,2813)),(2274,2603));assert np.array_equal(np.array(g.crop((2274,2603,2958,2813))),np.array(old.crop((2274,2603,2958,2813))))
changed=[];fields=[]
for c in p['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];part=g.crop((x,y,x+w,y+h))
 if part.tobytes()!=old.crop((x,y,x+w,y+h)).tobytes():
  path=O/(c['id']+'.png');part.save(path);c.update(image=str(path.relative_to(R/'public')),sha256=sha(path));changed.append(c['id'])
 if not np.array_equal(field[y:y+h,x:x+w],oldfield[y:y+h,x:x+w]):
  path=O/(c['id']+'.bin');path.write_bytes(field[y:y+h,x:x+w].tobytes());c.update(mask=str(path.relative_to(R/'public')),maskSha256=sha(path));fields.append(c['id'])
frames={'palace-compound':[2020,720],'palace-entrance':[2048,685],'palace-east':[2720,925],'palace-route':[2048,990],'station-precinct':[2680,2480],'station-upper':[2598,2200],'station-front':[2598,2660],'station-right':[2960,2410],'retail-block':[1070,2250],'cafe-roof':[720,2100],'bookshop-roof':[1130,2120],'learning-roof':[1470,2090],'bridge-mainland':[3180,3550],'bridge-island':[3420,3600],'bridge-full':[3320,3570]}
entries={'palace-compound':[2048,1090],'palace-entrance':[2048,760],'palace-east':[2680,1080],'palace-route':[2048,1090],'station-precinct':[2598.5,2760],'station-upper':[2598.5,2760],'station-front':[2598.5,2760],'station-right':[2970,2680],'retail-block':[1128,2690],'cafe-roof':[717,2605],'bookshop-roof':[1128,2690],'learning-roof':[1470,2690],'bridge-mainland':[3130,3460],'bridge-island':[3500,3610],'bridge-full':[3130,3460]}
p['reviewEntries'].update(entries);p['nativeFrames'].update(frames)
# Initial candidate walkthrough spawns are valid public approaches; static native frames independent.
p['spawn']=[2048,1090];wr(O/'manifest.json',p);before=copy.deepcopy(m);before.update(id='aligned-before',reviewEntries=p['reviewEntries'],nativeFrames=p['nativeFrames']);wr(R/'public/assets/gate3/aligned-before/manifest.json',before)
over=g.copy()
for o in sorted(p['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
# Only reproducible guides/native semantic crops; no full-world replacement image.
for name,box in [('palace',(1280,120,2816,1144)),('station-canopy',(1920,1920,3456,2944)),('bridge',(2816,3072,4352,4096)),('retail',(320,1600,1856,2624))]:over.crop(box).save(S/(name+'-candidate-context.png'))
over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');p['overview']='assets/gate3/aligned-world/overview.png';wr(O/'manifest.json',p)
wr(S/'integration-provenance.json',{'baseline':'06b718a / reconciled-world','records':records,'groundChunksChanged':changed,'fieldChunksChanged':fields,'canonicalSources':'IMMUTABLE','planningFiles':'UNCHANGED','sevenReviewerImages':'NOT PROVIDED / requested','station8pxStrip':'UNCHANGED / CLOSED','bakery':'Required/unplaced; W0 rejected,Q1 unallocated','artAcceptance':'PENDING HUMAN / no technical self-approval'})
print('Aligned candidate:',len(changed),'ground chunks;',len(fields),'field chunks')
