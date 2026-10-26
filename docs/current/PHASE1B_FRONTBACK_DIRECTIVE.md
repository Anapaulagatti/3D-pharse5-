# PHASE 1B — TARGETED ANIMATION CORRECTION
# FRONT/BACK WALK + RUN MUST FOLLOW JUNI AS THE MOTION GOLD STANDARD

The new characters look visually good now, but the remaining issue is animation quality.

Do NOT redesign the characters.
Do NOT change their identities, outfits, colors, faces or hairstyles.
Do NOT rebuild the roster system.
Do NOT touch the map, world, NPCs, UI, selection flow or working side-view animations unless required for atlas consistency.

Your task now is ONLY to correct the FRONT and BACK walk/run animations for:
- Haneul
- Bomi
- Minjun

Juni is the approved gold standard for motion.

## CORE DIRECTIVE

Use Juni as the animation reference model for:
- walk front
- walk back
- run front
- run back

for all new characters.

This means the new characters must inherit Juni’s approved motion logic, including:

1. frame-to-frame pose progression
2. contact and passing positions
3. alternating leg rhythm
4. arm swing timing
5. body weight shift
6. stride readability
7. loop closure quality
8. front-facing and back-facing silhouette behavior
9. native foot contact consistency
10. overall movement clarity at gameplay speed

Do NOT simply make the characters “similar”.
Instead, map the new characters’ front/back walk/run frames to Juni’s approved animation structure as closely as possible.

## REQUIRED FRAME MATCHING

For each of the three characters:
- Haneul
- Bomi
- Minjun

rebuild these animation sets using Juni as the direct motion template:

### Walk
- front walk: 8 real frames
- back walk: 8 real frames

### Run
- front run: 8 real frames
- back run: 8 real frames

For each corresponding frame index, the motion phase should align with Juni.

Example:
- if Juni frame 1 is left-foot contact in front walk, then Haneul/Bomi/Minjun frame 1 must represent the same motion phase
- if Juni frame 4 is crossing/passing pose in back run, then the new character’s same frame index must reflect that equivalent body phase

The new characters should preserve their own clothing and silhouette, but the locomotion mechanics must follow Juni.

## IMPORTANT ART CONSTRAINTS

Keep each character’s identity intact:
- Haneul remains Haneul
- Bomi remains Bomi
- Minjun remains Minjun

Do NOT turn them into recolored Juni.
Do NOT copy Juni’s face or costume.
Only copy the approved locomotion structure and animation language.

The following must remain unique per character:
- face
- hair
- costume
- accessories
- silhouette details

But the following must match Juni’s motion standard:
- gait logic
- frame sequencing
- forward/backward readability
- step rhythm
- run energy
- foot planting
- loop smoothness

## SPECIFIC QUALITY FAILURES TO ELIMINATE

Reject and correct any frame sets showing:
- same leading leg repeated across multiple frames
- weak or unclear alternation
- mirrored or fake motion without true gait structure
- front walk looking like bobbing instead of stepping
- back walk lacking proper rear-leg rhythm
- run cycles that do not feel faster/more energetic than walk
- floating feet
- inconsistent foot anchors
- sudden body width changes
- accessory jitter or detached props
- broken knees/ankles
- front and back animations that do not read clearly at gameplay scale

## METHOD

1. Extract or inspect Juni’s approved front/back walk/run native cycles.
2. Build a motion breakdown for Juni:
   - contact
   - down
   - passing
   - up
   - repeat on alternate side
3. Re-author Haneul, Bomi and Minjun front/back walk/run so each cycle follows that exact motion structure.
4. Keep side-view animations only if already acceptable; only update them if needed for consistency.
5. Re-export atlases and validate them in Phaser at native scale.
6. Test at actual gameplay speed, not just sheet preview speed.

## REVIEW DELIVERABLES

Deliver the following for review:

1. Juni front/back walk/run reference sheet
2. Haneul corrected front/back walk/run sheet
3. Bomi corrected front/back walk/run sheet
4. Minjun corrected front/back walk/run sheet
5. Side-by-side comparison:
   - Juni vs Haneul
   - Juni vs Bomi
   - Juni vs Minjun
6. Gameplay GIF or video showing:
   - front walk comparison
   - back walk comparison
   - front run comparison
   - back run comparison
7. A short QA note explicitly confirming:
   - front walk matched to Juni structure
   - back walk matched to Juni structure
   - front run matched to Juni structure
   - back run matched to Juni structure

## PASS CONDITION

This task passes only if:
- all three new characters keep their own identity
- their front/back walk cycles clearly follow Juni’s approved gait logic
- their front/back run cycles clearly follow Juni’s approved gait logic
- animation quality is readable and consistent at real gameplay scale
- no regression occurs to Juni, the world, or the character-selection system

Stop after delivering the corrected front/back motion review.
Do not start Phase 2.
Do not expand scope.
Do not merge main or deploy.