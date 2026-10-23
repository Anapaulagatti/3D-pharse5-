# G3-A pixel-fidelity review — human visual acceptance pending

Two rendering defects were corrected: Canvas fallback stretched each image by 0.5px, and flex centering placed the canvas on half CSS pixels in odd-sized windows. The remaining soft detail in the native WebGL view is already present in the approved PNGs. No artwork was changed, sharpened or regenerated. **G3-B remains blocked.**

Start with the [diagnosis and ten-point audit](REPORT.md), [machine-readable pixel proof](pixel-proof.json) and [QA status](QA.json).

| Review | Before | After |
|---|---|---|
| Station frontage, native WebGL 1280×900 | [PNG](before-auto-native.png) | [PNG](after-auto-native-backing.png) |
| Station frontage, native Canvas 1280×900 | [PNG](before-canvas-native.png) | [PNG](after-canvas-native-backing.png) |
| Stationary gameplay, 1280×900 | [PNG](before-auto-stationary.png) | [PNG](after-auto-stationary-backing.png) |
| Camera moving during actual A-key input, 1280×900 | [PNG](before-auto-moving.png) | [PNG](after-auto-moving-backing.png) |
| Canvas camera moving, 1280×900 | [PNG](before-canvas-moving.png) | [PNG](after-canvas-moving-backing.png) |
| Odd-window browser display | [PNG](before-auto-odd-display.png) | [PNG](after-auto-odd-display.png) |

- [Source / before / after, 2× nearest crops](SOURCE_BEFORE_AFTER.png). Source softness is deliberately visible.
- [Canvas-specific source / before / after crops](CANVAS_BEFORE_AFTER.png).
- [Stationary comparison](STATIONARY_COMPARISON.png) and [moving comparison](MOVING_COMPARISON.png): 50% nearest review boards; use native links above for pixel evaluation. Movement frames have different camera positions because they are real independent input runs, not aligned reconstructions.
- [Station 0.5px pivot, actual native engine readback](after-auto-station-pivot-backing.png): unchanged logical anchor, integer raster placement.
- [Scenic 50% on odd mobile viewport](after-auto-half-zoom-odd-backing.png), [Jeju tour in motion](after-auto-tour-moving-backing.png). These are nonnative scenic evidence, not 1:1 pixel-quality references.
- Original-resolution `*-1x.png` crops are included for each sampled soft region.
- [Playable review ZIP](G3A_PIXEL_CRISP_REVIEW.zip). Extract, run `python3 -m http.server 4281 --bind 127.0.0.1`, open `http://127.0.0.1:4281/`. No public deployment. Original native PNGs and previous review archives remain unchanged.

Open downloaded native PNGs at 100% zoom. Inline previews, JPEGs, video and browser fit-to-window previews cannot establish native pixel quality. Android Chrome and iPhone Safari physical-device acceptance remain **NOT TESTED**.

Human checkpoint: review the corrected rendering and the source-versus-engine crops. No final visual PASS is asserted; remaining source-level softness requires a separate localized art decision if unacceptable. This package does not authorize that work or G3-B.
