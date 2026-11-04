# CODEX MASTER PROMPT — PHASE 3B-D GAMEPLAY REDESIGN

## OBJECTIVE: REPLACE MENU-DRIVEN GAMEPLAY WITH REAL IN-WORLD INTERACTIONS

The owner has reviewed the deployed Phase 3B-D gameplay.

**ARTISTIC WORLD: ACCEPTED.**

**CORE GAMEPLAY EXPERIENCE: NOT ACCEPTED.**

The current implementation resembles an HTML administration panel layered over a Phaser map. Farming, quest progression and other actions are primarily performed through buttons inside a large overlay.

This is not the intended experience.

The target is an immersive pixel-art life-simulation RPG combining the interactive farming feel of Hay Day and the in-world character interaction of Pixels, while maintaining an original Korean-language-learning game.

This task is a focused gameplay redesign of the existing Phase 3B-D candidate, NOT a restart and NOT Phase 3B-E.

---

## TASK 1 — REPLACE FULL-SCREEN GAMEPLAY MENU

Remove the current oversized "Chuyện nhỏ trong thị trấn" gameplay panel from the normal gameplay flow.

Replace it with:

- Small quest tracker on screen.
- Compact inventory shortcut.
- Town Coins display.
- Contextual interaction indicator.
- NPC dialogue UI that appears only during conversations.
- Shop UI that opens only when interacting with a shopkeeper.
- Korean question UI that appears only at the appropriate quest-completion stage.

Preserve underlying quest, economy and farming business logic wherever correct.

Do not replace the existing panel with multiple floating HTML buttons that perform the same remote actions.

**Important:** Gameplay must happen primarily inside the Phaser world.

HTML overlays are acceptable for dialogue, inventory, accessibility and learning questions, but cannot substitute for the actual game activity.

---

## TASK 2 — REAL FARMING SYSTEM

Use the existing approved farm located in the northwest section of the map.

Do not relocate or regenerate the farm artwork.

### 2.1 — Physical farming plots

Identify the actual farming plot coordinates in the world.

Represent each plot with its own persistent state:

EMPTY → PLANTED → GROWING → READY → HARVESTED → EMPTY.

Additional watering requirements may be represented independently without breaking the state machine.

### 2.2 — Real planting interactions

The player must physically reach or select an accessible farming plot.

Desktop:

- Walk using WASD.
- Approach a plot and press E or click it.
- Choose a seed from the quick inventory.
- Optionally drag an appropriate seed onto a nearby plot.

Mobile:

- Move using touch controls.
- Tap or long-press a nearby plot.
- Choose a seed and confirm planting with a touch-friendly action.

When planting:

1. Validate that the player is within interaction range.
2. Check seed quantity.
3. Play an actual planting animation or action feedback in Phaser.
4. Consume one seed.
5. Display the planted crop on that plot.
6. Save the plot's persistent state.

Do not allow planting from a remote menu.

### 2.3 — Watering

Allow the player to equip or use a watering can.

When watering a planted plot:

- Play character/tool animation.
- Show water droplets or another suitable effect.
- Update the actual plot state.
- Provide readable feedback.

Do not regenerate previously approved character sprites merely to fake tool animations.

Create compatible action overlays or dedicated non-destructive animations where needed.

### 2.4 — Crop growth

Crops must visibly progress through growth stages on the map.

Implement actual configurable growth time, persisted using trusted time data appropriate to the current local demo architecture.

The crop must continue growing after the player walks away.

Reloading should restore its correct stage.

No paid acceleration is required.

### 2.5 — Harvesting

When the crop reaches READY:

- Display a recognizable mature-crop sprite.
- Allow physical interaction with that plot.
- Play a harvesting action.
- Add the harvested product to inventory.
- Clear or reset the plot appropriately.
- Update relevant quest progress.

Prevent harvesting the same crop twice.

**Acceptance test:** The owner can physically approach a plot, plant, water, leave, return, harvest and receive an item without opening a large global gameplay panel.

---

## TASK 3 — ACTUAL NPC INTERACTION

The existing 26 NPCs are approved.

Do not rebuild their artwork or animation atlases.

Implement contextual NPC interaction:

- Walk within range.
- Press E or tap the NPC.
- NPC faces the player where supported.
- Show short dialogue.
- Offer an appropriate action such as Talk, Quest, Shop or Deliver.
- Close dialogue and resume normal NPC behavior.

Do not allow a quest to be completed from the global quest tracker.

The player's position, quest requirements and NPC interaction must be validated.

Quest indicators may appear above relevant NPCs when appropriate.

Use a small, visually cohesive pixel-game dialogue panel instead of the existing document-like interface.

---

## TASK 4 — MAKE THE THREE CORE QUESTS PHYSICAL

Convert the previously implemented three quest flows into actual gameplay interactions.

### Quest A — Jeju Orchard

The player:

1. Talks to Harin.
2. Accepts a harvesting task.
3. Travels to the Jeju orchard.
4. Interacts with actual harvestable objects or trees.
5. Collects the required items.
6. Returns to the assigned NPC.
7. Answers a Korean question.
8. Receives the quest reward.

### Quest B — Delivery

The player:

