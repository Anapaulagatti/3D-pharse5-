# KOREAN ARENA — V7 WORLD RECONSTRUCTION
## NON-NEGOTIABLE ENVIRONMENT QUALITY RECOVERY

**Repository:** `Anapaulagatti/3D-pharse5-`
**Working branch:** `rebuild/pixel-social-rpg-v3`

**Your role:** Principal Game Art Director, Senior Level Designer, Korean Urban Landscape Architect, Pixel Art Technical Director and Phaser Engineer.

## 0. CRITICAL INSTRUCTION — READ FIRST

The current map has undergone too many superficial revisions.

Previous passes repeatedly improved individual tiles while failing to correct the underlying environment composition.

**DO NOT perform another surface-level polish.**

The approved architectural assets are valuable. The existing road network, landscape circulation, modern district arrangement and waterfront construction are NOT visually approved.

You are authorized to completely reconstruct those defective systems.

**The objective is not to preserve the current roads. The objective is to deliver a genuinely beautiful, coherent and playable world.**

This task must be executed in the actual Phaser game, not merely planned or illustrated.

## 1. ESTABLISH THE BASELINE AND REFERENCE

Before editing:

1. Inspect the latest actual GitHub commit, current source, approved map assets and runtime dependencies.
2. Read `AGENTS.md`, `docs/ART_SKILL_REGISTRY.md`, production reports and relevant `STUDIO_*` files.
3. Read the installed Agent Sprite Forge skills and previous successful environment-generation records.
4. Inspect the previous approved composition reference at `docs/v6-restructure/reference-user.png`, if available.
5. Inspect the latest native Phaser overview and gameplay captures.
6. Create and verify a pushed recovery checkpoint.

**Use the earlier polished reference as the composition and art-direction quality target, NOT as a bitmap to paste, trace or stretch into the game.**

The reference demonstrates:

- Graceful enclosed Namsan park.
- Well-organized central modern station.
- Beautiful and clearly bounded amusement park.
- Balanced architectural spacing.
- Vivid but harmonious modern colors.
- Coherent waterfront promenade and ferry area.
- Attractive island paths and meaningful island arrival.
- A natural transition between historical and modern Korea.

If the reference cannot be found, use the existing repository review materials and documented requirements. Do not invent a claim that it was inspected.

## 2. LOCK APPROVED CONTENT — REBUILD REJECTED CONTENT

### MUST PRESERVE

- Juni's approved design, sprites and animation system.
- Historical palace, academy and traditional architecture.
- Approved major landmark artwork and recognizable silhouettes.
- Original high-quality pixel textures and their editable sources.
- Established Korean architectural identity.
- Working lessons, dialogue and interactions.
- Existing mobile landscape joystick controls.
- Source recovery points and Git history.

### AUTHORIZED TO REBUILD

- All defective ground paths, roads and paving.
- Modern district site planning and landscape arrangement.
- Namsan paths, enclosures and viewpoint circulation.
- Modern station forecourt and street hierarchy.
- Amusement-park pedestrian circulation.
- Waterfront promenade, ferry boarding area and pier surfaces.
- Jeju pedestrian paths and access connections.
- Landscaping, boundary treatments and environmental color balance.
- Navigation meshes, tilemaps, collisions and object coordinates required by the new layout.

**Do not preserve bad road geometry merely to keep old collider counts, coordinate values or tests unchanged.**

Update affected navigation and collision data correctly. Do not remove or weaken safety checks.

## 3. DELETE THE FAILED ROAD SYSTEM BEFORE REBUILDING

Do not stack new paving over old paving.

Perform an actual road-system reconstruction:

1. Identify the source layers generating the existing defective roads.
2. Remove obsolete road masks, overlapping paving layers, redundant patches and superseded path definitions.
3. Rebuild the road hierarchy from clean editable geometry.
4. Generate coherent ground surfaces, edges, corners, intersections and transitions.
5. Validate the composed terrain in the actual Phaser renderer.

**Forbidden shortcuts:**

- Painting rectangular patches over broken intersections.
- Adding fences to conceal poor layouts.
- Reusing one gray paving texture everywhere.
- Creating large geometric wedges to connect incompatible roads.
- Adding random props to hide empty or ugly spaces.
- Declaring victory because navigation tests pass.

A road is finished only when it is both functionally correct and visually convincing.

## 4. HISTORICAL NORTH — PROTECT ITS IDENTITY

The traditional northern district is already the strongest area.

