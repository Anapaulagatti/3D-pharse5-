# QA — TWO separate Jeju crossings

Hanbit is HUMAN ART APPROVED and LOCKED. Bridge engineering checks below do not grant human artistic acceptance.

| Check | Bridge A north | Bridge B south | Evidence / limit |
|---|---|---|---|
| Walk both directions | PASS | PASS | Actual original WASD/joystick, independent bridge review spawn, no in-route teleport |
| Run both directions | PASS | PASS | Actual original Shift100px/s, no speed override |
| Stop on both landings / narrow span | PASS selected recording | PASS selected recording | Original idle/stop atlas and native contact checks |
| Left/right turn and direction changes near rails | PASS selected recording | PASS selected recording | Native controls, actual wall stop then reverse back along travelled axis |
| Native contact support | PASS | PASS | 3755 sampled poses total;0 unsupported;40 genuine native body/pose readbacks |
| Visible deck / supports | PASS local engineering review | PASS local engineering review | Full native bridge/landing views; no synthetic floor over sea. Final artistic assessment PENDING HUMAN |
| Structural alignment | PASS local engineering review | PASS local engineering review | Source origin, planning/landmark registrations unchanged; new abutment/paving/rail terminations within exact edit masks |
| Pixel sampling/materials | PASS technical | PASS technical | 12498293 exact Phaser ground pixels; nearest1:1; binary source post mattes; no global filters |
| Human artistic acceptance | PENDING | PENDING | Must inspect actual native PNGs and gameplay |
| Physical Android/iPhone | NOT TESTED | NOT TESTED | Emulation cannot establish hardware acceptance |

## Preservation

- 2972 historical asset files unchanged. Approved Hanbit source pixels,3 registered architecture layers, full native surroundings, entrance and platform collision remain exact. See [hashes](protected-hashes.json) and [native station proof](station-preservation.json).
-0 static/ground/collision pixels changed outside the two exact bridge masks. No new island/mainland land allocation, protected landmark relocation or original masterplan edit. [Scope](out-of-scope-audit.json).
- 19 real Phaser collision queries verify station entry/platform and bridge floors/blocked rail zones; legacy station texture requests0. [Runtime](collision-runtime.json).

## Important route distinction

The original world plan remains byte-exact. Several old Jeju polylines describe obsolete source/collision guidance and do not follow the corrected, native-safe bridge top plane. They are not silently rewritten or declared PASS. The current tested corridors are explicit in [geometric-clearance.json](geometric-clearance.json), actual input in [movement-report.json](movement-report.json). Changes to historical centreline checks are listed below; all occur inside authorized bridge masks, with0 unrelated collision changes.
- `island-arrival`: 20 → 3 blocked1px samples.
- `jeju-native-ferry-arrival`: 0 → 293 blocked1px samples.
- `jeju-native-main-coast`: 5 → 28 blocked1px samples.
- `jeju-native-bridge-arrival`: 1 → 214 blocked1px samples.
- `jeju-gate2-bridge-connector`: 65 → 98 blocked1px samples.

These legacy guides require reconciliation at the planning/navigation checkpoint. The bridge-local walking corridors pass the selected real-control cases; this is not final whole-world navigation acceptance. Unchanged internal Jeju path/house/bridge guidance, Bakery required/unplaced (W0 rejected; Q1 unallocated), tower/retail and amusement projection questions remain open. No protected reservation amendment was forced.

## Test history

The initial adversarial harness stopped after pushing toward a rail and trying to slide along its angled boundary in the wrong recovery order. It is retained as diagnostic history, not final evidence. The first broad support envelope also included vertical masonry; it was rejected and replaced with a native top-plane trace and proper post foreground ownership. The final video/tests use only the final field; no collision was relaxed to force traversal.

## Limits

Chromium touch/reduced-motion checks are emulation. Hardware WebGL performance and physical Android Chrome/iPhone Safari remain NOT TESTED. Human artistic acceptance remains PENDING. No main merge/public deployment/paid external artwork API/separate application changes.

## Extracted playable package

PASS:16 actual entry loads, including both crossings and approved Hanbit;0 chunk/page errors. WASD, Chromium844×390 DPR3 joystick isolation, Tour Pause/Skip/collapse/Return, reduced motion and exported test JSON pass regression. This is emulation, not physical-device acceptance. [Smoke](package-smoke.json).
