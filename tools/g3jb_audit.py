"""Strict native scope, approved station/source hashes, renderer readback and geometry."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/jeju-bridges-v1';D=R/'docs/gate3-jeju-bridges'
def rd(p):return json.loads((R/p).read_text())
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def world(m):
 g=Image.new('RGBA',m['size']);f=np.zeros(m['size'][::-1],np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
 return g,f
def static(m,g):
 im=g.copy()
 for o in sorted(m['objects'],key=lambda o:o['sortY']):im.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 return im
lock=rd('assets-src/gate3/jeju-bridges-v1/baseline-lock.json');b=lock['manifest'];m=rd('public/assets/gate3/jeju-bridges-world/manifest.json');bg,bf=world(b);g,f=world(m);allow=np.array(Image.open(S/'edit-scope-mask.png'))>0;gd=np.any(np.array(bg)!=np.array(g),2);sd=np.any(np.array(static(b,bg))!=np.array(static(m,g)),2);fd=f!=bf
for kind,delta in [('ground',gd),('static',sd),('collision',fd)]:assert not np.any(delta&~allow),kind
assert m['logicalSolids']==b['logicalSolids'];assert m['targets']==b['targets'];assert m['stops']==b['stops'];assert m['workingPlan']==b['workingPlan'];assert m['deferredContent']==b['deferredContent']
for o in b['objects']:
 if o['id'].startswith('alignment/bridge-'):continue
 assert o==next(q for q in m['objects']if q['id']==o['id']),o['id']
for p,h in lock['files'].items():assert sha(R/p)==h,('PROTECTED FILE',p)
station=[o for o in b['objects']if o['id'].startswith('clean-station/')];assert len(station)==3
wr(D/'protected-hashes.json',{'status':'PASS','filesUnchanged':len(lock['files']),'files':lock['files'],'approvedHanbitCheckpoint':'checkpoint/g3d-hanbit-approved-20261025','canonicalStationObjectsExact':station,'stationRasterAndCollision':'EXACT / outside bridge scope','allOtherNonBridgeObjectsExact':True})
# Native station area is compared in full, not only source file names.
assert np.array_equal(np.array(static(b,bg))[2100:2850,2230:3050],np.array(static(m,g))[2100:2850,2230:3050]);assert np.array_equal(bf[2100:2850,2230:3050],f[2100:2850,2230:3050])
Image.fromarray(sd.astype('uint8')*255).save(D/'native-world-difference.png');wr(D/'out-of-scope-audit.json',{'status':'PASS','baseline':lock['HEAD'],'changedGroundPixels':int(gd.sum()),'changedStaticPixels':int(sd.sum()),'changedCollisionCells':int(fd.sum()),'outOfScopeGroundPixels':0,'outOfScopeStaticPixels':0,'outOfScopeCollisionCells':0,'stationFullNativeAreaAndCollision':'EXACT','masterplanAndTargets':'EXACT','sourceResampling':'NONE / native integer source coordinates','scope':rd('assets-src/gate3/jeju-bridges-v1/scope.json'),'limits':'Art quality requires human inspection. Scope PASS is not art approval.'})
# The guard field changes only inside authorized bridge mask.
q=b['contactCollision'];ox,oy,w,h=q['rect'];a=np.fromfile(R/'public'/q['physical'],np.uint8).reshape(h,w);n=np.fromfile(R/'public'/m['contactCollision']['physical'],np.uint8).reshape(h,w);assert not np.any((a!=n)&~allow[oy:oy+h,ox:ox+w])
# Native Phaser ground pixels and matched camera pairs (exclude dynamic Juni).
cap=rd('docs/gate3-jeju-bridges/native-captures.json');man={};grounds={};rows=[];pairs=[];total=0
for scene in ['jeju-bridges-before','jeju-bridges-world']:
 man[scene]=rd('public/assets/gate3/'+scene+'/manifest.json');grounds[scene]=world(man[scene])[0]
for row in cap['rows']:
 cam=row['audit']['camera'];assert cam['zoom']==1 and all(float(v).is_integer()for v in cam['scroll']);sx,sy=map(round,cam['scroll']);im=Image.open(D/(row['name']+'.png')).convert('RGB');sw,sh=im.size;wanted=grounds[row['scene']].crop((sx,sy,sx+sw,sy+sh)).convert('RGB');ok=np.ones((sh,sw),bool)
 for l in row['audit']['layers']:
  assert l['scaleMode']==1 and all(float(v).is_integer()for v in l['position'])
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  o=next(o for o in man[row['scene']]['objects']if'f/'+o['id']==l['key']);tex=Image.open(R/'public'/o['image']).convert('RGBA');x,y=o['x'],o['y'];lx=max(x,sx);ly=max(y,sy);rx=min(x+tex.width,sx+sw);ry=min(y+tex.height,sy+sh)
  if lx<rx and ly<ry:ok[ly-sy:ry-sy,lx-sx:rx-sx]&=np.array(tex.getchannel('A').crop((lx-x,ly-y,rx-x,ry-y)))==0
 s=row['state'];cx,cy=round(s['x'])-sx,round(s['y'])-sy;ok[max(0,cy-102):min(sh,cy+14),max(0,cx-50):min(sw,cx+50)]=False;diff=np.any(np.array(im)!=np.array(wanted),2)&ok;assert not diff.any(),(row['name'],'GROUND READBACK');total+=int(ok.sum());rows.append({'frame':row['name'],'exactGroundPixels':int(ok.sum()),'mismatches':0,'zoom':1,'integerCamera':True,'nearest':True})
 if row['phase']=='after':
  before=next(q for q in cap['rows']if q['phase']=='before'and q['entry']==row['entry']);assert cam==before['audit']['camera'];bi=Image.open(D/(before['name']+'.png')).convert('RGB');permitted=Image.fromarray(allow.astype('uint8')*255).crop((sx,sy,sx+sw,sy+sh));dr=ImageDraw.Draw(permitted)
  for rr in [before,row]:
   x,y=round(rr['state']['x'])-sx,round(rr['state']['y'])-sy;dr.rectangle((x-50,y-102,x+50,y+14),fill=255)
  assert not np.any(np.any(np.array(im)!=np.array(bi),2)&(np.array(permitted)==0)),(row['name'],'OUTSIDE SCOPE');pairs.append({'entry':row['entry'],'sameCamera':True,'outOfScopeNativePixels':0})
wr(D/'native-render-qa.json',{'status':'PASS','frames':rows,'pairs':pairs,'exactNativeGroundPixels':total,'mismatches':0,'outOfScopeNativePixels':0,'rendererAndJuni':'UNCHANGED','nearestNeighbor':'PASS','hardwarePerformance':'NOT TESTED','artAcceptance':'PENDING HUMAN'})
# Cross sections of physical source geometry. Native54x7 contact union is NOT a
# silhouette box; camera foreshortens deck depth. Before A uses old guard field.
oldphys=bf>0;oldphys[oy:oy+h,ox:ox+w]=a>0;newphys=np.array(Image.open(S/'visible-physical-support.png'))>0
def width(field,x,y,axis):
 if not field[y,x]:return 0
 lo=hi=0
 while lo<250 and field[y-(lo+1)*(axis=='y'),x-(lo+1)*(axis=='x')]:lo+=1
 while hi<250 and field[y+(hi+1)*(axis=='y'),x+(hi+1)*(axis=='x')]:hi+=1
 return lo+hi+1
sections=[]
for k,x,y,axis in [('A-entrance',3110,3460,'x'),('A-stone-span',3300,3555,'y'),('B-approach',3120,3975,'x'),('B-stone-span',3300,4020,'y')]:sections.append({'section':k,'world':[x,y],'scanAxis':axis,'beforeClearNativePixels':width(oldphys,x,y,axis),'afterClearNativePixels':width(newphys,x,y,axis)})
sections[0].update(scanBounds=[3042,3240],beforeClearNativePixels=int(oldphys[3460,3042:3241].sum()),afterClearNativePixels=int(newphys[3460,3042:3241].sum()),interpretation='Native timber entrance section only, excluding mainland paved street; old central bollard holes at adjacent rows reported separately')
wr(D/'alignment-measurements.json',{'method':'Native1px source floor traces plus exact current collision/old contact field, independent A/B. Camera-space deck scan widths are not claimed to be metres or full vertical sprite footprint.','sections':sections,'nativeContactUnion':{'frames':120,'width':54,'height':7,'model':'Opaque lowest4 atlas rows; raised feet projected to anchor, below-anchor toes retained.'},'sourceTransform':{'AAndBOriginalJejuOrigin':[3180,3200],'canonicalNativeIslandSize':[1024,1536],'newSourceOrigin':[2816,3200],'newSourceScale':1},'A':{'actualMainlandPublicAnchor':[3010,3460],'originalDiagnosticWaypoint':[3110,3460],'islandPublicAnchor':[3530,3640],'oldProposalNotAutoAdopted':'25px/4866px² historical shape was diagnostic only. New floor follows freshly visible structural artwork; no proposed old mask installed.'},'B':{'mainlandPublicAnchor':[3030,3920],'originalApproachEndEstimate':[3135,4020],'oldDeckStartEstimate':[3180,4030],'beforeNativeAxisGapPx':[45,10],'estimatePolicy':'Manually traced original visible source landing/deck junction, not an alleged protected control point. Original planned world geometry/endpoints stay untouched.','repairedLocalApproachVia':[3120,3975],'islandPublicAnchor':[3570,4060]},'workingPlan':'UNMODIFIED. Legacy bridgeConnector planning polyline retained; actual source-aligned corridor supplied in geometric-clearance.json, not silent masterplan rewrite.','approval':'Final visual alignment pending HUMAN'})
wr(D/'changed-assets.json',{'newSourceFiles':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(S.glob('*'))if p.is_file()],'runtimeFiles':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted((R/'public/assets/gate3/jeju-bridges-world').glob('*'))if p.is_file()]})
print('Scope/native PASS:',len(lock['files']),'unchanged sources;',total,'exact native pixels;',len(pairs),'matched pairs;station EXACT')
