# Phase3A QA

Current full final regression: **PASS**. Final report counters: `{"startTime": "2026-10-27T16:07:51.719Z", "duration": 972990.1390000001, "expected": 60, "skipped": 0, "unexpected": 0, "flaky": 0}`. Do not treat a running validation as PASS. Human artistic/linguistic acceptance remains pending.

| Area | Status | Evidence / scope |
|---|---|---|
| Accepted Phase2C pre-implementation baseline |PASS|116unit/53E2E,all required commands;baseline-logs |
| Typecheck/assets/lint/format |PASS|npm run typecheck/assets:check/lint/format:check |
| Unit |PASS recorded|131tests including15NPC cases; no skips |
| Full E2E |PASS|60tests: original53 plus7NPC/cross-zone/re-entry cases |
| Build/portable build |PASS|Actual existing Phaser4.2.1 bootstrap |
| NPC source art/animation |PASS technical|14identities/7zones/1456cells/448walkframes;8distinct/direction;native raster stance≤1px |
| Pilot before expansion |PASS technical|4actual contexts,20native readbacks,realinteraction/4directions |
| Final native actual renders |PASS technical|84captures,0unexplained opaque-pixel mismatch |
| Canonical navigation/clearances |PASS scope|14routes/approaches;criticaldoors/bridges/docks/plotsclear |
| Actual all14 approaches/dialogue/return |PASS scope|Original controls in canonical scene;not graybox |
| Cross-zone exploration |PASS scope|One uninterrupted mainland→northern Jeju bridgeA→orchard→house traversal |
| Re-entry/dialogue stability |PASS observed|12realcycles/60dialogues,reload,oneplayer,boundedNPCownership |
| Real visited/progress preservation |PASS scope|Actual palace discovery→NPCdialogue→reload;external learning account NOT integrated |
| Mobile landscape browser |PASS functional|667×375/844×390,Korean/Vietnamese,44px controls,joystick return |
| SoftwareWebGL |PASS smoke|2actual native readbacks,nearest;not hardware performance |
| World/characters/cosmetics/Studio |PASS hashes|6382frozenfiles;scene outside6additive hooks byte-identical |
| Independent ZIP |PASS technical|CRC/SHA; separately extracted runtime,all14NPC dialogues,all12curated looks,save/reset/reload and actual touch movement |
| NPC artistic/linguistic acceptance |PENDING HUMAN|No automatic art approval |
| Physical Android/iPhone/hardwareGPU/thermal |NOT TESTED|No unsupported device PASS |
| Historical technical/motion warnings |WARN retained|Earlier approved-baseline reports remain untouched |

The first expanded full suite had59PASS/1FAIL in the new cross-zone QA harness. The path hugged original collision boundaries and used insufficient control alignment. The harness now uses the exact existing walking-contact offsets,clearance-weighted verified paths and original analog fine alignment. No collision/scenery/speed override fixed the test. Subsequent full regression and actual traversal are recorded separately; tests were not skipped or removed.

Final visual inspection also corrected two coastal NPC standing positions onto existing paved public surfaces. All14actual native captures/navigation checks were regenerated after that adjustment. Scoped dialogue classes removed inherited HUD pointer interference; safe-area insets prevent asymmetric-notch positioning errors. Physical notch/device acceptance remains untested.

[Source QA](source-qa.json) · [navigation](navigation-qa.json) · [native readbacks](gameplay/native-pixel-qa.json) · [stability](stability.json) · [extra/mobile/WebGL/realvisited](extra-evidence.json) · [protected audit](protected-audit.json) · [device workflow](DEVICE_REVIEW.md).

No farming/shops/crafting/inventory/rewards/quizzes/economy/account synchronization,paid AI/image APIs,Phase3B,main merge or deployment. Existing unrelated world planning/performance issues are retained,not silently repaired or certified by this NPC phase.

Final scope: full60test regression passed with0skips/0flaky. Two subsequent QA-only approach-spawn amendments placed coastal review starts on coherent public routes; the independent bridge recording now starts at the existing approved `bridge-a-mainland` entry. Runtime art/game rules were unchanged. A fresh build and all7NPC browser cases passed again after those amendments. [Final7report](final-focused/e2e-results.json),[full60report](e2e/e2e-results.json),[logs](logs/full-60-e2e.log).

Independent artifact: [NPCsmoke](package-npcs-smoke.json),[12characters/Studio/persistence/touch](package-characters-smoke.json),[device export](device-export-smoke.json),[ZIP CRC/SHA inventory](package-proof.json),[source provenance](source-provenance.json). Large native scenes and full cross-zone/stability videos remain available at the immutable tag even where the compact ZIP links online.
