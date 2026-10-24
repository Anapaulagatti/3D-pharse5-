# G3-D final alignment candidate — consolidated review

[Visual gallery](VISUAL_REVIEW.html) · [Native BEFORE/AFTER](VISUAL_REVIEW.md) · [Playable ZIP](G3D_FINAL_ALIGNMENT_REVIEW.zip) · [QA](QA.md) · [Measurements](measurements.json) · [Source ownership](SOURCE_OWNERSHIP.md).

One isolated candidate corrects the palace entrance, eastern entrance ownership, station background/canopy, three commercial rooftops and both mainland–Jeju bridge landings. This is **not final world artistic acceptance**. Historical source artwork, geometry/plans, Juni, original station canopy, corrected planters and canonical forecourt remain protected. No merge or public deployment.

## Implemented

- Main hall: measured old door/stair axis1921 versus approved2048. Derived native front shifts material phase127px without moving the royal roof/contact reservation. Plinth bottom790→750; central door/stair axis2048, actual threshold685. One112×94 portal ownership patch; one foundation course, no duplicate plinth. Real movement reaches the door.
- Eastern archive: source support reserve150px from wall, roof projection46px from wall eave, painted low-platform envelope approximately52px. Original architecture stays registered. Native stairs become ground; side lanterns/gardens remain foreground. Door2580,923 reached through existing southern gateway and20px internal corridor. This corridor remains inadequate for final public-space acceptance.
- Station: obsolete upper/side source background alpha retired; HVAC, rear railing, facade RGB and source pivot preserved. Original canopy retained with a small independent terminal roof cap on existing supports. No new platform connector or added support foot. Canonical forecourt/raw ground and both corrected planters remain exact.
- Retail: verified full native source recovers legitimate roof/terrace/flower silhouettes; unrelated background removed with explicit alpha. Cafe/bookshop/learning base positions and approved facade RGB/alpha remain exact.
- Bridge: two bounded derived abutment repairs and local shared-water ownership; original Jeju PNG and land/internal scenery remain protected. Existing near rails/posts are depth-sorted foreground with exact static native composition. Actual locomotion crossing uses real timber/deck ground, not the obsolete mainland-wall shortcut. Full stop/turn contact clearance remains FAIL, separately measured.

## Decisions still required

1. **Archive public clearance:**20px remains tight. ONE88px secondary gate proposal at2536,1040,88,25, axis2580 is shown only in an overlay; current wall/plan unchanged. No automatic architectural acceptance from successful movement.
2. **Station material boundary:** protected canonical asphalt at2274,2755,684,58 remains historically softer/different in phase. An isolated `aligned-road-proposal` candidate restores native asphalt material only within an explicit mask. It is **NOT ADOPTED**, requires human approval, and changes no road geometry. Paving/curb/tactile/marks outside mask exact.
3. **Station source completeness:** the existing right potted-tree crown is clipped at sourceX2958. Complete verified crown unavailable; protected pot/floor not repainted or covered. Station fully seamless appearance remains **FAIL**, even though canopy repair and runtime pixel readback pass.
4. **Bridge full stop/turn clearance:** actual crossing succeeds, but original stop poses produce13 sampled contact failures in the full route and6 in the separate bridge recording. A strict union of native stop/turn contacts finds no safe route inside the unchanged physical deck. See [strict contact proposal](../../assets-src/gate3/alignment-v1/strict-stop-turn-contact-proposal.json) and [actual failing coordinates](body-clearance.json). No invisible deck enlargement, bridge resize or Juni shrink. A reviewed local landing/stair clearance or animation/contact decision remains required.
5. Station8px collision strip2950,2626,8,129 remains CLOSED. No rejected90×36 connector; platform transfer is not claimed.
6. Inherited public-route failures, tower/retail and carousel/canonical-road projections remain open; Bakery required/unplaced, W0 rejected, Q1 land unallocated. Physical Android Chrome/iPhone Safari and hardware WebGL performance NOT TESTED.

Seven marked screenshots were unavailable and requested. Annotation-specific validation is NOT TESTED. Native pairs and source geometry are the available evidence; no claim that all reviewer marks have been closed.

## Review and reproduction

Extract ZIP, run `python3 start_review.py`, open printed private localhost URL. Main candidate defaults to `aligned-world`; protected-road proposal is explicitly separate. All ten original region links plus fifteen focused review entries are available. WASD/arrows, Shift run and mobile landscape joystick retained. No ferry/train gameplay added.

See [physical-device checklist/export](DEVICE_REVIEW.md). Chromium touch emulation and software WebGL are not actual phone/hardware evidence. Full authoring reproduction requires repository sources and `tools/g3df_*`; built-in host authoring outputs/prompts retained with exact masks. One source checkpoint and immutable artifact checkpoint retain this batch. **STOP for consolidated human visual/spatial review.**
