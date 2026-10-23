"""Limited candidate registration. Exact approved pixel extraction; no new production artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-corrections';O=R/'public/assets/gate3/registration';O.mkdir(parents=True,exist_ok=True)
plan=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());base=json.loads((R/'public/assets/gate3/world/manifest.json').read_text());W,H=base['size'];ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8)
for c in base['chunks']:
 x,y,w,h=[c[k] for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
source=Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGBA');envelopes=json.loads((R/'assets-src/gate25-reconstruction/architecture-envelopes-final.json').read_text());mask=Image.new('L',source.size);md=ImageDraw.Draw(mask)
for e in envelopes:md.polygon([tuple(p) for p in e['points']],fill=255)
# Source rectangles are conservative native architecture envelopes, not newly painted side elevations.
def spec(id,box,origin,entry,foot,reservation,status):return dict(id=id,sourceRect=box,rasterOrigin=origin,sourceEntry=entry,collision=foot,reservation=reservation,status=status)
items=[spec('cafe',[35,200,450,756],[510,2035],[242,770],[510,2380,415,210],'cafe','CANDIDATE: east visual/contact envelope25px beyond390px slot'),spec('bookshop',[450,235,780,756],[980,2070],[598,770],[980,2380,330,210],'books','CANDIDATE: shares existing books reservation with learning'),spec('learning',[780,195,1080,756],[1310,2030],[888,770],[1310,2380,300,210],'books','CANDIDATE: paired party wall retained; visual height61px above facade reserve'),spec('convenience',[1080,245,1501,757],[220,2608],[1288,770],[220,2910,421,210],None,'NEW CANDIDATE plot on Namsan approach;140px west of tower zone on unreserved mainland, no protected reservation invented'),spec('bakery',[1537,0,2442,763],[1353,3060],[1998,780],[1380,3370,875,442],None,'NEW CANDIDATE waterfront plot; requires explicit local path amendments; original442px collision depth retained'),spec('station',[2539,283,3184,736],[2313,2196],[2824,697],[2322.5,2380,555,210],'civic','Protected anchor/collision unchanged; candidate source pivot(.5,0), raster edge2238, explicit human approval required')]
# Source clean-ground has no new planter bodies: carry the approved objects and baked contact shadows separately.
objects=[dict(o) for o in base['objects']];targets=[];solids=[]
for s in items:
 x,y,x2,y2=s['sourceRect'];crop=source.crop((x,y,x2,y2));owned=mask
 if s['id']=='station':
  owned=Image.new('L',source.size);ImageDraw.Draw(owned).polygon([tuple(pt)for e in envelopes if e['id']=='station' for pt in e['points']],fill=255)
 alpha=owned.crop((x,y,x2,y2));crop.putalpha(alpha);a=np.array(crop);a[a[:,:,3]==0,:3]=0;crop=Image.fromarray(a);crop.save(O/(s['id']+'.png'),optimize=True)
 # Verify all owned architecture pixels against approved ground before any registration.
 valid=np.array(alpha)>0;assert np.array_equal(np.array(crop)[:,:,:3][valid],np.array(source.crop((x,y,x2,y2)))[:,:,:3][valid])
 xx,yy=s['rasterOrigin'];s['worldEntry']=[s['sourceEntry'][0]-x+xx,s['sourceEntry'][1]-y+yy]
 if s['id']=='station':
  s['worldEntry']=[2598.5,2610];s['protectedSourceAnchor']=[2238.5,2180];s['sourcePivot']=[.5,0];s['fullSourceRasterOrigin']=[2238,2180];s['phasePolicy']='Explicit candidate pixel-center anchor on X; not a rounded/mutated planning coordinate. Original source-edge interpretation remains historical; final human approval required.'
 s['image']=f'assets/gate3/registration/{s["id"]}.png';s['opaquePixels']=int(valid.sum());s['sourceSha256']=hashlib.sha256((R/'assets-src/gate25-station-planters/final-clean-ground.png').read_bytes()).hexdigest()
 ob=dict(id='registration/'+s['id'],image=s['image'],x=xx,y=yy,width=x2-x,height=y2-y,sortY=s['collision'][1]+s['collision'][3],alphaSoftening=1,bytes=(x2-x)*(y2-y)*4)
 if s['id']=='station':ob.update(sourceAnchor=[xx+.5,yy],sourcePivot=[.5,0])
 objects.append(ob)
 targets.append(dict(id=s['id'],x=s['worldEntry'][0],y=s['worldEntry'][1],label=s['id']+' · candidate registration'))
 solids.append(dict(id=s['id'],rect=s['collision']))
# The platform canopy has a distinct support plane; do not flatten it into the station facade root.
canopyMask=Image.new('L',source.size);ImageDraw.Draw(canopyMask).polygon([tuple(pt)for e in envelopes if e['id']=='station-platform-canopy' for pt in e['points']],fill=255)
bodyMask=Image.new('L',source.size);ImageDraw.Draw(bodyMask).polygon([tuple(pt)for e in envelopes if e['id']=='station' for pt in e['points']],fill=255)
owned=(np.array(canopyMask)>0)&(np.array(bodyMask)==0);box=(3110,300,3184,736);part=source.crop(box);a=np.array(part);a[:,:,3]=owned[300:736,3110:3184].astype('uint8')*255;a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(O/'station-platform-canopy.png',optimize=True)
objects.append(dict(id='registration/station-platform-canopy',image='assets/gate3/registration/station-platform-canopy.png',x=2884,y=2213,width=74,height=436,sortY=2649,alphaSoftening=.65,sourceAnchor=[2884.5,2213],sourcePivot=[.5,0],bytes=74*436*4))
# Engineering-only pedestrian proposals; no streetscape art production.
routes=[dict(id='retail-front',points=[[470,2690],[1820,2690],[2048,2690]],width=112),dict(id='convenience-access',points=[[760,3140],[428,3140],[428,3133]],width=80),dict(id='namsan-west-bypass',points=[[950,3280],[760,3140],[760,2920],[750,2800]],width=80),dict(id='avenue-diversion',points=[[2048,3260],[2048,3308],[1340,3308],[1340,3900]],width=60),dict(id='east-bakery-bridge-link',points=[[2048,3308],[2292,3308],[2292,3480],[3160,3480]],width=60),dict(id='east-bakery-coast-link',points=[[2292,3480],[2292,3812],[2310,3900]],width=60),dict(id='promenade-local-diversion',points=[[1280,3790],[1280,3900],[2310,3900],[2310,3790],[2900,3790]],width=96),dict(id='bakery-entry',points=[[1814,3900],[1814,3840]],width=64)]
g=ImageDraw.Draw(ground)
for path in routes:g.line([tuple(p) for p in path['points']],fill='#aaa69a',width=path['width'],joint='curve')
# Mark local candidate public realm explicitly. Keep old baseline geometry/source plan untouched.
for s in items:
 x,y,w,h=s['collision'];x0,y0,x1,y1=int(x),int(y),int(x+w),int(y+h)
 # Native visible torso clearance:25px radius conservatively contains the49px Juni silhouette.
 walk[max(0,y0-25):min(H,y1+26),max(0,x0-25):min(W,x1+26)]=0
# Open only the proposed connected public pedestrian routes outside approved/proposed solids.
pathmask=Image.new('L',(W,H));pd=ImageDraw.Draw(pathmask)
for p in routes:pd.line([tuple(pt) for pt in p['points']],fill=255,width=p['width']-50,joint='curve')
new=np.array(pathmask)>127;walk[new]=255
for s in items:
 x,y,w,h=s['collision'];walk[int(y)-25:int(y+h)+26,int(x)-25:int(x+w)+26]=0
# Retail door approaches outside ground-contact rectangles.
for s in items[:4]:
 x,y=s['worldEntry'];walk[int(y)-1:int(y)+100,int(x)-18:int(x)+19]=255
# The55px inter-building gap is a non-public service recess, not a claimed accessible alley.
walk[2380:2590,925:980]=0
# Station source forecourt: exact approved pavement, tactile strip and crosswalk with baked shadows.
dx,dy=-226,1913;box=(2500,690,3184,900);ground.paste(source.crop(box),(box[0]+dx,box[1]+dy))
stationWalk=Image.open(R/'public/assets/gate2/district-planter-repair/walk.png').convert('L');part=np.array(stationWalk.crop((2500,690,3184,900)));walk[2603:2813,2274:2958]=part
# Door centre remains at the exact protected logical2598.5; no rounding in analytic collision geometry.
for o in json.loads((R/'public/assets/gate2/district-planter-repair/scene.json').read_text())['objects']:
 if 'planter' in o['id']:
  ob=dict(o);ob.update(id='registration/'+o['id'],image='assets/gate2/'+o['image'],x=o['x']+dx,y=o['y']+dy,sortY=o['sortY']+dy,sourceAnchor=[o['x']+dx+.5,o['y']+dy],sourcePivot=[.5,0],bytes=o['width']*o['height']*4);objects.append(ob)
  # Preserve exact approved source foot-clearance around both bodies, not a decorative overlay.
# Bake changed engineering ground/mask chunks only; reuse all unchanged approved chunk files.
chunks=[]
for c in base['chunks']:
 c=c.copy();x,y,w,h=[c[k] for k in ['x','y','width','height']];tile=ground.crop((x,y,x+w,y+h));raw=walk[y:y+h,x:x+w].tobytes()
 old=Image.open(R/'public'/c['image']).convert('RGBA')
 if not np.array_equal(np.array(tile),np.array(old)) or raw!=(R/'public'/c['mask']).read_bytes():
  tile.save(O/(c['id']+'.png'),optimize=True);(O/(c['id']+'.bin')).write_bytes(raw);c['image']='assets/gate3/registration/'+c['id']+'.png';c['mask']='assets/gate3/registration/'+c['id']+'.bin';c['sha256']=hashlib.sha256((R/'public'/c['image']).read_bytes()).hexdigest();c['maskSha256']=hashlib.sha256(raw).hexdigest()
 chunks.append(c)
overview=ground.copy()
for o in sorted(objects,key=lambda o:o['sortY']):overview.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(int(o['x']),int(o['y'])))
overview.thumbnail((870,973),Image.Resampling.NEAREST);overview.save(O/'overview.png',optimize=True)
manifest=dict(base,id='registration',chunks=chunks,objects=objects,targets=targets,spawn=[2598.5,2760],overview='assets/gate3/registration/overview.png',logicalSolids=[{'id':'protected-station','rect':[2322.5,2380,555,210]}],stops=[],artStatus='LIMITED CANDIDATE / engineering circulation only / human approval required')
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Exact intersections are evidence, never invented protected reservations.
def intersect(a,b):
 x,y=max(a[0],b[0]),max(a[1],b[1]);r,bt=min(a[0]+a[2],b[0]+b[2]),min(a[1]+a[3],b[1]+b[3]);return [x,y,r-x,bt-y] if r>x and bt>y else None
conflicts=[]
for s in items:
 for b in plan['buildings']:
  if b['id']==s['reservation'] or (s['reservation']=='books' and b['id']=='books'):continue
  hit=intersect(s['collision'],b['rect'])
  if hit:conflicts.append(dict(building=s['id'],approvedBuilding=b['id'],overlap=hit))
assert not conflicts,conflicts
proposal=dict(status='CANDIDATE_ONLY / final human approval required',baseline='602476d359e9b485ff455062a8d4652932bd4eaa',size=[W,H],approvedPlanUnchanged=True,approvedDistrictUnchanged=True,buildings=items,connectingRoutes=routes,serviceRecess={'rect':[925,2380,55,210],'public':False,'widthPx':55,'nextArtWork':'Close exposed source party walls with source-preserving side elevations/service treatment after approval; do not pretend this is a premium public alley.'},protectedStructureIntersections=conflicts,bakerySite={'plot':[1380,3370,875,442],'zone':'waterfront','protectedReservation':False,'requiresPlanningAmendment':True,'conflictingExistingPaths':['urban-avenue','island-arrival','harbor-link','promenade','market-waterfront-shortcut'],'ferryTerminalAndBridgeUnchanged':True,'widthBetweenBakeryAndMarket':80,'widthBetweenBakeryAndFerry':75,'playerVisibleWidth':49,'maxVisibleSideClearanceAtMidline':[15.5,13]},station={'sourceAnchor':[2238.5,2180],'sourcePivot':[.5,0],'rasterOrigin':[2238,2180],'logicalCollider':[2322.5,2380,555,210],'threshold':[2598.5,2610],'rasterDeltaFromLegacySourceEdge':[-.5,0],'appliedToApprovedMasterplan':False,'maxRasterQuantizationDeltaX':.5,'forecourtPatch':{'sourceRect':[2500,690,3184,900],'logicalSourceAnchor':[2274.5,2603],'sourcePivot':[.5,0],'rasterOrigin':[2274,2603]},'explicitPolicy':'Preserve logical reference point; adopt pixel-center X anchor with half-pixel source pivot in CANDIDATE ONLY, never silently round coordinates.'},limitations=['Shared Muneum party walls retained, unpainted exposed sides are not production-ready modular elevations.','Cafe facade/contact width exceeds slot25px; native facade heights exceed500px reserves by21-61px; no approval implied.','Bakery waterfront site has no protected building overlap, but needs5 named path amendments and final circulation/art approval.','Convenience plot is unassigned, partly in SW park gateway zoning;140px beyond tower-zone west edge.','Source facade visual projections extend above contact footprints; depth/visual overlap with future attractions requires G3-B review.','Station visual canopy overlaps platform reservation; not operational railway gameplay.'])
(R/'assets-src/gate3/registration/proposal-v1.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n');(D/'registration-proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n')
print('Candidate registration:',len(items),'buildings;',sum('/registration/' in c['image'] for c in chunks),'localized ground/mask chunks. No protected structural overlap.')
