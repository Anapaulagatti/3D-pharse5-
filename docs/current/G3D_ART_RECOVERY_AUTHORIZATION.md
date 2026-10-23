# CODEX — G3-D CRITICAL ART DIRECTION RECOVERY
## Restore Gate 1 / Gate 2.5 Visual Quality Across the Entire Korean Arena World

**Repository:** `Anapaulagatti/3D-pharse5-`

**Working branch:** `art-gate/gate3-full-world`

## 1. HUMAN REVIEW DECISION

The G3-B/C playable world prototype is acknowledged as a technical integration milestone.

However, **the current full-world artistic quality is REJECTED**.

The new environment no longer consistently follows the approved Gate 1 and Gate 2.5 artistic direction.

The world contains beautiful protected architecture and Jeju assets, but the newly authored terrain, landscaping, transitions and several landmarks look noticeably different in scale, material craftsmanship, environmental detail and composition.

This creates the impression of unrelated visual assets assembled into one map.

This is not merely an isolated texture or seam defect.

**It is a systemic art-direction consistency problem.**

Preserve the current prototype as a recoverable checkpoint. Do not discard the completed world engine or revert the project to Gate 2.

G3-D must include a coordinated visual recovery pass.

---

## TASK 1 — ESTABLISH THE CANONICAL ART DIRECTION

Use the original approved Gate 1 planning/artistic references and accepted Gate 2/2.5 native assets as the authoritative visual standard.

Mandatory references:

- Approved historical northern Korean environment.
- Muneum commercial street.
- Original 오월제과 Bakery.
- Hanbit Station with accepted restored native paving.
- Approved Jeju island and traditional cultural house.
- Accepted seamless district artwork.

Create a documented **Korean Arena Art Direction Bible**.

Define measurable visual characteristics for:

### Perspective and Scale

- Consistent top-down 3/4 orthographic-style perspective.
- Coherent architectural proportions.
- Building, tree, doorway, bench, street and path scale relative to Juni.
- Consistent roof, facade and ground relationships.
- No miniature-looking landmarks within full-scale surroundings.

### Materials

- Detailed Korean stone paving.
- Distinct stone joints and surface grain.
- Natural grass, foliage and soil.
- Believable asphalt, gravel, timber and basalt.
- Consistent texture frequency and pixel-detail density.
- No oversized or repeated ground samples that appear visibly tiled.

### Lighting and Color

- Consistent warm environmental illumination.
- Coherent shadow direction.
- Natural contact shadows.
- Harmonious regional colors.
- Consistent contrast and environmental depth.

### Landscape Composition

- Organic vegetation placement.
- Complete tree trunks and foliage silhouettes.
- Natural elevation changes.
- Designed public gardens and pathways.
- Architecturally believable transition spaces.
- No sudden rectangular changes between unrelated terrain sources.

The style reference must be based on actual approved assets, not newly invented generic pixel-art aesthetics.

---

## TASK 2 — PERFORM A FULL-WORLD VISUAL AUDIT

Review the current 4352×4864 world using both:

1. The entire world overview.
2. Actual native 1:1 Phaser screenshots for each region.

Do not evaluate fine pixel fidelity from the heavily downscaled world overview alone.

Inspect all ten planned regions.

### Historical North

Check the new palace, archive, workshop, courtyards, gardens and boundary walls.

Find areas where new materials fail to match the craftsmanship of the approved historical buildings.

Review architecture-to-ground transitions and environmental density.

### Historical-to-Modern Transition

Identify hard rectangular boundaries, mismatched grass, disconnected walls, paving-size changes and unnatural tree placement.

### Modern South

Retain the approved facades and streets.

Identify newly generated surrounding ground, landscaping and public-space materials that are inconsistent with Muneum.

### Namsan

Evaluate terrain slopes, hillside contours, tower scale, doorway dimensions, footpaths, forest composition and environmental depth.

