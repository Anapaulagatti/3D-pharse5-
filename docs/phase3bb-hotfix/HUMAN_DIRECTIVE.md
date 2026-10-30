PHASE 3B-B — HOTFIX MOVEMENT / HAIR ACCESSORIES / COMPLETE REMAINING 6 NPC

Context:
We already have a working playable GitHub Pages preview with 20 NPC.
The owner has manually tested the live build and found 3 concrete issues that must be fixed before continuing:

1) Hair accessories / hair-related cosmetics are visually wrong and ugly.
2) Movement has a visible frame/camera jerk:
   - when starting movement,
   - when combining movement keys,
   - sometimes the frame snaps or shifts briefly before stabilizing.
3) The remaining 6 NPC must now be completed and included so the review build contains the full 26 NPC.

IMPORTANT:
- Do NOT restart the project.
- Do NOT rebuild the world from scratch.
- Do NOT change the approved map art unless a tiny local adjustment is absolutely required for the bug fix.
- Do NOT regress the currently approved station, bridges, palace, hanok, world art, playable roster, cosmetics system, or review portal.
- Preserve existing save data compatibility if possible.
- Keep the current GitHub Pages review workflow.
- Maintain the same visual quality standard as the approved player characters and the better NPC batch.
- If any remaining 6 NPC still have unresolved likeness/commercial-risk concerns, convert them into clearly fictionalized public-safe variants:
  - new fictional public names,
  - small silhouette / hairstyle / facial-detail / clothing-detail changes,
  - no direct one-to-one likeness dependence,
  - still stylistically consistent with the rest of the game.

==================================================
TASK A — FIX HAIR ACCESSORIES / HAIR COSMETICS
==================================================

Problem:
The hair accessories currently look bad / visually broken.

Investigate and fix all hair-related accessory issues, including but not limited to:
- bad anchor position,
- bad offset on head,
- wrong layer ordering,
- clipping into hair or face,
- floating accessory placement,
- mismatch between front / back / left / right directions,
- mismatch between idle / walk / run / interaction states,
- ugly deformation or inconsistent pixel alignment,
- palette mismatch,
- accessories not matching the Juni-quality art standard.

Requirements:
- Accessories must look intentional, clean, and attractive.
- Pixel placement must stay stable across directions and motion.
- Each accessory must visually attach to the head correctly in:
  - idle,
  - walk,
  - run,
  - greet / interact,
  - any other supported review action.
- Keep the pixel-art fidelity consistent with the existing roster.
- Reuse the best approved character standards as the quality baseline.

Deliverables for Task A:
- corrected accessory rendering / atlas / offsets / layering,
- before/after gallery for at least the affected hair accessory cases,
- one compact review page or section showing:
  - front/back/left/right,
  - idle and moving states,
  - at least a few representative characters.

==================================================
TASK B — FIX MOVEMENT JERK / FRAME SNAP / COMBINED-INPUT GLITCH
==================================================

Problem:
Movement currently has a visible jerk:
- when movement begins,
- when multiple direction keys are pressed together,
- sometimes the camera/frame shifts for one moment,
- motion can feel like it snaps out of alignment.

Investigate the true root cause.
Potential areas to inspect include, but are not limited to:
- animation state transition timing,
- first-frame state selection,
- input buffering,
- diagonal movement resolution,
- body/cosmetic sync,
- camera follow smoothing,
- sprite origin / pivot mismatch,
- collider / physics body update timing,
- subpixel rounding,
- world-to-camera alignment,
- layer snapping,
- frame change on start-move,
- mismatched source atlas dimensions between states.

Required outcome:
- Starting movement must feel stable and clean.
- Combining keys (up/down/left/right combinations) must not cause a one-frame snap or camera pop.
- Character, cosmetics, and camera must stay visually locked together.
- No temporary offset jump.
- No “giật 1 phát” on move start.
- No visible frame misalignment when changing direction quickly.
- Preserve responsive controls.

Validation scenarios:
Test at minimum:
- start/stop movement in all 4 directions,
- diagonal or rapid direction-combo input,
- changing direction while running,
- changing direction near collision boundaries,
- switching between walk and run,
- interacting immediately after moving,
- testing with several different playable characters and several NPCs,
- testing with hair accessories enabled.

Deliverables for Task B:
- short technical root-cause summary,
- proof that the jerk is fixed,
- gameplay clips or native capture,
- QA notes listing tested movement scenarios,
- confirm whether the issue was animation-side, camera-side, collider-side, cosmetic-side, or a combination.

==================================================
TASK C — COMPLETE THE LAST 6 NPC AND INCLUDE THEM IN BUILD
==================================================

Goal:
Upgrade the review build from 20 NPC to the full 26 NPC.

Requirements:
- Finish the remaining 6 NPC to the same quality level as the approved NPC batch.
- Maintain consistency with the Jeju / Korean pixel world style.
- NPC quality must match the standard of the improved batch, not the rejected ugly early batch.
- Each NPC must have:
  - finalized sprite / visual identity,
  - correct in-world placement,
  - interaction support,
  - daily-life schedule integration if relevant to the current system,
  - correct collision / navigation behavior,
  - proper naming,
  - correct inclusion in review portal / gallery / manifest.
- If likeness rights remain uncertain, convert those NPC into fictionalized public-safe variants before inclusion:
  - use fictional names,
  - adjust appearance enough to avoid direct dependence,
  - keep them stylistically natural in the same world.

Do NOT leave the 6 NPC as half-finished placeholders.
Do NOT mark the phase complete if they are missing from the actual playable review build.

Deliverables for Task C:
- all 26 NPC present in the playable build,
- updated review gallery for 26 NPC,
- updated manifest / list / portal references,
- clear list naming all 26 NPC included,
- note which of the final 6 are original / fictionalized if applicable.

==================================================
TECHNICAL + REVIEW CONSTRAINTS
==================================================

Preserve:
- approved world/map art,
- approved player characters,
- current cosmetics system structure unless a small hotfix is needed,
- GitHub Pages review portal,
- save/load behavior whenever possible,
- prior approved checkpoints.

Do NOT:
- rework unrelated systems,
- rebuild the entire roster,
- reopen already-approved map fixes,
- introduce a new art style,
- silently drop NPCs,
- claim success without updating the playable review build.

==================================================
RELEASE / REVIEW OUTPUT
==================================================

Produce a single review package for this phase that includes:

1) Updated playable GitHub Pages review build.
2) Hair accessory before/after review section.
3) Movement hotfix QA evidence.
4) Full 26-NPC gallery / review sheet.
5) QA summary.
6) Checkpoint / commit reference.
7) Explicit note of anything still NOT TESTED.

Final status should clearly say one of:
- PASS — ready for owner review
or
- BLOCKED — with exact blocker

Do not say PASS if:
- hair accessories are still ugly/broken,
- movement still jerks,
- the remaining 6 NPC are not actually present in the playable build.

Stop after delivering the review build and evidence, so the owner can manually test the live playable version.