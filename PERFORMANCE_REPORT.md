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
