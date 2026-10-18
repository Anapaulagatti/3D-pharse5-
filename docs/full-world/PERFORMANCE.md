# Measured performance / limitations

Fresh Chromium per case, same7.8s real keyboard movement,1msCPU profiling, no capture/encoder concurrently; actual Phaser frame deltas and rAF timing, not video settings. Hardware: {'cpu': 'AMD EPYC 9V74 80-Core Processor', 'logicalCPUs': 5, 'platform': 'linux', 'node': 'v24.19.0'}. Native desktop1024x768, mobile844x390, DPR1/3 emulated.

| Case | Actual game FPS | rAF p95 ms | Renderer |
|---|---:|---:|---|
| before-software-WebGL | 24.62 | 66.60 | WebGL |
| before-Canvas | 60.07 | 16.80 | Canvas |
| after-default-heritage | 59.83 | 16.70 | Canvas |
| after-default-festival | 60.14 | 16.70 | Canvas |
| after-default-coast-mobile-DPR1 | 60.05 | 16.80 | Canvas |
| after-default-jeju-mobile-DPR3 | 60.10 | 16.80 | Canvas |

The new default selects Canvas when software GPU is identified, avoiding the observed software-WebGL bottleneck. Compared with the preserved baseline already forced to Canvas, performance is approximately equal near60on this machine; no universal speedup is claimed. Hardware/unknown GPU keeps AUTO/WebGL, manual override retained.296props are culled by camera/cell with margin; native render capped1024x768 independent of DPR; cached approved alpha occlusion avoids readback during movement. Camera follows rounded roots; analog adapter preserves approved speed/acceleration/144sprite frames and uses actual physics velocity. Water updates every480ms; eight region-anchored leaves, all pause/reduce-aware.

Raw frame/camera/animation samples and CPU profiles:quality/performance.json and corresponding .cpuprofile. No critical errors in the six measured cases. These are short cloud-Chromium measurements, NOT physical Android/iOS/Safari/hardware-GPU benchmarks or guaranteed sustained60FPS. Runtime during capture and actual encoded VFR throughput are reported separately in each clip verification JSON. No frame interpolation, retiming or FPS metadata used to fabricate smoothness.
