# Performance and cache observations

Actual production-browser observations cover initial load, all12 gallery previews,60 committed identity switches (five complete rotations), gameplay, reload and Studio reopen. One live player Sprite persisted. The existing limits remained:3 Phaser actor atlases (+1 temporary staging load),2 decoded base preview atlases and2 composed cosmetic atlases. Twelve-card portraits are small separately lazy-loaded PNGs; only the selected preview loads a full atlas. The initial world requested only Juni's full atlas, not all12.

Peak observed actor RGBA estimate: **17,024,272 bytes (16.24MiB)**. These are dimensions/owner counts, not total VRAM. Include CPU decoded image copies, canvas buffers, browser caches and the unchanged world pool in a real-device budget. A temporary incoming atlas can coexist before LRU eviction. The unchanged compositor remains lazy/bounded; no wardrobe permutations were eagerly built.

Retained browser JS heap changed by **885,220 bytes** between switch36 and60 after explicit GC. This observational growth includes whole-app state; it is not a zero-growth claim or hardware leak certification. [Raw stages and counts](memory-stability.json) include preserved old Ara preset data before/after reload.

Six new canonical station tests, mobile joystick and the two representative bridge traversals use the actual game. [BridgeA](bridge-regression/body-clearance.json) was walked by Nari out/return; bridgeB was run by Hyunwoo out/return. No speed, camera, collision or position override was used. All12 were switched through the real Studio UI. These are functional observations, not sustained target-FPS certification.

Native WebGL was exercised with desktop SwiftShader. **Physical Android Chrome, iPhone Safari, hardware WebGL FPS, thermal behavior and real device RAM pressure remain NOT TESTED.** The world/camera/tour implementations are unchanged. No unverified physical-device PASS is claimed.
