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

## v0.3 review candidate (complete)

| Asset | Source / output | Status | Provenance / evidence |
|---|---|---|---|
| Approved v0.2 originals | preserved-v02.json; baseline b5ed079; all old assets/exports/showcase and lockfiles | 37 exact hashes unchanged | No original model/source/texture/animation regenerated or replaced |
| Hanok polish layer | Studio/modeling/polish-v03.py; assets/v0.3/source-blend/hanok-polish.blend; exports/v0.3/models/hanok-polish.glb + manifest/dimensions | Generated, Validator 0/0, actual browser render verified | Original project-owned geometry; 527,852 bytes / 13,312 triangles / 21 primitives; GardenBreeze; no new textures/decoders |
| Expressive mascot/ambient systems | preview/src/LivingMascot.tsx, LivingWorld.tsx, PolishedCamera.tsx | Six real static/live clips and mesh/keyboard reactions verified | Original GLBs reused; cloned/accented samples + chin-hand/frown/gaze/blink at runtime; no new mascot mesh claimed |
| Actual visual comparisons | quality-reports/v0.3/final-render/ + candidate-render/, REVIEW.md | 11 + 11 browser checks PASS; actual photos inspected | Day/evening/night/hero, six poses, live pairs, details, default phone fit, fallback; 0 critical errors/missing resources |
| Real movement capture | capture/ original WebM + reviewed trims/frames; living-hanok-motion.mp4 | H.264 1280×720, 41.92s, 767,431 bytes; decoded frames inspected | Actual WebGL/browser playback, loading/resize trimmed only; no motion interpolation/speed-up; not GPU FPS evidence |
| Standalone review HTML | showcase-v0.3/index.html + build-info/launchers/README | Final build, 8 original embedded assets, private-content/strict static allowlist audit | Final checksum in build-info; actual extracted/prefix HTML render verified; original public showcase/ untouched |
| Local/static review packages | downloads/v0.3/ ZIPs + package-manifest.json | Final SHA verified; extracted launcher and /3D-pharse5-/ served/rendered correctly | Local HTTP viewer needs Python3, no Node/Blender/Internet; Windows launch text/code reused, native Windows GUI not measured |
| Review request/history | docs/reviews/VISUAL_POLISH_V03_USER_REQUEST.md; all review-pass/failed/interrupted reports | Preserved checkpoints | Source of v0.3 scope and section-13 release gate; historical failures are not final pass evidence |

No Hangul Garden/new district, paid provider, audio or backend assets were created. Physical-device FPS is unmeasured. Current candidate is ready for the user's visual feedback; public v0.3 is not deployed.

- PUBLIC-RELEASE-003: user authorized publication of the saved v0.3 HTML (8,213,753 bytes; SHA 0ce49e58b26baa3802bc6e22fa4cab91d7181232e0069adcedd4f9353270c2d6). Artifact staged as only index.html/.nojekyll; no source/model regeneration; all 37 baseline file hashes remain unchanged. Public verification pending.

- PUBLIC-RELEASE-003 complete (2026-10-14T03:41:55.638744+00:00): existing exact v0.3 artifact is PUBLIC_LIVE_VERIFIED at https://anapaulagatti.github.io/3D-pharse5-/. Release evidence in quality-reports/v0.3/pages-release/ (11 public checks, inspected screenshots, origin byte match). Original source assets/approved v0.2 HTML and 37 baseline checksums retained. No new asset generated for deployment.
