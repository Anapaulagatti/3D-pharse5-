# G3-D consolidated world recovery — human review candidate

The shared Gate1/Gate2.5 direction is conditionally approved; this ten-region production pass is **not final world acceptance**. [Download the playable ZIP](G3D_WORLD_RECOVERY_REVIEW.zip), [view the directly readable image gallery](VISUAL_REVIEW.md), or open the [HTML gallery](VISUAL_REVIEW.html) inside the package. [Coverage](COVERAGE.md), [actual native evidence](native-captures.json), [technical QA](technical-qa.json), [navigation](navigation-report.json) and [landmark projections](projection-report.json) retain the limits.

The opt-in Phaser scene is `recovery-world`. The approved historical sources, planning files and checkpoints remain unchanged. No main merge, public deployment, paid provider API or separate Korean Arena application change occurred.

## Implemented recovery

- Authored native regional ground plates share fine stone, asphalt, soil, planting and coastal material references. Binary ownership masks and native chunk crops replace the rejected large repeating material atlas. The full planned land footprint has authored or protected material ownership; this measures coverage, not artistic completion.
- Completed one palace roof with native timber/right-façade continuation over the original lower hall. There is no second stacked foundation. Original historical A and its approved architecture remain exact.
- Preserved the accepted Namsan terrain and105px doorway/body. The complete original antenna is retained; miniature-door trials and the previous30px tip shortening are not propagated. Its street projection remains an explicit P1.
- Original cafe/bookshop/learning/Maru textures and collisions are unchanged. Foregrounds soften to0.35 only while Juni stands behind them, restoring player visibility; otherwise they render at1.0.
- Added new low Korean fish market, compact ferry ticket hall, four-horse carousel and four-cab family observation-wheel candidates at native scale. These are new profiles, not downscaled old sprites. Their final program/style and residual projections require human review.
- Preserved Hanbit architecture, original canopy/pivot, corrected planters/independent shadows and canonical restored floor. A50px lower-road continuation outside the canonical floor completes the crosswalk/curb termination; it is not a platform connector.
- Retained original Jeju architecture/terrain/orchard/entrance artwork. New surrounding water/shore/arrival ownership does not repaint the island or implement ferry gameplay.
- Unified deep open water with the approved Jeju128px fine-wave component at native phase, removing rectangular regional water-color panels. Original Jeju and the authored near-shore band remain excluded; no rejected landscape tile or source color filter is used.
- Removed obsolete oversized prototype trees. Native tree-bank specimens and explicit contact feet provide restrained regional clusters. The new104×80 market approach clears only an obsolete placeholder margin beyond unchanged root3660. Two small loose-counter contacts are independently registered on existing non-route plaza land.

## Technical result and its limits

All1,440 protected source hashes and historical tags pass verification. The six protected renderer/cache/camera/registration files are unchanged. Station logical half-pixel source-pivot metadata is preserved. Runtime images/camera placements use integer native pixels and nearest-neighbor sampling. Eighteen actual1280×900 Phaser frames have zero mismatches over their eligible opaque ground pixels, excluding foregrounds/Juni and legacy translucent source pixels.

The actual continuous WASD/Shift run completed17 destination/entrance legs with unchanged real collision handling and no teleport. This proves selected foot-point movement; it does **not** certify every planned route or49px body clearance. Build/typecheck,28 existing tests, protected-asset checks and targeted lint pass. [Movement evidence](movement-report.json) and [source provenance](asset-provenance.json) retain the details.

The gameplay video is a real recorded run. Published MP4s are viewing encodes; pixel-quality evidence is the untouched native PNGs. The ZIP contains ten original native images; additional originals/crops remain in the repository. JPEG previews are under1MB. Neither previews, video compression, build success nor coverage counts grant artistic PASS.

## Remaining P1 decisions

| Issue | Current finding / safe next decision |
|---|---|
| Namsan versus retail | Full283×668 silhouette at protected root(1200,3240) still projects6,957 opaque pixels over the selected retail-road envelope. Keep position/accepted lobby; a coherent height/projection or localized planning decision is required. No arbitrary crop, street cover-up or protected move applied. |
| Station / amusement | New rides no longer overlap the station façade. Carousel finial still overlaps95 pixels of the canonical floor's lower road edge; carousel/wheel also project over the new lower-road continuation. This is visual occlusion, not a support/collision intersection. Human acceptance of that projection remains open. |
| Station transfer | Closed strip[2950,2626,8,129] and original canopy preserved. The eastern alternative is narrow; selected connectivity does not establish a safe full-body platform transfer. No new connector or scenery edit is installed. |
| Public route alignment | Six inherited centreline failures remain: archive access23 samples, retail364, leisure235, Jeju coast5, house approach32, bridge connector63. Protected scenery/route registration decisions are needed; no silent diversion or island repaint. |
| Native collision ownership | Fixed contacts and protected collision geometry remain intact, plus explicitly documented local approach/prop feet. Full49px clearance and every painted border/support/foreground edge are not certified. COL-001 remains open. |
| Required Bakery | Original905×763 오월제과 asset remains required/unplaced. W0 rejected; Q1 is a candidate only and no972,160px² land allocation is made. No repeated exhaustive search against the unchanged plan. |
| Hardware / devices | Logical managed texture budget was respected during the headless run, but nearly reached64MiB. This excludes driver/canvas/atlas overhead. Hardware WebGL performance and physical Android Chrome/iPhone Safari remain **NOT TESTED / unresolved**. |

## P2 / visual review items

Review upper-palace roof/course density and end junctions, protected-scene/water joins, low border/vegetation contact ownership, and new landmark lighting/material polish at1:1. The smaller-capacity carousel/wheel and modest regional ferry hall require artistic/program acceptance. Remaining source-edge softness is source artwork/alpha, not evidence of a new resampling defect; no global sharpening or recoloring was used.

The central [master defect register](../../GATE3_MASTER_DEFECT_REGISTER.md) preserves earlier findings and current recovery states. Bakery/P1 issues prevent any claim of complete-world acceptance.

## Reproduction and handoff

Use Node24 and the repository lockfile. `tools/g3dw_assets.py` extracts native owned components; `g3dw_build.py` rebuilds only the new recovery namespace; `g3dw_validate.py` checks hashes, registrations, fields and native readback. `g3dw_capture.mjs`, `g3dw_plan_walk.py` and `g3dw_walk.mjs` produce real evidence. Historical plans/manifests/PNG sources are read-only inputs. Exact host-authoring prompts/reference paths and rejected trials are retained under `assets-src/gate3/recovery-world-v1/`.

Extract the playable ZIP and run `python3 start_review.py`; open the printed localhost URL. Physical-device review uses the [device checklist/export workflow](DEVICE_REVIEW.md). Stop after the consolidated human artistic/spatial review; no release, merge or public deployment is authorized.
