from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-residual';S=R/'assets-src/gate3/residual-v1';TAG='checkpoint/g3d-residual-review-20261025';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
def rd(p):return json.loads(p.read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
qa=rd(D/'technical-qa.json');movement=rd(D/'movement-report.json');body=rd(D/'body-clearance.json');gate=rd(D/'gate-movement.json');proposal=rd(D/'bridge-clearance-proposal.json');reg=rd(S/'integration-provenance.json');water=rd(S/'ocean-material-registry.json');nav=rd(D/'navigation-report.json');failures={l['id']:l['contactFailureSamples']for r in body['controlReports']for l in r['legs']if l['contactFailureSamples']};pixels=sum(r['eligiblePixels']for r in qa['nativeGroundReadback']);assert movement['complete']and len(movement['legs'])==9;assert all(r['result']=='PASS_EXPECTED_BEHAVIOR'for r in gate['rows']);assert sum(r['unexplainedChangedJuniPixels']for r in body['nativeVisibility'])==0
qa['validation']={'typecheck':'PASS','unitTests':'30 PASS /9 files','actorAndSourceChecks':'PASS','privateViteBuild':'PASS','scopedESLintPrettier':'PASS','nativeMatchedPairs':20,'nativeGroundPixels':pixels,'groundReadbackMismatches':0,'continuousActualLegs':9,'actualBridgeOutAndBack':'PASS_LOCOMOTION_ONLY','capturedRealStopTurnPoses':len(movement['poseShots']),'spriteReadbackFrames':len(body['nativeVisibility']),'unexplainedChangedJuniPixels':0,'allPosePhysicalContacts':'FAIL / protected current geometry','contactFailureSamples':failures,'gatewayAndStripActualBehavior':'PASS_EXPECTED_BEHAVIOR / gate only proposal, strip remains blocked','sixReviewerImages':'NOT PROVIDED / NOT TESTED','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED'}
qa['visualClassification']={'palace':'IMPLEMENTED / actual axis and central rails exact; native apron and misplaced corner ownership corrected, human composition approval pending','stationRearAndCrown':'IMPLEMENTED / native completion and source-alpha decomposition; no canonical frontage pixel change, human art approval pending','stationRoad':'PROPOSAL ONLY / canonical main road retained, no silent replacement','commercial':'IMPLEMENTED / source-only edge retirement, original facade RGB/roof geometry retained; human visual review pending','bridgeLandings':'VISUAL CANDIDATE / improved source art preserved; water source seams corrected; current full native support FAIL, exact proposal separate','southernCoast':'IMPLEMENTED / one existing shared-water family wrap repaired using original texels; actual land/foam/Jeju protection preserved','entireWorld':'NOT ACCEPTED / mandatory content and P1 decisions remain'};qa['waterSourceProof']={'periodPhase':'UNCHANGED1536x1024 /3180,3200','newColorsOrInterpolation':'NONE / exact original integer texel origin map','oldWrapEdgeMeanDelta':water['oldEdgeMeanRGBDelta'],'newWrapEdgeMeanDelta':water['newEdgeMeanRGBDelta'],'broaderCanonicalWaterTrial':'REJECTED / NOT INSTALLED'};wr(D/'technical-qa.json',qa)
for n in ['DEVICE_REVIEW.md','DEVICE_REPORT_TEMPLATE.json']:
 text=(R/'docs/gate3-alignment'/n).read_text().replace('checkpoint/g3d-alignment-review-20261024',TAG);(D/n).write_text(text)
(D/'README.md').write_text('''# G3-D consolidated residual correction — human review candidate

[Native before/after gallery](VISUAL_REVIEW.md) · [Complete gallery/poses/video](VISUAL_REVIEW.html) · [Playable ZIP](G3D_RESIDUAL_REVIEW.zip) · [QA](QA.md) · [Source ownership](SOURCE_OWNERSHIP.md).

Review baseline9827761, metadata2eb4d29. **Final artistic acceptance remains withheld.** This is one coordinated residual batch, not a world reconstruction or new district production. Main plans, source originals, original Juni, existing registrations/collision, protected roof/forecourt/planters/Jeju and historical checkpoints remain preserved. No main merge or public deployment.

## Implemented corrections

- Palace: royal hall stays fixed, door/stair axis2048 and threshold685 exact. Central stone rails/treads/portal/roof remain unchanged. A misplaced source-side return balustrade leaking into a timber bay is retired using native reference pixels. A tightly masked native stone apron repairs the stair-foot/foundation/court transition; no hall shift or new monument.
- Station: obsolete source-side/rear/floor alpha is retired while authentic roof-attached greenery/HVAC, facade RGB, rear rail, native canopy metal roof and post/sign are preserved. Existing potted tree is extracted from duplicated source ownership; only its missing crown outside2958 receives authored pixels. Pot/trunk/native tree/forecourt static composition remain exact. Original station0.5 source-pivot convention is unchanged and is not blamed for blur.
- Retail: cafe background/vertical planting strip and roof-background remnants separated from genuine balcony flowers, lamp and entrance pot. Bookshop/learning obsolete background tips retire through explicit alpha; facade RGB/signage/windows/doors and true roof geometry remain native and unchanged. No new building authored or facade regeneration.
- Bridge/shared water: previously improved stone abutments/endpoints/native scale and foreground rails remain. The main recurring water line was the nonperiodic wrap of the already shared ocean source. Native minimum-error overlap ownership repairs that material, keeps period/phase exact and propagates only to already-owned shared-water wrap bands. Every repaired material pixel maps to an exact original texel. All original Jeju protection bitmap pixels, rock/foam/land, house, oreum/orchard/internal paths and source PNG remain exact. A broader water-mask trial was rejected/not installed.
- Southern waterfront: long source-water plate retires to the same shared native phase. Promenade, retaining/basalt edge, pier, ferry, foam/physical contacts and mainland footprint remain. All49 changed ground chunks are affected local corrections or shared offshore wrap propagation; land districts are not rebuilt.

## Three explicit review decisions — not adopted

1. **Station road:** isolated `residual-road-proposal` uses the existing native restoration proposal at2274,2755,684,58. Main canonical road remains unchanged. Native CURRENT/PROPOSED include both detail and full station precinct. Curb, crosswalk/tactile geometry, architecture and collision unchanged.
2. **Archive88px secondary gateway:** isolated `residual-gate-proposal` shows support opening2536,1040,88,25 and its49px roof-course projection. Current wall blocks real keyboard movement; the hypothetical opening reaches actual threshold2580,923. Main wall/field unchanged. Existing20px corridor is NOT final accepted public clearance. Gate end-cap detailing, public-space composition and cultural-roof projection remain human review matters; movement success is not architectural approval.
3. **Bridge full movement-pose clearance:** main walking route works both directions, but physical contact remains FAIL for native stop/turn poses. Strict source-anchor treatment preserves below-anchor toes instead of normalizing them upward. The separately measured conservative proposal needs at most25px shoulder within the bounded search,4866px² of visible support across three areas:30×27 at3128,3523;201×48 at3201,3539;90×31 at3344,3614. This is a floor-contact model, not a globally minimal engineering design or approved artwork. Support/rail/shore detailing must be visibly authored and reviewed before any live collision enlargement. Endpoints/source design/Juni remain fixed; no invisible land or live widening.

Station8px strip2950,2626,8,129 remains CLOSED; no rejected90×36 connector. Bakery required/unplaced,W0 rejected,Q1 unallocated. Inherited route failures/tower-retail and carousel-station projections remain separate. Hardware WebGL and physical Android Chrome/iPhone Safari NOT TESTED.

Six reviewer screenshots were not attached and were requested. Annotation-specific closure is NOT TESTED. Available source/native evidence, not unseen markings, guides this batch.

## Review package

Extract completely, run `python3 start_review.py`, open the private localhost URL. Main residual candidate plus three explicitly labelled proposal links. Original desktop WASD/arrows/Shift and mobile landscape joystick/Scenic/Tour/Return remain. No actual phone PASS inferred from Chromium emulation. [Device checklist/report export](DEVICE_REVIEW.md).

The ZIP contains gameplay and lightweight review copies; extra untouched native originals/full source masters resolve to the immutable review tag. Source reproduction needs the full repository, retained host authoring outputs and `tools/g3de_*`. Production builder imports only `g3de_ocean_wrap.py`; `g3de_water_family.py` is a rejected diagnostic trial. **STOP for one consolidated human artistic/spatial review.**
''')
(D/'QA.md').write_text(f'''# Residual technical, collision and artistic QA

[Machine technical report](technical-qa.json) · [Native matched gallery](VISUAL_REVIEW.md) · [Actual movement](movement-report.json) · [Body/foot evidence](body-clearance.json) · [Protected hashes](protected-hashes.json).

| Item | Classification | Evidence / limits |
|---|---|---|
| Build/typecheck/assets/unit checks | PASS |30 tests /9 files; does not approve art |
| Native matching / renderer fidelity | PASS |20 identical-camera pairs;{pixels:,} eligible pixels,0 mismatches; nearest native scale/integer camera; six renderer core modules exact |
| Original source/checkpoint protection | PASS with read-only diagnostic exception |1439/1440 library entries exact; PixelAudit adds opt-in pose observation only.242 previous alignment files exact; old tags preserved |
| Station canonical frontage/planters | PASS |Original file immutable; actual Phaser foreground comparison pixel exact excluding animated Juni. Only old baked-tree pixels retire beneath identical foreground. Main road/tactile/curb/crosswalk/shadows preserved |
| Station crown/alpha | PASS measured clipping/ownership criteria |New bounded crown, binary alpha; original pot/trunk/native source RGB exact. Human craftsmanship approval pending |
| Original canopy roof/post/HVAC | PASS source guards |Native metal roof/post/sign RGBA and HVAC exact; original registration/pivot/depth. Obsolete side-floor/background ownership retires; no protected platform-support movement |
| Palace axis/actual threshold | PASS |2048,685 reached via genuine controls; central native stairs/rails/portal/roof preserved; finishing remains human visual review |
| Retail original facade/native scale | PASS |All original RGB; structural facade RGBA guards. Cafe wide prior guard included nonarchitectural background, now explicitly separated |
| Continuous route / bridge locomotion | PASS selected movement |9 actual legs, complete mainland→Jeju→mainland; no teleport/collision/clock override |
| Captured stop/turn source pixels | PASS rendering only |12 genuine POST_RENDER poses both directions;25 native frames,0 unexplained changed Juni pixels. Expected foreground occlusion recorded separately |
| Full native current bridge contact | FAIL |{failures}; physical model retains actual below-anchor toes. Previous13/6 baseline used older normalized contact sampling; source atlas/game unchanged |
| Bridge structural-clearance proposal | PASS geometry model only / NOT ADOPTED |25px maximum bounded shoulder search,4866 visible-support pixels; actual current field unchanged. Railing/support architecture still requires review/production if authorized |
| Current archive public clearance | FAIL final acceptance |20px corridor not accepted as final; separate88px gate only |
| Current wall / hypothetical gate behavior | PASS expected engineering comparison |Current native wall blocks; proposal real movement reaches door. That is not final visual/public acceptance |
| Station platform transfer | FAIL / still blocked |Real input stops at rendered pixel2958;8px field closed. Simulation float2957.8015 correctly rounds to2958; raw initial float-threshold assertion retained |
| Main canonical road integration | FAIL pending decision |Original protected asphalt phase/softness retained. Isolated native road candidate shown, not silently applied |
| Full approved route network | FAIL |{sum(r['blockedCenterSamples']>0 for r in nav['routes'])} inherited planned centerlines still contain blocked samples; geometry-only diagnostics separate from actual selected route |
| Six marked reviewer images | NOT TESTED |Not supplied/requested; no claim that all exact marks were closed |
| Hardware WebGL / physical Android/iPhone | NOT TESTED |Desktop WebGL/Chromium touch emulation do not certify hardware/device performance |
| Final full-world artistic acceptance | FAIL / human decision withheld |Observable repairs delivered; mandatory Bakery, spatial/P1/device decisions remain |

## Source-fidelity findings

The residuals were source ownership/crop/material-wrap issues. The already corrected renderer remains unchanged; no half-pixel renderer diagnosis is reopened. Original0.5 station source-pivot convention retained. There is no global sharpening, blur, recolor, stretch or fractional resampling.

The shared ocean used the same1536×1024 source on both sides of the visible3180 line, but its opposite edges were not periodic. Minimum-error native overlap cuts preserve global period/phase and every RGBA texel's original integer source coordinate. Edge mean deltas X9.78→4.40,Y10.43→5.65 are technical diagnostics, not artistic approval. The broader physical-water trial was rejected, so the original Jeju protection bitmap remains exact.

Actual route recording uses original WASD plus native joystick fine control and screenshot instrumentation. Recorded duration is not an exploration-pacing or hardware-FPS benchmark. Lossy MP4s prove movement; untouched native PNGs prove pixels.
''')
(D/'SOURCE_OWNERSHIP.md').write_text('''# Exact ownership, source provenance and changed assets

[Exact source/runtime file list/SHA256](asset-provenance.json) · [Integration masks/records](../../assets-src/gate3/residual-v1/integration-provenance.json) · [Host jobs/prompts/original paths](../../assets-src/gate3/residual-v1/authoring-jobs.json) · [Ground changes](../../assets-src/gate3/residual-v1/ground-change-mask.png).

| Component | Native source and derived ownership |
|---|---|
| Palace front |Accepted alignment1010×160 unchanged registration. Only misplaced side return mask replaced with verified native lattice texels. Central rails/treads/portal/roof exact; no hall shift |
| Stair apron |One authored430×85 stone-ground mask below750; no architecture selected. No generic full-court regeneration |
| Cafe |All RGB original. Nonstructural left background alpha retired; real balcony flowers/lamp/entrance planter retained; structural facade guard localX>=38 |
| Bookshop/learning |Original native crop and RGB, true roof shape unchanged; only unrelated rooftop background alpha tips removed |
| Station |Original645×453 RGB and0.5 source convention; real facade/HVAC/railing/roof greenery retained. Source-only side/floor plates retired; original canopy roof/post/sign intact |
| Potted tree |Existing static native tree extracted at2820,2490; ground root2696. Native pot/trunk/crown pixels preserved in explicit mask; only2958..2989 missing crown can use authored output. New completion wins at outside border; retirement mask may include one column outside the original source. Preserved-native mask excludes that border |
| Canonical forecourt |Original file/historical checkpoint immutable. Only previously baked TREE pixels retire under identical native foreground; actual paving/tactile/curb/shadows and static native frontage exact. No full-scene replacement |
| Planters/canopy |Corrected rectangular planter images/shadows and original canopy sources remain hash exact. Derived canopy alpha separates actual roof/post/sign from obsolete source background, side-floor context and tree copy. Approved central tactile strip remains exact |
| Southern shore |One native ocean family/global phase replaces old nonstructural water plate; actual retaining/basalt/foam/promenade/pier/ferry/land unchanged |
| Ocean wrap |Existing1536×1024 source is repaired at its existing X/Y wrap through native overlap ownership. Original material file immutable. Every output RGBA equals an original texel, independently verified by integer origin map. No RGB interpolation, reflection, scaling, sharpening or new underwater rocks |
| Bridge |Improved native abutments/design/endpoints/foreground rails retained. Full-contact footprint proposal is a technical overlay only; live ground/field unchanged |

**New artwork:** only bounded station crown, palace apron and bridge-bay water source masks from retained built-in host outputs. No new external paid-provider API or credentials/integration. Other fixes recover/reassign native source pixels or alpha. Reusing approved architecture is not a claim of authoring new buildings. Broader canonical water-mask expansion was tested as a diagnostic and explicitly rejected/not installed.

**Exact native water derivation:** [material registry/cuts](../../assets-src/gate3/residual-v1/ocean-material-registry.json), [original-coordinate map](../../assets-src/gate3/residual-v1/ocean-native-origin-map.npz), [source edit mask](../../assets-src/gate3/residual-v1/ocean-wrap-source-change-mask.png), [world ownership mask](../../assets-src/gate3/residual-v1/shared-ocean-wrap-world-mask.png). This is an existing water-material edge repair, not a rejected landscape tile or full-world source regeneration.

**Geometry remains protected:** [gate proposal](../../assets-src/gate3/residual-v1/archive-secondary-gate-proposal.json), [road candidate](../../assets-src/gate3/residual-v1/road-proposal-only.json), [strict bridge proposal](bridge-clearance-proposal.json). All clearly separate; no historical plan/file silently edited. All approved source originals/checkpoints remain recoverable.
''')
(D/'COVERAGE.md').write_text('''# Actual localized coverage

This batch modifies local source ownership/ground finishing plus one existing shared offshore material's repeat edges.49 affected ground chunks rebuilt; every main collision chunk/root/plan unchanged. It does not reconstruct ten land districts or allocate new land.

| Existing region | Current batch | Remaining |
|---|---|---|
|Palace|Fixed side-return ownership/native stair apron; accepted axis/roof/threshold preserved|Human composition review |
|Academy/hanok|Structures preserved; shared offshore edge only where already water-owned|Inherited source-completeness issue retained |
|Archive/culture|Geometry preserved; real current approach retained; isolated88px gateway comparison|20px final public clearance FAIL; protected-wall decision |
|Historic-modern threshold|Land/streets/planting retained|Inherited navigation issues |
|Modern commercial|Three alpha-edge cleanups; no facade regeneration|Tower/retail projection separate |
|Hanbit railway|Rear/canopy/tree ownership, missing crown, canonical frontage exact; isolated road candidate|Road acceptance/8px transfer/source-projection decisions |
|Namsan/Maru|Accepted native terrain/root/scenic approach preserved|Tower/retail projection remains |
|Amusement|Attractions/roots/reservations retained|Carousel/station projection remains |
|Harbor/southern coast|Shared shoreline water-family repair; real promenade/ferry/footprint preserved|Bakery required/unplaced;W0 rejected,Q1 unallocated |
|Jeju/bridges|Approved island/nearshore bitmap exact; shared-owned ocean wrap fixed; both-directions actual movement/poses|Current full contact FAIL;25px shoulder proposal not adopted |

Physical Android/iPhone and hardware WebGL NOT TESTED. Six marked images unavailable. No completed asset count/build/source hash constitutes full-world artistic acceptance.
''')
wr(D/'change-summary.json',{'baseline':'9827761 visual /2eb4d29 metadata','branch':'art-gate/gate3-full-world','clientDate':'2026-10-25 Asia/Saigon','groundChunks':reg['groundChunksChanged'],'mainCollisionChanges':0,'sourceOriginals':'EXACT','canonicalStaticAndNativeFrontage':'EXACT','reviewOnlySpawnCorrection':'Old palace-east preview2680,1080 was a blocked review pose. Common BEFORE/AFTER review pose2580,1030 is valid; actual protected public approach/plan unchanged.','unadopted':['Station native asphalt material candidate','88px archive wall opening','25px bounded bridge support/rail/shore correction proposal'],'sixReviewerImages':'NOT PROVIDED / requested','fullWorldAcceptance':'WITHHELD / remaining P1 content/spatial/device items'})
files=sorted(p for p in D.glob('*.png')if 'native'in p.name or 'overlay'in p.name);(D/'NATIVE_LINKS.md').write_text('# Direct immutable native evidence\n\nActual PNG bytes. Open/download at100%. Source/geometry boards explicitly labelled; never substituted for in-engine screenshots.\n\n'+'\n'.join(f'- [{p.name}]({RAW}{p.relative_to(R)})'for p in files)+'\n')
print('Consolidated report:9 real legs,12 poses, native pixels exact; protected decisions/physical failures remain explicit')
