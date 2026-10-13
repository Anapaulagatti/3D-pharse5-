# QA checklist — v0.2.0

- [x] Existing React 19 / R3F 9 / Drei 10 reused; TypeScript and Vite production build pass.
- [x] Editable arena and mascot .blend sources, original modeling scripts and packed texture sources saved.
- [x] Real raw and optimized GLBs exist; both pass Khronos Validator with 0 errors / 0 warnings.
- [x] Source/output SHA-256, actual dimensions, scene geometry, clips and provenance saved in manifests.
- [x] Optimization preserves every node's topology/bounds and exact sampler arrays; one raw/optimized Celebration browser render is pixel-identical.
- [x] Six clips generate six distinct actual poses; live animation advances and pause freezes its time.
- [x] Arena renders; scene/light/quality/POI/reset controls and repeated scene switching work with no healthy-page exceptions.
- [x] Day/night output visually inspected; low mode lowers measured render cost.
- [x] 390px phone viewport renders without horizontal overflow; actual framing inspected. This is viewport coverage, not physical-device FPS testing.
- [x] OS reduced-motion preference respected; static pose changes trigger demand rendering correctly.
- [x] Missing WebGL, context loss and a failed model request show fallback; controls remain usable.
- [x] Desktop/phone posters captured from real delivered GLBs; UI status overlay excluded from portable posters.
- [x] Transparent portrait rendered from actual model: 800×1000 RGBA, alpha range 0–255.
- [x] No external asset purchases, image scraping, backend credentials or production Korean Arena modifications.
- [x] Recovery script reuses installed dependencies, validates exports and runs build + 9 tests; temporary output stays ignored.
- [ ] Physical desktop/mobile GPU FPS targets (>=50 / >=30) verified. BLOCKED: no target hardware available; cloud software sample is ~3.3 FPS.
- [ ] Six learning districts and full final world library delivered. TODO after the first slice.

Current browser suite: **9 passed, 0 failed, 0 skipped**, including the exact render-parity assertion. Historical failed attempts are retained in initial-browser-review.json/progress history; they are not represented as current passes. OpenImageDenoise absence, Html cleanup, demand-mode invalidation and resampling differences were diagnosed and fixed for this workflow.
