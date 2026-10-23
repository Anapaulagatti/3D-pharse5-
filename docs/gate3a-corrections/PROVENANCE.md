# Source, preservation and reproducibility

Authority: [targeted correction directive](../current/G3A_TARGETED_CORRECTIONS.md). Starting commit602476d359e9b485ff455062a8d4652932bd4eaa is preserved by`checkpoint/gate3a-before-targeted-corrections-20261023`. Approved district source remains01f4f954771595061d31cf2e8f53d49ce52910a0 and`checkpoint/gate25-final-approved-20261022`. Gate1 and all prior tags remain intact.

The 1,341 SHA256 entries in`docs/gate3a/protected-assets.json` cover approved art/source/Juni and shared prototype code. Verification has no changed protected input. The expanded Gate2.5 source plan and default G3 world/district ground, masks and objects are unchanged. `production-plan-v2-candidate.json` references the immutable plan and the separate proposal; it does not apply an amendment.

The six technical facade derivatives come from`assets-src/gate25-station-planters/final-clean-ground.png`, using the existing final architecture-protection polygons from`assets-src/gate25-reconstruction/architecture-envelopes-final.json`. Extraction changes alpha ownership only; owned RGB pixels are copied exactly. No resize, palette conversion, recoloring, source repaint, paid API or image generation is used. Transparent RGB is cleared. Original source files remain intact. These conservative ownership cuts include source context and exposed party walls: they are technical registration artifacts, not approved finished modular artwork.

The station canopy is separately owned, with original native pixels and depth 2649. Main station body depth2590 and corrected planter depth2691 are independent. Corrected planter PNGs and their approved forecourt/contact-shadow source pixels are reused. The new candidate logical station anchor/collider remain unchanged; the explicit0.5px source pivot is subject to human approval.

`tools/g3a_registration.py` produces only the candidate manifest, local technical ground/foot fields and extracted facade components. Ninety world ground chunk positions are retained;23 changed engineering ground/mask pairs live in the separate registration directory and all other pairs reference existing files. The offline logical canvas is not a runtime texture. Runtime source chunks remain at most512px per axis; native facade textures keep their actual dimensions. The small overview is deliberately downsampled and never used for pixel-quality assessment.

Shared original Juni motion, atlas, joystick and Gate2 camera/tour files remain unchanged. Only the G3 adapter/runtime is instrumented/optimized. Diagnostics are opt-in via`profile`; `baseline` reproduces the measured earlier hot paths, `unculled` isolates final render-culling changes. Current optimized behavior is the default. Source image/collision APIs and context-restoration ownership remain with Phaser4.2.1; a synchronous scoped filter guard in NativeTexture prevents redundant identical filter uploads and restores the renderer method immediately.

Native PNG captures are actual Phaser WebGL screenshots with zoom1 and DPR1. Readback matches12 visible opaque source regions exactly, and both original district planters match their approved native composite. Juni/overlapping later objects are excluded from facade comparisons. JPEGs are lightweight review copies, not pixel-test inputs. Context-loss proof compares over 1.13 million non-Juni screenshot pixels before/after software WebGL restoration.

`tools/g3a_diagnostics.mjs` records controlled non-video trials; the initial exploratory pilot is retained separately as diagnostics-before.json. The baseline/optimized trial pair uses a shared instrumented build; its compressed bundle and SHA256 are recorded for provenance. Stage2 culling is a separate controlled ablation on its recorded instrumented build. Traces are separate overhead-bearing investigations; traversal MP4s are input recordings and contribute no benchmark samples.

Reproduce with Node24/`npm ci` and Python dependencies from`tools/gate3-requirements.txt`:

```
python3 tools/g3a_registration.py
python3 tools/g3a_validation.py
python3 tools/g3a_registration_evidence.py
npm run typecheck
npm test
npm run lint
npm run format:check
npm run assets:check
npx vite build --config gate3.vite.config.ts
python3 tools/g3a_package.py
python3 -m http.server 4271 --bind 127.0.0.1 --directory dist-gate3
```

In another terminal run capture, controls, trace, culling and validation scripts from`tools/g3a_*.mjs` individually. For the controlled matrix: `G3_PORT=4271 G3_VARIANT=baseline node tools/g3a_diagnostics.mjs`, then `G3_PORT=4271 G3_VARIANT=optimized node tools/g3a_diagnostics.mjs`. The current optimized replay includes final culling; the supplied first-stage raw matrix predates that final ablation. Performance varies by host; no historic timing is asserted reproducible bit-for-bit.

Recording requires Chromium at`/usr/bin/chromium` and Playwright's compatible FFmpeg, or the installed`/usr/bin/ffmpeg` mapped to`/tmp/gate3-playwright/ffmpeg-1013/ffmpeg-linux`. Run`PLAYWRIGHT_BROWSERS_PATH=/tmp/gate3-playwright node tools/g3a_traversal.mjs`; convert the three`/tmp/g3a-*.webm` files to H.264 with FFmpeg. Capture/check original-resolution images using`g3a_capture.mjs`, `g3a_pixel_proof.py` and the context-restore scripts. No unrecorded art session is required.

No Gate3-B mass art, main merge, public site or separate application change is included. Physical Android Chrome/iPhone Safari remain NOT TESTED.
