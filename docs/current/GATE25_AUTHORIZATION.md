# CODEX — GATE 2.5: CINEMATIC MOBILE EXPERIENCE & WORLD INTEGRATION VALIDATION

**Repository:** `Anapaulagatti/3D-pharse5-`

**Working branch:** `art-gate/gate2-three-slices`

## AUTHORIZATION

The existing Gate 2 artistic direction is approved as the visual foundation for further development.

Preserve the approved Muneum craftsmanship standard, historical northern environment, modern architecture, Jeju artwork, traditional house entrance, railway station and Juni's original character assets.

This directive authorizes:

1. Cinematic Scenic Tour implementation.
2. Localized Jeju world expansion and connection alignment.
3. A larger multi-environment integration prototype.
4. Preparation and execution of real-device mobile testing when physical devices are available.

**This is Gate 2.5 validation work. Gate 3 full-world production remains LOCKED.**

---

## TASK 1 — CINEMATIC SCENIC TOUR

### Objective

Allow mobile players to appreciate Korean Arena's detailed environmental artwork through a beautiful, smooth, optional cinematic camera experience.

The current Full Scene Overview is useful for navigation, but the scene becomes too small on landscape mobile screens.

Cinematic Scenic Tour must showcase environmental details at a larger visual scale.

### 1.1 Jeju Cinematic Tour

Implement a guided camera tour through the existing Jeju scene.

Required sequence:

**Stop 1 — Coastal Arrival**

Begin near the bridge and coastal entrance. Showcase the turquoise water, basalt cliffs, waves, stone pathways and bridge architecture.

**Stop 2 — Volcanic Oreum**

Smoothly move toward the volcanic crater and elevated walking paths. Show the terrain, cliff formations and surrounding greenery.

**Stop 3 — Tangerine Orchard**

Guide the camera over the orchard, highlighting the planted rows, orange fruits, stone walls, flowers and surrounding landscape.

**Stop 4 — Traditional Jeju House**

Finish at the approved Jeju cultural house, showing its architecture, courtyard, improved entrance path, stairs and nearby coast.

Then offer a clear Return to Juni action.

### 1.2 Camera Behavior

- Use approximately 50% zoom as the primary cinematic framing.
- Adapt framing intelligently to the visible landmark and mobile aspect ratio.
- Smoothly interpolate camera positions between locations.
- Use gentle easing with no abrupt snapping or camera jitter.
- Allow short pauses at important landmarks.
- Maintain nearest-neighbor texture sampling and appropriate pixel alignment.
- Never stretch, distort or non-uniformly resize the artwork.
- Respect scene boundaries and world geometry.
- Preserve the original Juni position throughout the tour.

If 50% zoom cannot frame a landmark attractively, allow a small, justified per-stop zoom adjustment. Record the actual zoom values.

Do not force an entire tall Jeju scene into the phone's landscape viewport.

The purpose is to appreciate each location, not to display every part simultaneously.

### 1.3 Player Controls

Add a compact and accessible:

**Scenic → Start Tour**

During the tour, provide:

- Pause / Resume.
- Skip current landmark.
- Exit Tour / Return to Juni.
- Optional manual camera exploration after pausing.

Disable character movement during automatic camera motion.

Do not interfere with normal joystick input outside the tour.

Manual movement or an explicit exit action must safely cancel automatic camera control.

Respect `prefers-reduced-motion`. Use a static landmark selection or immediate framing instead of automatic motion when reduced motion is enabled.

### 1.4 Other Environments

Reuse the same camera architecture for optional tours of:

- Historical Korean palace and hanok surroundings.
- Modern Muneum commercial street.
- Railway station and entrance forecourt.

For Gate 2.5, only Jeju requires the full cinematic tour. At most one additional short environment demonstration is needed to prove reusability.

Do not generate new artwork.

### 1.5 Preserve Existing Mobile Modes

Keep all current modes:

