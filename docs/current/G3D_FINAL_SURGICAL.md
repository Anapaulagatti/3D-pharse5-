# CODEX — FINAL G3-D SURGICAL WORLD CORRECTION
## Self-Contained Execution · No Screenshot Attachments · Strict Map Preservation

**Repository:** `Anapaulagatti/3D-pharse5-`

**Working Branch:** `art-gate/gate3-full-world`

**Primary Review Reference:** `docs/gate3-residual/README.md`

**Historical Geometry Authority:** `assets-src/world-gate1/plan.json` plus all subsequently approved masterplan amendments.

**Visual Quality Authority:** Approved Gate 1, Gate 2.5, and the latest accepted G3-D architectural/environmental improvements.

---

# 0. CRITICAL HUMAN DIRECTIVE

The Korean Arena world is now very close to the desired artistic quality.

However, several identifiable residual visual defects remain, and two intentional changes are authorized:

1. Replace the problematic Hanbit Station rendering with a newly integrated Gate 1-quality station candidate.
2. Convert the small northwestern forest patch into a future gameplay-ready agricultural farm.

The remaining work must be performed as a **SURGICAL CORRECTION**, not a map reconstruction.

## MOST IMPORTANT RULE

**DO NOT REBUILD, REGENERATE, RECOMPOSE OR REDESIGN THE ENTIRE WORLD.**

The current approved-looking world must remain intact.

Only the specifically identified target regions may be modified.

The prior failure mode—changing large portions of an otherwise successful map while attempting localized visual repairs—must not occur again.

## NO SCREENSHOT ATTACHMENTS REQUIRED

The user will NOT provide additional annotated screenshots.

Do not ask for them.

Do not depend on red circles, black circles, uploaded images, chat attachments, or inaccessible previous conversation media.

Instead, identify every target by examining:

- The current repository.
- Approved masterplans.
- World-coordinate registrations.
- Source asset names and metadata.
- Existing Phaser scene definitions.
- Previously committed review galleries.
- Native source images already stored in the repository.
- Ground and foreground chunk ownership.
- Current collision and route definitions.

You are authorized to generate your OWN temporary native Phaser screenshots and diagnostic overlays for analysis.

Use actual repository evidence, not guessed image locations.

If an exact target cannot be identified reliably, leave that region unchanged and document the ambiguity. Do not arbitrarily modify another area.

---

# TASK 1 — ESTABLISH AN IMMUTABLE WORLD BASELINE

Before editing:

1. Identify the latest complete G3-D candidate and current Git HEAD.
2. Preserve a recoverable checkpoint.
3. Record all source-asset hashes.
4. Capture one full-world overview from the current runtime.
5. Capture native 1:1 views of the target regions.
6. Record current building placements, source rectangles and collision ownership.

Create:

`docs/gate3-final/BASELINE.md`

`docs/gate3-final/REGION_TARGETS.json`

The region-target file must include:

- Region name.
- Exact world-coordinate bounding box.
- Source assets involved.
- Runtime layers involved.
- Approved objects contained within the region.
- Allowed modification types.
- Protected neighboring objects.
- Maximum intended change area.

**These bounds must be discovered from the current project, not invented from screenshots.**

Establish a strict out-of-scope pixel-difference check.

Changes outside authorized regions must be treated as regression failures.

Do not use the entire world canvas as an allowed edit region.

---

# TASK 2 — RESTORE THE CLIPPED HISTORICAL HOUSE WEST OF THE PALACE

## Target identification

Locate the small traditional Korean house in the western/northwestern historical precinct, outside the main palace hall compound, near the historic academy-side pedestrian path.

This is the existing historical house whose upper-left roof/building silhouette appears incomplete or clipped.

Use the current source registrations and native architecture images to distinguish it from neighboring traditional buildings.

## Required repairs

- Recover its complete roof silhouette.
- Restore any missing upper-left roof geometry.
- Repair incomplete eaves, roof-end ornamentation and timber supports.
- Restore the readable architectural volume.
- Remove source-crop artifacts.
- Preserve the current approved facade and doors.
- Maintain native Gate 1 roof-tile detail, perspective and lighting.
- Preserve original building scale and world position.

If the full original roof exists in an earlier source, recover it without resizing.

If the source is genuinely incomplete, create only the missing architectural continuation as a bounded derived asset.

Do not replace the building with a different hanok.

## Acceptance

The building must look like one complete traditional Korean house.

No half-roof, cropped corner, visibly pasted extension or disconnected architectural element.

---

# TASK 3 — RESTORE THE COURTYARD DIRECTLY BELOW THE SAME HOUSE

## Target identification

Locate the landscaped courtyard immediately south/below the western historical house identified in Task 2.

This is the enclosed planted area associated with the same western historical precinct.

