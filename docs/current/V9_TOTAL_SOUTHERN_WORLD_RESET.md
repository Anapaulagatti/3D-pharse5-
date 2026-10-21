# KOREAN ARENA — V9 TOTAL SOUTHERN WORLD RESET
## Delete the Failed Southern Maps. Design a Completely New Korean Pixel City.

**Repository:** `Anapaulagatti/3D-pharse5-`
**Working branch:** `rebuild/pixel-social-rpg-v3`

**Role:** Lead Game World Architect, Senior Level Designer, Korean Urban Planner, Environmental Pixel Art Director, and Phaser Engineer.

## 0. FINAL DECISION — THE ENTIRE SOUTHERN MAP IS REJECTED

The current southern map is NOT approved.

V6, V7, V8 and previous revisions have repeatedly failed to produce the required environment quality.

The central problem is not a few bad paths or missing decorations.

**The entire southern environment's spatial planning, road network, district arrangement, urban composition, landscaping, and public-space design are fundamentally unsatisfactory.**

Therefore:

**DELETE THE FAILED SOUTHERN MAP IMPLEMENTATIONS AND REBUILD THE SOUTHERN WORLD FROM A CLEAN DESIGN BASELINE.**

Do not patch the existing southern environment.

Do not recolor its roads.

Do not preserve its existing district footprints.

Do not reuse its object coordinates as a planning reference.

Do not rebuild the same map with slightly rearranged buildings.

**The old southern layout must cease to be the foundation of development.**

The final result must be a genuinely NEW playable Korean pixel city.

---

## 1. SAFETY FIRST — ARCHIVE BEFORE DELETING

Before making destructive changes:

1. Inspect the latest GitHub branch and working tree.
2. Commit and push any recoverable active work.
3. Create and verify a recovery tag preserving the complete current game.
4. Preserve the approved northern historical district, Juni, original character assets and reusable source artwork.
5. Identify all old southern-map implementations, generated assets, reports, videos and review packages.
6. Build a dependency inventory distinguishing approved northern content, shared engine resources and rejected southern content.

After the recovery tag is verified:

- Remove obsolete V6/V7/V8 and earlier superseded southern-map implementations from the ACTIVE project tree.
- Remove unused generated terrain, road masks, obsolete district configurations and their abandoned runtime references.
- Remove redundant historical screenshots, ZIPs and reports from the active branch when safely recoverable from Git tags.
- Retain only necessary current project documentation, reusable original art sources, licensing information and new V9 review outputs.
- Update `.gitignore` to prevent generated review clutter.

**Deleting obsolete active files is explicitly authorized.**

Do not rewrite Git history, force-push, or delete recovery tags.

Do not accidentally remove working shared Phaser systems or the approved northern district.

Create `SOUTHERN_RESET_CLEANUP.md` listing deleted files, preserved assets, removed dependencies and exact restoration commands.

---

## 2. PROTECT THE NORTHERN HISTORICAL DISTRICT

The northern Korean historical district is approved.

It includes:

- Palace and royal compound.
- Hanok architecture.
- Historical gates and courtyards.
- Academy and cultural buildings.
- Traditional landscape and paths.
- Historical architecture and related assets.

**Do not rebuild or rearrange this area.**

Preserve its native art and geometry.

Create a fixed northern boundary and protect its asset and layout data with reproducible checks.

Only the southern-facing transition gateway may receive minimal integration changes if necessary.

Also preserve:

- Juni's appearance and approved animations.
- Existing controls and mobile landscape UI.
- Shared dialogue, learning and interaction systems.
- Reusable technical tooling.
- Original artwork source files that are valuable independently of the rejected southern layout.

---

## 3. STUDY PIXELS.XYZ BEFORE DESIGNING ANYTHING

Research the level-design and navigation principles demonstrated by:

https://www.pixels.xyz/

https://play.pixels.xyz/

https://pixels.fandom.com/wiki/Map:Terravilla

https://playpixels.vip/terravilla-map/

Analyze the real available map and gameplay references.

Focus specifically on:

- Clear central gathering hubs.
- Recognizable districts and destinations.
- Readable roads and paths.
- Logical building clusters.
- Efficient travel between activities.
- Human-scale exploration.
- Strong environmental readability.
- Meaningful public spaces.
- Social interaction opportunities.
- Clear connections between landmarks and gameplay.
- A sense of entering and exploring a living world rather than viewing a decorated poster.

Document the principles learned in `PIXELS_WORLD_DESIGN_STUDY.md`, distinguishing verified references from your own design interpretations.

**Do NOT copy Pixels.xyz artwork, layouts, tilesets or branding.**

