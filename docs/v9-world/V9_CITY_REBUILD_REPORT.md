# V9 — completely new Korean city review candidate

**USER VISUAL APPROVAL PENDING.** The playable reconstruction and technical delivery are complete; the map is not locked, merged to main or publicly deployed.

## View it

Download [playable-review.zip](playable-review.zip), extract the entire **Korean-Arena-V9-World-Review** folder, run `python start.py` (Windows: `py start.py`), then open **http://localhost:8765/3D-pharse5-/v9-world-review.html** in a web browser. Alternative: `python -m http.server 8765` from the extracted root. Never file:// or a raw HTML viewer. Python3 required; no Node/account/API key for the package. Internal cloud localhost is not a public preview link.

- [Whole-world web preview](V9_WEB_OVERVIEW.png) / [actual native4352×6144 Phaser overview](quality/final/V9_FULL_WORLD_OVERVIEW.png).
- [Honest V8/V9 comparison](V8_V9_REAL_DIFFERENCE.png), [editable masterplan PNG](V9_NEW_CITY_MASTERPLAN.png), [SVG](../../assets-src/v9-world/plan/city.svg), [JSON](../../assets-src/v9-world/plan/city.json), [verified navigation](V9_NAVIGATION.png).
- Native actual-engine district crops: [city](V9_CITY_STREETS.png), [Namsan](V9_NAMSAN.png), [station](V9_STATION.png), [leisure campus](V9_ENTERTAINMENT.png), [waterfront/ferry](V9_WATERFRONT.png), [Jeju](V9_JEJU.png).
- [Actual normal-entry gameplay video](quality/video/v9-gameplay.mp4); [native1024×768 gameplay crops](quality/final), [real844×390 mobile captures](quality/mobile).

Root district images are1:1 crops of the actual engine overview. Gameplay crops are the real follow camera. Web/comparison images are labeled1:4 nearest previews, not sharpness references. V8's5312px canvas is explicitly padded to the6144px comparison frame; no stretching, tracing or fabricated old terrain.

## Recovery and preservation

Full rejected V8 recovery **0b809ee883231fcfe46af6330a93e2142c98c299**, tag `recovery/before-v9-total-southern-reset-20261021`, was pushed/remote-verified before removal of4,931obsolete tracked files (4,087,341,729bytes). Exact audit/restoration: [SOUTHERN_RESET_CLEANUP.md](../../SOUTHERN_RESET_CLEANUP.md) and [deleted-file inventory](deleted-files.json). Clean foundation07d9ce5; verified grayboxbb8c9e7 precedes new image production.

Protected north:273objects/253source solids, literal4352×2240ground and native source art. Actual matched-camera1024×768 north frame remains byte-identical to archived V8 ([proof](quality/north-preservation/actual-render-comparison.json)). Original108native art kinds/60source sheet+provenance records, Juni144frames, editable character concepts and shared gameplay/Academy/UI remain preserved. Original3D/history/main survive their recovery history; the separate learning app was untouched.

The old V8 screenshot is read only by the comparison generator from its archive after V9 authoring. No rejected southern coordinates, road masks, plots, district footprints or terrain are imported into planning/build tools.

## New urban design

Original4352×6144 world,33hierarchical public routes and25planned sites. Main civic streets/blocks came before building placements. Northeast Namsan contrasts with southwest transit; the independent southeast amusement campus connects to the coast. New southwest Jeju uses one intentional ferry connection, no mainland-island bridge.

The civic ring contains a planted meeting island and useful shop frontages. The station has its railway behind the entrance, one perpendicular crossing, a full-width forecourt, a public shelter and a gallery-facing neighborhood lane. Modern plot thresholds differ from park paths and cultural-campus paving. The continuous promenade ends in purposeful viewing/gateway spaces; the terminal/wood landing/ferry share one clear boarding sequence. Jeju arrival1984,5504 is on its route outside the112px boarding trigger.

### New site coordinates (native artwork scale1)

