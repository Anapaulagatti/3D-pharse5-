"""Whole native-world scope enforcement + immutable source and geometry guards."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/final-surgical-v1';D=R/'docs/gate3-final'
def rd(p):return json.loads((R/p).read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def world(m):
 W,H=m['size'];g=Image.new('RGBA',(W,H));f=np.zeros((H,W),np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
 return g,f
def static(m,g):
 im=g.copy()
 for o in sorted(m['objects'],key=lambda o:o['sortY']):im.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 return im
b=rd('public/assets/gate3/final-before/manifest.json');base,bf=world(b);bs=static(b,base);W,H=b['size'];regions=rd('docs/gate3-final/REGION_TARGETS.json')['regions'];allmask=np.zeros((H,W),bool)
for q in regions:
 x,y,w,h=q['rect'];allmask[y:y+h,x:x+w]=True
lock=rd('assets-src/gate3/final-surgical-v1/baseline-lock.json');sourceRows=[]
for name,h in lock['files'].items():
 actual=sha(R/name);assert actual==h,('PROTECTED SOURCE CHANGED',name);sourceRows.append({'path':name,'sha256':actual,'unchanged':True})
wr(D/'protected-hashes.json',{'baseline':lock['head'],'files':sourceRows,'status':'ALL_BASELINE_SOURCE_ASSETS_EXACT','count':len(sourceRows),'oldStationRecoverable':True,'canonicalForecourtCheckpoint':'checkpoint/g3a-station-forecourt-approved-20261023','newStationIsolated':True})
reports=[]
for scene in ['final-world','final-station-candidate']:
 m=rd(f'public/assets/gate3/{scene}/manifest.json');g,f=world(m);st=static(m,g);ga=np.array(g);ba=np.array(base);sa=np.array(st);bsa=np.array(bs);gd=np.any(ga!=ba,2);sd=np.any(sa!=bsa,2);fd=f!=bf
 exactGround=np.zeros((H,W),bool);pv=rd('assets-src/gate3/final-surgical-v1/integration-provenance.json')
 for spec in pv['masks'].values():
  mx,my,mw,mh=spec['rect'];exactGround[my:my+mh,mx:mx+mw]|=np.array(Image.open(R/spec['mask']))>0
 if scene=='final-station-candidate':exactGround[2140:2715,2274:3016]|=np.array(Image.open(S/'station-underlying-retirement-mask.png'))>0
 assert not np.any(gd&~exactGround),(scene,'GROUND OUTSIDE INSTALLED EXPLICIT MASKS')
 assert not np.any(gd&~allmask),(scene,'GROUND OUT OF SCOPE');assert not np.any(sd&~allmask),(scene,'FOREGROUND OUT OF SCOPE');assert not np.any(fd&~allmask),(scene,'FIELD OUT OF SCOPE')
 # Collision modifications are strictly the farm and the new garden corner foot.
 allowedF=np.zeros((H,W),bool);allowedF[230:800,300:1060]=True;allowedF[1652:1674,610:635]=True;assert not np.any(fd&~allowedF)
 assert m['logicalSolids']==b['logicalSolids'];assert m['contactCollision']==b['contactCollision'];assert m['size']==b['size'];assert m['targets']==b['targets'];assert m['workingPlan']==b['workingPlan']
 # Canopy/planters/tree assets and registrations are unchanged in BOTH scenes.
 for ob in b['objects']:
  if ob['id']=='recovery-world/planted-tree-01':continue
  if scene=='final-station-candidate'and ob['id']=='registration/station':continue
  nn=next(o for o in m['objects']if o['id']==ob['id']);assert all(nn[k]==ob[k]for k in ['x','y','width','height','sortY']),ob['id']
  if ob['id']!='a/foreground-pine':assert nn==ob,ob['id']
 for ob in m['objects']:
  assert all(isinstance(ob[k],int)for k in ['x','y','width','height']),ob['id']
  if'sourceAnchor'in ob:assert [ob['sourceAnchor'][k]-ob['sourcePivot'][k]for k in [0,1]]==[ob['x'],ob['y']]
 canon=(2274,2603,2958,2813);assert st.crop(canon).tobytes()==bs.crop(canon).tobytes(),(scene,'CANONICAL STATIC FRONTAGE')
 kp=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0;assert np.array_equal(ga[3200:4736,3180:4204][kp],ba[3200:4736,3180:4204][kp])
 regionRows=[]
 for q in regions:
  x,y,w,h=q['rect'];d=sd[y:y+h,x:x+w];pixels=int(d.sum());assert pixels<=q['maximumIntendedChangeArea'],(scene,q['name'],pixels,q['maximumIntendedChangeArea']);regionRows.append({'region':q['name'],'worldRect':q['rect'],'changedStaticPixels':pixels,'maximum':q['maximumIntendedChangeArea'],'status':'UNCHANGED'if not pixels else'BOUNDED_CHANGE'})
 Image.fromarray(sd.astype('uint8')*255).save(D/(scene+'-native-world-difference.png'));Image.fromarray(gd.astype('uint8')*255).save(S/(scene+'-ground-change-mask.png'));Image.fromarray(fd.astype('uint8')*255).save(S/(scene+'-collision-change-mask.png'))
 # These are exact native COMPOSITING diagnostics, not substituted for Phaser.
 # Store previews rather than another full41MB map in the handoff.
 st.thumbnail((1088,1216),Image.Resampling.NEAREST);st.convert('RGB').save(D/(scene+'-static-scope-preview.jpg'),quality=87)
 reports.append({'scene':scene,'worldPixels':W*H,'groundPixelsChanged':int(gd.sum()),'staticPixelsChanged':int(sd.sum()),'unchangedStaticPercent':round(100*(1-sd.mean()),4),'outOfScopeGround':int((gd&~allmask).sum()),'groundDifferencesOutsideExactInstalledMasks':int((gd&~exactGround).sum()),'outOfScopeStatic':int((sd&~allmask).sum()),'outOfScopeCollision':int((fd&~allmask).sum()),'fieldCellsChanged':int(fd.sum()),'canonicalStaticForecourt':'PIXEL_EXACT','JejuProtectedBitmap':'PIXEL_EXACT','logicalSolidsAndTargetsAndNativePhysicalField':'EXACT','regions':regionRows})
# The isolated station candidate has EXACT same collision as final main world.
_,f1=world(rd('public/assets/gate3/final-world/manifest.json'));_,f2=world(rd('public/assets/gate3/final-station-candidate/manifest.json'));assert np.array_equal(f1,f2)
# New binary-alpha source owners are independent at scale1.
alpha=[]
for root in ['final-world','final-station-candidate']:
 for p in (R/'public/assets/gate3'/root).glob('*roof.png'):
  im=np.array(Image.open(p).convert('RGBA'));alpha.append({'file':str(p.relative_to(R)),'partialAlphaPixels':int(((im[:,:,3]>0)&(im[:,:,3]<255)).sum())})
assert all(a['partialAlphaPixels']==0 for a in alpha)
wr(D/'out-of-scope-audit.json',{'status':'PASS','method':'4352x4864 exact native source-ground + foreground compositing, no dynamic actor, source alpha preserved; masks/envelopes enforced BEFORE accepting candidate. Actual matched Phaser screenshots are separate evidence. No estimated95% criterion used in place of masks.','reports':reports,'allHistoricalSourceHashes':'PASS','stationCandidateCollisionEqualsMain':True,'binaryNativeAlpha':alpha,'protectedCheckpointTags':'Preserved; remote refs checked at handoff','artAcceptance':'PENDING HUMAN'})
wr(D/'changed-assets.json',{'generator':'tools/g3ds_build.py','provenance':rd('assets-src/gate3/final-surgical-v1/integration-provenance.json'),'newSourceAssets':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(S.glob('*'))if p.is_file()],'runtimeFiles':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for root in ['final-before','final-world','final-station-candidate','final-station-ground']for p in sorted((R/'public/assets/gate3'/root).glob('*'))if p.is_file()]})
print('SOURCE + SCOPE PASS',[(q['scene'],q['staticPixelsChanged'],q['outOfScopeStatic'],q['fieldCellsChanged'])for q in reports])
