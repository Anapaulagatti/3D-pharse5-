"""Five-task acceptance data only. Existing art/masterplan/entrance are read-only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,shutil,subprocess,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate2/acceptance';P=R/'public/assets/gate2';D=R/'docs/gate2/acceptance';C=R/'.cache/gate2/acceptance';C.mkdir(parents=True,exist_ok=True)
write=lambda p,o:p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
logs=[]
def command(*args):
 r=subprocess.run(list(map(str,args)),cwd=R,capture_output=True,text=True);logs.append(dict(command=list(map(str,args)),exit=r.returncode,stdout=r.stdout,stderr=r.stderr));write(S/'processing.json',logs);assert r.returncode==0,(r.stdout,r.stderr)
F=Path('/workspace/tooling-cache/agent-sprite-forge/skills')
if not (S/'original-native.png').exists():
 command('python3',F/'generate2dmap/scripts/conform_background.py','conform','--input',S/'original-host.png','--size','1024x1024','--mode','cover','--resampler','box','--strict','--output-dir',C/'original-conform')
 command('python3',F/'generate2dsprite/scripts/palette_tool.py','build','--input',C/'original-conform/background.png','--colors','255','--name','Owol-Bakery','--output-dir',C/'original-palette')
 command('python3',F/'generate2dsprite/scripts/palette_tool.py','apply','--input',C/'original-conform/background.png','--palette',C/'original-palette/palette.json','--alpha-threshold','128','--output-dir',C/'original-pixels')
 shutil.copy2(C/'original-pixels/background.png',S/'original-native.png')
folder=P/'original';folder.mkdir(exist_ok=True);shutil.copy2(S/'original-native.png',folder/'ground.png')
def mask(size,areas,paths,solids):
 im=Image.new('L',size);d=ImageDraw.Draw(im)
 for x,y,w,h in areas:d.rectangle((x,y,x+w,y+h),fill=255)
 for pts,width in paths:
  d.line([tuple(p)for p in pts],fill=255,width=width,joint='curve')
  for x,y in pts:d.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255)
 for x,y,w,h in solids:d.rectangle((x,y,x+w,y+h),fill=0)
 return im.filter(ImageFilter.MinFilter(17))
original=dict(id='original',label='Original · 오월제과 bakery',size=[1024,1024],spawn=[510,790],camera=[510,550],ground='original/ground.png',mask='original/walk.png',objects=[],targets=[dict(id='bakery',x=510,y=780,label='오월제과 · bakery entrance'),dict(id='crossing',x=510,y=965,label='Bakery crossing')],routes=[dict(id='entrance',points=[[510,965],[510,780]],width=78)],walkAreas=[[20,760,984,72],[20,947,984,64]],solids=[dict(rect=[76,310,875,442],reason='Original bakery lower elevation / ground contact')],provenance='One new host-image source, not a Muneum facade reuse; uniform1254→1024 authoring finish; no existing artwork modified')
mask((1024,1024),original['walkAreas'],[([[510,780],[510,965]],100)],[s['rect']for s in original['solids']]).save(folder/'walk.png');write(folder/'scene.json',original)
# Exact station fit: retain south contact y410; move only conservative north limit from190 to200.
folder=P/'station';station=json.loads((folder/'scene.json').read_text());station['solids'][0]['rect']=[84,200,555,210];station['solids'][0]['reason']='Refined collision excludes10px of upper facade projection; same south ground contact, approved art unchanged';station['footprintFit']=[555,210];station['targets']=[dict(id='station',x=360,y=430,label='한빛역 · entrance threshold'),dict(id='forecourt',x=360,y=520,label='Station entrance plaza')]
mask(tuple(station['size']),station['walkAreas'],[(r['points'],r['width'])for r in station['routes']],[s['rect']for s in station['solids']]).save(folder/'walk.png');write(folder/'scene.json',station)
# Independent approved Muneum/station join; no new art generation.
subprocess.run(['python3',str(R/'tools/gate2_small_join.py')],cwd=R,check=True)
seam=json.loads((P/'seam/scene.json').read_text())
# Separate localized world-fit candidate; approved Gate1 JSON is NEVER written.
plan=json.loads((R/'assets-src/world-gate1/plan.json').read_text());candidate=json.loads(json.dumps(plan));candidate['size']=[4352,4864];candidate['stage']='GATE2_LOCALIZED_FIT_CANDIDATE_NOT_APPROVED_MASTERPLAN';candidate['land'][1]=[3280,3240,910,1380];candidate['land'][4]=[3150,3956,180,128];candidate['seaLinks'][0]['points']=[[2560,4100],[3180,4020]]
for node in candidate['accessNodes']:
 if node['id']=='jeju-landing':node['point']=[3180,4020]
candidate['gate2LocalizedFit']=dict(nativeFrame=[3180,3200,1024,1536],bridgeConnector=[[3160,3480],[3180,3480],[3180,3560],[3200,3560]],nativeIslandReservationIncludesWater=True,stationCollisionWorld=[2322.5,2380,555,210],stationSourceOrigin=[2238.5,2180],stationThresholdWorld=[2598.5,2610],ferryGameplay=False,approval='CANDIDATE_ONLY',shoreline='Foot-clearance mask rejects sea; opaque image bounds are not shoreline.')
# Replace only Jeju-specific planning paths/features with native artwork registration.
c=json.loads((P/'c/scene.json').read_text())
candidate['paths']=[v for v in candidate['paths']if not v['id'].startswith('jeju-')]+[dict(id='jeju-native-'+r['id'],kind='scenic',width=r['width'],points=[[x+3180,y+3200]for x,y in r['points']])for r in c['routes']]+[dict(id='jeju-gate2-bridge-connector',kind='local',width=50,points=[[3160,3480],[3180,3480],[3180,3560],[3200,3560]])]
for b in candidate['buildings']:
 if b['id']=='jeju-culture':b['rect']=[3400,4160,390,210];b['entry']=[3590,4390]
for f in candidate['features']:
 if f['id']in ['oreum','basalt','orchard','jeju-culture']:
  r={'oreum':[400,40,540,560],'basalt':[120,450,380,320],'orchard':[600,760,340,260],'jeju-culture':[220,900,440,420]}[f['id']];f['rect']=[r[0]+3180,r[1]+3200,r[2],r[3]]
for z in candidate['zones']:
 if z['id']=='island':z['rect']=[3280,3240,910,1380]
for r in candidate['paths']:
 if r['id']=='island-arrival':r['points']=[[2048,3480],[2900,3480],[3160,3480]]
native_nodes={'oreum-rim':[3730,3335],'basalt-story':[3640,3770],'tangerine-orchard':[3960,4080],'jeju-arrival':[3500,3610]}
for n in candidate['accessNodes']:
 if n['id']in native_nodes:n['point']=native_nodes[n['id']]
candidate['landscapeSolids']=[v for v in candidate['landscapeSolids']if not(v['id'].startswith('orchard-tree-')or v['id']in ['oreum-core','basalt-a','basalt-b'])]+[dict(id='native-'+name,rect=[x+3180,y+3200,w,h])for name,(x,y,w,h)in [('oreum-core',(550,170,280,150)),('basalt-a',(120,450,220,200)),('basalt-b',(160,660,160,110))]]+[dict(id='native-orchard-'+str(i),rect=[v['rect'][0]+3180,v['rect'][1]+3200,v['rect'][2],v['rect'][3]])for i,v in enumerate(c['solids'][1:])]
candidate['gate2LocalizedFit']['authoritativeWalkMask']={'path':'public/assets/gate2/jeju-fit/walk.png','worldOrigin':[2350,3100],'scope':'Localized registered proof only; reservation rectangles are not a final shoreline polygon.'}
write(S/'world-fit-candidate.json',candidate)
folder=P/'jeju-fit';folder.mkdir(exist_ok=True);W,H=2002,1764;ox,oy=830,100
c=json.loads((P/'c/scene.json').read_text());fit=json.loads(json.dumps(c));fit.update(id='jeju-fit',label='Jeju fit · candidate / graybox shore',size=[W,H],ground='',grounds=[dict(image='c/ground.png',x=ox,y=oy)],mask='jeju-fit/walk.png',spawn=[760,380]);fit['objects']=[dict(o,x=o['x']+ox,y=o['y']+oy,sortY=o['sortY']+oy if o['sortY']>=0 else o['sortY'])for o in c['objects']]
fit['engineering']=[dict(rect=[0,0,810,880],color=0x596b67,label='MAINLAND / retained footprints · technical graybox'),dict(rect=[146,840,128,220],color=0x8b8c79,label='Terminal pier'),dict(rect=[800,886,30,68],color=0x8b8c79),dict(points=[[780,380],[830,380],[830,460]],width=50,color=0x8b8c79)]
for b in plan['buildings']:
 x,y,w,h=b['rect'];x-=2350;y-=3100
 if x+w>0 and x<810 and y+h>0 and y<880:fit['engineering'].append(dict(rect=[x,y,w,h],color=0x384646,label=b['label']))
local=mask((W,H),[[0,0,810,880],[146,840,128,220],[800,886,50,68]],[([[780,380],[830,380],[830,460],[850,460]],50)],[[b['rect'][0]-2350,b['rect'][1]-3100,b['rect'][2],b['rect'][3]]for b in plan['buildings']])
# Same accepted native foot mask, exact translation; ferry sea leg never becomes walkable.
import numpy as np
from scipy.ndimage import label
rgb=np.asarray(Image.open(P/'c/ground.png').convert('RGB')).astype(float)
blue=(rgb[:,:,2]>rgb[:,:,0]*1.45)&(rgb[:,:,1]>rgb[:,:,0]*1.3)&(rgb[:,:,2]>rgb[:,:,1]*1.12)&(rgb[:,:,2]>90)
labels,_=label(blue,np.ones((3,3)));ids=set(np.concatenate([labels[0,:],labels[-1,:],labels[:,0],labels[:,-1]]));ids.discard(0);sea=np.isin(labels,list(ids));sea_image=Image.fromarray((sea*255).astype('uint8'));clearance=sea_image.filter(ImageFilter.MaxFilter(17))
native_walk=ImageChops.subtract(Image.open(P/'c/walk.png').convert('L'),clearance)
write(D/'shoreline-guard.json',dict(method='Border-connected blue sea +8px clearance removed from translated accepted foot mask; technical bridge/pier support remains separately walkable',clippedOriginalWaterPixels=int(((np.asarray(Image.open(P/'c/walk.png'))>127)&sea).sum()),originalCWalkMaskModified=False,limitation='Conservative image-color guard plus restricted paths, not a complete semantic shoreline polygon'))
trans=Image.new('L',(W,H));trans.paste(native_walk,(ox,oy));combined=ImageChops.lighter(local,trans);combined.save(folder/'walk.png')
fit['targets']=[dict(id='bridge',x=ox+320,y=oy+410,label='Bridge arrival on Jeju'),dict(id='mainland-pier',x=210,y=1000,label='Mainland ferry terminal / future ferry'),dict(id='island-pier',x=ox+320,y=oy+855,label='Aligned Jeju landing'),dict(id='house',x=ox+410,y=oy+1190,label='Preserved Jeju house entrance')];fit['routes']=[dict(id='bridge-connector',points=[[760,380],[830,380],[830,460],[850,460],[1150,510]],width=50)];fit['registration']=candidate['gate2LocalizedFit'];write(folder/'scene.json',fit)
catalog=json.loads((P/'catalog.json').read_text());catalog=[v for v in catalog if v['id']not in ['original','seam','jeju-fit']];catalog.extend(dict(id=s['id'],label=s['label'])for s in [original,seam,fit]);write(P/'catalog.json',catalog)
# Explicit delta evidence, not a replacement masterplan approval.
write(D/'fit-decisions.json',dict(approvedPlanUnchanged=True,candidatePath=str((S/'world-fit-candidate.json').relative_to(R)),jejuNativeArtworkScale=1,entrancePatchPreserved=True,station=dict(before=[84,190,555,220],after=[84,200,555,210],southEdgeBefore=410,southEdgeAfter=410,world=[2322.5,2380,555,210],doorThreshold=[2598.5,2610],plaza=plan['station']['entrancePlaza'],platforms=plan['station']['platforms']),join=dict(overlapPx=48,source='Approved Muneum + station',registeredIndependentAssets=True,sourceRGBABytes=(1536*720+720*720)*4,chunkRGBABytes=(1536*720+720*720)*4)))
print('Built only new building, local fit data and two registered transition chunks; approved sources preserved')
