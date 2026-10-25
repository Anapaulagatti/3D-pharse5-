# CODEX — FINAL LOCAL FIX: WESTERN HANOK + LOWER COURTYARD REPAIR

Repository: Anapaulagatti/3D-pharse5-
Branch: art-gate/gate3-full-world

## CONTEXT

Hanbit Station is already approved and locked.
The Jeju bridges are now approved visually and should remain unchanged.
This task is a strictly localized repair in the western side of the palace district.

Do not ask for additional screenshots.
Use the current latest approved world state in the branch and identify the target areas directly from the map.

---

## TASK SCOPE

Repair ONLY these two western palace-side defects:

### TARGET A — WESTERN HOUSE NEAR THE PALACE
This is the hanok-style building on the west / left side of the palace district.

#### Current issue
The roof silhouette looks cut off / truncated / visually incomplete, as if part of the upper roof mass was clipped away.
The building currently reads like a half-cut structure rather than a fully intentional hanok building.

#### Required fix
Reconstruct the building so it reads as a complete, natural, fully intentional structure in the Gate 1 art style.

Mandatory requirements:
1. Restore a complete roof silhouette with correct hanok proportions.
2. Ensure the eaves, ridge line, roof corners and wall mass feel whole and not abruptly cropped.
3. Preserve the current architectural language of the palace zone.
4. Keep the building aligned with surrounding paths, planting and adjacent structures.
5. Do not oversize or redesign it into a different type of building.
6. Make it look like it was always part of the map, not pasted or patched.

Do not merely paint over the cropped roof edge.
Rebuild the visible structure properly so the whole house reads correctly at gameplay scale and native 1:1 zoom.

---

### TARGET B — LOWER COURTYARD / GARDEN AREA DIRECTLY BELOW THAT HOUSE
This is the landscaped courtyard / enclosed garden zone directly beneath the western house.

#### Current issue
This lower area also looks visually cut off / incomplete.
The enclosure, garden composition, and path/border logic do not read as a clean finished space.

#### Required fix
Rebuild and finish this courtyard so it becomes a coherent, intentional sub-area.

Mandatory requirements:
1. Restore complete enclosure logic:
   - fence / low wall / planter edge / stone border must feel continuous and intentional.
2. Repair the internal composition:
   - garden bed, shrubs, small trees, rock placements, and path edges should feel balanced and complete.
3. Remove any cropped or abruptly terminated visual forms.
4. Ensure the left and right ends of the courtyard both resolve cleanly.
5. Match surrounding palace landscaping style and texture language.
6. Keep the area readable for future gameplay use, but do not convert it into a new gameplay system or redesign the district.

This repair should feel like finishing an incomplete garden/courtyard, not inventing a brand new biome.

---

## STYLE REQUIREMENTS

Use the same approved Gate 1 visual language:
- clean pixel-art readability
- natural hanok roof geometry
- coherent palace landscaping
- believable stone/path/garden relationships
- no collage look
- no cut-and-paste appearance
- no random asymmetry unless architecturally justified

The result must blend with:
- the palace complex
- nearby western hanok buildings
- adjacent paths and planting
- the already approved world aesthetic

---

## STRICT PRESERVATION RULES

Do NOT modify:
- Hanbit Station
- Jeju bridges
- Jeju island
- the main palace building
- approved roads
- approved commercial district
- unrelated landscape outside the two target zones
- Juni sprite or scale

Only edit the minimal necessary local area around:
- the western house
- the courtyard directly below it

No broad repainting of the whole palace district.
No global regeneration.
No accidental pixel drift outside the repair masks.

---

## TECHNICAL / SPATIAL REQUIREMENTS

1. Determine exact edit bounds before changing anything.
2. Preserve walkable routes and collision behavior unless a local visual fix absolutely requires a matching correction.
3. If collision changes are needed, keep them minimal and localized.
4. Ensure no new clipping or blocked movement is introduced near the repaired house or courtyard.
5. Preserve native pixel sharpness and approved texture quality.
6. No blurry fill, no repeated obvious patch texture, no seam lines.

---

## ACCEPTANCE CRITERIA

The task is only PASS if:

### For the western house
- the roof no longer looks cut off
- the building reads as a complete hanok
- the silhouette is clean and intentional
- no pasted or truncated architecture remains

### For the lower courtyard
- the area no longer looks chopped or unfinished
- the enclosure and garden read as a complete designed space
- the borders resolve cleanly on all sides
- the layout feels naturally integrated into the palace district

### For both
- surrounding approved art remains untouched
- no new artifacts are introduced
- the result looks native to the map

---

## REQUIRED DELIVERABLES

Provide:
1. Native 1:1 BEFORE / AFTER for the western house
2. Native 1:1 BEFORE / AFTER for the lower courtyard
3. One combined local-area screenshot showing both repairs together
4. Short QA note confirming:
   - no unrelated areas changed
   - no station changes
   - no Jeju bridge changes
   - no new movement/collision issue introduced
5. Updated playable ZIP
6. Checkpoint saved before stopping

Stop after this localized repair for final human review.
Do not merge main.
Do not deploy.

## FINAL HUMAN DIRECTIVE

This is a narrow cleanup pass only.

Fix the western house so its roof no longer looks cut off.
Fix the courtyard below so it no longer looks incomplete or chopped.

Preserve everything else.
Make both areas feel finished, elegant, and native to the Gate 1 world.