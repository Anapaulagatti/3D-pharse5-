# Performance observations

Actual Phaser frame deltas and rAF intervals during7.8s of real movement;1ms CPU profiling identical per case. No video/encoder runs concurrently. Separate fresh browser per target. Canvas explicitly selected for baseline and candidate; WebGL explicitly forced only in named WebGL cases; default software-GPU fallback is tested separately in browser tests. Canvas default compositor; explicit software ANGLE Swiftshader only for WebGL cases. Mobile844x390DPR1/3 is emulated; same actual keyboard movement across baseline/candidate, not physical device. Same desktop native1024x768 baseline vs candidate; no universal FPS improvement claim.

| Target | Before | V4 |
| --- | ---: | ---: |
| urban-Canvas | 60.09 FPS | 59.79 FPS |
| urban-software-WebGL | 22.65 FPS | 23.12 FPS |
| park-Canvas | 59.88 FPS | 60.11 FPS |
| coast-mobile-DPR3 | 60.11 FPS | 60.07 FPS |

Actual cloud Chromium/Canvas and explicitly forced software ANGLE; eight fresh-browser7.8second samples,1msCPU profiling, real movement, no capture/encoding concurrent. The recording rate is a separate metric. Existing software-GPU Canvas fallback retained. Physical phones/iOS/Safari/hardwareGPU and universal60FPS are not verified. No universal speed improvement is claimed.

32new small sprites and static feet,6new reused PNGtextures; no new lights, particle systems, AI or simulation loop. Active props in sampled urban area30→41, park25→39, emulated coast19→27; unchanged culling/alpha cue/world dimensions/camera/native1024×768cap. Six tiny art modules share existing palette; atlas4096×1312/5208unique tiles, three additional unique tiles versus the previous5205, with the same atlas dimensions.

Profiler URLs measured the correct old modern-streets and new V4 entries; an inherited input-file metadata list was corrected after measurement to those unchanged frozen bundle hashes. Raw observations/CPU profiles are retained; no measurements or runtime bytes changed.
