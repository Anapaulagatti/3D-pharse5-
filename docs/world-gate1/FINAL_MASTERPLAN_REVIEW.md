# Final Gate 1 planning review — 22 October 2026 (Asia/Saigon)

**Art direction: provisionally approved. Masterplan: pending final user approval. Gate 2: locked.** The approved Muneum street sample is the mandatory craftsmanship benchmark for **both** traditional and modern environments. This review changes planning and the actual Phaser graybox only; it does not generate production art.

## Review files

- [Revised planning board](MASTERPLAN_BOARD.png), [HTML board](masterplan-board.html).
- [Actual Phaser native overview, 4096 × 4608](GRAYBOX_NATIVE_4096x4608.png), [browser-sized overview](MASTERPLAN_REVIEW.png).
- Native gameplay: [Namsan southwest](NAMSAN_SW_NATIVE_1X.png), [amusement southeast](AMUSEMENT_SE_NATIVE_1X.png), [Jeju/ferry landing](FERRY_PIERS_NATIVE_1X.png), [bridge/waterfront](COAST_NATIVE_1X.png), [traditional north](NORTH_NATIVE_1X.png).
- [Full-sized building reservation with Juni, actual Phaser zoom1](BUILDING_SCALE_NATIVE_1X.png). Outlines are planning dimensions, not generated architecture.
- [Revised playable ZIP](WORLD_GATE1_PLAYABLE.zip): extract, run `python3 start.py`, open its printed URL. Regular entry has no teleport hook. Use Overview for the map; native walk view stays zoom1. `?qa&scale` is an evidence-only camera offset that frames the complete commercial elevation reserve while retaining Juni at native size.
- [Planning/source audit](source-and-navigation.json), [rendered route audit](rendered-route-audit.json), [browser QA](browser-qa.json), [package verification](package-verification.json), [QA summary](validation.json).

## Findings and corrections

| Check | Finding | Decision / actual correction |
|---|---|---|
| Namsan / amusement reversal | The previous revision's notes record an east hill / west leisure choice but no compelling navigation constraint. Reachability alone did not justify reversing the preferred composition. | Restore Namsan southwest and entertainment southeast. Redraw only their access routes and garden loop. The east precinct fits both original-sized attraction footprints; neither attraction is miniaturized. |
| Jeju location | The southeast island and its physical bridge are coherent. Mainland x160–3160; Jeju x3290–4010. The 130px water gap is crossed by a land-connected bridge strip x3040–3440, y3390–3570; main arrival centerline y3480. | Keep island, bridge, curved island garden route and observatory positions unchanged; label Jeju explicitly. |
| Ferry relationship | The terminal was on solid mainland but had no explicit boarding pier. Thus the intended ferry relationship was under-specified. | Add a mainland pier x2496–2624/y3940–4160 and Jeju landing x3210–3390/y4036–4164. Public access links join the promenade and island garden. The proposed water crossing is x2560→3240 at y4100, well south of the bridge; no boat, teleport, sailing or ferry interaction is claimed. |
| Traditional identity | Palace, archive, gate pavilion, hanok academy, tea courtyard, culture court and heritage transition are intact; no modern floor is required in that core. | Keep all historic buildings, boundaries, historic paths and heritage/transition zones byte-equivalent as geometry to prior plan ae5fe5f. Material/art direction remains historic. Muneum-level craftsmanship is a binding requirement; it is **not** claimed achieved by colored blocks. Gate 2 must prove it in the north sample. |
| Full-sized detailed buildings | Previous 210px ground footprints did not explicitly reserve the roughly 500px vertical extent needed for detailed commercial elevations. Final art could have overlapped the heritage belt if fitted without planning space. | Move the café/book/civic ground footprints, entrances and frontage lane 200px south; reserve three 500px-high elevations starting y2090, beyond the heritage garden end y2080. Café/book/civic widths remain 390/720/560px, with original 210px ground depths. Place transit on the east side of civic rather than conflicting with the restored leisure garden. |

## Scale contract

Juni's original 96×112 atlas and approximately 80px visible body are unchanged. The elevation reservations are 500px tall (6.25 body heights), with 100px door openings (1.25 body heights), 60px door width and one source pixel per world pixel at normal zoom1. Commercial widths represent 4.875, 9 and 7 body heights, respectively; they are façade/block widths, not miniature icons.

The existing source footage/PNG of Muneum is a quality and scale reference, not a texture pasted into this new world. Pale 500px outlines and 100px door outlines in the actual graybox demonstrate space for future architecture. They have no decorative texture and do not masquerade as finished façades. Floor collider rectangles are deliberately separate from elevation envelopes.

Full-size visual reservations y2090–2590 leave the traditional transition untouched. The lane centerline moves y2490→2690. The amusement attractions move into the southeast and 90px south to leave a readable buffer below that lane; their dimensions remain carousel 390×260 and wheel 400×280. Namsan's tower base is 240×240, enlarged from 200×240, in a wide southwest garden. Its final vertical silhouette, foliage, roof depth, sightlines and art occlusion still require the later sample/production gates. Do not solve a future fit issue by shrinking final artwork into tiny buildings on vacant grass; amend its reservation before integration.

These checks establish planning capacity and scale intent. They do not prove final façade detail or artistic finish before those assets exist. Premium historic north must retain tiled roofs, timber, warm stone, gateways and enclosed courtyard hierarchy while reaching Muneum's material richness and polish. Modern signage, glass and asphalt are confined to the appropriate southern zone.

## Validation and limits

The revised source audit asserts historic geometry unchanged, original Jeju/bridge land rectangles unchanged, requested southwest/southeast placement restored, commercial footprint dimensions preserved and 500px/100px scale reservations intact. It retains original-runtime/art/lockfile preservation checks and rejects old southern imports.

Navigation covers all 16 building approaches plus the two new ferry pier endpoints. Browser checks sample all 19 actual rendered route centerlines, including Phaser splines, and exercise continuous keyboard movement from the avenue to both revised precincts, across the existing bridge, onto the mainland pier and from Jeju's dock into its land. QA may set each route's starting position; subsequent movement uses real keys. Mobile uses CDP touch in landscape. No operational ferry route is included in walkability or represented as a successful gameplay feature.

All captures are actual Phaser canvases at DPR1; native exports and native crops retain their pixels. The board explicitly discloses its overview reduction. Desktop uses Chromium Canvas; landscape mobile is emulated, not a physical phone. Geometric reachability cannot approve architecture, materials, final occlusion or the complete width of rendered roads. The original app build retains its known large-chunk warning.

No full-world art generation, Gate 2, main merge or deployment. Final Gate 1 approval is still required.

**Do you approve this revised masterplan and Phaser graybox as the final Gate 1 plan before Gate 2?**
