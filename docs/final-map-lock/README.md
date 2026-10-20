# Final locked V6 map — review package

[Full overview4352×5312](FINAL_LOCK_OVERVIEW.png) · [Browser overview2176×2656](FINAL_LOCK_OVERVIEW_WEB.png) · [Small overview](FINAL_LOCK_OVERVIEW_SMALL.png)

Actual1:1Phaser crops: [central connector](quality/after/civic-transition-native.png), [modern venues](quality/after/modern-forecourt-native.png), [park passage](quality/after/park-hall-passage-native.png), [harbor](quality/after/pier-approach-native.png), [Jeju garden](quality/after/island-garden-native.png), [Jeju scenic loop](quality/after/island-coast-loop-native.png), [mobile native](quality/after/mobile-native.png). Open at100% for native detail. Fitting a whole-world thumbnail necessarily loses detail.

Matched native before/after boards: [connector](CIVIC_TRANSITION_BEFORE_AFTER.png), [modern venues](MODERN_FORECOURT_BEFORE_AFTER.png), [park](PARK_HALL_PASSAGE_BEFORE_AFTER.png), [harbor](PIER_APPROACH_BEFORE_AFTER.png), [Jeju](ISLAND_GARDEN_BEFORE_AFTER.png), [scenic loop](ISLAND_COAST_LOOP_BEFORE_AFTER.png). BEFORE frames retained verbatim from approved2df01bf; AFTER frames newly rendered. Source/current rendering code untouched; unchanged heritage Canvas AND real nonblank WebGL frames match exactly.

## Play locally

Download [playable-review.zip](playable-review.zip). Extract the ENTIRE Korean-Arena-V6-Reconstructed-World-Review folder. Run `python3 start.py` (Windows:`py start.py`) from the directory containing start.py, then open its printed HTTP address ending `/3D-pharse5-/v6-world-review.html`. Python3required; noNode/account/API. Do not open file:// or the HTML source viewer. WASD/arrows move,Shift run,E Explore; mobile stick/Run/Explore/Talk/Emote,portrait pause and OS reduced-motion retained. Explore at the original public jetty and confirm travel to Jeju; island landing returns. Optional `--canvas` and explicit `--lan` for same-network phone, manual landscape,Ctrl+C stops.

This is a source review package, NOT a deployment. The cloud preview is internal; its localhost URL is not a user-accessible public link. Keep main and public website unchanged.

## Verification and preservation

497placements/108original prop images/552collision rectangles/144Juni frames,world/coast/forest/land-walk masks,all route centerlines,portals,entrances,gameplay/UI/source/lock/workflow remain exact. Ground-only material/inlay/corner finishing within the prior repair envelope. Northern0..2239ground and all pixels outside the exact new edit mask are protected. No tracing,generation,resizing or new physical obstacles.

Production/types/all asset guards,lint,format,12unit pass. Original6route/ferry/rail/mobile cases pass; final harbor-guide-only correction rechecked with2ferry/mobile cases. Actual Canvas/WebGL movement/screenshots,25native renders,10DPR/zoom/draw checks,full overview,source/ZIP native5district desktop/mobile equality,portrait/ferry/Academy/retained guests pass. Exact final GitHub CI/independent clean-clone results belong in the observed checkpoint/final-map-lock-verified-20261020 annotation after verification.

[Report](REPORT.md) · [Executed evidence](quality/verification.json) · [Pixel-locality/geometry guard](quality/preservation.json) · [Actual processing commands](../../assets-src/final-map-lock/forge-commands.json) · [Inherited warnings](quality/inherited-forge-warnings.json). Physical phones/Safari/hardware GPU unmeasured; no universal60FPS claim. STOP for user visual review.
