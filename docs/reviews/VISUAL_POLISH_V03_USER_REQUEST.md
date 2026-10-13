# KOREAN ARENA 3D STUDIO — VISUAL POLISH v0.3

## USER VISUAL REVIEW

I have reviewed the publicly deployed v0.2 showcase.

The current Hanok Rooftop Arena is aesthetically pleasant and has a coherent color palette, but it does not yet feel like a captivating, living game world.

My feedback:

1. The environment looks too static.
2. Character animation is not visually noticeable enough.
3. The scene lacks rich environmental details.
4. Night lighting is too dark and lacks focal contrast.
5. The environment appears too small within the available viewport.
6. The experience does not yet create enough curiosity or emotional engagement.
7. The visual presentation feels closer to a technical 3D demo than a polished indie game.

**Your next mission is to transform the existing v0.2 into a visually compelling v0.3.**

Do NOT begin Hangul Garden or other learning districts.

## 1. RESUME EXISTING WORK

Read:

- STUDIO_MASTER_PROMPT.md
- STUDIO_TASKS.md
- STUDIO_PROGRESS.md
- STUDIO_DECISIONS.md
- STUDIO_ASSETS.md
- ART_DIRECTION.md
- CAMERA_LANGUAGE.md
- COLOR_MATERIAL_SYSTEM.md
- PERFORMANCE_REPORT.md

Inspect the existing repository, Blender source files, GLB assets, animation clips, preview application, and Git history.

Treat this message as the user's visual review for `VISUAL-REVIEW-001`.

Create a new milestone named:

**VISUAL-POLISH-003 — Golden Vertical Slice v0.3**

Preserve the original artistic identity and approved source assets.

## 2. MAKE THE WORLD FEEL ALIVE

Improve environmental animation using restrained, high-quality motion.

Implement and visually verify:

- Subtle lantern swaying.
- Visible warm lantern flicker.
- Gentle moving foliage.
- Small drifting hanji-paper fragments.
- Carefully controlled floating particles.
- Subtle ambient environmental motion.
- Expressive mascot idle motion.
- Occasional natural mascot gestures.
- Beautiful but lightweight transitions.

Animations should be noticeable without becoming distracting.

The environment must feel alive even when the user is not interacting.

Avoid excessive particle spam, distracting loops, and visually chaotic motion.

## 3. FIX ANIMATION VISIBILITY

Inspect the existing React Three Fiber animation system.

Pay particular attention to:

- `settings.reducedMotion`
- `settings.paused`
- `useAnimations`
- animation mixer updates
- active action selection
- `frameloop`
- visibility handling

The application must respect the user's operating-system reduced-motion preference.

When reduced motion is enabled, provide a beautiful static or simplified presentation.

When reduced motion is disabled, animations must visibly play.

Do not silently override accessibility settings.

Verify all six existing mascot animations:

- Idle
- Happy
- Thinking
- Celebration
- Disappointed
- Greeting

Ensure that each animation is meaningfully different and recognizable to a human viewer.

A technically playing animation that is nearly imperceptible is not sufficient.

## 4. UPGRADE THE HANOK ENVIRONMENT

Preserve the existing hanok architecture and overall diorama composition.

Increase carefully art-directed details:

### Architecture

- Richer roof-edge ornamentation.
- More refined Korean wooden joinery.
- Subtle decorative beam patterns.
- More expressive entrance structures.
- Carefully designed windows and latticework.
- Small architectural storytelling details.

### Courtyard

- Handcrafted stepping stones.
- Small ceramic pots.
- Better ground material variation.
- More detailed garden borders.
- Miniature benches and props.
- Decorative paper elements.
- Natural asymmetry.

### Vegetation

- Improved plum blossom tree.
- More organic foliage arrangements.
- Subtle wind animation.
- Small clusters of flowers and plants.

### Atmosphere

- Layered miniature city silhouettes.
- Environmental depth.
- Subtle distance haze where feasible.
- Warm accent lighting.
- Carefully placed focal highlights.

Do not increase polygon count blindly.

Prioritize details that are noticeable from the actual camera distance.

## 5. TRANSFORM THE MASCOT INTO A REAL GAME CHARACTER

The Ceramic Seed Spirit should become the emotional centerpiece of the scene.

Improve:

- Facial expressiveness.
- Eye animation.
- Body squash and stretch where appropriate.
- Anticipation before movement.
- Follow-through after movement.
- Clear emotional poses.
- Character silhouette.
- Surface material quality.
- Small secondary movements.

Required interactions:

- The mascot notices the camera.
- The mascot greets the user.
- The mascot reacts when clicked.
- The mascot performs a playful celebration.
- The mascot returns naturally to idle.

Use tasteful, expressive animations rather than constant exaggerated motion.

Retain the character's original identity.

## 6. IMPROVE LIGHTING AND MATERIALS

### Daylight

Create soft, luminous, welcoming daylight.

Ensure:
- readable shadows;
- good object separation;
- balanced highlights;
- attractive ceramic materials;
- clearly visible architectural depth.

### Evening

