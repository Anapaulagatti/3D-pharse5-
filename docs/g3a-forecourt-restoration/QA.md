# Technical QA and visual review

**Actual repaired candidate delivered. Final artistic acceptance remains PENDING. G3-B is BLOCKED.**

| Check | Result | Evidence / limit |
|---|---|---|
| Native source restoration | PASS | New derived floor and explicit masks; native same-coordinate recovery plus integer translations for ground hidden by retired props. No resize, sharpening, artificial upscale or image API. |
| Runtime integration | PASS | Only ground chunks 4-5 and 5-5 have new textures. Candidate-only manifest; approved world and previous candidate textures unchanged. |
| Native Phaser readback | PASS | 24 ROI readbacks across before/after WebGL/Canvas equal their expected source+foreground composites exactly; see technical-proof.json. This alone is not visual approval. |
| Pixel registration / nearest sampling | PASS | Integer chunk and object raster positions, scale 1, NEAREST; WebGL min/mag 9728. Renderer, camera and source-pivot policy unchanged. |
| Architecture / planter / shadow / Juni preservation | PASS | 1,341 protected asset hashes unchanged; existing source and world/runtime directories unchanged. Foreground objects, depths and logical solids identical to baseline. |
| Patch alpha / halos | PASS | Derived floor and changed chunks opaque; no translucent repair rectangle. Existing planter alpha sources and shadow files unchanged. |
| Curb / crosswalk / entrance geometry | PASS | No changes outside the explicit floor mask. Curb y812 onward remains exact; curb and door reference crops are pixel-identical. Tactile route uses a separate fixed material mask. |
| Entrance collision clearance | PASS | All 11,125 sampled positions in the unchanged 89×125-pixel aisle are walkable. Juni max visible width 49; source/body scale unchanged. Actual W/S threshold approach and return, plus short lateral aisle movement recorded. |
| Collision ownership | PASS | All collision references and hashes, logical station collider and entrance target unchanged. Existing lateral boundary near world x2531, y2734 is retained; the candidate does not widen or reroute existing walkability. |
| Build / preservation checks | PASS | TypeScript check and existing actor/Juni/historical preservation checks pass. Package asset hashes/CRC and extracted-package launch checked separately. |
| Stone joints / tactile readability | IMPROVED — REVIEW | Native 1:1 inspection shows fine stone grain, defined mortar and readable gold studs/ridges replacing the smeared central patch. Human comparison to surrounding architecture remains required. |
| Old objects / shadow duplication | PASS local inspection | No retired bench, old planter or bollard visible in restored floor. Exclusion masks and source map document reconstruction; current shadows applied once. |
| Shadow/material integration and patch seams | REVIEW | Local inspection shows coherent native material and retained contact shadows. Human approval is still required for subtle row-pattern repetition and the transition to protected surrounding source pixels. |
| WebGL performance acceptance | NOT TESTED | Headless capture validates rendering, not physical hardware performance or presentation FPS. |
| Physical Android Chrome / iPhone Safari | NOT TESTED | No recorded physical-device evidence. |
| Human artistic approval / G3-B | PENDING / BLOCKED | No automated result grants art approval. |

## Remaining visual issues and limits

The reconstructed ground under removed objects uses repeated clean native row material. It is crisp, but its subtle pattern rhythm, lighting balance and edge integration require human inspection. The current protected curb, road, crosswalk and surrounding source art can still contain historical baked softness; they were not sharpened or replaced. The original tactile route's existing breaks and turns are retained rather than redesigned.

This repair does not resolve the wider G3-A bakery/Maru reservations or grant final world-registration approval. The station's explicit 0.5px source-pivot convention remains unchanged and was not treated as the historical blur cause.

## Reproduce

`python3 tools/g3a_restore_forecourt.py` creates derived assets only. Build with `npx vite build --config gate3.vite.config.ts`; serve the build with asset directories available. `tools/g3a_restoration_capture.mjs` records actual controls and post-render screenshots. `python3 tools/g3a_restoration_proof.py` checks native readbacks, protection, collision references and lossless crop comparisons. No QA teleport or gameplay state injection is used.
