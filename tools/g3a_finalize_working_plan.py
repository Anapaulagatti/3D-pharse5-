"""Versioned accepted planning amendments + one isolated native platform ownership candidate.
Never rewrites historical plans, approved art, canonical floor or existing manifests.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-controlled-finalization';S=R/'assets-src/gate3/station-platform-resolution';O=R/'public/assets/gate3/registration-working-v3'
for p in [D,S,O]:p.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def digest(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
basePlan=read('assets-src/gate25/world-plan-v1.json');plan=copy.deepcopy(basePlan);prior=read('assets-src/gate3/registration/proposal-v2-comparison.json');accepted=read('public/assets/gate3/registration-review/manifest.json');base=read('public/assets/gate3/world/manifest.json');W,H=base['size']
plan['stage']='G3-A WORKING V3 / accepted amendments only; final registration review pending'
plan['reviewState']['revision']='G3-A working version3 / controlled finalization; final acceptance pending'
plan['reviewState']['gate3']='G3-A_FINAL_REVIEW_PENDING / G3-B_BLOCKED'
next(b for b in plan['buildings']if b['id']=='cafe')['rect']=[510,2380,415,210]
plan['buildings'].append({'id':'convenience','label':'Maru convenience store','rect':[180,3120,421,210],'entry':[326,3343],'kind':'modern','approval':'HUMAN_APPROVED_LOCATION_AND_APPROACH'})
tower=next(p for p in plan['paths']if p['id']=='tower-approach');assert tower['points'][:4]==[[2048,3260],[1800,3260],[1460,3260],[950,3280]]
tower['points']=tower['points'][:4]+[[700,3140],[700,2920],[750,2800]]
plan['paths'].append({'id':'maru-front-access','kind':'local','width':80,'points':[[700,3140],[700,3380],[326,3380],[326,3343]]})
plan['publicExclusions']=[{'id':'maru-west-shore-gap','rect':[160,2818,20,512],'public':False},{'id':'retail-service-recess','rect':[925,2380,55,210],'public':False}]
plan['registrationEasements']=[{'id':'cafe','contact':[510,2380,415,210],'visualEnvelope':[510,2035,415,556],'eastContactEasementPx':25,'northSouthProjection':[55,1],'transitionProjectionPx':45,'status':'CONDITIONAL_APPROVAL / heritage and circulation checks required'},{'id':'bookshop','contact':[980,2380,330,210],'visualEnvelope':[980,2070,330,521],'northSouthProjection':[20,1],'transitionProjectionPx':10,'status':'CONDITIONAL_APPROVAL / heritage and circulation checks required'},{'id':'learning','contact':[1310,2380,300,210],'visualEnvelope':[1310,2030,300,561],'northSouthProjection':[60,1],'transitionProjectionPx':50,'status':'CONDITIONAL_APPROVAL / heritage and circulation checks required'}]
plan['contentAllocations']=[{'id':'bakery','label':'오월제과 Bakery','requiredWorldContent':True,'artAsset':'assets/gate3/registration/bakery.png','nativeSize':[905,763],'assetSha256':digest('public/assets/gate3/registration/bakery.png'),'allocation':'DEFERRED / no production coordinates allocated','W0':'RETIRED_AS_PRODUCTION_LOCATION','Q1':'CANDIDATE_ONLY / land not allocated','candidateRecord':'assets-src/gate3/registration/proposal-v2-comparison.json','checkpointRequirement':'At waterfront production planning present a coherent quay destination: public-space purpose, landscape composition, useful return circulation and measured pacing. No repeated exhaustive unchanged-plan site search.'}]
# Keep old facade reserve rectangles as immutable reservation references; native easements are explicit above.
plan['workingAmendment']={'version':3,'authority':'docs/current/G3A_SPATIAL_DECISION.md','historicalBase':'assets-src/gate25/world-plan-v1.json','historicalBaseSha256':digest('assets-src/gate25/world-plan-v1.json'),'finalG3A':'PENDING','G3B':'BLOCKED','stationGroundRegistry':'assets-src/gate3/approved-station-forecourt.json','noNewLandAllocated':True}
registrations=[copy.deepcopy(b)for b in prior['buildings']if b['id']!='bakery']
for b in registrations:b['status']='PROTECTED_STATION_REGISTRATION'if b['id']=='station'else'HUMAN_APPROVED_MARU'if b['id']=='convenience'else'CONDITIONALLY_APPROVED_RETAIL'
working={'version':'G3-A WORKING V3','status':'Final registration acceptance pending; G3-B blocked','plan':plan,'registrations':registrations,'stationEngineeringCandidate':{'status':'PROPOSED_OWNERSHIP_DETAIL / local station-platform production BLOCKED pending transfer decision','platformReservationUnchanged':[2920,2350,100,400],'reportedProjectionOverlap':[2920,2350,38,299],'remainingTransferConflict':{'worldMaskEdge':[2950,2626,8,129],'sourceMaskEdge':[3176,713,8,129],'maskSource':'public/assets/gate2/district-planter-repair/walk.png','status':'INHERITED_BLOCKED / approved collision preserved','decisionRequired':'Authorize a separately bounded collision-ownership opening in this legacy source-edge guard, excluding all real supports/tree/planters, or explicitly allocate a connector around the edge. No such change is applied.'},'detail':'Separate native overhead, ground, support/sign and garden ownership; replace only conflicting railing end inside platform with a native end post outside reservation. Independent support colliders do not replace or move protected station collider.'}}
write(R/'assets-src/gate3/production-plan-v3-working.json',working)
def patch(a,b,path=''):
 out=[]
 if isinstance(a,dict)and isinstance(b,dict):
  for k in a.keys()-b.keys():out.append({'op':'remove','path':path+'/'+k})
  for k in b.keys()-a.keys():out.append({'op':'add','path':path+'/'+k,'value':b[k]})
  for k in a.keys()&b.keys():out+=patch(a[k],b[k],path+'/'+k)
 elif isinstance(a,list)and isinstance(b,list):
  for i in range(min(len(a),len(b))):out+=patch(a[i],b[i],path+'/'+str(i))
  for i in range(len(a)-1,len(b)-1,-1):out.append({'op':'remove','path':path+'/'+str(i)})
  for i in range(len(a),len(b)):out.append({'op':'add','path':path+'/'+str(i),'value':b[i]})
 elif a!=b:out.append({'op':'replace','path':path,'before':a,'value':b})
 return out
write(D/'plan-diff.json',{'base':'assets-src/gate25/world-plan-v1.json','baseSha256':digest('assets-src/gate25/world-plan-v1.json'),'result':'assets-src/gate3/production-plan-v3-working.json#/plan','operations':sorted(patch(basePlan,plan),key=lambda x:x['path'])})
# Native canopy ownership. Source remains immutable. Only a local railing opening is detailed.
src=Image.open(R/'public/assets/gate3/registration/station-platform-canopy.png').convert('RGBA');a=np.array(src);h,w=a.shape[:2];yy,xx=np.indices((h,w));opaque=a[:,:,3]>0
# Exact review mask: remove crossbars/posts in the platform's western38px; retain green foliage.
green=(a[:,:,1].astype(int)>a[:,:,2].astype(int)*1.25)&(a[:,:,1].astype(int)>a[:,:,0].astype(int)*.9)
opening=opaque&(xx>=36)&(yy>=282)&(yy<=315)&~green
# Native paver underpaint only at the removed rail pixels. Integer source translations, no resizing.
material=np.array(Image.open(R/'assets-src/gate25-reconstruction/original-ground.png').convert('RGBA'))
Image.fromarray(material).crop((2848,741,2894,762)).save(S/'native-paver-reference.png')
localFloor=np.zeros_like(a)
for y,x in zip(*np.where(opening)):
 dx=2848+(x-36)%46;dy=741+(y-282)%21;localFloor[y,x]=material[dy,dx];localFloor[y,x,3]=255
# End the railing with an existing full native metal post, moved only within this derived detail.
finished=a.copy();finished[opening]=0
post=a[282:316,61:68].copy();finished[282:316,29:36]=post
# Ground landing is owned below the player, not sorted as one tall solid canopy rectangle.
support=np.zeros((h,w),bool);support[170:184,45:56]=True
sign=np.zeros((h,w),bool);sign[183:204,31:61]=True;sign[204:284,41:56]=True
support &= opaque;sign &=opaque;sign &=~support
landing=opaque&(yy>=173)&(yy<284)&~support&~sign
roof=opaque&(yy<173)&~support&~sign&~landing
greenFinished=(finished[:,:,1].astype(int)>finished[:,:,2].astype(int)*1.25)&(finished[:,:,1].astype(int)>finished[:,:,0].astype(int)*.9)
fence=(finished[:,:,3]>0)&(yy>=282)&(yy<=315)&~greenFinished
for owner in [roof,support,sign,landing]:owner[fence]=False
garden=(finished[:,:,3]>0)&~roof&~support&~sign&~landing&~fence
# Railing opening startsy282; ensure removed pixels don't survive in any owned layer.
for owner in [roof,support,sign,landing,garden,fence]:owner[opening]=False
objects=[];ownerRecords=[]
def obj(name,pixels,root,soft=1):
 inds=np.where(pixels[:,:,3]>0)
 if not len(inds[0]):return
 x,y,x2,y2=int(inds[1].min()),int(inds[0].min()),int(inds[1].max())+1,int(inds[0].max())+1
 im=Image.fromarray(pixels).crop((x,y,x2,y2));path=O/(name+'.png');im.save(path,optimize=True)
 origin=[2884+x,2213+y];objects.append({'id':'station-platform/'+name,'image':str(path.relative_to(R/'public')),'x':origin[0],'y':origin[1],'width':x2-x,'height':y2-y,'sortY':root,'alphaSoftening':soft,'sourceAnchor':[origin[0]+.5,origin[1]],'sourcePivot':[.5,0],'bytes':(x2-x)*(y2-y)*4});ownerRecords.append({'id':name,'cropWithinOriginal':[x,y,x2,y2],'rasterOrigin':origin,'root':root,'pixels':int(len(inds[0]))})
for name,m,root,soft in [('roof-overhead',roof,2398,.65),('canopy-support',support,2398,1),('sign-and-post',sign,2495,1),('landing-ground',landing,-90,1),('retained-railing-and-end-post',fence,2530,1),('garden-context',garden,2649,.65)]:
 pixels=finished.copy();pixels[~m]=0;obj(name,pixels,root,soft);Image.fromarray(m.astype('uint8')*255).save(S/(name+'-mask.png'))
obj('railing-opening-native-ground',localFloor,-89,1)
# A small native paving connector remains strictly inside the unchanged platform reservation.
plate=np.zeros((36,90,4),np.uint8)
for py in range(36):
 for px in range(90):
  if px<10 and py>30:continue
  plate[py,px]=material[741+py%21,2848+px%46];plate[py,px,3]=255
platePath=O/'platform-opening-connector.png';Image.fromarray(plate).save(platePath,optimize=True)
objects.append({'id':'station-platform/opening-connector','image':str(platePath.relative_to(R/'public')),'x':2920,'y':2495,'width':90,'height':36,'sortY':-91,'alphaSoftening':1,'sourceAnchor':[2920.5,2495],'sourcePivot':[.5,0],'bytes':90*36*4})
Image.fromarray(opening.astype('uint8')*255).save(S/'railing-opening-mask.png');Image.fromarray(finished).save(S/'derived-ownership-preview.png')
# Physical support bases: independent ownership, station collider untouched. Third base is outside platform.
supports=[{'id':'platform-canopy-support-base','rect':[2929,2389,11,9]},{'id':'platform-sign-pole-base','rect':[2928,2489,11,6]},{'id':'platform-railing-end-base','rect':[2913,2524,7,6]}]
write(S/'ownership.json',{'source':'public/assets/gate3/registration/station-platform-canopy.png','sourceSha256':digest('public/assets/gate3/registration/station-platform-canopy.png'),'sourceRasterOrigin':[2884,2213],'sourcePivot':[.5,0],'nativeResampling':'NONE','owners':ownerRecords,'groundSupportBases':supports,'railingDetail':{'openingMask':'railing-opening-mask.png','nativePavingSource':'assets-src/gate25-reconstruction/original-ground.png','nativePavingSourceSha256':digest('assets-src/gate25-reconstruction/original-ground.png'),'nativePavingDonor':[2848,741,46,21],'nativeEndPostDonor':[61,282,7,34],'nativeEndPostDestination':[29,282],'platformConnector':[2920,2495,90,36],'scope':'Local platform-side context only, above canonical forecourt; no original source writes'},'status':'RESOLUTION_CANDIDATE / human native visual review required'})
# Fresh working runtime derives from immutable approved foundation; no Q1 land or W0 diversions.
ground=Image.new('RGBA',(W,H));walk=np.zeros((H,W),np.uint8);acceptedWalk=np.zeros((H,W),np.uint8)
for c in base['chunks']:
 x,y,cw,ch=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));walk[y:y+ch,x:x+cw]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(ch,cw)
for c in accepted['chunks']:
 x,y,cw,ch=[c[k]for k in ['x','y','width','height']];acceptedWalk[y:y+ch,x:x+cw]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(ch,cw)
oldLoop=[[950,3280],[540,3140],[500,2920],[750,2800]];erase=Image.new('L',(W,H));ImageDraw.Draw(erase).line([tuple(p)for p in oldLoop],fill=255,width=100,joint='curve');ground.paste(Image.new('RGBA',(W,H),'#52635b'),(0,0),erase)
for p in plan['paths']:
 local=Image.new('RGBA',(W,H));ImageDraw.Draw(local).line([tuple(pt)for pt in p['points']],fill='#8d8c7c',width=p['width'],joint='curve')
 if p['id']=='tower-approach':
  changedLoop=erase.copy();ImageDraw.Draw(changedLoop).line([tuple(pt)for pt in p['points'][3:]],fill=255,width=p['width'],joint='curve');local.putalpha(Image.fromarray(np.minimum(np.array(local.getchannel('A')),np.array(changedLoop))))
 elif p['id']!='maru-front-access':local.putalpha(Image.fromarray(np.minimum(np.array(local.getchannel('A')),np.array(erase))))
 ground.alpha_composite(local)
for s in registrations:
 x,y,cw,ch=s['collision'];walk[max(0,int(y)-25):min(H,int(y+ch)+26),max(0,int(x)-25):min(W,int(x+cw)+26)]=0
for s in registrations[:4]:
 x,y=s['worldEntry'];walk[int(y)-1:int(y)+100,int(x)-18:int(x)+19]=255
for r in plan['publicExclusions']:
 x,y,cw,ch=r['rect'];walk[y:y+ch,x:x+cw]=0
# Reuse exact approved station collision field and restored paving. Never recompose accepted floor.
walk[2196:2813,2274:2958]=acceptedWalk[2196:2813,2274:2958]
floor=Image.open(R/'assets-src/gate3/forecourt-restoration/restored-ground.png').convert('RGBA');ground.paste(floor,(2274,2603))
for ac in accepted['chunks']:
 if '/registration-forecourt/' in ac['image']:ground.paste(Image.open(R/'public'/ac['image']),(ac['x'],ac['y']))
for s in supports:
 x,y,cw,ch=s['rect'];walk[y-25:y+ch+26,x-25:x+cw+26]=0
assert np.array_equal(walk[2603:2813,2274:2958],acceptedWalk[2603:2813,2274:2958])
# No bakery sprite, solid, target, land or spur allocated. Intended content remains explicitly deferred in plan.
obs=[copy.deepcopy(o)for o in accepted['objects']if o['id']not in ['registration/bakery','registration/station-platform-canopy']]+objects
chunks=[]
for c in base['chunks']:
 c=copy.deepcopy(c);x,y,cw,ch=[c[k]for k in ['x','y','width','height']];tile=ground.crop((x,y,x+cw,y+ch));raw=walk[y:y+ch,x:x+cw].tobytes()
 # Reuse the exact canonical station image chunks when identical, never generate duplicate replacements.
 ac=next(z for z in accepted['chunks']if z['id']==c['id'])
 if np.array_equal(np.array(tile),np.array(Image.open(R/'public'/ac['image']).convert('RGBA'))):c['image']=ac['image'];c['sha256']=ac['sha256']
 elif not np.array_equal(np.array(tile),np.array(Image.open(R/'public'/c['image']).convert('RGBA'))):
  tile.save(O/(c['id']+'.png'),optimize=True);c['image']=str((O/(c['id']+'.png')).relative_to(R/'public'));c['sha256']=digest('public/'+c['image'])
 if raw!=(R/'public'/c['mask']).read_bytes():
  path=O/(c['id']+'.bin');path.write_bytes(raw);c['mask']=str(path.relative_to(R/'public'));c['maskSha256']=hashlib.sha256(raw).hexdigest()
 chunks.append(c)
manifest=copy.deepcopy(base);manifest.update(id='registration-working-v3',chunks=chunks,objects=obs,targets=[{'id':s['id'],'x':s['worldEntry'][0],'y':s['worldEntry'][1],'label':s['id']+' / '+s['status']}for s in registrations],spawn=[2598.5,2760],logicalSolids=[{'id':s['id'],'rect':s['collision']}for s in registrations]+supports,stops=[],artStatus='G3-A WORKING V3 / Maru approved, retail conditional, bakery deferred, station-platform detail proposed; final acceptance pending',reviewEntries={'station':[2598.5,2760],'platform':[2980,2690],'convenience':[326,3380],'retail':[1128,2690],'namsan':[700,3000],'waterfront':[1440,3740]},nativeFrames={'station':[2598.5,2460],'platform':[2970,2450],'retail':[1128,2360],'convenience':[700,3100],'namsan':[900,3020],'waterfront':[1700,3750]},workingPlan='assets-src/gate3/production-plan-v3-working.json',deferredContent=plan['contentAllocations'])
overview=ground.copy()
for o in sorted(obs,key=lambda v:v['sortY']):overview.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
overview.thumbnail((870,973),Image.Resampling.NEAREST);overview.save(O/'overview.png',optimize=True);manifest['overview']=str((O/'overview.png').relative_to(R/'public'))
write(O/'manifest.json',manifest)
write(D/'generation.json',{'scope':'Only accepted planning amendments and one local station-platform engineering detail; G3-B blocked','newGroundChunks':sum('/registration-working-v3/'in c['image']for c in chunks),'newMaskChunks':sum('/registration-working-v3/'in c['mask']for c in chunks),'canonicalGroundChunks':[c['image']for c in chunks if'/registration-forecourt/'in c['image']],'bakeryInActiveObjects':False,'bakeryContentStillRequired':True,'landEqualsHistorical':plan['land']==basePlan['land'],'protectedForecourtMaskExact':True,'nativeOwnershipDetail':'assets-src/gate3/station-platform-resolution/ownership.json'})
sourceKeep={'ownership.json','railing-opening-mask.png','derived-ownership-preview.png','native-paver-reference.png'}|{r['id']+'-mask.png'for r in ownerRecords}
for f in S.iterdir():
 if f.is_file()and f.name not in sourceKeep:f.unlink()
keep={'manifest.json','overview.png'}|{Path(c[k]).name for c in chunks for k in ['image','mask']if'/registration-working-v3/'in c[k]}|{Path(o['image']).name for o in obs if'/registration-working-v3/'in o['image']}
for f in O.iterdir():
 if f.is_file()and f.name not in keep:f.unlink()
print('Working V3 built; bakery deferred, no land expansion; canonical floor untouched; platform ownership candidate isolated')
