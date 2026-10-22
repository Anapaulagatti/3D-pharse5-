Current revision: [final masterplan review](FINAL_MASTERPLAN_REVIEW.md). Art provisionally approved; final planning approval pending; Gate 2 locked. Packaging excludes its own prior ZIP/GitHub verification receipts to avoid stale self-verification claims.

# Reproduce without generation or deployment

Use the unchanged package-lock and Node24+. Fresh dependency setup: `npm ci --ignore-scripts --cache .cache/npm`. In this session the already verified lock-matching node_modules was reused; no fresh-install success is claimed. Python3 is required for offline navigation/packaging, Chromium at /usr/bin/chromium for browser verification. No provider keys or image tools needed.

1. `npm run dev -- --port 4240`; isolated entry `/3D-pharse5-/world-gate1.html`.
2. `python3 tools/world_gate1_validate.py` (source preservation + 16px grid reachability).
3. `npm run typecheck`, `npm test`, `npm run lint`, `npm run format:check`.
4. `npm run build` checks preserved original app (known large-chunk warning). `npx vite build --config world-gate1.vite.config.ts` builds this separate preview.
5. `node tools/world_gate1_review.mjs`: actual Phaser input/route/nearest/mobile tests and screenshots. Requires dev server above. No map generation or provider call.
6. `python3 tools/world_gate1_package.py`; `node tools/world_gate1_verify_package.mjs`: ZIP extraction, manifest hashes, own HTTP server, keyboard and real CDP touch.

The package contains preview code/Juni plus explicitly labelled reference images and review material. Its own post-pack verification receipt is supplied beside the ZIP in this repository; it cannot be included as proof of its own future archive bytes. Runtime source updates require rebuilding/retesting before repackaging. Native canvas export is 4096×4608 at zoom1/DPR1; browser overview is intentionally scaled and labelled.

Pinned Forge generate2dmap/codeart2d instructions read; custom graybox/data/browser tools executed. No Forge generation/bundle/Tiled acceptance is claimed, no billable route called. No final artwork is produced in Gate 1. Human approval remains pending.
