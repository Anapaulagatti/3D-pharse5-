from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/reconciliation-v1';D=R/'docs/gate3-reconciliation'
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
approved=json.loads(subprocess.check_output(['git','show','checkpoint/gate1-approved-planning-20261022:assets-src/world-gate1/plan.json'],cwd=R));current=read('assets-src/world-gate1/plan.json');work=read('assets-src/gate3/production-plan-v3.1-restored.json');m=read('public/assets/gate3/zoned-world/manifest.json');assert approved==current
assert approved['boundaries']==work['plan']['boundaries'];assert [b for b in approved['buildings']if b['kind']=='heritage']==[b for b in work['plan']['buildings']if b['kind']=='heritage']
g=Image.new('RGBA',m['size'])
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
regions={'palacewest':[1000,120,1536,1024],'palaceeast':[1664,120,1536,1024],'station':[1792,1920,1536,1024],'commercial':[1280,1740,1536,1024],'waternorth':[2816,3020,1536,1024],'watersouth':[2816,3840,1536,1024]}
for name,(x,y,w,h)in regions.items():
 part=g.crop((x,y,x+w,y+h));part.save(S/(name+'-before-ground.png'),optimize=True);d=ImageDraw.Draw(part)
 if name.startswith('palace'):
  for b in approved['boundaries']:
   bx,by,bw,bh=b['rect'];d.rectangle((bx-x,by-y,bx+bw-x-1,by+bh-y-1),outline='#ff716f',width=3)
  for b in approved['buildings']:
   if b['kind']!='heritage':continue
   bx,by,bw,bh=b['rect'];d.rectangle((bx-x,by-y,bx+bw-x-1,by+bh-y-1),outline='#e9a7d0',width=2)
  d.rectangle((1830-x,790-y,2259-x,1064-y),outline='#7be2ed',width=3)
  for path in approved['paths']:
   if path['kind']=='heritage':d.line([(px-x,py-y)for px,py in path['points']],fill='#7be2ed',width=2)
 part.save(S/(name+'-guide.png'),optimize=True)
# Conservative native preservation envelopes, not permission to move protected artwork.
protectedArchitecture=[{'id':'baked-main-hall','rect':[1510,650,1010,140]},{'id':'baked-west-pavilion','rect':[1320,685,430,290]},{'id':'baked-academy','rect':[640,975,465,390]},{'id':'baked-teahouse','rect':[1180,1035,430,335]}]
findings=[{'id':'palace-wall-west','approved':[1110,170,30,870],'visibleSourceWallApprox':[1070,650,35,390],'finding':'Upper perimeter incomplete. Visible lower roof envelope is not its support footprint; restore exact registered support without treating roof projection as displacement.'},{'id':'palace-wall-south-west','approved':[1110,1040,720,25],'visibleSourceWallApprox':[1070,995,760,70],'finding':'Source roof/course band may project above the1040 support plane; opening width and added eastern compound hierarchy require reconciliation, not automatic wall displacement.'},{'id':'ceremonial-court','approvedAxis':[2048,920,2048,1150],'derivedClearCourt':[1830,790,430,275],'finding':'Central430px south opening should stay open; source garden pockets narrow the court to about144px. Clear intrusive nonarchitectural scenery in derived ownership only.'},{'id':'palace-plinth','approvedContact':[1510,290,1050,460],'visiblePlinthBottom':790,'approvedBottom':750,'finding':'40px source stair/plinth extension is not an approved northern easement. Architecture remains unchanged; deliver localized native-layer re-registration proposal, not silently move it.'},{'id':'academy-cropped-source','approvedContact':[490,1110,530,250],'sourceFrameLeft':640,'finding':'Approved sample crops the western academy silhouette at its left frame. Roof/facade envelope is not a measured ground footprint. Full completion/registration cannot be certified from this clipped source; bounded derived-layer proposal required.'}]
authority={'approvedGate1':{'checkpoint':'checkpoint/gate1-approved-planning-20261022','commit':subprocess.check_output(['git','rev-parse','checkpoint/gate1-approved-planning-20261022^{}'],text=True).strip(),'file':'assets-src/world-gate1/plan.json','workingFileExact':True},'latestWorking':{'file':'assets-src/gate3/production-plan-v3.1-restored.json','authority':['docs/current/GATE25_AUTHORIZATION.md','docs/current/G3A_SPATIAL_DECISION.md','docs/current/G3BC_WORLD_PRODUCTION_AUTHORIZATION.md'],'embeddedHistoricalGateStatus':'Superseded by subsequent human authorization, not a rollback to G3-A blocked status.','historicBuildingsAndBoundariesExact':True,'acceptedAmendments':['4352x4864 extent / native Jeju source registration','Maru contact180,3120,421,210 and corrected door326,3343 / western scenic loop','Cafe25px eastern easement / native retail facade projections','Canonical station0.5px pivot / restored forecourt / original canopy'],'deferred':['Bakery required/unplaced; W0 rejected; Q1 land unallocated','Station8px transfer strip remains closed']},'visualAuthority':['Gate1 / Gate2.5 approved native artwork and Art Direction Bible'],'eightMarkedImages':{'received':0,'status':'NOT PROVIDED / exact annotations unexamined'},'geometryCaveat':'Building roof/silhouette envelope is not automatically a ground footprint. Gate1 entry dots are public approach targets, not exact facade-door thresholds.'}
write(S/'registry.json',{'baselineCommit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'baselineManifest':'public/assets/gate3/zoned-world/manifest.json','regions':regions,'architecturePreservation':protectedArchitecture,'authority':authority,'findings':findings,'approvedBoundaries':approved['boundaries'],'northernBuildings':[b for b in approved['buildings']if b['kind']=='heritage'],'protectedFloor':[2274,2603,684,210],'protectedJeju':[3180,3200,1024,1536],'noPlanningAmendments':True})
write(D/'spatial-fidelity.json',{'authority':authority,'findings':findings,'geometryStatus':'FAIL_PENDING_DERIVED_RECONCILIATION / protected architecture conflicts not auto-approved'})
# Registered semantic overlay. Source walls manually located approximate; approved geometry exact.
full=g.copy()
for o in sorted(m['objects'],key=lambda o:o['sortY']):full.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
full=full.crop((1000,100,3050,1600));d=ImageDraw.Draw(full)
for b in approved['boundaries']:
 x,y,w,h=b['rect'];d.rectangle((x-1000,y-100,x+w-1001,y+h-101),outline='#59ecff',width=4)
for b in approved['buildings']:
 if b['kind']!='heritage':continue
 x,y,w,h=b['rect'];d.rectangle((x-1000,y-100,x+w-1001,y+h-101),outline='#ffe282',width=3);d.text((x-995,y-92),b['id'],fill='white',stroke_width=1,stroke_fill='black')
for f in findings:
 if 'visibleSourceWallApprox'in f:
  x,y,w,h=f['visibleSourceWallApprox'];d.rectangle((x-1000,y-100,x+w-1001,y+h-101),outline='#ff666b',width=3)
full.save(D/'palace-semantic-overlay-native.png',optimize=True);full.thumbnail((1025,750),Image.Resampling.NEAREST);full.convert('RGB').save(D/'palace-semantic-overlay-preview.jpg',quality=88,optimize=True)
print('Authority ledger verified;6 native guides / semantic mismatch overlay prepared')
