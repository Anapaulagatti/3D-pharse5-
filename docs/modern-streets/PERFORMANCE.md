# Measured performance

Uncaptured fresh cloud Chromium, four paired comparisons/eight cases and7.8seconds of real input per case;1msCPU sampling. No capture/encoder concurrently. These are short cloud samples, not physical-phone/hardwareGPU or sustained60FPS claims.

| Case | Actual renderer | Measured Phaser FPS | rAF p95 ms |
| --- | --- | ---: | ---: |
| before-urban-Canvas | Canvas | 60.14 | 16.80 |
| after-urban-Canvas | Canvas | 60.01 | 16.70 |
| before-urban-software-WebGL | WebGL | 21.83 | 66.70 |
| after-urban-software-WebGL | WebGL | 23.17 | 66.70 |
| before-park-Canvas | Canvas | 59.91 | 16.70 |
| after-park-Canvas | Canvas | 60.14 | 16.80 |
| before-coast-mobile-DPR3 | Canvas | 60.08 | 16.70 |
| after-coast-mobile-DPR3 | Canvas | 60.18 | 16.80 |

Canvas uses1024x768desktop/844x390emulated landscapeDPR3; softwareWebGL is explicitly forced ANGLE Swiftshader, automatic compatibility fallback remains Canvas and was separately tested with actual --disable-webgl. No new renderer optimization or speed promise; scenery counts/culling/physics/Juni stay fixed. Native 5205tile atlas4096x1312 remains below4096texture limit. Flush infrastructure is baked into ground,0extra props/lights/draw calls.

Raw frame deltas/rAF/sample timings/CPU profiles and input hashes are in quality/performance.json and *.cpuprofile. All8cases had0browser errors.
