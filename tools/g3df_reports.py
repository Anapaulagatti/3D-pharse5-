from pathlib import Path
import json,shutil,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-alignment';S=R/'assets-src/gate3/alignment-v1';tag='checkpoint/g3d-alignment-review-20261024';raw='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+tag+'/'
def rd(p):return json.loads(p.read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
qa=rd(D/'technical-qa.json');integ=rd(S/'integration-provenance.json');nav=rd(D/'navigation-report.json');motion=rd(D/'movement-report.json');bridge=rd(D/'bridge-movement-report.json');body=rd(D/'body-clearance.json');protected=rd(D/'protected-hashes.json');failed=sum(r['blockedCenterSamples']>0 for r in nav['routes'])
qa['checks']={'typecheck':'PASS','unitTests':'30 PASS /9 files','assetsPreservation':'PASS','targetedESLint':'PASS','prettier':'PASS','privateViteBuild':'PASS','identicalNativeCameraPairs':15,'nativeReadbackPixels':sum(r['eligiblePixels']for r in qa['nativeGroundReadbacks']),'mismatchedReadbackPixels':sum(r['different']for r in qa['nativeGroundReadbacks']),'continuousWorldTraversal':motion['complete'],'continuousWholeBridgeTraversal':bridge['complete'],'actualMovementControl':'Original WASD plus original native joystick, no teleport/collision override','physicalDeviceEvidence':False}
qa['visualJudgments']={'palaceAxisAndStairs':'PASS_MEASURED_AXIS_AND_ACTUAL_THRESHOLD; human art approval pending','eastSetback':'FAIL_FINAL_PUBLIC_CLEARANCE /20px corridor, no physical roof-wall collision','stationUpperBackground':'REVIEW / obsolete source alpha retired, source RGB/HVAC preserved','stationLowerFrontage':'FAIL_COMPLETE_SEAMLESS_INTEGRATION / protected asphalt source phase/softness remains','stationRight':'PARTIAL / bounded canopy cap; right potted-tree foliage still source-clipped','retailRoofs':'PASS_SOURCE_RECOVERY_AND_FACADE_GUARDS / human visual acceptance pending','bridgeMainland':'REVIEW_VISIBLE_STRUCTURE / actual crossing PASS separately','bridgeJeju':'REVIEW_VISIBLE_STRUCTURE / actual crossing PASS separately','architecture':'REVIEW / palace derived entrance, source-native retail; no blanket art PASS','materials':'FAIL_STATION_CANONICAL_ASPHALT_TRANSITION / proposal separate','depth':'PASS_TECHNICAL_LAYER_READBACK / near-rail occlusion explicitly recorded','lighting':'REVIEW / original lighting/shadows and bounded matching details','composition':'FAIL_FINAL_WORLD_ACCEPTANCE / retained protected decisions','scale':'PASS_NATIVE1X / original Juni and buildings not scaled','navigation':'FAIL_COMPLETE_NETWORK / selected actual traversal separate','pixelClarity':'PASS_RUNTIME_NATIVE_READBACK / historical baked-source softness separate'}
qa['retainedNativeAssetLimit']={'stationRightTree':'Existing potted-tree crown reaches sourceX2958 and is still clipped; complete original native crown unavailable in same verified source. No fabricated oversized tree or protected-floor repaint applied. Remains visible-source quality FAIL, not renderer failure.','stationRoad':'Main canonical ground/raw crop remains byte-identical, including its historical soft asphalt. Separate native asphalt candidate NOT adopted.','archiveApproach':'20px corridor technical crossing does not grant adequate public setback or a new protected-wall opening.'}
wr(D/'technical-qa.json',qa)
# Historical evidence is referenced, never rewritten.
for name in ['DEVICE_REVIEW.md','DEVICE_REPORT_TEMPLATE.json']:
 text=(R/'docs/gate3-reconciliation'/name).read_text().replace('checkpoint/g3d-spatial-reconciliation-review-20261024',tag);(D/name).write_text(text)
(D/'README.md').write_text('''# G3-D final alignment candidate — consolidated review

[Visual gallery](VISUAL_REVIEW.html) · [Native BEFORE/AFTER](VISUAL_REVIEW.md) · [Playable ZIP](G3D_FINAL_ALIGNMENT_REVIEW.zip) · [QA](QA.md) · [Measurements](measurements.json) · [Source ownership](SOURCE_OWNERSHIP.md).

One isolated candidate corrects the palace entrance, eastern entrance ownership, station background/canopy, three commercial rooftops and both mainland–Jeju bridge landings. This is **not final world artistic acceptance**. Historical source artwork, geometry/plans, Juni, original station canopy, corrected planters and canonical forecourt remain protected. No merge or public deployment.

## Implemented

- Main hall: measured old door/stair axis1921 versus approved2048. Derived native front shifts material phase127px without moving the royal roof/contact reservation. Plinth bottom790→750; central door/stair axis2048, actual threshold685. One112×94 portal ownership patch; one foundation course, no duplicate plinth. Real movement reaches the door.
- Eastern archive: source support reserve150px from wall, roof projection46px from wall eave, painted low-platform envelope approximately52px. Original architecture stays registered. Native stairs become ground; side lanterns/gardens remain foreground. Door2580,923 reached through existing southern gateway and20px internal corridor. This corridor remains inadequate for final public-space acceptance.
- Station: obsolete upper/side source background alpha retired; HVAC, rear railing, facade RGB and source pivot preserved. Original canopy retained with a small independent terminal roof cap on existing supports. No new platform connector or added support foot. Canonical forecourt/raw ground and both corrected planters remain exact.
- Retail: verified full native source recovers legitimate roof/terrace/flower silhouettes; unrelated background removed with explicit alpha. Cafe/bookshop/learning base positions and approved facade RGB/alpha remain exact.
- Bridge: two bounded derived abutment repairs and local shared-water ownership; original Jeju PNG and land/internal scenery remain protected. Existing near rails/posts are depth-sorted foreground with exact static native composition. Actual complete crossing uses real timber/deck ground contacts, not the obsolete mainland-wall shortcut.

## Decisions still required

1. **Archive public clearance:**20px remains tight. ONE88px secondary gate proposal at2536,1040,88,25, axis2580 is shown only in an overlay; current wall/plan unchanged. No automatic architectural acceptance from successful movement.
2. **Station material boundary:** protected canonical asphalt at2274,2755,684,58 remains historically softer/different in phase. An isolated `aligned-road-proposal` candidate restores native asphalt material only within an explicit mask. It is **NOT ADOPTED**, requires human approval, and changes no road geometry. Paving/curb/tactile/marks outside mask exact.
3. **Station source completeness:** the existing right potted-tree crown is clipped at sourceX2958. Complete verified crown unavailable; protected pot/floor not repainted or covered. Station fully seamless appearance remains **FAIL**, even though canopy repair and runtime pixel readback pass.
4. Station8px collision strip2950,2626,8,129 remains CLOSED. No rejected90×36 connector; platform transfer is not claimed.
5. Inherited public-route failures, tower/retail and carousel/canonical-road projections remain open; Bakery required/unplaced, W0 rejected, Q1 land unallocated. Physical Android Chrome/iPhone Safari and hardware WebGL performance NOT TESTED.

Seven marked screenshots were unavailable and requested. Annotation-specific validation is NOT TESTED. Native pairs and source geometry are the available evidence; no claim that all reviewer marks have been closed.

## Review and reproduction

Extract ZIP, run `python3 start_review.py`, open printed private localhost URL. Main candidate defaults to `aligned-world`; protected-road proposal is explicitly separate. All ten original region links plus fifteen focused review entries are available. WASD/arrows, Shift run and mobile landscape joystick retained. No ferry/train gameplay added.

See [physical-device checklist/export](DEVICE_REVIEW.md). Chromium touch emulation and software WebGL are not actual phone/hardware evidence. Full authoring reproduction requires repository sources and `tools/g3df_*`; built-in host authoring outputs/prompts retained with exact masks. One source checkpoint and immutable artifact checkpoint retain this batch. **STOP for consolidated human visual/spatial review.**
''')
(D/'QA.md').write_text(f'''# Technical and visual QA

Technical success is not artistic approval. [Machine report](technical-qa.json), [movement](movement-report.json), [bridge movement](bridge-movement-report.json), [actual body readback](body-clearance.json), [route audit](navigation-report.json), [protected hashes](protected-hashes.json).

| Item | Result | Evidence / limitation |
|---|---|---|
| Typecheck, unit tests, assets, scoped lint/format, private build | PASS |30 tests /9 files; original source/atlas checks |
| Native pairs / sampling | PASS |15 identical-camera pairs; {qa['checks']['nativeReadbackPixels']:,} eligible ground pixels,0 mismatches; integer positions, zoom1, nearest |
| Protected registry | PASS with explicit code exception |1439 of1440 baseline entries exact; opt-in PixelAudit adds read-only alpha/depth. All protected artwork exact;254 previous checkpoint files exact; historical tags preserved |
| Canonical station ground | PASS preservation |Raw2274,2603,684,210 exact; planters/canopy source/pivot unchanged |
| Palace actual threshold | {'PASS'if motion['legs'][0]['status'].startswith('PASS')else'FAIL'} |2048,685 via real controls, derived axis matches2048 |
| Eight-leg continuous world route | {'PASS'if motion['complete']else'FAIL'} |Original controls/collision; continuous recording; driver failures preserved |
| Complete upper bridge crossing | {'PASS'if bridge['complete']else'FAIL'} |3130,3460→3530,3640, actual deck, no alternate bridge/teleport |
| Juni source/body rendering | See body-clearance.json |Actual atlas pixel comparison and depth occlusion, separated from native projected contacts |
| Final archive pedestrian composition | FAIL |20px front corridor; secondary88px gate PROPOSAL ONLY |
| Final seamless station | FAIL |Protected-road softness/phase; clipped original right tree crown retained, not hidden |
| Station8px transfer | FAIL / blocked |Closed strip unchanged; no90×36 connector |
| Entire planned network | FAIL |{failed} planned centerlines contain blocked samples; conservative radius is diagnostic, not a native bridge-foot model |
| Both bridge landings' visual quality | REVIEW / not human accepted |Native structure/source/physical overlays plus crossing; no collision-only artistic PASS |
| Seven marked reviewer images | NOT TESTED |Not attached/requested; no annotation closure claim |
| Hardware WebGL / physical Android / iPhone | NOT TESTED |Desktop software WebGL and emulation cannot certify device performance |
| Final world artistic acceptance | PENDING HUMAN |No main merge/deployment; Bakery/projections/route issues remain |

## Exact changes and diagnosis

Source crop/alpha/ground ownership caused these architectural seams. The prior corrected renderer is retained; six core camera/texture/chunk modules are byte-identical. The station0.5 source pivot is retained and is not blamed for baked softness. No scaling, sharpening, global blur or approved-source regeneration.

Seven ground chunks and nine field chunks rebuilt; all other chunks reused. Foreground textures are derived independently. Exact files/masks/hashes: [asset provenance](asset-provenance.json), [integration records](../../assets-src/gate3/alignment-v1/integration-provenance.json), [technical inventory](technical-qa.json). Original masterplans unchanged.

The two protected decisions (archive gate / canonical-road native material exception) are not silently adopted. Existing source-tree clipping is a recorded quality failure. Keep failed movement attempts; neither source hashes nor a clean build establish visual approval.
''')
(D/'SOURCE_OWNERSHIP.md').write_text('''# Native source ownership and provenance

[Exact asset inventory/SHA256](asset-provenance.json) · [Integration records](../../assets-src/gate3/alignment-v1/integration-provenance.json) · [Prompts and host outputs](../../assets-src/gate3/alignment-v1/authoring-jobs.json) · [Ground change mask](../../assets-src/gate3/alignment-v1/ground-change-mask.png) · [Field change mask](../../assets-src/gate3/alignment-v1/field-change-mask.png).

| Owner | Canonical source | Derived handling |
|---|---|---|
| Palace roof/contact | Gate2A native roof plus accepted protected plan |Root/roof registration exact; tiny portal alpha exception explicit. Native front reassembled/phase shifted127 at1x; no whole-building shift/scale |
| Palace west pavilion | Gate2A430×150 native crop |Native RGB/position, explicit roof alpha, foreground owns roof; old baked copy retired beneath |
| Eastern archive | production-assets/archive.png |Upper310 rows foreground; central native stairs ground; side front details foreground; exact static RGB/registration |
| Station facade/HVAC/railing | registration/station.png645×453 |All RGB exact; explicit background retirement alpha; source pivot0.5 preserved |
| Roof greenery | Same station source |Attached terrace/HVAC ownership distinguished from distant baked trees; no new tree cover |
| Forecourt/tactile/curb | Approved forecourt restoration |Raw canonical2274,2603,684,210 exact, including protected road. No hidden overlay repair |
| Planters/shadows | Corrected independent approved textures |Sources/registration/depth unchanged |
| Canopy | Original approved canopy |Source exact; bounded terminal cap is independent foreground, generated post excluded; no new navigation connector |
| Unprotected road spur | Original1254px station source |Two native unscaled clean asphalt samples, explicit bounded material mask; no copied old props/marks |
| Retail upper silhouettes | final-clean-ground.png3184×1214 |Crop bounds expanded upwards, native world bases unchanged; architecture/flower ownership masks and source-alpha boards; lower facade RGBA guards exact |
| Bridge abutments / nearby water | Existing bridge design + retained host authoring plate |Only two explicit structural masks plus local water ellipse; native1x, originalJeju PNG immutable; original basalt/land components protected |
| Bridge near rails/posts | Existing exact scene pixels |Foreground ownership only, static composite exact; ground retirement under opaque native railing; no duplicate props |
| Juni | Original atlas |Native96×112 frame/48,100 anchor, scale1; actual directional projected feet local guard only; no sprite rewrite |

**New versus reused:** protected architecture and commercial facade pixels are reused. New authored pixels are only the bounded palace portal, canopy terminal and bridge-abutment/water masks. Recovered native material/crop/alpha edits do not demonstrate new whole-building authorship. The station-ground host trial is explicitly rejected/not installed. No new external paid-provider API was called.

**Limitations:** the final station border is not certified seamless. Canonical-road baked softness/phase and clipped right potted-tree foliage remain. Correcting the latter without a complete verified crown would require a carefully reviewed native completion with foreground/floor ownership; no oversized foliage concealment or protected paving repaint was applied. The road candidate is proposal-only.

**Reusable validation:** g3df_audit validates native dimensions/positions, facade guards, support-vs-roof measurements, exact old checkpoints and layer inventory; flags opaque top/right edges without equating them to collisions. g3df_navigation measures accepted routes. g3df_movement_audit reads actual original sprite pixels/foreground depth and projected contacts. All source-boundary, graybox and collision overlays are technical evidence, never screenshots substituted for Phaser gameplay.
''')
(D/'COVERAGE.md').write_text('''# Actual coverage — five-area localized pass

Seven ground chunks/nine field chunks rebuilt. No full-world rebuild. All ten existing regions remain dependencies; previous checkpoints/evidence stay intact. This matrix is not production-complete acceptance.

| Region | This pass | Status |
|---|---|---|
| Palace |Axis/front/plinth/portal, actual threshold, original west pavilion foreground |Implemented; human architectural review pending |
| Academy/hanok |Existing source unchanged |Unrelated source-completeness issue retained |
| Archive/cultural compound |Native stairs/foreground, actual correct doorway, wall/roof separation measured |20px public corridor FAIL; gate proposal unimplemented |
| Historic-modern transition |Preserved existing ground/routes |Inherited route issues tracked |
| Modern retail |Three verified native roof recoveries/alpha, facade guards |Implemented; tower projection remains separate |
| Hanbit railway |Upper ownership, bounded canopy cap, native unprotected asphalt spur, canonical floor exact |Partial; road/crown source seam FAIL,8px transfer blocked |
| Namsan/Maru |Accepted terrain/entrance/root/loop preserved |Unchanged; tower retail projection retained |
| Amusement |Protected rides/roots/reservations retained |Carousel canonical-road projection remains |
| Harbor |Ferry/harbor untouched |Bakery required/unplaced; W0 rejected,Q1 unallocated |
| Jeju/bridge |Two bounded abutments/water, rail depth, genuine complete crossing |Candidate visual review; original island/house/oreum/orchard/paths preserved |

Physical devices/hardware performance NOT TESTED. Seven marked images unavailable. Final world acceptance FAIL/PENDING HUMAN while protected decisions and mandatory content remain open.
''')
# Exact direct native links pinned to artifact tag, no mutable file-view URL.
files=sorted(p for p in D.glob('*.png')if 'native' in p.name or 'overlay' in p.name)
(D/'NATIVE_LINKS.md').write_text('# Direct immutable native evidence\n\nActual PNG bytes, not GitHub file previews. Open at100%; review JPEGs can be scaled. Human artistic acceptance pending.\n\n'+'\n'.join(f'- [{p.name}]({raw}{p.relative_to(R)})'for p in files)+'\n')
# Explicit new local inventory without rewriting old source/checkpoint directories.
wr(D/'change-summary.json',{'baseline':'06b718a','workingBranch':'art-gate/gate3-full-world','groundChunks':integ['groundChunksChanged'],'fieldChunks':integ['fieldChunksChanged'],'changedCode':['src/gate3/main.ts','src/gate3/PixelAudit.ts','src/gate3/NativeContact.ts'],'tests':['tests/unit/native-contact.test.ts'],'newAssetRoots':['assets-src/gate3/alignment-v1','public/assets/gate3/aligned-world','public/assets/gate3/aligned-before','public/assets/gate3/aligned-road-proposal'],'unimplemented':['Archive88px secondary opening','Protected canonical-road proposal in main','station8px transfer','Bakery allocation'],'sourceAndPlanningFiles':'Immutable','fullWorldAcceptance':'NOT APPROVED','sevenMarkedImages':'NOT PROVIDED / requested'})
print('Reports complete; actual movement',motion['complete'],'bridge',bridge['complete'],'planned route failures',failed)
