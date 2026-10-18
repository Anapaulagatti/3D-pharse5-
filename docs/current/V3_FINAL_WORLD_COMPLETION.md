# KOREAN ARENA — V3 FINAL WORLD COMPLETION
## Final Environment Art, Modern Korea Redesign & World Quality Lock

**Role:** Principal Game World Art Director, Korean Architectural Designer, Level Designer, Pixel Artist and Phaser Performance Engineer.

**Repository:** `Anapaulagatti/3D-pharse5-`  
**Development branch:** `rebuild/pixel-social-rpg-v3`

## THE FINAL MISSION

We have spent too long iterating on the map.

The existing 4352×4800 playable world, approved zoning, Juni character and art pipeline are our production foundation.

**This is the FINAL major environment-design pass.**

Finish the existing world into one beautiful, coherent, exploration-ready Korean pixel RPG environment, with an unmistakable visual distinction between historical Korea and contemporary Korea.

Do not restart the game, propose endless alternatives, or stop after producing concepts. Implement, integrate, test, document and deliver the completed playable world.

## 1. MANDATORY EXISTING WORKFLOW

Before modifying anything, read:

- `AGENTS.md`
- `docs/ART_SKILL_REGISTRY.md`
- `docs/full-world/REVIEW.md`
- `docs/full-world/LAYOUT.md`
- `docs/full-world/world-plan.json`
- Approved urban-zoning documents.
- Previous Agent Sprite Forge production records.
- The latest `STUDIO_*` checkpoints.

Use the proven `0x0funky/agent-sprite-forge` pipelines, particularly `generate2dmap` and `generate2dsprite`, for original assets, tilesets, prop extraction, layered composition, Tiled exports, navigation and pixel QA.

Preserve the approved 144-frame Juni animations.

No paid APIs without authorization. Do not reinstall working tools unnecessarily.

Create a verified Git recovery checkpoint before major changes.

## 2. FIRST: CORRECT THE CURRENT MAP'S STRUCTURAL DEFECTS

Use the user's latest blue/red annotated overview as a defect reference.

### Red-marked cramped building

The small commercial building in the lower-right part of the historical district is awkwardly crowded against nearby architecture.

- Relocate or reorganize that micro-block.
- Provide appropriate frontage, access, landscaping and visual separation.
- Prevent roof collisions, overlapping facades and blocked circulation.
- Preserve useful existing architecture.

### Blue-marked forest and terrain boundaries

The large forest strips and map-section edges look like rectangular blocks pasted onto grass.

**This is unacceptable in the final world.**

Replace visible artificial borders with proper terrain composition:

- Irregular, organically shaped forest boundaries.
- Layered undergrowth, rocks, trees, shrubs and groundcover.
- Seamless grass/soil/stone transitions.
- Natural paths entering and leaving vegetation.
- Believable differences in terrain elevation.
- Proper shoreline, retaining-wall and promenade transitions.
- No exposed rectangular map-chunk boundaries or abrupt checkerboard changes.

Use correctly joined terrain tiles or masks and verify the actual composed Phaser result.

Do not hide bad seams by simply covering them with oversized trees.

### Empty X-marked terrain

Remove purposeless empty terrain surrounding the lower districts.

Use one of two justified approaches:

1. Design meaningful scenery and routes where players should explore.
2. Convert inaccessible unused terrain into natural world boundaries and appropriate camera limits.

Do not turn empty grass into equally empty decorative forests.

## 3. HISTORICAL KOREA — PRESERVE AND FINISH

Keep the approved northern historical area largely intact.

Its identity should remain:

- Royal Korean palace architecture.
- Gwanghwamun-inspired gate and enclosed compound.
- Sejong Academy and scholarly courtyards.
- Jang Yeong-sil's invention workshop.
- Yi Sun-sin's historical museum.
- Hanok cultural streets, bookshops and traditional details.

Perform only targeted corrections to roads, walls, entrances, collision, awkward spacing and missing architectural details.

Do not regenerate successful buildings unnecessarily.

## 4. MODERN KOREA MUST LOOK GENUINELY MODERN

**Highest visual priority.**

The southern world currently looks too similar to the historical north in materials, landscaping and spatial organization.

Fix this decisively.

### Historical material language

- Timber and giwa roofs.
- Traditional stone foundations.
- Hanji-style windows.
- Courtyard walls and ceremonial gates.
- Natural stone and historic paving.
- Traditional lanterns and signs.
- Asymmetric gardens and organic planting.

### Contemporary material language

- Glass curtain walls and large modern windows.
- Steel and aluminum structural elements.
- Contemporary concrete and engineered stone.
- Clean geometric architecture.
- Asphalt, modern sidewalks and patterned urban paving.
- Metal railings, transit platforms and elevated walkways.
- Contemporary streetlights and illuminated signage.
- Modern landscaping, urban furniture and transport infrastructure.

