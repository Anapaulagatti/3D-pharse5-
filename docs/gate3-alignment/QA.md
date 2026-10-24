# Technical and visual QA

Technical success is not artistic approval. [Machine report](technical-qa.json), [movement](movement-report.json), [bridge movement](bridge-movement-report.json), [actual body readback](body-clearance.json), [route audit](navigation-report.json), [protected hashes](protected-hashes.json).

| Item | Result | Evidence / limitation |
|---|---|---|
| Typecheck, unit tests, assets, scoped lint/format, private build | PASS |30 tests /9 files; original source/atlas checks |
| Native pairs / sampling | PASS |15 identical-camera pairs; 13,680,765 eligible ground pixels,0 mismatches; integer positions, zoom1, nearest |
| Protected registry | PASS with explicit code exception |1439 of1440 baseline entries exact; opt-in PixelAudit adds read-only alpha/depth. All protected artwork exact;254 previous checkpoint files exact; historical tags preserved |
| Canonical station ground | PASS preservation |Raw2274,2603,684,210 exact; planters/canopy source/pivot unchanged |
| Palace actual threshold | PASS |2048,685 via real controls, derived axis matches2048 |
| Eight-leg continuous world route | PASS |Original controls/collision; continuous recording; driver failures preserved |
| Complete upper bridge crossing | PASS |3130,3460→3530,3640, actual deck, no alternate bridge/teleport |
| Juni source/body rendering | See body-clearance.json |Actual atlas pixel comparison and depth occlusion, separated from native projected contacts |
| Full bridge stop/turn body clearance | FAIL |13 whole-route and6 bridge-proof samples outside physical surface; strict native stop/turn union has no safe route within current deck |
| Final archive pedestrian composition | FAIL |20px front corridor; secondary88px gate PROPOSAL ONLY |
| Final seamless station | FAIL |Protected-road softness/phase; clipped original right tree crown retained, not hidden |
| Station8px transfer | FAIL / blocked |Closed strip unchanged; no90×36 connector |
| Entire planned network | FAIL |7 planned centerlines contain blocked samples; conservative radius is diagnostic, not a native bridge-foot model |
| Both bridge landings' visual quality | REVIEW / not human accepted |Native structure/source/physical overlays plus crossing; no collision-only artistic PASS |
| Seven marked reviewer images | NOT TESTED |Not attached/requested; no annotation closure claim |
| Hardware WebGL / physical Android / iPhone | NOT TESTED |Desktop software WebGL and emulation cannot certify device performance |
| Final world artistic acceptance | PENDING HUMAN |No main merge/deployment; Bakery/projections/route issues remain |

## Exact changes and diagnosis

Source crop/alpha/ground ownership caused these architectural seams. The prior corrected renderer is retained; six core camera/texture/chunk modules are byte-identical. The station0.5 source pivot is retained and is not blamed for baked softness. No scaling, sharpening, global blur or approved-source regeneration.

Seven ground chunks and nine field chunks rebuilt; all other chunks reused. Foreground textures are derived independently. Exact files/masks/hashes: [asset provenance](asset-provenance.json), [integration records](../../assets-src/gate3/alignment-v1/integration-provenance.json), [technical inventory](technical-qa.json). Original masterplans unchanged.

The two protected decisions (archive gate / canonical-road native material exception) are not silently adopted. Existing source-tree clipping is a recorded quality failure. Keep failed movement attempts; neither source hashes nor a clean build establish visual approval.
