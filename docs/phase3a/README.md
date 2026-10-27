# Korean Arena · Phase3A Living NPC World

Review candidate:14 authored inhabitants in7home zones,within the approved canonical world. Human Phase3A artistic acceptance is PENDING. Phase3B remains LOCKED.

[Playable ZIP](PHASE3A_LIVING_NPC_WORLD_REVIEW.zip) · [visual gallery](REVIEW.html) · [14 actual native NPCs](fourteen-actual-native.png) · [2× nearest review](fourteen-actual-review-2x.png) · [QA](QA.md) · [device handoff](DEVICE_REVIEW.md).

## Authority and recoverability

Human approved Phase2C12characters/28cosmetics/46variants/12looks/Studio/world. Exact review32d7d4743dfe5bd6cb1bc3bfb7eb2525b268af2d; accepted source/receipt `9583d7fa8414c2f9c7e0ddd8bdb62780705685a8`. New immutable approval reference `checkpoint/phase2c-fashion-studio-approved-20261027`. Fresh baseline116unit/53E2E passed before implementation; all required command logs in baseline-logs/. Physical-device status and historical WARNs were not promoted to PASS.

Branch `feature/phase3a-living-npc-world`. Four-context pilot `checkpoint/phase3a-four-context-pilot-20261027` (a492d22): actual Seoyeon/Minseo/Harin/Eunji,20native captures,all4walking directions,interaction/return. Only then expanded. Fourteen-resident checkpoint `checkpoint/phase3a-fourteen-residents-20261027` (62644cd),followed by coordinated costume/placement/UX/QA polish. Final review reference `checkpoint/phase3a-living-npc-world-review-20261027`. No historical reference overwritten.

## What is implemented

-14 independent native actor identities;104cells each/1,456total. Four-direction idle and8distinct walk frames,greeting and occupation gestures. Approved Juni motion landmarks guide rhythm; no playable face,costume or atlas pixels were copied.
- Typed/runtime-validated NPC Registry,deterministic finite-state actors,verified local waypoints,canonical collision queries,occupancy/yielding,proximity selection and structured Korean/Vietnamese dialogue.
- Native96×112 registration,48,100foot anchor,integer sprite/camera phase and nearest rendering. Consistent depth and contact shadows. Existing player engine remains the only player engine.
- Zone activation/camera culling/lower offscreen tick rate,at most4active NPCs/4resident NPC textures/2loads. All14records remain available; deactivation freezes intended activity without teleporting.
- Separate NPC-only local state; existing v1/v2 character/appearance,world position,visited markers and progress survive. No new accounts or fabricated learning completion.

## Play locally

Extract ZIP,run `python3 start_review.py`,open `http://127.0.0.1:4378/REVIEW.html`. The actual compiled game runs locally/offline without Node or external APIs. Compact evidence is included; large full traversal/stability recordings and full PNGs may resolve online at the immutable review tag. `--lan` is explicit opt-in for testing on your own LAN,not public deployment.

Choose any of the original12players and original28cosmetics as before. Walk toward a resident; use E,the proximity button or Explore. Read Korean/Vietnamese,choose a topic,advance and close. Residents resume their activity. Normal gameplay has no NPC placement markers. Explicit `?qa&npcReview=npc-...` URLs only select separately documented mask-validated QA approach spawns; they do not alter approved map metadata or normal spawn.

[NPC roster](NPC_ROSTER.md) · [zones](NPC_ZONES.md) · [navigation](NAVIGATION.md) · [dialogue](DIALOGUE_SYSTEM.md) · [performance](PERFORMANCE.md) · [protected audit](PROTECTED_AUDIT.md).

No world regeneration,collision rewrite,map enlargement,approved character/cosmetic/Studio edit,shop/economy/inventory/farming/rewards/quizzes/account sync,paid AI/image API,main merge or public deployment. Stop for human Phase3A review.
