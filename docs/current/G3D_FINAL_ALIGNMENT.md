# CODEX — G3-D FINAL ARCHITECTURAL ALIGNMENT & SCENE INTEGRATION CORRECTION

**Repository:** `Anapaulagatti/3D-pharse5-`  
**Working branch:** `art-gate/gate3-full-world`

## HUMAN REVIEW DECISION

The latest G3-D candidate has significantly improved the overall world.

The new historical walls, stone materials, urban landscaping and environmental coherence are largely successful.

However, final artistic approval is withheld due to several remaining architectural alignment and scene-integration failures.

**This pass must focus on three regions:**

1. Royal Palace compound.
2. Hanbit Railway Station.
3. Three-building modern commercial block.

Do not regenerate the entire world.

Do not reopen already accepted Namsan, Jeju, historical wall or general landscape artwork unless a directly related defect requires a bounded correction.

Use the seven newly supplied review screenshots as primary visual references.

## TASK 1 — CORRECT MAIN PALACE ALIGNMENT

### Problem

The main royal hall does not visually align convincingly with the ceremonial courtyard axis and public approach.

The approved walls are much better now, but the visible main-hall staircase, doorway, painted foundation and central entrance must be reconciled.

### Required actions

1. Load the actual approved Gate 1 graybox and latest authorized G3 working masterplan.
2. Identify the approved palace compound axis and southern gateway.
3. Measure the actual rendered doorway center, staircase center, building support footprint, painted plinth and visual silhouette.
4. Compare those measurements against the approved courtyard axis.
5. Determine whether the apparent misalignment comes from sprite registration, the source artwork, baked ground/paving or genuinely incompatible geometry.
6. Implement a non-destructive derived-layer correction where the approved footprint permits it.

Important planning references:

- Ceremonial axis: world X = 2048.
- Southern gateway opening: X = 1830–2260.
- Main-hall contact: `(1510,290,1050,460)`.
- Documented painted-plinth conflict: 40px beyond approved support.

These are validation references, not instructions to blindly center every visible pixel.

The apparent center of a roof is not automatically the center of the doorway or structural footprint.

### Palace entrance requirements

The main entrance must have:

- A clearly visible doorway.
- Properly aligned stairs.
- A believable threshold.
- An unobstructed ceremonial approach.
- Correct contact shadows and courtyard paving.
- Collision clearance appropriate to Juni.
- A visually continuous walking route from the southern compound gate to the main entrance.

Do not simply draw a path toward a closed or inaccessible architectural facade and call it completed.

Demonstrate actual character movement to the intended entrance threshold.

If the protected artwork cannot fit the approved geometry, present one narrowly scoped derived-art correction rather than silently relocating the royal hall.

---

## TASK 2 — CORRECT EASTERN PALACE BUILDING AND WALL CLEARANCE

### Problem

The right-side traditional building appears excessively close to the eastern palace boundary.

Its roof and surrounding architectural composition lack convincing separation from the enclosing wall.

The pedestrian entrance is also visually unclear.

### Requirements

- Measure ground-support clearance separately from roof overhang.
- Check the building's footprint against the approved archive/cultural-building reservation.
- Ensure walls do not intersect architecture or block its public entrance.
- Establish a believable side setback and environmental contact where planning permits.
- Preserve the original roof design, ornamental columns, doors and facade craftsmanship.
- Recompose non-protected adjacent landscaping, paving or wall-side details if needed.
- Provide an unobstructed public approach to the correct doorway.

Do not relocate the wall, archive or cultural building solely because their roof projections overlap in screen space.

Distinguish decorative roof overhang, real physical support overlap and inadequate architectural composition.

Where actual protected footprints conflict, provide one measured proposal for human authorization.

---

## TASK 3 — COMPLETELY INTEGRATE HANBIT STATION INTO THE WORLD

### Problem

Hanbit Station still resembles a separate image pasted into the surrounding map.

Three regions remain unacceptable:

