# Setup validation — 2026-10-13

Scope: initialize `Anapaulagatti/3D-pharse5-`, preserve uploaded documents, prepare the independent 3D Studio toolchain and a functional procedural demo. The attached master prompt is saved as project documentation; its five art-production stages have not been completed by this setup.

## Verified in this cloud instance

| Check | Result |
|---|---|
| Node / npm | 24.19.0 / 11.9.0 |
| React / R3F / Drei | 19.3.0 / 9.8.1 / 10.7.9; `npm ls` completed, no peer-dependency errors |
| Three.js | 0.186.1 |
| Vite / TypeScript | 8.3.4 / 5.9.3 |
| Blender | 4.3.2, background mode; GLB export and editable `.blend` saved successfully |
| glTF Transform / gltfjsx | 4.5.1 / 6.5.3; inspect, optimize and TSX generation completed |
| Khronos Validator | 2.0.0-dev.3.10; original and optimized GLB both 0 errors, 0 warnings |
| Frozen reinstall | `bash Studio/scripts/setup.sh` completed successfully after initial install; uses `npm ci` for both packages |
| Typecheck + production build | Passed |
| Browser smoke suite | 5 passed, 0 failed, 0 skipped; Chromium 154.0.8037.57, headless SwiftShader |

Browser checks exercised actual WebGL rendering, scene switching, light/quality/mood controls, pause, camera reset, a 390px phone viewport, reduced motion preference, missing WebGL and context loss fallback. Screenshots were inspected to confirm visible geometry, rather than relying on a port or canvas element alone:

- [Desktop](preview-desktop.png)
- [Phone viewport](preview-mobile.png)
- [WebGL unavailable](preview-fallback.png)

Toolchain test fixture: 7,428-byte GLB before optimization; 6,076 bytes after conservative optimization, 151 vertices and 224 triangles in both. No required extensions or decoders. Unused UVs were removed because the fixture has no textures. This verifies tooling on a static fixture, not animation/rig/texture parity for future assets. Saved Validator outputs: [original](toolchain-validation.json), [optimized](toolchain-validation-optimized.json).

## Limits and next work

- Blender is installed on the cloud machine, not on the user's own computer. No cloud DISPLAY/desktop session; the GUI was not exercised.
- Blender's optional Draco export library is absent. Standard GLB export works, and tested optimization deliberately adds no Draco/meshopt/texture decoder requirements.
- Three/R3F emits Clock and shadow-map deprecation warnings; the tested rendering path works with Three's supported fallback. No page exceptions in the interactive control test.
- Vite reports a large lazy-loaded 3D engine chunk: approximately 933 kB minified / 248 kB gzip. This is a foundation demo, not final bundle-performance hardening.
- No physical phone or hardware-GPU FPS measurement; the phone result is viewport coverage only. No 30/60 FPS claim.
- Preview geometry and fallback SVG are original procedural studies. Asset-production, mascot selection, polished animation, licenses/manifest completion and `exports/v1` remain future work. `ASSET_MANIFEST.csv` stays the provided empty template. Smoke `.blend`/GLB/TSX outputs are ignored fixtures in `Studio/.cache/`, not final assets.
- No production Korean Arena repo, backend or credentials were needed. External framework source repos were not cloned; the requested tools were installed as packages.

GitHub delivery and cloud publication are separate from these runtime checks. Environment draft saving does not publish the environment, and fresh-task snapshot restoration has not been independently tested.
