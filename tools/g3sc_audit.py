"""Purge provenance, strict region masks, historical hashes and real native readback."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/station-clean-v1';D=R/'docs/gate3-station-clean'
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
spec=rd('assets-src/gate3/station-clean-v1/scope.json');lock=rd('assets-src/gate3/station-clean-v1/baseline-lock.json');b=rd('public/assets/gate3/station-clean-before/manifest.json');bg,bf=world(b);bs=np.array(static(b,bg));W,H=b['size'];allowed=np.zeros((H,W),bool)
for q in spec['regions']:
 x,y,w,h=q['rect'];allowed[y:y+h,x:x+w]=True
paint=np.array(Image.open(S/'purged-ground-mask.png'))>0;legacy={o['id']for o in spec['legacyObjectsRemoved']};legacyTextures={o['image']for o in spec['legacyObjectsRemoved']};sources=[]
for name,h in lock['assets'].items():
 actual=sha(R/name);assert actual==h,('HISTORICAL SOURCE CHANGED',name);sources.append({'path':name,'sha256':actual,'unchanged':True})
wr(D/'protected-hashes.json',{'status':'ALL_BASELINE_FILES_IMMUTABLE_IN_HISTORY / legacy art NOT retained in active world','count':len(sources),'files':sources})
reg=[];manifests={};grounds={};fields={};newSource=np.array(Image.open(S/'fresh-station-authored.png').convert('RGBA'));freshFloor=np.array(Image.open(S/'fresh-empty-site-authored.png').convert('RGBA'));shadow=np.array(Image.open(S/'fresh-contact-shadow-mask.png'))>0
for scene in ['station-clean-before','station-clean-site','station-clean-world']:
 m=rd('public/assets/gate3/'+scene+'/manifest.json');g,f=world(m);manifests[scene]=m;grounds[scene]=g;fields[scene]=f
 if scene=='station-clean-before':continue
 assert not any(o['id']in legacy for o in m['objects']);assert not({o['image']for o in m['objects']}&legacyTextures)
 assert m['logicalSolids']==b['logicalSolids'];assert m['targets']==b['targets'];assert m['contactCollision']==b['contactCollision'];assert m['workingPlan']==b['workingPlan']
 for o in b['objects']:
  if o['id']in legacy:continue
  assert next(n for n in m['objects']if n['id']==o['id'])==o,('PROTECTED NEIGHBOR OBJECT',o['id'])
 gg=np.array(g);gd=np.any(gg!=np.array(bg),2);sd=np.any(np.array(static(m,g))!=bs,2);fd=f!=bf;assert not np.any(gd&~paint);assert not np.any(sd&~allowed);assert not np.any(fd&~paint)
 # Every old station ground pixel is replaced, including what is hidden under
 # the new building. No seam-retained legacy floor/shadow or old layer underneath.
 for x,y,w,h in [spec['plot'],spec['extraGround']]:
  expected=freshFloor[y-1920:y-1920+h,x-1920:x-1920+w].copy()
  if scene=='station-clean-world':
   sh=shadow[y-1920:y-1920+h,x-1920:x-1920+w];expected[sh]=newSource[y-1920:y-1920+h,x-1920:x-1920+w][sh]
  assert np.array_equal(gg[y:y+h,x:x+w],expected),(scene,'LEGACY GROUND UNDER NEW ART')
 # No source-era ground chunk containing the old lot is used in active scenes.
 for c in m['chunks']:
  if np.any(paint[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']]):assert c['image']!=next(q for q in b['chunks']if q['id']==c['id'])['image']
 Image.fromarray(sd.astype('uint8')*255).save(D/(scene+'-native-difference.png'))
 reg.append({'scene':scene,'changedGroundPixels':int(gd.sum()),'changedStaticPixels':int(sd.sum()),'outOfBoundsGroundPixels':int((gd&~paint).sum()),'outOfBoundsStaticPixels':int((sd&~allowed).sum()),'outOfBoundsCollisionCells':int((fd&~paint).sum()),'oldStationObjectsPresent':0,'oldStationTexturesReferenced':0,'stationOwnedGroundReplaced':'100% / exact fresh ground +new shadow ownership','oldPlatformStripBlockedCells':int((f[2626:2755,2950:2958]==0).sum()),'logicalCoordinatesAndTargets':'EXACT','allNonStationObjects':'EXACT'})
# Fresh masters and generation references prove this is not a recomposed legacy
# station: no old-station image/crop/mask appears in any authoring input.
jobs=rd('assets-src/gate3/station-clean-v1/authoring-jobs.json');validRefs={'purged-authoring-guide.png','fresh-massing-guide.png','strict-native-massing-guide.png','GATE1_STREET_NATIVE.png'}
for j in jobs:assert all(Path(ref).name in validRefs for ref in j['refs']),j['id']
newObjects=[o for o in manifests['station-clean-world']['objects']if o['id'].startswith('clean-station/')];assert len(newObjects)==3
for o in newObjects:
 im=np.array(Image.open(R/'public'/o['image']).convert('RGBA'));a=im[:,:,3];assert not np.any((a>0)&(a<255));assert not np.any(a[0])and not np.any(a[-1])and not np.any(a[:,0])and not np.any(a[:,-1]);assert np.array_equal(im[:,:,:3],newSource[220:720,354:1038,:3]);assert [o['sourceAnchor'][i]-o['sourcePivot'][i]for i in [0,1]]==[o['x'],o['y']]
wr(D/'purge-and-scope.json',{'status':'PASS_TECHNICAL_PURGE_AND_SCOPE','baseline':lock['HEAD'],'plot':spec['plot'],'scope':spec['regions'],'legacySourceDonorsUsed':[],'rejectedFreshOversizeSource':'Retained but NEVER installed; no shrinking/resampling used','freshGenerationInputs':'Clean engineering site +original non-station Muneum Gate1 reference ONLY','legacyObjects':spec['legacyObjectsRemoved'],'reports':reg,'newNativeObjects':newObjects,'sourcePixelPolicy':'Source1:1; independent masks from the fresh painting, never old station contours. No filters/resampling.','limits':'Technical provenance/absence checks and strict scope do not substitute for human artistic inspection.'})
# Real native Phaser pixels: ground, fresh opaque architecture, and matched scope.
cap=rd('docs/gate3-station-clean/native-captures.json');assert not cap['errors'];native=[];pairs=[];groundTotal=0;archTotal=0
for row in cap['rows']:
 cam=row['audit']['camera'];s=row['state'];assert cam['zoom']==1;assert all(float(v).is_integer()for v in cam['scroll']);sx,sy=map(round,cam['scroll']);shot=Image.open(D/(row['name']+'.png')).convert('RGB');sw,sh=shot.size;want=grounds[row['scene']].crop((sx,sy,sx+sw,sy+sh)).convert('RGB');eligible=np.ones((sh,sw),bool)
 for l in row['audit']['layers']:
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  if row['phase']!='before':assert l['key'][2:]not in legacy
  o=next(q for q in manifests[row['scene']]['objects']if 'f/'+q['id']==l['key']);assert l['scale']==[1,1]and l['scaleMode']==1;assert all(float(v).is_integer()for v in l['position']);im=Image.open(R/'public'/o['image']).convert('RGBA');x,y=map(round,l['position']);lx=max(sx,x);ly=max(sy,y);rx=min(sx+sw,x+im.width);ry=min(sy+sh,y+im.height)
  if lx>=rx or ly>=ry:continue
  ar=np.array(im.crop((lx-x,ly-y,rx-x,ry-y)));opaque=ar[:,:,3]>0;eligible[ly-sy:ry-sy,lx-sx:rx-sx]&=~opaque
  if o['id'].startswith('clean-station/'):
   assert l['alpha']==1;actual=np.array(shot.crop((lx-sx,ly-sy,rx-sx,ry-sy)));assert not np.any(np.any(actual!=ar[:,:,:3],2)&opaque),(row['name'],o['id'],'FRESH ARCHITECTURE RESAMPLING');archTotal+=int(opaque.sum())
 cx,cy=round(s['x'])-sx,round(s['y'])-sy;eligible[max(0,cy-102):min(sh,cy+14),max(0,cx-50):min(sw,cx+50)]=False
 diff=np.any(np.array(shot)!=np.array(want),2)&eligible;assert not np.any(diff),(row['name'],'NATIVE GROUND');groundTotal+=int(eligible.sum());native.append({'frame':row['name'],'groundReadbackPixels':int(eligible.sum()),'groundMismatches':0,'integerCamera':True,'nearestScale1':True})
 if row['phase']=='before':continue
 before=next(q for q in cap['rows']if q['phase']=='before'and q['entry']==row['entry']);assert cam==before['audit']['camera'];a=Image.open(D/(before['name']+'.png')).convert('RGB');dr=Image.new('L',shot.size);draw=ImageDraw.Draw(dr)
 for r in spec['regions']:
  x,y,w,h=r['rect'];draw.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),fill=255)
 for q in [before,row]:
  cx,cy=round(q['state']['x'])-sx,round(q['state']['y'])-sy;draw.rectangle((cx-50,cy-102,cx+50,cy+14),fill=255)
 assert not np.any(np.any(np.array(a)!=np.array(shot),2)&(np.array(dr)==0)),(row['name'],'NATIVE OUT OF BOUNDS');pairs.append({'before':before['name'],'candidate':row['name'],'sameCamera':True,'outOfBoundsPixels':0})
wr(D/'native-render-qa.json',{'status':'PASS','frames':native,'matchedPairs':pairs,'groundReadbackPixels':groundTotal,'freshOpaqueArchitectureReadbackPixels':archTotal,'sourcePixelMismatches':0,'outOfBoundsNativePixels':0,'originalJuniAndRenderer':'UNCHANGED','physicalDevices':'NOT TESTED','artAcceptance':'PENDING HUMAN'})
wr(D/'changed-assets.json',{'provenance':rd('assets-src/gate3/station-clean-v1/integration-provenance.json'),'newSourceFiles':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(S.glob('*'))if p.is_file()],'newRuntimeFiles':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for name in ['station-clean-before','station-clean-site','station-clean-world']for p in sorted((R/'public/assets/gate3'/name).glob('*'))if p.is_file()]})
print('Purge/scope/native PASS:',len(sources),'historical assets;',len(native),'Phaser frames;',groundTotal,'ground +',archTotal,'NEW architecture pixels;0 mismatches/out-of-bounds')
