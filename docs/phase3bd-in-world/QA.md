# QA · Fresh2026-11-04 recovery verification

| Check | Result |
|---|---|
|typecheck|PASS|
|lint|PASS|
|format|PASS|
|unit|PASS 203/203|
|e2e|{'startTime': '2026-11-04T01:20:28.802Z', 'duration': 721871.5009999999, 'expected': 69, 'skipped': 0, 'unexpected': 2, 'flaky': 0}|
|e2eRepeatedFollowup|{'startTime': '2026-11-04T01:35:07.787Z', 'duration': 37767.407, 'expected': 8, 'skipped': 0, 'unexpected': 0, 'flaky': 0}|
|currentE2ECoverage|PASS all71current cases across runs:69full-suite passes+2corrected snapshot-observation cases repeated4times each(8/8). Initial full69/71 and first follow-up4/8 remain disclosed, NOT one clean71-test run.|
|actualWorldGameplay|PASS ACTUAL PHASER THREE PHYSICAL QUESTS + SHOP|
|mobileLandscape|PASS MOBILE LANDSCAPE TOUCH|
|protectedAssets|PASS|
|physicalAndroid|NOT TESTED|
|physicaliPhone|NOT TESTED|
|hardwareGPU|NOT TESTED|
|humanKoreanReview|PENDING_HUMAN_REVIEW|
|humanGameplayArt|PENDING|
|publicExposure|PENDING_EXACT_NEW_MANIFEST_APPROVAL|

Actual flow: GAMEPLAY_QA.json/MOBILE_QA.json and videos/native PNGs. Desktop full loop uses identity selection only, no seeded items/coins/quests/time and no coordinate setter. Mobile isolated1seed/QA-entry fixture disclosed; actual joystick/tap interaction.

203unit cases include physical tutorial,range/ground checks,retry and one-time rewards,additive old-save migration,quota rollback and unordered distinct orchard objects. Existing tests retained; obsolete global-panel assertions changed to verify its removal. Four independent cold-start fixtures are separate cases with identical assertions/timeouts, not a raised aggregate timeout.

Source/test game served from a frozen copied build; no concurrent rebuild of the served tree. Previous lost local results do not count. Technical PASS does not grant owner artistic/educational/exposure approval.

One128x20RGBA tool atlas adds10240decoded bytes. Native tool scale1,NN; existing world/player/NPC pools unchanged. No new full-scene texture or world cache; hardware/GPU/memory soak not certified.

Exact ZIP:3570manifest files (3571ZIP entries including manifest), CRC/SHA256/extraction PASS. Actual extracted Phaser native960x640/catalog26/gallery12/oneJuni/zoom1/NN, real starter-seed/plant/water/elapsed-growth/harvest, bothvideo playback PASS. All3570asset URLs/hash checks pass; zero normal console/resource errors and zero external-origin network requests. Local blob textures are classified by parsed origin; initial observer false positive retained. Portal320/390/667/960fits without horizontal overflow. These final sidecars do not mutate frozen payload/manifest.