Pixels provides game-world organization principles.

The architectural and urban identity must come from original contemporary Korean city design.

Korean Arena is a Vietnamese-first Korean-language learning RPG, not a farming clone or a Web3/NFT economy.

---

## 4. RESET THE ENTIRE SOUTHERN LANDSCAPE

Create a completely new southern-map planning file.

The design must start without importing any of the rejected southern:

- Road geometry.
- Path masks.
- Plot boundaries.
- Building coordinates.
- Decorative placement data.
- District footprints.
- Failed terrain composition.
- Existing hardscape layout.

Set up a new editable world-coordinate system for the southern district.

Use a clean terrain base for production.

Existing landmark illustrations may be retained in a reusable asset library, but **their previous locations and site plans must not be inherited**.

Choose placement only after the new city plan is complete.

Do not use the previous full-map screenshot as a geometric template.

---

## 5. DESIGN A REAL CONTEMPORARY KOREAN CITY

The new southern district must feel like a believable, attractive miniature urban environment inspired by modern Korea.

It must NOT look like isolated attractions arranged on green grass.

### Required urban elements

Build a coherent network of:

- Main boulevards and pedestrian streets.
- Smaller local streets and alleys.
- Defined city blocks and property plots.
- Commercial frontages.
- Public squares and plazas.
- Parks and landscaped courtyards.
- Street-facing building entrances.
- Realistic station and transport facilities.
- Pedestrian crossings and appropriate sidewalks.
- Streetlights, benches, planters and wayfinding.
- Accessible waterfront promenades.
- Clearly separated scenic and entertainment destinations.

### Fundamental planning principles

**Roads first. City blocks second. Buildings third. Landscaping fourth.**

Every road needs a purpose.

Every building needs a plot and entrance.

Every plaza needs a function.

Every district needs a clear identity.

Every boundary needs architectural logic.

Every decorative object needs a meaningful reason to exist.

Avoid both excessive crowding and oversized empty lawns.

---

## 6. BUILD FIVE DISTINCT SOUTHERN DESTINATIONS

The rebuilt southern world must contain five integrated yet recognizable destinations.

### A. MODERN KOREAN CIVIC AND COMMERCIAL CENTER

This is the new urban heart.

Create:

- A distinctive central gathering square.
- Modern commercial buildings.
- Shops, cafés and public services.
- Organized pedestrian streets.
- Contemporary building frontages.
- Clean sidewalks, curbs and intersections.
- Attractive tree-lined walkways.
- Public seating and gathering spaces.
- NPC-ready social and educational interaction points.

**The civic center should feel like a living Korean neighborhood, not a featureless tiled plaza.**

### B. NAMSAN SCENIC PARK

Design an independent, premium-quality landscape park.

- Iconic tower as the main focal point.
- Graceful winding trails.
- A complete scenic walking loop.
- Naturally integrated viewing platforms.
- Proper low fences and park boundaries.
- Rock gardens and planted slopes.
- Rest areas and attractive viewpoints.
- A clear main entrance connected to the city.
- Purposeful secondary paths.

No crude beige loops, awkward angular paths or random boulders.

**The park must feel landscaped by a professional designer.**

### C. CONTEMPORARY KOREAN TRANSIT DISTRICT

Create a believable modern train station and transit zone.

- Clearly recognizable station building.
- Attractive forecourt.
- Organized rail alignment.
- Proper train platform and access.
- Modern transit shelter.
- Blue, white, steel and glass architectural accents.
- Walkable connections to shops and the civic center.
- Safe railway crossings.
- Clean modern surface materials.
- Appropriate transport signage.

The transit district must feel integrated into the city, not like a train sitting between random buildings.

### D. ENTERTAINMENT AND CULTURAL LEISURE PARK

Build a self-contained modern attraction district.

- Distinctive entrance gateway.
- Clearly defined property boundary.
- Properly composed internal pedestrian loop.
- Ferris wheel plaza.
- Carousel plaza.
- Entertainment pavilion.
- Visitor information area.
- Landscaped recreational spaces.
- Decorative lighting and vibrant paving.
- Appropriate benches, planters and queue areas.

Attractions should be arranged around the circulation system.

**Do not place rides first and draw walkways around them afterward.**

### E. COASTAL DISTRICT AND JEJU TRAVEL CONNECTION

Design a contemporary coastal destination with:

- Continuous waterfront promenade.
- A proper ferry terminal.
- Structured boarding areas.
- Attractive coastal cafés and lookout points.
- Safe railing and shoreline treatment.
- Clear connections to the modern city.
- A functional ferry route to the island.

