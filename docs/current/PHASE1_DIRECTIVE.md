# CODEX MASTER PROMPT — KOREAN ARENA PIXEL TOWN
## PHASE 1: WORLD FREEZE, SAFE REPOSITORY CLEANUP & MULTI-CHARACTER FOUNDATION

**Repository:** `Anapaulagatti/3D-pharse5-`

**Starting branch:** `art-gate/gate3-full-world`

**Proposed development branch:** `feature/phase1-character-foundation`

**Engine:** Existing Phaser 4 + TypeScript + Vite architecture.

**Current product:** Korean Arena Pixel Town — 2D Korean-themed educational social RPG.

---

# 0. NEW HUMAN DEVELOPMENT DIRECTIVE

The map production phase is now considered artistically accepted as the baseline for gameplay development.

We are moving from world-art production into character systems, NPC systems and gameplay development.

This directive supersedes all previous instructions requiring Codex to stop exclusively for Gate 3 map-art review.

However, it does NOT authorize destructive map modification, a public release or changes to the separate Korean Arena learning application.

## PRIMARY OBJECTIVE

Deliver a clean, maintainable, recoverable Korean Arena game project with:

1. An immutable approved world baseline.
2. A safely cleaned and organized active repository.
3. The existing approved Juni character preserved.
4. A scalable multi-character architecture.
5. Four fully playable, visually distinct characters in total, including Juni.
6. An actual character selection interface.
7. Persistent local character selection.
8. Verified desktop and mobile landscape gameplay.
9. A clear architecture for future NPCs, quests, education, economy and rewarded advertising.

**Do not implement the full gameplay loop in Phase 1.**

Phase 1 establishes the reliable production foundation.

---

# 1. LOCK THE APPROVED WORLD

## 1.1 Identify the real current world

Before any edits, inspect:

- Git HEAD and working-tree status.
- `AGENTS.md`.
- `STUDIO_TASKS.md` and `STUDIO_PROGRESS.md`, if present.
- Latest Gate 3 Palace Cleanup checkpoint.
- Approved Hanbit Station checkpoint.
- Approved Jeju bridge checkpoint.
- Western hanok and courtyard corrections.
- Northwestern farm.
- Current playable world entrypoint.
- Phaser scene registration.
- Asset loading and rendering pipeline.

Be careful: historical V10, graybox and old review code may still coexist with the actual latest playable game.

**Do not accidentally select an old V10 graybox as the canonical production world.**

Verify which assets and scene registrations are actually used by the latest complete approved game.

Resolve duplicate or obsolete active-world entrypoints only after proving which one is canonical.

## 1.2 Create a permanent baseline

Create a recoverable checkpoint and branch from the verified complete world state.

Suggested reference:

`checkpoint/world-art-approved-phase1-20261026`

If that reference already exists, do not overwrite it. Choose a non-conflicting name.

Record the exact SHA and protected asset hashes.

## 1.3 Protected map content

Freeze:

- Historical North and palace compound.
- Western hanok and completed garden.
- Modern South and commercial buildings.
- Newly approved Hanbit Station.
- Namsan.
- Amusement park.
- Coastal areas.
- Both Jeju bridge crossings.
- Jeju island.
- Northwestern farm.
- Existing roads and environmental assets.
- World coordinates and approved collisions.
- Cinematic Scenic Tour and camera functionality.

No map regeneration, artistic polishing or relocation is authorized.

Minor map changes may be proposed later but must not occur in Phase 1.

## 1.4 Juni preservation

Preserve the approved Juni source atlas, native proportions, character identity, animation frames and movement behavior.

Juni must remain an available default playable character.

Do not replace Juni with the older procedural `hero` actor merely because the older actor has convenient sprite-generation utilities.

---

# 2. SAFE REPOSITORY CLEANUP

The repository contains extensive historical experiments, review artifacts, outdated instructions, temporary outputs and superseded world implementations.

