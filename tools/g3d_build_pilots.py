"""Versioned three-pilot ownership compositor. Native copies only, no art resampling.
Approved sources, production manifest/chunks and original masterplans are read-only.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/recovery';D=R/'docs/gate3-recovery';O=R/'public/assets/gate3/recovery-pilots';O.mkdir(exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('public/assets/gate3/production/manifest.json');base=read('public/assets/gate3/registration-working-v3/manifest.json');W,H=m['size'];ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8);basewalk=walk.copy()
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
for c in base['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];basewalk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
oldground=ground.copy();oldwalk=walk.copy();records=[];objects=copy.deepcopy(m['objects']);remove=[]
# A: native clean plate behind independently sorted original archive/workshop candidates.
a=Image.open(S/'north-ground-authored.png').convert('RGBA')
a.save(S/'north-ground-derived.png',optimize=True)
# Clear architecture beneath independently sorted approved storefronts; retain authored public street pixels.
b=Image.open(S/'south-authored.png').convert('RGBA');bclean=Image.open(S/'south-ground-clean-authored.png').convert('RGBA');bmask=Image.new('L',b.size);bd=ImageDraw.Draw(bmask)
for box0 in [(94,75,508,630),(509,75,563,630),(564,110,893,630),(894,70,1193,630)]:bd.rectangle(box0,fill=255)
b.paste(bclean,(0,0),bmask);bmask.save(S/'south-architecture-underpaint-mask.png',optimize=True);b.save(S/'south-ground-derived.png',optimize=True)
# Remove partial Maru/market guide imagery only; original sprites remain separate and unchanged.
c=Image.open(S/'namsan-ground-authored.png').convert('RGBA');cclean=Image.open(S/'namsan-ground-clean-authored.png').convert('RGBA');cmask=Image.new('L',c.size);cd=ImageDraw.Draw(cmask);cd.rectangle((0,345,186,867),fill=255);cd.rectangle((135,785,859,1023),fill=255);c.paste(cclean,(0,0),cmask);cmask.save(S/'namsan-architecture-underpaint-mask.png',optimize=True);c.save(S/'namsan-ground-derived.png',optimize=True)
tower_source=Image.open(S/'namsan-authored-v3.png').convert('RGBA');poly=[(858,93),(864,112),(864,159),(880,164),(880,188),(868,191),(880,241),(902,248),(902,270),(918,280),(929,313),(931,350),(921,374),(895,391),(897,489),(941,502),(944,621),(967,633),(982,649),(990,666),(987,682),(967,697),(944,707),(944,760),(790,760),(790,707),(758,700),(731,689),(711,676),(708,659),(724,644),(755,632),(757,505),(813,489),(817,391),(791,382),(781,355),(781,320),(787,290),(804,279),(800,267),(814,247),(838,237),(845,192),(831,187),(831,164),(850,159),(851,112)]
mask=Image.new('L',tower_source.size);ImageDraw.Draw(mask).polygon(poly,fill=255);mask.save(S/'tower-ownership-mask.png',optimize=True)
# Shorten only the NEW candidate antenna rod by30 native pixels, without scaling.
# Move its tiny tip93..122 down30, clear vacated top; preserves root and avoids approved retail facade.
tower_source.putalpha(mask);tip=tower_source.crop((848,93,869,123));tower_source.paste((0,0,0,0),(848,93,869,153));tower_source.alpha_composite(tip,(848,123));mask=tower_source.getchannel('A');box=mask.getbbox();tower=tower_source.crop(box);tower.save(O/'tower-native.png',optimize=True)
# Source root(858,766) -> unchanged logical tower centre/root(1200,3240), integer translation only.
tx,ty=1200-858+box[0],3240-766+box[1];newtower={'id':'recovery/tower','image':'assets/gate3/recovery-pilots/tower-native.png','x':tx,'y':ty,'width':tower.width,'height':tower.height,'sortY':3240,'alphaSoftening':.65,'bytes':tower.width*tower.height*4}
regions=[('north',a,(1536,576),(2176,650,3072,1600)),('south',b,(416,1960),(416,1960,1952,2760)),('namsan',c,(416,2470),(416,2760,1952,3340))]
edit=np.zeros((H,W),bool)
for name,plate,(x,y),boxworld in regions:
 assert plate.size==(1536,1024),name
 mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((boxworld[0],boxworld[1],boxworld[2]-1,boxworld[3]-1),fill=255)
 # Preserve complete approved historical/Jeju ground and canonical station floor even outside normal pilot extents.
 md=ImageDraw.Draw(mask)
 for bx,by,bw,bh in [(640,650,1536,1024),(3180,3200,1024,1536),(2274,2603,684,210)]:md.rectangle((bx,by,bx+bw-1,by+bh-1),fill=0)
 localmask=mask.crop((x,y,x+1536,y+1024));localmask.save(S/(name+'-edit-mask.png'),optimize=True);ground.paste(plate,(x,y),localmask);edit|=np.array(mask)>0
 records.append({'pilot':name,'worldOrigin':[x,y],'source':str((S/(name+'-ground-derived.png'if name=='north'else 'south-ground-derived.png'if name=='south'else'namsan-ground-derived.png')).relative_to(R)),'ownershipMask':str((S/(name+'-edit-mask.png')).relative_to(R)),'ownedPixels':int(np.count_nonzero(np.array(localmask))),'resampling':'NONE','otherRegionsRemainRejected':True})
# Remove giant rejected trees only if their complete ground roots lie in pilot-owned regions.
for o in list(objects):
 if o['id']in ['production/tower','production/palace']:remove.append(o['id']);objects.remove(o);continue
 if o['id'].startswith('production/tree-'):
  rootx=o['x']+o['width']//2;rooty=o['sortY']
  if any(o['x']<box[2] and o['x']+o['width']>box[0] and o['y']<box[3] and o['y']+o['height']>box[1] for box in [(2176,650,3072,1600),(416,1960,1952,2760),(416,2760,1952,3340)]):
   objects.remove(o);remove.append(o['id']);walk[rooty-8:rooty+10,rootx-13:rootx+14]=basewalk[rooty-8:rooty+10,rootx-13:rootx+14]
objects.append(newtower)
# Native55px service-side treatment recovered from the authored pilot; independent foreground, no baked duplicate.
service=Image.open(S/'south-authored.png').convert('RGBA').crop((509,75,564,631));service.save(O/'service-side-native.png',optimize=True);objects.append({'id':'recovery/service-side','image':'assets/gate3/recovery-pilots/service-side-native.png','x':925,'y':2035,'width':55,'height':556,'sortY':2591,'alphaSoftening':.65,'bytes':55*556*4});walk[2380:2590,925:980]=0

# Two approved189x196 trees are reused at native scale in non-route hill planting pockets.
added_tree_feet=[]
for i,(rootx,rooty)in enumerate([(1600,2980),(1750,3100)]):
 image='assets/gate2/b/prop-heritage-tree.png';im=Image.open(R/'public'/image);tw,th=im.size
 objects.append({'id':f'recovery/native-tree-{i}','image':image,'x':rootx-tw//2,'y':rooty-th+6,'width':tw,'height':th,'sortY':rooty,'alphaSoftening':.65,'bytes':tw*th*4})
 walk[rooty-6:rooty+8,rootx-11:rootx+12]=0;added_tree_feet.append([rootx-11,rooty-6,23,14])
# Pilot-only public approach ownership: remove inherited placeholder margins OUTSIDE fixed building footprints.
# Does not touch protected historic A, station floor/strip, main routes or approved solid rectangles.
approach_repairs=[{'id':'archive-step-approach','rect':[2508,1020,104,90],'reason':'Old placeholder blocks until1082,62px beyond fixed archive root1020; clear only104px stair approach to1110 public path.'},{'id':'tower-step-approach','rect':[1160,3240,80,20],'reason':'Old placeholder blocks until3257,17px beyond fixed tower root3240; clear existing80px threshold approach.'}]
for repair in approach_repairs:
 x,y,w,h=repair['rect'];walk[y:y+h,x:x+w]=255

# Pixels beneath the approved opaque store sprites do not replace approved art; their original files/coordinates are unchanged.
# Deliberately no station strip change, no new physical land, no new tower collision footprint.
for x,y,source in [(640,650,R/'public/assets/gate2/a/ground.png'),(3180,3200,R/'public/assets/gate2/c/ground.png'),(2274,2603,R/'assets-src/gate3/forecourt-restoration/restored-ground.png')]:
 im=Image.open(source).convert('RGBA');assert ground.crop((x,y,x+im.width,y+im.height)).tobytes()==im.tobytes()
chunks=[];changed=[]
for orig in m['chunks']:
 c0=copy.deepcopy(orig);x,y,w,h=[c0[k]for k in ['x','y','width','height']];before=oldground.crop((x,y,x+w,y+h));after=ground.crop((x,y,x+w,y+h));wm=walk[y:y+h,x:x+w]
 if after.tobytes()!=before.tobytes():
  out=O/(c0['id']+'.png');after.save(out,optimize=True);c0['image']=str(out.relative_to(R/'public'));c0['sha256']=sha(out);changed.append(c0['id'])
 if not np.array_equal(wm,oldwalk[y:y+h,x:x+w]):
  out=O/(c0['id']+'.bin');out.write_bytes(wm.tobytes());c0['mask']=str(out.relative_to(R/'public'));c0['maskSha256']=sha(out)
 chunks.append(c0)
review=copy.deepcopy(m);review.update(id='recovery-pilots',chunks=chunks,objects=objects,artStatus='THREE REPRESENTATIVE PILOTS ONLY / HUMAN APPROVAL PENDING / rest of world remains rejected',reviewEntries={'north':[2280,1110],'south':[1128,2690],'namsan':[1200,3260],'station':[2598.5,2760],'north-occlusion':[2560,1110],'south-occlusion':[1128,2250],'namsan-occlusion':[1200,2800]},nativeFrames={'north':[2306,1100],'south':[1184,2410],'namsan':[1184,2940],'station':[2598.5,2460],'north-occlusion':[2306,1100],'south-occlusion':[1184,2410],'namsan-occlusion':[1184,2940]},spawn=[1128,2690]);review['stops']=[{'id':name,'label':label,'x':x,'y':y,'zoom':.5,'travelMs':1800,'holdMs':2300}for name,label,x,y in [('north','A · historical garden pilot',2306,1100),('south','B · modern street pilot',1184,2410),('namsan','C · Namsan material pilot',1184,2940)]]
over=ground.copy()
for ob in sorted(objects,key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png',optimize=True);review['overview']='assets/gate3/recovery-pilots/overview.png';write(O/'manifest.json',review)
write(S/'integration-provenance.json',{'generator':'tools/g3d_build_pilots.py','onlyThreePilotRegions':True,'fullWorldPropagation':False,'canonicalFloorExact':True,'historicalGroundExact':True,'jejuGroundExact':True,'approvedObjectSourcesAndCoordinates':'UNCHANGED','nativeScale':1,'resampling':'NONE','regions':records,'architectureUnderpaintOwnership':{'north':'Entire cleanplate behind independent archive/culture; approved A exact mask wins.','south':'south-architecture-underpaint-mask.png clears only original storefront envelopes; native55px service strip separately sorted at925,2035, root2591, source crop[509,75,55,556].','namsan':'namsan-architecture-underpaint-mask.png clears partial Maru/market guide imagery; original sprites/pivots retained.','resampling':'NONE'},'changedChunks':changed,'reusedChunks':[c['id']for c in chunks if c['id']not in changed],'removedRejectedObjects':remove,'newTower':newtower,'newCandidateAntennaAssembly':'Tip translated down30px;30px rod removed at native1x, no resampling. Approved retail facade envelope ends2591; candidate antenna begins2597.', 'towerSourceCrop':list(box),'towerSourceRoot':[858,766],'fixedWorldRoot':[1200,3240],'doorClearOpeningSource':[814,552,79,105],'towerGroundOwnership':'Original240x240 building foot retained; extraction excludes outer garden planters. Native stair/plinth projection reviewed separately from fixed collision, no physical expansion.','palace':'Two new continuation authoring trials REJECTED internally; not installed. Rejected duplicate-plinth foreground omitted in review only; incomplete upper compound remains outside pilot A owned area, not presented as repaired.','collisionChanges':{'pilotOwnershipRepairs':approach_repairs,'removedRejectedTreeFeetAndTwoApprovedTreeFeet':True,'addedTreeFeet':added_tree_feet,'serviceRecess':[925,2380,55,210],'serviceRecessPolicy':'Explicitly accepted non-public service recess; no public route allocation.','changedPixelCount':int(np.count_nonzero(walk!=oldwalk)),'protectedStationStrip':'UNCHANGED / CLOSED','newTowerCollision':'Fixed240x240 building foot unchanged; only17px inherited margin outside root cleared in80px public approach. Body clearance remains separate.','masterplanChange':False}})
print('Built pilots:',len(changed),'new ground chunks;',len(objects),'foregrounds;',len(remove),'rejected objects removed locally')
