from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';S=R/'assets-src/gate3/final-surgical-v1'
def rd(p):return json.loads((R/p).read_text())
move=rd('docs/gate3-final/movement-report.json');body=rd('docs/gate3-final/body-clearance.json');scope=rd('docs/gate3-final/out-of-scope-audit.json');native=rd('docs/gate3-final/native-render-qa.json');collision=rd('docs/gate3-final/collision-runtime.json');nav=rd('docs/gate3-final/navigation-report.json');prior=rd('docs/gate3-residual/navigation-report.json')
assert move['complete'] and len(move['legs'])==7 and not move['errors'];assert not collision['errors'];assert len(body['nativeVisibility'])>=23 and sum(r['unexplainedChangedJuniPixels']for r in body['nativeVisibility'])==0
assert [(r['id'],r['blockedCenterSamples'])for r in nav['routes']]==[(r['id'],r['blockedCenterSamples'])for r in prior['routes']]
failPose=[p for p in body['capturedPoseContact']if p['status']=='FAIL'];failSamples={l['id']:l['contactFailureSamples']for r in body['controlReports']for l in r['legs']if l['nativeContactSamples']};counts={r['scene']:r for r in scope['reports']}
qa={'scope':'PASS /0 unexpected native-world and matched Phaser pixels','protectedSourceAssets':2870,'nativePhaserFrames':len(native['frames']),'matchedNativePairs':len(native['pairs']),'eligibleGroundPixels':native['eligiblePixels'],'groundMismatchPixels':0,'actualMovementCases':move['legs'],'actualCapturedPoseCount':len(body['capturedPoseContact']),'actualCapturedPoseFailures':len(failPose),'bridgeMotionSampleFailures':failSamples,'unexplainedJuniPixelChanges':0,'sourceScale':'Native1:1 / no source resampling','mainCanonicalStation':'Retained exact','stationCandidate':'PENDING HUMAN / isolated, not adopted','farm':'Six plot reservations/anchors/states; actual aisle walk and all6 interaction/soil collisions validated; no farming system','stationPlatformTransfer':'FAIL /8px strip still blocks real input','fullRouteNetwork':'FAIL /7 inherited centerlines unchanged','bridgeCompletePoseContact':'FAIL / measured25px/4866px2 proposal remains unadopted','physicalDevices':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED','artAcceptance':'PENDING HUMAN','tests':{'typecheck':'PASS','assets:check':'PASS','vitest':'30 tests /9 files PASS','vite':'PASS','scopedLint':'PASS'},'initialHarnessFailure':'Native photo mode hides joystick; first movement harness attempt retained, corrected by using ordinary original gameplay UI. No game/control/collision/clock override.','recordingEnvironment':'Linux Chromium1280x1000 hasTouch, DPR1, real original WASD +native pointer joystick; system/usr/bin/ffmpeg via private/tmp/g3ds-browser-cache/ffmpeg-1013, PLAYWRIGHT_BROWSERS_PATH=/tmp/g3ds-browser-cache. Not physical device evidence.'}
(D/'technical-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
(D/'QA.md').write_text(f'''# Surgical technical and visual QA

[Whole-native-world scope](out-of-scope-audit.json) · [Actual Phaser readback](native-render-qa.json) · [Controls](movement-report.json) · [Native body/contact](body-clearance.json) · [Runtime collision](collision-runtime.json) · [Protected hashes](protected-hashes.json).

| Check | PASS / FAIL / NOT TESTED | Limit |
|---|---|---|
| Exact authorized bounds | PASS |0 out-of-scope ground, foreground/static or field pixels at4352×4864; region max-area guards enforced |
| Actual native Phaser fidelity | PASS |{len(native['frames'])} native frames /{len(native['pairs'])} matched pairs;{native['eligiblePixels']:,} eligible source-ground pixels,0 mismatches; same camera/pose; nearest/native integer placement |
| Historical source preservation | PASS |All2,870 baseline assets exact; plans, Juni, historical checkpoints/source art immutable |
| Canonical station frontage | PASS |Main and isolated new-station static composition at2274,2603,684,210 exactly matches baseline; planters/canopy/tree/shadows unchanged |
| Western house completion | PASS local observed repair / human review pending |Missing left roof/eave continued; source facade/door/stairs/native position retained, proper local foreground roof owner |
| Courtyard | PASS local observed enclosure / human review pending |Narrow western stone/fence return; original garden/pine/fixtures core preserved; new25×22 support foot and existing western path validated |
| Farm spatial readiness | PASS |6×180×128 plot reservations, native soil/crop/interaction/state metadata; all6 anchors walkable/all6 soil centers blocked in live Phaser; actual aisle loop PASS |
| Farming game system | NOT IMPLEMENTED, as instructed |No inventory/economy/timer/quest/crop-state implementation |
| Canonical station asphalt phase | PENDING protected material decision |Protected floor stays exact, including historical asphalt phase; prior native-road candidate remains unadopted. New architecture alone does not approve district seamlessness |
| New station architecture integration | PENDING / not adopted |Independent roof/upper/facade, architecture-free ground stage, native registration, unchanged collision; relative artistic superiority requires human comparison |
| Actual regional movement | PASS selected cases |7 real-input cases: farm, house, courtyard, new entrance, crosswalk, complete bridge outward/return. Declared scene starts; no in-movement teleport or speed/frame/collision override |
| Native Juni visibility | PASS source readback |23 recorded frames,0 unexplained changed Juni pixels. Expected roof/rail/garden foreground occlusion explicitly accounted for |
| Full native bridge contact | FAIL |Movement trace sampled failures {failSamples};{len(failPose)}/{len(body['capturedPoseContact'])} genuinely captured stop/turn poses have unsupported contact. A zero sampled return count does NOT prove return-pose clearance |
| Structural bridge proposal | NOT ADOPTED |Prior bounded25px/4866px² visible support, same unchanged physical field; no invisible land, endpoint change or Juni shrink |
| Station platform transfer | FAIL |Actual held A stops at nativeX2958;8px strip unchanged; no90×36 connector |
| Full approved circulation | FAIL, inherited |7 planned centerlines retain EXACT same blocked counts as residual baseline. New farm/garden collision does not add failures to those approved routes |
| Coast/road contact materials | PASS bounded source handling / human review pending |Small mainland water/asphalt native masks; preserved curbs/shore/Jeju. Not a claim that every offshore boundary is artistically seamless |
| Palace/retail/island-landing minor inspection | UNCHANGED after inspection |No independent evidence requiring another modification; no unrelated repaint |
| Build/typecheck/assets/unit regression | PASS |30 tests/9 files; does not approve art |
| Physical Android Chrome / iPhone Safari | NOT TESTED |Emulated touch, software/browser WebGL and builds cannot certify real phones |
| Hardware WebGL performance | NOT TESTED |Browser update intervals are not certified hardware/presentation FPS |
| Final full-world artistic acceptance | PENDING HUMAN |Mandatory unplaced Bakery and P1 spatial/navigation/device issues remain |

Main scene changes{counts['final-world']['staticPixelsChanged']:,} static pixels ({counts['final-world']['unchangedStaticPercent']}% native composition unchanged); isolated new-station candidate changes{counts['final-station-candidate']['staticPixelsChanged']:,} ({counts['final-station-candidate']['unchangedStaticPercent']}% unchanged). These percentages are consequences of exact masks, not permission to edit an arbitrary percentage.

## Retained failed attempt / reproduction

[Initial movement harness report](movement-initial-native-ui-harness-failure.json) is retained. It used native PHOTO framing, where UI deliberately hides the joystick. The harness was corrected to use normal existing gameplay UI; original game controls/collision stayed unchanged. Final7-case report/video are a fresh completed recording. No failed game movement is silently counted as a successful run.

Source reproduction: full repository checkout; `python3 tools/g3ds_build.py`, `python3 tools/g3ds_audit.py`, local Vite build/server, capture/native audit, real-control recorder and movement audit. Browser recording requires Playwright FFmpeg; this workspace uses `/usr/bin/ffmpeg` symlinked at `/tmp/g3ds-browser-cache/ffmpeg-1013/ffmpeg-linux` and `PLAYWRIGHT_BROWSERS_PATH=/tmp/g3ds-browser-cache`. Runtime playback does not need these authoring tools. Raw WebM is locally preserved; MP4 is lossy movement evidence, untouched native PNGs prove pixel quality.

No screenshot request/dependency, main merge, public deployment, new paid external image API, separate-app changes or full-world regeneration.
''')
(D/'COVERAGE.md').write_text('''# Ten existing regions / surgical coverage

| Region | This pass | Remaining |
|---|---|---|
|Historic palace|Royal hall/axis/walls pixel-identical; inspected existing finishing|Human acceptance/archival corridor decision |
|Western academy/hanok|Missing house left-roof continuation +narrow garden west return|Human native architectural review |
|Archive/culture|Unchanged|20px public corridor unaccepted;88px gate separate |
|Historic-modern threshold|Unchanged|Inherited route network findings |
|Modern commercial|All cafe/bookshop/learning art/scale/registrations unchanged|Tower projection remains |
|Hanbit railway|OLD main exact; NEW isolated roof/upper/facade candidate and architecture-free ground stage|Human replacement decision;8px transfer closed |
|Namsan/Maru|Unchanged|Tower/retail projection remains |
|Amusement|Unchanged|Carousel/station projection remains |
|Waterfront/harbor|Only actual1664 asphalt material join and tiny mainland landing water mask|Bakery required/unplaced,W0 rejected,Q1 unallocated; broader offshore review not claimed |
|Jeju|Canonical island/nearshore/house/orchard/oreum/internal paths/endpoints exact|Full bridge stop/turn contact FAIL; support proposal unadopted |

Local farm is only the existing NW woodland envelope west of palace wall1107; it is not a new region or land allocation. Six gameplay-ready metadata plots; no farming system. All other composition outside REGION_TARGETS remains pixel-identical, not merely visually similar. Physical devices/hardware WebGL NOT TESTED.
''')
print('QA reports:7 movement PASS; bridge contact FAIL,',len(failPose),'actual pose failures; no artistic self-approval')
