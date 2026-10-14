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

## v0.4 overhaul in progress

Baseline source/export/published artifacts preserved by quality-reports/v0.4/preserved-v03.json. New files will use assets/v0.4, exports/v0.4, showcase-v0.4 and quality-reports/v0.4; no existing approved files overwritten. Mascot v0.4 derives actual Blender geometry with new leg pivots and authored facial/full-body clips.

- New actual sources/assets: assets/v0.4/source-blend/mascot-living.blend and hanok-living.blend; exports/v0.4/models GLBs, asset-manifest with 12/1 clips and Validator 0/0. Original geometry/versions preserved; detail bands reduced from 64 to 24 segments, 25,792→18,112 triangles. Runtime scene and clean five-action UI implemented, pending human/render validation.

- Corrected v0.4 mascot source/GLB retains native per-state face/leg reset tracks, 696,568 bytes and 12 clips. Actual face geometry seen in static browser shots; separate versioned GLB/source retained. No old approved .blend/GLB/texture changed.

- Saved showcase-v0.4/index.html and downloads/v0.4 review/static ZIPs; asset URLs embedded as Blob URLs, no CDN/server assets required. Candidate audit PASS. These are new recoverable outputs; live v0.3 deployment inputs remain untouched.

- Production final-render/verification.json PASS (10 stages), actual desktop/mobile/face/motion screenshots saved and inspected. All five GLBs Validator 0/0. Native compositor video captured 52 actual frames/44.92s; raw JPEGs/timestamps retained. Remove the asynchronous film-caption strip from the final video, without retiming or changing character pixels.

## v0.4 final inventory — complete for review (2026-10-14T04:52:37.822903+00:00)

| Output | Status / evidence |
|---|---|
| mascot-living.blend / GLB | Original geometry derived from actual approved source, independent feet/arms/head/ears and editable 12 NLA clips including native facial reset channels; 696,568 bytes / 11,074 triangles / 47 source primitives; Validator 0/0 |
| hanok-living.blend / GLB | Original complementary 18,112-triangle / 799,860-byte / 20-primitive detail layer, CanopyWind; architecture, courtyard props, stronger canopy and skyline; Validator 0/0 |
| exports/v0.4/asset-manifest.json | Hashes/provenance, true clip duration/channels, geometry and bind-pose bounds; no decoder or new texture |
| final-render/ and candidate-render/ | 10+10 actual browser stages PASS; desktop/three moods/12 static + live pairs/detail/mobile/fallback and inspected images saved |
| living-hanok-v04-motion.mp4 | 44.92s, H.264 1280×660, 641,340 bytes, actual compositor timestamps; decoded frames inspected; raw 52 JPEGs/timestamps and uncropped movie preserved |
| showcase-v0.4/ and downloads/v0.4/ | Final 10,213,265-byte HTML with 10 embedded verified assets; review/static ZIPs and tested HTTP launcher/subpath package; audit PASS |
| REVIEW / VERIFICATION_SUMMARY | Before/after gallery, source/file change mapping, all required evidence links, limitations and STOP handoff |

All 43 baseline files preserved; no app package or lockfile changes, paid service, optional audio or future district. Public v0.3 remains exact old artifact; v0.4 is a review candidate. Physical device FPS unmeasured.

- PUBLIC-RELEASE-004 staging: saved v0.4 HTML (10,213,265 bytes, cd238a4c) authorized for publication; no art/model regeneration. Source/GLB/textures/old showcase files unchanged; only two recorded deployment configuration changes. Site allowlist index.html/.nojekyll; public verification pending.

- PUBLIC-RELEASE-004 COMPLETE (2026-10-14T14:59:37.097480+07:00): exact reviewed v0.4 HTML is PUBLIC_LIVE_VERIFIED at https://anapaulagatti.github.io/3D-pharse5-/. Ten real public browser stages passed, actual public screenshots inspected; evidence in quality-reports/v0.4/pages-release/. All art/source/model/texture/animation/previous artifact/lockfile bytes remain intact; only two authorized deployment config changes. No new/regenerated art for publication.

## v0.5 Gate A preparation

- Archived exact user scope in docs/reviews/REFORGE_V05_USER_REQUEST.md (normalized line endings only).
- quality-reports/v0.5/preserved-v04.json:75 protected source/art/export/package/modeling/deployment hashes at verified main9cc1381. No approved asset changed.
- existing-glb-inspection.json: direct structural inspection of five actual GLBs, including12 v0.4 mascot clips and zero skins/JOINTS/WEIGHTS/morphs. v0.5 requires a new genuinely skinned human after concept approval.
- New concept art and planning outputs are not yet production meshes, Blender projects, GLBs, animation clips or actual v0.5 render proof. No new exported asset claimed at this gate.