Do not rebuild its approved buildings or ceremonial compound.

Preserve:

- Palace hierarchy and stone courtyards.
- Hanok and academy surroundings.
- Historical entrances and paths.
- Existing forest framing and architectural proportions.

**Rebuild only the southern transition corridor where modern pavement currently intrudes into historic ground.**

Design an elegant historical-to-contemporary threshold using appropriate transitional paving, landscaping, framed entrances and pedestrian hierarchy.

Modern concrete must not suddenly invade the traditional palace streets.

The change in architectural eras should feel gradual and deliberate.

## 5. NAMSAN — COMPLETE LANDSCAPE RECONSTRUCTION

The existing Namsan route network is visually rejected.

Its paths are too rough and its park boundaries too weak.

### Mandatory reconstruction

- Build an elegant winding walking loop around the tower.
- Add properly composed secondary scenic trails.
- Provide a clear primary entrance and tower arrival sequence.
- Use natural curves with consistent widths and professionally finished edges.
- Add appropriate low fences, park railings, retaining walls and planted boundaries.
- Make the observation plaza recognizable and spacious enough to enjoy.
- Introduce balanced flowerbeds, trees, rocks and resting/viewing pockets.
- Preserve sightlines toward the tower.
- Keep the park distinctly separate from the station and modern commercial zone.

The player must feel they are visiting a beautiful Korean hillside park, not crossing a random sand trail.

**Namsan must look like a carefully landscape-designed destination even without NPCs.**

## 6. BUSAN STATION — MAKE THE CENTRAL MODERN DISTRICT A VISUAL HIGHLIGHT

This is the highest-priority modern architecture and streetscape correction.

The current central area feels pale, under-composed and insufficiently organized.

### Required transformation

Create a strong central transit district featuring:

- A visually prominent modern station.
- An attractive, symmetrical or deliberately balanced forecourt.
- Clear entrance steps and plaza thresholds.
- Proper station frontage and modern pedestrian connections.
- Dedicated rail/platform circulation.
- Coordinated contemporary paving.
- Glass, steel, clean concrete and blue architectural accents.
- Modern streetlights, benches, flower planters and directional signs.
- Strong visual framing of the station.
- Distinct commercial frontage and public gathering areas.

Do not randomly move small buildings around the station.

Each commercial building must have a defined plot, entrance, frontage and relationship to the main pedestrian network.

**The station must look like the centerpiece of the modern district, not just another building placed on gray paving.**

## 7. AMUSEMENT PARK — GIVE IT A COMPLETE INDEPENDENT CAMPUS

The Ferris wheel, carousel and amusement structures currently lack a unified site composition.

Rebuild their surroundings into a single recognizable leisure destination.

### Mandatory features

- Clearly recognizable main entrance/gateway.
- Coherent perimeter treatment using attractive low fences, hedges and landscaped edges.
- One organized internal pedestrian loop.
- Separate courts for the Ferris wheel and carousel.
- Distinct access paths and resting pockets.
- Coordinated colorful attraction paving.
- Attractive flowerbeds, lights, banners and queue areas.
- Breathing room between major rides and commercial structures.
- Clear pedestrian exit toward the main modern district.

The site must feel planned, not assembled from unrelated decorative objects.

**At a full-map zoom, the player should immediately recognize where the amusement park begins and ends.**

## 8. MODERN ROADS — REBUILD THE URBAN HIERARCHY

Create a coherent modern street system with three levels:

**Primary pedestrian boulevard**
- Connects the historical transition, transit hub and waterfront.
- Straight or gently aligned where appropriate.
- Consistent widths, clean intersections and coordinated modern materials.

**Secondary destination streets**
- Connect the station, shops, park and amusement facilities.
- Have readable entrances and appropriate curbs/landscaping.

**Local scenic paths**
- Used inside Namsan, Jeju and landscaped attraction areas.
- Natural curves, softer edges and place-specific materials.

Use clearly different textures:

- Historic ground: warm stone, sand and traditional paving.
- Modern civic areas: refined concrete and patterned engineered-stone paving.
- Namsan: natural compacted trail materials and landscaped stone.
- Amusement campus: decorative contemporary paving.
- Coast: promenade surfaces, railings and appropriate boardwalk.
- Jeju: local sand, basalt and natural stone paths.

**Do not solve all environments with the same gray tile.**

Remove awkward stubs, oversized triangular intersections, sudden changes of width, inconsistent road edges and visual seams.

