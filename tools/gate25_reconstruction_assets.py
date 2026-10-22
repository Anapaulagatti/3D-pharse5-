"""One authored environment plane, protected architecture, separately owned complete foreground.
The full canvas is authoring data only; runtime has three independent nonoverlapping native textures.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import binary_closing,binary_fill_holes,binary_dilation,label,find_objects
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-reconstruction';P=R/'public/assets/gate2';O=P/'district-reconstruction';D=R/'docs/gate25-reconstruction';W,H=3184,1214
source=Image.open(S/'original-ground.png').convert('RGB');raw=Image.open(S/'ground-revised-host.png').convert('RGB');ground=raw.resize((W,H),Image.Resampling.NEAREST)
# Freeze actual host input; architectural mattes can then be refined without changing provenance.
for name in ['environment-authoring-guide.png','architecture-protection.png','architecture-envelopes.json']:
 v=S/(Path(name).stem+'-v1'+Path(name).suffix)
 if not v.exists():v.write_bytes((S/name).read_bytes())
polys=json.loads((S/'architecture-envelopes-v1.json').read_text())
for p in polys:
 if p['id']=='muneum-convenience':p['points']=[[1080,286],[1450,286],[1469,335],[1469,555],[1476,555],[1476,620],[1469,620],[1469,756],[1080,756]]
 if p['id']=='bakery':p['points']=[[min(x,2434) if y<539 or y>575 else x,y]for x,y in p['points']]
protected=Image.new('L',(W,H));pd=ImageDraw.Draw(protected)
for p in polys:pd.polygon([tuple(v)for v in p['points']],fill=255)
# Separate complete blue crates from the baked architectural plate, including their original foot shadow.
box=(1420,677,1495,771);rgb=np.array(source.crop(box));v=rgb.astype(float);blue=(v[:,:,2]>v[:,:,0]*1.4)&(v[:,:,2]>v[:,:,1]*1.08)&(v[:,:,2]>45)
silhouette=Image.new('L',(75,94));ImageDraw.Draw(silhouette).polygon([(14,3),(33,3),(34,14),(52,14),(57,21),(54,33),(57,39),(57,51),(56,73),(45,81),(14,78),(3,65),(3,49),(6,43),(5,25),(12,18)],fill=255)
blue=(v[:,:,2]>v[:,:,0]*1.9)&(v[:,:,2]>v[:,:,1]*1.2)&(v[:,:,2]>45)
core=binary_fill_holes(binary_closing(blue,iterations=1))&(np.array(silhouette)>0)
labs,n=label(core);sizes=np.bincount(labs.ravel());sizes[0]=0;core=labs==int(np.argmax(sizes))
a=np.zeros(core.shape,np.uint8);a[core]=255
# The nearby garbage bin and brown trunk are deliberately excluded from this complete-crate matte.
for yy in range(81,89):
 for xx in range(8,58):
  if v[yy,xx].mean()<100:a[yy,xx]=min(130,int(max(0,110-v[yy,xx].mean())*1.5))
rgba=np.dstack([rgb,a]);Image.fromarray(rgba).save(O/'crates.png');Image.fromarray(a).save(S/'crate-alpha.png')
pa=np.array(protected);part=pa[box[1]:box[3],box[0]:box[2]];part[a>0]=0;pa[box[1]:box[3],box[0]:box[2]]=part;protected=Image.fromarray(pa);protected.save(S/'architecture-protection-final.png');(S/'architecture-envelopes-final.json').write_text(json.dumps(polys,indent=2)+'\n')
ground.paste(source,(0,0),protected)
# Complete sidewalk bollards: independent foreground ownership and measured foot solids.
# Extracted from the newly authored environment, not pasted as rectangular scenery cards.
post_specs=[(61,779),(294,779),(520,781),(747,779),(1385,779),(1478,781),(1561,778),(1817,770),(2199,770),(2434,770),(2533,782),(2615,792),(2747,782),(2909,782),(3027,793),(3120,782)]
posts=[];feet=[];plate=np.array(ground).copy();clean=plate.copy()
for index,(cx,top) in enumerate(post_specs):
 left=cx-15;right=cx+32;bottom=821;rgb=plate[top:bottom,left:right].copy();luma=rgb.astype(float).mean(2)
 dark=luma<150
 labs,n=label(dark);seed_y=min(805-top,len(labs)-1);seed_x=15
 chosen=int(labs[seed_y,seed_x])
 if not chosen:
  candidates=labs[max(0,seed_y-3):seed_y+4,11:20];chosen=int(np.bincount(candidates.ravel())[1:].argmax()+1)
 core=binary_fill_holes(labs==chosen);core=binary_dilation(core,iterations=1)
 # Restrict the cast shadow to its pavement support, retaining the complete upright.
 upright=Image.new('L',(right-left,bottom-top));ud=ImageDraw.Draw(upright)
 ud.rounded_rectangle((8,0,23,813-top),radius=3,fill=255)
 shape=(np.array(upright)>0)|core
 shape[:max(0,807-top),25:]=False
 alpha=shape.astype('uint8')*255
 obj=Image.fromarray(np.dstack([rgb,alpha]));name=f'bollard-{index+1:02d}.png';obj.save(O/name)
 # Neighboring clean pavers at identical Y provide underpainting only beneath this owned alpha.
 replacement=plate[top:bottom,left+48:right+48].copy() if right+48<W else plate[top:bottom,left-48:right-48].copy()
 local=clean[top:bottom,left:right];local[shape]=replacement[shape]
 feet.append([cx-7,810,cx+9,824]);posts.append(dict(id=f'bollard-{index+1:02d}',image='district-reconstruction/'+name,x=left,y=top,width=right-left,height=bottom-top,sortY=818,alphaSoftening=1))
ground=Image.fromarray(clean);ground.save(S/'reconstructed-ground.png')
# Reassembly must reproduce the authored environment exactly before actual player occlusion.
assembled=ground.convert('RGBA')
for ob in posts:assembled.alpha_composite(Image.open(O/Path(ob['image']).name),(ob['x'],ob['y']))
assert np.array_equal(np.array(assembled.convert('RGB')),plate)
(S/'foreground-ownership.json').write_text(json.dumps(dict(bollards=posts,footSolids=feet,ownedAlphaReassemblyPixelExact=True,underpainting='same-Y neighboring clean pavers, only underneath extracted alpha',crates='original source RGB / complete blue silhouette / own contact shadow'),indent=2)+'\n')
# Three technical windows remain exactly at the confirmed runtime boundaries; no overlapping ownership.
old=json.loads((P/'district-polish/scene.json').read_text());scene=dict(old,id='district-reconstruction',label='Gate2.5 · environment reconstruction review',grounds=[],objects=[dict(id='complete-crates',image='district-reconstruction/crates.png',x=box[0],y=box[1],width=75,height=94,sortY=762,alphaSoftening=1)])
scene['objects']+=posts
for name,x,end in [('west',0,1512),('center',1512,2488),('east',2488,W)]:
 ground.crop((x,0,end,H)).save(O/(name+'.png'));scene['grounds'].append(dict(id=name,image='district-reconstruction/'+name+'.png',x=x,y=0,width=end-x,height=H))
# Geometry reconstructed from actual architectural envelopes and visible planted beds.
arch=np.array(protected)>0;block=binary_dilation(arch,iterations=8)
# Station threshold/plaza is exterior, below its ground-contact wall (source south edge677+8).
block[686:770,2556:3099]=False
new=np.array(raw.resize((W,H),Image.Resampling.NEAREST)).astype(float);green=(new[:,:,1]>new[:,:,0]*1.08)&(new[:,:,1]>new[:,:,2]*1.18)&(new[:,:,1]>48)&(~arch)
vegetation=binary_closing(green,iterations=3);labs,n=label(vegetation);rects=[]
for i,bb in enumerate(find_objects(labs),1):
 if bb is None:continue
 count=np.count_nonzero(labs[bb]==i)
 if count<110:continue
 y0,y1=bb[0].start,bb[0].stop;x0,x1=bb[1].start,bb[1].stop
 # Painted garden canopies remain inside conservative inaccessible garden reserves.
 if x1-x0>12 and y1-y0>8:
  rects.append([max(0,x0-10),max(0,y0-7),min(W,x1+10)-max(0,x0-10),min(H,y1+9)-max(0,y0-7)])
walk=Image.fromarray((~block).astype('uint8')*255);wd=ImageDraw.Draw(walk)
for x,y,w,h in rects:wd.rectangle((x,y,x+w,y+h),fill=0)
# Foreground collision describes the complete crates' actual foot support; no obsolete tree/bike/lamp solids.
wd.rectangle((1417,747,1499,774),fill=0)
for rect in feet:wd.rectangle(tuple(rect),fill=0)
wd.rectangle((0,0,W-1,7),fill=0);wd.rectangle((0,H-8,W-1,H-1),fill=0);wd.rectangle((0,0,7,H-1),fill=0);wd.rectangle((W-8,0,W-1,H-1),fill=0)
walk.save(O/'walk.png');scene['mask']='district-reconstruction/walk.png';scene['limitations']='Reconstructed environment review; approved architecture/entrances/native Juni and tour preserved. Independently loadable native chunks; human art review and physical-device acceptance pending.'
scene['routes']=[dict(id='frontages',points=[[1200,780],[1552,780],[1998,780],[2548,790],[2824,697]],width=24)]
(O/'scene.json').write_text(json.dumps(scene,indent=2,ensure_ascii=False)+'\n');(S/'collision-geometry.json').write_text(json.dumps(dict(architecturalProjection='protected polygons with8px clearance; station exterior threshold carve below wall south contact',gardenReserves=rects,foregroundFootprint=[1417,747,82,27]),indent=2)+'\n')
cat=json.loads((P/'catalog.json').read_text());cat=[c for c in cat if c['id']!='district-reconstruction'];
for c in cat:
 if c['id']=='district-polish':c['label']='HISTORY · REJECTED polish'
 if c['id']=='district':c['label']='HISTORY · technical district prototype'
cat.append(dict(id=scene['id'],label='CURRENT · reconstruction / review pending'));(P/'catalog.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
actual=np.array(ground);original=np.array(source);assert np.array_equal(actual[pa>0],original[pa>0]);assert scene['spawn']==old['spawn'] and scene['targets']==old['targets']
mat=np.array(walk);connected,num=label(mat>127);sx,sy=scene['spawn'];component=connected[sy,sx];assert component
for t in scene['targets']:assert connected[t['y'],t['x']]==component,t
proof=dict(protectedArchitecturalPixels=int((pa>0).sum()),protectedPixelsIdentical=True,originalFacadeSourceUnresampled=True,sourceFilesRetained=True,spawnAndEntranceCoordinatesUnchanged=True,technicalChunkEdges=[1512,2488],nativeRuntimeScale=1,groundChunkCount=3,foregroundObjects=len(scene['objects']),bollardOwnedAlphaReassemblyExact=True,noOverlappingGrounds=True,removedDerivedObjects=[o['id']for o in old['objects']],completeNewForeground='source-derived blue crates / independent alpha and owned contact shadow / ysort762',gardenReserves=len(rects),entrancesInSameWalkComponent=True,worldSize=[W,H])
(D/'source-and-collision.json').write_text(json.dumps(proof,indent=2)+'\n');ground.resize((1592,607)).save(S/'authoring-preview.png');print('PASS protected architecture /3 native windows / complete owned foreground /connected entrances')
