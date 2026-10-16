# KOREAN ARENA — BUILD LIVING SEOUL
## Premium Korean Pixel RPG World Production

**Role:** Lead World Designer, Korean Architecture Art Director, Pixel Artist and Phaser Engineer.

**Repository:** `Anapaulagatti/3D-pharse5-`
**Branch:** `rebuild/pixel-social-rpg-v3`

## MISSION

The refined 4096×3072 Living Seoul urban masterplan is **APPROVED**.

Begin building the real playable Korean district, using the approved zoning plan as the architectural and spatial source of truth.

The result must feel like exploring a beautiful, believable Korean historical neighborhood — not an assortment of similar houses and randomly placed decorations.

**Quality, architectural authenticity, exploration and distinctive locations are the priorities.**

## 1. MANDATORY SKILL PIPELINE

Before production, read:

- `AGENTS.md`
- `docs/ART_SKILL_REGISTRY.md`
- `docs/urban-zoning/PLAN.md`
- `docs/urban-zoning/BUILDING_SCHEDULE.md`
- `docs/urban-zoning/HISTORICAL_REFERENCES.md`
- `docs/urban-zoning/placement-rules.md`
- `docs/urban-zoning/zoning-plan.json`
- Previous Juni animation and Gwanghwamun Forge execution reports.

Use the relevant installed skills from:

- `0x0funky/agent-sprite-forge` — original pixel assets, tiles, maps, palettes, extraction, Tiled exports and QA.
- `tachikomared/character-animation-creator-skill` — NPC animation when needed.
- Existing validated Phaser, TypeScript and Vite workflows.

Use the actual tools and document their execution. Never claim a skill was used merely because it was installed.

No paid provider APIs without explicit authorization.

## 2. WORLD DESIGN — BUILD A REAL KOREAN DISTRICT

Follow the approved 4096×3072 masterplan and its building coordinates, entrances, roads, courtyards, walls, bridges and water network.

Preserve the urban logic:

- Palace compound with coherent enclosing walls and functional gates.
- Formal ceremonial avenue connected to the central plaza.
- Organic secondary streets, hanok alleys and pedestrian shortcuts.
- Distinct educational, historical, cultural, residential and garden areas.
- Connected stream, pond, believable banks and purposeful bridges.
- Accessible public buildings, courtyards and interaction points.
- Exploration loops rather than a single linear corridor.

Do not arbitrarily relocate approved landmarks or change the zoning logic.

Use Korean historical architectural references, particularly Gyeongbokgung, Changdeokgung, seowon academies and traditional hanok villages.

The fictional game district must be culturally grounded without claiming to be an exact historical reconstruction.

## 3. EVERY BUILDING MUST BE UNIQUE

**Absolutely no repeated near-identical hanok buildings with simple color changes.**

Every major structure needs:

- A unique architectural silhouette and footprint.
- A distinctive roof structure and facade rhythm.
- Its own entrance, courtyard and exterior arrangement.
- A recognizable material/color character.
- Purposeful surrounding objects and vegetation.
- A clear function, story and reason for players to visit.
- At least one memorable visual feature visible at normal gameplay scale.

Buildings should remain identifiable even with their labels hidden.

### Required destination identities

**Gwanghwamun Gate and Palace Boundary**
- Grand, ceremonial and monumental.
- Distinctive gate roof, stone foundations, enclosing walls and formal approach.
- Must feel like the district's major historical landmark.

**Sejong Hangul Academy**
- Peaceful, scholarly, welcoming.
- Unique study hall, library wings, reading courtyard and Hangul details.
- Future home for King Sejong's language-learning activities.

**Jang Yeong-sil Invention Workshop**
- Curious, inventive and technical.
- Asymmetric workshop, observation instruments, demonstration courtyard and original scientific props.
- Must not resemble the academy.

**Yi Sun-sin Historical Museum**
- Disciplined, heroic and educational.
- Distinct long exhibition building, military-history exhibits, maps and strategy pavilion.
- No fictional harbor unless logically justified by the approved world plan.

**Shin Saimdang Art Studio**
- Elegant, artistic and nature-oriented.
- Distinct painting hanok, botanical courtyard, brushes, artwork and flowers.
- A calm creative destination.

**Bookshop and Stationery Street**
- Intimate storefronts with individually designed facades.
- Bookshelves, hanji paper, writing tools, reading niches and meaningful shop signs.

**Traditional Tea House**
- Warm, social and relaxing.
- Unique low roof, veranda, tea garden and seating courtyard.

**Craft Workshop**
- Functional artisan architecture.
- Open workspace, craft equipment, drying area and material storage.

**Residential Hanok Alleys**
- Varied U-shaped, L-shaped, detached and garden houses.
- Unique household courtyards, gardens, low walls and entry gates.
- Believable residential scale, not miniature copies of palace buildings.

**Lakeside Pavilion and Garden**
- Open pavilion, landscape framing, natural planting and calm water views.
- A memorable scenic destination.

## 4. CONSISTENT PERSPECTIVE AND PIXEL QUALITY

Use premium handcrafted-looking pixel art.

