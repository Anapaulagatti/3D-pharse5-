# Reproduce stored V10 production

Ordinary review/setup uses the committed native/runtime outputs and never generates art. Run `npm ci --ignore-scripts` and `bash tools/setup.sh`; no Forge or provider credentials are required. Play the ZIP through `start.py` over local HTTP.

Authoring tools in this run: Python3.12.14, Pillow12.3.0, numpy2.3.5, scipy1.17.0; Forge at `/workspace/tooling-cache/agent-sprite-forge`, pinned5324342fdfab72430f4e9604f3fe427009f8596d. Source sheets/prompts are retained. Host image generation is not deterministic and is never replayed by setup.

To intentionally reprocess original art in an independent disposable authoring clone, preserve committed native outputs first and use clean owned output destinations for the extraction/material/palette steps. `python3 tools/v10_prepare_art.py` performs measured extraction and uniform fitting. Forge refuses pre-existing export directories; do not remove useful caches blindly or relax strict QA. Follow the exact palette build/apply commands in `art-processing-log.json`, copy the final palette outputs back to native, and refresh `pixel-finish.json`/native SHA values. The committed original hash manifests make final inputs independently auditable; command receipt paths identify the actual authoring run.

`python3 tools/v10_final_build.py` composites only approved geometry, new native art and protected north. Do not run `v10_plan.py` or the old graybox compiler over final outputs. The plan SHA assertion deliberately rejects rezoning. The final collision refinements are new decoration placement and door-approach landscaping only.

After any authorized runtime asset/collision mutation, retain the previous hashed bundle as a receipt and generate a fresh one with `map_bundle.py hash`. Run strict bundle validation, road clearance, `map_nav.py check` in a new directory, Tiled export/readback, scene preview and unchanged upstream browser verifier. Refresh `qa/nav-report.json`, `qa/nav-debug.png` and `qa/provenance.json` only after the new checks pass; offline setup rejects stale proofs. Scene preview's debug actor is not Juni and is never presented as actual Phaser evidence.

Actual engine evidence scripts: `v10_final_capture.mjs`, `v10_walkthrough_routes.py`/`v10_walkthrough.mjs`, `v10_performance.mjs`, `v10_final_package.py`, `v10_verify_final_package.mjs`. Read their entry URL/camera/recording annotations before use. Walkthrough navigation uses normal keyboard controls at unchanged speeds; screenshot/performance camera placement is disclosed. No script injects player positions during the full walkthrough.

Diagnostic-only source audit may compare hashes of archived assets. It is not a build dependency and must never export legacy coordinates/textures into production. The approved northern screenshot is used only for preservation comparison.