The ferry must appear physically connected to the boarding infrastructure.

Avoid oversized artificial wooden surfaces, overlapping piers, disconnected stairs and ambiguous entrances.

The island must be a deliberate travel destination rather than a random piece of land beneath the map.

---

## 7. COMPLETELY REDESIGN JEJU'S LANDSCAPE

Treat Jeju as a new environment-design project.

Preserve useful original character/landmark artwork only when it fits the new design.

Create:

- A clear arrival harbor.
- An attractive volcanic landscape.
- A natural scenic trail network.
- An oreum-inspired hill and viewpoint.
- Jeju basalt stone walls.
- Tangerine gardens.
- A distinctive village/cultural area.
- Meaningful destination entrances.
- A complete exploration loop with optional scenic branches.

Natural paths should follow terrain contours.

Their curves must be intentional and smooth in native pixel-art geometry.

Avoid rigid rectangular sand roads, angular dead ends, floating structures or arbitrary dark ground patches.

Ferry access must remain understandable and playable.

Do not invent a long mainland-island bridge merely because earlier drafts mentioned one. Choose a geographically and mechanically coherent connection, prioritizing a polished ferry system for this fictional Korean travel world.

---

## 8. CREATE A NEW PREMIUM ENVIRONMENT ART STYLE

The previous modern district has weak material definition and flat composition.

Rebuild the southern materials as an original coordinated pixel-art set.

### Modern city materials

- Clean contemporary stone and concrete.
- Patterned pedestrian paving.
- Asphalt only where real streets require it.
- Defined curbs and sidewalks.
- Glass, steel and aluminum details.
- Modern lighting and street furniture.
- Contemporary signage.
- Coordinated planter and landscape systems.

### Scenic materials

- Natural stone trails.
- Grass, shrubs and planted borders.
- Distinctive Namsan hillside terrain.
- Coastal stone and timber where appropriate.
- Jeju basalt, volcanic soil and natural sand.

### Color direction

The modern south must be visibly:

- Fresher.
- Brighter.
- More vivid.
- More varied.
- More visually appealing.

Use a cohesive modern Korean city palette: contemporary cool stone, sophisticated blue/white details, fresh green landscaping, selective warm lighting and distinctive amusement color accents.

**Do not increase saturation globally or apply image filters.**

Generate or edit the source textures and materials themselves.

Preserve consistent pixel scale and crisp native rendering.

---

## 9. BUILD A PLAYER-FIRST EXPLORATION ROUTE

The new city must be designed for gameplay, not only for an attractive overview.

Plan the player's journey:

**Historical Gateway → Modern Civic Center → Shops & Station → Namsan Park / Entertainment Park → Waterfront → Jeju Ferry Destination.**

Implement a recognizable main route and useful secondary loops.

Design to avoid:

- Excessive walking through empty terrain.
- Dead ends without destinations.
- Hidden building entrances.
- Obstacles across important walkways.
- Confusing transport transitions.
- Unnecessary long detours between learning activities.

Every major destination should support future:

- Korean vocabulary discovery.
- NPC conversation.
- Cultural quests.
- Social meeting spots.
- Interactive learning minigames.
- Exploration rewards.

Do not implement unrelated major gameplay systems now. Reserve their locations and interaction anchors.

---

## 10. USE THE INSTALLED PRODUCTION SKILLS

Before production, inspect:

- `AGENTS.md`.
- `docs/ART_SKILL_REGISTRY.md`.
- Existing successful Gwanghwamun and Juni skill records.
- Existing map/export and Phaser QA scripts.

Use applicable skills from:

https://github.com/0x0funky/agent-sprite-forge

Especially the verified 2D map generation, compositing, tilemap, original environment asset and pixel QA workflows.

Use additional installed skills only when appropriate.

Record actual tool executions, outputs, warnings and limitations.

Do not claim a tool was used merely because its documentation was read.

No unauthorized paid APIs.

---

## 11. MANDATORY PRODUCTION PIPELINE

### STAGE A — REMOVE THE REJECTED SOUTHERN WORLD

Archive and remove superseded southern-map implementations from the active branch.

Verify the approved north and shared systems remain intact.

### STAGE B — NEW URBAN MASTERPLAN

Create a NEW southern plan with:

- Road hierarchy.
- City blocks.
- Property plots.
- District boundaries.
- Building footprints.
- Main pedestrian routes.
- Station circulation.
- Park entrances.
- Coastal infrastructure.
- Travel connections.

**No final artwork is allowed before the plan is spatially validated.**

### STAGE C — PLAYABLE GRAYBOX

Implement the new city using temporary simple geometry.