- Top-down with a light 3/4 perspective.
- Solid, dimensional buildings with clear visible front walls.
- Roof ridges predominantly horizontal or perpendicular.
- Minimal diagonal/isometric skew.
- Stable proportions, lighting direction and pixel density.
- Architectural depth from pillars, eaves, layered roofs, foundations and shadows.
- Detailed Korean roofs, wooden joinery, windows, courtyards and landscaping.

**Do not tilt entire buildings diagonally just to simulate 3D.**

Keep Juni's approved 80px character scale and animation system. Buildings, gates, doors and steps must be believable relative to Juni.

Avoid flat placeholders, inconsistent scales, copied sprites and generic fantasy architecture.

## 5. PROFESSIONAL URBAN COMPOSITION

Every prop must have a spatial or gameplay reason to exist.

- Benches belong in resting pockets, gardens and scenic edges.
- Lanterns mark entrances, street corners and bridge approaches.
- Onggi jars belong beside appropriate household or service courtyards.
- Trees frame streets and plazas without hiding important entrances.
- Signs belong beside real destinations.
- Shop goods belong near storefronts.
- Paths follow usable public circulation, not arbitrary decorative curves.

Keep primary streets unobstructed and secondary paths navigable.

Courtyard walls must enclose meaningful spaces or include functioning gates.

Riverbanks must connect naturally to bridges, slopes and surrounding terrain.

Use visual hierarchy and negative space. **More props do not automatically mean a better map.**

## 6. MAKE EXPLORATION REWARDING

Design the district as a place players want to explore.

Each major destination should offer:

1. A recognizable exterior landmark.
2. An inviting approach and readable entrance.
3. A distinctive courtyard, activity area or interior.
4. At least one discoverable educational or cultural interaction.
5. A logical connection to nearby streets and attractions.

Create environmental storytelling through books, instruments, sculptures, craft materials, garden details and authentic Korean cultural elements.

Provide opportunities for future quests and social interaction without implementing unnecessary new systems now.

## 7. HISTORICAL NPC INTEGRATION

Reserve and validate purposeful locations for:

- King Sejong — Hangul Academy.
- Jang Yeong-sil — Invention Workshop.
- Shin Saimdang — Art Studio.
- Admiral Yi Sun-sin — Historical Museum.

Their surroundings must reflect their identity and educational purpose.

Use the approved Juni art quality and animation pipeline when producing the new NPCs.

Do not reuse previously rejected historical character artwork.

NPCs must never obstruct entrances or essential pedestrian routes.

## 8. PLAYABLE MAP IMPLEMENTATION

Produce a real Phaser map, not only a concept image.

- Use original Sprite Forge assets and editable layered tilemaps.
- Export Tiled-compatible source data.
- Implement reliable collision and Y-depth sorting.
- Handle rooftop/tree occlusion correctly.
- Connect streets and map sections seamlessly.
- Preserve actual building entrances and interaction anchors.
- Stream or cull map content where appropriate.
- Maintain stable camera-follow movement and mobile touch controls.
- Reuse Juni's existing real animation frames.

The world should feel large because it contains meaningful destinations, not empty terrain.

## 9. PRODUCTION CHECKPOINTS

**Stage A — Architecture Art Bible**

Create a visual comparison of the major building types at consistent scale.

Prove each structure has a unique identity, architectural mass and gameplay purpose.

**Stage B — First Finished Playable District Slice**

Implement the palace gateway, plaza, surrounding streets and first connected landmark buildings with near-final pixel art.

Demonstrate correct scale, unique facades, walls, roads, entrances and landscaping in Phaser.

**STOP for visual approval of Stage B before mass-producing the remaining buildings.**

**Stage C — Full District Production**

After approval, complete the remaining approved streets, cultural buildings, gardens, housing, workshops and historical destinations.

**Stage D — NPC and Educational Integration**

Integrate distinct historical NPCs and associated cultural interactions using the approved character workflow.

Validate after each stage and preserve recoverable Git checkpoints.

## 10. REQUIRED PROOF AND QA

Deliver:

- An actual Phaser overview of the completed production area.
- A building-identity comparison board at matching scale.
- Native-scale exterior and courtyard screenshots.
- A real gameplay walkthrough showing Juni exploring connected destinations.
- A playable review ZIP.
- A short report explaining each landmark's design identity and historical references.
- Collision, navigation, map-boundary, occlusion, mobile, build and test results.
- Actual skill/tool execution records.

A static concept board is not proof that the playable map has been implemented.

## 11. SAFETY AND GITHUB

- Keep the existing playable game recoverable.
- Preserve Juni's approved animations and the existing learning systems.
- Use only `rebuild/pixel-social-rpg-v3` for development.
- Keep `main` as the stable branch.
- Maintain `AGENTS.md`, the skill registry and four `STUDIO_*` files.
- Commit and push tested milestones with verified recovery checkpoints.
- No force-push, automatic public deployment or paid services.
- Do not modify the separate Korean Arena learning application.

## FINAL QUALITY STANDARD

When exploring Korean Arena, players should feel:

**"Every street leads somewhere interesting. Every building has its own personality. This genuinely feels like discovering a charming district of Korea."**

Not:

"These are similar-looking houses placed randomly around a large map."

**The masterplan is approved. Start real production now, complete Stage A and the first playable Stage B, then stop for visual review before mass production.**