These are distracting future development prompts.

We need a clean active project without losing important history.

## 2.1 Mandatory dry-run inventory

Before deleting anything, produce:

`docs/current/CLEANUP_MANIFEST.md`

Classify files into:

**A — PROTECTED**

Approved production art, source atlases, canonical world files, scripts, current tests, required tools, licenses, checkpoints and dependency files.

**B — SAFE TO CLEAN**

Verified disposable build outputs, generated temporary caches, stale unreferenced QA scratch files and exact duplicates with proven redundant ownership.

**C — HISTORICAL / RECOVERABLE**

Superseded art, old V6–V10 prototypes, obsolete review outputs and previous development experiments.

**D — UNCERTAIN**

Anything whose references or ownership cannot be proven.

## 2.2 Cleanup rules

For category B:

Remove safe disposable content from the active workspace.

For category C:

First verify historical recovery through existing Git history, tags or an archival reference.

Remove obsolete files from the active working tree only where no current build, test, documentation or gameplay dependency requires them.

For category D:

Do not delete. Record for future review.

Never remove a file simply because its name contains `old`, `legacy`, `backup`, `review` or `test`.

## 2.3 Explicit protections

Never destructively delete:

- Juni source and runtime assets.
- Approved new Hanbit artwork.
- Approved Jeju bridge artwork.
- Original map source files required for rebuilding.
- Character animation tools.
- Sprite Forge tools/skills or their dependencies.
- Current Phaser runtime dependencies.
- Existing valid tests.
- Required historical checkpoints.
- Project configuration and licenses.

No Git history rewrite, force push or broad deletion of source directories.

## 2.4 Consolidate active instructions

The existing `AGENTS.md` contains numerous historical Gate 3 instructions, some of which no longer describe the active development stage.

Create one clear current authority document:

`docs/current/PROJECT_STATE.md`

It must state:

- Map development is frozen for Phase 1.
- Approved map and station are canonical.
- Juni is protected.
- Current development priority is player character selection.
- Future phases are NPCs, quests, learning and economy.
- No changes to the separate learning website.
- No main merge or public deployment.

Keep `AGENTS.md` concise and point it to the current authority.

Preserve historical engineering decisions in recoverable documentation.

Avoid conflicting STOP directives from superseded Gate 3 review cycles.

---

# 3. DESIGN THE MULTI-CHARACTER SYSTEM

Currently the project has a Juni animation pipeline and an older actor pipeline that includes historical NPC-style actors.

Do not assume those pipelines already form a complete selectable-player system.

Build one scalable player-character architecture.

## 3.1 Character Registry

Every playable character must have a structured definition including:

- Stable character ID.
- Korean and Vietnamese display names.
- Short profile description.
- Character preview art reference.
- Sprite atlas reference.
- Animation definition.
- Native sprite dimensions.
- Foot/contact anchor.
- Collision configuration.
- Movement animation mapping.
- Idle animation mapping.
- Running animation mapping.
- Emote definitions.
- Cosmetic metadata.
- Availability/unlock metadata for future use.

Use strongly typed TypeScript interfaces and runtime validation where appropriate.

## 3.2 Player Character Manager

Create one central manager responsible for:

- Loading player character definitions.
- Loading/selecting character assets.
- Creating the active player sprite.
- Managing correct animation playback.
- Switching the selected character.
- Keeping correct world position.
- Preserving player progress independently of avatar identity.
- Handling scene transitions.
- Maintaining consistent camera and collision behavior.

Do not duplicate movement and collision logic separately for each character.

All playable characters must use the same core controller.

## 3.3 Character identity versus account progress

Character choice is cosmetic and identity-based, not an educational progression reset.

Design the data model so that:

`PlayerAccount → PlayerProgress → SelectedCharacterID`

Character identity must not determine:

- Lessons completed.
- Player level.
- Experience.
- Currency.
- Inventory.
- Quest completion.
- Korean learning progress.