The tower should feel naturally built into a real Namsan hill environment, not placed on a flat grass texture.

### Amusement Park

Evaluate carousel and wheel scale, foreground projection, station visibility, entrance design, pedestrian areas and thematic consistency.

### Railway District

Protect the station artwork.

Review how the new platforms, tracks, roads and surrounding spaces integrate with the accepted station environment.

### Waterfront

Review harbor architecture, market, ferry building, coastal paths and shoreline continuity.

### Jeju

Preserve the approved island.

Inspect its connections to mainland, bridge, coastal water and neighboring world materials.

Do not recreate the approved island simply to match poorer newly generated terrain.

### Audit Deliverable

Create:

`GATE3_WORLD_ART_DIRECTION_AUDIT.md`

For every region, report:

- Approved assets retained.
- Newly generated assets requiring correction.
- Visual style deviations.
- Scale inconsistencies.
- Material inconsistencies.
- Landscape composition defects.
- Transition problems.
- Required correction families.
- Severity and affected source assets.

---

## TASK 3 — REBUILD THE SHARED MATERIAL SYSTEM

The existing new terrain materials show excessive repetition and differences in detail scale.

Do not solve this with global sharpen, blur, random noise or additional oversized decorative objects.

Instead, create a coordinated material system compatible with the approved environments.

### Ground Material Families

Build coherent native-resolution material families for:

- Historical Korean courtyards.
- Modern Korean sidewalks.
- Roads and curb transitions.
- Namsan soil and vegetation.
- Garden paths.
- Amusement-park walkways.
- Coastal ground and basalt.
- Harbor platforms and wooden decking.
- Grass, gravel and planting beds.

### Strict Requirements

- Consistent perspective.
- Correct native texel density.
- Material-specific variation without obvious repeated patterns.
- Natural transitions between materials.
- Correct contact shadows and surface boundaries.
- No pixel-level softness caused by resizing.
- No large rectangular material patches.
- No painting over approved architecture.

Fix shared material sources centrally and regenerate only dependent world chunks.

Avoid independently repainting the same repeated defect hundreds of times.

---

## TASK 4 — RESTORE COHERENT ENVIRONMENTAL COMPOSITION

Treat the full world as one designed environment rather than individual sprites placed on large ground textures.

### Northern Region

Create a coherent landscape connecting the palace, courtyards, archive, workshop and approved historical district.

### Southern Region

Connect commercial areas, Namsan, station, amusement park and waterfront using intentional urban design.

### Namsan

Develop believable hillside contours, vegetation layers and pedestrian routes without changing protected landmark positions.

### Amusement Park

Create an attractive surrounding park composition while retaining existing reservation requirements.

### Coastline

Make the transition from mainland to water, bridge and Jeju feel natural and spatially consistent.

### Critical Rules

- No visible collage boundaries.
- No isolated building surrounded by mismatched grass.
- No incomplete scenery.
- No floating or sliced trees.
- No disconnected wall segments.
- No abrupt changes in lighting or terrain scale.
- No unexplained empty regions presented as completed artwork.

Design neighboring chunk boundaries together.

---

## TASK 5 — REVALIDATE ALL NEW LANDMARKS

Audit every newly authored architectural asset beside Juni at native scale.

Priority:

- Palace continuation.
- Archive.
- Cultural workshop.
- Namsan Tower.
- Carousel.
- Ferris wheel.
- Harbor market.
- Ferry building.

Verify:

- Door scale.
- Building footprint.
- Roof and facade proportions.
- Native texture sharpness.
- Ground contact.
- Correct visual occlusion.
- Foreground depth.
- Architectural identity.
- Lighting compatibility with surrounding environments.

If a generated asset has the wrong inherent proportions or visual language, produce a corrected candidate rather than attempting to disguise the mismatch with landscaping.

Never shrink Juni or globally rescale buildings to conceal a style conflict.

---

## TASK 6 — PRESERVE THE EXISTING WORLD ENGINE

