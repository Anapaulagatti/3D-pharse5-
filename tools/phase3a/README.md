# Phase3A native NPC tooling

Approved Phase2C source is immutable. These tools write only Phase3A-specific art,bindings,evidence and review artifacts. No paid image or AI API was used.

Dependencies for offline authoring/QA: Python3,Pillow12.3.0,NumPy2.3.5,SciPy1.17.0. Runtime remains existing Phaser4.2.1/TypeScript/Vite; no new game engine or runtime package. Browser evidence uses installed systemChromium and Playwright. Recording uses `PLAYWRIGHT_BROWSERS_PATH=/tmp/phase2b-playwright` with `ffmpeg-1013/ffmpeg-linux`→`/usr/bin/ffmpeg`.

`art.py` is the own-native authoring recipe. It reads approved Juni motion LANDMARK JSON only; no playable face,costume or atlas pixels enter the NPC authoring process. First generated Seoyeon/Minseo/Harin/Eunji; expanded only after actual pilot. `bind.py pilot|full` writes separate NPC bindings from frozen canonical masks/metadata and verified local offsets. Importing it is read-only; regeneration must be deliberate. Four pilot atlases remain exact at the pilot checkpoint.

`source_qa.py` validates all14/1456cells/448walkframes,8distinct images per direction and independently extracts raster outsole stance for positive/negative profile travel (≤1px quantization). `navigation_qa.py` checks whole native29×9contact at every route pixel and keeps critical doors,stairs,bridges,docks and plots clear. `protected.py` freezes6382acceptedfiles and strips exactly6marked additive hooks to reproduce the approved scene byte for byte.

`full_capture.mjs` records actual original-control approaches,ambient directional walking,occupational activity,greeting,dialogue and return. An optional list of NPC IDs recaptures only affected residents while preserving the valid independent evidence. `readbacks.py` independently compares native PNG bodies with actual atlas cells. Redundant full backing PNGs remain in `/tmp/phase3a-full-native`; all84native body crops and14representative full scenes are delivered. `pilot_motion.mjs` similarly records the four-context gate; temporary journals are ignored.

`cross_zone_plan.py` reads original masks and the exact union of existing walking contact offsets. Clearance-weighted offline QA paths and verified axis shortcuts are not a new runtime collision model. `walk.mjs` drives only original keys and,when needed,the original analog joystick for precise alignment; it never changes coordinates,speed,physics,clock or sprites. The continuous actual cross-zone proof uses northern Jeju bridgeA. No broader route certification is implied.

`stability.mjs` records12real zone exit/entry cycles and60actual dialogues,reload and state/resource checks. `extra_evidence.mjs` captures mobile layouts,actual softwareWebGL and a real visited landmark before NPC dialogue/reload. `performance_probe.mjs` observes desktop cadence/heap and verifies ScenicTour preserves exact player position. Physical devices/hardware remain NOT TESTED.

`media.py` creates compression-only1280×900 review MP4s,without source-sheet substitution or retiming. PNG is pixel authority. `gallery.py`,documentation and package tools assemble review evidence only. The game uses no review placement markers. Stop for human Phase3A acceptance;Phase3B remains locked.

Portable delivery: `node tools/phase3a/build_review.mjs`, `python3 tools/phase3a/package.py`; extract and run `python3 start_review.py`. `package_npcs.mjs`, `package_characters.mjs` and `device_smoke.mjs` test localhost4378 from the independent extracted artifact, including14real NPC approaches,all12original curated looks,save/reset/reload,touch movement and evidence-gated device report export. Large full traversal/stability videos remain online; all14NPC clips and compact native evidence are bundled.
