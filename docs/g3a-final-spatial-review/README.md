# Final G3-A decision packet

**Station forecourt: HUMAN APPROVED. Final world registration: WITHHELD. G3-B: BLOCKED.**

The native station floor accepted at `3739266d2acd88242bfc4cf58f770a2d7d4b87ca` is frozen. Subsequent station work must reuse [the canonical asset registry](../../assets-src/gate3/approved-station-forecourt.json). Its masks, native floor, source map, two chunks, shadows, architecture and collision have not been revised. Historical sources, screenshots and packages retain their original bytes and original review-time status; this approval supersedes only their forecourt-approval status.

The current in-engine review is `gate3-review.html?scene=registration-review&entry=station`. This manifest adopts the exact accepted ground chunk references without approving other placements. Use `entry=bakery`, `entry=convenience`, `entry=namsan` or `entry=retail` to inspect the existing spatial proposals. Default `world`, earlier comparison scenes and the approved masterplan remain unchanged. No new buildings, painting, terrain or collision was generated.

The preserved playable ZIP is an archive of the accepted restoration delivery, not a rebuilt package. In that ZIP use `scene=registration-forecourt` for the accepted floor plus Q1/Maru comparison, `scene=registration-refined` for the older ground comparison, and `scene=registration` for W0. The new `registration-review` identifier is available in the current repository build only.

## Decisions still required

| Decision | Exact proposal and conflict | Review choice / recommendation |
|---|---|---|
| Bakery site | W0 image origin `(1353,3060)`, native 905×763; contact `(1380,3370,875,442)`. Conflicts with five routes and carousel visual envelope 38×90. | Retire W0 as preferred. Do not divert the approved main/amusement routes to force it in. |
| Bakery Q1 alternative | Image `(523,3990)`, contact `(550,4300,875,442)`, threshold `(984,4770)`. No existing route or carousel overlap. Quay parcel `(460,3940,1120,908)` needs 972,160px² additional land, about 4.59% of world canvas. | **Recommend defer allocation** unless the additional quay land and long access are expressly accepted. Q1 is an alternative for review, not an approved placement. Preserve the native bakery asset; do not shrink it. |
| Maru location and park allocation | Contact `(180,3120,421,210)`; native envelope `(180,2818,421,512)`; visible glass-door threshold `(326,3343)`. Native image moves `(−40,+210)`; source artwork unchanged. Occupies partly unassigned western Namsan gateway land. | Approve or reject the land allocation together with the local scenic-loop and entrance-marker amendments below. Engineering reachability alone does not settle composition. |
| Maru / Namsan pedestrian amendment | Replace only west loop with `(950,3280)→(700,3140)→(700,2920)→(750,2800)`, width 100. Front connector `(700,3140)→(700,3380)→(326,3380)→(326,3343)`, width 80. Main eastern Namsan approach stays fixed. | Review as one local amendment; keep west 20px shore gap non-public. Preserve market/front circulation and reserve facade clearance before any neighboring production. |
| Cafe contact width | Cafe contact `(510,2380,415,210)` exceeds 390px slot by 25px east. Remaining 55px recess is service space. | Explicitly accept the 25px allocation easement or withhold the cafe registration. Do not label the residual space a public alley. |
| Retail facade-height easements | Against 500px reserve: cafe 556px high projects 55px north/1px south; bookshop 521 projects 20/1; learning 561 projects 60/1. Their visual envelopes enter the transition zone by 45/10/50px respectively. | Approve or reject each visual easement. Historic northern geometry remains protected; no implicit consent to overwrite it. Native buildings remain full size. |
| Station facade / platform relationship | Logical anchor `(2238.5,2180)`, pivot `(0.5,0)`, collider `(2322.5,2380,555,210)`, entry `(2598.5,2610)` stay fixed. Facade reserve overhang 7px west/78px east/59px south; canopy/platform 1 envelope overlap `(2920,2350,38,299)`. | Review the existing projection/platform composition separately. Forecourt approval does not authorize moving station, platforms or reservation edges. |

The protected carousel, ferry terminal, Jeju bridge, station and historic northern geometry remain in place under every review choice. No masterplan amendment has been silently applied.

## Pedestrian clearances and pacing

These are existing measured engineering results, not new physical-device or artistic certification. Travel uses 60px/s walk and 100px/s run; times exclude stops, acceleration and onward network travel.

