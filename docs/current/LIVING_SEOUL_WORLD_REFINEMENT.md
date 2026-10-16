# KOREAN ARENA — LIVING SEOUL WORLD REFINEMENT
## Palace Interior, Urban Density, Architecture Diversity & Smooth Gameplay

**Repository:** `Anapaulagatti/3D-pharse5-`  
**Branch:** `rebuild/pixel-social-rpg-v3`

You are the Lead Korean World Designer, Pixel Art Director, Urban Planner and Phaser Performance Engineer.

The current architectural quality is accepted as the working baseline, but the world still feels too empty, widely spaced, visually repetitive and insufficiently alive.

**Improve the existing world instead of rebuilding approved artwork from scratch.**

## 1. MAKE THE PALACE WORTH EXPLORING

The current Gwanghwamun-inspired gate looks impressive, but the space beyond it feels empty.

Create a meaningful palace experience with:

- An attractive entrance courtyard and ceremonial pathway.
- A distinct inner gate, landscaped court and recognizable main hall.
- Korean royal architectural details, banners, stone lanterns and gardens.
- A small cultural exhibition or educational interaction.
- Clear routes, gates, walls, entrances and collision.
- An inviting destination visible shortly after passing the main gate.

Use Gyeongbokgung and Changdeokgung as architectural references without falsely claiming historical reconstruction.

Preserve the approved palace wall geometry or document any necessary changes.

Do not build a huge empty courtyard or a palace composed only of repeated gates.

## 2. FIX WORLD SCALE AND WALKING DISTANCES

The current map feels too spread out. Important destinations are separated by excessive empty walking space.

Perform a **gameplay-density and urban-layout pass**:

- Bring related buildings and attractions closer together.
- Create compact walkable neighborhoods with meaningful street frontages.
- Reduce oversized empty lawns, courtyards and road segments.
- Connect destinations through appealing streets, alleys and shortcuts.
- Add interesting corners, social gathering spots and discoveries along the way.
- Keep intentional open space for major ceremonial landmarks.

Use the existing 4096×3072 plan as a reference, **not a mandatory footprint that must be filled**. If a smaller, denser playable area offers a better experience, propose and implement justified adjustments on the review candidate while preserving the approved overall district logic.

Do not simply increase Juni's movement speed to hide poor map composition.

Measure travel times between major destinations at normal gameplay speed. Provide a before/after comparison.

Players should encounter meaningful scenery and opportunities for interaction frequently, not spend most of their time crossing empty ground.

## 3. ADD REALISTIC PROPERTY BOUNDARIES AND DISTINCTIVE BUILDINGS

Several buildings look exposed without surrounding walls, gates, courtyards or a clear relationship to the street.

Improve architectural composition:

- Hanok homes: low walls, entrance gates, private gardens and household courtyards.
- Academy: scholarly compound walls, recognizable gateway and organized learning courtyard.
- Historical museum: ceremonial approach and landscaped frontage.
- Invention workshop: workshop courtyard, equipment enclosures and service entrance.
- Shops and cafés: welcoming street-facing facades, not unnecessarily enclosed compounds.

Use fences and walls only where logically appropriate. Do not surround every building with identical fences.

Every destination must have a different identity through silhouette, roof arrangement, building proportions, entrance design, facade, materials, landscaping and function.

**No repeated hanok templates with different colors.**

Preserve clear public access, interaction points and collision-free walking routes.

## 4. INTRODUCE MODERN KOREAN LANDMARKS

Korean Arena should represent **both traditional and modern Korea**, not only ancient architecture.

Introduce a thoughtfully planned transition toward a modern Seoul neighborhood.

Potential original pixel-art interpretations:

- N Seoul Tower — skyline and scenic destination.
- Dongdaemun Design Plaza — contemporary architecture and cultural events.
- Modern Seoul cafés and shopping streets.
- Contemporary Korean bookstores, convenience stores and fashion shops.
- A small modern city plaza with lighting, signage and social activity.

Do not randomly place skyscrapers next to the royal palace.

Create a coherent progression:

**Historical Palace → Traditional Hanok Streets → Cultural/Commercial Transition → Modern Seoul District**

Use real Korean landmarks as visual and cultural references, but create original pixel artwork and appropriately scaled adaptations.

For now, establish the transition area and prototype **one distinctive modern landmark or street corner** for review. Do not mass-produce an entire modern district without approval.

Maintain consistent pixel density, lighting, top-down/light-3/4 perspective and scale relative to Juni.

## 5. ELIMINATE STUTTER AND IMPROVE SMOOTHNESS

The exploration video appears noticeably choppy. Determine whether this comes from gameplay performance, animation timing, frame pacing, camera movement or video encoding.

**Do not assume the game is slow simply because the previous video was encoded at 15 FPS.**

Profile and improve:

- Phaser actual frame time and FPS.
- Camera-follow smoothness and integer pixel snapping.
- Input responsiveness and character animation cadence.
- Tilemap/chunk rendering and asset culling.
- Texture management and draw-call overhead.
- Large transparent sprites, occlusion and depth sorting.
- Collision-update efficiency.
- Mobile rendering and high-DPI scaling.
- Loading transitions between buildings and outdoor scenes.

Eliminate unnecessary per-frame allocations and expensive recomputation where demonstrated by profiling.

Maintain sharp pixel art without visible camera jitter or character movement jumping between pixels.

Capture new real-input gameplay at **at least 30 FPS**, preferably 60 FPS if capture hardware supports it.

Report measured runtime FPS/frame times separately from encoded video FPS.

Compare before/after under equivalent scenes and hardware conditions.

Do not invent performance measurements or weaken existing tests.

## 6. MANDATORY PRODUCTION RULES

Before work, read:

- `AGENTS.md`
- `docs/ART_SKILL_REGISTRY.md`
- Current urban masterplan and building schedule.
- Previous Agent Sprite Forge execution reports.
- Juni animation and existing production QA documentation.

Use the appropriate verified `generate2dmap`, `generate2dsprite`, map-processing, pixel-finishing and Tiled workflows.

Preserve Juni's approved character identity and 144-frame animation system.

Preserve the current functional game and create a recovery checkpoint before significant map changes.

No paid APIs, unrelated gameplay systems, automatic deployment or premature merge into `main`.

## 7. DELIVERABLES AND APPROVAL

Provide:

1. An improved palace interior/courtyard gameplay preview.
2. A more compact district layout with measured walking distances.
3. Before/after comparisons of fences, entrances and building identity.
4. One modern Korean landmark or street-corner prototype integrated logically into the world.
5. A real 30/60 FPS gameplay video demonstrating smooth exploration.
6. Actual gameplay performance measurements and optimization report.
7. Native-scale Phaser screenshots, playable review build and verified tests.

Validate collisions, route reachability, entrances, camera, assets, mobile input, reduced motion, TypeScript, unit tests, browser tests and production build.

Commit recoverable checkpoints on the development branch.

**STOP for user visual and gameplay approval before expanding the full modern district or implementing the remaining NPCs.**

## FINAL QUALITY STANDARD

The player should feel they are exploring a compact, lively, memorable Korean neighborhood.

Every short journey should lead to something visually interesting or interactive.

Every building should have its own architectural identity.

The palace should feel like a real destination.

Traditional and modern Korea should coexist through believable urban transitions.

Exploration should feel smooth, engaging and rewarding.

**START NOW. Improve density, palace experience, building boundaries, visual diversity and measured performance — not merely increase the map size or number of assets.**