Do not confuse it with the central palace ceremonial courtyard.

## Required repairs

Restore the complete small courtyard composition:

- Garden enclosure.
- Stone edging.
- Low walls.
- Benches or original fixtures where applicable.
- Original vegetation silhouettes.
- Stone paving transitions.
- Paths connecting to nearby pedestrian circulation.
- Natural ground contact and shadows.

Eliminate:

- Half-rendered garden structures.
- Cut-off flowerbeds.
- Unnatural rectangular vegetation boundaries.
- Disconnected enclosure corners.
- Floating stones or props.
- Incomplete source-image fragments.

Use the current approved scene as the design basis.

Do not turn this courtyard into another large forest area.

Do not extend the repair beyond its actual courtyard and immediate connection boundaries.

---

# TASK 4 — REPLACE THE NORTHWEST FOREST PATCH WITH A SMALL FARM

## Authorized design change

Convert the existing small forest patch at the TOP-LEFT / NORTHWEST portion of the world into a compact, attractive Korean agricultural farm.

## Target identification

Find the unprotected woodland patch:

- Near the northwestern outer edge of the mainland.
- West/northwest of the palace compound.
- North of the western historical academy precinct.
- Outside the protected palace ceremonial grounds and wall-support footprint.

Use the latest authorized masterplan to identify the actual available space.

This is a LOCAL LAND-USE REPLACEMENT, not permission to redesign the complete northern region.

## Farm composition

Create a beautiful small traditional Korean farming area.

Target approximately **4–8 separate cultivated plots**, depending on the actual available dimensions.

Prefer a clean, intentional arrangement such as two rows of three plots if the footprint supports it.

Every plot should have:

- Clear boundaries.
- Consistent native dimensions.
- Readable soil texture.
- Distinct plot ID.
- Walkable access between plots.
- Defined crop-growth display area.
- Appropriate ground ownership.

Introduce a restrained selection of:

- Cultivated soil beds.
- Small green crops.
- Narrow paths.
- Low wooden fencing or stone borders.
- Simple agricultural props.
- Watering/storage decoration where space permits.

A tiny shed may be included only if it fits without crowding the farm or obstructing existing routes.

## Future gameplay readiness

The farm should support future farming gameplay.

Create lightweight metadata for each plot, including:

- Unique plot ID.
- World-space bounding rectangle.
- Crop-display anchor.
- Interaction anchor.
- State placeholder such as empty, planted or ready.
- Navigation/collision classification.

Do NOT implement a new farming system, inventory, economy, crop timers or quests yet.

Only prepare the farm spatially and structurally for later gameplay integration.

## Strict location restrictions

Do not:

- Modify palace buildings or historic walls.
- Remove protected historic gardens.
- Block the existing main walking paths.
- Allocate new world land.
- Change the coastline.
- Move the palace or academy.
- Turn the entire northwest into farmland.

Preserve existing useful border trees when they help transition the agricultural area into the surrounding landscape.

## Artistic objective

The farm must look like it was always intended to belong in Korean Arena.

Use the same perspective, pixel density, warm lighting, stonework and vegetation craftsmanship as the approved Gate 1 environment.

---

# TASK 5 — CONTROLLED REPLACEMENT OF HANBIT RAILWAY STATION

## Important human authorization

Previous localized compositing attempts have repeatedly failed to make Hanbit Station look naturally integrated with the surrounding world.

Therefore, a controlled new station artwork candidate is explicitly authorized.

**This is permission to replace the active rendered station asset—not permission to delete the historical source or rebuild the railway district.**

## Step A — Preserve the existing station

Before replacement:

- Save the old station and all relevant source files.
- Record its full source bounds.
- Record its world registration and logical coordinates.
- Record its entrance and platform relationship.
- Preserve the original station canopy and prior approved references.
- Preserve collision and navigation data as the initial technical baseline.

The old station must remain recoverable.

Do not destructively erase it from the repository.

## Step B — Reconstruct the surrounding ground first

Identify and isolate the authorized station architectural footprint.

Remove the OLD STATION'S ACTIVE RENDERED INSTANCE from the isolated replacement candidate.

Do not leave the old station baked beneath the new version.

Rebuild the underlying non-protected environmental ground only where the old station source owned obsolete pixels.

The surrounding world must remain untouched.

The rebuilt local environment should include coherent:

- Stone paving.
- Sidewalks.
- Station approach space.
- Urban landscape borders.
- Rear paved ground.
- Appropriate roof/background depth.
- Road-to-forecourt transition.
- Eastern platform approach.

Preserve approved road and curb positions.

Preserve the canonical restored native station forecourt and approved planters unless a separate bounded visual candidate is required to resolve an actual conflict.

## Step C — Create the new station as native world artwork

Create a new Hanbit Railway Station that:

