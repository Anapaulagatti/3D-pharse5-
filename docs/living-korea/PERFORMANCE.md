# Measured runtime performance

Actual Phaser frame deltas and rAF intervals during7.8s of real movement;1ms CPU profiling identical per case. No video/encoder runs concurrently. Separate fresh browser per target. Canvas default compositor; explicit software ANGLE Swiftshader only for WebGL cases. Mobile844x390DPR1 is emulated real-CDP-touch, not physical device. Same desktop native1024x768 baseline vs candidate; no universal FPS improvement claim.

{'cpu': 'AMD EPYC 9V74 80-Core Processor', 'logicalCPUs': 5, 'platform': 'linux', 'node': 'v24.19.0'}

| Case | Actual Phaser FPS | rAF p95 ms | rAF p99 ms | Visible / total props |
|---|---:|---:|---:|---|
| baseline-desktop-Canvas | 60.09 | 16.70 | 16.80 | 77/149 |
| north-desktop-Canvas | 60.07 | 16.70 | 16.80 | 81/144 |
| namsan-desktop-Canvas | 60.13 | 16.80 | 16.80 | 31/35 |
| namsan-mobile-landscape-Canvas | 60.12 | 16.70 | 16.80 | 24/35 |
| north-software-WebGL | 22.13 | 66.80 | 83.40 | 82/144 |
| namsan-software-WebGL | 23.85 | 66.70 | 83.40 | 31/35 |

Identical1msCPU profiling, fresh browser per case and no concurrent video/encoding. Desktop baseline and new north both use native1024x768Canvas; mobile844x390is touch emulation, a different viewport and not directly comparable to desktop. Each measured window is about7.8seconds, not a long thermal/device benchmark. Scene culling, geometry and original per-frame alpha cache are retained. DPR3 layout checks cap native rendering cost; no high-DPI blanket upscale.

The cloud has software ANGLE Swiftshader for forced WebGL. Its22–24FPS cases are slow; use the explicit Canvas fallback for review. Automatic WebGL availability fallback is retained, but software-GPU slowness is not automatically detected. No hardware-GPU/physical-phone/iOS performance guarantee or universal60FPS claim.

Raw samples, bundle hashes and all six CPU profiles are in quality/performance.json and *.cpuprofile. Actual gameplay/capture FPS is recorded separately in capture.json and video-verification.json, never inferred from encoder metadata.

## Capture is separate

Whole-browser MP4: 9282actual frames /155.311s, 59.76FPSaverage VFR. All source CDP frames retained; max relative PTS error 0.500ms. Original simultaneous native VP9 has8888decoded frames, 57.23FPSfirst/last average; its missing container-duration metadata is documented. During simultaneous recording/screencast the measured Phaser frame rate was 59.82, not inferred from video. These observations are not constant60FPSfootage or device certification. Actual browser decoding/playback/seek and changed decoded pixels pass in video-playback.json.
