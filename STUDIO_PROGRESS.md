# Verified handoff — animation, historical guests and cleanup

Gates A–E are complete as a review candidate. Read AGENTS.md, docs/current/MISSION.md and all four STUDIO records before resuming. Stay in this repository and preserve unknown work. No further implementation or publication until user visual feedback.

## Review

Current files are in docs/review: avatar-review-board.png, town.png, mobile.png, animation-review.mp4 and playable-review.zip. The board labels source-atlas views separately from actual Phaser crops. The 40.28-second video contains an actual archived BEFORE excerpt followed by 34.47 seconds / 816 compositor frames of actual current gameplay. Original timestamps are preserved; no pose injection, teleporting or speed change. Decoded walk/run/stop/turn/emote frames and a natural blink were visually inspected.

Extract the ZIP, enter Korean-Arena-Review and run `python3 start.py` (Windows: `py start.py`). Open the printed HTTP URL. Python 3 is needed; Node is unnecessary for viewing. The exact extracted ZIP was tested through its HTTP launcher on desktop and emulated mobile DPR2, including real input, native CSS pixels, all four guests and no missing requests or critical console errors. Do not provide cloud loopback as a public preview.

## Source and verification

Fresh depth-one HTTPS clone of `3a22e62de62abd598f0ad0d24b95ddbb9f1fd98c`: npm ci, type/lint/format, 8 unit tests, production build/source QA and 5 Playwright flows passed. Every built file matches the review ZIP manifest. Source CI 38720697542 succeeded. Prior assertions incorrectly equated frame count with elapsed simulation time and sampled patrol endpoints; the verified fix changes tests only. No art/runtime changes followed capture and packaging. docs/current/clean-clone-verification.json records actual results.

Current hero: 48×68 padded canvas, root24,64, 284 frames ×11 layers; sixteen accepted neutral master combinations unchanged. Four guests: 196 frames each, shared anatomy/palette, original historically informed costumes, Vietnamese-first dialogues and concept-only hooks. World: 24 source files, generated original object atlas/provenance and map preserved byte-for-byte. Current source/runtime/generator pixel equality, palette, binary alpha, gutters, no clipping, 77 colliders, eleven reachable landmarks and all patrol footprints pass.

Forge: all five skills inspected; fifteen free commands actually executed, including registration of 24 walk/run frames, two clips with zero warnings and six passing pixel-QA envelopes. Video route unavailable. Outline heuristics explicitly skipped; map CLI capability check is not Forge map generation. No paid calls, image model or copied portraits. See docs/SPRITE_FORGE_USAGE.md.

## Recovery and publication boundary

The active tip contains 193 tracked files, down from 5948; old files remain in immutable recovery tags and full Git history. Pixel tag3b62e9b and 3D tagf1f13f2 were freshly remote-cloned and all 5948/2738 tracked files hashed; pre-cleanup current guest tagbd241a9 was independently verified on origin. See docs/RECOVERY.md. No force-push or history rewrite.

Cleaned source was fast-forwarded to main after source CI and Pages inspection. Legacy workflow383196743 was disabled; the new tree contains read-only pixel CI only. Public Pages remains the old separately deployed v0.5 artifact (SHA256082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f), verified before/after source promotion. This review game has NOT been deployed. Final exact SHA, both branch refs and CI result are recorded in annotated tag checkpoint/pixel-animation-history-cleanup-20261015; never retarget it.

## Resume environment

Reuse exact Node24+/npm/Pillow12.3.0/Chromium/ffmpeg dependencies. `bash tools/setup.sh` validates without regenerating art. Dev4200 and production preview4201 serve /3D-pharse5-/. Restart processes after a snapshot and verify actual HTTP/Phaser readiness. assets-src contains editable current PNG atlases/master frames/JSON and original deterministic authors; transient frames and QA live in ignored .cache. No unnecessary regeneration.

Physical phone performance and Windows GUI launcher are untested. No 60 FPS guarantee or user visual approval is claimed. Historical educational content needs qualified review before lessons are published. Environment configuration Review/Save/Publish, Git checkpoints and public website deployment are separate actions.
