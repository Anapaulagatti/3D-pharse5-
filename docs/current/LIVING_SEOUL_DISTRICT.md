# KOREAN ARENA — LIVING SEOUL DISTRICT EXPANSION

Repository: `Anapaulagatti/3D-pharse5-`  
Branch: `rebuild/pixel-social-rpg-v3`

You are the World Designer, Pixel Art Director, Character Animator and Phaser RPG Engineer.

## 1. MANDATORY SKILL MEMORY

The required skill registry has already been committed to GitHub.

Before starting, read:

- `AGENTS.md`
- `docs/ART_SKILL_REGISTRY.md`
- `docs/gwanghwamun/FORGE.md`
- `docs/juni-animation/TOOLCHAIN.md`
- All four `STUDIO_*` files.

Read the applicable upstream SKILL.md files before every relevant art, map, animation or NPC production task.

Reuse the verified Agent Sprite Forge, Character Animation Creator and Phaser pipelines that produced Juni and Gwanghwamun.

Keep this requirement persistent in AGENTS.md for all future Codex sessions.

## 2. OBJECTIVE — A REAL EXPLORABLE KOREAN DISTRICT

The current Gwanghwamun Plaza is too small to feel like a living RPG world.

Expand it into a large, connected, beautifully crafted Seoul-inspired pixel district.

Take inspiration from Pixels.xyz's sense of exploration, walkable communities and discoverable activity areas.

Do NOT copy Pixels.xyz's actual maps, artwork, buildings, characters or proprietary game systems.

Preserve the approved Juni animations, Korean architecture and existing Gwanghwamun artwork.

The new environment should feel like exploring an entire neighborhood, not an oversized empty plaza.

## 3. WORLD DESIGN

Create a cohesive district containing:

- Gwanghwamun central plaza.
- Sejong Hangul Academy and library.
- Jang Yeong-sil invention workshop and observatory.
- Shin Saimdang art hanok and botanical garden.
- Yi Sun-sin historical museum and strategy pavilion.
- Traditional hanok residential alleys.
- Korean market street, cafés and resting corners.
- Gardens, small streams, stone bridges and decorative courtyards.

Architecture must reflect Korean identity: giwa roofs, timber framing, traditional gates, stone foundations, courtyards and authentic cultural details.

Use interconnected main streets, smaller side alleys, landmarks, scenic corners and shortcuts.

Allow players to discover meaningful locations naturally while walking.

Do not arrange everything in a rigid square grid.

## 4. INTELLIGENT BUILDING AND PROP PLACEMENT

Every building must have a purpose, entrance, accessible route and believable surroundings.

Place objects logically:

- Benches near gardens, trees or resting areas.
- Lamps beside paths, gateways and bridges.
- Onggi jars near traditional buildings.
- Signs beside meaningful entrances.
- Market goods beside stalls.
- Flowers, fences and shrubs framing courtyards.

No random isolated benches, blocked entrances, meaningless clutter or props scattered through main roads.

Use visual hierarchy, carefully planned negative space, natural-looking clusters and recognizable navigation landmarks.

Ensure every important NPC and building is reachable.

## 5. HISTORICAL NPCs AND ASSOCIATED BUILDINGS

Create four original premium-quality animated historical educational guests:

**King Sejong**
- Home location: Hangul Academy.
- Teaching space with books, Hangul displays and a courtyard.
- Beginner Hangul matching activity.

**Jang Yeong-sil**
- Home location: Invention Workshop.
- Instruments and scientific demonstrations inspired by Joseon achievements.
- Numbers and object-vocabulary activity.

**Shin Saimdang**
- Home location: Art Hanok and Garden.
- Painting workspace, flowers, natural scenery.
- Colors, nature and art-vocabulary activity.

**Admiral Yi Sun-sin**
- Home location: Historical Museum.
- Naval-history exhibits, maps and strategy displays.
- Simple Korean instruction and dialogue activity.

Treat these figures as educational historical guests from different eras.

Give each NPC unique facial features, clothing, personality, four-direction sprites, real idle/walk/greeting animations and expressive dialogues.

Match Juni's approved character scale and pixel quality.

Use original, historically informed artwork and accurate Vietnamese-first Korean-learning content.

## 6. GAMEPLAY AND WORLD SYSTEMS

Implement:

- Smooth camera-following exploration.
- Seamless or carefully masked transitions between outdoor areas.
- Accessible building entrances and lightweight interiors.
- NPC approach, dialogue and interaction.
- Simple quest markers and a district mini-map.
- Local progress saving for first learning activities.
- Proper collision, occlusion, depth sorting and navigation.
- Mobile touch controls and performance-conscious map streaming.

Build a world substantially larger than the current 1024×768 plaza, but choose its dimensions based on gameplay density and performance rather than arbitrary size.

Use reusable map chunks, original tiled assets, layered maps and Tiled-compatible exports where suitable.

No large empty areas just to make the map appear bigger.

## 7. INCREMENTAL IMPLEMENTATION

Follow these milestones:

**A — Master District Plan**
Create a readable connected district layout, road network, building footprints, entrances and NPC locations.

**B — World Expansion**
Produce the connected outdoor map using verified Sprite Forge pipelines. Preserve the existing plaza and approved art.

**C — Historical Buildings**
Create four distinct landmark buildings and their accessible educational spaces.

**D — Living NPCs**
Integrate four genuinely animated characters using the approved Juni animation pipeline.

**E — Learning and Exploration**
Add four original short Korean-learning activities, dialogues and navigational guidance.

Complete and test each milestone before proceeding. Preserve working checkpoints and recoverability.

## 8. VALIDATION AND DELIVERY

Provide:

1. Full district overview map.
2. Actual native-scale Phaser screenshots.
3. Playable exploration build.
4. Real gameplay video showing Juni walking between multiple areas and entering a historical building.
5. Four historical buildings and NPC character review boards.
6. NPC dialogue and learning activity demonstrations.
7. Navigation, collision, performance, mobile and test reports.
8. Actual Sprite Forge and skill execution records.

Run typecheck, lint, unit tests, build, browser tests, map reachability and asset integrity checks.

Update AGENTS.md, the skill registry if necessary, and all STUDIO records.

Commit and push verified checkpoints to the development branch.

Do not use paid APIs without explicit approval.
Do not modify the separate Korean Arena learning app.
Do not automatically publish the unfinished game or trigger GitHub Pages deployment.

**SUCCESS = A large, beautiful, connected Korean pixel district where Juni can genuinely explore, enter meaningful buildings, meet expressive historical NPCs and learn Korean through gameplay.**

Start with the master district plan, then implement the first connected playable expansion. Produce review evidence before mass-producing the remaining areas.