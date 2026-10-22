# Gate 2 acceptance — technical results and human review

## Five-task status

| Task | Technical result | Human/artistic status and practical limit |
| --- | --- | --- |
| One original commercial building | PASS — one new source, readable 오월제과 signage, native Juni scale, entrance/crosswalk collision and actual-input navigation | New bakery craftsmanship requires human review. Source is generated/finished artwork, not claimed hand-drawn. Muneum reuse alone is not the originality proof. |
| Jeju localized world fit | PASS within the separate candidate — unchanged native art/entrance, bridge connection, aligned landing, blocked ferry sea and checked paths | Candidate dimensions/registration need acceptance. The approved masterplan is untouched. Gray mainland/connector geometry is technical proof, not production bridge art or structural certification. |
| Station exact fit | PASS —555×210 blocker fits560×210 reservation, south contact/door scale preserved, walkable threshold, no platform overlap | Artwork unchanged. Collision refinement excludes10px of upper projected facade, not visible building pixels. No interior/train operation. |
| One representative world join | PASS — independent Muneum/station sources at1:1, compatible perspective/light, actual crossing, no transparent gaps | Human seam/composition review pending. One48px ownership overlap is not a generalized world-asset or tilemap pipeline. |
| Premium mobile camera prototype | PASS for repeatable Chromium emulation — follow, run/look-ahead, drag/pinch, boundaries, overview, return, optional showcase and reduced-motion behavior | Ergonomics and cinematic feel require user/device review. No physical-device FPS, thermal, Safari or real-cutout validation claim. |

## Camera coverage and quality

At844×390, gameplay uses the full-height canvas and native zoom1; the prior mobile canvas was844×281. That increases the viewable gameplay area by approximately38.8% without changing Juni or building scale. Letterboxing is applied when an environment is narrower than the camera view.

| Mode | Jeju view at844×390 | Source area covered | Meaning |
| --- | --- | --- | --- |
| Follow |844×390 at1× |20.9% | Native movement, approximately80px Juni, nearby architecture. |
| Scenic50% |1024×780 world pixels |50.8% | More composition; controls separated from camera. Demonstrated in recording. |
| Scenic33⅓% |1024×1170 world pixels |76.2% | Broad landscape/house/orchard context; inspected screenshot and touch QA. |
| Full scene25% |1024×1536 world pixels |100% | Entire Jeju footprint, current Juni, destinations and previous viewport. |

Muneum’s full-scene view uses33⅓% and covers its complete1536×1024 source. The fitted viewport uses fractional viewport dimensions where needed so a source edge is not discarded by integer viewport rounding. The artwork’s camera origin and world-edge sampling are aligned; native gameplay remains1×.

| Mobile criterion | Judgment |
| --- | --- |
| Touch controls / joystick separation | PASS — actual CDP joystick walk/run, drag, two-finger pinch, disabled movement in Scenic and restored movement after Return. |
| Scene boundaries | PASS — checks use Phaser’s actual rendered worldView, including large drags and scene-edge clamping; northern-edge HUD gets a separate probe. |
| Zoom sampling | PASS for sampled nearest behavior —144 unchanged-terrain pixels per permitted zoom match an independent nearest-source render with zero mismatches at1,½,⅓,¼; texture sampling remains nearest. This samples terrain, not every pixel of every object. |
| Pixel/detail readability | PASS for native entrances/Juni and overview landmark orientation. **FAIL for reading small shop text/fine craft at25–33%**: downsampling necessarily removes detail. Inspect native PNGs/crops or return to follow for that purpose. No filtered-image blur is claimed as detail preservation. |
| Rendering behavior | PASS for the tested short software/cloud sessions: no browser asset/page errors or observed texture loss; raw update intervals recorded. Physical-device sustained FPS and total memory residency are NOT TESTED. |
| Showcase behavior | PASS — opt-in, stationary-only start, actual movement cancels, no teleport/repeat, reduced-motion suppression. No forced scene tour during active control. |