## 9. WATERFRONT, PIER AND FERRY — RECONSTRUCT THE REAL ARRIVAL LOGIC

The existing coastal transportation area still looks unresolved.

Build one understandable boarding composition:

**Modern boulevard → Waterfront promenade → Ferry terminal → Boarding pier → Ferry → Island landing.**

Mandatory:

- Properly structured promenade and coastal railings.
- Clear ferry terminal frontage and waiting area.
- A physically convincing wooden or stone boarding pier.
- Correctly positioned ferry relative to the loading edge.
- Visually distinct dock, lookout deck and pedestrian walkway.
- Appropriate stairs, railings, mooring posts and shoreline transitions.
- No oversized unexplained wooden platform protruding into the sea.
- No overlapping pier images, floating walkway sections or fake boarding spaces.

Retain functional ferry interactions and make them correspond to the visible boarding location.

### Island bridge / crossing

The previous request for a mainland-island bridge must be addressed explicitly.

Provide a convincing short pedestrian bridge, elevated walkway or appropriate designed crossing where compatible with the fictional geography and scale.

If a continuous walkable bridge would conflict with the ferry gameplay or world logic, retain the ferry as the primary travel connection and provide a clearly designed boarding-to-arrival route. Document the rationale instead of silently omitting the bridge requirement.

**Never create a decorative bridge that appears usable but is not actually traversable.**

## 10. JEJU — COMPLETE SCENIC PATH RECONSTRUCTION

The island is visually important and must not have crude rectangular routes.

Rebuild the island pedestrian circulation using:

- Smooth, graceful winding trails.
- A scenic loop around the volcanic hill.
- Clear routes from arrival to the village, pavilion, learning garden and viewpoint.
- Natural basalt or low-stone edging.
- Balanced garden transitions and rest/viewing spaces.
- Gentle curves around existing vegetation and rocky landmarks.
- Coherent arrival and departure access.

Keep the distinctive Jeju atmosphere, village architecture, volcanic rock formations and island vegetation.

The island must look scenic and intentional, not like broad beige polygons pasted onto grass.

## 11. FIX MODERN COLOR AND MATERIAL QUALITY

The modern south should be more vivid and attractive, but not artificially oversaturated.

Use the earlier polished visual direction as the target.

### Mandatory art direction

- Richer coastal blue and turquoise highlights.
- Cleaner blue/white station architecture.
- More refined contemporary stone surfaces.
- More colorful but coordinated amusement attractions.
- Fresh landscaping greens and flower accents.
- Clearer distinction between buildings, plazas and planted areas.
- Warm lighting accents that complement the blue modern infrastructure.

Use coherent local material palettes.

**Do not apply a global saturation, contrast, sharpen or color filter to the whole screenshot.**

The richer appearance must come from actual source materials, environment composition and lighting choices.

Preserve native pixel sharpness.

## 12. USE THE INSTALLED SKILL PIPELINE — PROVE ACTUAL USAGE

The repository already contains valuable pixel-art production workflows.

Read and appropriately use:

- Agent Sprite Forge `generate2dmap`.
- `generate2dsprite` where new original environmental elements are needed.
- `generate2dmedia` for approved asset routes when applicable.
- Existing Tiled-compatible tilemap and atlas tooling.
- Existing environment composition and pixel QA tools.
- Other installed approved skills only when relevant.

Skill documentation alone is not implementation.

Record which commands were actually executed, their outputs and any failures or unavailable capabilities.

Do not fabricate successful skill execution.

Do not use paid generation APIs or install redundant services without permission.

## 13. REQUIRED WORKFLOW — NO MORE ENDLESS CONCEPT PASSES

Execute this sequence:

**PHASE A — AUDIT**
- Identify every rejected road source and layout defect.
- Record baseline screenshots and recovery checkpoint.
- Prepare one actionable reconstruction plan.

**PHASE B — RECONSTRUCT**
- Remove failed road layers.
- Rebuild Namsan and the traditional-modern transition.
- Rebuild Busan Station and the central modern streets.
- Recompose the amusement park campus.
- Rebuild coastal arrival, ferry facilities and island paths.

**PHASE C — INTEGRATE**
- Update actual Phaser scenes, tilemaps, assets, positions, navigation and collision.
- Verify all five destinations are playable.

**PHASE D — VISUAL QUALITY CONTROL**
- Capture actual Phaser renders.
- Inspect them at full-map scale and native gameplay scale.
- Reject visually poor or incomplete results.
- Fix failed areas before packaging.

