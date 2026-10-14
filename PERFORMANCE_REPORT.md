# Performance report — first slice v0.2.0

Actual exported files and rendered costs, not assumed frame-rate claims.

| Model | Optimized bytes | Scene-instance triangles | Model draw primitives | Clips | Validator errors / warnings |
|---|---:|---:|---:|---:|---:|
| arena-hero | 3,379,732 | 89,012 | 29 | 1 | 0 / 0 |
| mascot-base | 289,652 | 10,026 | 36 | 6 | 0 / 0 |

Both models meet the provisional file-size budgets (arena <=4 MB, mascot <=1 MB). Embedded original textures are 256×256 PNG, sRGB. Animation key samples, named-node topology and world bounds are preserved exactly by optimization. No mesh simplification, texture recompression or required Draco/meshopt decoder. Static serialized mesh totals can decrease with dedup; instance counts above describe rendered geometry.

Observed full-scene costs at 844×490 drawing-buffer size:

- Medium: 152 draw calls / 198,618 triangles including shadow passes; 6 GPU textures reported.
- Low: 69 draw calls / 99,544 triangles; shadows, extra night point lights and paper motes disabled.
- On-demand rendering stops decorative loops for reduced motion, pause, offscreen view and hidden tab. Six static clip poses are available.
- First measurable budgets: <=4 MB arena, <=1 MB mascot, <=120,000 triangles and <=80 draws in low; <=180 draws including shadows in medium; texture dimensions <=1024 (current originals 256).

Short measured headless Chromium 154.0.8037.57 SwiftShader samples, 1280×1000 browser viewport:

| Quality | Observed software FPS | Frames / sample seconds |
|---|---:|---|
| Medium | 3.27 | 5 / 1.528 |
| Low | 3.32 | 5 / 1.505 |

Software rendering in this cloud instance is slow: approximately 3.3 FPS. Lowering draw cost did not materially improve this short sample. This is an actual limitation, not a passing 30/60 FPS result. These samples are not sustained, hardware-GPU or physical-phone benchmarks. Physical device profiling and possible geometric LOD/baked lighting remain QA-004. Use static posters where the real device cannot render comfortably.

The lazy 3D JS chunk is approximately 1,006.68 kB minified / 269.87 kB gzip; app shell 239.27 kB / 75.31 kB gzip. Vite warns about the large engine chunk. Further bundling and real-device profiling remain outside the first art-delivery scope.

Evidence: quality-reports/renderer-desktop.json, renderer-low.json, software-benchmark.json, GLB validation reports, current manifest, browser captures and nine passing smoke tests. No claim of measured physical-device acceptance or full production performance is made.

## Living Hanok v0.3 candidate

Original v0.2 model/source/export bytes remain unchanged. The new original additive layer costs 527,852 bytes, 13,312 triangles and 21 primitives; no new textures or required decoders. Combined arena + detail GLBs total 3,907,584 bytes, below the original 4 MB arena budget. Static props share material primitives, foliage uses three wind pivots, paper/motes/petals use instancing. An invisible raycast-only tree hit area does not draw.

Actual production diagnostics at 872×560 CSS pixels, captured in quality-reports/v0.3/final-render/verification.json:

| Quality | Render calls | Triangles including applicable shadow passes |
|---|---:|---:|
| Low | 91 | 112,697 |
| Medium | 180 | 225,327 |

Low meets the existing <120,000-triangle budget; the new detail layer raises draws above the old 80-call low provisional target. Medium meets the existing <=180-call target. These are observed costs, not physical-device FPS acceptance. Default phones use Low, no shadow pass, DPR 1; Medium/High DPR caps are 1.25/1.75 instead of the earlier 1.5/2. Limited non-shadow point lights and no bloom/postprocessing. Both higher tiers were actually rendered during verification.

The self-contained review HTML is 8,213,753 bytes; compressed HTTP ZIP is 3,076,718 bytes. It embeds eight checksum-verified original assets and dependency notices. No external asset/CDN request is needed by the app. A browser clip shows real-time software-GPU movement; encoded video FPS must not be represented as actual GPU FPS. Hardware/phone profiling remains QA-004, and existing SVG/PNG fallback remains available.

## v0.4 measured render costs

Production final-render/verification.json: Low 115 calls / 131,121 triangles; Medium and High 228 calls / 262,175 triangles including shadow passes. Scene uses preserved base arena + v0.3 details + v0.4 narrative layer + new mascot; static details merged by material, 3 new independent canopy clusters, particles instanced. Hidden alternate face meshes skip browser draws. Low disables shadows and extra atmospheric particle layers; phone defaults Low/DPR1, Medium DPR≤1.25, High≤1.75/2048 shadow map.

Compared with v0.3 Low 91 calls/112,697 triangles, the increase is 24 calls/~18.4k triangles for the larger detail canopy/architecture and expressive character. This exceeds the original provisional 80-draw ambition; functional QA enforces a current v0.4 ceiling of 135 draws/155k Low triangles. World GLBs together are 4,707,444 bytes (~4.49 MiB), so the older 4MB world budget is exceeded explicitly; no hidden optimization claim. New detail bands use 24 rather than 64 segments (25,792→18,112 new-layer triangles, 989,304→799,860 bytes). No large new texture, decoder, HDRI, bloom, audio or dependency added.

Versioned mascot GLB: 696,568 bytes/11,074 triangles/47 source primitives/12 native clips. Required constant face/pose channels retained as minimal keys; never remove their semantics for size. Narrative GLB: 799,860 bytes/18,112 triangles/20 primitives/CanopyWind. Saved standalone HTML 10,213,265 bytes; review ZIP 3,645,525 bytes; dependencies/libraries/license bytes embedded for reliable offline/subpath loading.

Actual screenshots, moving mixer/pixels, native actions, camera focus, pause/OS/offscreen and 390×844/fallback checks executed on cloud Chromium SwiftShader. Real timestamp compositor video is presentation evidence, not measured hardware FPS; software capture may stutter. Physical phone/desktop GPU FPS remains unmeasured (QA-004); no 60 FPS claim. Wider device profiling/true geometry LOD remains future work, not a completed test.