**Modern Korea must NOT look like hanok buildings with new paint.**

The distinction must be visible through architecture, silhouettes, geometry, materials, streets, public spaces and lighting — not merely a different color palette.

Maintain consistent pixel density, top-down/light-3/4 perspective, character scale and lighting across all areas.

Avoid excessive diagonal/isometric building skew.

## 5. COMPLETE FOUR DISTINCT MODERN/TRAVEL DESTINATIONS

### A — NAMSAN / N SEOUL TOWER

Transform the existing tower zone into a recognizable modern observation destination.

- Clearly identifiable observation tower silhouette.
- Contemporary observation building with steel/glass elements.
- Proper elevated viewing terrace.
- Mountain forest approaches and scenic paths.
- Modern guardrails, information signs and lighting.
- Clear contrast between natural hillside and man-made structure.

The tower must feel like a major destination, not an ordinary pavilion with a tower on top.

### B — BORA BLOOM / ENTERTAINMENT PARK

Build a genuinely lively modern amusement area inspired by Korean theme-park culture.

- Distinctive modern entrance and ticket plaza.
- Recognizable Ferris wheel and carousel.
- Additional original entertainment architecture or scenic attraction.
- Colorful but coordinated amusement-park paving.
- Modern lighting, railings, flowerbeds and queue areas.
- Connected paths between attractions.
- Attractive rest and social gathering spaces.

Make it feel like an actual planned amusement park rather than three unrelated rides on grass.

Use original fictional branding and artwork.

### C — BLUE LETTER COAST / BUSAN

Build a visually distinctive contemporary coastal transport destination inspired by Haeundae Blue Line Park.

- Recognizable scenic train and proper station.
- Railway tracks with logical continuity.
- Modern station facade and platform.
- Coastal promenade, viewing decks and boardwalk.
- Seawalls, railings, beach transitions and natural shoreline.
- Contemporary cafés, tourism signage and rest areas.
- Functional bridges and clearly separated tracks/walkways.

The coast must read as a real seaside destination, not a railway placed beside a rectangular blue water texture.

### D — WINDSTONE / JEJU

**Completely upgrade the island's destination identity.**

The current island is too empty and visually unmemorable.

Make Jeju worth taking the ferry to visit:

- A distinctive oreum-inspired volcanic hill.
- Recognizable basalt formations and stone walls.
- Dol hareubang-inspired guardian sculptures.
- Tangerine orchard and unique Jeju vegetation.
- Traditional Jeju-inspired village or cultural courtyard.
- Coastal lookout with dramatic cliffs or sea views.
- A memorable pavilion, garden or nature-learning destination.
- At least one original lightweight interactive cultural discovery.

Build a proper ferry arrival, clear exploration loop and visually satisfying focal point.

Do not simply scatter more trees onto the existing island.

Jeju is a separate travel destination connected by ferry, not an island physically next to real Seoul.

## 6. UNIFY THE WORLD THROUGH A BELIEVABLE EXPLORATION JOURNEY

The full map must have a clear visual and navigational progression:

**Royal Heritage → Cultural Town → Contemporary Urban Gateway → Namsan / Leisure / Busan Coast → Jeju Ferry Destination**

Design a coherent connective network:

- One recognizable main exploration route.
- Useful secondary routes and shortcuts.
- Smooth changes in paving materials.
- Landmarks that help orientation.
- Attractive streets and travel hubs.
- Appropriate signs, lighting, benches and vegetation.
- Clear travel transitions to geographically distant destinations.

Do not connect unrelated destinations by enormous empty roads.

Make modern districts feel connected through urban infrastructure, while preserving distinctive local environments.

The world is a fictional educational miniature of Korea, not a geographically accurate real-world map.

## 7. FINAL ART AND LAYOUT QUALITY GATES

Before accepting any area, inspect its actual Phaser render at native gameplay scale.

Reject or repair:

- Repeated or nearly identical buildings.
- Excessively large empty lawns or plazas.
- Broken wall/fence connections.
- Artificial rectangular terrain seams.
- Random prop placement.
- Abrupt transitions between scene chunks.
- Roofs intersecting neighboring buildings.
- Inaccessible doors or blocked pathways.
- Incorrectly scaled stairs, roads or platforms.
- Fake modern buildings that still look historical.
- Featureless water or generic Jeju scenery.
- Poorly composed areas visible in the full overview.

Every landmark must have a distinctive silhouette, architectural materials, entrance, surrounding landscape and gameplay purpose.

**The entire world should look intentionally art-directed, not procedurally assembled.**

