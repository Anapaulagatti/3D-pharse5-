MASTER PROMPT — LIVING SEOUL FULL MAP + MOBILE MOBA UI + WORLD REFINEMENT
You are working on:
- Repository: Anapaulagatti/3D-pharse5-
- Active branch: rebuild/pixel-social-rpg-v3
The district/zoning plan is approved.
Proceed with the next production step.
GOAL
Turn the current project into a more complete and reviewable Living Seoul pixel game by doing all of the following in one coordinated pass:
1. Build a full connected world map based on the approved zoning plan.
2. Export a true full-map overview so the whole world can be reviewed at once.
3. Replace the current mobile controls with a landscape MOBA-style UI inspired by Arena of Valor / Wild Rift ergonomics.
4. Refine the world so it feels like exploring a Korean district / mini-city, not a loose collection of separated buildings.
5. Fix current world issues:
   - some compounds feel too empty
   - some buildings are too far apart
   - some fences/walls overlap or fail to enclose compounds properly
   - some buildings look too similar
   - the lower half of the map needs stronger contrast and more modern landmarks
   - gameplay video still feels too stuttery / not smooth enough
Do not redesign from scratch.
Use the approved plan as the foundation.
1) FULL CONNECTED MAP
Build and maintain one coherent connected world that feels like a living Korean district.
Core map principles
- The map must feel planned and logical, not randomly decorated.
- Roads, plazas, alleys, walls, rivers, bridges, gardens, and building entrances must have believable relationships.
- If something is a fortress / palace / walled compound, it must have logical surrounding walls, gates, courtyards, and internal structure.
- If something is a street district, it must have proper roads, frontage, trees, props, shop edges, and pedestrian flow.
- Each district should feel like a destination, not filler.
Spatial design rules
- Reduce the feeling that buildings are too far apart.
- Compress travel distances where needed so movement feels enjoyable.
- Keep enough space for exploration, but avoid excessive empty walking.
- When entering a gate or walled area, the inside must not feel barren — add meaningful spatial content:
  - court / garden / monument / pavilion / side buildings / signage / resting spaces / interactive learning points.
- Fix all fence and wall issues:
  - no broken enclosure logic
  - no awkward overlaps
  - no clipped wall segments
  - no “half-enclosed” compounds unless intentionally designed
- Add proper boundaries for compounds using walls, hedges, fences, stone edges, or water edges where appropriate.
2) DISTINCT BUILDING IDENTITY
Every major building or landmark must have its own identity.
Requirements
- Do not let all buildings feel like slight variations of the same hanok.
- Each major destination must have:
  - unique silhouette
  - unique entry composition
  - unique courtyard or frontage
  - unique prop language
  - unique color/material emphasis within the approved art direction
  - unique gameplay purpose or emotional tone
