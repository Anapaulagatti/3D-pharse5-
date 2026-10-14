# Studio progress

Current milestone: REFORGE-005 — Joseon Fantasy Reforge. Gates A/B/C/D/E DONE; PUBLIC-RELEASE-005 IN_PROGRESS (not yet deployed). The user explicitly authorizes finishing remaining tasks AND publishing v0.5: “tiếp tục hoàn thành những task còn lại và xuất bản bản v.05”. Do not ask again. No new districts.

Last independently matched remote checkpoint:6b7658cb610db014cb9dafb92a003163f6daee8c. Recovery tag checkpoint/v0.4-pre-reforge-005→9cc1381. Public v0.4 remains live; its HTML cd238a4c, all approved source/model/map/ZIP files and old staging script remain unchanged. Only the authorized Pages workflow is prepared locally to switch to v0.5; DO NOT push that workflow until final Gate E passes.

Gate A: user approved recommended A — Nari. Original three-concept board/approval preserved. Gate B: complete four-sided neutral Hanok,419modules/209support pairs0gaps, actual33views/stepped360 inspected; graybox source/GLB immutable. Gate C: real continuous bone-heat humanoid,28joint skin,20native clips,10morph expressions and native controller; source/C GLBs preserved.

Gate D accepted: separate hanok-reforge.blend/GLB and nari-messenger-art.blend/GLB, original packed256px PBR v2 maps; supported roof tile rolls/ornaments/joinery, actual doors/lattice, paved courtyard/planters/bench/plum/lanterns/banner/basin/historic silhouette backdrop. Day/evening/night, ambient3nativewind clips/flicker/ripples/particles, meaningful mascot/lantern/tree reactions, landing/celebration effects with Off/Reduced/Full, smooth focus/follow/orbit and responsive framing. Actual13world/face/mobile views opened, plus final face/20pose/side/rear/live galleries. Physical hanji depth.028 vs timber.065 fixes coplanar lattice flicker. Gate D final images quality-reports/v0.5/gate-d/final-layer-review. No material/geometry/rig changes remaining.

Final world:5,714,488B/75,514tri/60primitives/3clips; Nari2,923,840B/23,794tri/6primitives/1skin28joints/20clips/10morphs. Validator0errors0warnings; source weights normalized≤4, textures embedded, no remote decoders. KHR_mesh_quantization plus exact post-quantization weld; initial70zero-UV-area cap tangents get valid orthonormal fallback. All75baseline hashes passed before deployment work; current74unchanged and only explicitly authorized workflow update differs. Quantization base transforms retained for doors/ripples. World normal maps/environment/pointlights off in Low; Medium/High preserve detail. Low combined budget100ktri/<100draws, shadow-inclusive Med/High<210draws; no physical30/60FPS claim.

Gate E passed so far: production/typecheck; source/GLB/texture/privacy allowlist; exact74NariPNG capture (20livepairs/all20poses/10expressions/4sides), human galleries inspected; native9Lowcontrols/physics air/land/stairs/door/entry/gesture/pause/OS/touch on standalone; shared full-world physics6checks PASS. Final Nari SHA remains unchanged across latest world-only layer fix. Earlier wedges, context-reset, first-color/chin/quantization transform defects and failed tests retained; not called passes. First Medium native controller timed out while still moving under slow SwiftShader; final Low native flow passed. Tree test originally checked metrics before next render; render-awaited native trunk click passes. OS test must actually transition no-preference→reduce after manual override; repeating same emulation state emits no event. Current final-access retry addresses this, without changing application accessibility behavior.

Exact final standalone: showcase-v0.5/index.html,13,543,219B, SHA082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f. Direct Reforge entry,4verified embedded assets (world/Nari/actualv05poster/unchanged legacy companion download), inlineCSS/JS/licenses. No external assets/API/source maps. Static artifact allowlist index.html/.nojekyll only. Review ZIP includes tested PythonHTTP launcher and Windows launcher; extracted exact bytes, launcher active4188. Static subpath4187/3D-pharse5-/; no user-facing localhost links. Existing production preview4186. No dependency/lockfile changes.

Remaining: finish final-access OS/offscreen/mobile/WebGL tests, final exact HTML HTTP-browser check, genuine full gameplay capture/encode/visual review and final acceptance summary. Current capture-attempt-1 is partial/FAIL because getByRole excluded controls hidden by capture-only CSS; new capture uses includeHidden UI buttons and preserves native handlers/physics. Keep raw frames/original CDP timestamps, no speedup/interpolation/FPS claim. Then commit/push checkpoint, commit prepared Pages workflow, monitor Actions and inspect real public exact URL/SHA/images before claiming deployment success. Pages Source already GitHub Actions; API read succeeded, no active deployment at preparation. Old v0.4 artifact/script unchanged.

## NEXT SESSION HANDOFF

**Current milestone:** REFORGE-005, A/B/C/D DONE, E IN_PROGRESS, v0.5 publication explicitly authorized after verification.

**Current task ID:** REFORGE-GATE-E-005 then REFORGE-RELEASE-005.

**Last verified checkpoint:**6b7658cb610db014cb9dafb92a003163f6daee8c origin matched; later save follows.

**Completed work:** Approved concept/full supported Hanok/real rig/controller/art/PBR/lights/life; final actual source/rig/world/Low gameplay and privacy checks as above.

**Unfinished work:** Final access/extracted+subpath artifact proof, complete real gameplay video and review, final reports/checkpoint, authorized public release and actual public render verification.

**Files to inspect:** final-layer-review; gate-e/final-static-character and gallery; play-low; access-final-pass-2; capture/capture.json or failure.json; exact showcase-v0.5 build-info; prepared .github/workflows/showcase-pages.yml + Studio/scripts/prepare-reforge-pages.py. Before-after links should use final-layer-review.

**Known blockers:** None requiring user action. Cloud software renderer slow; physical GPU/FPS unmeasured (QA-004). Earlier usage-limit review failure resolved after reset; no bypass.

**Exact next action:** Collect running access/capture outputs, encode and inspect native frames, verify exact final static HTML/launcher, checkpoint accepted Gate E BEFORE committing/pushing prepared workflow. Do not regenerate models or add districts.

**Verification required:** Actual final access/context-loss/mobile/OS state and media review; then Actions deployment success plus public200text/html exact297d4e9c and real WebGL render/controls/fallback.

**Remote save status:**6b7658c verified. Public still v0.4. Local deployment files prepared but not committed; never publish while the required final tests are pending.

Final capture review found stale gesture replay after play→portrait Canvas change. Clear gesture on mode change; no asset/rig/physics changes. New final HTML 082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f; preserve earlier297d4e9c/126frame113.64s partial attempt. Recapture holds three actual interior compositor frames and waits for portrait Idle. OS reduced preference passes after true OS transition; offscreen test now waits for actual motion=false rather than a fixed400ms during slow render. Exact response hash uses an independent same-URL HTTP GET plus real browser200/render because Chromium evicts the13.5MB document body from inspector cache. Final access/media/artifact verification pending, no deployment yet.

Gate E COMPLETE: final access12checks PASS (realOS/offscreen/WebGL), extracted exactHTTP8checks PASS, final video185realframes/86s with decoded walk/run/jump/greeting/cheer/inside/Idlefaces inspected. Source297→082 change only clears prior gesture on mode switch; final artifact082c661b. All final GLB/build/privacy/rig/nativeplay gates pass; see quality-reports/v0.5/REVIEW.md and VERIFICATION_SUMMARY.json. Authorized PUBLIC-RELEASE-005 next, not deployed yet.
