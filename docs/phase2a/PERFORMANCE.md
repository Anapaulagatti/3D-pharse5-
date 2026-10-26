# Texture/memory observations

24 recorded switches and a separate48-switch stability run retained one live actor, at most3 owned Phaser actor atlases,2 decoded base preview images and2 composed preview atlases. Atlas loading is lazy; planned identities have no image assets. Sparse native patch images are decoded on request, used to compose one full registered atlas, then released from application ownership. Cached variants are keyed by identity and normalized equipped IDs. Missing/invalid items fall back to original assets.

Peak observed actor RGBA estimate: **17,024,272 bytes (16.24MiB)**. A new load may temporarily stage one additional atlas before the old cache entry is pruned. For comparison only, loading twelve atlas-sized identities would require about60.53MiB for RGBA texels alone; no future six identities were produced or loaded.

These are owner/dimension estimates, not measured total VRAM. Include additional CPU image/canvas copies, CanvasTexture image-data buffers, transient patch decodes, browser caches and the unchanged frozen-world pool when budgeting a device. Shared references can appear under more than one owner. Only2 composed looks are retained; all36 combinations are validated offline without emitting eager runtime permutation atlases.

Warmup stability: retained browser JS heap changed by **238,157 bytes** between repeated24-switch schedules with the same final actor and cache counts (cached look identities differ) after explicit GC. See [raw stability](memory-stability.json) and [24-switch observations](memory-observations.json). Initial-to-warm growth includes the bounded caches; these observations do not prove every browser/GPU allocation is leak-free.

The capture environment is desktop headless Chromium. Video/readback instrumentation and software rendering affect cadence. Actual gameplay traces show all8 gait poses; this is not a target-FPS certification. Customized WebGL rendering was tested with SwiftShader, not a physical mobile GPU. **Android Chrome, iPhone Safari, sustained hardware FPS, thermal behavior and device RAM pressure remain NOT TESTED.**
