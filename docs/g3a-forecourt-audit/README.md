# Station forecourt audit — visible softness remains unresolved

**Forecourt visual quality: FAIL / OPEN.** The paving is still softer than the preserved facade, doors and corrected planters. Pixel-exact texture transport does not resolve that appearance. No source repair, sharpening, upscaling, recoloring or renderer change was applied in this audit. **G3-B remains blocked.**

[Verified direct native PNG links](NATIVE_LINKS.md) · [Exact lineage, extraction and native readback](proof.json) · [Non-destructive repair proposal](FIX_PLAN.md)

## Native1:1 before/after crops

These are actual Phaser backing-store crops, not browser-scaled images. “Before” and “after” mean before/after this focused audit of unchanged art; **they are identical, not a claimed visual improvement**. Juni was moved out of the sampled ground using the S key. Full frames and per-renderer crops are retained alongside [capture metadata](captures.json).

| Area | Source coordinates `(left,top,right,bottom)` | Before audit | After audit / still unresolved |
|---|---|---|---|
| Entrance ground |(2768,706,2895,775) |[127×69 PNG](entrance-ground-before-1x.png) |[127×69 PNG](entrance-ground-after-1x.png) |
| Tactile strip |(2798,700,2853,813) |[55×113 PNG](tactile-strip-before-1x.png) |[55×113 PNG](tactile-strip-after-1x.png) |
| Left planter-adjacent paving |(2528,756,2775,813) |[247×57 PNG](left-planter-pavement-before-1x.png) |[247×57 PNG](left-planter-pavement-after-1x.png) |
| Right planter-adjacent paving |(2895,756,3135,813) |[240×57 PNG](right-planter-pavement-before-1x.png) |[240×57 PNG](right-planter-pavement-after-1x.png) |

[Native1x contact sheet: source / before / after](NATIVE_1X_COMPARISON.png) includes the [crisp door reference](crisp-door-reference-after-1x.png) and [planter stone reference](crisp-planter-reference-after-1x.png) at the same pixel scale. No crop is enlarged, sharpened or filtered. View originals at100% zoom.

Full1280×900 actual Phaser PNGs: district WebGL [before](district-auto-before-native.png) / [after](district-auto-after-native.png); district Canvas [before](district-canvas-before-native.png) / [after](district-canvas-after-native.png); registered station WebGL [before](registration-refined-auto-before-native.png) / [after](registration-refined-auto-after-native.png).

## What caused the contrast

1. **Central ground source is soft.** All8,763 entrance-ground pixels are the2030×775 host background finished to3184×1214 with historical NEAREST resizing. Of6,215 tactile-crop pixels,5,940 belong to that background and275 to the preserved original plate. The door reference's15,950 pixels come entirely from the original native plate. Native architecture was restored separately, leaving a visible change of source detail below the protected station region ending at source y704.
2. **The planter-adjacent ground has a different authoring history.** Local floor underpainting was resized2170×725→608×188 with NEAREST and applied through binary masks around the old planters. That historical resize is anisotropic (about8.05% aspect-ratio change), and its painted/resampled pavement is already baked into the ground. Additional same-Y native paver underpainting exists below extracted bollards. Owned planter shadows were then composited once. These operations predate this audit; hidden ground under sprites and visible ground ownership are distinguished in `proof.json`.
3. **Patch extraction adds no softness.** Source `(2500,690)–(3184,900)` is copied to world raster `(2274,2603)` at684×210. All**143,640** extracted/stitched source pixels match exactly, with alpha255 throughout. The original district east texture also matches that same source crop. No feathered patch boundary, patch-size change or RenderTexture resampling exists in this path.
4. **Current rendering adds no softness in the tested regions.** Thirty-six native ROI comparisons across WebGL district, Canvas district and registered-station WebGL all match the appropriate ground-plus-foreground source composite exactly: zero changed pixels, max channel delta0. Native layer placement/scale, camera phase and nearest filtering are preserved. The previously corrected Canvas dimension expansion remains disabled. The station's0.5px source pivot resolves to integer raster placement and is not this defect's cause.

NEAREST sampling does not mix neighboring colors, but it cannot recover missing source detail. The central smear and mixed material detail are visible in the stored source before Phaser sees it. No new Gaussian blur, runtime interpolation or alpha halo was found. This is a **source-fidelity and historical source-compositing problem**, even though the earlier Canvas defect was real and remains corrected.

## Recoverable crisp reference and proposed remedy

An earlier native source at the same station coordinates retains crisp paver joints and tactile detail: `assets-src/gate25-reconstruction/original-ground.png`. [Current versus earlier native reference](NATIVE_RECOVERY_REFERENCE_NOT_APPLIED.png). The earlier source includes old baked props, so it is **not a safe drop-in replacement**.

The correct repair path is a separate, masked native-ground restoration candidate using verified clean pixels from that earlier source, with object/door/tactile geometry locked and no resampling. [Detailed proposal and safeguards](FIX_PLAN.md). It has not been applied or presented as gameplay. The existing soft source and all approved artwork/checkpoints remain recoverable.

## QA and limits

| Item | Judgment |
|---|---|
| Forecourt visual crispness relative to facade |**FAIL / unresolved** |
| Source/extraction/compositing diagnosis |PASS evidence; exact stored-source lineage identified |
| Native WebGL/Canvas transport in tested regions |PASS:36 source-composite comparisons;143,640 extraction pixels exact |
| Source restoration implementation |**NOT APPLIED / proposal only** |
| Original art, renderer and checkpoints |PASS preservation;1,341 protected hashes and all `src/gate3` files unchanged fromb7cf611 |
| Final human visual acceptance |**NOT GRANTED** |
| WebGL hardware performance / physical Android+iPhone |UNRESOLVED / NOT TESTED; no new performance/device claim |
| G3-B |**BLOCKED** |

No approved source, masterplan, building, entrance, planter, Juni asset, collision layout or runtime was changed. No merge or site deployment.
