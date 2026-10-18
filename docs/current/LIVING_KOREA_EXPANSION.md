# KOREAN ARENA — LIVING KOREA WORLD EXPANSION
## Fix Architecture, Expand Modern Landmarks & Create a Seamless Korean Exploration World

**Role:** Lead World Designer, Korean Architecture Art Director, Pixel Artist, Urban Planner, and Phaser Engineer.

**Repository:** `Anapaulagatti/3D-pharse5-`
**Working branch:** `rebuild/pixel-social-rpg-v3`

## MISSION

The current Korean pixel world is visually promising, but several architectural placement issues remain.

Refine the existing northern historical district and develop the southern area into a vibrant, contrasting Korean travel and modern-culture district.

**The final world must feel like a connected miniature journey through Korea, not a random collection of landmarks.**

Preserve Juni's approved animations, working gameplay, existing high-quality artwork, and recoverable Git checkpoints.

## 1. FIX THE EXISTING NORTHERN DISTRICT

Use the user's annotated full-map screenshot as a visual defect reference.

The blue-circled areas contain visible wall, fence, and placement problems.

Fix all of them:

- Disconnected palace wall segments.
- Incorrect wall-to-gate connections.
- Overlapping fence sprites and roof edges.
- Broken wall corners and awkward intersections.
- Fences that fail to define coherent property boundaries.
- Decorative boundaries that appear to float or terminate without purpose.
- Academy compound walls that overlap other objects.
- Workshop fences that look unfinished or disconnected.

Every boundary must have a clear architectural purpose.

**Rules:**

- Palace walls must form a coherent enclosure with valid gateways.
- Hanok compounds should have appropriate low walls, courtyards, and entrances.
- Workshops may use open timber fences and service gates.
- Commercial buildings should not be unnecessarily surrounded by walls.
- No overlapping tiles, duplicate posts, blocked entrances, or exposed unfinished wall ends.

Also improve the spacing between the two crowded buildings in the lower-right area of the existing northern district.

Give them proper frontage, pedestrian access, visual separation, and purposeful landscaping.

Do not unnecessarily redesign the approved northern architecture.

## 2. DEVELOP THE SOUTHERN WORLD — TRADITIONAL TO MODERN KOREA

The northern district represents Korea's historical heritage.

The southern district should introduce visually distinct destinations inspired by modern Korea, tourism, nature, and entertainment.

Create four recognizable thematic destinations:

### A. N Seoul Tower / Namsan

- Iconic tower silhouette.
- Elevated park atmosphere.
- Viewing platform and scenic overlooks.
- Hillside paths, greenery, and observation areas.
- A distinctive destination for exploration and social interaction.

### B. Everland-Inspired Entertainment Park

- Colorful amusement park entrance.
- Original rides, attractions, and playful decorations.
- Cheerful landscaping and welcoming pedestrian routes.
- Strong contrast with the quiet historical district.

Create an original fictional amusement-park identity rather than copying Everland's protected branding or artwork.

### C. Haeundae Blue Line Park-Inspired Coastal Area

- Scenic coastal railway and small train station.
- Recognizable seaside sightseeing train.
- Coastal walkway, beach, and water scenery.
- Viewing platforms, bridges, and seaside seating.
- A lively tourism atmosphere inspired by Busan.

Rail lines, platforms, bridges, and coastlines must connect logically.

### D. Jeju-Inspired Nature District

- Volcanic stone features.
- Distinctive Jeju landscape and vegetation.
- Coastal paths, stone walls, gardens, and scenic viewpoints.
- Jeju-inspired cultural details such as dol hareubang sculptures.
- A peaceful natural atmosphere different from the urban districts.

**Important geographical rule:** Namsan, Yongin, Busan, and Jeju are real locations far apart. Korean Arena is a fictional, condensed educational travel world, not a geographically accurate neighborhood of Seoul.

Present these areas as connected themed destinations with clear wayfinding, transport transitions, or travel gateways. Do not falsely imply that all landmarks physically exist in one real Korean district.

