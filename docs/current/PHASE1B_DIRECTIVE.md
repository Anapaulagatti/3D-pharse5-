# CODEX — PHASE 1B: COMPLETE THE PLAYABLE CHARACTER ROSTER

**Repository:** `Anapaulagatti/3D-pharse5-`

**Branch:** `feature/phase1-character-foundation`

**Existing review:** `docs/phase1/README.md`

**Character QA:** `docs/phase1/character-art-status.json`

**Protected baseline:** `checkpoint/world-art-approved-phase1-20261026`

## HUMAN REVIEW DECISION

The Phase 1 technical foundation is ACCEPTED.

The world freeze, repository cleanup, Character Registry, Player Character Manager, selection interface and persistence system must be preserved.

However, Phase 1 itself is NOT COMPLETE because only Juni is genuinely playable.

Your new task is to finish the missing character-art and animation work for:

1. Haneul — 하늘
2. Bomi — 보미
3. Minjun — 민준

Do not restart Phase 1.

Do not repeat completed cleanup.

Do not rebuild the world.

Do not create a new character engine.

Extend the existing accepted architecture.

---

# TASK 1 — ANALYZE AND CORRECT THE FAILED ANIMATION WORKFLOW

Review the previous Haneul animation attempts, including:

`docs/phase1/character-art-status.json`

`docs/phase1/SOURCE_PROVENANCE.md`

Study the existing native Juni animation and runtime registration.

The earlier Haneul attempts failed because:

- All eight walk-front poses retained the same leading-leg hierarchy.
- The gait did not alternate naturally.
- Generated body proportions did not match the requested native registration.
- The extracted result could not be safely accepted as a playable atlas.
- Source sheet generation did not respect the expected body/ground alignment.

Do NOT repeat the same failed approach without changing the production method.

## Required production strategy

Use a controlled, frame-by-frame or accurately layered animation workflow.

First establish:

1. Character identity sheet.
2. Full-body front pose.
3. Full-body rear pose.
4. Left profile.
5. Right profile.
6. Consistent native ground anchor.
7. Approved proportions relative to Juni.
8. Actual walk-cycle key poses.
9. Intermediate motion frames.
10. Final atlas and Phaser registration.

Generate and validate a representative eight-frame front walk cycle for Haneul before producing every other animation.

Do not process dozens of additional frames if the underlying gait is still anatomically incorrect.

Use real authored limb motion.

A valid walk cycle must include alternating legs, believable weight transfer and consistent foot contact.

Do not fake movement by translating a static portrait.

Do not use a single static image with cosmetic bobbing as a replacement for actual animation.

---

# TASK 2 — ESTABLISH EXACT NATIVE CHARACTER SCALE

Juni remains the visual and technical benchmark.

Preserve Juni's original:

- 96 × 112 native atlas cells.
- Foot anchor (48,100).
- Approved visible body proportions.
- Native rendering scale.
- Original animation files.
- Original movement behavior.

The new characters must be composed and registered for compatible gameplay proportions.

They may have different hairstyles, clothing volumes and silhouettes, but must not look dramatically larger or smaller than Juni without an explicit artistic reason.

Avoid taking a large generated illustration and blindly shrinking it to fit 96 × 112.

Instead author native-ready character art with planned proportions and integer pixel placement.

When resizing source elements is unavoidable, use an explicit quality-controlled sprite-redraw process.

Reject:

- Blurred edges.
- Broken anatomy.
- Missing facial details.
- Uneven outlines.
- Distorted body proportions.
- Incorrect feet.
- Excessively small faces.
- Collapsed clothing details.

Do not weaken existing quality validators to obtain a PASS.

---

# TASK 3 — FINALIZE THREE DISTINCT CHARACTER IDENTITIES

## HANEUL — 하늘

A cheerful contemporary adventurer.

Appearance:

- Blue-based casual outfit.
- Distinctive hairstyle.
- Energetic silhouette.
- Comfortable footwear.
- Bright, expressive personality.

Keep the existing approved design direction where visually suitable.

Replace the rejected animation pilot with a properly authored native motion set.

## BOMI — 보미

A warm, elegant character inspired by Korean traditional fashion.

Appearance:

- Coral and cream palette.
- Hanbok-inspired contemporary jacket.
- Distinctive hair arrangement.
- Soft but recognizable facial expression.
- Graceful idle and walking personality.

Do not design Bomi as Juni with recolored clothing.

Her face, hair, outfit structure and silhouette must create a distinct identity.

## MINJUN — 민준

A curious, friendly student and explorer.

Appearance:

- Sage green and cream outfit.
- Distinctive short or medium hairstyle.
- Recognizable face.
- Subtle student/explorer accessory.
- Curious and relaxed personality.

Any accessory must remain correctly attached throughout the animation.

No floating notebook, detached bag strap or flickering clothing details.

---

# TASK 4 — AUTHOR COMPLETE NATIVE ANIMATION PACKS

Each new character requires:

## Four-direction movement

- Idle front.
- Idle back.
- Idle left.
- Idle right.
- Walk front.
- Walk back.
- Walk left.
- Walk right.
- Run front.
- Run back.
- Run left.
- Run right.

## Additional actions

- Wave.
- Celebrate.
- Directional turn/start/stop transitions required by the existing character controller.

Use at least eight distinct authored frames for each walk and run direction, consistent with the existing registry validation.

That means a minimum of 64 actual walk/run frames per character, plus the required idle and action frames.

### Animation quality requirements