|Site|Artwork ground anchor|Street entrance/approach|Original asset|
|---|---|---|---|
| bookshop | [1648, 2672] | [1648, 2784] | fw-bookstore |
| library | [2544, 2656] | [2544, 2784] | rf-prod-library |
| neighborhood-service | [800, 3216] | [800, 3280] | v3-urban-hub |
| cafe | [2672, 3184] | [2672, 3264] | rf-cafe |
| tower | [3520, 2904] | [3520, 2960] | v3-tower |
| garden-pavilion | [3704, 3200] | [3704, 3272] | v3-trail-pavilion |
| station | [1376, 3896] | [1376, 3960] | v3-station |
| transit-shelter | [2224, 3592] | [2224, 3648] | v3-bus-stop |
| coastal-cafe | [672, 4136] | [672, 4256] | v3-coastal-cafe |
| lookout | [1392, 4168] | [1392, 4256] | v3-seawall |
| wheel | [3136, 3856] | [3136, 3920] | v3-wheel |
| carousel | [3840, 4128] | [3840, 4216] | v3-carousel |
| visitor | [3872, 3672] | [3872, 3744] | v3-kiosk |
| discovery-hall | [3776, 4480] | [3776, 4536] | v3-discovery-hall |
| campus-entry | [3216, 4480] | [3216, 4592] | v3-bloom-entry |
| ferry-terminal | [2352, 4560] | [2352, 4656] | v3-ferry-terminal |
| oreum | [1280, 5520] | [1280, 5584] | v3-oreum |
| village | [1296, 5840] | [1296, 5904] | v3-jeju-court |
| nature-center | [1856, 5808] | [1856, 5872] | v3-nature-centre |
| cliff-lookout | [832, 5712] | [672, 5744] | v3-cliff-lookout |
| basalt-learning | [1536, 5920] | [1536, 5976] | v3-basalt-discovery |
| corner-grocery | [1280, 2728] | [1280, 2784] | new-grocery |
| bakery | [1280, 3216] | [1280, 3280] | new-bakery |
| language-center | [2016, 2672] | [2016, 2784] | new-language |
| design-gallery | [2192, 3904] | [2192, 3968] | new-gallery |

These positions were selected from the new plan, not retained to satisfy old tests. Public entrances, collision and source/runtime Tiled exports were updated together. Future learning/social anchors are reserved; no unrelated multiplayer, PvP, ads, backend or mass NPC production was added.

## Actual art and tool execution

Four real host image_gen calls: original16material swatches, four distinct Korean shops, a local water-material edit (only2cells adopted;14others unchanged) and two distinct park/campus fence modules. References were original project station/cafe/shop artwork only. No Pixels map/sprite/branding/texture is shipped. Host model and price are unexposed; no billable provider API was invoked and Forge paid-request budget stayed0. Public-reference access limits and interpretations are documented in [PIXELS_WORLD_DESIGN_STUDY.md](../../PIXELS_WORLD_DESIGN_STUDY.md).

Forge pinned5324342fdfab72430f4e9604f3fe427009f8596d actually executed prop extraction, terrain extraction, palette build/apply, map hash/validation, Tiled export, linked world/Academy navigation, layered composition and its unchanged browser verifier over HTTP. 79recorded commands; 74exit0, 5recorded failed diagnostics. Exact commands/stdout/stderr: [forge-commands.json](../../assets-src/v9-world/forge-commands.json). Skill reads alone are not counted. No master_still/sprite_set/video synthesis is claimed: Juni was preserved.

Four shop PNGs256×224/192colors and two fence PNGs144×48/96colors have padded binary alpha. Original approved art keeps its pixels/native scale. Ground RGB comes from original generated image textures; geometry/masks place materials. Natural-repeat reflections and32six-phase source-pixel water groups are image transforms, not a code-drawn substitute world or video synthesis. No global saturation filter, blur or approved-art resampling.

523actual separate Phaser prop instances/101runtime kinds, over editable tile layers; 478exact source/runtime bodies. Atlas4096×1216/4846tiles. The engine overview is not a flattened generated background.

### Retained warnings and corrected failures

- `{"file": "assets-src/v9-world/art/shops-extracted/prop-pack.json", "id": "edge_touch", "status": "warn", "value": ["new-grocery", "new-bakery", "new-language"], "threshold": 0}`
- `{"file": "assets-src/v9-world/art/fences-extracted/prop-pack.json", "id": "edge_touch", "status": "warn", "value": ["park-fence"], "threshold": 0}`

Native outputs were inspected with transparent padding and in-game contexts; numeric acceptance is not user art approval. The initial all-data-URI Forge diagnostic exceeded its16000000byte default (`html-size22521450`). A diagnostic-only32000000byte budget passes; all route/movement/Y-sort assertions remain unchanged and that HTML is not shipped. The Vite main chunk remains above1600kB; actual distribution/ZIP size and measured cloud behavior are reported, not hidden by increasing its warning threshold. Unused resvg-py is unavailable; no unrelated reinstall.

Actual first screenshots exposed a service building hiding the square, isolated mulch strips, curb rings at joins, a too-narrow station forecourt and false soil halos around piers. The plan/graybox/site placement and material unions were corrected. Raw earlier schema/status/size diagnostics remain in tool receipts. Source CI39540303557 had51passed/2long-route timeouts while awaiting CDP input; the CI host now uses the same CPU-compositor flag as local verification. No timeout, collision, speed or acceptance assertion was weakened.