1. Talks to Minseo.
2. Accepts a parcel.
3. Receives an actual parcel inventory item.
4. Travels to the designated recipient.
5. Interacts with that NPC to hand over the parcel.
6. Completes the Korean question.
7. Receives the reward.

### Quest C — Farm Tutorial

The player:

1. Talks to Cheolsu.
2. Receives seeds.
3. Walks to a real plot.
4. Plants seeds.
5. Waters the plot.
6. Harvests after the appropriate growth stage.
7. Returns to Cheolsu.
8. Answers the Korean question.
9. Receives a reward.

The gameplay must be triggered by in-world events rather than selecting "Complete" or "Harvest" from a remote quest panel.

---

## TASK 5 — IMMERSIVE SHOP

Keep the existing shop economy and inventory data layer.

Replace remote shop actions with shopkeeper interaction.

The player must approach the relevant shop/NPC and open the shop interface.

The shop should feature:

- Item sprites.
- Seed names and prices.
- Buy/sell tabs.
- Item quantity.
- Available Town Coins.
- Stock and inventory feedback.
- Clear error messages when funds or stock are insufficient.

Buying seeds adds items to inventory.

Selling crops removes the sold quantity and grants the correct Town Coins.

All transactions must be atomic/idempotent where applicable.

Avoid new financial integrations, cryptocurrency, NFTs or real-money purchasing.

---

## TASK 6 — IMMERSIVE UI AND FEEDBACK

The world must remain clearly visible during ordinary gameplay.

Use a compact HUD rather than a full-screen administration panel.

Requirements:

- Native-resolution pixel-art presentation.
- Smooth camera following.
- No movement-frame snapping.
- No collision regression.
- Short contextual hints.
- Relevant sound effects only if appropriate original/licensed assets already exist.
- Clear planting, watering, harvesting and reward feedback.
- Inventory and quest tracker are optional views, not the primary way to complete actions.
- No excessive modal interruption.
- Mobile controls remain usable.
- Support keyboard and touch input.

Preserve the approved map, NPC visuals, character roster and the cleanup of rejected map assets.

---

## TASK 7 — KOREAN QUESTION INTEGRATION

The Korean question remains a mandatory educational step to complete a quest.

But it must appear at the correct moment:

The player finishes physical objectives → reports back to NPC → NPC initiates learning challenge → player answers → reward becomes claimable.

Wrong answer:

- Provide meaningful feedback.
- Present another question of equivalent difficulty.
- Do not complete the quest.

Correct answer:

- Complete the quest.
- Grant base rewards exactly once.
- Trigger appropriate celebration/reward feedback.

Keep website synchronization disabled unless an authorized and verified integration already exists.

Preserve the demo disclaimer and educational content review status.

---

## TASK 8 — IN-GAME QA, NOT JUST UNIT TESTS

Existing unit tests are insufficient to establish gameplay quality.

Automate real player interaction scenarios through the actual Phaser world.

Required E2E flows:

1. Move from starting area to farm.
2. Select an accessible farming plot.
3. Plant a seed using in-world interaction.
4. Water the planted crop.
5. Observe growth stages.
6. Harvest and verify inventory.
7. Enter a shop and buy a seed.
8. Sell a crop and verify Town Coins.
9. Approach and talk to Harin.
10. Complete the orchard quest.
11. Complete a delivery interaction.
12. Answer one Korean question incorrectly and retry.
13. Complete a quest with a correct answer.
14. Reload and verify saved progress.
15. Verify rewards cannot be duplicated.
16. Verify camera, movement, NPC interaction and collision remain stable.

Run desktop and mobile emulation checks.

Actual Android/iPhone hardware testing remains NOT TESTED unless independently performed.

Capture real gameplay footage demonstrating the complete loop.

Screenshots of menus alone are not acceptable proof.

---

## TASK 9 — DELIVERABLES AND RELEASE CONTROL

Work on an isolated branch based on the verified Phase 3B-D candidate.

Do not restart earlier phases.

Do not regenerate approved world/character assets.

Do not restore rejected maps.

Keep the existing public GitHub Pages build available as a rollback.

Create one updated playable review candidate containing:

- Real in-world farming.
- Real crop growth and harvesting.
- Physical NPC quest interaction.
- Contextual shops.
- Compact HUD.
- Korean-learning verification.
- Persistent rewards and inventory.
- Responsive desktop/mobile experience.

Provide:

1. Working branch and exact commit SHA.
2. Changed-file summary.
3. Unit/E2E results.
4. Gameplay video.
5. Artifact and SHA256 manifest.
6. Rollback reference.
7. Known limitations.
8. Exact GitHub Pages review deployment instructions.

Do not silently publish a changed artifact. Prepare the required approval receipt and request approval for the exact new candidate before replacing the public Pages version.

Do not claim success if the physical gameplay remains menu-driven.

Do not start Phase 3B-E.

## FINAL ACCEPTANCE STANDARD

The owner must be able to play the game without using the old full-screen action menu.

The core loop is:

**WALK → INTERACT → PERFORM ACTION → OBSERVE WORLD CHANGE → COMPLETE OBJECTIVE → ANSWER KOREAN QUESTION → CLAIM REWARD → CONTINUE PLAYING.**

The result should feel like a real playable pixel-art farming/life-simulation RPG, not an HTML task dashboard with a game background.