# Measured scope and unresolved hardware

Two actual modern↔station roundtrips cover5344px with original controls,including historical art teardown/host restoration. Observed sampled maximum3active,4loaded,0pending;unchanged hardlimits4/4/2. Loaded NPC texture estimate peaks at17891328bytes (17.06MiB),not all26atlases preloaded. Each768×1456RGBA atlas estimates4,472,832decodedbytes;this excludes temporary decode/inflight/browser/GPU overhead. Heap endpoint range18676976–24536294bytes is sparse shared-host telemetry,not a leak proof.

Actual180RAFcallback intervals:p50=16.7ms,p95=16.7ms,max=16.8ms. Shared cloud Chromium callback cadence is not certified presentationFPS or physical mobile performance. Actual sprite/native fidelity is proven separately by PNGreadbacks,not timing.

Eight same-context switches,all six approaches,zone exit/re-entry and offline-package playback are checked. Twelve original players and28cosmetics/46variants retain their previous lazy/bounded lifecycle;world chunk budget/camera/tour remain unchanged. No second actor engine or eager26texture preload.

SoftwareWebGLSwiftShader2native draws are a compatibility smoke only. Physical AndroidChrome/iPhoneSafari,real GPUmemory/battery/thermal,low-enddevice stability and long-session hardware testing:NOTTESTED. Prior motion/Forge warnings are retained. No device PASS is inferred from browser emulation or successful build.
