# Three illustrated NPC pilot tools

New primary source route:host_image `image_gen.imagegen`,7actualcalls,not code-painted sprites. Source/direction/pose provenance in assets-src/npcs/phase3a-art-rebuild/run-manifest.json. No external paidAPI/video/agent. Pinned SpriteForge/Creator diagnostics documented in docs/phase3a-art-rebuild/ART_PIPELINE.md;tools never weaken those thresholds. AIvideo generation unavailable;approved own-source PNG-layer workflow used.

Dependencies:Python3,Pillow12.3.0,NumPy2.3.5,SciPy1.17.0;existingNode24/npm/Phaser4.2.1/Playwright;systemChromium/FFmpeg. No new game runtime dependencies. Optional tools remain in /workspace/tooling-cache at exact requested commits,not vendored. Runtime assets are finished PNG atlases only;no authoring dependencies needed to play.

Reproduce only the3pilots in the full Git repository:

1. prepare.py — crop explicit source ownership,one fixed scale,shared native palette/binaryalpha.
2. native_retouch.py — explicit own-palette eye edits and fixed per-view head registration.
3. props.py — actual illustrated source-prop extraction.
4. rig.py — actual image-alpha limb masks/manual joints/own-source occlusion recovery.
5. animate.py --export — existing protected pure PNG-affine helpers,Juni numeric front/back poses,accepted forward stance profile;104cells,unchanged atlas mappings.
6. audit.py/head_qa.py — source/alpha/ownership/connected anatomy/loop/raster/preservation/literal head checks.
7. skill_qa.py — pinned unmodified third-party diagnostics;requires fresh output directories,all original FAIL/WARNs retained.
8. capture.mjs — actual AFTER canonical gameplay;--before uses exact checkpoint PNG bytes at original URLs. --only=npc-harin resumes valid other pilots from working JSON. No pose/route/position/clock override. Some Harin heading/frame combinations are unreachable on frozen12pxsegments;do not modify routes to force evidence.
9. inspector_capture.mjs — separately labelled actual Phaser clip utility,not canonical-world proof.
10. readbacks.py/gallery.py — exact source-versus-real-render controls,foreground ownership records,native comparisons,lightweight reviews.
11. media.py — unretimed/unscaled1280×900 compression-only MP4s.
12. build_review.mjs/package.py — portable actual game plus supplemental inspector,3source packs and all required canonical runtime dependencies. package_npcs/package_characters/package_inspector and package_verify exercise the independent extraction/runtime/SHA/CRC. Source authoring audits require full original Git history,not just the standalone play ZIP.

Recordings need PLAYWRIGHT_BROWSERS_PATH=/tmp/phase2b-playwright with ffmpeg-1013/ffmpeg-linux pointing to /usr/bin/ffmpeg. The review server bindslocalhost4388 by default;--lan is explicit local-network opt-in,not publicdeployment.

Never run the rejected tools/phase3a/art.py for new production. Never write the original12players,28cosmetics,world,collision,NPCdata or engine. Elevenremaining rebuilds/Phase3B LOCKED until explicit human approval. No delegation,no mainmerge/deployment.
