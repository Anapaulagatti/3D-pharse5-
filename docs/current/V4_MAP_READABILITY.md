KOREAN ARENA — V4 FINAL MAP READABILITY & COMPOUND BOUNDARY POLISH
Repository: Anapaulagatti/3D-pharse5-
Branch: rebuild/pixel-social-rpg-v3
OBJECTIVE
The current world map is close to approval.
Do not redesign the whole world.

This task is a targeted final polish pass focused on two specific issues only:
1. Fix the remaining path / road / walkway defects in the areas marked with blue circles.
2. Improve readability and navigation in the southern modern district by giving each destination a clearer independent compound / boundary / frontage, so the area feels organized instead of visually messy.
The map should become easier to read at a glance, easier to navigate as a player, and more spatially logical.
1) FIX THE BLUE-CIRCLE PATH ISSUES
Inspect the currently approved world map and repair the remaining awkward pathing areas marked by the user.
Required path fixes
- Remove small visual glitches, broken edges, awkward joints, or inconsistent paving transitions.
- Ensure curves, corners, and intersections look intentional and clean.
- Align paths better with entrances, stair access, plazas, and transitions between districts.
- Avoid “half-road / half-path” awkward shapes that look like accidental leftover tiles.
- Ensure no path segment looks clipped, disconnected, misaligned, or too narrow.
- If a path belongs to a mountain / park / nature area, keep it organic.
- If a path belongs to the modern district, make it structured and orderly.
Important
Do not over-widen everything.
Do not turn every path into a road.
Preserve the environmental identity of each zone.
2) CLEAN UP THE SOUTHERN MODERN DISTRICT
The red-marked southern area currently feels too cluttered and visually blended together.
The player cannot immediately understand where one destination begins and another ends.
Main requirement
Give each major southern destination a clearer independent compound identity.

That means each destination should have some combination of:
- a defined entrance zone,
- a small fence / railing / hedge / planter boundary,
- a distinct paving language,
- a frontage plaza,
- a local edge treatment,
- clearer separation from neighboring attractions,
- a more obvious approach path.
The goal is not to wall everything off heavily.
The goal is to make each place feel like a recognizable destination with its own readable footprint.
3) APPLY THIS TO EACH SOUTHERN DESTINATION
A. Namsan / Tower hillside zone
This zone should feel like a scenic park destination, not random assets on grass.

Improve by:
- clarifying the arrival path,
- making the observation area feel like a proper site,
- using landscape edging, low railings, stone borders, small retaining edges, or planted boundaries,
- separating the tower zone from adjacent circulation routes,
- keeping it natural and elevated, not boxy.
B. Station / transit / promenade core
This area is the central modern mobility hub and must be the clearest area in the south.

Improve by:
- creating a very readable main pedestrian spine,
- clarifying platform forecourt vs. retail frontage vs. waterfront movement,
- separating circulation lanes from destination spaces,
- using paving hierarchy and low barriers / curbs / planters,
- making it obvious where players pass through and where they stop/explore.
C. Amusement / attraction zone
The amusement park section currently reads as separate objects placed near each other.

Improve by:
- giving the attractions a shared mini-district logic,
- using one entrance sequence,
- creating a coherent internal pedestrian loop,
- adding decorative boundary elements such as hedges, light fences, banner posts, ticket frontage, or plaza edges,
- making the ferris wheel / carousel / arch feel like parts of one destination rather than isolated items.
D. Modern shop / building frontages
Modern buildings should not just sit beside the road with weak definition.

Improve by:
- giving storefronts a proper frontage,
- adding small entry courts, sidewalks, planters, signage zones, and façade-facing space,
- separating commercial frontage from through-traffic,
- making each building easier to read from the player’s perspective.
4) USE SOFT COMPOUND BOUNDARIES, NOT HARD MAZE WALLS
The problem is not lack of walls only — it is lack of readable spatial structure.

Use light boundary language where appropriate:
- low fences,
- railings,
- stone edging,
- hedges,
- planter lines,
- curb transitions,
- lamp-lined edges,
- gate-like entries,
- small retaining walls,
- pavement borders.
Do not trap the player.
Do not over-enclose everything.
All compounds must remain visually open and playable.

The result should feel like:
- “this is the Namsan destination,”
- “this is the station/promenade district,”
- “this is the amusement destination,”
- “this is the shop/commercial frontage.”
At first glance, the player should immediately understand where to go.
5) PRESERVE THE NORTH / TRADITIONAL DISTRICT
The northern historical district is already mostly approved.

Do not redesign it.

Only allow minimal repair if needed for path continuity near the central transition.

Preserve:
- palace composition,
- academy / hanok identity,
- traditional path language,
- natural forest framing.
6) IMPROVE PLAYER WAYFINDING
Besides visual cleanup, improve navigation readability.

Add subtle wayfinding support through:
- clearer path hierarchy,
- more obvious entrances,
- better sightlines,
- cleaner open/closed spatial edges,
- stronger plaza-to-path relationships.
If helpful, add a few tasteful signposts, landmark approach markers, or gateway moments — but do not clutter.

The player should no longer feel:
- “everything is mixed together,”
- “I don’t know which place is which,”
- “I don’t know where I’m supposed to walk.”
7) GAMEPLAY & TECHNICAL SAFETY
All polish must preserve:
- existing world structure,
- approved buildings and landmark identities,
- player navigation,
- Juni scale and animation,
- collision correctness,
- camera flow,
- mobile landscape mode,
- existing performance targets.
Do not introduce collision traps with fences or boundaries.
Do not block key access routes.
Do not create fake entrances that are not traversable.
8) DELIVERABLES
Provide the following:
1. FINAL_MAP_V4_FULL_OVERVIEW.png
   - full world overview from the actual game.
2. READABILITY_BEFORE_AFTER.png
   - side-by-side comparison showing:
   - path fixes in the blue-circle areas,
   - improved compound separation in the southern red-zone area.
3. SOUTHERN_DISTRICT_READABILITY_BOARD.png
   - zoomed panels of:
   - Namsan zone,
   - station/promenade core,
   - amusement zone,
   - shop/commercial frontage.
4. A short gameplay video
   - walking from the central transition into the southern modern district,
   - proving that navigation now feels clearer and more intuitive.
5. A concise report
   Explain:
   - what path defects were fixed,
   - how each southern destination gained a clearer identity,
   - what boundary language was used,
   - whether any collisions / navigation routes were adjusted.
FINAL ACCEPTANCE CRITERIA
This polish is successful only if:
- the blue-circled path problems are visibly cleaned up,
- the southern red-marked district is less messy,
- each modern destination reads as its own place,
- the player can intuitively understand where to go,
- the map still feels open, beautiful, and playable,
- the world remains a coherent contrast between traditional Korea and modern Korea.
This is a focused readability and boundary polish — not a full redesign.
Complete the fixes, verify them in-engine, and stop for approval.