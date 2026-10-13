# Studio progress

- Current milestone: first golden-slice task complete; next development milestone 8 (not started).
- Current task ID: SHOWCASE-001 (DONE; latest user request to see index.html). WORLD-001 remains the next unblocked development task, not started by this viewing request.
- Last completed task: SHOWCASE-001 / actual interactive app packaged into one downloadable HTML and offline content verified.
- Last verified remote checkpoint: 68ea4880d3db5662aa772a1976718d0661c1dbe4, independently confirmed before the showcase checkpoint. The new showcase checkpoint follows in git log and will be checked after push.
- Last checkpoint date/time: 2026-10-13 11:48 UTC.
- Latest session: reused all existing packages/models/art; added showcase/index.html (7,493,330 bytes), seven checksum-verified embedded exports, inline app/styles/license notices, build metadata, opening instructions and actual screenshots. Changed Poster to resolve via assetURL and set GLB download filenames. No asset regeneration, framework changes or optional tool installation.
- In progress: remote checkpoint saving for this HTML delivery. SHOWCASE-002 (personal-desktop direct-file verification) blocked by cloud managed-browser policy; offline content checks passed. install/start draft from previous session remains separate from GitHub and Publish.
- Files created/modified: four STUDIO records and AGENTS.md; Studio/modeling/; asset build/sync/verify/recovery scripts; preview/src/, tests/package scripts; .blend/GLB/texture/poster sources and exports/v1/; ASSET_MANIFEST.csv; art/camera/material/license/performance/QA/handoff docs and quality-reports/. See Git commits for exact diffs.
- Assets generated: original three-direction concept, 2 editable models, 2 embedded/source textures, 3 actual rendered posters, 6 distinct mascot pose captures. Inventory is STUDIO_ASSETS.md.
- Exported GLBs: arena-hero (3,379,732 bytes, LanternSway), mascot-base (289,652 bytes, six 2s clips). Both Validator 0 errors / 0 warnings.
- Dependencies: existing pinned tools reused; @gltf-transform/core and extensions 4.5.1 declared directly for bounds/topology/sampler analysis (already installed transitively). No framework upgrades, optional sprite forge or paid external provider.
- Successful commands: assets:pack with exact sample/topology/bounds checks; assets:verify with file/source checksums; actual-model gltfjsx generation; typecheck/Vite build; browser suite 9 passed, 0 failed/skipped; recover-check.sh reused installed packages and repeated build + all 9 tests with outputs in ignored cache. Transparent portrait rendered in Cycles with unsupported denoising disabled.
- Fixed defects: Html/Suspense DOM cleanup during scene switching; demand-mode clip changes missing invalidate; paper leaf placement/normals and brass seam; unavailable OIDN; resampling caused tiny render differences, now disabled and sampler arrays kept exact. Raw/optimized Celebration captures are byte-identical after correction.
- Known limits/blockers: cloud SwiftShader renders only ~3.3 FPS in a short sample, no physical GPU/phone available for >=50/30 FPS acceptance. QA-004 BLOCKED; low mode cuts draw calls 152→69 but software FPS remains slow. Large lazy 3D JS chunk ~1 MB minified. Six learning districts remain TODO. See PERFORMANCE_REPORT.md.
- New successful commands: showcase:build; showcase:verify (6 offline functional checks, zero external requests/JS errors, exact downloadable GLB checksums); preview typecheck/build; 2 targeted served-preview regression tests passed. Earlier full 9-test baseline remains recorded above; it was not rerun in full for this viewing request.
- New evidence: showcase/build-info.json records HTML checksum 21188f32ac760531c043f300c63160511bb886edecb094c3073f7456e50259a3; quality-reports/showcase-offline.json explicitly records file:// blocked and the same HTML bytes rendered in about:blank offline. Four showcase screenshots preserve actual render/fallback evidence.
- Exact next action for viewing: download showcase/index.html to a personal desktop, keep its .html extension, open with Chrome/Edge; see showcase/README.md for an HTTP fallback. Direct-file opening on that device remains unverified here. When development is requested again, begin WORLD-001 with one reusable Hangul Garden slice; QA-004 still needs physical target hardware.
- Recovery: read all four STUDIO files and AGENTS.md, inspect git status/log and assets. Reuse node_modules/exports; run recover-check.sh only if restoration/verification is needed. Never repeat native image generation or rebuild saved models without a reason. Each cloud task is isolated; no Git worktree needed.

## NEXT SESSION HANDOFF

**Current milestone:** First arena/mascot slice delivered; next M8 expansion, with device profiling QA-004 still blocked.

**Current task ID:** SHOWCASE-001 DONE; SHOWCASE-002 blocked by cloud browser file policy. WORLD-001 TODO and QA-004 blocked on target hardware remain unchanged.

**Last verified checkpoint:** 68ea488, previous handoff independently matched remote main before this session's showcase checkpoint. Inspect newest git log/remote main for the following delivery checkpoint.

**Completed work:** Prior v0.2 slice retained. Added actual single-file showcase, verified embedded assets/downloads, six offline content checks and two targeted served-preview regression tests; preserved four new screenshots and opening/build instructions.

**Unfinished work:** Direct file opening on personal desktop (cloud policy prevents testing it), physical-GPU performance/LOD, six learning districts and full world library. This viewing request does not authorize starting new districts now.

**Files to inspect for viewing:** showcase/index.html, showcase/README.md, showcase/build-info.json, quality-reports/showcase-offline.json, Studio/scripts/build-showcase.mjs and verify-showcase.mjs. Prior modeling/source references remain unchanged.

**Known blockers:** Managed Chromium URLBlocklist blocks file://; did not bypass policy. Same HTML renders offline in about:blank; do not mark direct-file testing passed. No physical GPU/phone; software ~3.3 FPS is not device acceptance.

**Exact next command or action:** Read four progress files/AGENTS and check git status/log/remote. For user viewing, provide saved showcase/index.html and actual screenshot; do not rebuild it or models merely to open it. If app/export changes later, run npm --prefix Studio run showcase:build followed by showcase:verify with installed modules. Start WORLD-001 only on a further development request; no concept/model regeneration for recovery.

**Verification required:** SHOWCASE-002 direct-file test on a personal desktop browser; QA-004 physical hardware FPS. Offline content is already verified. Future districts still require existing model/export/render gates.

**Remote GitHub save status:** Previous 68ea488 was verified; new showcase delivery checkpoint will be pushed and independently compared with origin/main. On recovery compare newest local HEAD/remote rather than resetting. Previous install/start draft is separate; no environment draft/network changes were needed for HTML delivery.
