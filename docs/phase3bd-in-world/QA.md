# QA · Fresh2026-11-04 recovery verification

| Check | Result |
|---|---|
|typecheck|PASS|
|lint|PASS|
|format|PASS|
|unit|PASS 203/203|
|e2e|RUNNING|
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