- Follow Mode — native 1:1 gameplay.
- Scenic Mode — manual drag/pinch exploration.
- Full Scene Overview — entire environment for orientation.
- Cinematic Tour — guided landmark showcase.

These modes must coexist without conflicting gestures or broken camera state.

---

## TASK 2 — APPROVED JEJU LOCALIZED WORLD EXPANSION

### Decision

**The proposed localized Jeju enlargement is APPROVED as a planning amendment.**

You are authorized to integrate the approved candidate into a new versioned working masterplan on the Gate 2.5 branch and validate it in Phaser.

Do not overwrite the original Gate 1 checkpoint.

### Approved Planning Parameters

- Previous world canvas: `4096 × 4608`.
- Authorized candidate canvas: `4352 × 4864`.
- Jeju artwork: retain original native `1024 × 1536` source.
- Jeju study-frame origin: `[3180, 3200]`.
- Preserve the approximately `910 × 1380` painted island without shrinking.
- Keep northern and mainland landmarks at their existing approved coordinates.
- Preserve Namsan southwest and the amusement park southeast.
- Preserve the completed Jeju house entrance.

### Bridge Connection

Approve the localized connection between:

- Mainland shore: `[3160, 3480]`.
- Jeju artwork bridge endpoint: `[3180, 3560]`.

Implement an appropriate connecting path and validate the resulting physical crossing.

Requirements:

- A visually and geometrically continuous connection.
- No disconnected paths or invisible walkable gaps.
- Correct shoreline and bridge collision.
- No unnecessary changes to mainland architecture.
- Juni must cross through normal player movement.
- Do not disguise technical graybox as final bridge artwork.

### Ferry Landing

Approve the proposed island-side landing relocation:

- Mainland boarding: `[2560, 4100]` — unchanged.
- Jeju island landing: `[3180, 4020]`.

Ensure both boarding areas connect naturally to their respective land paths.

The water crossing must remain blocked for pedestrian navigation.

**No operational ferry system, teleportation, boat controls or ferry animations are authorized.**

### Validation

Produce a revised working masterplan, native-resolution Phaser screenshots, collision overlays and actual player-traversal evidence.

Demonstrate that the expanded Jeju remains compatible with the mainland and future world integration.

Preserve the previously approved Gate 1 masterplan as an immutable reference.

---

## TASK 3 — LARGER MULTI-ENVIRONMENT INTEGRATION PROTOTYPE

### Objective

The previous proof joined Muneum Street with the railway station.

Now demonstrate a larger, continuous playable district made from at least THREE independent approved environment sources.

Recommended sequence:

**Muneum Street → Original 오월제과 Bakery → Railway Station Forecourt**

Include the newly created bakery to validate original architecture alongside previously approved assets.

### Requirements

- Preserve native artwork dimensions.
- No arbitrary stretching or shrinking.
- No visible transparent seams.
- No obvious duplicated shadows, roads, objects or vegetation.
- Maintain coherent architecture and scene perspective.
- Align sidewalks, roads, crossings and building entrances.
- Preserve correct Y-sort and occlusion behavior.
- Maintain walkability across every join.
- Avoid double-rendering extracted foreground elements.
- Maintain consistent lighting direction and environmental density.

Do not conceal mismatched joins with arbitrary oversized decorative objects.

If a join is incompatible, identify the exact issue and propose a localized asset or geometry correction.

### Architecture

Use a modular chunk-based loading approach suitable for later expansion.

Avoid assembling the future full world as one enormous image.

Demonstrate:

- Loading adjacent scene chunks.
- Stable camera motion across chunk boundaries.
- Correct collision at joins.
- Asset cache management.
- Reasonable memory usage.
- No repeated loading or visible scene flicker.

This task is an integration prototype only, not authorization to build the entire world.

### Evidence

Deliver one actual playable composite scene, native screenshots, seam close-ups, actual movement footage, route validation and rendering/memory observations.

