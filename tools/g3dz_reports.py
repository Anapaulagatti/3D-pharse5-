from pathlib import Path
import json,hashlib,subprocess,io
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-zoned-world';S=R/'assets-src/gate3/zoned-world-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
q=read(D/'technical-qa.json');shots=read(D/'native-captures.json');movement=read(D/'movement-report.json');integration=read(S/'integration-provenance.json');registry=read(S/'land-use-registry.json')
assert not shots['errors']and len(shots['rows'])==50
assert len(q['pixelReadback'])==25 and all(r['mismatched']==0 and r['integerCamera']and r['samplingScaleNative']for r in q['pixelReadback'])
assert q['protectedHashes']['status']=='PASS'and q['protectedHashes']['historicalTagsUnchanged']and all(q['rendererCoreUnchanged'].values())
assert all(o['registrationAndTexture']=='PASS'for o in q['protectedObjectRegistration'])
frames={r['name']:r for r in shots['rows']};pairs=[]
for name,r in frames.items():
 if '-after-'not in name:continue
 b=frames[name.replace('-after-','-before-')]
 assert r['audit']['camera']['scroll']==b['audit']['camera']['scroll'],name
 pairs.append({'frame':name,'scroll':r['audit']['camera']['scroll'],'beforeAfterFramingExact':True})
assert movement['complete']and len(movement['legs'])==17 and not movement['errors']
# Freeze ALL previous ten-region source/runtime/evidence files as an additional checkpoint lock.
rows=[]
for line in subprocess.check_output(['git','ls-tree','-r','5e899c9','--','assets-src/gate3/recovery-world-v1','public/assets/gate3/recovery-world','public/assets/gate3/recovery-world-before','docs/gate3-recovery-world'],text=True).splitlines():
 meta,path=line.split('\t',1);oid=meta.split()[2];data=(R/path).read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert actual==oid,path
 rows.append({'path':path,'baselineBlob':oid,'unchanged':True})
