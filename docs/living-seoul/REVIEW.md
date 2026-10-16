# Living Seoul — first connected playable expansion

The master plan and **first** playable slice are ready for visual review. This does not claim the entire planned neighborhood/four historical guests are complete.

- [Review board](living-seoul-review-board.png): actual Phaser overview/native/detail/room, not concept art.
- [Gameplay MP4](exploration-gameplay.mp4):34.88s,1440×1200,872encoded25fpsframes, real keyboard/buttons, normal time. Juni crosses the original bridge, walks the book alley, enters the Academy, matches three letter names, returns to courtyard. [Decoded video contact](gameplay-video-contact.png), [actual input timeline](recording.json).
- [Full native2048×768engine overview](district-overview-native.png), [Academy1×](academy-native.png), [evening](academy-evening.png), [room1×](reading-room-native.png), [mobile Canvas](mobile-canvas-native.png), [lesson](learning-activity.png).
- [Master diagram](master-district-plan.png), [plan](PLAN.md), [machine-readable footprints/entrances/NPC planning positions](district-plan.json). Muted/planned areas are not generated gameplay.
- [Toolchain and honest QA](TOOLCHAIN.md), [local verification](verification.json), [preservation proof](preservation.json), [package verification](package-verification.json), [limited software performance measurements](performance.json).

## Play the actual build

Download [playable-review.zip](playable-review.zip), extract **Korean-Arena-Living-Seoul-Review**, run `python3 start.py` (Windows:`py start.py`). Python3required, noNode to view. Open the printed HTTPURL ending **/3D-pharse5-/district-review.html**. Do not open index/HTML in a source viewer or file://. Stop server with Ctrl+C.

WASD/arrows walk, Shift or mobile Run accelerates. Cross the stone bridge, follow east book alley to the central Academy steps; press E or Explore to enter. Walk toward the room's writing desk and E for the letter activity. Wrong answers retry. Match ㄱ—giyeok, ㄴ—nieun, ㅁ—mieum. These are **letter names**, not universal pronunciation rules. Close message to resume. E near the south door returns outside. Completion saves locally when available; storage denial does not prevent play. Brand link opens preserved previous town. Older plaza-review.html and character-review.html still work.

The exact ZIP6,253,697bytes / SHA256`e8cd41b5f3f8f76118a960ab4882f997df27e02761e22b2f1744b11eb3ac34ea` was independently extracted and opened through its own launcher. Desktop and DPR2mobileCanvas rendered images match the fresh source pixels byte-for-byte; actual movement/interior/return and oldtown4guests verified. No public site/tunnel/loopback preview link created. Pages remains old public build.

## Scope and review

Outdoor2048×768is twice original map area. Original west32placements/terrain and all144Juni frames remain; new original Academy +readingkit, book alley, library kiosk/restgarden and one lazy-loaded768×576room. Both bundles have editable layer/prop/collision/Tiled data.438protected source/assets/lock files compared directly to baseline5b0eaba; original movement update/UI template unchanged. Local12unit/12browser/type/lint/format/build/source checks pass. Tests cover real traversal/collision/occlusion/OSreducedmotion/pause/mobiletouch/Canvas/activity/reload/private-storage; thresholds not relaxed.

Known limitations: hard32px garden/path boundaries and simple rill remain visible. Fine terrain transitions are not claimed seamless. Raw extraction warns18tiny unowned high-resolution source pixels; official Forge room marker keyboard displacement fails on downward portal-reset (routes5/5/assets/Ysort pass), while actual Phaser explicit E entry/exit passes. Pre-existing Juni right-idle/small-wave detector warnings remain. Mobile is emulated, physicalphoneFPS/WindowsGUI not certified. Short stationary softwareGPU/Canvas measurements are not a60FPS claim.

Historical Academy guest Sejong, Jang workshop/observatory, Saimdang artgarden, Yi museum/pavilion, residential/market/park areas and their remaining activities are **planned, not mass-produced**. Existing rejected historical sprites were not presented as redesigned guests. Master plan gives their future purpose, footprint, entrance and NPC positions.

Please review Academy architecture/scale against Juni, courtyard density/road layout, readable room/props, and exploration on your screen. **STOP here before remaining-area/NPC production.** No cleanup, separate learning-app changes, main promotion, paid provider or Pages deployment.

Recovery before work:`recovery/before-living-seoul-20261016`→5b0eaba. Plan checkpointd987a4a/sourceCI38830636718success. Actual final verified sourceSHA/CI/clean-checkout result is recorded in immutable annotated tag`checkpoint/living-seoul-first-slice-20261016` only after observed verification; inspect the real tag rather than inferring success from this prospective handoff.