Regular framing uses approximately60px horizontal and42px vertical directional look-ahead with eased tracking, aspect-aware vertical lead and pixel-aligned output. Safe-area insets protect controls. Emulated viewports include740×360,844×390,932×430(DPR2) and960×432. Real notches and touch hardware have not been tested.

## Timing and memory evidence

`probes.json` contains warm short-session samples from actual `performance.now()` update intervals, not Phaser’s smoothed delta. These are cloud Chromium Canvas/mobile emulation observations, not hardware FPS guarantees:

| Scene | Samples | Median interval |95th percentile | Maximum observed |
| --- | --- | --- | --- | --- |
| Jeju |300 |16.7ms |17.3ms |18.5ms |
| Muneum |300 |16.7ms |17.0ms |19.4ms |
| Independent join |300 |16.7ms |17.0ms |19.9ms |

Active texture dimensions correspond to roughly19–20MiB RGBA8-equivalent in those scenes. Chrome-reported JS heap snapshots were roughly49MiB. **Neither is total measured GPU/browser RAM:** shared decoded images can reduce backing allocations; CPU walk arrays, canvas buffers, native allocations and browser overhead add others. The join uses two ground textures(1536×720 and720×720), approximately6.20MiB RGBA8 combined. Full-world streaming, long-session leaks, memory-pressure recovery and maximum-device-texture behavior remain unproven.

The camera recording is approximately11seconds of normal-entry Phaser with actual touches, no QA hook/teleport/static-image replacement. CDP timestamps are retained in variable-frame-rate H.264; video is lossy, so native PNGs remain the pixel-quality evidence.

## Validation and provenance

- 12 acceptance browser cases cover actual new-building/station/join/Jeju-fit traversal, sea rejection, mobile camera interaction, three further landscape HUD sizes, optional-showcase behavior and reduced motion. The independent join has a separate continuous crossing trace; its result replaces the earlier registered-transition control in the final report.
- 9 render/collision/memory probes cover all four distinct zoom levels, the station wall stop, the exact future landing/collar and three short timing samples. A separate north-edge HUD test passes.
- Forge schema/file/hash validation has zero errors; navigation and unmodified-preview route checks pass for original, station, independent join and Jeju-fit. Warnings remain explicit: **`actorRadius 0 treats the actor as a point`** describes an already8px-eroded foot mask; image chunks do not individually cover the world by design. These are not warning-free reports.
- The world-fit shoreline guard removes border-connected blue sea plus8px clearance from the translated accepted path mask. Six original edge pixels were classified as open water before clearance. The original C walk mask and accepted art are unchanged. This is a conservative guard plus curated paths, not an automatically complete semantic shoreline polygon.
-TypeScript, ESLint, formatting, the18 existing foundation tests, protected actor/Juni/north checks and the dedicated Vite build pass. Build/test success does not grant artistic approval.
- 94 specifically retained source/native files match their saved hashes. The approved masterplan, northern/mainland geometry, Juni atlas, accepted Jeju entrance and approved checkpoint are preserved. New-art provenance retains the one original host output, exact prompt, approved reference, guide, finishing commands and palette. Host model and price are not exposed and are recorded as null. No paid provider API was used.

[Browser results](browser-qa.json) · [join traversal](small-join-qa.json) · [render/collision/timing probes](probes.json) · [edge HUD](edge-hud.json) · [Forge reports](contracts/preview-routes.json) · [source/fit checks](source-and-fit-verification.json) · [new-art provenance](new-art-provenance.json) · [recording provenance](camera-video-provenance.json) · [package hashes](package.json) · [eight extracted-package scene checks](package-qa.json).

Unresolved: human bakery/seam/mobile artistic acceptance; approval of the separate Jeju candidate; final bridge production/structural work; generalized modular/tilemap/full-world joins and streaming; physical-device ergonomics, sustained rendering, memory and Safari validation. These are disclosed limits, not authorization to proceed.

**STOP after this five-task review. Gate3 remains locked. No whole-world production, main merge, public deployment or separate-app changes.**
