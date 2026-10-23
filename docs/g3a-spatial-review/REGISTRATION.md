# Revised building registration and site comparison

**Architecture accepted in principle; spatial approval withheld.** Existing masterplan4352×4864, original candidate, original native artwork and protected checkpoints remain unchanged. `registration-refined` is a separate engineering comparison. It does not authorize the land, zoning or path amendments below.

## Bakery: preserve the network before allocating a site

Both options use the same unchanged905×763 native image and875×442 contact footprint. No resizing, rotation, recoloring or regenerated facade. The comparison board shows geometry, not concept art; [native screenshots](README.md#actual-native-phaser-placement-screenshots) show the actual engine.

| | W0: existing waterfront proposal | Q1: southwest quay alternative |
|---|---|---|
| Native image origin |(1353,3060) |(523,3990) |
| Contact footprint `(x,y,w,depth)` |(1380,3370,875,442) |(550,4300,875,442) |
| Threshold |(1814,3840) |(984,4770) |
| Approved contact-route intersections |**5:** urban-avenue, island-arrival, harbor-link, promenade, market-waterfront-shortcut |**0** |
| Visual-envelope route intersections |Also includes leisure-access, leisure-garden-loop and tower-approach |**0**, using the same conservative full visual envelope |
| Carousel envelope conflict |38×90px at(2220,3060); physical footprints do not intersect |**None** |
| Amusement access |Buried by part of the conservative bakery projection; main routes need diversion |Original leisure access, carousel and wheel stay fixed and clear |
| Land / network cost |Existing land, but five diversions and narrowed side corridors |Explicit new quay parcel **(460,3940,1120,908)**; no approved route diversion |
| New access |Previously proposed waterfront diversion |96px east access `(1490,3790)→(1490,4790)→(984,4790)`;64px entry to `(984,4770)` |
| Pacing |Previous checked bakery→bridge route28.8s after diversion; not final pacing approval |New entrance spur1526px = **25.43s walk /15.26s run**, before onward network travel |
| Decision |**FAIL / retire as preferred location** |**PASS route separation; FAIL final readiness** until land, pacing and composition are approved |

The quay parcel covers1,016,960px², with44,800px² overlapping existing mainland; **972,160px² is additional land (about4.59% of the current world canvas)**. It stays inside the existing canvas but is a substantial site amendment, not existing available land. This is disclosed rather than silently written into the approved plan. It does not move or occupy the carousel, ferry terminal, station or Jeju bridge/island reservation.

The candidate opens only reserved public paths on the added parcel. Unfinished gray terrain is not presented as a premium park or accepted walkable empty grass. There is no proposed ferry/rail gameplay. The long access, dead-end destination character, shoreline shape and future public-realm design remain unresolved; this comparison does not invent activities or scenery to claim the walk is engaging.

**Recommendation:** reject W0. Review Q1 only if a quay land allocation and its travel cost are acceptable. Otherwise leave the bakery unallocated in the world while preserving its approved native asset; do not shrink it or force the five main-route diversions. No bakery site has been granted final approval by this work.

A conservative10px-grid screen checked23,504 contact origins on approved land, with16px shore inset, full905×763 visual rectangles excluding protected building/facade/native-north rectangles and all existing path widths; no clean site passed. [Method and limits](site-scan.json). Rectangular context/transparent areas make this conservative: it is **not** proof that no other composition could work under different explicit easements.

## Maru: validate land, the visible door and Namsan access

| Item | Original proposal | New comparison |
|---|---|---|
| Contact footprint |(220,2910,421,210) |(180,3120,421,210) |
| Native image envelope |(220,2608,421,512) |(180,2818,421,512) |
| Retail-street visual overlap |21,888px² of the conservative envelope |**0**; roof begins64px below the retained128px street corridor |
| Namsan access |Blocks western tower-approach loop |Only the western scenic loop is proposed for amendment; main eastern approach and lookout stay fixed |
| Entry |Source landmark `(1288,770)` / world `(428,3133)` points at merchandise window |Existing glass door centre at source `(1226,770)` / world **(326,3343)** |

The native image moves **(−40,+210)**. Its old landmark would become `(388,3343)`; the candidate corrects that marker a further62px west to the visible glass door. **The door artwork does not move within its source image.** Original source pixels, original proposal and approved prototype's metadata remain recoverable and unchanged. This is a documented candidate interaction/approach correction, not a silent protected station entrance change.

Contact is entirely inside the existing mainland. It straddles the western Namsan zone edge on partly unassigned land; explicit public-land/park-gateway allocation is still needed. The20px west shore margin is **not a public passage**. Public circulation uses the east and front.

Retain the main100px Namsan approach through `(2048,3260)→(1800,3260)→(1460,3260)→(950,3280)`. Replace only its western loop `(950,3280)→(540,3140)→(500,2920)→(750,2800)` with **`(950,3280)→(700,3140)→(700,2920)→(750,2800)`**, retaining100px width. East path centre700 is99px from Maru's native envelope edge601; the100px reservation leaves49px between the envelope and path edge.

New80px front access: **`(700,3140)→(700,3380)→(326,3380)→(326,3343)`**. The revised visual envelope does not cover the unchanged retail street. The90px contact gap between Maru's south face3330 and market's north face3420 accommodates the80px proposal; the checked foot-centre field at x560 spans y3356–3394 (39px). At centre y3380, Juni's49px visible width leaves nominal25.5px/15.5px to those two contact lines. The future market roof/side elevations and park-gateway composition still need artistic review.

Conservative glass-door clear opening, identified by direct native inspection: crop-local **x112–180, width68px**. Juni's49px maximum silhouette leaves9.5px nominal per side. The exact candidate threshold `(326,3343)` is walkable and reached with real keyboard input. The centre-position field at that threshold is37px wide, distinct from the68px visual doorway. This confirms access to the existing front door, **not an implemented enterable interior** or final accessibility certification. [Original-resolution door crop](maru-door-source-native.png).

## Retained registrations, easements and station

These placements do not change in the comparison:

| Building | Image origin / native envelope | Contact footprint | Threshold / approach |
|---|---|---|---|
| Cafe |(510,2035),415×556 |(510,2380,415,210) |Native(717,2605); retained public node(700,2690) |
| Bookshop |(980,2070),330×521 |(980,2380,330,210) |Native(1128,2605); retained shared node(1350,2690) |
| Learning |(1310,2030),300×561 |(1310,2380,300,210) |Native(1418,2605); retained shared node(1350,2690) |
| Station body/envelope |(2313,2196),645×453 |**(2322.5,2380,555,210)** |**(2598.5,2610)** |

Cafe415px contact width exceeds its390px slot by **25px east**. The remaining55px recess is non-public service space, not a premium public alley. Bookshop/learning share630px of the720px books allocation and retain their source party wall.

All three retail facade-height easements against the500px reserve at y2090–2590 remain explicit:

| Building | Native height | Total excess | North / south projection | Intrusion into transition zone ending2080 |
|---|---|---|---|---|
| Cafe |556 |56 |55 /1 |45 |
| Bookshop |521 |21 |20 /1 |10 |
| Learning |561 |61 |60 /1 |50 |

No historic northern geometry changes. These are requests for visual easements, not automatic approvals based on walkability. Exposed source-context cuts, side walls and rooftop vegetation ownership remain unfinished modular-art issues.

Station logical anchor **(2238.5,2180)**, collider and threshold remain protected. Explicit pivot **(0.5,0)** yields full-source raster origin **(2238,2180)**; cropped body anchor2313.5 minus0.5 gives2313. Canopy and corrected planters retain the same convention, native art, placements and depth sorting. The pivot is **not** the blur cause; no contrary evidence was found.

Station aisle remains89px; Juni49px leaves20px each side at the protected centreline. Source-aligned forecourt/tactile/crosswalk and corrected planters are untouched. The conservative station projection still overhangs its facade reserve7px west/78px east/59px south; canopy envelope overlaps platform1 by `(2920,2350,38,299)`. This existing platform/composition issue is **OPEN**, not solved by approving pixel registration.

## Verification and decision boundary

[Seven exact centreline checks](spatial-validation.json) include Maru front, Namsan loop, quay/door, main avenue, amusement access, Jeju arrival and protected station threshold. Every endpoint is checked with continuous logical collision plus the actual mask; segments use≤1px samples rather than a near-goal substitute. [Real WASD/Shift traversal](traversal.json) reaches the quay, Maru and station thresholds. No teleports or QA movement overrides are used. [Native readback](native-pixel-proof.json) verifies17 foreground regions and the corrected Canvas ground against source pixels; camera phase/native scale/nearest remain intact.

**Engineering reachability is not visual or pedestrian acceptance.** Full spatial readiness is FAIL pending human decisions on Q1 land/pacing (or bakery deferral), Maru allocation/door marker/local-loop amendment, retail easements and station/platform composition. WebGL hardware performance is unresolved and physical Android/iPhone are NOT TESTED. Source softness remains documented separately. G3-B is blocked; no approved plan overwrite, main merge, deployment or protected checkpoint rewrite.
