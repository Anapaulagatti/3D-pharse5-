from pathlib import Path
import hashlib,json,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery-world';S=R/'assets-src/gate3/recovery-world-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
q=read(D/'technical-qa.json');movement=read(D/'movement-report.json');shots=read(D/'native-captures.json')
assert movement['complete']and len(movement['legs'])==17 and not movement['errors']
assert not shots['errors']and all(x['mismatched']==0 and x['integerCamera']and x['samplingScaleNative']for x in q['pixelReadback'])
assert q['protectedHashes']['status']=='PASS'and q['protectedHashes']['historicalTagsUnchanged']
assert all(q['rendererCoreUnchanged'].values())
q['checks']={'typecheck':'PASS','protectedActorAndHistoricalAssetChecks':'PASS','targetedLint':'PASS','existingUnitTests':'28 PASS /8 files','reviewBuild':'PASS','nativeFrames':18,'eligibleOpaqueGroundPixels':sum(x['opaqueGroundPixels']for x in q['pixelReadback']),'nativeGroundMismatchPixels':0,'actualContinuousMovementLegs':17,'fullBodyOrAllPublicRouteAcceptance':'FAIL / NOT CERTIFIED'}
q['visualAxes']={'architecture':'REVIEW / complete native candidate forms, protected architecture retained; no human acceptance inferred','materials':'REVIEW / propagated native system; upper compound/density/joins P2 remain','depth':'TECHNICAL_SELECTED_CASE_PASS / foreground visibility repaired; projection P1 open','lighting':'REVIEW / consistent source direction, grounding/shadow polish requires human inspection','composition':'FAIL_FINAL_ACCEPTANCE / tower, residual ride-road projection, missing Bakery and route decisions','scale':'NATIVE_1X_PASS /105px accepted tower door retained; new landmark profiles require human proportion/program review','navigation':'FAIL_FULL_NETWORK /17 selected foot-point legs pass, six planned-line failures and49px clearance remain','pixelClarity':'PASS_RUNTIME / integer placement, nearest sampling, opaque pixel readback exact; source-alpha/detail is separate visual review'}
q['managedCache']={'peakLogicalBytes':max(x['chunks']['peakBytes']for x in movement['samples']),'budgetBytes':67108864,'hardwarePerformanceAcceptance':'UNRESOLVED','limits':'Logical managed resources only; excludes browser/driver/canvas/atlas overhead. Headless recording and update cadence are not hardware FPS proof.'}
q['evidenceVersion']={'continuousRun':'Final shared-water/landmark build; final binary overlap-ownership normalization does not change collision geometry. All18 native frame readbacks verified against final assets.','conservativeCoastalDiagnostic':'coastal-clearance-diagnostic.json / not a successful movement test'}
write(D/'technical-qa.json',q)
records=[]
for p in sorted(S.rglob('*')):
 if p.is_file()and not p.name.endswith('-before-ground.png'):records.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
write(D/'asset-provenance.json',{'authority':'docs/current/G3D_WORLD_RECOVERY_AUTHORIZATION.md','approvedStyleSources':'KOREAN_ARENA_ART_DIRECTION_BIBLE.md','authoring':'Built-in host imagegen only; no external paid provider API called. Exact prompts/reference paths retained. Rejected trials preserved, not automatically approved.','derivation':'Native integer crop/ownership/registration, native approved fine-wave water reuse, lossless PNG only. No artwork resizing, sharpening, global recoloring or approved-source edits.','assetSources':records,'integration':'assets-src/gate3/recovery-world-v1/integration-provenance.json','nativeAssets':'assets-src/gate3/recovery-world-v1/native-assets.json','protectedRegistry':'assets-src/gate3/recovery-world-v1/protected-lock.json','originalArtwork':'Read-only /1440 protected hashes verified','physicalDevices':'NOT TESTED'})
video={}
for name in ['world-traversal.webm','world-traversal-native-resolution.mp4','world-traversal-review.mp4']:
 p=D/name;info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate:format=duration,size','-of','json',str(p)]));video[name]={'bytes':p.stat().st_size,'sha256':sha(p),'probe':info,'published':name.endswith('.mp4')}
