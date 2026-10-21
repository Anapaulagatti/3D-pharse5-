# V10 clean workspace audit — 21 October 2026 (Asia/Saigon)

Status: playable GRAYBOX, awaiting user masterplan/layout approval. This report does not approve final art.

## Git and workspace

- Repository: Anapaulagatti/3D-pharse5-. Fresh HTTPS depth-one clone of rebuild/pixel-social-rpg-v3 into /workspace/southern-city-v10; no worktree or reset.
- Verified V9 base: ed007df73dac31ed834cb3fbb85a3cc80bdf26a0. Created and pushed recovery/before-v10-cleanroom-20261021; independent git ls-remote returned the same full commit.
- Existing recovery tags remain untouched. Main remains33360ed1989e4db9fc3fc4e3686ca385e0b00908; original development branch remainsed007df. New work goes only to rebuild/southern-city-cleanroom-v10.
- Initial independently authored plan committed as eea64e4 BEFORE reading the V9 plan for comparison. Subsequent two trail-control corrections came from collisions against the NEW placeholders. Final plan SHA256: 808ca4aa56be22afb11b35f30cbe557a5a5915dce272af0e9465257032233cc0.
- The prior setup's own Vite process was stopped. New V10 dev used port4210; Playwright production preview4201; the extracted ZIP launcher4212 initially, then an ephemeral port36069 for the final ZIP verification. These are internal validation addresses, not public previews.

## Hygiene and source isolation

The fresh checkout brought no ignored node_modules, dist, .cache, Python bytecode, browser profile or authoring cache. npm ci --ignore-scripts installed138locked packages using the existing lock. Node24.19.0, Python3.12.14, Pillow12.3.0 and systemChromium were reused. No dependency declarations/lockfiles changed. All browser contexts were fresh; capture/package contexts explicitly blocked service workers. No old tabs were reused. During native visual inspection, a gap in the tall tower placeholder facade was corrected; ground, plots, roads, collisions and protected assets were unchanged, and fresh dependent hashes/navigation/engine/package checks were run.

V9 generated public/assets/world and v9-world-review.html were removed from the V10 active runtime after verified remote recovery. V9 editable/original source files and historical evidence remain inactive and recoverable, not repurposed or renamed. Original source art, licenses and tools were preserved. The Vite build has only index.html and v10-city-review.html; no old runtime asset directory ships in the ZIP.

V10 compile inputs are independent authored literals, assets-src/v10-city/plan/city.json, protected-north and north-only original library images. No old southern image, tile atlas, mask, road, plot or placement input enters tools/v10_plan.py or tools/v10_build.py. The comparison script is a separate diagnostic, not a build dependency. New atlas SHA256: eb94b49c07c9dd65a52c78f9c6c52470ec4fbc8ed4ecb925270135dff19fd952.

## Protected foundations

336files are enumerated by hash in assets-src/v10-city/protected-files.json, in addition to the original protection records. All273north objects,253north solids,4352×2240native ground, Juni144frames, source artwork, Academy, shared engine/motion/joystick and lockfiles pass integrity checks. Actual matched Phaser north canvas is pixel-identical to the stored V9 frame: SHA2568ce1954373cb69289e5cc521f6bc31d541bbbf60767781d3a0d3bea35bab0fe3. Conditions: Canvas, native1024×768, camera1664,884,zoom1,DPR1,reduced-motion. This is one matched view, not a claim about every possible frame/device.

## Runtime provenance and tests

See captures.json for exact HTTP URLs, canvas sizes, camera positions, PNG hashes and every request path. Captures are actual Phaser canvases; QA placement composes screenshots and does not count as navigation evidence. All requested outdoor map resources use assets/v10-city; no assets/world or v9-world requests occurred. Separately, seven routes used real keyboard input at unchanged speeds after one QA start per route. Normal-entry north and extracted-ZIP desktop/mobile movement tests expose no QA hook.

Typecheck, lint, format,12unit tests, build and15browser cases passed,0skipped/0unexpected/0flaky. Forge final bundle validates with0warnings;32targets reachable,0unreachable pockets/0thin gaps. Every authored road centerline passes the full Forge collision model. Both ferry directions,23venue interactions, rail/building collisions, designated crossing, Academy, mobile CDP joystick, portrait pause and forced WebGL passed. Tiled readback matches every runtime ground pixel and collider.

The actual ZIP was extracted and served through its Python launcher. All125built files match the production build byte-for-byte; normal-entry desktop keyboard and emulated-mobile touch moved Juni without missing resources/page errors. ZIP SHA256: 7547734a0f98cd52a924d9b12a9b2009469729490525e6bd70d7983763d011a8.

## Honest limits and retained failures

- Main JS chunk1725.75kB exceeds the existing1600kB warning budget; unchanged threshold. No performance guarantee or physical-device test.
- First Forge bundle attempts failed on schema metadata (art_source/world/layer name); corrected to the documented contract. Missing object layer initially produced a warning; added. A stale derived hash was rejected after new graybox generation; old derivation retained in .cache and fresh hashes/nav proof generated. Initial diagnostic envelopes are in validation/initial-*.json. Final envelopes are distinct and pass.
- Forge doctor reports7optional missing capabilities, including unused resvg and provider/video routes. No provider/key was requested; no image/video generation or paid call occurred. The host image tool was identified only, not executed.
- Pixels homepage, play site and both Terravilla references returned proxy403. No firsthand study of inaccessible gameplay/maps is claimed. Urban design rationale here is our own interpretation of the user brief; no proprietary assets/geometry were copied.
- V9 geometry-specific tests are archived in tests/archive/v9, unrun and not counted. V10 has its own meaningful route/entrance/ferry/collision suite plus preserved foundation tests.
- This is placeholder geometry, NOT finished southern pixel art. Tiled editor GUI, physical phones and Windows GUI launcher were not tested. Public website deployment and main merge were not performed.

## Approval boundary

PhasesA–C are presented for visual review. Stop here. Do not start final artwork or phasesD–F until the user explicitly approves this masterplan and playable graybox. Automated checks establish technical feasibility only.

GitHub Actions API status could not be read: api.github.com returned proxy403. Native HTTPS Git operations work; no token was requested. Do not infer CI success from local checks or workflow triggers.
