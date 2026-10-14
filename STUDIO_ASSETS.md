# Studio asset inventory

All outputs below exist. Source and export SHA-256, dimensions, node-instance geometry and clip metadata are in exports/v1/asset-manifest.json and ASSET_MANIFEST.csv. Concept art is not counted as a mesh. Older prototype source is retained in Git d355dca, superseded by delivered GLBs.

| Asset | Editable source | Output / format | Status | Milestone / usage | Validation / provenance |
|---|---|---|---|---|---|
| arena-hero | assets/source-blend/arena-hero.blend; Studio/modeling/arena.py + common.py | assets/models/arena-hero.glb; exports/v1/models/arena-hero.glb | Saved and browser-verified v0.2.0 | M4/M5, preview and portable export | Validator 0/0; 3,379,732 export bytes; exact animation sample / topology / bounds parity; original procedural |
| mascot-base | assets/source-blend/mascot-base.blend; Studio/modeling/mascot.py + common.py | assets/models/mascot-base.glb; exports/v1/models/mascot-base.glb | Saved and browser-verified v0.2.0 | M4/M5, preview and portable export | Validator 0/0; 289,652 export bytes; exact animation sample / topology / bounds parity; original procedural |
| Three-direction concept | Original text + native image_gen; concepts/mascot-directions-v1.json | concepts/mascot-directions-v1.png | Saved; A selected through rubric, not user approval | M3 | Actual generated concept sheet, original input, not a model |
| Hanji / stone grain | Studio/modeling/common.py | assets/textures/hanji-grain.png, courtyard-stone.png; exports/v1/textures/; embedded GLB maps | Saved 256×256 PNG | Materials | Original procedural, checked PNG dimensions/hash |
| Arena posters | preview/tests/studio.spec.ts rendering actual GLBs | assets/posters/arena-desktop.png, arena-mobile.png; exports/v1/posters/ | Saved without UI status overlay | M7 / fallback | Actual browser renders, original artwork |
| Transparent mascot | render-mascot.py + mascot-base.blend | assets/posters/mascot-transparent.png; exports/v1/posters/ | Saved RGBA 800×1000 | M7 / portrait fallback | Cycles render, alpha 0–255 inspected, original 3D |
| Character animations | mascot.py + mascot-base.blend | Six clips embedded in mascot-base.glb; assets/animations/mascot-clips.json descriptor | Six distinct poses and live playback checked | M6 | Idle/Happy/Thinking/Celebration/Disappointed/Greeting, 2 seconds each; exact sample preservation |
| Lantern sway | arena.py + arena-hero.blend | LanternSway embedded in arena-hero.glb | Checked animated GLB | M6 | 3-second transform clip, original procedural |
| Current visual / QA evidence | preview/tests/studio.spec.ts | quality-reports/preview-*.png, mascot-*.png, arena-night.png, renderer*.json, software-benchmark.json and Validator reports | Saved | M7 | 9 passing browser tests, raw/optimized pose pixel-identical; software ~3.3 FPS, not target-device acceptance |
| Legacy toolchain fixture | Studio/scripts/create-smoke-fixture.py | Ignored Studio/.cache/smoke/*.blend, *.glb, TSX | Tooling test only | M2 | Historical Validator reports; not final art |
| Portable actual showcase | Existing preview/src/ + Studio/scripts/build-showcase.mjs | showcase/index.html, build-info.json, README | Saved, offline content verified | SHOWCASE-001 / requested HTML viewing | Same interactive app; 7.15 MiB; seven embedded exports checked against manifest, download bytes verified; six offline checks; direct file:// navigation blocked by managed cloud browser policy |
| Portable showcase evidence | Studio/scripts/verify-showcase.mjs | quality-reports/showcase-{desktop,mascot,mobile,fallback}.png, showcase-offline.json | Saved | SHOWCASE-001 | Actual HTML rendering with network offline; zero external requests/JS errors; personal-desktop direct-file opening not yet verified |
| HTTP viewing package | Existing showcase/index.html + start.py/START_WINDOWS.cmd/README/DEPLOYMENT + Studio/scripts/package-showcase.py | downloads/showcase-v0.2-http.zip, package-manifest.json | Saved; extracted HTTP engine/browser verified | PREVIEW-ACCESS-001 | 2,916,077 bytes; unchanged embedded assets; Linux Python launcher actually served the ZIP HTML; native Windows GUI launch not tested |
| Deployable static package | Same existing HTML; no new assets | downloads/showcase-v0.2-static.zip; .github/workflows/showcase-pages.yml; showcase/DEPLOYMENT.md | Preserved; same approved HTML now publicly deployed | PREVIEW-DEPLOY-001 / PAGES-LIVE-001 | 2,910,445-byte recovery ZIP; current authorized workflow supports scoped deployment-file pushes/manual dispatch; public success below |
| Current HTTP render evidence | Studio/scripts/verify-preview-http.mjs and existing smoke suite | quality-reports/preview-access/ screenshots, http-verification.json, dev-tests.json, VISUAL_REVIEW.md, INITIAL_DIAGNOSIS.md | Saved and visually inspected | PREVIEW-ACCESS-001 | 21 HTTP checks and 9 smoke tests pass; root/nested static path, real camera/lighting/poses/reduced motion/fallback, 0 critical console errors/missing resources |

Current HTML is 7,493,366 bytes, SHA-256 9105a93b022e6751831ba66ae4d353317c43179aa3f045824a329ffdcfc76c17. The old offline report above belongs to the earlier HTML before the favicon-only patch; current verification is the HTTP report. All approved GLB, PNG, .blend and animation sources/exports are unchanged.

No learning-alley, celebration scene or six district assets are claimed in v0.2.0. Keep approved/successful outputs; regenerate only after a documented source change and checkpoint.

| Deployment output | Source | Status | Evidence / limits |
|---|---|---|---|
| Approved Pages artifact | Existing unchanged showcase/index.html, prepare-pages-site.py | Locally staged and verified | Exactly index.html + .nojekyll; HTML SHA 9105a93b022e6751831ba66ae4d353317c43179aa3f045824a329ffdcfc76c17; no private source/Blender/cache files in site |
| Initial deployment QA | verify-preview-http.mjs; artifact/source/provenance audit | Saved local/attempt-1 history | quality-reports/pages-deployment/ with artifact-audit.json and 7 local HTTP checks, desktop/6 poses/night/camera/mobile/fallback screenshots; later public verification below |
| Public GitHub Pages site | Approved scoped push/manual workflow in existing repo | LIVE, public render verified | https://anapaulagatti.github.io/3D-pharse5-/; run 38402363567 attempt 2 success, deployment 7039586635; public 200 HTML/approved SHA, 7 browser checks and actual screenshot inspection |
| Public-site verification evidence | Deployed website + verify-preview-http.mjs | Saved and visually inspected | quality-reports/pages-live/ deployment.json, http-verification.json, VISUAL_REVIEW.md and actual scene/day/night/camera/six poses/mobile/fallback screenshots; zero critical console/missing-resource errors |

## v0.3 candidate work

| Asset | Source/output | Status | Provenance/preservation |
|---|---|---|---|
| Approved v0.2 baseline | quality-reports/v0.3/preserved-v02.json; baseline b5ed079 | Hashes recorded before polish | All original assets/source/exports/deployed HTML retained |
| v0.3 review request | docs/reviews/VISUAL_POLISH_V03_USER_REQUEST.md | Saved | User's authored visual review and explicit release gate |
| Hanok polish layer | Studio/modeling/polish-v03.py; assets/v0.3/source-blend/hanok-polish.blend; exports/v0.3/models/hanok-polish.glb and manifest | Generated and Validator verified; render pending | Original additive artwork; 527,852 bytes, 13,312 triangles, 21 primitives; GardenBreeze clip; 0 errors/0 warnings |

| Initial v0.3 rendered evidence | quality-reports/v0.3/initial-render/ | Seven baseline browser checks PASS | Final light balance and new interaction/motion verification pending; do not use initial overbright shots as final art approval |
| v0.3 preview implementation | Existing preview/src plus LivingMascot/LivingWorld/PolishedCamera/useStudioModel | Production build and typecheck PASS, detailed QA in progress | Original six GLB clips copied/accented at runtime; no approved GLB/source bytes changed |

| Reaction/camera correction evidence | quality-reports/v0.3/intro-diagnostic.json; review-pass-1/2/3/ | Native Greeting→Idle confirmed; previous failures preserved | Identical DOM canvas bounds, actual mixer advance; final screenshots/full QA pending |
| Separate v0.3 standalone candidate | showcase-v0.3/index.html + build-info.json | Built; full candidate QA pending | 8,212,845 bytes/8 verified embedded base+detail assets; does not alter public v0.2 |

| Verified production polish evidence | quality-reports/v0.3/final-render/verification.json and full screenshot set | 11 checks PASS; final face review refinement pending | Actual static/live six poses, three lights, hero/detail/orbit, responsive/fallback captures; zero critical errors/missing resources |

| Final production render/interaction evidence | quality-reports/v0.3/final-render/ | 11 checks PASS, actual images inspected | Refined six static/live poses, actual three object mesh clicks + keyboard, camera/motion/accessibility/mobile/fallback; 0 critical errors/missing resources |
| Final candidate HTML/ZIPs | showcase-v0.3/; downloads/v0.3/ | Rebuilt to a667e98b…; privacy/integrity audit PASS | 8,213,612-byte HTML; 8 checksum-verified original assets; all 37 v0.2 originals unchanged; not publicly deployed |