**PHASE E — FINAL VERIFICATION**
- Run production build, TypeScript, lint, unit tests and browser tests.
- Test desktop and mobile landscape controls.
- Verify entrance accessibility, ferry travel, bridge/crossing behavior, route continuity and interaction points.
- Preserve or measure performance without unsupported FPS claims.

**Do not stop after Phase A or deliver another concept-only preview. Complete the implementation and quality review.**

## 14. REQUIRED VISUAL ACCEPTANCE GATES

Each of the following must independently PASS:

| Area | Acceptance condition |
|---|---|
| Historical north | Approved heritage buildings preserved; no intrusive modern paving |
| Namsan | Elegant winding trails, enclosed landscaped park, recognizable tower arrival |
| Busan station | Premium modern civic plaza and coherent urban organization |
| Amusement park | Clearly bounded campus, attractive internal loop and distinct ride courts |
| Modern paths | Consistent hierarchy, polished junctions, no crude paving patches |
| Waterfront | Logical promenade, terminal and boarding pier |
| Island access | Functional, visually convincing ferry/crossing arrangement |
| Jeju | Scenic curved paths and recognizable destination sequence |
| Color | Modern zone visibly fresher and more vibrant without losing detail |
| Runtime | Actual gameplay routes, collision and interactions functional |

**A passing build is NOT a passing art review.**

If any gate fails, correct it before declaring the production candidate finished.

Never report a gate as passed without supporting visual or functional evidence.

## 15. MANDATORY DELIVERABLES

Create a final review folder containing:

1. `FINAL_WORLD_OVERVIEW_NATIVE.png` — actual full-resolution Phaser world.
2. `FINAL_WORLD_OVERVIEW_WEB.png` — browser-friendly review image.
3. `REFERENCE_VS_FINAL.png` — composition comparison, clearly separating reference artwork from real-engine output.
4. `NAMSAN_BEFORE_AFTER.png`.
5. `BUSAN_STATION_BEFORE_AFTER.png`.
6. `AMUSEMENT_PARK_BEFORE_AFTER.png`.
7. `TRANSITION_ROADS_BEFORE_AFTER.png`.
8. `WATERFRONT_FERRY_BEFORE_AFTER.png`.
9. `JEJU_BEFORE_AFTER.png`.
10. `WORLD_NAVIGATION.png` — actual connected route network with entrances, port and crossing.
11. Real gameplay walkthrough through all districts.
12. Playable review ZIP.
13. `FINAL_WORLD_RECONSTRUCTION_REPORT.md` containing visual gate results, executed skills, testing, performance and recovery instructions.

All before/after comparisons must use equivalent camera locations, scale and render settings.

Screenshots must be from the real game. Do not substitute standalone generated illustrations or concept boards for implementation proof.

## 16. STRICT RELEASE AND PRESERVATION RULES

- Work only on `rebuild/pixel-social-rpg-v3`.
- Preserve Juni, historical architecture, approved landmark identities and source assets.
- Update colliders/navigation honestly where the reconstructed world requires it.
- Create and verify recovery checkpoints.
- Do not force-push or rewrite Git history.
- Do not merge into `main`.
- Do not publish GitHub Pages or the unfinished game.
- Do not touch the separate Korean Arena main learning application.
- Do not introduce paid dependencies or unauthorized services.
- Update project task/progress/decision/asset documentation.

Commit and push verified work to GitHub.

## 17. FINAL DIRECTIVE

**Stop patching the broken environment. Reconstruct the defective systems properly.**

The required result must have:

- A beautiful historical Korean north.
- A scenic, elegantly enclosed Namsan park.
- A vivid, organized modern Busan transit district.
- A recognizable, coherent amusement-park campus.
- Attractive modern roads and public spaces.
- A properly designed coastal promenade and ferry terminal.
- Clear, functional island access.
- A scenic Jeju environment with graceful natural paths.
- Strong architectural and material contrast between historical and modern Korea.
- Crisp, original pixel art throughout.

At first glance, the final full-map overview must feel professionally composed.

**DO NOT declare victory merely because 12 unit tests, 56 browser tests or GitHub CI are green.**

**DO NOT submit another version that only changes ground colors, road masks, thin borders or decorative props while leaving the rejected composition intact.**

Complete the actual reconstruction, inspect the real game, correct your failed visual gates and deliver one fully documented production candidate.

**STOP only for a genuine permission/capability blocker or after delivery for the user's final visual approval.**

START EXECUTION NOW.
