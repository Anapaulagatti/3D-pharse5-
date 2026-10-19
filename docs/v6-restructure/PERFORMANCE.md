# Measured V6 performance

Actual Phaser frame deltas and rAF intervals during7.8s of real movement;1ms CPU profiling identical per case. No video/encoder runs concurrently. Separate fresh browser per target. Canvas explicitly selected for baseline and candidate; WebGL explicitly forced only in named WebGL cases; default software-GPU fallback is tested separately in browser tests. Canvas default compositor; explicit software ANGLE Swiftshader only for WebGL cases. Mobile844x390DPR1/3 is emulated; same actual keyboard movement across baseline/candidate, not physical device. Same desktop native1024x768 baseline vs candidate; no universal FPS improvement claim.

| Paired case | V4 FPS | V6 FPS |
| --- | ---: | ---: |
| urban-Canvas | 58.51 | 53.68 |
| urban-software-WebGL | 11.12 | 14.66 |
| park-Canvas | 57.54 | 59.02 |
| coast-mobile-DPR3 | 60.10 | 59.92 |

These are short uncaptured cloud-Chromium samples with1msCPUprofiling, not physical Android/iOS/Safari or hardware-GPU results. V6 urban Canvas is slower in this sample; park improves slightly and emulated mobile is similar. No uniform improvement or universal60FPS claim. Forced software WebGL remains slow; production automatically uses Canvas when WebGL reports software GPU or is unavailable, with an explicit Canvas option. The forced WebGL result is still disclosed.

Host CPU: INTEL(R) XEON(R) PLATINUM 8573C; logical CPUs: 5. Actual poses, native canvas dimensions, frame deltas, rAF p50/p95/p99, long tasks and raw1ms CPUprofiles are saved under quality. V4/V6 layouts differ, so local landmark-facing poses differ and are explicitly recorded. Each case opens a fresh browser. No video recording or encoding ran concurrently.

Geometry remains reused/native:497props/108images,552static bodies versus V4 438/109/653. Existing camera-culling/cached alpha masks/visible-water-only updates are retained; no high-resolution texture/character regeneration. New worldheight5312supports visible-water range to row166. No new runtime dependencies.