- Follows the Gate 1 / Gate 2.5 artistic quality benchmark.
- Retains Hanbit Station identity.
- Preserves a recognizable Korean station character.
- Has appropriate entrance doors and ticket-hall readability.
- Has clear Korean signage and clock.
- Has believable roof, upper story and facade proportions.
- Matches Juni's approved native scale.
- Integrates structurally with the surrounding urban environment.

Use authentic architectural composition, native-scale assets and consistent perspective.

Do not create a generic small building merely because it is easier to composite.

The station must look complete and appropriate in the planned district.

## Step D — Integrate the station directly into the environment

The new station must use independent logical rendering layers:

1. Ground.
2. Architecture.
3. Roof and elevated architecture.
4. Foreground props.
5. Station/platform components.
6. Appropriate shadows and occlusion.

Remove obsolete source-background ownership from the candidate.

Do not create a large rectangular building image containing incompatible baked ground.

The station must connect naturally to:

- Rear plaza.
- Eastern platform stairs.
- Main entrance.
- Existing approved forecourt.
- Sidewalk.
- Public road.
- Nearby amusement-park precinct.

## Step E — Preserve planning and gameplay

Keep the authorized railway-station reservation and approved logical station coordinates.

Preserve the intended entrance destination and station function.

Do not move the attraction area or protected roads.

Do not modify Juni.

Ensure actual character movement reaches the station entrance.

Maintain established depth sorting.

The historical 8px platform-transfer collision defect remains a separate issue. Do not falsely mark it solved merely because the new station looks complete.

Do not reintroduce the previously rejected 90×36 paving connector.

## Step F — Replace only if the candidate is better

Produce an isolated OLD versus NEW comparison using identical native Phaser camera placement.

Verify:

- Visual integration.
- Correct building scale.
- Entrance alignment.
- No rectangular seams.
- No clipped roof or vegetation.
- No collision regression.
- No damaged neighboring scenery.
- No changes outside the authorized station precinct.

If the new station fails these requirements, preserve the old active station and submit the new asset as a separate rejected or pending candidate.

**Do not force a visually worse replacement into the main playable world.**

---

# TASK 6 — REPAIR REMAINING COASTLINE AND BRIDGE LANDINGS

The existing coastal environment and Jeju island are largely successful.

Do not recreate them.

Target only the known residual defects in:

- Mainland bridge landing.
- Jeju-side bridge landing.
- Water immediately adjacent to both landings.
- Local retaining-wall contacts.
- Southern mainland promenade and asphalt-material join.

## Required repair

Identify the actual source-image and world-coordinate ownership boundaries.

Correct:

- Abrupt vertical texture cuts.
- Bridge-to-shore geometry mismatch.
- Unnatural water-edge transitions.
- Incomplete basalt/stone contacts.
- Misaligned terminal posts and railings.
- Local paving and road seams.
- Rectangular ground or water fragments.

Preserve:

- Jeju island canonical source image.
- Oreum volcanic terrain.
- Orchard.
- Traditional house.
- Internal paths.
- Turquoise coastline.
- Approved bridge endpoints.
- Existing ferry pier and southern promenade.
- Original Juni.

Do not redesign the bridge or alter its approved endpoints.

The known bridge stop/turn contact defects must remain accurately reported.

If complete native clearance requires widening structural support, create a separate measured proposal rather than silently adding invisible collision floor.

---

# TASK 7 — MINOR HISTORICAL AND COMMERCIAL RESIDUAL CLEANUP

Perform only localized fixes to defects identified from existing scene/source ownership.

### Historical palace

Inspect the already-corrected ceremonial entrance.

Repair only remaining genuine architectural contact defects, incomplete stone-rail endings or courtyard seams.

Do not reposition the royal hall.

Do not reopen the approved palace-wall layout.

### Modern commercial buildings

Preserve the approved cafe, bookshop and learning-building facades.

Only correct genuine remaining roof/background source-edge defects.

Do not regenerate the commercial block.

Do not add excessive rooftop or street vegetation.

Do not change protected storefront signs, windows, doors or native scale.

These are low-scope cleanup actions, not separate rebuilding tasks.

---

# TASK 8 — STRICT CHANGE-SCOPE ENFORCEMENT

This task requires enforceable protection against accidental map-wide regeneration.

## Allowed changes

Only:

- Western historical house roof/completion.
- Its immediately associated courtyard.
- Northwestern unprotected forest-to-farm conversion.
- Isolated Hanbit Station replacement candidate and its necessary local environment.
- Specifically bounded coastal/bridge junction repairs.
- Small proven historical/retail residual corrections.

## Forbidden changes