**A. Upper station background**

The area behind the roof contains visible source-boundary artifacts, baked vegetation and abrupt paving changes.

**B. Lower station frontage**

The station's forecourt and road edge appear compositionally compressed or misaligned.

The building seems to intrude into the sidewalk/road relationship.

**C. Right station boundary**

The canopy/platform approach and ground are abruptly cut at a source-image edge.

### Required approach

Audit the full station source and its independent runtime layers.

Create explicit ownership for:

- Architecture and roof.
- Roof-attached greenery.
- Background ground.
- Foreground props.
- Canonical forecourt.
- Sidewalk.
- Road and curbs.
- Right-side platform/canopy.
- Shadows and depth-sorted details.

### Upper background repair

Retire obsolete baked ground/background pixels outside the actual building silhouette.

Create clean native environmental ground behind and beside the station.

Ensure the roof's complete intended silhouette remains intact.

Do not remove genuine roof-attached vegetation or HVAC equipment.

No obvious rectangular edges, hard texture cutoffs or leftover source-background fragments.

### Lower frontage repair

Measure:

- Station support footprint.
- Actual building entrance threshold.
- Canonical forecourt bounds.
- Sidewalk clear width.
- Curb position.
- Road lane boundaries.
- Crosswalk alignment.
- Planter placement.

Make the forecourt, sidewalk and road form a credible continuous transit environment.

Do not solve apparent road encroachment by simply hiding the bottom of the station sprite.

Preserve the approved canonical native forecourt pixels, station architecture and corrected planters.

If there is a genuine conflict between the canonical forecourt and protected road, present a specific registration/ownership proposal instead of repainting protected artwork.

### Right boundary repair

Complete the visible station-side canopy and platform approach using correctly separated layers.

Remove the abrupt vertical truncation.

Preserve the original accepted canopy and its architectural identity.

Do not reintroduce the rejected 90×36 paving connector.

Do not claim the 8px platform collision strip has been solved unless actual collision and character movement prove it.

### Final station quality requirement

At native 1:1 and normal gameplay framing, a viewer should not be able to identify the borders of the original station illustration from the surrounding environment.

The station must look deliberately constructed within the same city.

---

## TASK 4 — RESTORE THE THREE MODERN BUILDINGS' UPPER SILHOUETTES

### Problem

The three approved commercial buildings still show unnatural upper-background boundaries.

The rooftops, terraces, planters and surrounding ground look clipped or abruptly composited.

Affected block:

- Modern cafe.
- Bookshop.
- Learning building.

### Required actions

1. Inspect original full-resolution source assets and all crop rectangles.
2. Determine whether each source image contains a complete roof or an already clipped silhouette.
3. Separate roof-attached vegetation from unrelated baked background vegetation.
4. Remove obsolete rectangular source-background remnants.
5. Restore the entire legitimate rooftop and architectural outline.
6. Continue the surrounding ground using compatible urban paving.
7. Correct alpha masks, depth sorting and contact shadows.
8. Eliminate visible seams between the building silhouettes and nearby public space.

If a source image is genuinely clipped, recover a complete verified source where available.

Otherwise, create the minimal native-scale architectural continuation necessary to finish the silhouette.

Preserve approved facade RGB, signage, storefronts, doors, windows and original scale.

Do not hide clipped rooftops under newly added trees.

Do not replace the approved commercial block with a different architectural design.

---

## TASK 5 — CORRECT THE COMMON ROOT CAUSE

These defects suggest an architectural-registration and source-ownership problem, not merely a lack of decorative detail.

Audit:

- Actual facade footprint versus planning contact.
- Roof projection versus ground support.
- Sprite crop bounds.
- Baked background ownership.
- Alpha-mask boundaries.
- Ground texture phase.
- Layer ordering.
- Collision ownership.
- Original artwork completeness.
- Independent environment chunk boundaries.

Build one shared validation process that flags these issues for other existing and future buildings.

Do not treat all visible silhouette overlaps as physical collisions.

