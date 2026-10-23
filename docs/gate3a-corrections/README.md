# G3-A targeted corrections — review package

**[Download updated playable ZIP](G3A_TARGETED_REVIEW.zip)** · [PASS/FAIL/NOT TESTED report](REPORT.md) · [Registration proposal](REGISTRATION.md) · [Renderer diagnostics](PERFORMANCE.md)

The approved district/masterplan remain unchanged. A separate candidate registers six native buildings individually, retains station logical coordinates and declares the 0.5px raster pivot. Bakery and convenience locations are new unassigned proposals; plot/path/easement approval is still required. Grey terrain and source ownership cuts are technical proof, not completed district art. G3-B mass production has not begun.

## Planning and alignment

- [Current versus proposed world-registration diagram](CURRENT_VS_PROPOSED.png).
- [Building footprint comparison](FOOTPRINT_COMPARISON.png), [source/proposed entrance coordinates](ENTRANCE_COORDINATES.md), [exact conflicts](spatial-conflicts.json).
- [Pixel-phase/collision diagram](PIXEL_PHASE_AND_COLLISION.png), [native pixel readback](native-pixel-and-phase.json), [candidate plan data](registration-proposal.json).

## Native Phaser evidence

| View | Original1:1 PNG | Lightweight preview |
| --- | --- | --- |
| Station, corrected planters and Juni | [Native](station-native.png) | [Preview](station-preview.jpg) |
| Muneum cafe/bookshop/learning with Juni | [Native](retail-native.png) | [Preview](retail-preview.jpg) |
| Bakery at proposed waterfront plot | [Native](bakery-native.png) | [Preview](bakery-preview.jpg) |
| Convenience store at Namsan approach | [Native](convenience-native.png) | [Preview](convenience-preview.jpg) |
| Original district retained | [Native](preserved-district-native.png) | [Left planter1:1](left-preserved-planter-1x.png) / [Right1:1](right-preserved-planter-1x.png) |
| Historical/Jeju preserved | [North native](preserved-north-native.png) | [Jeju native](preserved-jeju-native.png) |
| Candidate overview | [Actual Phaser planning overview](registration-overview.png) | Overview is a downsampled proxy, not native art |

[Approved source versus actual Phaser, original-resolution crops](NATIVE_SOURCE_COMPARISON.png). Native PNGs are untouched; JPEGs are review derivatives.

## Actual gameplay

- [Station entrance approach](STATION_APPROACH.mp4).
- [Retail to station across native chunks](RETAIL_TO_STATION.mp4).
- [Bakery forecourt around proposed bypass to bridge approach](BAKERY_TO_BRIDGE.mp4).

[Input/state report](traversal-report.json) · [Six-route collision audit](static-validation.json) · [Touch/reduced-motion/export report](controls-report.json).

## Diagnostics and preservation

[First-stage baseline](diagnostics-baseline.json) / [optimized](diagnostics-optimized.json) · [final culling ablation](culling-ablation.json) · [layer/viewport isolation](render-isolation.json) · [GC/main-thread trace summary](trace-summary.json) · [resource recovery](resilience-report.json) · [context-restore native proof](context-native-proof.json).

[North/Jeju/district prior-frame pixel preservation](preserved-frame-proof.json) · [Source/provenance and reproduction](PROVENANCE.md) · [Device handoff](DEVICE_CHECKLIST.md) · [Package integrity](package-proof.json).

Physical Android Chrome/iPhone Safari remain **NOT TESTED**. Software WebGL frame-rate acceptance remains unresolved; no hardware claim follows from SwiftShader. Final individual registration and artistic seam acceptance remain pending.

Please review the registration/pivot/plot and path proposal before G3-B, as required by the [targeted correction directive](../current/G3A_TARGETED_CORRECTIONS.md). No main merge or public deployment.
