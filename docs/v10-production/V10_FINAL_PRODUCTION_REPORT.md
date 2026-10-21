# V10 original city art — final visual review candidate

The approved V10 masterplan now runs with new original southern artwork in Phaser. It is a candidate for the user's final visual review. This report does not grant artistic approval. No main merge or public deployment is authorized or performed.

## Plan and source authority

Approved base3c323bc1d844c80b3e0ca0d62df3f1806a7a972f, preserved by remote-verified `recovery/v10-approved-graybox-before-art-20261021`. Production branch `production/v10-original-city-art` is an independent fresh clone from that base. Plan SHA-256 remains808ca4aa56be22afb11b35f30cbe557a5a5915dce272af0e9465257032233cc0. All23 property plots and major positions,19 road/trail definitions, district topology and ferry triggers/arrivals are unchanged.

Every new southern major sprite and material traces to ten new model image outputs.44 native sprites plus16 materials are palette-finished from retained editable raw source sheets;23 original major architectural frames replace every graybox frame. Archived V1–V9 southern sources do not feed the compiler, including transitively via helpers. The final hash-only diagnostic found no original/native image matching191 distinct archived image hashes. See the [source audit](V10_FORBIDDEN_SOURCE_AUDIT.md) and [asset provenance](V10_ART_ASSET_PROVENANCE.md).

Protected north y0..2239 remains exact:336 protected files,273 placements,253 solids, native terrain and fixed-camera pixel comparison. Juni's144 frames, anchors, gait/movement, Academy, gate intent, joystick, UI and source/licenses are preserved. New materials start below the protected boundary.

## Art and playable integration

| District | Implemented and inspected in actual Phaser |
| --- | --- |
| Modern town | Distinct shopfronts with Korean signs, reverse-facing upper patios for south-side shops, glass/steel façades, connected sidewalks/alleys, crossings, street trees/bikes/lights, civic seating and planted court |
| Station | New blue/white glass station, canopy, track-aligned train, platform and signed pedestrian crossing, forecourt and commercial neighbors |
| Namsan | Existing curved route topology, new granite/meadow/basalt textures, tower arrival, pergola, scenic deck with railing, rock/plant details, pine groves and rest pockets |
| Entertainment | New east-facing entrance, continuous planted boundary with straight fence sections, modern mosaic internal loop and linked ride courts, wheel/carousel/pavilion, queues/flowers/benches |
| Waterfront | Continuous coastal paving/rail rhythm, modern fish market and sea café, terminal, waiting area, timber boarding pier and aligned moored ferry, reciprocal UI boarding/arrival |
| Jeju | Curved basalt olle/village trail, village hall/tea house, volcanic oreum, dry-stone gates, tangerines, coast viewpoint and ferry arrival |

Allowed finishing refinements are recorded in `assets-src/v10-city/production/access-refinements.json` and `decorations.json`. They connect attraction doors to the approved campus loop, stop shop approaches at the curb and place small landscape/furnishing colliders. No rezoning or major topology change occurred.

Native engine inspection rejected initial roadway paving caps, separated attraction pads and disconnected perimeter modules. Those were revised; the rejected current-V10 images remain under `iterations/first-engine/`. Real keyboard tests then found a bench obstructing Namsan and a basalt wall obstructing a Jeju route; exact road clearance additionally found an oreum/furnishing conflict. New props were moved beside the route. Failures are retained under `iterations/first-navigation/`; the final actor-footprint check now clears every sampled centre-line segment of all19 approved roads. Mere graph connectivity was not accepted as sufficient evidence.

## Review artifacts

`V10_FINAL_WORLD_NATIVE.png` is the actual4352×5888 Phaser Canvas overview, not a composited mockup. `V10_FINAL_WORLD_WEB.png` is a nearest-neighbor quarter-size export of that capture. The six named district PNGs are actual1024×768 native canvas crops; `V10_NORTH.png` is the preserved baseline comparison camera. `captures.json` gives positions, sizes, hashes, camera data, loaded URLs and errors. Camera QA placement is for screenshot composition and is not traversal proof.

