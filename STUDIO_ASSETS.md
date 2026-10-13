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

No learning-alley, celebration scene or six district assets are claimed in v0.2.0. Keep approved/successful outputs; regenerate only after a documented source change and checkpoint.
