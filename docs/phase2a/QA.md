# Phase2A review QA

| Check | Result | Evidence |
|---|---|---|
| Permanent approved4 baseline | PASS |51ac4b4; approval tag and SHA manifest preserve all original art/configs/previews/layers/tools |
| World/collision/camera/controller preservation | PASS |3,082 protected world/core and224 Juni hashes exact;6,868,992 paired native world pixels,0 changes |
| Default appearance preservation | PASS |Four original actual Phaser native body readbacks exact; unit identity/clip/motion-step assertions |
| Ara and Doyun | PASS, review candidate |Own host-image identities,112 native slots each,64 distinct gait poses,34clips; Ara validated before Doyun production |
| Cosmetic catalog | PASS, review candidate |2hair +2outfits each for2 identities,2accessories; every supported frame registered |
| Pair ownership / alpha / registration | PASS |36combinations ×112poses =4,032 direct-source matches; binary native masks and integer rectangles |
| Actual gameplay/native fidelity | PASS |85 native readbacks with0 unexplained opaque-pixel mismatch;48 actual gait cycles each show all8frames; emotes/idle/directions also observed |
| Studio/persistence/v1/state retention | PASS |Actual UI selection/save/reset/reload; real visited landmark and position retained; synthetic lesson sentinel unchanged |
| Resource ownership | PASS, bounded observations |One sprite,3actor textures,2base/2composite caches;24switch observations and48switch stability run |
| Build/typecheck/assets/lint/unit | PASS |68unit tests; original validation commands pass |
| Full E2E | PASS |32tests:21 canonical production/Studio and11 retained historical V10 checks; historical results are not canonical ferry/gameplay/art approval |
| Landscape/orientation regression | PASS, Chromium emulation |Additional targeted rotation test;844×390 and667×375 browser images/geometry |
| Forge numerical diagnostics | WARN retained |0hardFAIL,6new side-leg heuristic WARNs; [verbatim warnings](FORGE_WARNINGS.md).11 earlier approved Phase1B warnings retained |
| Final new-art acceptance | NOT TESTED / awaiting human |Original4 are human-approved; new2/cosmetics await Phase2A artistic acceptance |
| Physical Android Chrome / iPhone Safari | NOT TESTED |No physical evidence recorded |
| Hardware WebGL/FPS/thermal/device memory | NOT TESTED |SwiftShader render smoke and desktop estimates only |
| Canonical interiors | NOT TESTED / unsupported |The frozen canonical world has no interior transition; no invented interior test PASS |

Existing world/planning issues remain separate and unchanged: Bakery allocation remains deferred (W0 rejected/Q1 not approved); inherited station strip/route failures and station/amusement conflict remain recorded in historical world reviews. No world rebuild or planning amendment is performed here. Automatic build/geometry tests are not human artistic approval.

Phase2A is delivered as a playable review candidate. No remaining new Phase2A P1 functional defect is known from this scope. Retained P2/review items:6automatic profile-motion WARNs, full Korean/English localization review, physical notch/keyboard/mobile memory and sustained performance. Do not treat these as completed device acceptance.

No Phase2B, main merge, public deployment, paid external media API or separate Korean-learning website changes.
