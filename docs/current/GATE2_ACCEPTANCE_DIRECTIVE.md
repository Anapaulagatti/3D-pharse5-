# CODEX — GATE 2 FINAL ACCEPTANCE CORRECTIONS + PREMIUM MOBILE EXPERIENCE

**Repository:** `Anapaulagatti/3D-pharse5-`

**Working branch:** `art-gate/gate2-three-slices`

## Current Approval Status

The overall Gate 2 artistic direction is accepted for further validation.

The historical north, Jeju architecture, environment details, and historical-to-modern transition have reached the intended visual direction.

The localized Jeju house entrance correction is accepted. Preserve it.

**Gate 3 is NOT authorized yet.**

Complete only the following five final acceptance tasks.

---

## TASK 1 — Original Modern Commercial Architecture Proof

Create exactly ONE new, original modern Korean commercial building at the same craftsmanship level as the approved Muneum street.

Requirements:

- Distinct Korean commercial architecture.
- Full-sized proportions relative to Juni.
- Readable and natural Korean signage.
- Detailed storefronts, windows and interior hints.
- Convincing depth, shading and lighting.
- Sidewalk, doorway and collision consistency.
- Actual playable Phaser scene.

Do not reuse, recolor or rearrange an existing Muneum facade and claim it as new architecture.

Provide native 1:1 screenshots with Juni.

---

## TASK 2 — Jeju Localized World-Fit Correction

Prepare and validate the proposed larger Jeju reservation without shrinking the approved artwork.

Preserve:

- Historic northern geometry.
- Existing mainland buildings.
- Southwest Namsan.
- Southeast amusement park.
- Jeju house, orchard, basalt coast and entrance path.

Resolve bridge-to-island access, ferry landing alignment and shoreline collision.

Do not implement ferry gameplay.

Do not silently modify the approved masterplan.

---

## TASK 3 — Railway Station Exact Fit

Resolve the 10px collision-depth discrepancy locally.

Preserve the approved railway-station artwork.

Verify:

- Full-sized entrance.
- Juni-to-door scale.
- Walkable threshold.
- Collision boundaries.
- Station-to-forecourt connection.
- No unintended overlap with the platform reservation.

Provide native gameplay evidence.

---

## TASK 4 — Small World-Integration Proof

Demonstrate ONE representative seamless connection between approved environment assets.

Validate:

- Consistent camera perspective.
- Native pixel sharpness.
- Correct collision and navigation.
- Compatible environmental lighting.
- No obvious image seams.
- Basic rendering and memory behavior.

Do not build the entire world.

---

## TASK 5 — PREMIUM MOBILE CAMERA & SCENIC EXPLORATION

### Problem

Korean Arena has beautiful, highly detailed environments, but the current mobile viewport shows only a small portion of each scene.

On mobile landscape screens, players may miss the architectural scale, coastal scenery, gardens, landmarks and environmental composition.

The result can feel visually restrictive despite the quality of the artwork.

### Objective

Create an adaptive mobile camera experience that lets players comfortably control Juni while also enjoying the beautiful environments.

The system must feel polished, intuitive and cinematic without compromising the existing artwork.

### 5.1 Smart Follow Camera

Implement an improved mobile-follow camera:

- Keep Juni comfortably visible during movement.
- Allow gentle look-ahead in the walking direction.
- Adapt camera framing to the viewport aspect ratio.
- Respect scene boundaries.
- Avoid jitter, abrupt camera jumps and unwanted cropping.
- Keep architectural entrances and nearby landmarks reasonably visible.
- Maintain comfortable visual scale during regular gameplay.

Do not globally shrink Juni or buildings to make more scenery fit.

### 5.2 Scenic Exploration Mode

Add a visible, compact mobile button for a dedicated Scenic Mode.

When activated:

- Allow users to zoom out to admire more of the environment.
- Allow one-finger camera dragging.
- Allow two-finger pinch-to-zoom.
- Keep the camera inside valid scene boundaries.
- Temporarily separate camera movement from Juni's movement controls.
- Provide a clear "Return to Juni" action.
- Restore the prior gameplay camera smoothly.