Actual account and learning progress synchronization will be implemented in later phases.

For now, implement only the appropriate local character-selection state.

Do not invent an authenticated server account.

---

# 4. CREATE THE FIRST PLAYABLE CHARACTER ROSTER

## Phase 1 target: Four fully playable characters

Create:

### Character 01 — Juni

The already approved original protagonist.

Preserve the exact approved artwork and animations.

Default selection for existing players.

### Character 02 — Haneul (하늘)

A cheerful modern Korean adventurer.

Design direction:

- Distinct hairstyle and silhouette.
- Blue-toned casual outfit.
- Comfortable modern shoes.
- Energetic character personality.
- Clean, expressive chibi pixel art.

### Character 03 — Bomi (보미)

A character inspired by elegant Korean traditional fashion mixed with a contemporary aesthetic.

Design direction:

- Distinctive hair arrangement.
- Tasteful hanbok-inspired jacket.
- Warm red/coral and cream palette.
- Friendly, expressive visual identity.
- Modern playable-character practicality.

### Character 04 — Minjun (민준)

A curious Korean student/explorer.

Design direction:

- Visibly different hair and face silhouette.
- Casual green/cream outfit.
- Small personal accessory where appropriate.
- Calm, curious personality.
- Readable animation at gameplay scale.

These are initial creative art specifications, not instructions to copy existing copyrighted characters.

## 4.1 Artistic quality standard

All newly created player characters must match Juni and the approved Gate 1 environment in apparent scale, detail density, lighting, outline treatment and overall pixel-art craftsmanship.

Do not deliver:

- Static portrait cutouts pretending to be playable sprites.
- Characters with only color-swapped clothing.
- Three copies of Juni with different hair colors.
- Low-resolution procedural placeholder humans.
- Stretched sprites.
- Blurry AI upscales.
- Animation made by sliding a static image.
- Visually identical body silhouettes for every character.

New characters must have individually authored visual identities.

## 4.2 Animation requirements

Each character must support:

- Four-direction idle.
- Four-direction walk.
- Four-direction run.
- Start and stop motion where supported.
- Proper directional turns.
- Wave emote.
- Celebrate emote.

Use actual multi-frame animation for walk and run.

Aim for eight genuinely distinct walk frames and eight run frames per direction where the existing animation architecture supports them.

Preserve the approved visual scale and feet/ground registration.

Animation atlas dimensions may be character-specific internally, but all characters must have consistent visible gameplay proportions and correct world-space contact.

Do not resample artwork at fractional scales.

If the project cannot produce new characters at the required quality with available tools, deliver the completed technical foundation and identify the unfinished character art honestly. Do not present placeholders as approved final characters.

## 4.3 Animation quality

Validate:

- No missing frames.
- No clipped hair or clothing.
- No frame-to-frame character jumping.
- Consistent grounded foot placement.
- Correct movement facing.
- Natural idle behavior.
- No excessive limb deformation.
- No inverted or mismatched body parts.
- No sprite floating above the road.

Each character must remain visually distinct when seen next to Juni.

---

# 5. CHARACTER SELECTION INTERFACE

Implement a new character selection experience.

## Initial launch

New local players should see a character selection screen before entering the world.

Existing players who already have saved preferences may load directly with their selected character.

Default safely to Juni if no valid saved selection exists.

## Selection interface

Provide:

- Character gallery.
- Character name in Korean and Vietnamese.
- Large animated preview.
- Walk/idle preview.
- Short character description.
- Clearly visible selected state.
- Confirmation action: "Bắt đầu hành trình".
- Return to selection from game settings.

The player must be able to explore characters and select a preferred appearance.

## Interface style

Use a polished Korean Arena visual identity.

The interface should complement the existing high-quality world rather than look like a generic administration panel.

Desktop: comfortable gallery/card layout.