Do not claim that matching source hashes proves correct visual placement.

Do not use arbitrary blurring, sharpening, scaling or foliage overlays to conceal defects.

---

## TASK 6 — COORDINATED CORRECTION, NOT MICRO-APPROVAL

Implement all authorized, non-destructive corrections for the three affected areas in one production batch.

Use internal checkpoints and a consolidated defect register.

Do not pause after each planter, roof detail or pavement join.

If protected geometry prevents a particular fix, retain the current accepted artwork for that conflict and prepare a measured alternative. Continue the other independent repairs.

Do not silently reinterpret a protected coordinate or entrance reservation.

---

## TASK 7 — FINAL ACCEPTANCE EVIDENCE

Provide native Phaser before/after images with identical cameras for:

1. Complete palace compound.
2. Main hall entrance and ceremonial axis.
3. Eastern palace building and wall clearance.
4. Palace southern gateway to main hall walking route.
5. Complete Hanbit Station precinct.
6. Station upper-background integration.
7. Station lower frontage, sidewalk, road and crosswalk.
8. Station right canopy/platform boundary.
9. Entire three-building commercial block.
10. Rooftop/upper-silhouette close-ups.

Also provide:

- Registered graybox/current/corrected overlays.
- Actual measured doorway and footprint coordinates.
- Collision/body-clearance audit.
- Real continuous movement video.
- Playable review ZIP.
- Protected-source hash verification.
- Exact list of changed assets and masks.
- PASS / FAIL / NOT TESTED judgments.
- Remaining spatial conflicts requiring human approval.

Review the seven annotated screenshots if available in the task context. If not available to Codex, request their attachment and do not falsely claim annotation-specific validation.

### Visual acceptance

The palace's approach, entrance and architectural hierarchy must read as one coherent compound.

The eastern traditional building must have believable wall relationships and entrance access.

The station must no longer appear as an inserted rectangular illustration.

The three commercial buildings must have complete, naturally integrated upper silhouettes.

## HARD RESTRICTIONS

- No full-world regeneration.
- No changes to approved Gate 1 history.
- No destructive edits to canonical artwork.
- No modification of Juni's original atlas or native size.
- No unapproved relocation of protected buildings.
- No restoration of rejected station connector artwork.
- No new paid image provider API.
- No merge to main or deployment.
- No self-approval based solely on technical tests.

## FINAL INSTRUCTION

**Correct the architectural alignment, physical entrances and environmental ownership—not simply the decorative textures.**

Preserve all recent successful improvements.

Perform this as ONE coordinated correction pass across Palace, Hanbit Station and the modern commercial block.

