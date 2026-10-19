# V6 actual map reconstruction

Authority: ../current/V6_MAP_RESTRUCTURE.md, read completely. User rejects V4's coordinate-preserving decoration-only approach. Explicitly authorizes moving buildings, rail, colliders, doors, routes, ferries and camera bounds to reconstruct the supplied reference. Branch rebuild/pixel-social-rpg-v3; before-edit recovery/before-v6-map-restructure-20261019→2b5244db06d4cabbaa47196d0f2c78f55d6107ca was pushed and independently remote-peeled. Keep old V4 and all sources/review entries intact. No main merge, public deployment, paid APIs, new characters, unrelated gameplay, cleanup, delegation, force/reset/worktrees.

Original Drive PNG received after planning:1161×1355 (the inline image was the southern crop). Preserve the exact original PNG/hash and compare the COMPLETE world at the same aspect using letterboxing, with an additional matching southern detail. Northern history remains preserved. Use world4352×5312 to retain native landmark/Juni scale, give the station/park/shore enough real space and keep the island distinct. Pixel size remains1world unit; top-down/light3/4, native96×112Juni canvas/80pxbody,8×4feet; no avatar/art resizing. Ground source is existing image-generated material RGB; new geometry masks, editable tilemaps and positioned sprites reconstruct layout, not a flattened reference painting.

| Existing landmark | V4 anchor | Planned V6 anchor | Spatial purpose |
| --- | --- | --- | --- |
| Bookshop |1760,2280|1688,2552|Independent upper civic frontage west of formal avenue|
| Namsan tower |832,2912|704,3008|Western enclosed hillside park, winding approaches|
| Lookout terrace |1120,3104|1120,3376|Separate southeast hill overlook and arrival|
| Nature pavilion |352,3360|1104,2784|Upper hill trail discovery|
| Transit station |1792,2752|2240,2912|Central station, broad forecourt above tracks|
| Rail/platform |2320,2920/3008|2240,3152/3240|One organized horizontal infrastructure band|
| Train |2640,2912|2624,3144|Aligned with relocated rail|
| Public rail crossing/stairs |2048,2920/3032|2240,3152/3264|Realigned physical crossing and platform stair|
| Modern hub |2560,2688|1776,3456|Independent southwest shop frontage below rail|
| Cafe |1568,3168|2656,3456|Independent southeast retail frontage below rail|
| Ferry terminal |2848,3088|2240,3632|Central coastal civic frontage, pier branch visible|
| Ferris wheel |3392,2744|3328,3040|Northwest entertainment court|
| Carousel |4000,2784|3968,3008|Northeast entertainment court|
| Entertainment gate |3712,3200|3552,3504|Single main southern entry sequence|
| Discovery hall |4144,3056|4016,3504|Southeast entertainment court|
| Refreshment kiosk |3712,2400|3728,2576|Upper garden amenity|
| Jeju cultural ensemble |existing native positions|+320pxY|Keep identity and proportions beyond expanded waterfront|

Layout bands: north0–2239retained; civic transition2240–2640; Namsan x128–1408/y2448–3648; transit x1568–2912/y2592–3744; entertainment x3136–4288/y2448–3648; clear boulevard strips x1472and3024; waterfront promenade y3744; ferry pier x2496; distinct enlarged natural Jeju envelope beyond y4000. A strong north→civic route branches visibly to hill/transit/park/ferry. Routes avoid actual building masses; rear of station is not a fake entrance. Update original interaction/label/anchor/portal coordinates with each moved landmark.

Rebuild southern physical footprints from unchanged approved native building templates, real doors/stairs/rail gaps, low campus edges and new shoreline walkmask. Do not keep old327sea/forest blockers at obsolete coordinates. Preserve old northern colliders and actual room/lesson logic. Preserve every approved art file and144Juni frames. New source layout/relocation manifest/Tiled and actual native before/after must prove repositioning. Reuse real Forge palette/hash/validate/nav/Tiled/compose/HTTP checks. No new image/provider route needed when original art suffices. Verify all five destinations in actual input-driven Phaser, mobile joystick/portrait/reduced motion/Canvas-WebGL and uncaptured performance; normal-entry full-world walkthrough, exact ZIPHTTP and production/tests/Git checkpoint before STOP for final user art review.


Implementation refinement: original Drive reference is1161×1355/full world; preserve exact original and use complete-world comparison (southern inline crop was incomplete). New source selection:497objects/122relocated/101curated edge-and-buffer placements; optional native coastal deck uses its actual stair and separate open return, not a through promenade obstruction. Mainland pier2496,3912; island trigger2496,4208; island spawn2496,4280 stays outside portal shape. Original collision geometry retained per moved building; new conservative32px shore bodies derive from every outside-water pixel, never loosened old physics. Initial physical/nav diagnostics retained under quality/diagnostics; final validation still in progress.
