# Phase2C QA

TECHNICAL PASS — ARTISTIC APPROVAL PENDING. Final full E2E status: PASS; actual report counters `{"startTime": "2026-10-27T11:11:17.977Z", "duration": 629122.409, "expected": 53, "skipped": 0, "unexpected": 0, "flaky": 0}`. The full rerun completed with no skipped or flaky tests.

| Area | Result | Evidence / limit |
|---|---|---|
| Typecheck |PASS| npm run typecheck |
| Asset preservation/validation |PASS| npm run assets:check; protected audit5453files |
| Lint /format |PASS| npm run lint /npm run format:check |
| Unit |PASS|116tests /17files,0skipped |
| Full E2E |PASS|53tests, original suites plus7new Phase2C cases |
| Production /portable build |PASS|npm run build; separate relative-base Vite artifact |
| Original10 foundation |PASS technical|196 actual native captures,0mismatch |
| New pilot |PASS technical|28 actual clips,0mismatch |
| Final all12 looks/defaults |PASS technical|192 native captures,0mismatch |
| Catalog and exhaustive source composition |PASS technical|28items /46variants /5248registeredcells;192looks /21760frames |
| Actual WebGL native readback |PASS software smoke|SwiftShader; not hardware performance |
| Long session |PASS observed|60actualswitches,100preview/apply,one sprite,bounded caches |
| Persistence /migration /reset /cancel |PASS|v1/v2 readable,local presets+world/visited/progress retained |
| Mobile landscape browser |PASS layout/input|667×375,844×390; native preview+touch isolation |
| Independent ZIP |PASS|CRC/SHA,12curatedlooks,presets/reload/reset,touch movement and native readback0mismatch |
| Native art and animation aesthetics |PENDING human|No technical result grants artistic approval |
| Android Chrome /iPhone Safari physical |NOT TESTED|No recorded physical-device evidence |
| GPU/thermal/sustained mobile memory |NOT TESTED|No hardware certification |
| Historical Forge motion warnings |WARN retained|Earlier Phase2A/B reports not rewritten or weakened |

The first full E2E run was52PASS/1FAIL: a missing-texture test waited for an optimistic selected button after the app had already correctly recovered defaults. The test was corrected to assert recovered default selection, one player, unchanged position and original atlas; final complete suite rerun is recorded separately. No retry/skip hides that failure. See logs/e2e-first-run.log and final logs.

[Source QA](source-qa.json) · [protected](protected-audit.json) · [foundation](foundation-gate.json) · [pixel readbacks](gameplay/native-pixel-qa.json) · [UI geometry](ui-probe.json) · [long session](long-session.json) · [WebGL](webgl-evidence.json) · [performance](PERFORMANCE.md) · [device workflow](DEVICE_REVIEW.md).

All12 approved base assets, animations, world/collision/controller/camera/tour remain immutable. Bakery and earlier world planning/performance decisions are not resolved or altered by this character-only phase. No economy, NPC, quest, learning integration, paid API, Phase3, main merge or public deployment.
