# G3-A foundation review — approval pending

Gate3 is officially authorized. This delivery is its first engine/integration checkpoint; it is not a completed production world. No merge or deployment occurred. G3-B expansion has not begun, as the user's final authority explicitly requires first G3-A evidence review before scaling an unverified pipeline.

## What is playable

A4352×4864 registered foundation with approved historical/Jeju art at native coordinates and clearly visible engineering geometry elsewhere. The unchanged corrected3184×1214 district runs in a separate cache laboratory using exactly the same engine. WASD/arrows, Shift run, E exploration, Space greeting, original Juni motion/atlas, landscape joystick, Follow, Scenic, overview proxy and four-stop Jeju Tour are available. The original approved prototype ZIP is preserved byte-for-byte inside the new package.

The bounded streaming pool reserves decoded RGBA plus collision bytes before requests start, permits2 concurrent resources, deduplicates keys, prefetches384px, pins visible/player dependencies, evicts off-view LRU resources, cancels stale loads, backs off failures and disposes images/textures on eviction/shutdown. An oversized desired set is bounded too, preventing prefetch from continuously evicting itself. Movement sweeps at most1px per substep and rejects unloaded collision/foreground dependencies. It does not teleport Juni to repair loading failures.

Normal cache budget64MiB covers streamed RGBA estimates plus one-byte collision masks, including in-flight reservations. **This is not total process RAM or certified VRAM.** Fixed Juni and overview textures add approximately10.1MB for world review; decoder buffers, browser canvas/GPU copies, JS objects, temporary response buffers and driver allocations add overhead.24MiB is an explicit diagnostic stress profile, not the normal setting. No runtime full-world texture is loaded. Overview is a downsampled planning proxy and must not be used to judge native pixel quality.

## Unresolved registration decision — do not silently move assets

Protected station source origin is(2238.5,2180). Its source origin inside the approved intact district is(2464,267). Registering the whole plate to the protected station implies district origin **(-225.5,1913)**:225.5px outside the western canvas, with a half-pixel phase. This is a source/world registration conflict, not proof that the approved facade should be shrunk or moved.

No amendment has been applied. The production plan records the conflict and the district remains in its original local frame. [Spatial diagram](registration-conflict.png).

Recommended next review: register the approved full-sized buildings individually within their existing world reservations, retain original facade pixels and protected station anchor, and design localized connecting ground in G3-B. This will require a concrete local layout/half-pixel registration proposal; the current continuous district's local spacing cannot also be assumed to be locked world spacing. Alternatives such as expanding the canvas west or shifting the station would amend explicit planning constraints and are not applied here. The0.5px station issue also requires an explicit pixel-phase decision before native world placement.

## Validation judgments

| Item | Result | Scope / evidence |
| --- | --- | --- |
| Approved source/Juni/checkpoints preserved | PASS |1,341 protected hashes; Gate1/Gate2.5/main refs; baseline tag |
| Chunk/native pixel preservation | PASS |111 ground/mask pairs; exact crop reconstruction; integer origins, scale1, nearest sampling |
| Corrected station planters | PASS for technical preservation |Native WebGL readback matches16,530 left and15,770 right pixels exactly. Existing human art approval applies to preserved baseline, not future districts |
| Foreground ownership / root-depth order | PASS for foundation checks |Whole objects retained across boundaries, dependency readiness; native scenes and input evidence. Whole-world occlusion is not yet validated |
| Cache boundedness / eviction | PASS for logical resource budget |24MiB stress:53 evictions,79 loads, peak25,110,344B below25,165,824B; no admission failure or load error; Juni preserved |
| Failure gating / retry | PASS |Injected collision503 blocks movement, then recovery after retry; Canvas fallback also exercised |
| Actual traversal | PASS for two recorded routes |District crosses both art joins and multiple512px boundaries; north exits native art onto planning spine. No QA placement or speed override |
| Static routes | PASS for five sampled paths |8px cardinal search,4px safety inset, each segment checked every1px; not exhaustive whole-world reachability |
| Follow / Scenic / overview / Jeju Tour | PASS for Chromium engineering samples |Two normal tour/return cycles, positions preserved; touch/reduced-motion/control-export checks have separate report |
| Full-world district registration | FAIL / unresolved |Intact district would extend225.5px west; protected station has0.5px phase. No coordinate changes applied |
| Complete production art / scene-to-scene artistic continuity | FAIL / unfinished |World contains explicitly marked engineering geometry and visible plate boundaries. Internal chunk fidelity does not establish artistic seam acceptance |
| Production navigation / all destinations / collision against future art | NOT TESTED |Sampled static paths and2 traversals do not certify finished full-world exploration |
| Sustained60Hz in recorded desktop WebGL emulation | FAIL |Recorded desktop update p95~91.5–99ms, with parallel QA/video overhead; software SwiftShader. No physical/hardware conclusion |
| Isolated renderer sample | MEASURED, not release PASS |WebGL SwiftShader p95~42ms; Canvas p95~17ms. Raw browser update cadence, not presentation FPS or total-memory certification |
| Physical Android Chrome / iPhone Safari | NOT TESTED |Mandatory before final release recommendation |
| Typecheck / lint / formatting / asset checks / unit tests / dedicated build | PASS |23 tests in6 files, including cache lifecycle/cancellation/budget checks |
| Final human G3-A acceptance | NOT TESTED / pending |Build/tests/old art approval do not approve this integration architecture |

Static pacing examples: north→spine768px /12.8s walk; bridge→house1832px /30.5s; oreum→house1624px /27.1s; mainland→boarding2712px /45.2s; district1704px /28.4s. Calculations use original60px/s walk,100px/s run. Actual timings include turns, loading and browser scheduling; static lengths are not measured play durations. Longer mainland routes are planning geometry requiring G3-B/C composition and pacing review, not accepted empty production terrain.

## Reproduce

Node24, `npm ci`; Python3 with Pillow/numpy/scipy; installed Chromium and FFmpeg for captures. Then:

```
python3 tools/gate3_assets.py
npm run typecheck
npm run assets:check
npm run lint
npm run format:check
npm test
npx vite build --config gate3.vite.config.ts
python3 tools/gate3_package.py
python3 -m http.server 4261 --bind 127.0.0.1 --directory dist-gate3
```

In another terminal: `node tools/gate3_capture.mjs`, `python3 tools/gate3_routes.py`, `node tools/gate3_resilience.mjs`, `node tools/gate3_controls.mjs`, `node tools/gate3_bench.mjs`, `python3 tools/gate3_verify.py`, `python3 tools/gate3_boards.py`. Ref verification queries origin/main read-only.

Gameplay recording: `PLAYWRIGHT_BROWSERS_PATH=/tmp/gate3-playwright node tools/gate3_gameplay.mjs`. Install Playwright's FFmpeg in that location, or map the installed compatible `/usr/bin/ffmpeg` to `/tmp/gate3-playwright/ffmpeg-1013/ffmpeg-linux` as used here. Convert the three saved`/tmp/*.webm` recordings to H.264 with FFmpeg; the MP4s in this delivery are actual input/camera captures, not generated animation. Avoid concurrent captures when comparing cadence; the recorded desktop runs had concurrent evidence work, disclosed above.

The ZIP has per-file SHA256 and CRC checks. User-device JSON export includes environment/camera/cache/session data and explicitly does not certify a real device. [Device checklist](DEVICE_CHECKLIST.md).

**Checkpoint:** review this G3-A foundation and registration issue before expanding the pipeline into G3-B. No full-world art acceptance, main merge, public deployment or final-release recommendation is claimed.