Mobile landscape: touch-friendly, responsive controls, no clipped character previews or horizontal overflow.

## Switching characters

When choosing a different character:

- Preserve current progress.
- Preserve relevant player location.
- Stop existing animation and release old runtime sprite references safely.
- Load the new sprite and animation definition.
- Reuse the same movement logic.
- Preserve scene/camera functionality.
- Prevent switching during unsafe scene transitions.
- Avoid creating duplicate player bodies or collision objects.

Do not reset the map or teleport players unnecessarily.

---

# 6. SAVE AND RESTORE CHARACTER SELECTION

Implement local persistence using a versioned schema.

Example:

`korean-arena-player-preferences-v1`

Store only necessary information such as:

- Selected character ID.
- Preferences schema version.
- Optional local cosmetic configuration.

Do not store personal account secrets.

Handle:

- Missing saved preferences.
- Corrupt data.
- Unknown character IDs.
- Browser storage unavailable.
- Future character additions.
- Browser refresh.
- Scene reload.

Character selection must never corrupt or reset existing Korean-learning or world progress.

Prepare a clean storage abstraction so a future authenticated backend can replace local persistence.

---

# 7. PREPARE FUTURE GAMEPLAY ARCHITECTURE

Do not build NPC missions, shops, economies or advertisements yet.

However, establish lightweight extensibility contracts for later phases.

## Future subsystems

Create a brief technical design specifying how the following will connect:

- NPC Registry.
- Dialogue Engine.
- Quest State Machine.
- Inventory.
- Currency Wallet.
- Farming Plots.
- Crafting and Gathering.
- Shops.
- Korean Question Provider.
- Lesson Progress Provider.
- Reward Eligibility.
- Optional Rewarded Advertisement.
- Account Progress Persistence.

Do not instantiate fake production services or create decorative non-working gameplay controls.

## Educational architecture requirement

Later, quest completion will follow this state sequence:

`ACTIVE → OBJECTIVE_DONE → QUIZ_PENDING → QUIZ_PASSED → REWARD_GRANTED`

Incorrect Korean answers must keep the mission pending and return a different appropriate question at the same learning level.

The future question provider must prioritize verified learning progress from the main Korean learning website, when an authorized integration is available.

If the user has no progress, the beginner curriculum should be used.

For Phase 1, document these as future contracts only.

Do not implement quiz reward logic yet.

## Rewarded ads architecture

Prepare a short design note stating:

- Advertisements must be optional.
- Base rewards must not require advertising.
- A validated ad may provide an additional reward up to the designed 2× total.
- Rewards must not be granted merely because the client claims a video was watched.
- Ad availability, cancellation or failure must not block normal quest completion.

No ad SDK integration in Phase 1.

---

# 8. PHASER IMPLEMENTATION RULES

Use the existing technology stack.

Respect actual installed Phaser APIs and project versions.

Avoid unnecessary dependency upgrades.

Preserve:

- Desktop WASD and arrow controls.
- Running controls.
- Existing interaction key.
- Mobile landscape joystick.
- Mobile interaction buttons.
- Smooth camera movement.
- Scenic Tour.
- Existing working scene transitions.
- Native pixel rendering.
- Approved collision geometry.

Ensure the selected playable character replaces only the active player representation, not unrelated NPC or scenery assets.

Existing historical actor artwork, such as Sejong and other educational figures, should remain reserved for appropriate future NPC use unless explicitly redesigned and approved as player characters.

Do not interfere with the map's existing coordinate system.

---

# 9. TESTS AND QUALITY ASSURANCE

Run the existing checks where available:

- `npm run typecheck`
- `npm run assets:check`
- `npm run lint`
- `npm test`
- `npm run test:e2e`
- `npm run build`

Extend the test suite to cover:

### World preservation

- Existing world geometry is unchanged.
- Approved art source hashes remain stable.
- Collision data remains unchanged.
- No unrelated native world pixels change.
- Existing Juni movement still works.

