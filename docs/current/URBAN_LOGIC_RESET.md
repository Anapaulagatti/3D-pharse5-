MASTER PROMPT — REBUILD KOREAN DISTRICT MAP WITH REAL URBAN LOGIC
You are rebuilding the Korean Arena / Living Pixel Seoul world map.
Core objective
Do not place buildings and props randomly for visual appeal.
Build the map like a real Korean historical district / urban quarter with clear planning logic, readable exploration flow, and distinct landmarks.
Visual direction
- Pixel art, polished and readable.
- Korean historical / cultural atmosphere.
- Top-down or very light 3/4 view.
- Buildings must feel solid and structured, not overly tilted or diagonally skewed.
- Avoid the “random asset collage” look.
- Keep strong Korean identity in roofs, gates, stone paths, courtyards, lanterns, walls, trees, and public spaces.
World-planning rules
1. Plan the district first, decorate later.
2. The map must feel like one connected Korean quarter, not separate pretty screenshots.
3. Every major structure must have a function:
   - main plaza
   - academy / Hangul school
   - historical guest / NPC buildings
   - market street / bookstore / tea house
   - residential hanok area
   - pavilion / garden / pond
   - fortress gate / wall / cultural monument
4. If there is a fortress wall, it must logically continue and define a boundary.
5. If there is a river / stream, it must have believable edges, crossings, bridges, and route purpose.
6. If there is a street, it must have road hierarchy, walking routes, trees, benches, signs, and frontage logic.
7. Props must be placed with rules — no awkward random bench or object in the middle of a route unless intentionally designed.
8. Use Korean historical references so the space feels culturally grounded and believable.
Required map structure
Design the district as an explorable macro-layout with multiple connected zones:
- Central Plaza: social hub, NPC gathering, player meeting space.
- Academy District: Hangul / TOPIK learning zone, courtyard, classroom entry.
- Historical Street: NPCs based on Korean historical figures, each tied to a meaningful building or mini-location.
- Market / Culture Street: bookstore, stationery, tea house, craft stall, cultural shop.
- Garden / Rest Area: pond, pavilion, stone path, shaded trees.
- Fortified / Landmark Zone: gate, wall segment, monument, or symbolic civic building.
Architectural logic
- Each building must be visually distinct in shape, footprint, facade rhythm, and surrounding props.
- Do not clone similar hanok buildings with only color changes.
- Use different scales:
  - civic / monumental
  - educational
  - residential
  - market
  - ceremonial
- Preserve coherence while avoiding repetition.
NPC integration
Add meaningful NPC placements tied to architecture:
- each important NPC belongs to a place
- their building or zone should reflect their identity
- do not place NPCs randomly in open space without environmental meaning
Historical NPCs can be inspired by safe public-domain Korean historical figures or educationally suitable equivalents.
Gameplay flow
The player should feel like they are exploring a district, not a tiny diorama.
Create:
- clear main route
- side routes
- discovery corners
- readable entrances
- logical transitions between zones
- room for future quests, dialogue, mini-games, and learning events
Deliverables
1. A district masterplan before final placement.
2. A cleaned, large connected map layout.
3. Distinct buildings and landmarks.
4. Logical roads, walls, water, courtyards, and vegetation.
5. A short planning document explaining why each zone exists and how the player moves through it.
6. Keep current good pixel quality, but prioritize urban logic, exploration clarity, and Korean cultural authenticity.
Important restrictions
- Do not make buildings overly diagonal.
- Do not place rivers, walls, bridges, or props arbitrarily.
- Do not produce repeated near-identical buildings.
- Do not shrink the world into a tiny decorative board.
- Build for long-term expansion with NPCs, quests, learning loops, and district-scale exploration.
Final quality test
Before finalizing, verify:
- Does this feel like a believable Korean district?
- Does each structure have a clear purpose?
- Is the route logic understandable?
- Are major landmarks distinct?
- Do walls, roads, trees, and water obey placement rules?
- Does the player feel they are exploring a real place?

Before drawing or assembling the final map, first produce a district zoning plan and placement logic. Only after the zoning is approved should you build the final playable map.

## ADDITIONAL TASK — SAFE MAIN BRANCH PROMOTION

Repository: `Anapaulagatti/3D-pharse5-`

Keep `main` as the stable pixel-game branch and `rebuild/pixel-social-rpg-v3` as the active development branch.

The current district redesign is NOT yet approved for production.

### Requirements

1. Continue all Korean urban-planning, architecture, map, NPC and gameplay development on `rebuild/pixel-social-rpg-v3`.
2. Preserve the existing stable `main` branch.
3. After the new Korean district passes user visual review, gameplay tests and clean-clone verification, prepare a Pull Request targeting `main`.
4. Audit code differences, deleted assets, recovery tags, GitHub Actions, Pages settings and deployment triggers.
5. Update the outdated README and documentation to reflect the actual approved game.
6. Confirm the skill registry and `AGENTS.md` will be included in the future merge.
7. Ensure no unwanted GitHub Pages publication will occur.
8. Run full CI and resolve merge conflicts before requesting approval.

**Do not merge the Pull Request until the user explicitly approves the new district and authorizes the merge.**

After approval, perform a normal safe merge or fast-forward without force-pushing, rewriting Git history or deleting recovery tags.

Keep the development branch available for future features.

**Current action: Continue development on the existing branch. Prepare for a future main promotion, but do not merge or deploy yet.**