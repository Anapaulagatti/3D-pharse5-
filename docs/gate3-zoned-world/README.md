# G3-D coordinated zoning / environment correction — consolidated review

The world is a **human review candidate, not artistically accepted**. [Playable ZIP](G3D_ZONED_WORLD_REVIEW.zip) · [Direct visual gallery](VISUAL_REVIEW.md) · [HTML gallery inside ZIP](VISUAL_REVIEW.html) · [Landscape masterplan](LANDSCAPE_MASTERPLAN.md) · [Global land-use/material registry](../../assets-src/gate3/zoned-world-v1/land-use-registry.json) · [Coverage](COVERAGE.md).

Baseline preserved: `checkpoint/g3d-world-recovery-review-20261023`. Safety checkpoint: `checkpoint/g3d-before-zoning-correction-20261024`. New authored sources/masks: `checkpoint/g3d-zoning-environment-sources-20261024`. Final review artifact: `checkpoint/g3d-zoned-world-review-20261024`. Runtime candidate is opt-in `zoned-world`; historical source/default manifests remain unchanged.

## Five coordinated batches

1. **Zoning and vegetation:** one registry distinguishes historic compounds, commercial city, forested Namsan, rail, attractions, harbor and canonical Jeju. New native urban ground replaces forest floor with continuous fine granite service alleys, sidewalks and open public space. Seven noncanonical trees were removed based on obstructed service/arrival space, not an arbitrary density percentage. Useful historical/park trees remain.
2. **Shared public space:** common paving unifies the commercial/transit/park arrival areas. Fine paved ride courts replace empty dirt receivers, with low perimeter flowerbeds and clear arrivals. A native144×96 road/curb ownership patch west of the station continues its existing frontage strip to the avenue. This is ground-only, outside the canonical forecourt, and is **not** the rejected90×36 platform paving connector. No existing road/crosswalk/source location or collision is moved.
3. **Historic/park boundaries:** eastern traditional courts receive coherent low wall endings and entrance openings; traditional source architecture stays exact. The commercial service landscape transitions through a bounded heritage garden. Accepted Namsan terrain, stairs and entrance remain pixel-exact; its protected tower projection is not arbitrarily cropped or moved.
4. **Waterfront/ocean:** market/terminal approaches use fine public quay paving, low coastal beds and a grounded rock/foam edge. Railbed weeds are reduced around unchanged track/platform reservations. A narrow low granite seawall grounds the existing straight western city coast without new land or a change to Maru’s nonpublic20px gap. A shared native offshore surface prevents independent water-panel palettes. Authored coast ownership follows depth/shore contours with binary native-texel transitions; external Jeju edge water uses documented native1:1 reflected **water-only** donors to match its border. No land/bridge/foam donor objects, approved-source RGB filters or source resampling. The entire original1024×1536 Jeju image and its foregrounds remain exact.
5. **Final QA:** actual Phaser native pairs, identical-framing overview proxies, targeted native crops, real input traversals, protected hashes/collisions and a single offline package. Build/readback/coverage are technical evidence, not human art approval.

## Evidence and technical limits

[Native captures](native-captures.json), [technical QA](technical-qa.json), [navigation](navigation-report.json), [movement](movement-report.json), [registrations/collisions](native-registration-checks.json), [asset provenance](asset-provenance.json), [protected hashes](protected-hashes.json), [prior G3-D checkpoint hashes](prior-g3d-checkpoint-hashes.json), [projection measurements](projection-report.json).

Native PNGs are actual1280×900 Phaser POST_RENDER exports, DPR1/zoom1, not browser-scaled screenshots or concept images. JPEGs are viewing copies under1MB. Both overviews use the same scaled Phaser proxy framing with existing wayfinding overlays; they are not pixel evidence. Native pixel comparisons exclude foreground/Juni rectangles and legacy translucent ground pixels and do not certify artistic quality.

The final continuous WASD/Shift run uses real field collisions and original Juni, no teleport or collision override. The station-to-amusement leg follows the west-side/perimeter approach, not an untested direct shortcut through a ride. Jeju arrival uses the existing western bridge. Selected foot-point reachability is not49px full-body/public-network acceptance. Videos are compressed viewing encodes; original PNGs establish pixel fidelity. WebGL hardware and physical Android Chrome/iPhone Safari remain **NOT TESTED**. Managed cache counts exclude browser/GPU/atlas overhead.

## Remaining P1 / decisions

| Item | Status / next decision |
|---|---|
| Exact six marked screenshots | **NOT TESTED:** images were neither attached nor found; reattachment requested. Z01–Z08 evidence maps the textual defect list only. Do not infer exact red/blue-marked acceptance. |
| Tower / modern street | **FAIL final composition:** protected complete283×668 silhouette at root(1200,3240) still projects6,957 opaque pixels over the selected retail-road rectangle. Native position/accepted105px door are preserved. A separately approved complete architectural projection treatment is needed; no antenna crop, facade move or street cover-up applied. |
| Station / amusement projection | **REVIEW OPEN:** protected station facade remains clear. Carousel finial still contributes95 opaque pixels over the canonical lower-road edge; wheel/carousel also project over the external apron, which is now intentional park arrival paving rather than unrelated asphalt. This is visual projection, not a support/collider intersection. See [alternatives](SPATIAL_DECISIONS.md); no ride/reservation move is made. |
| Station platform transfer | **BLOCKED:** strip[2950,2626,8,129] stays closed. The narrow eastern alternative is not certified for49px clearance. No new platform connector. |
| Public routes | **FAIL full network:** six inherited planned-centerline failures remain; actual movement takes valid existing-space alternatives. Original centerlines/reservations are not silently rerouted. Historic/canonical island and station conflicts require explicit planning/source-ownership decisions. |
| Collision ownership | Four new visible low-bed bases and a narrow constructed western quay wall have explicit contacts outside protected facades and all public path widths; removed tree feet are restored from baseline. **COL-001 remains open** for complete painted-border/support ownership and49px clearance beyond selected tests. New historic wall/entrance scenery and every perimeter detail still require native human/body-clearance review. |
| Bakery | Required/unplaced. Original 오월제과 artwork is preserved. W0 remains retired; Q1 is a candidate only, no972,160px² land allocation. |
| Devices / performance | Physical Android Chrome/iPhone Safari and hardware WebGL endurance/FPS remain NOT TESTED. No headless/emulated PASS is substituted. |

## P2 / native art review

Inspect global paving density, remaining low-border joins, rail/coast shadow contacts, palace/courtyard boundaries and source ownership at1:1. The native asphalt texture change where the new west approach meets the protected station frontage remains a material-match review item; the canonical road pixels were not filtered or repainted to conceal it. Water transition is materially improved but its wave/dither cadence requires human inspection. Canonical Jeju contains tiny detached green/edge pixels near the top open-water border and source-edge softness; these were preserved under the immutable-source rule and are not a new runtime-filter defect. Removing them would require a narrowly approved source-water ownership exception, not global blur/sharpening or island regeneration.

The shared direction and protected architecture are retained; the new environment composition is **not** self-approved. No merge to main, public deployment, separate application change, paid provider API or checkpoint rewrite occurred.

## Run and review

Extract the whole ZIP and run `python3 start_review.py`. Open the printed localhost URL; no Node is required for playback. The root menu exposes all ten review entries; native links use1:1 framing. [Physical-device checklist/export workflow](DEVICE_REVIEW.md). Full source reproduction requires the repository at the checkpoint, including immutable historical inputs; included tools document the pipeline rather than a partial source-only rebuild.

Stop for one consolidated human artistic/spatial review before any merge or deployment.