## 3. CREATE A VISUAL GRADIENT THROUGH KOREAN ERAS

The player should feel a natural progression:

**Royal Palace → Hanok Neighborhood → Cultural Street → Modern City → Tourism & Nature Destinations**

Express this transition through:

- Road materials and street layouts.
- Traditional stone paths gradually transitioning into modern paving.
- Architecture, storefronts, lighting, and street furniture.
- Historical lanterns evolving into contemporary streetlights.
- Changing vegetation, signage, public spaces, and environmental details.
- Distinct music/ambient zones where existing systems support them.

Avoid abrupt visual changes where a futuristic building appears directly beside a royal palace without an architectural transition.

Preserve consistent native pixel density, lighting, character scale, and camera perspective.

## 4. EVERY LANDMARK MUST HAVE A UNIQUE IDENTITY

Every destination must be recognizable without reading its name.

For each major landmark, provide:

1. A distinctive silhouette.
2. Unique architectural geometry.
3. Appropriate materials and color palette.
4. A meaningful entrance or arrival sequence.
5. Original surrounding props and vegetation.
6. A recognizable cultural or geographic identity.
7. One memorable exploration or educational interaction point.

Do not reuse the same hanok building with only different colors.

Avoid overly diagonal buildings and exaggerated isometric perspective.

Maintain the approved solid, readable top-down/light-3/4 pixel RPG style.

## 5. PROFESSIONAL URBAN AND LANDSCAPE PLANNING

Plan the district before placing artwork.

- Establish clear main routes and smaller exploration paths.
- Build believable boundaries between zones.
- Keep streets and entrances navigable.
- Organize props into meaningful functional clusters.
- Ensure rivers, lakes, coastlines, railways, bridges, hills, and walls have spatial logic.
- Avoid isolated decorative objects in main walkways.
- Provide appropriate gathering spaces and scenic pauses.
- Maintain a comfortable density of destinations.

The southern expansion should feel rich and explorable without becoming oversized or exhausting.

Do not expand empty terrain merely to increase map dimensions.

Use connecting paths, shortcuts, and travel transitions where necessary.

## 6. REUSE THE VERIFIED PRODUCTION PIPELINE

Before editing, read:

- `AGENTS.md`
- `docs/ART_SKILL_REGISTRY.md`
- Existing Agent Sprite Forge execution reports.
- Approved urban-zoning documents.
- Current Living Seoul production and refinement reports.

Use applicable skills from:

https://github.com/0x0funky/agent-sprite-forge

Especially `generate2dmap` and `generate2dsprite` for maps, landmarks, original props, finishing, validation, and Tiled-compatible exports.

Preserve Juni's approved 144-frame animation system.

Do not install redundant tools or invoke paid AI providers without explicit approval.

Document which tools were actually executed.

## 7. REAL PHASER INTEGRATION

Implement a genuinely playable world, not just concept boards.

Verify:

- Logical collision boundaries.
- Connected pedestrian routes.
- Functional entrances and travel transitions.
- Reliable Y-depth sorting and occlusion.
- Smooth camera movement.
- Correct object and character scale.
- Efficient map rendering and asset culling.
- Responsive mobile controls.
- Consistent animation playback.

Profile actual game FPS separately from recorded-video FPS.

Prefer a measured, performant implementation over unnecessarily large maps.

## 8. IMPLEMENTATION STAGES

**Stage A — Northern District Repair**

Fix all blue-marked walls and fences, improve crowded building spacing, and verify collisions.

**Stage B — Southern Masterplan**

Create a detailed southern zoning layout showing Namsan, entertainment, Busan coast, Jeju nature, transition areas, roads, and travel connections.

**Stage C — Landmark Production**

Use Sprite Forge to create four original, premium-quality thematic environments with clearly different silhouettes and atmospheres.

Integrate them into the playable Phaser world.

**Stage D — Final Integration and QA**

