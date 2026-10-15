# Korean Arena — Living Pixel Seoul

ONE original unified pixel social-town art proof, V4 Gate2. All prior A/B/C rejected. Current build reuses Phaser4/TypeScript/Vite and implements a single modular Central Plaza, layered32×48 avatar, true four-direction idle/walk/run, wave/celebration/social pose, two hairstyles/two outfits/satchel. No real online players; Mira is a local demo NPC.

## Run

Node24+, exact npm lock; existing packages first. `bash tools/setup.sh` verifies prerequisites, source/asset QA, types/lint/format/unit/build/browser checks without regenerating art. `npm run dev` from this root starts development; production `npm run build` then `npm run preview`. Base `/3D-pharse5-/`. Cloud loopback is internal, not a public preview link.

WASD/arrows walk, Shift runs, E talks near Mira, Space waves. UI and touch buttons provide alternatives. Try clothes/hair/accessory,1×/2×/3×, pause/reduced motion. HTML dialogue uses readable Korean/system fonts. Source is original native image_gen pixel objects plus code-raster layered chibi/ground; source atlas/crops/palette/native exports preserved. No copied game pixels or whole-scene illustrated background. See PIXEL_ART_BIBLE.md and assets-src/unified-v4/manifest.json.

## Review and approval

quality-reports/unified-v4/REVIEW.md contains final actual engine images/video and viewing instructions. Portable package under downloads/unified-v4, unzip then `python3 start.py` (Windows `py start.py`), open printed HTTP URL. Python required; Node not required to view. Gate2 technical readiness is not user visual approval.

STOP before Gate3, public replacement or further gameplay. Full roadmap in docs/UNIFIED_V4_ROADMAP.md and35design entries in docs/UNIFIED_V4_MINIGAMES.csv. First Delivery, two minigames, learning courses, real social/multiplayer/PvP and optional disabled rewarded ads are planned, not shipped. All learning/exam paths remain free by design.

## Recovery

Previous rejected pixel checkpoint2554327/tag checkpoint/pixel-art-reset-v2-review-20261015. Complete3D remote archive f1f13f2/tag checkpoint/3d-before-pixel-v3-20261015, fresh2738file hash recovery repeated at V4Gate0. Exact recovery steps docs/reviews/unified-v4/RECOVERY.md. Existing Pages retains publicv0.5. No force/history rewriting, no separate Korean Arena main app changes.