Create a warm golden-hour atmosphere.

Use:
- warm directional light;
- soft shadows;
- subtle lantern glow;
- pleasing color contrast.

### Night

Create a magical lantern-lit Korean courtyard.

The scene must remain readable.

Do not allow large areas to disappear into near-black darkness.

Use controlled warm/cool contrast.

Do not rely on excessive bloom to make the scene beautiful.

### Materials

Improve:
- celadon ceramics;
- wooden beams;
- roof tiles;
- stone;
- hanji paper;
- decorative metal accents.

Materials should feel intentionally handcrafted.

## 7. IMPROVE CAMERA COMPOSITION

The current environment feels too small in the viewport.

Rework the camera system so the scene has a stronger visual impact.

Requirements:

- Attractive default opening composition.
- Larger and clearer hero subject.
- Less unnecessary empty space.
- Better subject framing.
- Smooth camera transitions.
- Focus presets for the mascot, roof and garden.
- Comfortable orbit limits.
- No unwanted clipping.
- Responsive desktop/mobile framing.

Aim for the meaningful environment to occupy approximately 65–80% of the main 3D presentation area in the default hero view, where appropriate.

Preserve user-controlled camera rotation.

Add an optional cinematic showcase camera mode with a gentle camera path.

Do not use aggressive automatic camera movement.

## 8. ADD MEANINGFUL INTERACTIVITY

Implement a small number of polished interactions.

Examples:

- Click the mascot → greeting or playful reaction.
- Click a lantern → subtle glow response.
- Click the plum tree → gentle falling petals.
- Select a roof point → smooth camera focus.
- Switch day/night → elegant transition.

Every interaction must provide visible feedback.

Do not implement complex game mechanics or backend systems.

## 9. OPTIONAL AMBIENT AUDIO

If appropriate, prepare a lightweight ambient sound system.

Examples:

- Soft environmental wind.
- Subtle lantern chime.
- Gentle character reaction sounds.

Audio must:
- remain optional;
- start muted;
- respect browser autoplay restrictions;
- have a clear mute control;
- use original or appropriately licensed sounds.

Do not add a paid audio service.

Audio is lower priority than animation and visual quality.

## 10. PRESERVE PERFORMANCE

This is a browser-based learning game asset studio.

Do not sacrifice performance to increase visual complexity.

Optimize:

- geometry reuse;
- instancing where suitable;
- draw calls;
- texture dimensions;
- material reuse;
- animation updates;
- light and shadow cost;
- GLB size;
- mobile rendering quality.

Do not claim 60 FPS unless measured on suitable hardware.

Provide low, medium and high quality settings.

Keep reduced-motion support and the WebGL fallback.

## 11. VISUAL VERIFICATION

Do not rely only on automated unit tests.

Inspect actual rendered output.

Required evidence:

1. Daytime screenshot.
2. Evening screenshot.
3. Nighttime screenshot.
4. Mascot close-up.
5. Full arena hero shot.
6. Mobile viewport screenshot.
7. A short animation capture demonstrating actual movement, when capture tooling is available.
8. Before/after visual comparison.

Verify:

- Animations are visibly running.
- The mascot performs distinct reactions.
- Camera transitions are smooth.
- Lighting is readable.
- Scene details are visible.
- Mobile performance remains usable.
- GLB assets remain valid.
- No critical console errors.

Save visual evidence inside `quality-reports/`.

## 12. CHECKPOINT AND RESUME

Continue using the existing persistent checkpoint system.

After every completed subtask:

- Update STUDIO_TASKS.md.
- Update STUDIO_PROGRESS.md.
- Update STUDIO_ASSETS.md.
- Update STUDIO_DECISIONS.md when needed.
- Preserve Blender source files.
- Save generated assets.
- Run relevant tests.
- Create a recoverable Git checkpoint using the authorized workflow.

Do not overwrite approved work without retaining a recoverable version.

If the session is interrupted, the next session must continue from the last verified checkpoint.

## 13. RELEASE POLICY

Work toward a candidate named:

**Korean Arena 3D Studio v0.3 — Living Hanok Showcase**

Before any public deployment:

- Run the production build.
- Validate exported GLB files.
- Verify all animations.
- Inspect rendered results.
- Check for secrets and restricted assets.
- Confirm that the user has authorized publication of the updated showcase.

Do not publish incomplete or unreviewed artwork automatically.

## 14. DEFINITION OF DONE

This milestone is complete when:

1. The Hanok environment is noticeably more detailed.
2. The mascot has clear, expressive motion.
3. Ambient animation is visibly active.
4. Day/evening/night lighting is polished.
5. Camera composition has improved.
6. Interactive objects provide meaningful feedback.
7. The scene feels alive rather than static.
8. Mobile and desktop layouts work.
9. Reduced-motion mode remains accessible.
10. GLB validation passes.
11. Production build passes.
12. Visual evidence is saved.
13. All work is checkpointed.

**Do not begin Hangul Garden.**

Complete the existing golden vertical slice first.

STOP after the v0.3 polish milestone and present the visual results for review.