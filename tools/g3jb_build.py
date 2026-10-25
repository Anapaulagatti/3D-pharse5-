"""Two localized structural paintings, native masks and collision matching visible deck."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib,numpy as np
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/jeju-bridges-v1';D=R/'docs/gate3-jeju-bridges';O=R/'public/assets/gate3/jeju-bridges-world'
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((S/'baseline-lock.json').read_text());m=copy.deepcopy(lock['manifest']);W,H=m['size'];scope=Image.open(S/'edit-scope-mask.png');allow=np.array(scope)>0;g=Image.new('RGBA',(W,H));f=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
bg=g.copy();bf=f.copy();src=Image.open(S/'bridges-authored.png').convert('RGBA');assert src.size==(1536,1024);
wide=Image.open(S/'wide-landing-authored.png').convert('RGBA');full=src.copy();full.paste(wide.crop((0,0,1536,540)),(0,0));src=full
# Keep canonical shared ocean wherever BOTH source and new painting are water.
# Only6px native structural contact rim is newly painted; no blue rectangular
# canvas replacement around the southern bridge. All pixels remain integer RGB.
from scipy.ndimage import binary_dilation
oldpix=np.array(bg.crop((2816,3200,4352,4224)));newpix=np.array(src)
def water(a):
 r,g,b=[a[:,:,i].astype(float)for i in range(3)];return(b>r*1.22)&(g>r*1.15)&(b>65)
both=water(oldpix)&water(newpix);rim=binary_dilation(~both,iterations=6);keep=both&~rim;newpix[keep]=oldpix[keep]
# Local upper seam: original CANONICAL nearshore native texels translated64px
# west across only the obsolete x3180 source edge. Preserve rocks/foam and every
# structural pixel. No image averaging, blur, stretch, repeat tile or recoloring.
yy,xx=np.indices(both.shape);donor=np.zeros_like(oldpix);donor[:,:-64]=oldpix[:,64:];guard=binary_dilation(~water(oldpix),iterations=3)
seam=both&water(donor)&~guard&(xx>=334)&(xx<=380)&(yy>=120)&(yy<295)
newpix[seam]=donor[seam];Image.fromarray(seam.astype('uint8')*255).save(S/'upper-native-water-seam-mask.png');src=Image.fromarray(newpix);src.save(S/'combined-native-authoring.png');g.paste(src,(2816,3200),scope.crop((2816,3200,4352,4224)))
# All old bridge-only foregrounds were physically replaced inside the declared mask.
retired=[];objects=[]
for ob in m['objects']:
 if not ob['id'].startswith('alignment/bridge-'):objects.append(ob);continue
 im=Image.open(R/'public'/ob['image']).convert('RGBA');a=np.array(im.getchannel('A'));x,y=ob['x'],ob['y'];inside=allow[y:y+im.height,x:x+im.width];outside=(a>0)&~inside
 if outside.any():
  a[inside]=0;im.putalpha(Image.fromarray(a));p=O/(ob['id'].split('/')[-1]+'-outside.png');im.save(p);ob=copy.deepcopy(ob);ob['image']=str(p.relative_to(R/'public'));objects.append(ob)
 retired.append(ob['id'])
m['objects']=objects
# Fine traced deck-top polygons, excluding all rail/post bases. These are visible
# floor only: no support extends onto open water, vertical pier faces or foliage.
floors={'A':[(3010,3435),(3042,3425),(3180,3443),(3180,3470),(3202,3498),(3250,3527),(3350,3555),(3450,3592),(3535,3635),(3560,3640),(3560,3685),(3500,3670),(3400,3635),(3300,3605),(3200,3578),(3110,3528),(3040,3510),(3010,3500)],'B':[(3010,3900),(3060,3910),(3155,3970),(3210,3988),(3310,4000),(3400,4018),(3495,4044),(3595,4043),(3600,4084),(3510,4088),(3400,4072),(3300,4052),(3200,4037),(3130,4010),(3050,3970),(3010,3950)]}
phys=np.array(Image.open(S/'before-walkable.png'))>0
q=lock['manifest']['contactCollision'];ox,oy,ww,hh=q['rect'];old=np.fromfile(R/'public'/q['physical'],np.uint8).reshape(hh,ww)>0;phys[oy:oy+hh,ox:ox+ww]=old
# Final surface is the TOP PLANE. The first broad envelope included vertical
# pier faces and is rejected. Projected rail/post shafts may occlude floor behind
# them; they are not a floor silhouette or an invisible water expansion.
floors={'A':[(3010,3435),(3042,3425),(3180,3443),(3180,3470),(3202,3498),(3250,3518),(3350,3548),(3450,3584),(3535,3629),(3560,3640),(3560,3668),(3500,3647),(3400,3613),(3300,3583),(3200,3553),(3130,3518),(3040,3505),(3010,3500)],'B':[(3010,3900),(3060,3910),(3155,3960),(3210,3980),(3310,3995),(3400,4012),(3495,4030),(3595,4043),(3600,4077),(3510,4066),(3400,4048),(3300,4032),(3200,4018),(3130,3995),(3050,3960),(3010,3950)]}
floor=np.zeros((H,W),bool)
for key,poly in floors.items():
 plane=Image.new('L',(W,H));ImageDraw.Draw(plane).polygon(poly,fill=255);pa=(np.array(plane)>0)&allow;Image.fromarray(pa.astype('uint8')*255).save(S/(key+'-visible-deck-mask.png'));floor|=pa
Image.fromarray(floor.astype('uint8')*255).save(S/'traced-material-floor.png');phys[allow]=floor[allow]
points=json.loads((R/'assets-src/gate3/residual-v1/bridge-clearance-proposal.json').read_text())['contactOffsets'];valid=np.ones((H,W),bool)
for dx,dy in points:
 shifted=np.zeros((H,W),bool);x1=max(0,-dx);x2=min(W,W-dx);y1=max(0,-dy);y2=min(H,H-dy);shifted[y1:y2,x1:x2]=phys[y1+dy:y2+dy,x1+dx:x2+dx];valid&=shifted
from scipy.ndimage import binary_erosion
valid=binary_erosion(valid,structure=np.ones((3,3),bool)) #1px floor/round phase safety
# Only bridge ownership is changed. Conservative centre mask guarantees every
# original idle/stop/turn/run contact fits without changing animation or controls.
f[allow]=valid[allow]*255
Image.fromarray(phys.astype('uint8')*255).save(S/'visible-physical-support.png');Image.fromarray(valid.astype('uint8')*255).save(S/'all-pose-supported-centres.png');np.asarray(phys[oy:oy+hh,ox:ox+ww],np.uint8).tofile(O/'bridge-a-physical.bin');m['contactCollision']=copy.deepcopy(q);m['contactCollision']['physical']=str((O/'bridge-a-physical.bin').relative_to(R/'public'))
changed=[];fields=[]
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];im=g.crop((x,y,x+w,y+h))
 if im.tobytes()!=bg.crop((x,y,x+w,y+h)).tobytes():p=O/(c['id']+'.png');im.save(p);c['image']=str(p.relative_to(R/'public'));c['sha256']=sha(p);changed.append(c['id'])
 if not np.array_equal(f[y:y+h,x:x+w],bf[y:y+h,x:x+w]):p=O/(c['id']+'.bin');p.write_bytes(f[y:y+h,x:x+w].tobytes());c['mask']=str(p.relative_to(R/'public'));fields.append(c['id'])
frame=json.loads((R/'public/assets/gate3/jeju-bridges-before/manifest.json').read_text());m.update(id='jeju-bridges-world',artStatus='Hanbit ART APPROVED LOCKED / TWO JEJU CROSSINGS REVIEW',nativeFrames=frame['nativeFrames'],reviewEntries=frame['reviewEntries']);over=g.copy()
for ob in sorted(m['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
over.save('/tmp/g3jb-after-world.png');over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');m['overview']=str((O/'overview.png').relative_to(R/'public'));wr(O/'manifest.json',m)
wr(S/'integration-provenance.json',{'baseline':lock['HEAD'],'source':'combined-native-authoring.png','origin':[2816,3200],'sourceScale':'EXACT1:1 / no resampling','scope':'edit-scope-mask.png','nativeTopPlanePolygons':floors,'actualPhysicalSurface':'traced-material-floor.png / manually traced native TOP PLANE and timber, excluding vertical pier faces. Raised railing shafts have separate foreground ownership; they are not ground-plane holes.','fractionalNativeSafety':'1px conservative centre padding handles floor-vs-round phase without changing original Juni movement','retiredOldBridgeForegrounds':retired,'groundChunks':changed,'collisionChunks':fields,'nativeAllPoseUnionOffsets':points,'Hanbit':'APPROVED LOCKED / all objects/source/registration unchanged','landBoundaries':'No new island/mainland land. Only existing crossing deck/abutment over-water structural support. Endpoints/logical plans unchanged.','humanArtAcceptance':'PENDING'})
print('Affected ground chunks',changed,'collision',fields)
# Diagnostic local connectivity only; actual original controls remain mandatory.
from scipy.ndimage import label
labs,_=label((f>0)[3300:4170,2950:3640]);
for key,a,b in [('A',(3010,3460),(3530,3640)),('B',(3100,3930),(3540,4070))]:print(key,'all-pose centres component',labs[a[1]-3300,a[0]-2950],labs[b[1]-3300,b[0]-2950])