| Route / clearance | Evidence and practical implication |
|---|---|
| Q1 new bakery access |1526px,25.43s walk /15.26s run **before onward travel**. Width 96px. Centre-position field at y 4500 is 46px. Long dead-end access/public-realm composition remain unresolved. |
| Maru front connector |651px,10.85s walk /6.51s run. Physical front contact gap 90px; tested centre field 39px. Width 80 is the reservation, not a claim of 80px collision-centre freedom. |
| Revised Namsan west loop |636.531px,10.61s walk /6.37s run. East reservation 100px;49px between Maru envelope and path edge. |
| Maru glass door |68px visible opening, Juni max silhouette 49px, nominal 9.5px per side. Centre-position field 37px. Interaction marker corrected from the merchandise window to the existing door; no enterable interior implemented. |
| Station approach |150px,2.5s walk /1.5s run. Accepted 89px aisle, Juni 49px,20px nominal each side. Existing collision and entrance preserved. |
| Main amusement access |452px,7.53s walk /4.52s run. Existing protected route retained. |
| Main avenue south |530px,8.83s walk /5.30s run. Existing protected route retained. |
| Island-arrival main connection |1112px,18.53s walk /11.12s run. Bridge/ferry reservation unchanged; ferry gameplay not implemented. |

All seven previous route centrelines passed actual logical-solid plus mask checks at≤1px intervals, including exact endpoints. Real keyboard traversal reached bakery, Maru and station thresholds. These checks do not prove corridor comfort, final facade composition or engagement on long walks. Retained lateral station boundary near `(2531,2734)` remains a collision constraint, not a new route opened by the floor restoration.

## Evidence for the decision

- [Site comparison diagram](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/05335a58900741a37c9704dd49e1ba2dd1da5679/docs/g3a-spatial-review/SITE_COMPARISON.png): technical geometry, not gameplay.
- [Q1 bakery native Phaser](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/05335a58900741a37c9704dd49e1ba2dd1da5679/docs/g3a-spatial-review/bakery-quay-1x.png) and [W0 native Phaser](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/05335a58900741a37c9704dd49e1ba2dd1da5679/docs/g3a-spatial-review/bakery-waterfront-1x.png).
- [Revised Maru native Phaser](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/05335a58900741a37c9704dd49e1ba2dd1da5679/docs/g3a-spatial-review/maru-revised-1x.png) and [Namsan approach](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/05335a58900741a37c9704dd49e1ba2dd1da5679/docs/g3a-spatial-review/namsan-access-1x.png).
- [Accepted station frontage with Juni](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/3739266d2acd88242bfc4cf58f770a2d7d4b87ca/docs/g3a-forecourt-restoration/station-with-juni-1x.png). Earlier station-ground images in the spatial packet are superseded visually by this approved frame.
- [Detailed registrations](../g3a-spatial-review/REGISTRATION.md), [route/clearance data](../g3a-spatial-review/spatial-validation.json), [actual traversal log](../g3a-spatial-review/traversal.json), [accepted forecourt evidence/package](../g3a-forecourt-restoration/README.md).

## Separate technical gates

| Item | Current status | Evidence needed |
|---|---|---|
| Forecourt visual acceptance | **HUMAN APPROVED** | Complete; no further art revision requested. |
| Native registration / collision / source protection | PASS technical | Current asset-lock verification and prior native readbacks. |
| Final bakery/Maru/circulation/easement decisions | **PENDING HUMAN REVIEW** | Explicit choices above; implement only authorized amendments. |
| WebGL hardware performance | **UNRESOLVED** | Controlled hardware GPU timing/session evidence; software/headless capture is insufficient. |
| Android Chrome / iPhone Safari physical validation | **NOT TESTED** | Real model, OS/browser/DPR, package hash, exported session JSON, recorded gameplay and defect report. [Existing checklist](../gate3a-corrections/DEVICE_CHECKLIST.md); Options → Export test report remains the handoff workflow. |
| Final G3-A / G3-B authorization | **WITHHELD / BLOCKED** | Explicit human decision; forecourt acceptance does not unlock mass production. |

Stop at this decision packet. No main merge or deployment.

## Recover the accepted baseline

Approved checkpoint: `checkpoint/g3a-station-forecourt-approved-20261023`. It retains the exact accepted pixels and the current adoption record. To inspect without overwriting a working tree: `git worktree add --detach /tmp/hanbit-approved checkpoint/g3a-station-forecourt-approved-20261023`. The earlier candidate and all earlier approved tags remain unchanged.
