# CODEX MASTER PROMPT — PHASE 3B-C
## Hair Accessory Removal + World Collision Audit + First NPC Quest Gameplay Loop

### PROJECT CONTEXT

Project: Korean Pixel Town / Tiếng Hàn So Easy

Current playable review:

https://anapaulagatti.github.io/3D-pharse5-review/play/

The 26-NPC preview is now playable and has been manually reviewed by the project owner.

Approved live baseline manifest:

`db9d4bb68f31c819d79ec95efaad1befce257086e64c41a5c93c2ba6fe7deb2f`

The owner considers the current build acceptable for continuing development, but has identified two remaining defects:

1. Hair accessories are still visually unacceptable, even after previous repair attempts.
2. Some world passages are inaccessible or have excessively narrow collision clearance despite appearing walkable.

The owner authorizes these cleanup tasks together with implementation of **Phase 3B-C: NPC Quest & First Gameplay Loop**.

Do not restart the project or perform another full artistic reconstruction.

---

# TASK A — COMPLETELY REMOVE BROKEN HAIR ACCESSORIES

Previous hotfix attempts did not meet the owner's visual expectations.

**Decision: Remove the problematic hair accessory feature instead of repairing it again.**

Requirements:

- Remove hair accessory equipment and overlays from gameplay.
- Remove affected items from Character Studio, customization menus, equipment selectors and item previews.
- Remove obsolete accessory attachment logic, offsets and z-index rules where no longer required.
- Keep all approved character hairstyles, original hair sprites, facial features and outfits.
- Preserve unaffected cosmetics, including clothing and other correctly rendered accessories.
- Maintain compatibility with existing saved character presets. Unsupported hair accessory selections should be safely ignored or migrated.
- Do not leave floating decorations, missing-texture placeholders, invisible clickable items or console errors.
- If deprecated assets are still required by historical checkpoints, archive or exclude them from the active build rather than destructively removing recovery sources.

No new hair accessories are needed in this phase.

Acceptance criteria:

- All 12 player characters render without broken hair accessories.
- Idle, walking, running and interaction animations remain visually stable.
- Character Studio no longer offers unavailable hair accessories.
- No regression in the approved hairstyles or other cosmetics.

---

# TASK B — WORLD COLLISION & ACCESSIBILITY AUDIT

## Problem

The live game contains areas that visually appear accessible but cannot be entered, or have collision corridors so narrow that movement feels obstructed.

This is a gameplay navigation problem and must be addressed systematically.

## Required investigation

Audit actual player collision and reachable walkable space throughout the approved world.

Priority locations:

1. Palace entrances, side buildings and courtyard pathways.
2. Modern commercial streets, shop entrances and rear passages.
3. Hanbit Station entrance, platforms and adjacent walkways.
4. Jeju bridges and both mainland-to-island connection points.
5. Jeju house, volcano, orchard and connecting paths.
6. Farm entrance and walkable areas between farming plots.
7. Waterfront, ferry terminal and harbor promenades.
8. Parks, leisure attractions, decorative walls, flower beds and narrow passages.

Do not assume that passing scripted route tests means all real-world passages are accessible.

## Collision correction rules

- Separate visual asset bounds from collision geometry.
- Remove unnecessary collision from transparent image padding and non-solid decorative details.
- Inspect sprites with oversized invisible hitboxes.
- Distinguish solid obstacles from walkable ground and decorative overlays.
- Ensure passable corridors have enough clearance for the actual player physics body, with a practical safety margin.
- Align door trigger volumes with visible entrances.
- Preserve real obstacles such as walls, water, cliffs, buildings and fences.
- Do not solve pathfinding by making the entire map non-collidable.
- Fix unreachable passages locally, prioritizing collision geometry over artwork modifications.
- Preserve existing world coordinates, checkpoint positions and the approved map composition.

If a passage truly requires artwork changes, make a minimal proposed change within the affected area and document it. Do not redesign that district.

## Automated navigation QA

Build or extend a collision-debug system that displays:

- Player hitbox
- Solid collision shapes
- Walkable regions
- Entry and exit points
- Unreachable areas
- Narrow passages and collision bottlenecks

Run actual Phaser player-body traversal tests between meaningful accessible locations.

Include stationary starts, walking, running, diagonal movement, turns, wall sliding and movement through entrances.

A visual screenshot alone is not proof that the route is passable.

Also preserve the previously corrected movement behavior:

- No one-frame camera snapping.
- No sprite origin/pivot jumping.
- No unexpected animation reset when combining direction inputs.
- No camera jitter at entrance boundaries.

## Acceptance criteria

Every location intended to be accessible in this phase must have a reachable route from its intended entry point.

Produce one concise collision review with a list of repaired regions and any intentionally blocked locations.

---

# TASK C — PHASE 3B-C: FIRST FUNCTIONAL NPC QUEST LOOP

We now move beyond passive NPC schedules into actual interactive gameplay.

The game should take inspiration from the satisfying gameplay loops of farming, life-simulation and quest-based games, while maintaining its original Korean-learning identity.

Do not copy another game's code, assets or proprietary content.

## C1 — NPC interactions

Connect the existing NPC Daily Life system to a reusable Quest Manager.

NPCs should be able to:

- Offer contextual quests.
- Display dialogue and quest objectives.
- React to player progress.
- Accept completed objectives.
- Provide gameplay rewards.
- Resume their daily-life routines after an interaction.

Use the 26 approved fictional NPC identities and their existing environment placements.

Prioritize a small but genuinely functional vertical slice rather than generating a large number of superficial quests.

## C2 — First gameplay activities

Implement at least three complete, distinct quest examples using existing world locations.

Suggested examples:

**Quest 1 — Jeju Orchard**