- Regenerating the full world atlas.
- Replacing the entire ground map.
- Rebuilding the historical north.
- Reconstructing the modern south.
- Modifying approved Jeju land artwork.
- Repositioning the palace.
- Moving approved bridges.
- Rescaling Juni.
- Shifting unrelated buildings.
- Replacing unrelated background chunks.
- Global texture-filter or color changes.
- Uncontrolled ocean regeneration.
- Automatic masterplan rewriting.

## Automated regression requirements

Capture baseline and candidate full-world images at identical resolution and camera registration.

Compare pixel differences outside the explicitly approved regions.

Every unexpected difference must be investigated.

Dynamic Juni, animated water and other non-deterministic effects must be excluded or rendered in a deterministic test mode for fair comparison.

Reject changes that modify unrelated locations.

Maintain protected source hashes.

Report all changes to:

- Source images.
- Derived images.
- Ground chunks.
- Foreground chunks.
- World registrations.
- Collision fields.
- Metadata.

No unrelated cleanup or opportunistic refactoring.

---

# TASK 9 — REPRODUCIBLE NATIVE VALIDATION

After all authorized corrections, run actual Phaser validation.

Capture:

1. Full-world overview — BEFORE and AFTER.
2. Northwestern farm — BEFORE and AFTER.
3. Western historical house — BEFORE and AFTER.
4. Historical courtyard — BEFORE and AFTER.
5. Hanbit Station — OLD and NEW candidate.
6. Station surrounding ground and right platform approach.
7. Mainland bridge landing.
8. Jeju bridge landing.
9. Southern promenade material join.
10. Any accepted minor palace/retail repairs.

All comparisons must use matching camera positions.

Supply actual native 1:1 screenshots, not only resized previews.

## Gameplay validation

Verify actual Juni movement:

- Around the repaired historical house.
- Through the small courtyard.
- Along the farm paths.
- Toward the railway-station entrance.
- Through existing nearby road crossings.
- Across mainland and Jeju bridge approaches.

Preserve all previously working routes.

Do not claim that build tests prove collision clearance.

## Quality checks

Verify:

- No clipped roofs.
- No broken courtyard corners.
- No pasted station plates.
- No duplicate old/new station layers.
- No cropped architectural edges.
- No obvious material joins.
- No visible unintentional alpha seams.
- No floating bridge structures.
- No unexpected map-wide pixel changes.
- No broken entrances.
- No damage to protected artwork.

---

# TASK 10 — FINAL DELIVERY PACKAGE

Produce one consolidated review package containing:

1. Updated playable ZIP.
2. Full-world BEFORE/AFTER overview.
3. Native comparison gallery.
4. New station standalone review and integrated gameplay views.
5. Northwestern farm layout and plot metadata.
6. Corrected historical house and courtyard evidence.
7. Bridge and coastline repair comparisons.
8. Actual gameplay movement video.
9. Out-of-scope pixel-difference audit.
10. Changed-file and changed-chunk manifest.
11. Protected asset hash report.
12. Updated defect register.
13. PASS / FAIL / NOT TESTED summary.

List the exact authorized areas modified and confirm which regions remained pixel-identical.

Keep all unresolved Bakery placement, inherited public-route, bridge body-clearance and physical mobile-performance issues visible rather than claiming they disappeared.

---

# EXECUTION POLICY

You are authorized to complete all tasks in this prompt in one coordinated development pass.

Do not request screenshots or image attachments from the user.

Do not interrupt work for approval of individual plants, roof corners, minor ground details or alpha masks.

Do not abandon the whole task merely because one protected spatial conflict cannot be solved. Complete all independent authorized corrections and report any blocked item separately.

Preserve all approved checkpoints.

No force pushes.

No destructive source replacement.

No new paid image-generation API.

No merge into main.

No public deployment.

No modification of the separate Korean Arena application.

## STOP CONDITION

Stop once after the consolidated candidate, playable package, native evidence and regression report are ready.

If a critical issue requires an unauthorized world-layout change, do not implement that change. Document the conflict and complete all other independent tasks.

---

# FINAL NON-NEGOTIABLE INSTRUCTION

**THIS IS NOT A FULL-WORLD REBUILD.**

The world is already close to the intended artistic result.

Your responsibility is to preserve the beautiful existing environment while executing a few exact, bounded corrections.

Complete the clipped historic house, its courtyard, the compact northwestern farm, a properly integrated Hanbit Station candidate and the remaining coastal connections.

All other world regions must remain unchanged.

**Preserve 95%+ of the achieved visual composition as the design intent—not as permission to modify the remaining 5% arbitrarily.**

Enforce this through explicit region masks and out-of-scope regression checks rather than an estimated percentage alone.

The final game world must look intentionally authored in a consistent Gate 1 artistic language.

Do not solve local defects by rebuilding unrelated parts of the map.

**MAKE THE WORLD BETTER WITHOUT DESTROYING WHAT IS ALREADY GOOD.**