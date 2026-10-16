# Living Seoul — actual art and map execution

Authority: [user specification](../current/BUILD_LIVING_SEOUL.md), approved immutable4096×3072masterplan. First finished candidate is northern4096×1728at original coordinates; remaining buildings, connected stream/pond/two bridges and new NPCs wait for Stage B approval.

Actual upstream Agent Sprite Forge revision5324342fdfab72430f4e9604f3fe427009f8596d, MIT. Applicable generate2dmap / generate2dsprite / generate2dmedia SKILL.md and layered-map/prop contracts were read before production; registry and earlier Juni/Gwanghwamun reports reused. Doctor ran with host_image capability:0FAIL,0WARN,7optional tools missing; no video generation route. Existing Juni144frames remain pixel-identical; no video2dsprite action generation or new NPC production claimed.

Ten actual referenced host `image_gen` calls produced2architecture study sheets, gate, academy hall/wings, workshop, museum, wall kit, science kit and targeted museum-volume correction. All originals, prompts, actual reference paths, returned sizes/hashes and route metadata are retained in assets-src/seoul-production/image-route.json. Built-in route does not expose model or USD estimate: both null. Paid API/provider requests0. A configured key was never treated as authorization; `FORGE_MAX_PAID_REQUESTS=0` on CLI processing. No claim of provider video or CLI image generation.

Actual pinned commands and full stdout/stderr/exit codes: assets-src/seoul-production/commands.json. Reproducible authoring entry points (optional external Forge cache required; never run during setup):

```sh
python3 tools/production_art.py --studies
python3 tools/production_art.py --production
python3 tools/build_seoul_production.py
python3 tools/production_preview.py
python3 tools/production_boards.py
```

These execute real `extract_prop_pack.py` measured boxes / connected-component alpha / radius3despill, `finish_frames.py hd` premultiplied area finishing, `palette_tool.py build/apply` shared192colors without orphan deletion; `map_bundle.py hash/validate`, `map_nav.py check` with reciprocal linked room, `export_tiled.py export --embedded-variant`, `compose_layered_preview.py` with real collision audit. No code-painted replacement building or floor artwork. Authoring road/court geometry and terrain alpha masks is map DATA; RGB comes pixel-exactly from the accepted generated granite/earth/grass textures. Native atlas includes reusable alpha-edge variants, not certified seamless/Wang tiles. No GUI Tiled verification claimed.

Architecture Art Bible has14original studies at approximate declared0.5world-relative scale. Future civil/cultural/residential studies are CONCEPT ONLY, not mass-produced runtime districts. Native identity board uses completed Stage B assets and unchanged Juni at1x, not a Phaser screenshot. Separate quality/Phaser PNGs prove actual rendered runtime.

Initial institution-sheet extraction FAILED `Accepted props touch a cell edge` for all6studies: the image model inserted white panel rules. Raw source retained; measured boxes were inset3source pixels to exclude actual rule/antialias margins, then strict edge rejection passed. No threshold relaxation or painting replacement. Initial shallow museum was visually rejected by agent; original retained and a real referenced generation corrected its volume. First browser test drafts used fixed sleeps, synthetic pointer events and omitted lesson Next button; those test harness errors were corrected using position polling, real CDP touch and the existing lesson flow. Raw local attempts remain in.cache/production; no failed attempts represented as success.

Current retained composition warning: `bounds`,9clipped edge-tree canopies, off_canvas0/empty0, threshold `visible pixels (alpha > 16) inside the canvas`. Exact IDs/value/file in quality/retained-warnings.json. Those trees deliberately continue orchard/background foliage beyond the north edge; their trunks remain in-bounds and traversable reservations are clear. Compose actor checks skipped because composition board contains no actor; actual Juni scale/occlusion/movement are verified separately in Phaser. Earlier approved Juni right-idle/small-wave strict warnings remain historical limitations; no new animation QA success inferred.

Official unmodified Forge browser verifier ran over HTTP through tools/verify_map_preview.py; actual21/21routes,26/26assets, keyboard, pixel Y-sort and no external requests/errors PASS (read exact counts in quality/forge-http-verification.json). This diagnostic uses Forge's marker, not Juni. Real Phaser checks and screenshots are separate. Static nav represents the main gate OPEN; browser tests separately prove closed/open/safe-close collision and the closed inner palace.

Offline setup: `bash tools/setup.sh`; validates stored art only, never generates. Optional numpy/scipy/Forge tools are authoring caches, not new game/setup dependencies. Browser evidence is emulated Chromium, not a physical-phone FPS certificate or artistic approval.

Final visual audit found side arches looked open while permanently blocked. Reused the actual generated door-pair prop for two closed side-leaf overlays; no new image/provider calls or geometry changes. Central runtime leaf remains interactive; static map/nav represents its open state. Updated native board/stills, continuous gameplay and exact HTTP ZIP after the correction. Video encoding and decoded-frame evidence are reproducible through tools/finish_seoul_review.py (FFmpeg15fps/CRF30; encoded FPS is not measured game FPS).
