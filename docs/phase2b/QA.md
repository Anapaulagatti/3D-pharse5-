# Phase2B — TECHNICAL PASS / ARTISTIC REVIEW PENDING

| Check | Result | Evidence |
|---|---|---|
| Phase2A freeze before production | PASS | Approval tag at ed75734; freeze committed first at44d65a8 |
| Twelve stable free identities | PASS | Six completed packs promoted through existing registry; planned-only list now empty |
| Approved six / wardrobe / world | PASS | Byte-exact source hashes and identity snapshots;0 changed paired world pixels |
| New native packs | PASS, review candidates |6×112 poses,34 authored clips each,8 distinct frames per four-direction walk/run |
| Social compatibility | PASS | One additional runtime `social-front` alias to the8-frame greeting; no extra native frame slots or new input binding |
| Native registration/rendering | PASS |85 actual readbacks,0 opaque-pixel mismatch; integer placement, nearest sampling,96×112/48,100 |
| Locomotion and gestures | PASS, review candidates |48 real gait cycles show all8 frames; idle/wave/celebrate, stop/direction changes and shared native transition graph tested |
| Opposing profile arms | PASS |New six only; forearm-owned pixel changes,0 front/back or outside-owned-region changes; pairs re-recorded after correction |
| Production typecheck/assets/lint/format/unit/build | PASS |85unit tests; [commands/logs](VALIDATION_COMMANDS.md) |
| Full E2E | PASS |40tests:29 canonical production/Studio,11 retained historical V10; historical routes are not evidence of canonical success |
| Existing cosmetics/presets/v1/v2 | PASS |Approved asset/config bytes unchanged; actual existing Studio regressions and old Ara preset retained after60 switches/reload |
| Player/state/cache ownership | PASS, observations |One active Sprite;3 actor/2 base/2 composite cache bounds,60 switches through all12 |
| Working canonical bridges | PASS, representatives |Nari A walk +Hyunwoo B run, both out/return;1,688 sampled native contacts,0 unsupported; correct source-body readbacks |
| Mobile landscape | PASS, Chromium emulation |12-entry scroll gallery,667×375 and844×390, full native preview, touch joystick, orientation/reopen |
| Forge diagnostics | WARN |18new numerical warnings: {'seam': 7, 'leg_alternation': 11};0hardFAIL. [Verbatim values/thresholds](FORGE_WARNINGS.md) |
| Physical Android / iPhone | NOT TESTED |No recorded physical-device evidence |
| Hardware FPS/thermal/VRAM | NOT TESTED |Desktop heap/dimension estimates and SwiftShader only |
| Final artistic acceptance | PENDING |No invented human approval for the new six; Phase2C locked |

The initial profile-arm same-phase defect was corrected in the six new packs. Before-correction sources/reports are retained under history and earlier wave checkpoints. Current native/gameplay evidence uses corrected packs. The first bridge recorder used a screenshot-only native mode that hid the joystick; that harness failure is archived. Actual out/return traversal was then recorded with normal controls at zoom1/native backing resolution. No world collision patch was made.

No remaining new P1 functional defect is known in this scope. P2/review items: numerical gait/seam warnings and human review of costume/face/loop quality; physical-device and sustained performance validation. Palette-specific/outline-specific Forge checks were skipped when no matching palette/outline color was supplied, not silently marked PASS.

Inherited map issues remain unchanged and separate: Bakery placement (W0 rejected/Q1 deferred), station strip/route/planning defects and station/amusement conflict. Canonical interiors remain unsupported; no interior transition PASS is invented. No map regeneration, new gameplay systems, learning backend, Phase2C, main merge or public deployment.
