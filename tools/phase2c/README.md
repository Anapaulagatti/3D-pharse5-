# Phase2C authoring and evidence tools

These tools write only derived Phase2C assets/evidence. Approved bases and old sources are read-only. Do not import historical front/back restoration scripts: some have top-level historical write behavior.

The review candidate is already authored. Do not regenerate it simply to review. `protected.py`, `source_qa.py` and native readback tools verify it without rewriting approved artwork.

Authoring order for a deliberately new revision: `foundation.py` → real `foundation_capture.mjs` / `foundation_readbacks.py` → foundation checkpoint → `collection.py pilot` → real pilot capture/readback → `collection.py full` → QA. `designs.py` contains the native art recipes. `refresh_accessories.py` and `refresh_festival.py` are narrowly scoped repair helpers, not base exporters. Keep per-file provenance, pose bindings and content revisions. Any new base gait requires a real pose migration and review; never change only a hash to bless stale art.

`studio_upgrade.py` is a historical one-time implementation patch script, **not idempotent; do not rerun**. `merge_captures.py` is also a one-time merge and must not be applied again to the already merged192-row result. Final immutable reports and PNGs are the review record; temporary working journals are ignored.

Runtime capture tools require the local Vite/preview ports recorded in each script, Chromium and Playwright. Recording uses systemFFmpeg through `PLAYWRIGHT_BROWSERS_PATH=/tmp/phase2b-playwright` with `ffmpeg-1013/ffmpeg-linux` pointing to `/usr/bin/ffmpeg`. `media.py` preserves source dimensions/timing and creates lossy review MP4s; native PNG remains pixel authority. Sources use Pillow/NumPy. No paid image service is involved.

`build_review.mjs` creates an independent relative-base build in `/tmp/phase2c-review`. `package.py` includes only actual runtime dependencies, compact native sheets and five representative gameplay videos. Remaining videos/crops/full native screenshots are linked at the immutable final review tag. `package_smoke.mjs` runs against an independently extracted ZIP at localhost4362, using normal UI/input. Native readback observes an actual rendered pose; it does not force the player frame.

Human art acceptance and physical-device performance remain separate. Phase3 is locked.