- Buildings should feel like interesting destinations in Korea.
Architectural logic
- Preserve Korean identity, but do not make the whole world 100% old-fashioned.
- Mix traditional, cultural, educational, scenic, and modern-famous Korean place inspiration.
- Keep structures mostly readable and grounded — avoid awkward “tilted / overly diagonal / pseudo-3D boxy” compositions that feel uncomfortable.
- Buildings should feel like clean pixel architecture with readable fronts and logical footprints.
3) TRADITIONAL-TO-MODERN KOREA TRANSITION
The world should feel like a journey across Korea.
Northern / traditional side
Retain the approved historical / palace / academy logic.
Southern / contrast side
Create stronger contrast using Korean-inspired modern or iconic destinations, for example:
- N Seoul Tower / Namsan
- Everland-inspired leisure zone
- Haeundae Blue Line Park-inspired scenic/coastal mobility zone
- Jeju-inspired nature/leisure zone
Transition requirement
The lower half should feel like a gradient from traditional Korea to modern Korea:
- path design should guide this transition naturally
- materials, props, greenery, lighting, and architecture should evolve gradually
- the full map should feel alive and varied, not split into disconnected themes
4) FULL MAP OVERVIEW EXPORTS
I need to review the whole world clearly.
Create and export:
1. One full-map overview image
2. One labeled planning overview
3. One gameplay-scale overview
4. One journey overview showing how the player moves through the districts
5. If useful, one before/after comparison board
The overview must make it easy to inspect:
- district boundaries
- landmark identities
- road logic
- walls/fences
- density and spacing
- travel flow
- traditional-to-modern transition
5) MOBILE LANDSCAPE UI — MOBA STYLE
The current mobile experience feels wrong.
Replace it with a more natural landscape mobile game UI using the layout ergonomics of Arena of Valor / Wild Rift.
Requirements
Left side
- Replace directional buttons with a virtual joystick
- Bottom-left placement
- smooth drag movement
- support 8-direction feel where appropriate
- should feel like a real movement stick, not web buttons
Right side
Use a clean bottom-right action cluster, adapted for exploration/learning rather than combat:
- Interact / Explore
- Talk / Confirm
- Sprint / Move Faster if useful
- Emote / Expression
- optional Quest / Map shortcut only if it improves usability
Do not turn the game into a combat-heavy UI.
Use MOBA control ergonomics, not combat clutter.
Top UI
Keep top UI compact:
- area name
- minimap
- pause/menu
- current hint/objective if needed
Mobile orientation
- Mobile play must be landscape only
- Do not use portrait preview as the primary mobile mode
- respect thumb zones and safe margins
- avoid large floating web-style panels during play
6) GAME FEEL + PERFORMANCE
Improve overall feel so it no longer looks like static images sliding around.
Requirements
- movement should feel smoother
- camera movement should feel stable
- animation playback should feel more natural
- traversal should feel pleasant on the larger map
- reduce visible stutter and lag in review builds
- keep FPS stable where possible
- optimize rendering on the larger world
- if needed, segment/stream distant content sensibly
- preserve actual animated movement, not fake sliding
7) PRESERVE CURRENT STRENGTHS
Keep and build upon:
- approved zoning plan
- current pixel-art direction
- Korean architectural identity
- current character quality (including Juni and approved character work)
- existing working codebase
- current branch work
- existing verified review assets that are still relevant
Do not:
- revert to 3D
- replace the project with a generic RPG template
- destroy approved map logic
- publish publicly unless explicitly approved
8) DELIVERABLES
Produce all of the following:
1. Updated playable build
2. Full connected map implementation
3. Full-map overview PNG
4. Labeled world-plan PNG
5. Mobile landscape UI screenshots
6. Short mobile gameplay clip
7. Short traversal clip across multiple districts
8. Short report describing:
   - what changed in the map
   - what changed in mobile UI
   - how spacing/travel was improved
   - how fences/walls were fixed
   - how major buildings were differentiated
   - how traditional-to-modern transition was handled
   - current performance notes
   - remaining blockers, if any
9) VALIDATION
Before reporting completion:
- run build
- run tests
- verify mobile landscape controls
- verify joystick and action buttons
- verify overview exports exist
- verify full-map traversal works
- verify no major UI overlap
- verify compounds have correct enclosure logic
- verify building identities are visually distinct
- verify travel distances feel reasonable
- verify the map does not feel empty after entering gates/compounds
- verify gameplay is smoother than before
Do not claim completion unless the full-map overview, mobile controls, and map refinements are actually implemented.
10) START NOW
Use the approved zoning plan as the source of truth.
Execution order:
1. refine the connected world structure
2. fix spacing, fences, and compound logic
3. strengthen landmark identity and traditional-to-modern contrast
4. export the full-map overview set
5. replace mobile controls with landscape MOBA-style UI
6. optimize movement/game feel
7. produce review assets and report
The final result should feel like exploring a small but vivid Korean district/city in pixel form, with clear landmark identity, logical planning, enjoyable traversal, and a proper mobile game interface.