The first V9 recording aborted with ENOSPC. Its footage was not reused. Before removing obsolete task-owned JPEG caches, the full archived V8 MP4 was rehashed to5d67b8d69eeeb1757a62543fdcbdd833164ead3b60136b0956f7370da3f9e171. Original source art/tags/encoded recovery video remain intact. The final recording started fresh with a6GiB preflight.

## Technical and visual verification

- 12unit tests, full52case local browser suite plus1additional cached/reference occlusion case. Exact-source GitHub CI: [41210999009](https://github.com/Anapaulagatti/3D-pharse5-/actions/runs/41210999009) at `d8ef46108e11cc2d85d5741124daf8801545c083`: 53browser cases passed. No queued-run success inference.
- All33routes traversed in actual Phaser using public input. Academy lesson/return, blocked rails/designated crossing, building foundations, reciprocal ferry, basalt feedback, actual Juni walk/run/wave/celebrate/idle and mobile landscape/portrait controls work.
- Source/runtime image/collision hashes match, both linked Forge nav reports pass, upstream browser61targets/keyboard/Y-sort pass. This diagnostic reachability is separate from actual Phaser input tests.
- Actual draw-time Canvas atlas sampling has no smoothing; WebGL atlas min/mag are NEAREST. Native avatar image pixels match DPR1/3. Disabled WebGL automatically falls back to a nonblank playable Canvas view.
- Reduced-motion follows OS preference: actual water pixels/ambient clock stop; normal mode visibly animates. New-tree cue matches source-alpha reference and clears after Juni walks out. No critical browser console/network errors in final native/mobile/package captures.
- Full native engine overview and follow-camera/mobile images were actually inspected and corrected, not accepted merely because screenshots were written.

### Uncaptured cloud samples

|Case|Renderer|MedianRAF ms|p95RAF ms|MedianRAF Hz|
|---|---|---|---|---|
|desktop-civic|Canvas|16.70|16.80|59.88|
|desktop-coast|Canvas|16.70|16.80|59.88|
|mobile-leisure|Canvas|16.70|16.70|59.88|
|software-webgl-station|WebGL|33.30|50.00|30.03|

Eight seconds percase after warmup; no capture/concurrent local browser suite. These are cloud browser RAF samples, not physical Android/iOS/Safari/hardware-GPU measurements or a universal60FPS guarantee.

## Video, ZIP and reproducibility

Actual normal-entry31stop walkthrough, **388.219s**, 8399captured=8399encoded frames, 79,945,901bytes. Original capture timestamps preserved to a maximum0.000500s error at1ms encoding timebase. Public joystick/run/dialog/emote/ferry controls only; no QA placement, artificial scene skip, retiming, interpolation, repeated footage or still-image replacement. Capture is JPEG78/everyNthFrame2; H264 is lossy and native PNGs remain the sharpness reference. Real Chromium play/5seeks/changing decoded pixels were verified; representative frames inspected, not every-frame visual review. [Encoding proof](quality/video/encoding-verification.json), [playback proof](quality/video/browser-playback.json).

ZIP **14,542,176bytes/148files**, SHA256`0fb2dceb95b2ded85722871f28269bfb6390320497cacdce7769ef7ec4f6dd67`, runtime/art source`77f8c6848e98af6646938925c778ce00cc97db17`. Its own HTTP launcher was run. Native source/ZIP pixels match in six districts; mobile analog movement, portrait pause, both ferries, Academy and basalt wrong/correct feedback work. All packaged runtime file hashes verified. No credentials, original source masters, old reviews or unrelated3D/private files are shipped. [HTTP proof](quality/package/http-verification.json).

Independent clean checkout`d8ef46108e11cc2d85d5741124daf8801545c083`: locked npm installation, no authoring-tool dependency, stored-asset/type/lint/format/unit/build/browser checks pass. 53browser/12unit. Complete distribution matches the package/runtime build ([clean setup proof](quality/clean-setup.json)). This is a fresh checkout verification, not a claim that a new-task cloud snapshot has been restored.

`main` remains33360ed1989e4db9fc3fc4e3686ca385e0b00908. Public siteHTTP200/13,543,219bytes still SHA256`082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f`. No Pages publication/merge/history rewrite/force push. Delivery checkpoint and observed final CI are recorded by the annotated review/recovery tag, avoiding a report pretending to know its own commit SHA.

**STOP: user visual approval is required before map lock, additional content or publication.**
