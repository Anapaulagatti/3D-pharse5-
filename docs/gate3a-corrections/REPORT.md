# Targeted G3-A corrections — final registration approval pending

This delivery replaces neither the approved district nor the masterplan. It supplies an individual-building candidate, limited playable proof and controlled renderer diagnostics. Gate3 remains authorized overall; G3-B mass artwork production has not begun.

## Registration outcome

The invalid rigid group is removed from the proposed integration architecture: cafe, bookshop, learning, convenience store, bakery and station have explicit source/world registrations. The protected station reference(2238.5,2180), collision(2322.5,2380,555,210), threshold(2598.5,2610), canvas and all other protected structures remain unchanged in the approved plan. A declared source pivot0.5 gives candidate raster edge2238; that convention requires approval and is not a hidden rounding of the protected coordinate.

Bakery is a new **unassigned waterfront plot**, not a fictional protected bakery reservation. Contact size875×442 fits the zone without intersecting a protected building contact, but requires five named path amendments. Convenience is an unassigned western Namsan-approach plot with a proposed local path bypass. Cafe and visual facade envelopes also need the explicit easements listed in [REGISTRATION.md](REGISTRATION.md). The bakery projection overlaps a future carousel envelope38×90px; no carousel moves. Source cutouts are not production-ready side elevations or finished streetscapes.

[World diagram](CURRENT_VS_PROPOSED.png) · [Footprints](FOOTPRINT_COMPARISON.png) · [Entrances](ENTRANCE_COORDINATES.md) · [Exact spatial conflicts](spatial-conflicts.json) · [Phase/collision diagram](PIXEL_PHASE_AND_COLLISION.png).

## Performance outcome

Controlled trials isolate cold loading, warm stationary rendering, keyboard movement, Scenic/Tour transitions and24MiB stress. Two trials per renderer reverse order; no recording or concurrent browser work contributes. [PERFORMANCE.md](PERFORMANCE.md) contains the full limits and results.

The identified redundant upload path improves from90 to30 texture uploads for 30 streamed cold-station images; texture-admission CPU p95 decreases9.1→5.1ms. CPU allocation/admission work is reduced without resizing artwork. Final culling skips cached objects outside the actual camera using whole padded image bounds; its separate ablation reduces tour submissions/batches but does **not** establish a frame-rate improvement. Stationary WebGL still measures around28ms p95 on SwiftShader; Canvas around17ms. Native-area/layer probes support a software raster/fill/texture-bandwidth contribution. Main-thread GC pauses are too small in the sampled traces to explain the whole gap. GPU timer queries are unavailable, and hardware/mobile performance is NOT TESTED.

The deliberately undersized24MiB desktop scenic tests enforce their budget but report admissionBlocked=true. They are **not** a successful low-memory-device test. Normal64MiB trials report no admission failure. Logical decoded-resource budget is not total process RAM/VRAM; fixed textures, decoding, framebuffers, copies and driver overhead remain outside it.

## PASS / FAIL / NOT TESTED

| Check | Judgment | Evidence / limitation |
| --- | --- | --- |
| Approved art/Juni/shared prototype preservation | PASS |1,341 protected hashes unchanged; original plan/source/prototype retained |
| Canvas4352×4864 and protected station geometry | PASS |No approved-plan edit; continuous half-pixel collider tests |
| Native source scale/material/pixel preservation | PASS technically |12 opaque native readback regions exact; both corrected planters exact; source-comparison crops |
| Proposed source pivot / final registration | NOT TESTED by human |Explicit -0.5px raster convention and planning easements await approval |
| Bakery site versus protected building contacts | PASS for contact intersection |No protected contact overlap; route/projection conflicts explicitly reported, not approved |
| Fit against all unchanged facade reservations | FAIL |Cafe25px width and native height/visual overhangs need amendment; new bakery/convenience plots unassigned |
| Sampled candidate collision routes | PASS |Six4px-grid paths with3px safety inset and1px segment checks; not exhaustive full-world navigation |
| Actual input traversal | PASS for three recordings |Station threshold, retail→station and bakery→bridge; normal scene entries, original60/100px/s controls, no teleport/speed override |
| Planter entrance clearance | PASS technically |Retained89px field versus49px Juni visible width; both source objects and root depths preserved |
| Candidate foreground/root separation | PASS for limited proof |Station canopy separated from facade; original planter roots; whole-object bounds culling |
| Collision failure gating/retry / cache eviction | PASS for tested emulator cases |Injected503 blocks movement then recovers; bounded24MiB small-landscape resilience run; no unbounded resource retention |
| Software WebGL context restoration | PASS for tested browser |Native non-Juni pixel comparison before/after context restore; no physical-GPU conclusion |
| Upload/render-work optimizations | PASS for measured work reduction |No source-resolution reduction; final culling ablation and raw counters supplied |
| Sustained60Hz software WebGL | FAIL in these conditions |Around28ms warm p95; no claimed universal frame-rate gain |
|24MiB desktop scenic complete visible admission | FAIL / intentionally undersized stress |Admission failure signalled; stable budget enforcement does not certify image completeness |
| Touch joystick / reduced motion / controls / export | PASS for Chromium emulation |Source behavior retained; separate controls report |
| Finished connected district artistry / reusable art completeness | NOT TESTED / unfinished |Engineering terrain and conservative cut boundaries are not finished art or seam approval |
| Full-world navigation/performance/release acceptance | NOT TESTED |No mass integration or G3-D acceptance claimed |
| Physical Android Chrome / iPhone Safari | NOT TESTED |Recorded real devices remain mandatory before release recommendation |
| Typecheck / lint / format / asset checks / unit tests / build | PASS |26 tests in7 files; dedicated portable build |
| Final human G3-A registration approval | NOT TESTED / pending |Successful tests do not grant approval |

## Remaining engineering risks and next actions

1. Human review must select/approve the declared raster/source-pivot convention and exact local plot/easement/path changes. Keep the approved masterplan untouched until then.
2. Before G3-B reuse, author and review complete side elevations, semantic vegetation/foreground ownership and coherent surrounding pavement. Preserve every approved facade pixel; do not mass-place the technical polygon cutouts or conceal them with large props.
3. Validate bakery roof/attraction projection and rear/side route occlusion at native scale; this technical registration does not establish completed visual composition or full exploration pacing.
4. Measure real Android/iPhone GPU, memory pressure, loading, camera transitions and input. Keep Canvas fallback. A future Phaser upgrade must rerun upload/context-restoration/native-pixel proofs because the scoped filter guard depends on4.2.1 behavior.
5. Determine a device-appropriate working-set budget/viewport policy before release.24MiB cannot cover the tested desktop50% view. Do not reduce native source art to hide this limitation.

The ZIP includes the candidate, original world/district review modes, byte-identical approved prototype archive, source hashes, proposal data and device checklist. Videos and original native PNGs are linked separately for direct inspection.

**STOP:** the user's directive requires explicit human final-registration approval before extending the pipeline into G3-B. No mass artwork, main merge, public deployment or separate application change has occurred.
