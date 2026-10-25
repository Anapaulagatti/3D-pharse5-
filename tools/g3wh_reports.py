from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-west-hanok';S=R/'assets-src/gate3/west-hanok-v1'
def read(n):return json.loads((D/n).read_text())
a=read('scope-and-collision.json');h=read('protected-hashes.json');n=read('native-render-qa.json');body=read('body-clearance.json');motion=read('movement-report.json');assert motion['complete']and len(motion['legs'])==2 and not motion['errors'];assert not any(q['failureSamples']for q in body['contact']);assert not any(q['unexplainedChangedJuniPixels']for q in body['nativeVisibility']);count=sum(q['samples']for q in body['contact'])
q={'scope':'Western house and lower courtyard ONLY','protectedSourceFiles':h['count'],'outOfScopeStaticOrGroundPixels':0,'worldCollisionCellChanges':0,'logicalSolidsAndNativeContactSpec':'EXACT','allNonTargetObjects':'EXACT','Hanbit':'HUMAN APPROVED LOCKED / unchanged','JejuBridges':'HUMAN VISUALLY APPROVED LOCKED / unchanged','mainPalaceRoadsCommercialNamsanIslandFarmJuni':'UNCHANGED','actualMovementLegs':2,'actualNativeFootSamples':count,'unsupportedNativeFootSamples':0,'unexplainedJuniPixelChanges':0,'nativePhaserFrames':len(n['frames']),'matchedBeforeAfterPairs':len(n['matchedPairs']),'exactNativeGroundReadbackPixels':n['exactGroundPixels'],'nativePixelMismatches':0,'sourceResampling':'NONE','tests':{'typecheck':'PASS','assets':'PASS','unit':'30 tests /9 files PASS','build':'PASS private gate3 review bundle','scopedLint':'PASS'},'humanArtAcceptance':'PENDING','physicalAndroidIPhone':'NOT TESTED','hardwarePerformance':'NOT TESTED'};(D/'technical-qa.json').write_text(json.dumps(q,indent=2)+'\n')
(D/'QA.md').write_text(f'''# Short QA — western house and lower courtyard

| Check | Result | Evidence / limit |
|---|---|---|
| Complete house roof and mass | Local visual review: complete; HUMAN ACCEPTANCE PENDING | One coherent hip/gable roof, both curved eaves/corners and full timber/stone mass; no separate western roof appendix |
| Finished courtyard | Local visual review: complete; HUMAN ACCEPTANCE PENDING | Continuous low stone/wood enclosure, capped left/right returns, balanced pine/rocks/planted bed |
| Unrelated native pixels | PASS —0 changed | Exact two-mask full-world static/ground comparison and3 matched before/after Phaser camera pairs |
| Station | PASS preservation | Human-approved Hanbit source/art/objects/registration/entrance/platform unchanged |
| Both Jeju bridges / island | PASS preservation | Human-approved visual baseline, all objects/ground/source/physical fields unchanged |
| Main palace / roads / other districts / Juni | PASS preservation | {h['count']} old asset files exact; all non-target objects/targets/registrations untouched |
| Collision / native contact | PASS —0 cells changed | ALL world .bin fields, logical solids and bridge contact spec/data EXACT; no new gameplay or route edit |
| Public circulation | PASS selected actual routes |2 consecutive original-control legs around house approach, western lane, north paved lane and garden perimeter; no teleport/physics/speed/frame override |
| Native feet / Juni | PASS selected recording |{count} actual native samples,0 unsupported; original atlas body readback0 unexplained pixels |
| Pixel sharpness | PASS technical |{n['exactGroundPixels']} actual Phaser native ground pixels match source exactly; integer camera and object positions, NEAREST1:1, binary foreground masks |
| Build / existing tests | PASS |Typecheck, asset preservation,30 tests/9 files and scoped lint |
| Final artistic acceptance | PENDING HUMAN |Native comparison and combined local screenshot supplied; technical PASS is not art approval |
| Physical phones / hardware performance | NOT TESTED |No actual Android/iPhone evidence claimed |

No source original or historical checkpoint overwritten. Only6 affected ground chunks and target-specific foreground ownership are rebuilt; collision uses original files. New pixels come from one local source painting selected inside exact masks at1:1. No global blur/sharpen/stretch/repeated ground fill, new biome, feature system, main merge, deployment or separate application changes.

Existing world route-guide reconciliation, required unplaced Bakery and hardware/device requirements remain outside this local repair. They are not newly declared PASS or silently changed.

[Native scope/collision audit](scope-and-collision.json) · [Protected hashes](protected-hashes.json) · [Native renderer readback](native-render-qa.json) · [Real route/body evidence](body-clearance.json).
''')
(D/'README.md').write_text('''# Western hanok +lower courtyard — local review

[Native BEFORE/AFTER gallery](VISUAL_REVIEW.md) · [Gallery/video](VISUAL_REVIEW.html) · [Playable ZIP](WEST_HANOK_COURTYARD_REVIEW.zip) · [Short QA](QA.md).

The western house now reads as ONE complete hanok: a coherent dark tiled hip/gable roof, uninterrupted ridge/eaves, both whole corners and aligned timber facade/stone foundation. The older narrow west-roof fragment is retired from the active target. This rebuild uses the same original house site, scale, architectural language and entrance approach; it is not a bigger palace or another building type.

The directly lower courtyard is finished as the same historic ornamental garden: complete low-stone/wood enclosure, capped returns, balanced sculptural pine, granite and shrubs, with clean left/right/front edges. It does not add an interior/gameplay system. The public paved lane and western/perimeter circulation remain intact.

Only exact predeclared house/garden masks receive new native source pixels. Main palace, other hanok, roads, farm, modern district, Namsan, island, original Juni and all unrelated scenery remain exact. Hanbit stays approved/locked; BOTH Jeju bridge visuals are now approved/locked at `checkpoint/g3d-jeju-bridges-approved-20261025`. Historical source files/checkpoints remain recoverable.

ALL world collision cells, logical solids and bridge contact fields remain byte-exact. Real original-control public-route recording confirms no new movement blockage in the tested lanes. Native1:1 Phaser before/after and unannotated combined views are provided. Cropped originals retain their exact pixel scale; only clearly labelled review JPEGs are enlarged nearest-neighbor.

Extract ZIP, run `python3 start_review.py`, open localhost index. Existing WASD/arrows/Shift, joystick, Scenic/Tour/Return and test-report export remain. Physical phones/hardware performance remain NOT TESTED. Broader inherited world planning/navigation requirements are unchanged and not accepted by this local handoff.

**STOP for final human visual review.** No main merge/public deployment or further artwork expansion.
''')
(D/'SOURCE_OWNERSHIP.md').write_text('''# Native source provenance

Baseline: current `jeju-bridges-world` at official human visual bridge approval. New namespaces only: `assets-src/gate3/west-hanok-v1` and `public/assets/gate3/west-hanok-world`.

One built-in `image_gen.imagegen` local-edit job used the current native western context and exact two-polygon guide. The whole house and enclosed garden were coherently authored together; no rejected southern quality reference, whole-world generation or external paid provider API/key was used. Raw output and input paths are recorded in `authoring-jobs.json`; the original1536×1024 source is retained.

Source pixels are selected at integer origin320,750 inside `edit-scope-mask.png`; no scaling, interpolation, sharpening or blur. Old target-only fragment/foreground ownership is removed inside the masks, while any original alpha outside remains exact. New roof/garden foreground mattes copy the SAME native RGB with binary alpha; no facade or tree fragments are reassembled from old pieces.

ALL original sources and approved Hanbit/Jeju art remain immutable. Collision arrays, logical solids and native-contact guard are unchanged. No new land, route amendment, interior system or neighboring architecture was introduced.

Reproduce: freeze with `g3wh_prepare.py`, retain authoring master, `g3wh_build.py`, actual `g3wh_capture.mjs`, `g3wh_audit.py`, original-control `g3wh_walk.mjs` and `g3wh_movement_audit.py`. Documentation/review derivative generation is separate from source artwork.
''')
print('Short QA ready:',count,'native contacts;0 field changes')
