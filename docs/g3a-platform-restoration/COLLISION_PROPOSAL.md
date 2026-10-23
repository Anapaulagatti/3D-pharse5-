# Collision ownership — proposal only; scenery frozen

## Measured cause

The remaining blocked strip is world **[2950,2626,8,129]**, matching source **[3176,713,8,129]** in `public/assets/gate2/district-planter-repair/walk.png`, translated by(-226,+1913). Its eight columns are closed in both BEFORE and current restored fields.

`tools/gate25_reconstruction_assets.py` explicitly closes the last8 source columns with `wd.rectangle((W-8,0,W-1,H-1),fill=0)`. Later refinement/planter masks inherit that border. This source-image safety border is not itself a station wall, canopy support or platform reservation. The visible tree/pot, railing and curb still require independent collision ownership; identifying the border does **not** establish that the whole strip is traversable.

The original canopy envelope intersects the fixed platform reservation at[2920,2350,38,299]. A tall roof projection is allowable visual occlusion where its physical supports are respected. Its whole sprite rectangle must not be used as a solid wall. Conversely, the original railing and tree cannot be ignored merely because their pixels belong to a foreground sprite. The rejected support/base proposal is no longer active and must not be cited as validated geometry.

Actual ordinary keyboard A movement from the existing platform spawn(2980,2690) reaches(2958,2690) and stops for the remaining samples of a3-second input. No teleport, collision override or successful-transfer claim is used. The current runtime samples the player's foot point; this is not proof that the full49px visible Juni width fits a corridor.

## Preferred minimal nonvisual correction, subject to review

Create a **separate derived collision-owner layer**, retaining all source PNGs and approved masks. Confine initial review to the8×129 border: remove only the generic image-edge guard contribution; reconstruct the union of real planter/tree-pot feet, rail/support feet, curb/road limits and the protected station collider from independently documented native geometry. Pixels belonging to a genuine obstacle remain blocked even if also covered by the generic border guard. The canonical forecourt mask west ofx2950 must remain untouched.

This is a proposed ownership operation, **not authorization to clear the entire8×129 rectangle**. Document the exact resulting open intervals and body/visual clearances before applying it. The southern paving sliver below the tree is visibly narrow and adjacent to the curb; a foot-point-only path there must not be presented as a safe public passage. There is currently no certified full-width aperture in the retained scenery.

Before accepting any candidate: verify a connected route from the station entrance(2598.5,2610) through the existing public plaza to the fixed platform, exclude railing/pot/curb penetration, check Juni at native scale in motion, test both directions and diagonal approaches, and show native collision overlays. If recovering border ownership leaves insufficient clearance, retain the block. Do not remove the railing, move vegetation, add paving, or change source art to force success.

## Alternative requiring a separate circulation decision

Use the existing southern public approach to the platform as the access route, rather than promise a direct passage through the canopy/garden edge. First audit its connection to the approved public road/crossing network and its full walking clearance. A detour around the strip's southern endpoint at y2755 is **not automatically safe**: it reaches the curb/road environment. A new road crossing or route reservation requires explicit planning review and may fail the unchanged-scenery constraint. No route is added to the accepted plan here.

**Remaining decision:** authorize a bounded collision-only ownership candidate and its movement/clearance validation, or retain local station-platform production blocked pending an approved alternative public route. No new visual connector is proposed or implemented. G3-B remains blocked.
