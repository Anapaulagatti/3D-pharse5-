# V6 pixel sharpness and path system repair

Status: complete local technical review candidate. User visual approval remains pending. Final exact CI/independent-checkout facts are recorded in the actual verified checkpoint annotation after observation.

The edit target is the existing V6 at `543a572c1499fd53bb59ec51f21386599f7ee552`. Its complete recovery tag is `recovery/before-v6-path-sharpness-20261019`, pushed and independently peeled to that commit before edits. The new user-supplied blue issue image is retained verbatim in `issue-user-original.png`, with download/hash/dimension provenance. `issue-register.json` groups its marks into twelve repair areas in world coordinates. The cleaner full reference remains `../v6-restructure/reference-user.png`.

## Sharpness audit

V4 and original V6 were rendered at the same actual player/camera pose, zoom1, Canvas or WebGL, viewport1440×1140, DPR1, and native1024×768 canvas extraction. In the unchanged heritage comparison both renderer pairs are pixel-identical: no V6-specific native blur was detected. Both games already enable pixelArt/roundPixels, disable Canvas/WebGL antialiasing and use CSS `image-rendering:pixelated`. The WebGL texture-filter observer recorded only NEAREST. Canvas observation records smoothing at each image draw, rather than inferring it from restored post-render context state; image textures were drawn with smoothing disabled, including at zoom2.

An odd desktop viewport centers the canvas at a half-CSS-pixel coordinate; the actual browser screenshot was checked against native pixels and Chromium snaps it cleanly to the physical grid. This was not treated as evidence of blur. DPR2/3 and zoom0.5/1/2 evidence is retained. The native scene uses source pixels directly; source sprite/material files have not been sharpened or resampled.

The earlier browser-friendly overview reduces the4352×5312 world to1088×1328 using nearest sampling. It necessarily discards three quarters of the samples in each dimension; a browser fitting that image to another size can further rescale it. V6 also fits a taller world than V4 into the same preview area. A fitted whole-map thumbnail is therefore not a native gameplay sharpness comparison. New deliverables include a full native frame, an integer-half-size web overview, and actual1:1 gameplay crops. No sharpening filter or change to smooth movement is applied to disguise lost export detail.

## Path repairs

`assets-src/v6-path-fix/path-network.json` is the editable source of path widths, centerlines and destination courts. The terrain-only repair runs inside the existing V6 builder; it composes the approved native concrete/paver/sand/grass/basalt textures through recorded geometry masks. It does not call an image generator or draw generic replacement art.

- Local museum and civic joins: align the inherited dark path and the straight old-to-modern spine; keep traditional branch character outside the tiny repair envelopes.
- Side boulevards: remove empty north-facing stubs and begin the aligned streets at the real civic cross street.
- Station and retail: unite the station approach and stair landing, align bookshop/library/cafe paving, and route public circulation around the actual terminal mass.
- Attraction campus: replace backtracking joins with an attraction circuit, a clear entrance axis and purposeful ride/kiosk/hall courts.
- Namsan: retain nature trails and genuine tower/lookout stairs; consolidate their thresholds without adding an urban road through the garden.
- Waterfront and ferry: connect the promenade and actual deck stairs, retain both existing wooden pier images and the open-water ferry gap. Reuse literal native plank/beam pixels from the approved pier for the existing support-floor surfaces only; no new walkable water or changed body.
- Island: remove the inherited road envelopes before composing one coherent discovery network; connect the dock, oreum, lookout, village, learning garden and nature centre. The scenic southern loop avoids the unchanged orchard trunks and windbreak bodies.

All497prop placements,108approved prop sources,552collision rectangles,144Juni frames, land/walk masks, camera bounds, world size, spawns, portals, interactions, movement and UI are protected exactly. Ground outside the recorded edit mask is checked against the original V6 RGB checksum. The previous all-north-ground freeze is narrowed only for the explicitly requested local northern path fixes; every remaining northern pixel stays protected.

## Actual workflow and limits

