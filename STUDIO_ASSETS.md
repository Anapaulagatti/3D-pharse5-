# Pixel asset registry

3D assets: removed from pixel working tree only; complete archive inventory/SHA256 in docs/migration/3d-archive-proof.json. Immutable old release kept outside build at showcase-v0.5.

Original pixel sources: assets-src/directions.json, layout.json, plaza.tmj, per-direction indexed PNG masters and tools/export_art.py. Derived PNG atlases/Phaser frame JSON,tiles/props and direction sheets: public/assets. Hash/provenance/license: assets-src/manifest.json. REVIEW_CANDIDATE_NOT_APPROVED. Code-authored,no image model, no licensed third-party artwork. Actual rendered evidence not created yet.

Gate1 runtime checkpoint: Phaser4.2.1 production builds and real tilemap/sprite/Arcade collision, four-direction walk/run, dialogue, OS-reduced motion, native Chromium touch and real Canvas fallback executed. Initial browser suite fails only missing favicon404; retained attempt-1 evidence, fixing favicon and mobile framing before final PASS. First actual render inspected: source remains crisp, phone roof framing requires upward follow offset. Three art directions now receive distinct character/roof treatments. Next: final render regression + media/clean install.
