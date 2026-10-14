# v0.5 — Joseon Fantasy Reforge

Nari (approved concept A) replaces the main playable mascot. All v0.4 sources, Blender projects, exports, standalone HTML and its recovery tag remain available. No new learning district or backend was added.

## Source preview

Use the existing pinned installation: `npm --prefix preview run dev`. Open the Vite server with `?candidate=v05`; the legacy source viewer remains the default for recovery. Five modes: hero, third-person play, portrait, architecture, animation review. Source entry is `preview/src/reforge/App.tsx`.

## Authoring and export

The Graybox and functional Gate C assets are preserved. Art uses separate paths.

- `blender -b -t 2 --python Studio/modeling/hanok-v05.py` creates the original full Hanok source/GLB and structure/collider contract.
- `node Studio/scripts/optimize-reforge-world.mjs` constructs valid tangent frames for degenerate UV caps, performs exact weld, quantizes positions14bits/normals12bits, then welds again. Tiled UVs remain float32. KHR_mesh_quantization is supported natively by Three; no remote decoder.
- `blender -b -t 2 --python Studio/modeling/nari-v05.py -- --art` creates the separately skinned Nari art asset. Bone-heat continuous anatomy,28 joints,20 real clips,10 morphs; source weights normalized to at most4 influences. Stylized custom head normals remove the warp/voxel chin crease; geometry is not replaced with an image.
- PBR PNGs are deterministic256px original project pixels, with hashes/provenance in assets/v0.5/textures. All images are packed in Blender and embedded in GLB. v1 draft maps remain retained; v2 corrects double sRGB conversion.
- Validate/record exact source hashes: `node Studio/scripts/pack-reforge-v05.mjs` before deployment inputs change. Re-running this pre-release audit after publication intentionally fails the old workflow hash; inspect the explicitly authorized workflow change rather than updating the baseline hashes blindly.

## Build and static package

`npm --prefix preview run build` typechecks, syncs exports and builds source preview. After actual render review and a current v0.5 poster manifest: `node Studio/scripts/build-reforge-v05.mjs --candidate`, then `python3 Studio/scripts/package-reforge-v05.py`.

The standalone imports Reforge directly, embeds four verified assets (Hanok, Nari, real fallback PNG, optional original legacy mascot download), inline JS/CSS and dependency notices. Public files are ONLY index.html and .nojekyll. There are no external textures, GLBs, CDN scripts, runtime APIs or credentials. Blob assets work at the GitHub Pages /3D-pharse5-/ subpath without a Vite base-path dependency. Source .blend files and quality reports are never staged publicly by the deployment workflow.

## Quality and accessibility

Low: DPR1, no shadow pass, no environment map or point lights, world normal maps off, smaller foliage selection, bounded particles. Medium/High restore the original maps, PMREM and two non-shadowing warm lights; one shadow map1024/2048 and DPR caps1.25/1.75. Final asset budgets: world≤6MiB/80ktri; character≤3.5MiB/24ktri; source total99,308tri before Low selective detail, Low draw goal<100, shadow-inclusive Medium/High<210. Cloud SwiftShader is visibly slow at high settings and is not target-device profiling. No30/60FPS claim; QA-004 remains physical-hardware work.

Reduced motion follows OS preference and can be explicitly changed. It freezes decorative motion and samples expressive static poses. Deliberate player movement still works; pause freezes physics/mixers. Offscreen/hidden tabs suspend decorative frames and clear held input. Effects have Off/Reduced/Full controls. WebGL absence or actual context loss uses a genuine current v0.5 screenshot.

Known scope: stylized lightweight prototype, not a certified architectural reconstruction or finished full learning game. Optional audio was omitted. All earlier failed visual/test evidence is retained; final acceptance reports identify the accepted outputs.