A local NPC asks the player to harvest or collect tangerines.

Player flow:

Talk to NPC → accept quest → reach orchard → perform collection interaction → return to NPC → complete Korean learning challenge → claim reward.

**Quest 2 — Modern District Delivery**

A shopkeeper requests delivery of a parcel to another character.

Player flow:

Receive package → navigate to correct location → interact with recipient → complete Korean challenge → receive reward.

**Quest 3 — Farm Preparation**

An NPC introduces the existing farming area.

Player flow:

Receive seeds → prepare an available plot → plant a crop → perform an appropriate progression step → complete Korean challenge → earn initial farming rewards.

Do not require the player to wait unnecessarily during the tutorial.

Implement these activities with real in-world triggers and interaction logic, not fake buttons that immediately complete tasks.

## C3 — Korean learning verification

The core requirement is that completing a game objective alone does not fully finish the quest.

The player must also successfully answer a Korean learning question.

Question selection rules:

1. If the website's real learning-progress data is available through an authorized integration, select questions from material the player has already studied.
2. If the player has no learning history, use the beginner curriculum.
3. If the website integration is not ready, implement a clean LearningProgressAdapter with a clearly labeled local demo mode and original beginner question data.
4. Never invent user learning history or claim that demo progress is synchronized with the website.

Question behavior:

- Correct answer: quest is completed and the base reward is granted.
- Incorrect answer: give helpful feedback and generate a different question at the same difficulty.
- Prevent immediate repetition of the same question where a suitable alternative exists.
- The player must answer correctly to finish the quest.
- Provide readable Korean text, Vietnamese explanations and accessible input controls.
- Avoid unfairly penalizing mistakes or requiring paid services.

Question content should be original or properly licensed.

Add a human-review status for Korean content before treating it as educationally validated.

## C4 — First rewards and inventory

Implement a minimal functional reward system:

- Town Coins
- Experience points
- Basic quest items
- Seeds or harvested crops where relevant
- Inventory updates
- Quest progress persistence

Use configurable reward values rather than inventing an irreversible economy.

Ensure rewards cannot be claimed repeatedly through page refreshes, quest re-entry or duplicate interaction events.

Use stable quest IDs and idempotent reward transactions.

Do not implement the full marketplace or economy balancing in this phase.

## C5 — Optional double-reward architecture

Prepare a RewardedAdAdapter interface for future integration.

Rules:

- Base quest rewards are granted without watching ads.
- A future optional rewarded ad may offer an additional reward after verified completion.
- Never require an ad to complete a mission.
- Never multiply Korean mastery, proficiency or assessment scores.
- Do not connect a real ad provider or claim that an ad was watched successfully without valid verification.
- Keep the ad integration DISABLED until its own approval and compliance review.
- If a test simulation is needed, label it clearly as developer/demo behavior and keep it separate from real rewards.

---

# TASK D — GAMEPLAY UX & MOBILE SUPPORT

Improve only the interfaces necessary to play the new quests.

Required:

- NPC dialogue panel
- Accept / decline quest
- Active quest tracker
- Objectives and progress indicator
- Korean question panel
- Reward confirmation
- Minimal inventory view
- Clear interaction feedback

Desktop:

- WASD / arrow movement
- E to interact
- Existing run controls
- Keyboard-accessible quest and answer selection

Mobile:

- Existing virtual joystick or movement buttons
- Easy-to-tap interaction controls
- Responsive quest dialogue
- Korean question UI that fits narrow screens
- No controls overlapping critical gameplay content

Test mobile emulation, and explicitly state that physical-device performance is NOT TESTED unless actual-device results exist.

---

# TASK E — CHECKPOINT, QA & GITHUB PAGES REVIEW

Preserve the currently deployed 26-NPC preview as a rollback checkpoint.

Do not silently overwrite the approved live artifact.

Implement Phase 3B-C on an isolated development branch.

Required testing:

1. All 26 NPCs remain present and functional.
2. Hair accessories are completely removed from the active game.
3. Original hairstyles and unaffected cosmetics remain unchanged.
4. Main walkable entrances and pathways pass collision tests.
5. Camera and movement remain smooth.
6. Three quests can be completed end-to-end.
7. Incorrect Korean answers trigger an alternative equivalent-difficulty question.
8. Correct answers unlock quest completion.
9. Rewards and inventory persist correctly.
10. Reloading does not duplicate quest rewards.
11. Desktop and mobile-emulation interactions work.
12. The approved map and character artwork are not unintentionally modified.

Generate one consolidated review page with:

- A playable Phase 3B-C candidate.
- A concise summary of eliminated hair accessories.
- Collision audit results and repaired routes.
- The three playable NPC quests.
- Korean question and reward demonstrations.
- PASS / FAIL / NOT TESTED results.
- New checkpoint, exact artifact manifest and rollback reference.

After passing technical QA, prepare the GitHub Pages review update.

The owner authorizes implementation of this phase, but any changed public artifact still requires exact-manifest approval before publishing.

Do not mark the public deployment complete until the new manifest is approved and the actual HTTPS build is verified.

No unrelated artwork reconstruction, no production-site changes and no Phase 3B-D implementation.

## FINAL OBJECTIVE

Deliver a cohesive playable Phase 3B-C candidate with:

- No broken hair accessories.
- Accessible, correctly aligned walkable passages.
- Smooth player movement.
- 26 functional NPCs.
- Three complete interactive quest loops.
- Korean-learning verification before quest completion.
- Basic persistent inventory and rewards.
- A single review destination rather than dozens of separate files.

Execute all achievable work in one controlled continuation. Stop only for a genuine external permission, essential owner approval or an unresolved technical blocker. Report incomplete work truthfully.