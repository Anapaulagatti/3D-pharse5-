# NPC performance and memory

Initial observed load: 1527ms.12realzonecycles and60actualdialogues;88resource snapshots. Observed JS heap range56,596,411–70,170,599bytes; this is JS heap only.

[Long-session raw observations](stability.json) · [loading/cadence/tour observations](performance-observations.json) · [all-region gameplay traces](gameplay/actual-gameplay.json) · [cross-zone trace](cross-zone-actual.json).

## Bounded ownership

All14definitions/state records stay available; relevant home zones activate only up to4nearest NPCs. A talking actor is prioritized within that same cap. At most4native NPC textures and2concurrent loads; no duplicate IDs/keys. Each768×1456RGBA atlas estimates4,472,832bytes;4resident atlases estimate17,891,328bytes per texture owner. Browser-decoded image and GPU ownership are separate and must not be summed as measured totalGPU memory. Fourteen eager atlases would estimate62,619,648bytes,which the runtime does not preload.

Camera culling hides offscreen actors/shadows. Visible simulation ticks around50ms; offscreen active simulation is coarser250ms. Inactive zones freeze models; no full-world NPC pathfinding runs per frame. Bounded histories,retry/backoff,request cancellation and shutdown cleanup prevent repeated entry creating orphan actors. The source asset pool shares one cache across residents and never removes player/Studio/world keys. Dialog previews reuse loaded native atlases without another portrait decode.

The world’s existing64MiB chunk budget and character/composite cache policies remain unchanged. NPC estimates are separate,not a new claim about total browser/GPU memory.

## Measurement limits

Actual environment: systemChromium,headless desktop,Canvas; shared cloud host with possible concurrent QA/encoding. Frame/update intervals and browser RAF callback cadence are reported as observations,not certified presentation FPS. JS heap fluctuates with garbage collection; bounded counts and one extended session do not prove indefinite leak freedom.

Software SwiftShader WebGL uploads/rendering passed native readback for2residents. This is not hardware FPS,GPU-memory,thermal or Android/iPhone certification. Browser landscape667×375/844×390 validates functional layout/input only. Physical Android Chrome,iPhone Safari,notch hardware and sustained device performance: NOT TESTED.

ScenicTour is separately checked to return to the exact original player position,with NPC simulation suspended appropriately. Historical renderer/performance/motion warnings remain recorded in earlier reports and are not erased by Phase2C approval.

## Actual desktop probe

Observed initial ready time: 2531ms. These shared-host measurements are observations,not hardware certification.

| Stage | RAF samples | p50 ms | p95 ms | NPC sim updates | NPC animation updates |
|---|---:|---:|---:|---:|---:|
| idle with2actualresidents | 241 | 16.70 | 16.70 | 136 | 43 |
| original keyboard exploration and followcamera | 61 | 16.70 | 16.80 | 34 | 14 |
| ScenicTour camera motion withNPCsimulation suspended | 358 | 16.70 | 16.70 | 0 | 0 |
| return to original player | 180 | 16.70 | 16.80 | 108 | 44 |

ScenicTour returned to exact original player coordinates: `[2125.0031999999837, 1096]` → `[2125.0031999999837, 1096]`. Physical/hardwareGPU status stays NOT TESTED.
