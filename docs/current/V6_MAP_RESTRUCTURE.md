# KOREAN ARENA — V6 FINAL MAP RESTRUCTURE
## Match the Approved Reference Image — Execute, Don't Just Polish

**Repository:** `Anapaulagatti/3D-pharse5-`  
**Branch:** `rebuild/pixel-social-rpg-v3`

**ROLE:** Senior Pixel RPG World Director, Urban Level Designer and Phaser Engineer.

## MISSION

The attached reference image represents the layout I want.

**Reorganize the ACTUAL playable Phaser world to closely match its spatial composition. This is a real layout reconstruction, NOT another decorative polish pass.**

Previous V4 changes added fences and pavement but failed to solve the underlying problem: modern landmarks remain crowded and poorly organized.

This time, **MOVE and REPOSITION buildings, attractions, routes and compounds where necessary**.

Do not claim success by merely adding more decorations.

## 1. MATCH THE REFERENCE LAYOUT

Preserve the existing premium pixel-art quality and approved landmarks.

Use the attached image as the visual layout target:

- **NORTH:** Keep the existing historical palace and hanok neighborhood substantially unchanged.
- **SOUTHWEST:** Namsan Tower inside a clearly enclosed, landscaped hillside park with winding nature trails.
- **SOUTH CENTER:** Modern transit district featuring the train station, organized platforms, shops, public plaza and coastal promenade.
- **SOUTHEAST:** Self-contained entertainment park with Ferris wheel, carousel, entrance gate, internal paths and landscaped boundaries.
- **WATERFRONT:** Continuous seafront promenade with a clear public ferry terminal.
- **JEJU:** Distinct island destination with natural trails, basalt formations, traditional structures, lookout and accessible ferry arrival.

The final full-map silhouette and zoning should be immediately recognizable from the reference.

Do not copy the reference image as a flat background. Reconstruct its composition using editable source assets, tilemaps and properly positioned Phaser game objects.

## 2. FIX THE MODERN DISTRICT DECISIVELY

The southern area must no longer look like a pile of buildings.

Mandatory changes:

1. Physically redistribute crowded landmarks.
2. Establish independent compound boundaries and entrances.
3. Create landscaped buffers between destinations.
4. Give the station a properly organized transit forecourt.
5. Give the amusement park a recognizable enclosed campus.
6. Give Namsan its own hillside park and arrival sequence.
7. Separate pedestrian streets, rail infrastructure and coastal walkways.
8. Remove leftover awkward paving and unnecessary clutter.

**Do not keep the old positions simply because they already have coordinates or colliders.**

Update those systems to match the improved layout.

## 3. CLEAR MODERN URBAN DESIGN

Use a coherent contemporary Korean material language:

- Clean concrete and engineered-stone plazas.
- Modern paving, sidewalks and curbs.
- Steel/glass station architecture.
- Organized rail platforms and crossings.
- Metal railings, landscaped planters and modern lighting.
- Clearly defined pedestrian boulevards and public spaces.

Maintain the contrast:

**Traditional Korea = wood, giwa roofs, stone courtyards, organic historical paths.**

**Modern Korea = glass, steel, concrete, organized streets, transit and leisure infrastructure.**

Modern compounds must have clear footprints without becoming closed mazes.

## 4. PLAYER NAVIGATION MUST BE OBVIOUS

Create one strong main pedestrian route from the historical district to the modern civic plaza.

From there, provide clearly readable branches toward:

- Namsan park.
- Transit station and waterfront.
- Amusement park.
- Ferry terminal and Jeju.

Every landmark needs a visible entrance, approach space and useful route.

No blocked doors, confusing intersections, unnecessary detours or endless empty walking.

Keep a fictional Korean travel-world structure: distant real-world destinations are thematic locations, not geographically accurate neighbors.

## 5. MANDATORY SKILLS AND SAFETY

Read `AGENTS.md`, `docs/ART_SKILL_REGISTRY.md`, existing world reports and the approved asset manifests.

Reuse the verified Agent Sprite Forge / Phaser / Tiled workflow.

Preserve:

- Juni's approved appearance and 144 animation frames.
- Original landmark artwork wherever usable.
- Mobile landscape MOBA-style joystick and action controls.
- Historical district identity.
- Jeju's existing cultural details.
- The functional learning activities.

Create a recoverable Git checkpoint before changing spatial layouts.

No paid API calls, main-branch merge, public deployment or changes to the separate Korean Arena application.

## 6. IMPLEMENT AND VERIFY

Work in this order:

**A.** Compare the existing map with the attached reference and produce a relocation plan.

**B.** Reposition landmarks and rebuild southern district boundaries, routes and landscape buffers.

**C.** Update tilemaps, object coordinates, entrances, colliders, navigation and camera bounds.

**D.** Test real player traversal throughout all five destinations, including ferry access and mobile joystick input.

**E.** Produce final review evidence.

### REQUIRED DELIVERABLES

- `V6_FULL_MAP_OVERVIEW.png` — entire actual Phaser world.
- `V6_REFERENCE_COMPARISON.png` — reference versus implemented layout at matching proportions.
- `V6_BEFORE_AFTER.png` — proves buildings and districts were actually repositioned.
- `V6_NAVIGATION_MAP.png` — main roads, branches, entrances and ferry routes.
- Real Phaser gameplay walkthrough covering all major districts.
- Playable ZIP.
- Build, collision, navigation, mobile and performance test results.
- Git commit and recovery checkpoint.

Export a smaller browser-friendly overview PNG as well.

## NON-NEGOTIABLE ACCEPTANCE TEST

The work FAILS if:

- Modern buildings are still crowded in the central strip.
- The four southern destinations remain visually merged.
- The only improvements are new fences, paving or flowerbeds.
- The final world does not resemble the approved reference composition.
- Any district becomes unreachable or gameplay systems break.
- The overview is concept art instead of actual Phaser output.

The work PASSES only when the full map clearly shows:

**Historical Palace ABOVE → Namsan Park LEFT → Modern Transit CENTER → Entertainment Park RIGHT → Waterfront BELOW → Jeju Island BEYOND.**

**Execute the actual map restructuring now. Do not stop at suggestions or mockups.**

Commit and push the verified playable result to the development branch, provide the evidence and STOP for my final visual approval.