- Real alternating-leg walk cycle.
- Readable arm swing.
- Consistent body proportions.
- Correct facing direction.
- No identical repeated frames masquerading as animation.
- No visual teleporting between frames.
- No accidental hair/body deformation.
- No sliding across the ground.
- Correct foot-contact alignment.
- Natural animation loop closure.
- No clipping inside atlas cells.

Use independently authored directional details when asymmetrical clothing, hairstyle or accessories make mirroring visually incorrect.

The animation must look good at actual gameplay speed, not merely when individual frames are viewed separately.

---

# TASK 5 — BUILD PRODUCTION ASSETS

For each completed character, provide:

- Native transparent sprite atlas.
- Valid Phaser atlas JSON.
- Native animation frame sources.
- Animation clip definitions.
- Character preview artwork.
- Source/provenance manifest.
- Registered origin and foot-contact metadata.
- Character-specific animation QA.

Use the current character architecture.

Update existing Character Registry entries rather than creating another parallel registry.

Do not duplicate the player movement engine.

Characters must use the same world-coordinate and collision model.

All completed assets must resolve correctly in the production build.

---

# TASK 6 — ACTIVATE THE FOUR-CHARACTER SELECTION SYSTEM

After each character passes validation:

Change its availability from `incomplete` to `playable`.

Do not unlock it before the real asset pack is ready.

The final character selection screen must contain four usable characters:

- Juni.
- Haneul.
- Bomi.
- Minjun.

Each must have:

- Animated preview.
- Vietnamese/Korean name.
- Character description.
- Working selection.
- Persistent saved choice.
- Actual playable character in the world.

## Switching behavior

Switching must preserve:

- Current world position where safe.
- Camera.
- Player progression state.
- Existing preferences.
- Map state.
- Scene-transition integrity.

Destroy or release old sprite runtime ownership safely without creating duplicate player bodies.

Do not rewrite the movement controller to accommodate one character.

Fix character art and registration to work with the accepted architecture.

---

# TASK 7 — REAL GAMEPLAY TESTING

Test all four characters in the actual Phaser world.

Mandatory tests:

1. Select a character.
2. Enter the map.
3. Walk in four directions.
4. Run in four directions.
5. Stop and turn.
6. Wave.
7. Celebrate.
8. Walk around Hanbit Station.
9. Enter and leave an existing supported interior.
10. Cross the Jeju bridge routes.
11. Switch to another character.
12. Refresh the browser.
13. Restore the saved character.
14. Verify no loss of progress or position.
15. Verify mobile landscape input and UI through supported browser testing.

Do not alter the map or collision geometry to conceal an avatar registration problem.

If a character fails a previously valid walking route because its sprite envelope is incorrect, correct the character.

Do not shrink Juni or change the approved world.

Actual physical mobile testing must be marked NOT TESTED unless performed on physical devices.

---

# TASK 8 — IMMUTABLE WORLD AND JUNI PROTECTION

The following are strictly protected:

- Complete world artwork.
- Main palace and historical north.
- Modern south.
- Hanbit Station.
- Both Jeju crossings.
- Namsan.
- Amusement park.
- Northwestern farm.
- Existing world collision.
- Juni original animation.
- Approved camera and scenic tour.
- Existing technical foundation.

Use:

`docs/phase1/protected-world.json`

`docs/phase1/protected-juni.json`

Run hash and visual regression checks.

All source assets outside the authorized character feature scope must remain unchanged.

Do not reopen old Gate 3 art tasks.

---

# TASK 9 — DELIVERY AND QUALITY GATE

Deliver:

1. Four-character playable review ZIP.
2. Native full-character lineup.
3. Native 1:1 comparison beside Juni.
4. Four-direction walking animation demonstration.
5. Four-direction running animation demonstration.
6. Wave and celebration demonstrations.
7. Actual character selection gameplay video.
8. Gameplay showing switching between all four characters.
9. Desktop and mobile-landscape selection screenshots.
10. Character atlas and source manifests.
11. Updated art-provenance report.
12. Full unit/E2E/build reports.
13. Protected world/Juni hash audit.
14. Final PASS/FAIL/NOT TESTED table.

## PASS REQUIREMENTS

Phase 1B only passes if:

- Four characters are genuinely selectable.
- Three newly authored native animation packs are complete.
- Each character has a distinct visual identity.
- All required directional animations exist and play.
- Walk/run motion is anatomically coherent.
- All characters work with the shared controller.
- Selection is persistent.
- No map or Juni source regression occurs.
- The playable ZIP actually contains the four working characters.

Do not claim that four characters are playable when only selection cards exist.

Do not mark failed animation tests as PASS.

## ARTISTIC REVIEW

Technical validation does not automatically approve visual quality.

Produce clear native comparison material and stop for human artistic review.

If a newly generated character fails the art benchmark, keep that character unavailable and report the exact reason.

Do not hide unfinished work.

---

# FINAL HUMAN DIRECTIVE

The Phase 1 technical foundation is already accepted.

**DO NOT REBUILD IT.**

Your assignment is to complete the remaining three characters and demonstrate a fully functioning four-character roster.

Prioritize consistent beautiful pixel art, believable movement and native gameplay integration.

Do not start NPC development, shops, quests, farming systems, Korean quizzes or advertisements.

Do not merge main or deploy publicly.

Finish Phase 1B, deliver actual playable evidence and STOP.

**PHASE 2 REMAINS LOCKED UNTIL THE FOUR-CHARACTER ROSTER IS VISUALLY AND TECHNICALLY APPROVED.**