---

## TASK 4 — REAL MOBILE DEVICE VALIDATION

### Objective

Before expanding artwork production, verify that the new camera and multi-environment prototype provide an enjoyable mobile experience.

Browser emulation alone is insufficient for final mobile acceptance.

### Test Platforms

Prepare testing for at least:

- One physical Android device using Chrome.
- One physical iPhone using Safari.

Use actual connected devices only when accessible.

If physical devices are unavailable, provide a reproducible testing package and a clear manual test procedure.

**Never claim physical-device testing based on desktop browser emulation.**

### Required Test Cases

**Camera and controls**

- Regular Juni movement and running.
- Touch joystick responsiveness.
- Scenic drag and pinch.
- Cinematic tour playback.
- Pause, Skip and Return to Juni.
- Camera clamping near scene edges.
- Smooth transitions between camera modes.
- No gesture conflicts.
- No unintended player teleportation.

**Visual quality**

- Sharp pixel rendering.
- Clear architecture and readable landmark composition.
- No distorted buildings or characters.
- Comfortable Juni visibility.
- No severe UI overlap with the playable scene.
- Correct landscape layout and safe-area insets.
- Reasonable readability on smaller phone screens.

**Performance**

Record actual device model, OS, browser and screen parameters.

Test both short gameplay sessions and a longer continuous exploration session.

Measure, where accessible:

- Average and low-percentile frame-rate behavior.
- Frame-time spikes and camera stutter.
- Scene loading and chunk transition delays.
- Memory-related failures or tab reloads.
- Responsiveness after repeated camera-mode switching.
- Any noticeable thermal or battery issues.

Do not invent FPS, memory, battery or temperature values when measurements are unavailable.

### Mobile UX Acceptance

Evaluate whether a player can comfortably:

1. Move Juni.
2. Recognize surrounding architecture.
3. Enjoy detailed scenery through the cinematic camera.
4. Understand their location through Overview.
5. Return to gameplay without confusion.
6. Explore the larger connected district without major performance or control issues.

Flag any failure requiring a localized correction.

---

## TASK 5 — FINAL GATE 2.5 REVIEW PACKAGE

Deliver a compact but complete review package containing:

1. Cinematic Jeju Tour gameplay video.
2. Mobile Follow / Scenic / Overview / Tour comparisons.
3. Revised Jeju working-masterplan evidence.
4. Bridge and ferry landing alignment/collision evidence.
5. Three-environment playable integration prototype.
6. Native 1:1 screenshots with Juni.
7. Updated browser QA and collision reports.
8. Actual device reports if physical devices are available.
9. A repeatable manual mobile test checklist if they are not.
10. A clear PASS / FAIL / NOT TESTED report.

Explicitly separate:

- Completed implementation.
- Automated/emulated verification.
- Real physical-device verification.
- Human visual/UX approval.
- Remaining production risks.

---

## NON-NEGOTIABLE RESTRICTIONS

- Preserve approved artwork and visual style.
- Preserve Juni's original identity and atlas.
- Preserve Muneum as the craftsmanship benchmark.
- Do not redesign the Jeju cultural house or its entrance.
- Do not rebuild the historical northern world.
- No unnecessary new image generation.
- No implementation of train or ferry gameplay.
- No mass production of new world artwork.
- No main-branch merge or public deployment.
- Do not modify the separate Korean Arena application repository.
- Preserve recoverable checkpoints and original source assets.

## STOP CONDITION

Complete only the authorized Gate 2.5 work.

Jeju's localized planning expansion is approved, but final production bridge artwork, full-world streaming readiness and physical-device acceptance must be validated independently.

**Gate 3 remains LOCKED.**

If the required physical devices are unavailable, mark that acceptance requirement `NOT TESTED`, prepare the handoff package, and stop.

Do not automatically begin full-world production.

Await explicit human approval for Gate 3.