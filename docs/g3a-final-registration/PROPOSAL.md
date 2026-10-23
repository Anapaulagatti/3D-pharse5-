# Final individual-building registration proposal — approval requested

**Candidate only.** Rendering corrections are provisionally accepted technically. Individual world registration, planning amendments and final visual acceptance are not approved. The4352×4864 canvas, approved masterplan and intact3184×1214 district remain unchanged. This review consolidates the existing candidate; it introduces no new placement or artwork.

[Native review and evidence](README.md) · [Spatial overlays](../gate3a-corrections/CURRENT_VS_PROPOSED.png) · [Footprint comparison](../gate3a-corrections/FOOTPRINT_COMPARISON.png) · [Exact candidate JSON](../../assets-src/gate3/registration/proposal-v1.json) · [Existing playable candidate with corrected renderer](../gate3a-pixel-audit/G3A_PIXEL_CRISP_REVIEW.zip)

## Exact native registration

Coordinates are world pixels. Contact footprint notation is `(x, y, width, depth)`, with half-open right/bottom edges. Image envelopes include source-owned context; they are not ground contact dimensions. All art remains scale1. Thresholds are distinct from public approach nodes.

| Building | Raster origin | Native image envelope | Contact footprint | Native threshold |
|---|---|---|---|---|
| cafe | (510, 2035) | 415×556 | (510, 2380, 415, 210) | (717, 2605) |
| bookshop | (980, 2070) | 330×521 | (980, 2380, 330, 210) | (1128, 2605) |
| learning | (1310, 2030) | 300×561 | (1310, 2380, 300, 210) | (1418, 2605) |
| convenience | (220, 2608) | 421×512 | (220, 2910, 421, 210) | (428, 3133) |
| bakery | (1353, 3060) | 905×763 | (1380, 3370, 875, 442) | (1814, 3840) |
| station | (2313, 2196) | 645×453 | (2322.5, 2380, 555, 210) | (2598.5, 2610) |

The cafe, bookshop and learning thresholds connect to retained public approach nodes `(700,2690)` for cafe and `(1350,2690)` for bookshop/learning. The source bookshop/learning party wall remains paired. Their combined630px contact width uses the existing720px books reservation. Convenience and bakery plots are **new allocations proposed on unassigned land**, not existing protected reservations.

## Station pivot policy and entrance

Protected full-source logical anchor **(2238.5,2180)**; explicit source pivot **(0.5,0)**; resulting full-source raster edge **(2238,2180)**. The declared−0.5px raster delta from the historical literal source-edge interpretation requires human registration approval. The logical anchor, contact footprint **(2322.5,2380,555,210)** and threshold **(2598.5,2610)** are unchanged. Do not round these protected planning/collision coordinates.

Cropped station source anchor `(2313.5,2196)` minus pivot gives integer raster `(2313,2196)`. Canopy raster `(2884,2213)`, left planter `(2319,2608)`, right planter `(2682,2612)` and forecourt patch `(2274,2603)` use the same declared phase convention. Body support depth2590, canopy2649 and planters2691 remain independent for occlusion. The original civic public approach `(2570,2690)` remains distinct from the protected native threshold; its entrance plaza `(2290,2610,700,160)` provides the shared connection. Source columns84/360 have pixel centres2322.5/2598.5, aligning with the logical collision edge/entrance axis.

The protected source aisle maps to **89px clear width** at candidate x2554–2643; Juni's49px maximum visible width leaves20px per side on its2598.5 centreline. No planter, tactile paving or crosswalk is moved. Source readback proves four station-owned body/canopy/planter regions exact. **The0.5px pivot was not a blur cause.** See [phase diagram](../gate3a-corrections/PIXEL_PHASE_AND_COLLISION.png), [current native station evidence](../gate3a-pixel-audit/after-auto-station-pivot-backing.png) and [pixel proof](../gate3a-pixel-audit/pixel-proof.json).

## Bakery placement and pedestrian connections

Bakery contact plot **(1380,3370,875,442)** stays inside waterfront zone `(330,3360,2700,520)`. Native image envelope905×763 starts `(1353,3060)`; original442px collision depth is retained. Door approach `(1814,3840)` connects to the proposed local promenade at y3900. Ferry terminal and bridge positions stay unchanged.

The plot intersects no approved building contact footprint, but requires amendments to **urban-avenue, island-arrival, harbor-link, promenade, market-waterfront-shortcut**. North approach plaza y3308 feeds60px pedestrian side links. Market gap80px and ferry gap75px leave15.5/13px per side around Juni on their midlines; the60px link reservation itself leaves5.5px per side. These are pedestrian links, not a176px vehicular avenue. The96px promenade diversion returns to existing y3790; the64px bakery entry connects y3900 to3840. Accessibility, road cross-sections and public-realm quality remain review items.

