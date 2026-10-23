# G3-B/C world prototype and consolidated G3-D review

A4352×4864 continuous Phaser prototype now covers all ten planned regions with preserved approved historical/Muneum/Maru/station/Jeju sources, new palace continuation, archive, cultural workshop, Namsan tower, carousel, wheel, harbor market, ferry building, shared terrain/paths, vegetation and railway geometry. **This is not finished production or final artistic acceptance.** Bakery remains required and unplaced;13 coverage entries are partial.

[![World overview](world-overview-review.jpg)](VISUAL_INDEX.md)

Start with the [lightweight visual gallery](VISUAL_REVIEW.html), [world overview](world-overview-review.jpg), or [actual Phaser overview](world-overview-phaser.png). Regional original1:1 Phaser PNGs are linked from the gallery, alongside under1MB JPEG viewing copies. [Original native composite](world-composite-native.png) is an offline scene assembly, explicitly not a Phaser screenshot.

## Playable review

Download `GATE3_WORLD_PROTOTYPE_REVIEW.zip`, extract it, and run `python3 start_review.py`; open `http://127.0.0.1:4294/`. No Node install is needed. Use WASD/arrows, Shift run, E explore; mobile landscape retains joystick/Run/Explore, Follow/Scenic/Overview and tour controls. The original station baseline and historical district remain selectable/recoverable. The full-world prototype is the new default review scene, not a silent edit to historical manifests.

The ZIP contains the runtime,10 major-region native PNGs, lightweight previews/video, reports, source metadata and repository reproduction scripts. All18 native captures are preserved in the repository; additional originals are linked from the packaged gallery using the immutable review tag. Original host artwork, complete sources and the full native recording remain in the repository; they are not all duplicated in the lightweight package. All new runtime artwork is generated/derived native art; it is not claimed hand-drawn.

## Measured results and limits

- [Coverage matrix](COVERAGE.md):31 entries present in prototype,13 partial,1 Bakery placement blocked. Presence means content can be inspected, not premium quality accepted.
- [Actual gameplay video, lightweight review](world-traversal-review.mp4); [full native recording](world-traversal.mp4); [movement report](movement-report.json):15 continuous actual keyboard legs from the original transition spawn through northern/mainland/Jeju destinations. No QA teleport, collision override or synthetic animation. The [failed earlier attempt](movement-attempt1.json) and [recording](world-traversal-attempt1.mp4) are retained; a wider driver margin corrected that instrumentation failure without changing game masks.
- [Measured walking circuit](walking-times.json):20,182px of sampled real movement; capture intervals include recording/loading/stops, separately from ideal60/100px-per-second timings.
- [Navigation report](navigation-report.json):27 registered target foot points are in the spawn component; six planned centrelines still intersect inherited collision. Full49px Juni clearance and all public circulation are **not certified**.
- [Protected sources](protected-assets.json):1,352 hashes verify; approved historical/Jeju/forecourt ground pixels and the frozen V3.1 plan/manifest are exact. The0.5px station source-pivot convention remains unchanged; it is not reclassified as a blur cause. New foreground projections can visually occlude retained ground; underlying pixel preservation is not proof of unobstructed composition.
- [Technical/art QA](technical-art-qa.json):18 native Phaser captures verify integer registration, zoom1 and nearest sampling. Typecheck and28 unit tests pass. Architecture/material/composition/scale/depth issues remain separately visible, rather than receiving artistic PASS from these checks.
- [Chunk/performance report](performance-report.json):90 native512px chunks,64MiB tracked budget; measured peak67,090,060bytes,153 loads,76 evictions,0 pool errors during the final trace. Raw headless recorded frame cadence is slow; no60fps or hardware WebGL acceptance claim. Tracked bytes do not measure total browser/GPU memory.
- [Mobile emulation](mobile-report.json):touch joystick moved Juni without zoom change, reduced-motion tour/Return preserved Juni, report export downloaded. [Physical-device handoff](DEVICE_REVIEW.md):Android Chrome and iPhone Safari remain **NOT TESTED**.

## Required decisions and unfinished work

See [spatial decisions](SPATIAL_DECISIONS.md), [master defects](../../GATE3_MASTER_DEFECT_REGISTER.md) and [consolidated correction plan](G3D_CONSOLIDATED_PLAN.md).

Attraction ground contacts are fixed, but native vertical projections overlap the station frontage. This is an openly recorded foreground-occlusion candidate, not accepted station visibility or footprint expansion. The tower doorway is undersized relative to Juni. Shared materials repeat and differ in scale; Namsan slopes, heritage transitions/boundary continuation and platform detailing need further production craft. New physical foundation/trunk ownership requires clearance validation. These prevent a finished-world/artistic PASS.

Bakery W0 remains retired; Q1 land remains unallocated. The full-size original asset is preserved as required content. A coherent quay concept/access-return decision is deferred; the world is not described as100% complete while Bakery is unplaced.

The station8px strip remains unchanged and tracked for consolidated ownership QA. The rejected90×36 visual connector and modified canopy layers are not loaded. The approved station floor and original BEFORE canopy source remain recoverable at their existing checkpoints.

New source provenance: [host records](../../assets-src/gate3/full-world/host-provenance.json), [native extraction/masks](../../assets-src/gate3/full-world/extracted-assets.json), [integration ownership](../../assets-src/gate3/full-world/integration-provenance.json). No paid provider API was used. No main merge, public deployment, protected checkpoint rewrite or separate Korean Arena application change.

**Stopped for consolidated human review of the prototype and correction plan. Final release and artistic acceptance are withheld.**