Stop for one consolidated visual and spatial review after implementation.
The bridge connection on the mainland side has a visibly misaligned structural transition.
The latest reviewer screenshot highlights an unnatural vertical boundary where the bridge meets the mainland waterfront.
The bridge, stone embankment, wooden/stone approach, railings and surrounding water do not appear to form one continuous construction.
1. Inspect the exact bridge start coordinates and the approved mainland landing geometry.
2. Compare the actual visible bridge support footprint with the authoritative Gate 1 graybox.
3. Identify whether the defect originates from misregistration, incomplete source artwork, crop boundaries, alpha masks or incompatible terrain ownership.
4. Reconstruct the localized transition between the mainland embankment and bridge structure.
5. Ensure that the bridge deck joins the mainland pedestrian path at the correct position, orientation and elevation implied by the 2D artwork.
6. Align stone blocks, bridge railings, foundation supports, paving patterns and contact shadows.
7. Correct the surrounding water, foam and shoreline masks to eliminate visible rectangular or vertical seams.
8. Ensure bridge supports have believable contact with the land and water.
9. Preserve the approved bridge design and its existing full-scale proportions.
10. Verify a continuous walkable connection for Juni.
Do not:
- Move the approved bridge endpoints without explicit authorization.
- Resize or distort the bridge.
- Cover structural misalignment with additional trees or bushes.
- Introduce a fake decorative connection that does not correspond to collision geometry.
- Modify the canonical Jeju island artwork.
- Alter unrelated harbor or ferry-terminal structures.
If the bridge support geometry and the approved mainland shoreline are genuinely incompatible, document the exact measured conflict and propose a localized adjustment.
- No visible vertical cut at the mainland bridge landing.
- Continuous pedestrian paving and correct bridge deck alignment.
- Natural stone, railing and foundation connections.
- No floating bridge sections.
- No rectangular water-compositing artifacts.
- Actual Juni traversal from mainland to bridge succeeds with full-body clearance.
The Jeju-side bridge connection also contains an obvious visual discontinuity.
The reviewer screenshot shows mismatched bridge foundations, shoreline contact and basalt cliff geometry near the island landing.
The bridge appears partially attached to a separately authored island illustration instead of being physically integrated into the Jeju terrain.
1. Inspect the approved Jeju bridge arrival coordinates and the current runtime registration.
2. Verify the bridge deck, support columns and railing alignment at the island entrance.
3. Compare the island-side bridge structure against the original Gate 1 physical bridge reservation and the accepted Gate 2 Jeju artwork.
4. Identify the exact source ownership boundary responsible for the unnatural cut.
5. Create a coherent structural transition between the bridge foundation, basalt coastline and island pathway.
6. Align the paving from the bridge into the main Jeju exploration route.
7. Reconstruct only the necessary derived shoreline and bridge-abutment details.
8. Preserve natural basalt rock formations, coastal vegetation, turquoise water and breaking-wave detail.
9. Remove visible vertical seams, clipping artifacts and disconnected stone supports.
10. Ensure bridge railings and their terminal posts have complete, logical endpoints.
11. Preserve the original Jeju house, oreum, orchard, internal footpaths and approved native artwork.
12. Validate physical traversal and visual continuity using actual Phaser gameplay.
The water on both sides of the bridge must belong to a coherent visual system.
Check:
- Wave-scale consistency.
- Water color and texture phase.
- Foam around bridge supports.
- Correct shoreline occlusion.
- No straight source-image borders.
- No artificial water rectangles.
- No duplicate underwater rocks or shadows.
Do not blur the water to conceal seams.
- The bridge visibly connects to the actual Jeju ground.
- Complete, naturally aligned bridge foundations and railings.
- Continuous paving from the bridge to the island pathway.
- No clipped basalt formations.
- No hard water or shoreline boundaries.
- Consistent perspective, material density and lighting.
- Actual Juni traversal from bridge to Jeju succeeds.
Add the following evidence to the existing final review package:
1. Mainland bridge landing — BEFORE / AFTER at native 1:1.
2. Jeju bridge landing — BEFORE / AFTER at native 1:1.
3. Full bridge overview showing both endpoints simultaneously.
4. Bridge structural-alignment overlay.
5. Alpha-mask and source-boundary comparison.
6. Collision and walkable-path overlay.
7. Actual continuous Juni traversal from mainland across the complete bridge onto Jeju.
8. Native 1:1 screenshots of the bridge during gameplay.
9. Protected artwork hash verification.
10. Honest PASS / FAIL status for both bridge landings independently.
Do not mark a bridge connection PASS based only on collision or route-coordinate alignment. Both its visible structural continuity and actual gameplay traversal must be correct.
The coordinated G3-D correction pass now includes FIVE major correction areas:
1. Royal Palace main hall alignment and ceremonial entrance.
2. Eastern palace building and wall clearance.
3. Hanbit Station environmental integration.
4. Modern commercial rooftops and upper silhouette completion.
5. Both Mainland–Jeju bridge landings (TASKS 8 and 9).
Complete these as one consolidated correction batch.
Preserve all previously approved artwork and checkpoints.
Do not request separate approval for each bridge endpoint.
Stop once for full visual and spatial review after all authorized corrections are implemented.
No main merge or deployment.