### Character registry

- IDs are unique.
- Asset definitions exist.
- Required animations resolve.
- Missing atlas data is handled.
- Unknown character IDs safely fall back to Juni.

### Selection

- First launch opens selection.
- Selected character appears in the world.
- Saved selection restores after reload.
- Switching characters preserves player state.
- No duplicate sprites or physics bodies.
- Character options remain responsive on mobile landscape.

### Movement

Test each of the four characters:

- Walking in four directions.
- Running in four directions.
- Idle and directional turning.
- Emotes.
- Movement around buildings.
- Scene transitions.
- Road/bridge collision behavior.
- Return from settings/selection screen.

### Visual testing

Generate actual native Phaser screenshots for every playable character.

Include at least one comparison showing all four characters beside an approved environment element for scale.

Test Canvas and WebGL rendering where feasible.

Hardware Android Chrome and iPhone Safari must remain NOT TESTED unless actual physical-device testing was performed.

A green automated test does not constitute artistic approval.

---

# 10. MANDATORY DELIVERABLES

Deliver the following:

## A. Production baseline

- Approved world checkpoint reference.
- Protected world manifest.
- Protected Juni manifest.
- Verified active production entrypoint.

## B. Repository cleanup

- Cleanup inventory.
- Files actually removed.
- Files preserved.
- Historical recovery references.
- Updated concise `AGENTS.md`.
- Centralized `PROJECT_STATE.md`.

## C. Character system

- Character Registry.
- Player Character Manager.
- Four selectable character definitions.
- Complete available character atlases.
- Animation configuration.
- Character selection UI.
- Persistent selection.

## D. Art review

- Character roster overview.
- Native 1:1 previews.
- Side-by-side visual scale comparison with Juni.
- Four-direction walk/run demonstrations.
- In-world gameplay screenshots.
- Before/after world-preservation evidence.

## E. QA

- TypeScript/build/test report.
- Movement and selection tests.
- Protected source hash audit.
- Out-of-scope pixel-difference check.
- Known limitations and unresolved issues.

## F. Playable delivery

- Updated playable review ZIP.
- Character selection available in the actual game.
- All completed characters controllable through the original input system.
- Short gameplay video demonstrating character selection and switching.

Do not provide only mockups or a static art gallery.

---

# 11. PHASE 1 STOP CONDITIONS

Phase 1 is complete only when:

1. The approved world baseline is protected and recoverable.
2. Safe cleanup has been performed with a clear audit.
3. Superseded instructions no longer control current development.
4. Juni remains visually and technically unchanged.
5. Four genuinely distinct playable characters are available, or any unfinished character is explicitly marked incomplete.
6. Character selection works in the real Phaser game.
7. Changing characters does not reset player progress or damage world functionality.
8. Native visuals and animation evidence are available.
9. No unrelated map change has occurred.
10. The review ZIP and QA report are delivered.

A partial character-art result must not be described as complete Phase 1 acceptance.

## OUT OF SCOPE

Do NOT:

- Build the full NPC population.
- Implement farming timers or harvest loops.
- Create shops or inventory economy.
- Implement Korean question completion logic.
- Connect to the learning website.
- Implement rewarded advertising.
- Introduce multiplayer.
- Regenerate the map.
- Modify the separate Korean Arena app.
- Deploy publicly.
- Merge into main without human authorization.

---

# FINAL INSTRUCTION

Korean Arena has finished its intensive world-art phase.

The next challenge is converting that approved world into a living educational RPG.

**Phase 1 must protect the world, remove obsolete development clutter safely and establish a premium-quality multi-character system.**

Prioritize art quality, clean architecture, recoverability and actual playable behavior over producing large quantities of low-quality content.

Complete the authorized Phase 1 work on a separate development branch.

Produce the review package and stop for human approval.

**DO NOT START PHASE 2 AUTOMATICALLY.**