| Proposed route | Exact centreline points | Width px |
|---|---|---|
| retail-front | (470, 2690) → (1820, 2690) → (2048, 2690) | 112 |
| convenience-access | (760, 3140) → (428, 3140) → (428, 3133) | 80 |
| namsan-west-bypass | (950, 3280) → (760, 3140) → (760, 2920) → (750, 2800) | 80 |
| avenue-diversion | (2048, 3260) → (2048, 3308) → (1340, 3308) → (1340, 3900) | 60 |
| east-bakery-bridge-link | (2048, 3308) → (2292, 3308) → (2292, 3480) → (3160, 3480) | 60 |
| east-bakery-coast-link | (2292, 3480) → (2292, 3812) → (2310, 3900) | 60 |
| promenade-local-diversion | (1280, 3790) → (1280, 3900) → (2310, 3900) → (2310, 3790) → (2900, 3790) | 96 |
| bakery-entry | (1814, 3900) → (1814, 3840) | 64 |

These are candidate engineering routes only; none is written into the approved masterplan. Existing static route checks and recorded keyboard traversal are [linked below](#navigation-evidence-and-limits).

## Conflicts requiring an explicit planning decision

| Item | Exact conflict | Proposed decision / unresolved consequence |
|---|---|---|
| Cafe width |415px contact versus390px slot;25px east extension |Approve the25px extension; remaining55px recess is non-public/service space, not a public alley. Missing side treatment remains unfinished. |
| Retail visual reserve |500px-high reserve at y2090–2590; native heights556/521/561 |Cafe/bookshop/learning project55/20/60px north and1px south, totals56/21/61px. They intrude45/10/50px into the transition zone ending2080. Approve visual easements without moving historical buildings/geometry. |
| Convenience |New421×210 contact plot140px west of tower zone;60px mainland edge clearance |Approve unassigned western Namsan-approach allocation and80px bypass. Southwest Namsan/tower destination remains fixed; park gateway zoning needs a local amendment. |
| Bakery routes / public land |New875×442 waterfront allocation intersects five named planning paths |Approve the allocation and exact pedestrian diversion concept above, subject to final road/public-realm design. No silent plan change. |
| Bakery / carousel projection |Visual envelope overlap **(2220,3060,38,90)**; contact footprints do not intersect |Unresolved depth/composition conflict. Do not move the carousel or claim it resolved; require a focused visibility/depth decision before affected production art. |
| Station / platforms |Conservative station envelope x2313–2958 exceeds civic reserve x2320–2880 by7px west/78px east and reaches59px beyond its y2590 front edge. Separate canopy envelope overlaps platform1 by `(2920,2350,38,299)` |Retain logical station footprint/anchor, review platform circulation, independent canopy depth and final railway composition. No operational railway implemented. |
| Extracted facade edges |Exposed party-wall ends, rooftop vegetation ownership and retained ground-context cuts |Registration proof is not finished modular world art. Missing side elevations and intentional ground transitions require separate production work after authorization. |

No proposed correction relocates the protected north, southwest Namsan, southeast amusement park, Jeju, bridge or ferry terminal. Source softness is separately documented in the [rendering diagnosis](../gate3a-pixel-audit/REPORT.md); it cannot be removed through registration approval or sharpening.

## Navigation evidence and limits

The existing [six-route static checks](../gate3a-corrections/static-validation.json) use4px BFS,3px safety inset and1px segment verification at60px/s. These are traversability checks, not final exploration-pacing approval:

| Route | Checked length px | Walk time s |
|---|---|---|
| station-threshold | 152 | 2.53 |
| bakery-entry | 56 | 0.93 |
| retail-to-station | 1544 | 25.73 |
| waterfront-bypass | 1308 | 21.80 |
| bakery-to-bridge | 1728 | 28.80 |
| convenience-entry | 144 | 2.40 |

Actual recorded traversal: [station approach](../gate3a-corrections/STATION_APPROACH.mp4), [retail to station](../gate3a-corrections/RETAIL_TO_STATION.mp4), [bakery to bridge](../gate3a-corrections/BAKERY_TO_BRIDGE.mp4). These recordings predate the fidelity-only renderer correction; geometry, collision and controls remain unchanged. Current [packaged WASD/scenic checks](../gate3a-pixel-audit/package-smoke.json) exercise the corrected renderer. Video is not pixel-fidelity evidence.

## Acceptance boundaries

- Rendering fix: **PROVISIONALLY ACCEPTED by the user**, retained unchanged. Native sampled pixels now match approved source in both renderers; successful tests do not establish artistic approval.
- Registration / planning amendments / final composition: **PENDING HUMAN APPROVAL**. Bakery-carousel projection and station-platform composition remain explicit conditions, not resolved issues.
- Source-art softness: **OPEN**. No sharpening, upscaling, recoloring or regeneration performed.
- WebGL performance: **UNRESOLVED**. Earlier desktop SwiftShader warm stationary interval p95≈28ms; culling reduced submissions but established no FPS gain. Latest renderer correction was not a new controlled GPU benchmark. No hardware GPU completion timing or mobile acceptance is inferred. [Detailed measurements and limits](../gate3a-corrections/PERFORMANCE.md).
- Android Chrome / iPhone Safari physical acceptance: **NOT TESTED**. [Existing device checklist and report-export workflow](../gate3a-corrections/DEVICE_CHECKLIST.md) retained.
- G3-B mass production: **BLOCKED**. Approval of registration must not be interpreted as automatic authorization to begin G3-B.

**Decision requested: approve the individual-building registrations, station pixel-centre convention and listed localized planning amendments, or identify changes/conditions. No masterplan amendment, G3-B production, merge or deployment has been executed.**
