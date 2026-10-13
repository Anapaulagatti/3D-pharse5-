# Studio progress

- Current milestone: first golden-slice task complete; next development milestone 8 (not started).
- Current task ID: WORLD-001 (TODO; next unblocked development task).
- Last completed task: SAVE-001 / confirmed remote artifact checkpoint and saved cloud recovery configuration.
- Last verified remote artifact checkpoint: 80bfc2a72f17469634d7c3513515f074a0c3b6bc; local HEAD matched GitHub main after push. This handoff update is saved in the following documentation checkpoint.
- Last checkpoint date/time: 2026-10-13 18:22:50 UTC+07 (Asia/Saigon).
- Latest session: reused working setup, saved persistent recovery records and supplied prompt; produced three concept alternatives, selected A, generated real arena/mascot .blend and GLB, exported six character clips plus lantern sway, implemented GLB preview/POIs/night/quality/static fallback, optimized and verified exact animation data, generated posters and inventory.
- In progress: none for the first-task delivery. install_script/start_skill draft save confirmed; user review/save/Publish remains separate.
- Files created/modified: four STUDIO records and AGENTS.md; Studio/modeling/; asset build/sync/verify/recovery scripts; preview/src/, tests/package scripts; .blend/GLB/texture/poster sources and exports/v1/; ASSET_MANIFEST.csv; art/camera/material/license/performance/QA/handoff docs and quality-reports/. See Git commits for exact diffs.
- Assets generated: original three-direction concept, 2 editable models, 2 embedded/source textures, 3 actual rendered posters, 6 distinct mascot pose captures. Inventory is STUDIO_ASSETS.md.
- Exported GLBs: arena-hero (3,379,732 bytes, LanternSway), mascot-base (289,652 bytes, six 2s clips). Both Validator 0 errors / 0 warnings.
- Dependencies: existing pinned tools reused; @gltf-transform/core and extensions 4.5.1 declared directly for bounds/topology/sampler analysis (already installed transitively). No framework upgrades, optional sprite forge or paid external provider.
- Successful commands: assets:pack with exact sample/topology/bounds checks; assets:verify with file/source checksums; actual-model gltfjsx generation; typecheck/Vite build; browser suite 9 passed, 0 failed/skipped; recover-check.sh reused installed packages and repeated build + all 9 tests with outputs in ignored cache. Transparent portrait rendered in Cycles with unsupported denoising disabled.
- Fixed defects: Html/Suspense DOM cleanup during scene switching; demand-mode clip changes missing invalidate; paper leaf placement/normals and brass seam; unavailable OIDN; resampling caused tiny render differences, now disabled and sampler arrays kept exact. Raw/optimized Celebration captures are byte-identical after correction.
- Known limits/blockers: cloud SwiftShader renders only ~3.3 FPS in a short sample, no physical GPU/phone available for >=50/30 FPS acceptance. QA-004 BLOCKED; low mode cuts draw calls 152→69 but software FPS remains slow. Large lazy 3D JS chunk ~1 MB minified. Six learning districts remain TODO. See PERFORMANCE_REPORT.md.
- Exact next action: when continuing development, begin WORLD-001 with one reusable Hangul Garden slice. Obtain target hardware results for QA-004 independently; do not label it passed.
- Recovery: read all four STUDIO files and AGENTS.md, inspect git status/log and assets. Reuse node_modules/exports; run recover-check.sh only if restoration/verification is needed. Never repeat native image generation or rebuild saved models without a reason. Each cloud task is isolated; no Git worktree needed.

## NEXT SESSION HANDOFF

**Current milestone:** First arena/mascot slice delivered; next M8 expansion, with device profiling QA-004 still blocked.

**Current task ID:** WORLD-001 (TODO), QA-004 blocked on target hardware.

**Last verified checkpoint:** 80bfc2a, artifact/QA checkpoint independently matched remote main; current documentation checkpoint follows in git log.

**Completed work:** Two real model/source pairs, seven exported model/texture/poster files, six mascot clips, animated lanterns, interactive GLB app and safe fallbacks, manifests/provenance, exact optimization parity, build and nine tests.

**Unfinished work:** Physical-GPU performance/LOD decisions, six learning districts and full final world library.

**Files to inspect:** STUDIO_TASKS.md, ART_BIBLE.md, concepts/DESIGN_REVIEW.md, Studio/modeling/common.py and arena.py, preview/src/SceneView.tsx, exports/v1/asset-manifest.json, PERFORMANCE_REPORT.md.

**Known blockers:** No target hardware. Cloud software ~3.3 FPS; do not claim phone/desktop acceptance. No missing secret/account is blocking art development.

**Exact next command or action:** Check git status/log and remote main; if installed modules are valid, use npm --prefix preview run dev. For WORLD-001, create one original Hangul Garden variant from the existing craft/material kit and checkpoint before export. Do not regenerate completed arena/mascot/concept to begin a new session.

**Verification required:** Future district raw/optimized Validator, exact topology/bounds/sampler checks, desktop/phone viewport and actual render review; target hardware measurements for QA-004.

**Remote GitHub save status:** 80bfc2a full model/QA/artifact checkpoint was pushed and independently verified; final handoff documentation follows. On recovery confirm newest local HEAD/remote main instead of resetting to an older checkpoint. install_script/start_skill draft saved successfully, requires user review/save/Publish; publication and fresh-task restoration were not claimed.
