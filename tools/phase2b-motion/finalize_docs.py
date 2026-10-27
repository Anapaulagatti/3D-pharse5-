from pathlib import Path
import json,collections
D=Path('docs/phase2b-motion');q=json.loads((D/'recovery-validation.json').read_text());assert all(r['exit']==0 for r in q)
e2e=D/'recovery-e2e/e2e-results.json';stats=json.loads(e2e.read_text())['stats']if e2e.exists()else None
if stats:assert stats['expected']==46 and stats['unexpected']==0 and stats['skipped']==0,stats
f=json.loads((D/'forge-diagnostics.json').read_text());warn=collections.Counter(x['check']['id']for x in f['warnings']);assert not f['hardFailures']
s='''# Motion recovery — technical QA

**Human motion acceptance PENDING. Phase2C LOCKED.** Recovered source commit `d988e12accfdc5a71212e88cabe4f77b0af69481`; no animation production repeated. The previous client execution transport failed; retained processes completed E2E46/46. The underlying infrastructure cause is unproven. No dependency, lockfile or application-code repair was necessary.

| Verification | Status | Evidence / limitations |
|---|---|---|
| Recovered source/checkpoint | PASS |d988e12 and checkpoint/phase2b-motion-source-20261027 present; before checkpoint and original rejected review preserved |
| Typecheck/assets/lint/format/build | PASS |Fresh recovery commands all exit0; see logs below. Standard asset validation retains legacyV10 checks; canonical checks supplied independently |
| Unit tests | PASS |93/93, including source-level foot raster matching and exact atlas scope preservation |
'''
s+='| Full E2E | '+('PASS |Fresh46/46;35 current/foundation/character/Studio cases and11 retained historicalV10 cases. V10 is not canonical-world artistic evidence |\n'if stats else'RUNNING |Previous completed46/46 retained; fresh recovery run underway |\n')
s+='''| Native Phaser readbacks | PASS |Reproduced1,008 opaque-pixel comparisons from retained actual Phaser PNGs:0 mismatch; nearest sampling, integer camera,zoom1 |
| Genuine runtime motion | PASS technical / visual review pending |42 actual clips (Juni +6 actors),126 sampled consecutive loops, real WASD/Shift at60/100speed; rightward positiveX, stop/turn and Studio entry captured |
| Source right support trajectory | PASS supplementary |Old source drift34px walk/48px run; repaired raster keyposes≤1px. Actual native phase-sample support drift1–8px; eight-pose hold quantization remains, not continuous subpixel foot lock |
| Front/rear walk and relevant runs | WARN human review |Own-material knee/foot-view correction uses Juni's actual indices, not vertical mirroring. Three consecutive loops per clip supplied; naturalness/weight/occlusion/closure await human review |
| Repair scope | PASS |402 files:6 atlas PNG +396 motion frame PNG.66 cells/actor (48 gait +18 start/stop),46 unchanged cells/actor. All left,idle,emotes exact. Head/hair top45RGBA rows exact in gait cells |
| Approved six and cosmetics | PASS |1,340 approved-six files,224 Juni files,57 runtime-file hashes +definition snapshots unchanged |
| World/collision/controller/camera/UI/progress | PASS |3,082 historical protected files +256 canonical dependencies exact; all src files identical to before motion repair |
| Native registration and clip semantics | PASS |96×112,anchor48,100;60/100speed,44/64stride; atlasJSON,clip order,timing,registration and default appearance unchanged |
| Original Forge | WARN |72 commands,0 hardFAIL;17 current leafWARNs (8leg alternation,6run-right phase coverage,3seam). Original18 Phase2B and17 earlier warnings retained; thresholds not weakened.48 each palette/outline/L-corner gates SKIPPED without required inputs |
| Portable runtime/media | See package proof |All12 actual atlases in ZIP compared byte-for-byte to recovered working files;6 Juni comparisons +6 actual gameplay recordings. Packaged recordings use lighter compression only; dimensions/frame counts/timing preserved |
| Physical Android/iPhone | NOT TESTED |Landscape/touch browser regression is emulation, not physical-device acceptance |
| Hardware WebGL/performance | NOT TESTED |Desktop/softwareWebGL regressions and Canvas capture are not real-device hardware certification |
| Human artistic motion approval | PENDING |Numerical PASS is not motion acceptance; review all six comparisons and raw-speed gameplay |

## Direct evidence

- [Native/gameplay gallery](REVIEW.html) and [full visual index](VISUAL_REVIEW.md).
- [Frame-change manifest](frame-change-manifest.json), [before5,302-file freeze](before-manifest.json), [protected-hash audit](protected-audit.json).
- [Reproduced1,008 readbacks](readbacks-juni-sori-jiwon-nari-taeyang-yuna-hyunwoo.json), [actual motion/contact QA](actual-motion-qa.json), [source foot raster tracks](directional-pixel-qa.json).
- [Diagnosis](MOTION_DIAGNOSIS.md), [source provenance](source-provenance.json), [video probe](video-probe.json), [portable video encoding provenance](packaged-video-provenance.json).
- [Fresh command results](recovery-validation.json), [previous completed E2E summary](interrupted-session-e2e-summary.json), [recovery infrastructure findings](RECOVERY.json).
- [Forge diagnostics](forge-diagnostics.json), [verbatim currentWARNs](FORGE_WARNINGS.md), [retained original18WARNs](../phase2b/forge-warnings.json). Eight unique poses alone never establish artistic quality; prior acceptance inference is withdrawn.

## Fresh command logs

'''
for name in ['typecheck','assets-check','lint','format-check','test','build']:s+=f'- [{name}](recovery-logs/{name}.log)\n'
if stats:s+='- [Full E2E log](recovery-logs/e2e.log) and [machine-readable report](recovery-e2e/e2e-results.json).\n'
s+='''
## Extracted ZIP validation

All12 identities,4 existing cosmetic presets, real progress/reload and mobile-landscape joystick passed from an independent local HTTP server serving the extracted archive. The six corrected characters also traversed positiveX for more than3 strides; six extra native readbacks matched atlas pixels exactly. See [package smoke](package-smoke.json) and [package native checks](package-native-readbacks.json).

The initial smoke helper read the previous frame's diagnostic snapshot immediately after Studio closed. Its identity assertion failed (retained [diagnostic](package-smoke-failure.json)); source inspection confirms the snapshot updates during the Phaser frame, after the async selection handler. The helper now waits for the requested character and exact preset outfit before performing unchanged position/single-sprite assertions. No application code or validator threshold changed.

## Remaining limits

Human review must judge forward-step perception, front/rear knee and arm coordination, garment/foot occlusion, loop closure and sliding at normal speed. Source geometry/contact checks supplement the videos; they do not grant art approval. Runs were repaired because the same construction defects were confirmed; all left clips remain untouched.

The6 run-right phase-coverage WARNs explicitly report no flight frame in either sampled half-cycle. This is an unresolved running-quality limitation of the recovered candidate, not a numerical PASS or a warning to erase. No re-authoring is performed during recovery; review these six run clips before acceptance.

No world/planning defect, Bakery allocation or station issue was changed. No new character, cosmetic, UI, engine, progress, quest, shop or learning-site feature was created. No main merge, force push or public deployment.

Review checkpoint: `checkpoint/phase2b-motion-corrected-review-20261027`. Original Phase2A approval, twelve-character rejected-motion review and before/source checkpoints remain recoverable. Exact final commit and remote verification are recorded in the delivery receipt. STOP for human artistic approval.
'''
(D/'QA.md').write_text(s)
print('QA', '46fresh E2E PASS'if stats else'fresh E2E pending',warn)
