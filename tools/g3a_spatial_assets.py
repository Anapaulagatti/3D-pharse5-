"""Separate G3-A placement candidate. Original masterplan/art/manifests remain immutable."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-spatial-review';O=R/'public/assets/gate3/registration-refined';O.mkdir(parents=True,exist_ok=True)
plan=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());base=json.loads((R/'public/assets/gate3/world/manifest.json').read_text());old=json.loads((R/'public/assets/gate3/registration/manifest.json').read_text());proposal=json.loads((R/'assets-src/gate3/registration/proposal-v1.json').read_text());W,H=base['size'];ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8)
for c in base['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
# Explicit candidate-only land extension. It does NOT alter original plan or default world.
land=[460,3940,1120,908];ld=ImageDraw.Draw(ground);ld.rectangle((460,3940,1579,4847),fill='#59615e',outline='#c2a968',width=3);ld.text((480,3950),'CANDIDATE QUAY EXTENSION / HUMAN APPROVAL REQUIRED',fill='white');walk[3980:4848,460:1580]=0 # New parcel public access is reserved paths only, not empty walkable grass.
# Retain the same native building textures and protected station/canopy/planters.
objects=copy.deepcopy(old['objects']);items=copy.deepcopy(proposal['buildings']);movements={'bakery':(-830,930),'convenience':(-40,210)}
for s in items:
 if s['id']in movements:
  dx,dy=movements[s['id']];s['rasterOrigin']=[s['rasterOrigin'][0]+dx,s['rasterOrigin'][1]+dy];s['collision']=[s['collision'][0]+dx,s['collision'][1]+dy,*s['collision'][2:]];s['worldEntry']=[s['worldEntry'][0]+dx,s['worldEntry'][1]+dy];s['status']='NEW COMPARISON CANDIDATE / masterplan unchanged'
# Original1288 was a landmark/merchandise-window reference, not the glass-door centre.
maru=next(s for s in items if s['id']=='convenience');maru['sourceEntry']=[1226,770];maru['worldEntry']=[326,3343]
for o in objects:
 name=o['id'].removeprefix('registration/')
 if name in movements:
  dx,dy=movements[name];o['x']+=dx;o['y']+=dy;o['sortY']+=dy
# Replace only the old western scenic-loop segment in candidate engineering terrain.
# No approved source architecture, scene images or default routes are edited.
oldloop=[[950,3280],[540,3140],[500,2920],[750,2800]];erase=Image.new('L',(W,H));ImageDraw.Draw(erase).line([tuple(p)for p in oldloop],fill=255,width=100,joint='curve');ground.paste(Image.new('RGBA',(W,H),'#52635b'),(0,0),erase)
# Redraw other approved route intersections affected by that local geometry erasure.
g=ImageDraw.Draw(ground)
for path in plan['paths']:
 if path['id']=='tower-approach':continue
 # Only redraw paths locally, preserving all original source pixels elsewhere.
 local=Image.new('RGBA',(W,H));ImageDraw.Draw(local).line([tuple(p)for p in path['points']],fill='#8d8c7c',width=path['width'],joint='curve');local.putalpha(Image.fromarray(np.minimum(np.array(local.getchannel('A')),np.array(erase))));ground.alpha_composite(local)
# Candidate-only connectors. All major circulation routes remain byte-identical in the base plan.
routes=[p for p in proposal['connectingRoutes']if p['id']=='retail-front']+[
 {'id':'namsan-west-loop-amendment','points':[[950,3280],[700,3140],[700,2920],[750,2800]],'width':100},
 {'id':'maru-front-access','points':[[700,3140],[700,3380],[326,3380],[326,3343]],'width':80},
 {'id':'quay-east-access','points':[[1490,3790],[1490,4790],[984,4790]],'width':96},
 {'id':'bakery-front-entry','points':[[984,4790],[984,4770]],'width':64}]
pathmask=Image.new('L',(W,H));pd=ImageDraw.Draw(pathmask)
for p in routes:
 g.line([tuple(pt)for pt in p['points']],fill='#aaa69a',width=p['width'],joint='curve');pd.line([tuple(pt)for pt in p['points']],fill=255,width=p['width']-50,joint='curve')
# Never turn sea or protected plan solids into a shortcut.
allowed=Image.new('L',(W,H));ad=ImageDraw.Draw(allowed)
for x,y,w,h in plan['land']+[land]:ad.rectangle((x+25,y+25,x+w-26,y+h-26),fill=255)
new=(np.array(pathmask)>0)&(np.array(allowed)>0);walk[new]=255
for b in plan['buildings']:
 if b['id']=='market': # Only the new narrow Maru-front gap needs the25px candidate clearance guard.
  x,y,w,h=b['rect'];walk[max(0,y-25):min(H,y+h+26),max(0,x-25):min(W,x+w+26)]=0
for s in items:
 x,y,w,h=s['collision'];walk[max(0,int(y)-25):min(H,int(y+h)+26),max(0,int(x)-25):min(W,int(x+w)+26)]=0
for s in items[:4]:
 x,y=s['worldEntry'];walk[int(y)-1:int(y)+100,int(x)-18:int(x)+19]=255
walk[2380:2590,925:980]=0
# Identical protected station forecourt and foot field from existing candidate, not resampled.
source=Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGBA');ground.paste(source.crop((2500,690,3184,900)),(2274,2603));stationWalk=np.array(Image.open(R/'public/assets/gate2/district-planter-repair/walk.png').convert('L').crop((2500,690,3184,900)));walk[2603:2813,2274:2958]=stationWalk
chunks=[]
for original in base['chunks']:
 c=copy.deepcopy(original);x,y,w,h=[c[k]for k in ['x','y','width','height']];tile=ground.crop((x,y,x+w,y+h));raw=walk[y:y+h,x:x+w].tobytes()
 if not np.array_equal(np.array(tile),np.array(Image.open(R/'public'/c['image']).convert('RGBA')))or raw!=(R/'public'/c['mask']).read_bytes():
  tile.save(O/(c['id']+'.png'),optimize=True);(O/(c['id']+'.bin')).write_bytes(raw);c['image']='assets/gate3/registration-refined/'+c['id']+'.png';c['mask']='assets/gate3/registration-refined/'+c['id']+'.bin';c['sha256']=hashlib.sha256((R/'public'/c['image']).read_bytes()).hexdigest();c['maskSha256']=hashlib.sha256(raw).hexdigest()
 chunks.append(c)
overview=ground.copy()
for o in sorted(objects,key=lambda o:o['sortY']):overview.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(int(o['x']),int(o['y'])))
overview.thumbnail((870,973),Image.Resampling.NEAREST);overview.save(O/'overview.png',optimize=True)
manifest=dict(base,id='registration-refined',chunks=chunks,objects=objects,targets=[{'id':s['id'],'x':s['worldEntry'][0],'y':s['worldEntry'][1],'label':s['id']+' / comparison candidate'}for s in items],spawn=[984,4790],overview='assets/gate3/registration-refined/overview.png',logicalSolids=[{'id':s['id'],'rect':s['collision']}for s in items],stops=[],artStatus='CANDIDATE ONLY / no new artwork / explicit quay and western scenic-loop amendments',reviewEntries={'station':[2598.5,2760],'bakery':[984,4790],'retail':[1128,2690],'convenience':[326,3380],'quay':[1490,3890],'namsan':[700,3000]},nativeFrames={'station':[2598.5,2460],'bakery':[975,4400],'retail':[1128,2360],'convenience':[700,3100],'quay':[1390,4100],'namsan':[900,3020]})
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
proposal.update(status='COMPARISON ONLY / G3-A approval withheld',baseline='46c6d2d',buildings=items,connectingRoutes=routes,bakerySite={'plot':[550,4300,875,442],'nativeEnvelope':[523,3990,905,763],'threshold':[984,4770],'candidateLandExtension':land,'extensionAreaPx':land[2]*land[3],'approvedPlanChanged':False,'majorRoutesDiverted':[],'newAccessLengthPx':1526,'newAccessWalkSeconds':1526/60,'limitation':'Requires explicit land/quay allocation; long new access and quay composition not accepted. If rejected, leave bakery unallocated rather than force waterfront diversion.'},maruSite={'plot':[180,3120,421,210],'nativeEnvelope':[180,2818,421,512],'threshold':[326,3343],'previousLandmarkReference':[388,3343],'entryCorrection':'Existing source door clear opening inspected at crop-localx112..180; door-centre x146 replaces old landmarkx208. Source pixels and original proposal unchanged.','doorOpeningCropLocal':[112,395,68,117],'doorVisibleWidthPx':68,'JuniVisibleWidthPx':49,'nominalDoorSideClearancePx':9.5,'shoreGapWestPx':20,'westSidePublicAccess':False,'eastLoopCentreX':700,'eastGapToNativeEnvelopePx':99,'localAmendment':'Only western tower-approach loop via7003140/7002920 replaces5403140/5002920. Existing100px scenic width retained; main Namsan destination and eastern approach unchanged.'},limitations=['All candidate land, zoning and local path amendments require explicit approval.','Bakery alternative avoids all existing route corridors but adds a large quay allocation and25.43s entrance spur; pacing and artistic composition unresolved.','Maru west20px margin is non-public. East80/100px access preserves public circulation; scenic-loop amendment remains pending.','Cafe25px width and retail visual-height easements unchanged.','Station/platform canopy projection remains unresolved; protected station geometry and pixels unchanged.'])
(R/'assets-src/gate3/registration/proposal-v2-comparison.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n');(D/'proposal-v2-comparison.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n')
# Remove only unreferenced newly generated technical files in this new variant folder.
keep={'manifest.json','overview.png'}|{Path(c[k]).name for c in chunks for k in ['image','mask']if '/registration-refined/' in c[k]}
for path in O.iterdir():
 if path.is_file()and path.name not in keep:path.unlink()
print('Generated separate comparison candidate:',sum('registration-refined' in c['image']for c in chunks),'technical chunks; no source textures or approved plans changed')