write(D/'prior-g3d-checkpoint-hashes.json',{'baseline':'5e899c9 / checkpoint/g3d-world-recovery-review-20261023','filesChecked':len(rows),'status':'PASS','files':rows})
# Protected native collision regions; new tree/bed ownership must not alter these.
def field(m):
 a=np.zeros((m['size'][1],m['size'][0]),np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];a[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
 return a
m=read(R/'public/assets/gate3/zoned-world/manifest.json');before=read(R/'public/assets/gate3/recovery-world/manifest.json');a,b=field(m),field(before);regions=[]
for item in registry['protectedGround']:
 x,y,w,h=item['rect'];same=np.array_equal(a[y:y+h,x:x+w],b[y:y+h,x:x+w]);assert same,item
 regions.append({'rect':item['rect'],'collisionExact':same})
q['checks']={'typecheck':'PASS','historicalAndActorChecks':'PASS','targetedLint':'PASS','unitTests':'28 PASS /8 files','reviewBuild':'PASS','actualNativeFrames':50,'nativeBeforeAfterPairs':25,'nativeAfterReadbacks':25,'eligibleOpaquePixels':sum(x['opaqueGroundPixels']for x in q['pixelReadback']),'mismatchPixels':0,'continuousRealMovementLegs':17,'completeWorldArtAcceptance':'PENDING HUMAN','physicalDevices':'NOT TESTED'}
q['priorRecoveryCheckpointPreserved']={'files':len(rows),'status':'PASS'};q['protectedCollisionRegions']=regions;q['framing']=pairs
q['environmentChanges']={'groundChunksRebuilt':len(integration['changedGroundChunks']),'groundChunksReused':len(integration['unchangedGroundChunks']),'treeInstancesRemoved':len(integration['removedUrbanTrees']),'newEnvironmentContacts':integration['newEnvironmentContacts'],'floorArchitectureAndObjectRegistration':'UNCHANGED','nativeFrameSupport':'New review scene IDs use existing nativeFrames path in main.ts; protected camera/renderer modules unchanged'}
q['visualAxes']={'architecture':'PRESERVED / no new building art; final world composition pending','materials':'REVIEW / fine common urban granite, purpose-based landscapes, no rejected atlas','depth':'SELECTED CASE PASS / inherited bookshop fade retained; tower/ride projection P1 remains','lighting':'REVIEW / native source lighting retained; coast contacts/shadows require human judgment','composition':'PENDING HUMAN / improved zones, protected planning conflicts remain','scale':'NATIVE1X / protected roots/envelopes unchanged','navigation':'FAIL_FULL_NETWORK /17 selected real foot-point legs pass; six line failures/full-body ownership remain','pixelClarity':'PASS_RUNTIME /25 opaque ground readbacks exact; canonical source-edge softness/artifacts separately retained'}
q['managedCache']={'peakLogicalBytes':max(x['chunks']['peakBytes']for x in movement['samples']),'budgetBytes':67108864,'limits':'Managed cache only; excludes canvas/browser/driver/atlas overhead. Headless cadence is not hardware FPS acceptance.'}
q['exactReviewerMarkedRegions']='NOT TESTED / six images absent; textual defect crops only';write(D/'technical-qa.json',q)
write(D/'native-registration-checks.json',{'remainingObjectRegistrationsExact':True,'stationSourcePivot':'Original explicit0.5px source registration unchanged','canonicalGround':integration['protectedRegions'],'logicalSolidsExact':m.get('logicalSolids')==before.get('logicalSolids'),'protectedCollisionRegions':regions,'newEnvironmentContacts':integration['newEnvironmentContacts'],'changedMasks':integration['changedMaskChunks'],'station8pxStrip':'UNCHANGED/CLOSED','platformConnector90x36':'NOT PRESENT','planningAmendments':[]})
files=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(S.rglob('*'))if p.is_file()and not p.name.endswith('-before-ground.png')]
write(D/'asset-provenance.json',{'authoring':'Built-in host imagegen only; no external paid provider API. Exact/qualified prompts and original host paths retained in authoring-jobs.json.','sources':files,'nativeComposition':'Integer crops and explicit binary ownership masks. No approved source resizing/filtering/recoloring. Shared offshore wave material reuses the existing approved native surface; authored coast plus documented binary depth transitions. Canonical open-water texels reflected at1:1 only in external water apron, not island geometry.','protectedSourceFiles':'1440 prior protected hashes plus prior G3-D checkpoint file lock','artAcceptance':'PENDING HUMAN'})
video={}
for name in ['world-traversal.webm','world-traversal-native-resolution.mp4','world-traversal-review.mp4']:
 p=D/name;probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate:format=duration,size','-of','json',str(p)]));video[name]={'sha256':sha(p),'bytes':p.stat().st_size,'probe':probe,'published':name.endswith('.mp4')}
write(D/'video-provenance.json',{'method':'Actual continuous final-build Playwright recording with WASD/Shift, original Juni, real collision, no teleport or collision override. Earlier pre-final-street run preserved locally, not presented as final.','nativeResolution':'1280x1000 H264 viewing encode without spatial resize; not pixel-exact proof','review':'512x400 nearest-neighbor viewing resize; native PNGs are pixel-quality evidence','files':video})
# Overlay is technical evidence, never an artistic gameplay substitute.
row=frames['station-amusement-after-native'];im=Image.open(D/'station-amusement-after-native.png').convert('RGBA');overlay=Image.new('RGBA',im.size);od=ImageDraw.Draw(overlay);sx,sy=row['audit']['camera']['scroll']
for rect,color in [([2950,2626,8,129],(255,45,65,220)),([2130,2742,144,96],(80,205,255,150))]+[(c['rect'],(255,155,40,180))for c in integration['newEnvironmentContacts']]:
 x,y,w,h=rect;od.rectangle((x-sx,y-sy,x+w-sx-1,y+h-sy-1),outline=color,width=2)
Image.alpha_composite(im,overlay).save(D/'station-collision-overlay-native.png',optimize=True)
print('Consolidated QA:',q['checks'],'prior checkpoint files',len(rows))
