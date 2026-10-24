# Residual technical, collision and artistic QA

[Machine technical report](technical-qa.json) · [Native matched gallery](VISUAL_REVIEW.md) · [Actual movement](movement-report.json) · [Body/foot evidence](body-clearance.json) · [Protected hashes](protected-hashes.json).

| Item | Classification | Evidence / limits |
|---|---|---|
| Build/typecheck/assets/unit checks | PASS |30 tests /9 files; does not approve art |
| Native matching / renderer fidelity | PASS |20 identical-camera pairs;17,919,981 eligible pixels,0 mismatches; nearest native scale/integer camera; six renderer core modules exact |
| Original source/checkpoint protection | PASS with read-only diagnostic exception |1439/1440 library entries exact; PixelAudit adds opt-in pose observation only.242 previous alignment files exact; old tags preserved |
| Station canonical frontage/planters | PASS |Original file immutable; actual Phaser foreground comparison pixel exact excluding animated Juni. Only old baked-tree pixels retire beneath identical foreground. Main road/tactile/curb/crosswalk/shadows preserved |
| Station crown/alpha | PASS measured clipping/ownership criteria |New bounded crown, binary alpha; original pot/trunk/native source RGB exact. Human craftsmanship approval pending |
| Original canopy roof/post/HVAC | PASS source guards |Native metal roof/post/sign RGBA and HVAC exact; original registration/pivot/depth. Obsolete side-floor/background ownership retires; no protected platform-support movement |
| Palace axis/actual threshold | PASS |2048,685 reached via genuine controls; central native stairs/rails/portal/roof preserved; finishing remains human visual review |
| Retail original facade/native scale | PASS |All original RGB; structural facade RGBA guards. Cafe wide prior guard included nonarchitectural background, now explicitly separated |
| Continuous route / bridge locomotion | PASS selected movement |9 actual legs, complete mainland→Jeju→mainland; no teleport/collision/clock override |
| Captured stop/turn source pixels | PASS rendering only |12 genuine POST_RENDER poses both directions;25 native frames,0 unexplained changed Juni pixels. Expected foreground occlusion recorded separately |
| Full native current bridge contact | FAIL |{'complete-bridge-to-jeju': 18, 'complete-jeju-to-mainland': 8}; physical model retains actual below-anchor toes. Previous13/6 baseline used older normalized contact sampling; source atlas/game unchanged |
| Bridge structural-clearance proposal | PASS geometry model only / NOT ADOPTED |25px maximum bounded shoulder search,4866 visible-support pixels; actual current field unchanged. Railing/support architecture still requires review/production if authorized |
| Current archive public clearance | FAIL final acceptance |20px corridor not accepted as final; separate88px gate only |
| Current wall / hypothetical gate behavior | PASS expected engineering comparison |Current native wall blocks; proposal real movement reaches door. That is not final visual/public acceptance |
| Station platform transfer | FAIL / still blocked |Real input stops at rendered pixel2958;8px field closed. Simulation float2957.8015 correctly rounds to2958; raw initial float-threshold assertion retained |
| Main canonical road integration | FAIL pending decision |Original protected asphalt phase/softness retained. Isolated native road candidate shown, not silently applied |
| Full approved route network | FAIL |7 inherited planned centerlines still contain blocked samples; geometry-only diagnostics separate from actual selected route |
| Six marked reviewer images | NOT TESTED |Not supplied/requested; no claim that all exact marks were closed |
| Hardware WebGL / physical Android/iPhone | NOT TESTED |Desktop WebGL/Chromium touch emulation do not certify hardware/device performance |
| Final full-world artistic acceptance | FAIL / human decision withheld |Observable repairs delivered; mandatory Bakery, spatial/P1/device decisions remain |

## Source-fidelity findings

The residuals were source ownership/crop/material-wrap issues. The already corrected renderer remains unchanged; no half-pixel renderer diagnosis is reopened. Original0.5 station source-pivot convention retained. There is no global sharpening, blur, recolor, stretch or fractional resampling.

The shared ocean used the same1536×1024 source on both sides of the visible3180 line, but its opposite edges were not periodic. Minimum-error native overlap cuts preserve global period/phase and every RGBA texel's original integer source coordinate. Edge mean deltas X9.78→4.40,Y10.43→5.65 are technical diagnostics, not artistic approval. The broader physical-water trial was rejected, so the original Jeju protection bitmap remains exact.

Actual route recording uses original WASD plus native joystick fine control and screenshot instrumentation. Recorded duration is not an exploration-pacing or hardware-FPS benchmark. Lossy MP4s prove movement; untouched native PNGs prove pixels.

Extracted playable ZIP regression: **PASS** ten existing region entries +three isolated proposals, desktop WASD, mobile touch gesture isolation, normal/reduced-motion tour controls, original-position return and exported JSON. This is Chromium emulation only, not physical-device or hardware-performance acceptance. See [package smoke](package-smoke.json). Scoped TypeScript/MJS ESLint and Prettier: PASS.