write(D/'video-provenance.json',{'source':'Real Playwright screen recording of continuous WASD/Shift movement with original Juni and actual Phaser collision. No teleport/pose animation/concept-image substitution.','master':'Original WebM retained locally; published MP4s are viewing encodes.','nativeResolutionCopy':'1280x1000,12fps H264, no spatial resize; not pixel-exact evidence due video compression.','lightReviewCopy':'512x400,8fps nearest-neighbor review resize, H264. Native PNGs remain the pixel-quality proof.','evidence':video})
core=[('palace','01 Palace'),('academy','02 Academy'),('culture','03 Cultural courtyard'),('transition','04 Heritage threshold'),('retail','05 Modern retail'),('station','06 Railway'),('namsan','07 Namsan'),('amusement','08 Amusement'),('market','09 Harbor'),('jeju-culture','10 Jeju')]
md='''# G3-D consolidated visual review

**Final artistic/spatial acceptance is pending.** The shared direction is conditionally approved; Bakery, tower/road projection, station strip, inherited routes and hardware/device requirements remain open. [QA / remaining decisions](README.md) · [Coverage](COVERAGE.md) · [Technical report](technical-qa.json) · [Physical-device handoff](DEVICE_REVIEW.md).

The playable ZIP includes the whole review world, ten untouched native PNGs and lightweight actual gameplay. The HTML gallery is available inside the ZIP; this Markdown gallery is directly viewable on GitHub without deploying a website.

## Updated Phaser overview

![Actual Phaser overview, scaled; waypoint markers and follow-view outline visible](world-overview-preview.jpg)

Overview is a scaled proxy rendered by actual Phaser, with built-in wayfinding overlays; it is not native-pixel evidence.

## Native Muneum comparison

[![Muneum and recovered environments at identical native crop scale](muneum-benchmark-preview.jpg)](muneum-native-benchmark-board.png)

Each art cell is an unscaled384×300 crop. Original Muneum screenshot and crop coordinates are recorded in [derivative provenance](review-derivatives.json). No board or metric grants artistic approval.

## Ten-region before / after

JPEG previews are under1MB each. BEFORE is the preserved three-pilot world context. Click native PNG/crop links for original1:1 pixels; previews and compressed video do not establish pixel fidelity.
'''
for key,title in core:
 md+=f'\n### {title}\n\n| Before | After |\n|---|---|\n| ![Before]({key}-before-preview.jpg) | ![After]({key}-after-preview.jpg) |\n\n[Before native PNG]({key}-before-native.png) · [After native PNG]({key}-after-native.png) · [Before unscaled crop]({key}-before-crop-1x.png) · [After unscaled crop]({key}-after-crop-1x.png)\n'
md+='''
## Actual movement and supporting native evidence

[Lightweight actual17-leg gameplay](world-traversal-review.mp4) · [Native-resolution1280×1000 viewing encode](world-traversal-native-resolution.mp4) · [Movement data](movement-report.json).

[Juni visible behind bookshop](bookshop-occlusion-after-native.png) · [Protected Maru](maru-after-native.png) · [Original canopy/platform surroundings](platform-after-native.png) · [Closed8px strip overlay](station-collision-overlay-native.png) · [Native compact ferry hall](ferry-after-native.png) · [Jeju arrival](jeju-arrival-after-native.png) · [Original oreum](jeju-oreum-after-native.png).

[Exact projection findings](projection-report.json) distinguish the cleared station façade from95 remaining carousel pixels over its lower-road edge and the new road-apron projections. [Navigation](navigation-report.json) retains six planned-line failures and the body-clearance limits. Source hashes, historical tags, forecourt and original Juni remain protected. No complete-world acceptance, main merge, public deployment or physical-device PASS is claimed.
'''
(D/'VISUAL_REVIEW.md').write_text(md)
write(D/'DEVICE_REPORT_TEMPLATE.json',{'checkpoint':'checkpoint/g3d-world-recovery-review-20261023','deviceModel':None,'OS':None,'browserVersion':None,'UTC':None,'physicalDevice':None,'sessionExportFile':None,'screenRecordingFile':None,'testDurationMinutes':None,'checks':{key:'NOT TESTED'for key in ['pixelStability','joystickIsolation','walkingCollision','bookshopVisibility','tourPauseSkipReturn','reducedMotion','chunkLoading','thermalMemoryStability','hardwareCadence']},'humanReviewer':None,'overall':'NOT TESTED / no automatic PASS'})
print('Final reports:',q['checks'],'cache peak',q['managedCache']['peakLogicalBytes'])
