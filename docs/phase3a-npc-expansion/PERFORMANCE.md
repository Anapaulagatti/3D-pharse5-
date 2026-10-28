# Measured runtime scope and unresolved hardware

Same NPC asset pool/model/FSM:4active,4loaded atlas textures,2in-flight loads.20metadata/actor records are not20loaded textures. Visitors use deterministic90s windows including a resident-only window;selection is held during a region stay and re-evaluated on re-entry. The chosen visitor replaces its host slot,preventing same-route stacking;talking actors remain pinned. Inactive NPC simulation remains frozen and offscreen updates throttled. Existing player/cosmetic caches remain unchanged.

[Actual3urban roundtrips](urban-stress-qa.json):Juni walks the unchanged1336px modern↔station corridor6times using original controls (8016px total),with real culling/entry/exit and observed visitors npc-modern-daon, npc-modern-haru, npc-modern-geonu, npc-modern-seorin. Sampled maximum active=3,loaded=4;pending samples=0. A test-only persisted visit epoch150s old initializes the calendar;real time runs thereafter,no actor/player position,route,collision,speed or animation-clock override. Pending2 remains a code/unit limit,not a claim that the sampled run reached2.

Each768×1456RGBA atlas is4,472,832bytes (4.266MiB). Four source surfaces are17.06MiB;two pending decoded images can add8.53MiB. These are source-surface estimates,NOT a total memory ceiling:HTMLImage,Canvas,WebGL copies,world/player/cosmetics and driver allocations are additional. Heap samples in the trace are JS heap only.

Actual180RAF callbacks on shared headless Chromium:median 16.70ms,p95 16.80ms,max 16.80ms. This is desktop callback cadence under concurrent QA,not certified device presentation FPS. Two actual SwiftShader WebGL native readbacks are0mismatch;software upload/readback is not hardware-GPU performance evidence. The5texture clip inspector is an isolated comparison utility,not the production4texture pool.

Physical Android Chrome,iPhone Safari,thermal/battery/low-memory behavior and hardware WebGL are NOT TESTED. Retain existing physical-device handoff/checklist and export the recorded device/browser/OS/viewport/FPS/memory/issues/video references;do not auto-fill PASS from desktop emulation.
