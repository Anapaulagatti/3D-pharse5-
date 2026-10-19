# Measured performance and mobile scope

Same cloud machine, fresh Chromium per case, real keyboard motion,7.8seconds sampling with actual Phaser frame deltas/rAF/1msCPU profile. Heavy browser capture/encoding was not running during the measurements. Native render cap1024x768; mobile844x390/DPR1and3, landscape. No physical-phone/Safari/hardware-GPU or sustained60FPS certification.

| Case | Actual renderer | Measured Phaser FPS | rAF p95 ms | Visible props |
| --- | --- | ---: | ---: | ---: |
| before-Canvas | Canvas | 60.06 | 16.80 | 71 |
| before-software-WebGL | WebGL | 24.41 | 66.70 | 71 |
| after-heritage-Canvas | Canvas | 60.05 | 16.80 | 68 |
| after-namsan-Canvas | Canvas | 60.07 | 16.70 | 49 |
| after-bora-Canvas | Canvas | 60.04 | 16.70 | 26 |
| after-coast-mobile-DPR1 | Canvas | 60.16 | 16.70 | 19 |
| after-jeju-mobile-DPR3 | Canvas | 60.16 | 16.80 | 20 |
| after-software-WebGL | WebGL | 31.91 | 50.00 | 68 |

Canvas-to-Canvas is approximately equal to the preserved baseline. Forced software ANGLE WebGL remains slower; normal entry detects a software/unavailable GPU and uses Canvas, while an explicit WebGL override is available for verification. No universal speedup claim. Raw movement samples, long-task records, actual hardware/runtime details and CPU traces are in quality/performance.json and adjacent cpuprofile files.

406placements reuse103image assets and cull by current camera cell/bounds.9source material textures feed one4096x1376native tile atlas; separate object pixels are reusable. Animated water updates only visible full-water cells at180msphases; shoreline tiles remain stable.8leaves/Juni motion stop for OSreduced motion/manual pause/document visibility. Original cached-alpha occlusion and rounded follow remain; no on-frame Canvas readback substitute. Native Juni144frames/80pxbody/60walk/100run speeds unchanged.

Landscape joystick preserves deadzone/fractional strength/diagonal movement/independent held sprint/partial release. Explore/Talk/Emote, minimum44pxtouch targets, safe areas, compact HUD/minimap, portrait rotate/pause, OSmotion preference and user pause are tested at568x320,640x360,844x390,932x430andDPR3. Mobile rendering is Chromium emulation, not Android/iOS hardware or Safari certification. Orientation lock is browser-dependent; manual rotation remains usable.

Video FPS is reported separately in the real capture/encoding reports; it is not the uncaptured runtime benchmark. No fabricated/interpolated frames, speed-up or duplicated recording frames are used to claim performance.