Verify:

- Player movement.
- Route continuity.
- Entrances.
- Spatial proportions.
- District connectivity.
- Camera behavior.
- Ferry access.

### STAGE D — HIGH-QUALITY PIXEL PRODUCTION

Use the verified skill pipeline to produce final original roads, environments, landscaping, transport surroundings and district boundaries.

Only now position approved reusable building assets where they suit the new plots.

### STAGE E — GAMEPLAY AND VISUAL QA

Integrate into the actual Phaser project.

Update all relevant collision, tilemap and navigation data.

Test desktop, mobile landscape, interactions, ferry transportation and performance.

Inspect actual Phaser screenshots.

Fix visual defects before packaging.

### STAGE F — FINAL GITHUB DELIVERY

Commit and push the verified new southern world.

Do not merge into `main` or deploy the unfinished game.

---

## 12. STRICT VISUAL QUALITY GATES

The reconstruction is NOT complete unless:

1. The new southern layout is clearly different from previous rejected versions.
2. It resembles a coherent miniature Korean city.
3. Major roads connect logical destinations.
4. Buildings face proper streets and occupy sensible plots.
5. The central district looks like a genuine modern town.
6. Namsan is a scenic, enclosed and beautifully landscaped park.
7. The station has an attractive modern forecourt.
8. The amusement park has a recognizable entrance and complete internal organization.
9. The coastal district has a believable promenade and ferry terminal.
10. Jeju has coherent scenic paths and a meaningful arrival.
11. The historical north remains protected.
12. Native pixel-art quality is preserved.
13. Player navigation and existing gameplay systems still function.

**Automated tests are mandatory but do not constitute visual approval.**

Do not declare success while any major visual gate is obviously failing.

---

## 13. REQUIRED DELIVERABLES

Create a NEW V9 review package:

- `V9_NEW_CITY_MASTERPLAN.png` — completely new urban zoning and route plan.
- `V9_FULL_WORLD_OVERVIEW.png` — actual Phaser world.
- `V9_WEB_OVERVIEW.png` — browser-friendly whole-world image.
- `V8_V9_REAL_DIFFERENCE.png` — true before/after demonstrating full southern reconstruction.
- `V9_CITY_STREETS.png` — main streets, plots and urban materials.
- `V9_NAMSAN.png` — park circulation and landscape.
- `V9_STATION.png` — transit masterplan and architecture.
- `V9_ENTERTAINMENT.png` — coherent amusement-campus layout.
- `V9_WATERFRONT.png` — coastal promenade and ferry.
- `V9_JEJU.png` — island landscape and routes.
- `V9_NAVIGATION.png` — verified player routes and destination connections.
- Real multi-district Phaser gameplay video.
- Playable review ZIP.
- `V9_CITY_REBUILD_REPORT.md` — deletion audit, new map layout, actual skill execution, tests, changed assets and recovery SHA.

Use actual-engine captures, not generated mockups presented as gameplay.

Provide links to the new GitHub files.

Stop for my visual approval before marking the map final.

---

## 14. NON-NEGOTIABLE RULES

DO NOT:

- Reuse the rejected southern geometry.
- Patch the old southern paths.
- Keep obsolete district arrangements.
- Preserve bad object coordinates for convenience.
- Use the previous map as a tracing template.
- Scatter buildings and connect them afterward.
- Create another generic gray concrete grid.
- Hide poor layouts with decorations.
- Rebuild the approved historical north.
- Damage Juni or existing gameplay.
- Rewrite Git history or delete recovery references.
- Touch the separate Korean Arena learning application.
- Merge into `main` or publish the unfinished game.
- Copy Pixels.xyz artwork or protected maps.

DO:

- Remove rejected southern implementations from the active project.
- Start with a genuinely blank southern layout.
- Study real Pixels.xyz exploration design.
- Apply Korean urban planning logic.
- Build streets and plots BEFORE placing buildings.
- Create a cohesive, vivid and navigable Korean miniature city.
- Preserve recoverable checkpoints.
- Produce working Phaser implementation and honest visual comparisons.

## FINAL ORDER

**FORGET THE OLD SOUTHERN MAP.**

**DELETE THE REJECTED IMPLEMENTATION.**

**START THE NEW SOUTHERN CITY FROM A BLANK DESIGN CANVAS.**

The northern historical district is protected, but everything south of the approved transition boundary must be reconsidered from first principles.

The result must be a genuine new Korean pixel city, not V8 with a different pavement texture.

**Do not stop at a planning document. Complete the playable rebuild, perform the full visual and technical QA, and deliver one fundamentally new candidate.**

START NOW.
