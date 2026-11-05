# Performance — measurements and limits

- Actual extracted candidate at960×700, ChromiumCanvas:37textures,43,279,548bytes RGBA(width×height×4) estimate; player6,702,352bytes, NPCpool8,945,664bytes at2loaded/0pending, existing4texture/2loadlimits. No twelve-character eager preloading.
- Eight physical seed-shop entry/exit cycles: texture count delta0, estimated decoded bytes delta0. This short bounded observation is not a memory-leak guarantee. BrowserJSheap is nonstandard, notGPU/processresidentmemory.
- Separate AUTO startup reportsWebGL,15currentlyloadedtextures/24,915,436estimatedbytes atsampletime; different asynchronousloadtiming/location, not claimed renderer-memoryoptimization or a deviceGPUbenchmark.
- DEVICE_QA.json:3DPR/viewport emulations, ~2.2secondRAF samples median16.7ms/p9516.7ms. These cloudbrowser short samples do not certify60FPS, mobiletemperature/battery/GPU or lowmemory resilience.
- Main JS2,017.61kB minified (~486.12kBgzip); chunk warning retained. No blanket heuristic or check disabled.
- PhysicalAndroidChrome/iPhoneSafari/hardwareGPU: NOTTESTED. No hardwareperformancePASS.