Validate navigation, transitions, landmarks, performance, mobile gameplay, and existing systems.

Preserve checkpoints between stages.

## 9. REQUIRED DELIVERABLES

Provide:

1. Before/after screenshots of every blue-marked northern defect.
2. One complete, readable overview map.
3. A southern-district masterplan showing all four themed destinations.
4. Native-scale screenshots of each unique landmark.
5. A visual comparison showing the traditional-to-modern progression.
6. A real Phaser gameplay walkthrough demonstrating connected exploration.
7. A playable review ZIP.
8. Navigation, collision, performance, and build/test reports.

Update the four `STUDIO_*` files and skill documentation if the pipeline changes.

Commit and push tested checkpoints to the development branch.

Do not merge into `main`, publish the unfinished game, use paid services, or modify the separate Korean Arena learning application.

## FINAL QUALITY STANDARD

The northern district should feel like a coherent historic Korean neighborhood with flawless architectural boundaries.

The southern district should feel like a memorable journey through modern Korean culture, entertainment, coastal tourism, and Jeju nature.

**Every destination should make the player want to explore it. Every transition should feel intentional. Every building should belong exactly where it stands.**

START NOW.

Complete Stage A, then produce and validate the Stage B masterplan. Proceed with playable landmark production in reviewable increments, and stop for user approval before mass-producing the entire southern world.
## 10. MOBILE LANDSCAPE MODE — MANDATORY

Korean Arena is a landscape-first pixel social RPG.

The current mobile preview uses portrait orientation, which is unsuitable for exploring the large Korean world.

**Implement a polished landscape gameplay experience on mobile devices.**

### Requirements

1. **Landscape-first gameplay**
   - Target 16:9 landscape as the primary mobile presentation.
   - Adapt gracefully to wider and narrower landscape aspect ratios.
   - Maintain correct pixel-art proportions without stretching, blurring or cutting off important content.
   - Preserve the existing desktop experience.

2. **Screen orientation**
   - Use the Screen Orientation API where supported to request landscape mode when entering gameplay.
   - If the browser cannot lock orientation, show a beautiful Korean Arena "Rotate your device" screen in portrait mode.
   - Automatically resume the game layout when landscape orientation is detected.
   - Do not falsely assume iOS Safari or all mobile browsers support orientation locking.

3. **Mobile controls**
   - Place a comfortable virtual joystick or directional pad on the lower-left.
   - Place interaction, run and emote buttons on the lower-right.
   - Keep controls transparent enough to preserve visibility of the world.
   - Support multi-touch, responsive input and configurable control sizes.
   - Respect notches, rounded corners and safe-area insets.

4. **Landscape camera and UI**
   - Optimize Phaser camera framing for horizontal exploration.
   - Keep Juni visible with useful forward-looking space.
   - Adapt dialogue panels, quests, minimap and interaction prompts to landscape.
   - Avoid oversized panels blocking the scenery.
   - Maintain readable Korean and Vietnamese text.

5. **Performance**
   - Use responsive resolution scaling and integer pixel-art rendering where appropriate.
   - Avoid unnecessary high-DPI rendering costs.
   - Preserve smooth character animation and camera movement.
   - Support Canvas fallback when WebGL performs poorly.

6. **Testing**
   - Test common mobile landscape resolutions and aspect ratios.
   - Verify Android Chrome and iOS Safari behavior where test environments are available.
   - Test portrait-to-landscape transitions, touch input, dialogue, UI scaling, safe areas and gameplay pause/resume.
   - Distinguish emulator tests from real-device testing.

### Required Deliverables

- Real Phaser mobile landscape screenshots.
- A landscape gameplay demonstration.
- A portrait-mode rotate-device screen.
- Responsive UI and touch-control verification.
- Performance measurements and browser compatibility notes.

**Acceptance criterion: On mobile, Korean Arena must feel like a native landscape RPG, not a portrait webpage rotated sideways.**

Do not break desktop gameplay, Juni animations or the existing world systems.