Use safe zoom limits, pixel snapping and nearest-neighbor rendering wherever appropriate.

Avoid image blurring, texture filtering artifacts and visually distracting pixel shimmer.

The scene must remain genuine Phaser gameplay rendering, not a static screenshot pretending to be an interactive world.

### 5.3 Full Scene Overview

Provide an optional full-scene overview that fits the complete current environment inside a mobile viewport.

This mode is intended for orientation and appreciating the overall scene composition.

It may use a separate appropriately downsampled overview representation when rendering the complete scene at readable gameplay scale is impossible.

Show:

- Current Juni position.
- Major destinations.
- Recognizable scene landmarks.
- A viewport or camera-position indicator.

Allow players to return to normal gameplay easily.

Do not confuse full-scene overview scale with native 1:1 gameplay scale.

### 5.4 Landmark Showcase Camera

Create a subtle optional environmental camera showcase when first arriving at a major location.

Examples:

- Jeju traditional house and coastal cliffs.
- Jeju orchard and volcanic scenery.
- Historical Korean palace or hanok courtyard.
- Modern Muneum commercial street.
- Railway-station forecourt.

The showcase should briefly reveal an attractive composition and then return control to the player.

Requirements:

- Optional and skippable.
- Never repeatedly interrupt exploration.
- Never teleport Juni.
- No forced camera movement while the player is actively controlling Juni.
- Respect reduced-motion accessibility preferences.

Do not generate new artwork for these showcases.

### 5.5 Mobile Interface

Keep the UI lightweight:

- Movement joystick stays comfortable.
- Run and Explore controls remain usable.
- Scenic Mode and Return-to-Juni controls are accessible.
- Camera controls must not interfere with the joystick.
- Respect mobile safe areas and screen cutouts.
- Support common landscape phone aspect ratios.
- Avoid large opaque overlays that conceal the artwork.

Prefer an elegant, minimal HUD rather than adding numerous permanent buttons.

### 5.6 Mobile Performance and Quality

Test the camera prototype on the existing Gate 2 scenes, prioritizing Jeju and one representative mainland slice.

Do not implement a full-world camera system yet.

Preserve original assets and native source resolution.

Measure and report:

- Gameplay camera zoom and viewport dimensions.
- Maximum viewable scene area.
- Camera behavior during walking and running.
- Scene-edge clamping.
- Pinch and drag interaction.
- Joystick gesture conflicts.
- Pixel clarity at each permitted zoom level.
- Browser frame-time behavior.
- Rendering or memory issues.

Use mobile emulation for repeatable testing. Clearly identify any checks not performed on physical devices.

Do not claim stable hardware FPS without physical-device evidence.

### 5.7 Required Evidence

Deliver:

1. Mobile Follow Mode screenshot.
2. Mobile Scenic Mode screenshot.
3. Full Scene Overview screenshot.
4. A short real in-engine recording showing camera-mode switching, pinch/drag and return to Juni.
5. Desktop-versus-mobile framing comparison.
6. PASS/FAIL results for touch controls, camera boundaries, zoom quality, visual readability and rendering behavior.

The result should answer a practical question:

**Can a mobile player both control Juni comfortably and appreciate the full beauty of Korean Arena's environments?**

---

## HARD RESTRICTIONS

- No redesign of approved historical or Jeju artwork.
- Preserve the approved Jeju house entrance.
- Do not replace Juni or its atlas.
- No unnecessary new image generation.
- No full-world production.
- No Gate 3.
- No merge to main.
- No deployment.
- No changes to the separate Korean Arena application.
- Preserve the approved Gate 1 checkpoints and recoverable source files.

## FINAL DELIVERY

Provide updated evidence for all five tasks.

Separate technical validation from human artistic judgments.

Report every unresolved issue honestly.

**STOP after delivering the five-task Gate 2 acceptance package. Await explicit human approval before opening Gate 3.**