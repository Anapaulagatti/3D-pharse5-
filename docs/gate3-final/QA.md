# Surgical technical and visual QA

[Whole-native-world scope](out-of-scope-audit.json) · [Actual Phaser readback](native-render-qa.json) · [Controls](movement-report.json) · [Native body/contact](body-clearance.json) · [Runtime collision](collision-runtime.json) · [Protected hashes](protected-hashes.json).

| Check | PASS / FAIL / NOT TESTED | Limit |
|---|---|---|
| Exact authorized bounds | PASS |0 out-of-scope ground, foreground/static or field pixels at4352×4864; region max-area guards enforced |
| Actual native Phaser fidelity | PASS |36 native frames /22 matched pairs;43,822,938 eligible source-ground pixels,0 mismatches; same camera/pose; nearest/native integer placement |
| Historical source preservation | PASS |All2,870 baseline assets exact; plans, Juni, historical checkpoints/source art immutable |
| Canonical station frontage | PASS |Main and isolated new-station static composition at2274,2603,684,210 exactly matches baseline; planters/canopy/tree/shadows unchanged |
| Western house completion | PASS local observed repair / human review pending |Missing left roof/eave continued; source facade/door/stairs/native position retained, proper local foreground roof owner |
| Courtyard | PASS local observed enclosure / human review pending |Narrow western stone/fence return; original garden/pine/fixtures core preserved; new25×22 support foot and existing western path validated |
| Farm spatial readiness | PASS |6×180×128 plot reservations, native soil/crop/interaction/state metadata; all6 anchors walkable/all6 soil centers blocked in live Phaser; actual aisle loop PASS |
| Farming game system | NOT IMPLEMENTED, as instructed |No inventory/economy/timer/quest/crop-state implementation |
| Canonical station asphalt phase | PENDING protected material decision |Protected floor remains exact, including historical asphalt phase; prior bounded native-road candidate remains unadopted. New facade alone is not district seamlessness approval |
| New station architecture integration | PENDING / not adopted |Independent roof/upper/facade, architecture-free ground stage, native registration, unchanged collision; relative artistic superiority requires human comparison |
| Actual regional movement | PASS selected cases |7 real-input cases: farm, house, courtyard, new entrance, crosswalk, complete bridge outward/return. Declared scene starts; no in-movement teleport or speed/frame/collision override |
| Native Juni visibility | PASS source readback |23 recorded frames,0 unexplained changed Juni pixels. Expected roof/rail/garden foreground occlusion explicitly accounted for |
| Full native bridge contact | FAIL |Movement trace sampled failures {'complete-bridge-to-jeju': 13, 'complete-jeju-to-mainland': 0};5/12 genuinely captured stop/turn poses have unsupported contact. A zero sampled return count does NOT prove return-pose clearance |
| Structural bridge proposal | NOT ADOPTED |Prior bounded25px/4866px² visible support, same unchanged physical field; no invisible land, endpoint change or Juni shrink |
| Station platform transfer | FAIL |Actual held A stops at nativeX2958;8px strip unchanged; no90×36 connector |
| Full approved circulation | FAIL, inherited |7 planned centerlines retain EXACT same blocked counts as residual baseline. New farm/garden collision does not add failures to those approved routes |
| Coast/road contact materials | PASS bounded source handling / human review pending |Small mainland water/asphalt native masks; preserved curbs/shore/Jeju. Not a claim that every offshore boundary is artistically seamless |
| Palace/retail/island-landing minor inspection | UNCHANGED after inspection |No independent evidence requiring another modification; no unrelated repaint |
| Build/typecheck/assets/unit regression | PASS |30 tests/9 files; does not approve art |
| Physical Android Chrome / iPhone Safari | NOT TESTED |Emulated touch, software/browser WebGL and builds cannot certify real phones |
| Hardware WebGL performance | NOT TESTED |Browser update intervals are not certified hardware/presentation FPS |
| Final full-world artistic acceptance | PENDING HUMAN |Mandatory unplaced Bakery and P1 spatial/navigation/device issues remain |

Main scene changes410,161 static pixels (98.0624% native composition unchanged); isolated new-station candidate changes640,265 (96.9753% unchanged). These percentages are consequences of exact masks, not permission to edit an arbitrary percentage.

## Retained failed attempt / reproduction

[Initial movement harness report](movement-initial-native-ui-harness-failure.json) is retained. It used native PHOTO framing, where UI deliberately hides the joystick. The harness was corrected to use normal existing gameplay UI; original game controls/collision stayed unchanged. Final7-case report/video are a fresh completed recording. No failed game movement is silently counted as a successful run.

Source reproduction: full repository checkout; `python3 tools/g3ds_build.py`, `python3 tools/g3ds_audit.py`, local Vite build/server, capture/native audit, real-control recorder and movement audit. Browser recording requires Playwright FFmpeg; this workspace uses `/usr/bin/ffmpeg` symlinked at `/tmp/g3ds-browser-cache/ffmpeg-1013/ffmpeg-linux` and `PLAYWRIGHT_BROWSERS_PATH=/tmp/g3ds-browser-cache`. Runtime playback does not need these authoring tools. Raw WebM is locally preserved; MP4 is lossy movement evidence, untouched native PNGs prove pixel quality.

No screenshot request/dependency, main merge, public deployment, new paid external image API, separate-app changes or full-world regeneration.

Extracted playable ZIP regression: **PASS** thirteen main entries (ten existing regions plus farm/house/courtyard) and two isolated station stages. WASD, original mobile joystick isolation, normal/reduced-motion Tour Pause/Skip/collapse/Return and exported report JSON checked in Chromium emulation. See [package smoke](package-smoke.json); physical devices still NOT TESTED.
