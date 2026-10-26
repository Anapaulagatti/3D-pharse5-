# Focused QA — motion candidate

| Item | Result | Evidence / limit |
|---|---|---|
| Front walk mapping | PASS, technical | Juni walk-front indices0–7 directly key all three new clips; explicit sole/hand/body landmarks, including integer0–2px lateral body shift from reference silhouette centroids |
| Back walk mapping | PASS, technical | Independent walk-back source indices0–7, not mirrored front poses |
| Front run mapping | PASS, technical | Independent run-front indices0–7 including large down/up body displacement and tucked flight poses |
| Back run mapping | PASS, technical | Independent run-back indices0–7 and source support/flight asymmetry |
| Real distinct corrected frames | PASS |8 per clip ×4 clips ×3 characters =96; no duplicated frames |
| Own identity / original source preservation | PASS, technical |559 tracked source/runtime files exact; original PNG parts supply all character colors/details; no Juni costume/face pixels |
| Other animations | PASS |80 other frame rectangles per character unchanged, including both side gaits, idle, starts/stops, turns/emotes; atlas JSON and selection preview unchanged |
| Juni / world / runtime / UI | PASS |224 Juni and3,082 protected world/core hashes unchanged; source/runtime byte comparison unchanged |
| Actual native integration | PASS |16 real POST_RENDER readbacks:0 unexplained opaque-sprite pixel differences, integer camera, zoom1, nearest layers |
| Actual movement | PASS, technical |All8 phases observed by real WASD/Shift input for16 character/clip combinations at existing60/100 speed. No teleport, frame forcing or controller changes |
| Build / preservation checks | PASS |Production build, typecheck and existing asset checks pass |
| Unit tests | PASS |50/50 |
| Character selection / browser regression | PASS |8/8 existing production character E2E tests pass, including all three native packs, persistence and emulated mobile joystick |
| Artistic contact / shoe roll / loop quality | PENDING HUMAN REVIEW |The pose landmarks are matched; projected own limbs, shoe silhouettes and accessory behavior still require visual judgment at gameplay speed. Pixel equality is not motion approval |
| Earlier Forge near/far classification WARNs | RETAINED |The earlier11 automatic side-view ambiguity warnings are not claimed resolved by this front/back-only correction; side art remains exact |
| Physical Android/iPhone / hardware WebGL performance | NOT TESTED |Desktop Chromium Canvas captures and browser regression establish no physical-device acceptance |

Source recipe and tool: `assets-src/characters/phase1b-frontback-juni/juni-motion-template.json`, `tools/phase1b-frontback-juni/restore.py`. These use nearest-neighbor offline articulated PNG layers. Own body/head pixels are translated, not repainted or scaled. Limbs adapt connected joints to own clothing; no claim of pixel-identical anatomical silhouettes. Earlier sources/atlas checkpoint remain recoverable at `checkpoint/phase1b-roster-review-20261026`.

Reference support/flight labels describe the source as observed, rather than imposing a generic evenly spaced gait. Native1× PNGs are authoritative pixel evidence. Source APNGs are100ms review playback. MP4s are native-scale vertical crops from actual browser recordings, retaining the entire900px canvas height to avoid cutting moving feet, with normal lossy video encoding; they are not pixel-readback evidence. Full original recordings remain alongside local evidence as `*-actual-phaser.webm`.

No world, NPC, camera, collision, controls, selection flow or Phase2 feature was changed. Human motion acceptance remains pending. Stop for review; no main merge/deployment.

The extracted portable package was additionally tested through real selection, movement, reload and emulated mobile touch, with0 missing resources/page errors: [package smoke](package-smoke.json).
