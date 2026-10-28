# Actual illustrated-source workflow

## Confirmed provenance and tools

[Phase1 source record](../phase1/SOURCE_PROVENANCE.md),[Phase1B source record](../phase1b/SOURCE_PROVENANCE.md),[approved Juni native reference](../../assets-src/characters/phase1/juni-style-reference.png). Juni is treated as immutable verified artwork;we do not assert an undocumented original creation method. Phase1B explicitly records independent built-in image-generated turnarounds,native finishing and authored PNG-layer animation. That confirmed workflow is the basis here.

Pinned skills read and applicable stages actually executed:

- [Sprite Forge generate2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/generate2dsprite/SKILL.md):doctor,master prompt jobs,actual host-image illustrations,selected-master keying/registration,and unmodified frame diagnostics.
- [Sprite Forge video2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/video2dsprite/SKILL.md):read;capability/FFmpeg doctor executed. AIvideo route unavailable. No `sprite_set run` or generated motion video is claimed. Explicitly authorized Phase1B own-layer rigging provides motion instead.
- [Character Animation Creator](https://github.com/tachikomared/character-animation-creator-skill/blob/9ce98dffb98c84488fe7b99b62c49fabee20abd6/SKILL.md):key-clean diagnostic,unmodified sheet/motion diagnostics. Its square-cell assumptions are not silently substituted for requested96×112. All results and limitations retained.

[Doctor](tooling/doctor.json),[doctor log](tooling/doctor.log),[video doctor](tooling/video-doctor.log),[executed diagnostic commands](tooling/execution-manifest.json),[raw Forge FAIL/WARN values](tooling/all-forge-warnings-and-failures.json),[verbatim selected-master warnings](tooling/selected-master-warnings.json). Tool clones remain pinned in `/workspace/tooling-cache`;no third-party tool source or AGPL dependency is added to the game. `master_still approve` means internal technical selection/preparation,not HUMAN artistic approval.

## Primary artwork

Seven actual `image_gen.imagegen` calls:3independent identity masters,3independently illustrated four-view source boards,1small illustrated prop board. [Exact prompt/source/reference/SHA provenance](../../assets-src/npcs/phase3a-art-rebuild/run-manifest.json). Route `host_image`. Host model/cost not exposed. No external paid image/video API,key or paid agent was used. Video-generation capability was not invented.

Juni and approved Bomi are style/proportion references,not pixel donors. No player face/costume/atlas pixels and no rejected procedural NPC bodies enter the new assets. Original generated files and copied raw masters remain immutable. Front/back/left/right are separately illustrated views in each board,not mirrored completed sprites. The high-resolution boards are NOT claimed to be native logical grids or animation sheets.

## Deliberate native finish and rig

- Inspect source ownership boundaries:explicit row splits627/640/612 avoid one view leaking into its neighbor. Remove saturated chroma alpha while preserving plum/jade/brown fabrics.
- One fixed source-to-native scale per identity,using the maximum rest-view extent so no view is enlarged above the80pxpeer envelope. Premultiplied/area BOX finish,binary alpha,shared96colour palette,no dither. No dynamic per-frame bbox fitting,upscaling,global sharpening or blur.
- Eight explicit own-palette eye-cluster retouches per identity. Static per-direction own-head translations align eye/neck landmarks without resizing heads or moving feet. Exact edits in each `native-retouches.json`;source originals retained.
- Author actual native PNG alpha masks,joints and ownership. Correct stray A-pose hands in leg masks and trouser pixels in forearms. Where a far arm is hidden,derive that arm from the SAME view's own illustrated visible sleeve/hand;not from torso,player or rejected art. Small under-arm torso recovery clones the same identity's illustrated garment only within an authored silhouette. Explicit recovery records remain in `rig.json`.
- Reuse the protected Phase1B pure PNG affine helpers. Front/back use actual approved Juni same-index foot/hand/bob landmarks. Profiles use the previously accepted44pxstance/Hermite swing logic with opposite arm swing. Only numeric direction-of-motion signs change;completed directional artwork is not mirrored. Own shoes provide lift/foreshortening. Round once at raster placement to avoid the diagnosed1.5pxdouble-rounding drift;independent resulting stance≤1px.
- Greeting and occupational activity have8distinct cells in every direction. Guidebook,espresso mug and tangerine derive from the separately illustrated prop board and are baked at the actual wrist,with back-view body occlusion. They are not floating runtime overlays.
- Export104cells/actor into the unchanged768×1456layout;keep original96×112frame names,atlas JSON,48,100anchor,clip timing,data,engine,movement and collision. Only3derived atlas/preview/provenance groups change.

[Native structural/raster audit](art-technical-qa.json),[literal own-head stability](head-stability.json),[actual world readbacks](native-render-qa.json),[supplemental inspector readbacks](inspector-native-qa.json). No successful count or automated check grants art approval.

Reproduce with Python3,Pillow12.3.0,NumPy2.3.5,SciPy1.17.0: `prepare.py` → `native_retouch.py` → `props.py` → `rig.py` → `animate.py --export` → `audit.py`/`head_qa.py`,all under `tools/phase3a-art-rebuild/`. These operate only on the3newsource namespaces and9authorized derived image/provenance files. Do not execute the rejected `tools/phase3a/art.py` for new production.