Pinned Agent Sprite Forge `5324342fdfab72430f4e9604f3fe427009f8596d`; actual generate2dmap/generate2dsprite/generate2dmedia skills read, and original Gwanghwamun/Juni production records reused. Doctor diagnostics are retained; optional missing API keys, Grok and SVG renderer do not block processing existing PNGs. User prohibition on paid routes overrides the upstream key-based consent default. No provider, host-image, video-generation or new character/architecture production is authorized or executed for this repair.

Actual palette, bundle validation, linked navigation, Tiled export and composition commands are recorded in the existing V6 command ledger. Geometry is checked against the unchanged bodies with the original8×4footprint and declared shoulders, sampled every8pixels; no tolerance is relaxed. Initial trial route conflicts are retained as diagnostics and corrected by moving path centerlines, not obstacles.

Final build, exact rendered before/after, desktop/mobile traversal and package results will be recorded below only after execution. Cloud browser/mobile emulation is not a physical Android/iOS/Safari or hardware-GPU performance claim. Existing northern edge-canopy/compose-footprint and Juni small-motion notes remain inherited limitations. No main merge or deployment.

Initial WebGL toDataURL readback was INVALID because the real production preserveDrawingBuffer=false clears its backbuffer after presentation. Blank images and their invalid equality are retained under quality/diagnostics/blank-webgl-readback. The corrected proof uses actual DPR1 browser-compositor canvas screenshots (HUD temporarily hidden only for unobstructed evidence), with nonzero image content and zero changed V4/V6 pixels. No production WebGL settings were altered. Initial source-route trials and the first visually rejected candidate remain under quality/diagnostics; these are not passed final evidence.

## Executed final local verification

Production build/all stored-asset/type checks, lint, format and12unit tests pass. Original traversal suite6/6 passed with0skipped/flaky/unexpected; after the final island threshold-only surface correction the relevant island/mobile cases were rerun2/2 with0skipped/flaky/unexpected. Complete exact-commit CI and independent HTTPS clone/setup outcomes belong in the observed checkpoint/v6-path-sharpness-verified-20261019 tag, not an assumed status.

39active authored paths pass11,040strict feet/shoulder samples;12landmark thresholds touch real paving.497placements/108original prop images/552collision rectangles and144Juni frames remain intact; source/rendering/movement/UI, lockfile and workflow files are unchanged. Ground outside the exact authorized edit mask matches original V6 RGB, and land/walk masks remain byte-identical. Both linked Forge nav reports pass45world targets with0pockets/0thin gaps.

Matched nonblank Canvas/WebGL V4/V6 heritage captures have0changed native pixels;20display/filter checks cover odd viewport, DPR1/2/3 and zoom0.5/1/2.25final native Phaser captures plus full4352×5312frame, half2176×2656web overview and required comparison boards are retained. Actual forced softwareWebGL rendering/movement across5districts and genuinely disabled-WebGL Canvas rendering/movement pass with0critical errors. Normal no-QA production entry boots and moves through real keyboard input with0errors/external requests. Physical phones/Safari/hardwareGPU are unmeasured.

The exact ZIP was extracted and launched via its own Python HTTP server; source/ZIP native hashes match in5districts on desktop and emulated mobile, plus portrait, reciprocal ferry, Academy and retained previous-game guests. 83760786bytes,851distfiles, SHA256`31070fc4421514b3f5b599b47861a27ae3365e30332b12098163d3aae665d712`. See quality/verification.json and package.json for executed results. Static allowlist/hash/credential-pattern audit and original notices are retained. No source/3D/private files are included in the static package; the pattern scan is not an exhaustive certification.

Actual 48Sprite Forge processing commands are preserved in assets-src/v6-path-fix/forge-commands.json, including intermediate validation/export passes.0new image/video/provider calls. Northern clipped-canopy warnings/footprint skips and inherited Juni small-motion notes remain visible in raw reports. No main merge or public website deployment. STOP for user visual review after verified source checkpoint handoff.
