# V4 measured artifact/runtime facts

Static build 1666980bytes; original pixel data 174461bytes across28files; ZIP 474901bytes. JS 1482513rawbytes; Python-computed theoretical gzip 383931bytes, not network transfer. Six512×1024RGBA avatar textures imply approximately12MiB base-level GPU allocation before driver overhead; actual device VRAM unmeasured.64prop sprites/65colliders; few ambient paper marks; no external audio/backend/ad SDK.

Actual Chromium/WebGL and forced genuine Canvas fallback tested.288CDP compositor frames/22.87s with original timestamps; phase frame counts/elapsed time are recorded in motion/capture.json. Capture samples include encoding/IPC/software-renderer overhead and are not a60FPS claim. Native browser suite3flows took21.62s, emulated phoneDPR1/2, not real-device certification. No load/multiplayer test claimed.

Measured first idle phase under cloud SwiftShader screencast: engine frame counter advanced150frames over6.003wallseconds, observed24.99engine frames/s. This is the actual capture session, with capture overhead, not a device performance guarantee.