The current G3-C technical prototype must remain recoverable and functional throughout the artistic correction process.

Preserve:

- Chunk loading and caching.
- Existing world dimensions.
- Current approved spatial plan.
- Juni's original atlas and controls.
- Mobile Follow, Scenic, Overview and Cinematic Tour.
- Collision and interaction infrastructure.
- Accepted station forecourt.
- Original station canopy BEFORE artwork.
- Approved Jeju assets.
- Protected Git checkpoints.

Artistic reconstruction must use new versioned derivative assets.

Do not silently rewrite approved source artwork.

Do not reactivate the rejected 90×36 station-platform connector.

Record unavoidable changes to physical object ownership or collision separately.

---

## TASK 7 — PRODUCTION VALIDATION STRATEGY

Do not immediately mass-generate a new complete world using an unverified art pipeline.

First validate the corrected shared style system across three representative regions:

**A. Historical North:** architecture, stone, grass and garden composition.

**B. Modern South:** approved commercial buildings plus newly corrected roads, sidewalks and vegetation.

**C. Namsan:** terrain depth, tower integration and natural hillside vegetation.

For each pilot, provide:

- Approved reference versus current prototype versus corrected candidate.
- Native 1:1 Phaser screenshots.
- Juni scale comparison.
- Pixel-density and material consistency analysis.
- Seam and ground-contact checks.

These are three representative tests of ONE shared art direction, not three separate artistic styles.

Stop once for human approval of this unified correction system.

After that approval, apply the accepted system across all remaining regions as one coordinated production batch.

Do not restart a separate approval cycle for every tree, building, paving detail or chunk.

---

## TASK 8 — CONSOLIDATED G3-D RECOVERY

Once the shared art direction has been validated:

1. Correct all affected ground-material families.
2. Complete region-specific landscape composition.
3. Repair old/new asset integration boundaries.
4. Resolve new landmark scale and depth issues.
5. Rebuild only impacted runtime chunks.
6. Inspect the whole world for remaining unfinished regions.
7. Update the coverage and defect registers.
8. Preserve the current Bakery placement decision as unresolved until expressly authorized.
9. Keep all genuine P1 navigation and performance issues visible.
10. Generate a full-world QA package.

The accepted artistic standard must be applied consistently throughout the world, including newly authored content.

Do not mark a region complete merely because it has an image, an atlas sprite, or a reachable destination.

---

## FINAL ACCEPTANCE CRITERIA

The corrected world must demonstrate:

- Consistent Gate 1 / Gate 2.5 visual identity.
- Buildings and environments that feel authored in the same artistic universe.
- Natural architectural and landscape continuity.
- Cohesive native detail scale.
- Crisp material rendering.
- Full-sized believable landmarks.
- No conspicuous collage boundaries.
- No repetitive large ground tiles.
- No incomplete terrain disguised as finished artwork.
- Preserved Juni and approved assets.
- Reproducible build, source provenance and actual Phaser evidence.

The overview must feel like one unified Korean world, not a collection of unrelated illustration patches.

## NON-NEGOTIABLE RESTRICTIONS

- No destructive asset overwrite.
- No changes to approved Gate 1 or Gate 2.5 checkpoints.
- No unauthorized major masterplan amendments.
- No paid image-generation services without permission.
- No replacing approved high-quality art with lower-quality alternatives.
- No main merge or public deployment.
- No claim of full production completion while required content remains missing.
- No false PASS based only on build, hashes, native resolution or movement tests.

## FINAL INSTRUCTION

**G3-B/C technical progress is retained. G3-D artistic recovery is authorized for planning and representative validation.**

First deliver the unified Art Direction Bible, full-world audit and three corrected representative regions.

Following explicit approval of the shared visual system, perform the full-world correction as a consolidated batch.

**DO NOT downgrade Gate 1 quality to fit the new world. Upgrade the new world to match Gate 1.**