## 8. COMPLETE THE MAP — DO NOT START ANOTHER CONCEPT CYCLE

Work in this order:

**Pass 1 — Structural Layout Fixes**
Repair all annotated defects, crowded buildings, terrain seams, map boundaries and disconnected routes.

**Pass 2 — Historical/Modern Material Separation**
Finalize contrasting architecture, roads, surfaces, lights and prop palettes.

**Pass 3 — Four Destination Production**
Complete Namsan, Bora Bloom, Busan Coast and Jeju with distinct near-final art.

**Pass 4 — World Integration**
Connect all areas, refine visual transitions, validate travel times and remove leftover placeholders.

**Pass 5 — Final Performance and Visual QA**
Review the entire world, repair blocking defects and generate the final review package.

Do not pause for another proposal or concept selection between passes unless a genuine blocker requires user authorization.

## 9. PERFORMANCE AND MOBILE

Preserve the approved landscape mobile experience and MOBA-style exploration controls:

- Bottom-left analog joystick.
- Bottom-right contextual interaction controls.
- Compact top HUD and minimap.
- Safe-area support and portrait rotate prompt.
- Reliable multitouch and responsive interaction.

Maintain Juni's real directional animation, movement and camera behavior.

Profile performance instead of guessing.

Use asset culling, logical chunk management and efficient rendering where needed.

Measure actual Phaser FPS separately from video FPS.

Never fake performance through duplicated/interpolated recording frames.

Verify desktop Canvas/WebGL where available and emulated landscape mobile; clearly disclose untested physical devices.

## 10. FINAL DELIVERABLES — MANDATORY

Create a clearly organized final review package containing:

1. **FINAL_FULL_WORLD_OVERVIEW.png** — the entire playable world, captured from actual Phaser.
2. **TRADITIONAL_VS_MODERN.png** — side-by-side native-scale comparison demonstrating clearly different architectural materials and environments.
3. **BEFORE_AFTER_MAP_FIXES.png** — annotated repairs for the red/blue-marked defects.
4. **DISTRICT_IDENTITY_BOARD.png** — all five destinations, each with a distinct visual identity.
5. **WORLD_JOURNEY_MAP.png** — actual routes, ferry connections, landmarks and travel flow.
6. **JEJU_BEFORE_AFTER.png** — proof that the island is now a meaningful destination.
7. A real full-world exploration gameplay video.
8. A real mobile landscape gameplay video.
9. A playable review ZIP.
10. A concise `FINAL_MAP_REPORT.md` covering design decisions, remaining limitations, tests, actual tool usage and checkpoint SHA.

**The full-map overview must be easy to inspect.**

Export both a high-resolution PNG and a smaller review PNG suitable for GitHub/browser preview. Use clear labels and provide direct GitHub file links.

Do not substitute concept art or stitched mockups for actual-engine evidence.

## 11. FINAL VERIFICATION

Run:

- TypeScript, lint and production build.
- Unit and Playwright browser tests.
- Clean-clone verification.
- All-district navigation and travel checks.
- Wall, fence, entrance and collision checks.
- Terrain seam and material-transition inspection.
- Mobile joystick, multitouch and UI checks.
- Character animation and camera checks.
- Asset-loading and runtime-error checks.
- Actual performance measurements.

Preserve all approved source artwork, Juni, historical recovery tags and verified development checkpoints.

Update `AGENTS.md`, `docs/ART_SKILL_REGISTRY.md` where necessary, and the four `STUDIO_*` files.

Commit and push verified work to `rebuild/pixel-social-rpg-v3`.

Do not merge into `main`, force-push, publish GitHub Pages, use unauthorized paid APIs or modify the separate Korean Arena learning application.

## 12. FINAL ACCEPTANCE STANDARD

The task is complete only when:

- The northern historical district looks coherent and polished.
- The southern districts look unmistakably contemporary and visually distinct.
- The entire map has no obvious artificial rectangular terrain seams.
- The red-marked building problem is fixed.
- The large blue-marked boundaries are resolved.
- Namsan, the amusement park, Busan Coast and Jeju each feel like unique destinations.
- Roads, railways, ferries, fences and landmarks follow believable spatial logic.
- The player can explore without long stretches of meaningless terrain.
- All five areas work in the actual Phaser game.
- Mobile landscape controls remain functional.
- The full-map overview demonstrates a strong traditional-to-modern progression at first glance.

**Do not mark the map FINAL simply because automated tests pass. Visual quality is an independent acceptance requirement.**

Deliver the finished candidate and STOP for the user's final map approval.

After approval, FREEZE WORLD ART and move development to NPCs, Korean-learning quests, interactions and gameplay — not another major map redesign.

**START THE FINAL PRODUCTION PASS NOW.**