`V10_NAVIGATION_REVIEW.png` overlays approved routes/doors on the actual engine overview for diagnosis; numerical navigation evidence is separate in `qa/nav-report.json` and `road-clearance.json`. `V10_SOURCE_ART_REVIEW.png` is explicitly a source-art sheet. `V10_MOBILE_NATIVE.png` is an emulated mobile canvas crop.

`V10_GAMEPLAY_WALKTHROUGH.mp4` records normal entry and actual keyboard input through the north, shops/station/civic court, Namsan, amusement, coast and Jeju, with reciprocal ferry UI. There is no QA URL or position injection. Waypoints come from the final collision grid with a safety margin; automation steers through actual keys and corrects stopping drift. CDP frame timestamps preserve elapsed time, with no speedup. `walkthrough.json` records visited positions, timing and runtime errors. The shorter `V10_MOBILE_LANDSCAPE.mp4` uses one disclosed camera start followed by real emulated joystick touches.

`V10_FINAL_REVIEW.zip` contains the exact production build and a local Python HTTP launcher. Extract, run `python3 start.py` (Windows: `py start.py`), then use WASD/arrows, Shift and E, or landscape touch controls. No Node or image authoring is required to play. `package-verification.json` records independently extracted desktop/mobile normal-entry checks and byte equality for all144 build files.

## Validation and practical limits

Final checks passed: exact-lockfile dependency installation; protected/new asset checks; TypeScript, lint and format;12 unit tests; production build; all15 browser cases with0 skips/failures/flaky results. Browser coverage includes23 venue entrances, actual-input district routes, north/Academy/gate preservation, collision/crossing, reciprocal ferry, mobile analog movement/orientation and forced Canvas/WebGL. Final Forge evidence passes32 targets with0 unreachable/pockets/thin gaps,515 clear sampled road segments and Tiled readback with0 differing pixels. The1802-frame full walkthrough lasts256.16s, has16 destinations, reciprocal ferry UI and0 runtime errors. ZIP verification confirms144 exact build files and normal-entry keyboard/touch movement. `validation.json` and `validation/` contain actual machine receipts; screenshots are not traversal proof. Forge bundle/nav/Tiled/native browser receipts are stored under `assets-src/v10-city/qa/production/`. See [skill execution](V10_SKILL_EXECUTION_LOG.md) for actual commands and precise limitations. Setup never regenerates art or invokes a paid provider.

Pixels public sites returned403; no firsthand live-map visit is claimed. Existing documented research was used for hub/entrance/readability principles, without copied assets or geometry. Model identity/billing are unexposed. Stylized Korean signage and repeated material motifs remain subjects for visual judgment. Terrain-cell extraction does not prove seamless Wang/autotile coverage. Tested browsers are Linux Chromium, with emulated mobile and software WebGL; physical phone/GPU/Safari/Firefox performance is unverified. Forced SwiftShader WebGL is slow on this shared headless host; normal software-GPU detection selects Canvas. The existing large Phaser JS chunk warning remains documented. No test, hash or source audit certifies premium artistic quality.

## Measured performance

Final sample: six district cameras per renderer,2.5s RAF after0.5s warmup, DPR1, headless Linux Chromium, after the other browser/encoding jobs completed. Ready times include local HTTP load on this host; these are measurements, not hardware guarantees.

| Mode | Average FPS range across six cameras | p95 frame time range | Initial ready |
| --- | --- | --- | --- |
| Desktop canvas | 55.0–58.8 | 16.8–33.3ms | 4138ms |
| Desktop webgl | 14.6–23.5 | 50.1–133.3ms | 4735ms |
| Mobile emulation Canvas | 58.4–60.3 | 16.7–16.8ms | 2155ms |

Forced WebGL uses SwiftShader and is slower; normal software-GPU detection chooses Canvas. The new-town joystick test moved127px with actual CDP touches after a disclosed QA camera start, then returned. No runtime errors or missing assets were recorded. Earlier concurrent-QA timing is retained separately under validation and is not presented as the final baseline. Physical devices and hardware GPUs remain unmeasured.

## Handoff gate

Review branch: `production/v10-original-city-art`. Immutable review checkpoint: `checkpoint/v10-original-art-review-20261021`. The validated candidate is delivered through these Git references without changing main or deploying. The requested stopping point is the user's final visual approval. Any further major city-plan change or release requires separate direction.
