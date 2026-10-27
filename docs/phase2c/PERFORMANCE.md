# Performance and memory

## Observed desktop session

[Raw long session](long-session.json): actual Chromium Canvas,60 genuine character switches,100 cosmetic preview/apply operations,82 resource snapshots, one active player throughout. Repeated presets, cancel, return and reload preserved position, real visited state and a learning-progress sentinel. This is not physical-device certification.

| Measurement | Observed |
|---|---|
| Character switch UI latency | median296ms /p95381ms /max432ms |
| Cosmetic preview→apply latency | median337ms /p95495ms /max596ms |
| Active/resident character textures | ≤3; unique keys |
| Base image cache | ≤2 |
| Composed atlas cache | ≤2 |
| Maximum resident character texture estimate |20,107,056bytes |
| Maximum base image estimate |11,863,312bytes |
| Maximum composite image estimate |13,404,704bytes |
| Observed JS heap range |65,941,976–123,818,877bytes |
| Final JS heap after reload |72,379,084bytes |

UI latency includes loading, decode, composition, UI scheduling and upload orchestration. Synchronous Canvas draw-loop samples are separately recorded in resource snapshots (bounded60samples); they exclude network/decode and do not measure GPU completion. JS heap is not decoded-image memory. Estimates are per-owner width×height×4, may include duplicate ownership of shared resources and must not be summed as measured GPU memory. Heap fluctuation and one bounded session do not prove indefinite leak freedom.

## Architecture

Only selected actors and requested compatible appearances load. Character image previews decode lazily; category thumbnails use lazy loading. Base and composite caches are independently bounded2 each; existing Phaser asset manager bounds resident character textures3. Selecting a new combination does not eagerly generate other combinations. Revision and actual-base-digest keys invalidate affected results without a global cache flush; selective character invalidation is available. Temporary composition canvases are released on failure/abort; stale UI jobs are aborted/token-guarded. Atlas/PNG owners retain only bounded completed resources.

New sparse asset directory is about4.4MiB on disk; that is compressed/source size, not total decoded memory. No12-base preload or huge prebuilt permutation atlas is introduced. Existing world chunk cache/budget is unchanged.

## Renderer and mobile status

Canvas native gameplay and actual SwiftShader WebGL upload/render smoke both passed independent native pixel readback. [WebGL evidence](webgl-evidence.json) explicitly identifies software rendering; observed cadence there is not hardware FPS. No GPU, thermal, sustained Android/iPhone memory or performance acceptance is claimed.

667×375 and844×390 landscape browser checks confirm native96×112 preview, reachable primary controls, no horizontal overflow and isolated touch gestures. Action selection collapses to a44px native control on small screens; it does not change the gameplay camera. Physical Android Chrome/iPhone Safari remain NOT TESTED. [Device handoff](DEVICE_REVIEW.md).
