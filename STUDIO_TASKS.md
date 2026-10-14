# Studio task checklist

Statuses: TODO, IN_PROGRESS, DONE, BLOCKED. DONE requires outputs and verification. Milestones follow the persistent-progress prompt (nine milestones).

Current task: ART-PIVOT-006 concept DELIVERY COMPLETE; PIVOT-APPROVAL-006 awaits user choice. STOP before full remodeling/prototype; public v0.5 preserved.

| Milestone | Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|---|
| 1 Environment | ENV-001 | Audit existing checkout, tools and version compatibility | DONE | d355dca baseline; Node 24.19, React 19.3/R3F 9.8/Drei 10.7, Blender 4.3.2 |
| 1 Environment | ENV-002 | Preserve recovery records and supplied master prompt | DONE | Four root STUDIO files, AGENTS.md, STUDIO_MASTER_PROMPT.md |
| 2 Pipeline | PIPE-001 | Blender export, Validator, glTF Transform, gltfjsx tooling | DONE | quality-reports/toolchain-validation*.json; existing smoke fixtures |
| 2 Pipeline | PIPE-002 | Load exported production GLB in the existing React preview | DONE | Actual served GLB hash and nine browser tests |
| 3 Art direction | ART-001 | Three distinct mascot/world explorations and selection rubric | DONE | concepts/mascot-directions-v1.png and DESIGN_REVIEW.md |
| 3 Art direction | ART-002 | Color, materials, silhouettes and camera standards | DONE | Existing ART_DIRECTION.md is the starting point |
| 4 Hanok Arena | ARENA-001 | Editable curved roof, timber, courtyard, garden and skyline | DONE | QA_CHECKLIST.md, current exports/manifest and 9 passing browser tests |
| 4 Hanok Arena | ARENA-002 | Export GLB, inspect, optimize and validate | DONE | |
| 5 Mascot | MASCOT-001 | Selected original character model and editable Blender source | DONE | QA_CHECKLIST.md, current exports/manifest and 9 passing browser tests |
| 5 Mascot | MASCOT-002 | Six distinct exported animation clips | DONE | Idle, Happy, Thinking, Celebration, Disappointed, Greeting |
| 6 Animation/polish | PREVIEW-001 | Lighting, camera, POIs, animated lanterns and restrained atmosphere | DONE | QA_CHECKLIST.md, current exports/manifest and 9 passing browser tests |
| 6 Animation/polish | PREVIEW-002 | Real asset info, loading, failure states and reduced motion | DONE | Existing accessible controls/fallback are preserved |
| 7 Optimization/QA | QA-001 | GLB stats, clip parity, checksums and provenance manifest | DONE | |
| 7 Optimization/QA | QA-002 | Build, desktop/phone viewport, animation and fallback browser checks | DONE | Baseline five tests passed in d355dca; rerun after changes |
| 7 Optimization/QA | QA-003 | Render review, fallback posters, transparent mascot portrait | DONE | QA_CHECKLIST.md, current exports/manifest and 9 passing browser tests |
| 8 Districts | WORLD-001 | Hangul Garden, Vocabulary Café, Grammar Library | TODO | Start only after golden slice is reviewed |
| 8 Districts | WORLD-002 | Listening Subway, TOPIK Academy, EPS Workshop | TODO | Start only after golden slice is reviewed |
| 9 Handoff | EXPORT-001 | Versioned portable exports, licenses and integration notes | DONE | No production integration |
| 9 Handoff | SAVE-001 | Verify remote checkpoint and session-end recovery instructions | DONE | bb483f0 public-success reports/screenshots pushed and independently matched remote main; deployed source 8b562d4; NEXT SESSION HANDOFF says STOP for visual feedback |

| 7 Device profiling | QA-004 | Physical desktop/phone GPU FPS and possible geometric LOD | BLOCKED | No target hardware; actual cloud software sample ~3.3 FPS, PERFORMANCE_REPORT.md |

## Requested showcase viewing

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| SHOWCASE-001 | One downloadable index.html containing the actual interactive app and verified assets | DONE | showcase/index.html, build-info.json, README; six offline checks, two served-preview regressions; checkpoint 0f3d648 pushed and independently verified |
| SHOWCASE-002 | Verify direct file:// opening on a personal desktop browser | BLOCKED | Cloud managed Chromium blocks file navigation; offline content rendering passed, direct-file opening is not claimed verified |

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| PREVIEW-ACCESS-001 | Existing v0.2 browser HTTP rendering and clear downloadable viewing package | DONE | downloads/ ZIPs/manifest, build PASS, 9 smoke + 21 rendered HTTP checks; 806f960 pushed/remote verified; STOP for user feedback |
| PREVIEW-DEPLOY-001 | Static site package and manual-only Pages configuration prepared without publication | DONE | showcase-v0.2-static.zip, DEPLOYMENT.md and parsed workflow_dispatch-only workflow |
| PREVIEW-ONLINE-001 | Publish publicly and inspect returned live URL | DONE | Owner enabled Source GitHub Actions; run 38402363567 attempt 2 package/deploy success; https://anapaulagatti.github.io/3D-pharse5-/ 200 text/html, approved SHA and 7 public browser checks PASS |
| VISUAL-REVIEW-001 | User reviews the rendered showcase before new districts | DONE | User supplied v0.3 visual critique: docs/reviews/VISUAL_POLISH_V03_USER_REQUEST.md; this authorizes polishing the existing slice, not new districts |

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| PAGES-PREP-001 | Production artifact/subpath/privacy/provenance audit without model rebuild | DONE | prepare-pages-site.py, artifact-audit.json, seven approved-artifact HTTP render checks including mobile fallback; HTML SHA unchanged |
| PAGES-NET-001 | Allow API/public hostname in cloud network | DONE | Saved api.github.com + anapaulagatti.github.io preserving presets; origins reachable. Direct integration Pages administration is restricted; owner enabled Source and Actions successfully published the site |
| PAGES-LIVE-001 | Public mascot/camera/lighting/animations/mobile-fallback render verification | DONE | quality-reports/pages-live/ deployment.json, public http-verification.json and actual inspected screenshots; zero critical console/resource errors |

## VISUAL-POLISH-003 — Golden Vertical Slice v0.3

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| POLISH-AUDIT-003 | Read review, inspect baseline and preserve originals | DONE | Request archived; b5ed079 remote matched; preserved-v02.json hashes approved files; pinned tools installed |
| POLISH-ASSETS-003 | Additive original handcrafted Hanok detail GLB + editable Blender source | DONE | hanok-polish.blend + GLB/manifest; Validator 0 errors/0 warnings, 13,312 triangles/21 draws/527,852 bytes; 37 original hashes unchanged; visual review in POLISH-QA-003 |
| POLISH-MOTION-003 | Six expressive clips, ambient motion and meaningful interactions | DONE | Final 11 production checks PASS; human-verified chin-hand Thinking/frown Disappointed; actual mascot/lantern/tree mesh clicks, keyboard cheer, all six live clips and native return to idle |
| POLISH-CAMERA-003 | Larger responsive hero, smooth focus and optional cinematic mode | DONE | Actual intermediate focus positions, cinematic movement/yield to orbit, full unclipped portrait and mobile framing verified |
| POLISH-QA-003 | Production build, Validator, desktop/mobile/fallback, video and before/after | DONE | Typecheck/build PASS; 3 GLBs Validator 0/0; 11 production + 11 extracted-repo-prefix browser checks PASS; actual screenshots and decoded video frames inspected; REVIEW.md/VERIFICATION_SUMMARY.json |
| POLISH-REVIEW-003 | Package candidate and checkpoint for user review | DONE | Final standalone HTML, two ZIPs/manifest, audited strict static file allowlist, 42s real video, before/after gallery and session handoff; final Git checkpoint follows |

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| VISUAL-POLISH-003 | Golden Vertical Slice v0.3 — Living Hanok Showcase candidate | DONE | quality-reports/v0.3/REVIEW.md, VERIFICATION_SUMMARY.json, final production/artifact browser evidence and downloadable review ZIP |
| VISUAL-REVIEW-003 | User reviews v0.3 visual results | DONE | User explicitly requested v0.3 Pages publication after candidate handoff; await further visual feedback after release |
| PUBLIC-RELEASE-003 | Publish approved v0.3 and verify actual public render | DONE | Actions 38507114065/deployment 7056177598 success; exact origin HTML SHA; 11 public browser checks PASS and real screenshots inspected; pages-release/deployment.json |

## BIG-UPDATE-004 — Living Hanok Showcase Overhaul

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| OVERHAUL-AUDIT-004 | Archive review, inspect source and preserve v0.3 | DONE | AUDIT.md and preserved-v03.json; remote baseline verified |
| OVERHAUL-MASCOT-004 | Versioned rig, 12 authored clips, expressive face | DONE | Final production 10-stage browser PASS and actual images inspected; exports/build valid |
| OVERHAUL-WORLD-004 | Readable architectural/courtyard/garden/skyline detail | DONE | Final production 10-stage browser PASS and actual images inspected; exports/build valid |
| OVERHAUL-LIFE-004 | Refined ambient life and day/evening/night materials | DONE | Final production 10-stage browser PASS and actual images inspected; exports/build valid |
| OVERHAUL-PRESENT-004 | Hero/portrait camera, clean action UI, reactions | DONE | Final production 10-stage browser PASS and actual images inspected; exports/build valid |
| OVERHAUL-QA-004 | Actual render/12 states/mobile/fallback/Validator/build/video | DONE | 10 production + 10 exact static-subpath checks PASS, five GLBs 0/0, actual images/45s decoded video inspected; VERIFICATION_SUMMARY.json |
| OVERHAUL-REVIEW-004 | Portable review candidate and remote verified checkpoint | DONE | HTML/ZIP/audit/gallery/45s video and persistent handoff saved; checkpoint through 7bd2ada remotely verified, complete-evidence save follows |

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| BIG-UPDATE-004 | Living Hanok Showcase v0.4 review candidate | DONE | quality-reports/v0.4/REVIEW.md + VERIFICATION_SUMMARY.json; source/exports/images/video/ZIP verified |
| VISUAL-REVIEW-004 | User reviews the v0.4 upgrade | DONE | User explicitly requested v0.4 publication after candidate handoff; further visual feedback follows public verification |
| PUBLIC-RELEASE-004 | Publish reviewed v0.4 and verify public scene | DONE | Actions 38530210414/deployment 7059737978 success; exact origin SHA, 10 public browser stages PASS and actual images inspected; pages-release/deployment.json |

## REFORGE-005 — Joseon Fantasy Reforge

| Stable ID | Deliverable | Status | Evidence / next gate |
|---|---|---|---|
| REFORGE-AUDIT-005 | Inspect sources/history/GLBs, verify public and remote baseline, preserve v0.4 | DONE | AUDIT.md;75 protected hashes; read-only Blender inspection of five sources; five directly parsed GLBs; actual saved v0.4 images inspected; origin/main and recovery tag matched |
| REFORGE-CONCEPT-005 | Three original humanoid concepts, comparison and architecture rebuild plan | DONE | concepts/v0.5/character-concepts.png + CONCEPT_REVIEW.md/provenance/prompt; docs/v0.5/ARCHITECTURE_REBUILD_PLAN.md; GATE_A_REVIEW.md and gate-a-verification.json; a6c1959 independently matched origin/main |
| REFORGE-GATE-A-005 | User approves one final character direction | DONE | concepts/v0.5/APPROVAL.json: user explicitly selects recommended A — Nari |
| REFORGE-GATE-B-005 | Complete four-sided Hanok graybox, scale/support checks and actual 360° review | DONE | gate-b/render actual33 views inspected;209 support bounds0gaps; editable source/GLB Validator0/0; production PASS; structure-360.mp4 |
| REFORGE-GATE-C-005 | Skinned humanoid,20 clips,10 expressions, playable collision/controller and touch input | DONE | gate-c/REVIEW.md; final-rig-review actual20clips/10faces/20moving pairs visually inspected; play-pass-4 native9checks PASS; BoneHeat fixes wedges; Validator0/0 |
| REFORGE-GATE-D-005 | Architecture/material/environment/lighting/game-feel polish | DONE | final-layer-review actual13views, updated PBR/source/GLB, native lantern/tree feedback and advancing3windclips |
| REFORGE-GATE-E-005 | GLB/build/browser/gameplay/video/accessibility/mobile/performance proof | DONE | Validator0/0, build PASS, final Nari74actual frames inspected,9native playchecks PASS; remaining final access/video/exact-static proof |
| REFORGE-RELEASE-005 | Publish completed v0.5 and verify public URL | DONE | User explicitly authorizes completion/publication; publish exact297d4e9c after Gate E, preserve v0.4 sources/artifact |


Intermediate Gate D failures and fixes are preserved in Git history and quality-reports/v0.5. Latest authoritative state is STUDIO_PROGRESS.md.

Final capture review found stale gesture replay after play→portrait Canvas change. Clear gesture on mode change; no asset/rig/physics changes. New final HTML 082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f; preserve earlier297d4e9c/126frame113.64s partial attempt. Recapture holds three actual interior compositor frames and waits for portrait Idle. OS reduced preference passes after true OS transition; offscreen test now waits for actual motion=false rather than a fixed400ms during slow render. Exact response hash uses an independent same-URL HTTP GET plus real browser200/render because Chromium evicts the13.5MB document body from inspector cache. Final access/media/artifact verification pending, no deployment yet.

Gate E COMPLETE: final access12checks PASS (realOS/offscreen/WebGL), extracted exactHTTP8checks PASS, final video185realframes/86s with decoded walk/run/jump/greeting/cheer/inside/Idlefaces inspected. Source297→082 change only clears prior gesture on mode switch; final artifact082c661b. All final GLB/build/privacy/rig/nativeplay gates pass; see quality-reports/v0.5/REVIEW.md and VERIFICATION_SUMMARY.json. Authorized PUBLIC-RELEASE-005 next, not deployed yet.

| VISUAL-REVIEW-005 | User reviews the publicly verified v0.5 | DONE | User requested v0.6 chibi art-direction pivot; docs/reviews/ART_PIVOT_V06_USER_REQUEST.md |

PUBLIC-RELEASE-005 COMPLETE: Actions38573493700/deployment7066939380 success; canonical+fresh exact082c661b,8actual public checks and all7public images inspected. Final checkpoint tag checkpoint/v0.5-public-verified is saved after this report. No new work authorized beyond release.

## ART-PIVOT-006 — Playful Hangeul Town v0.6

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| PIVOT-AUDIT-006 | Archive review, preserve v0.5, inspect source and measure baseline | DONE | AUDIT.md, preserved-v05.json; fresh public browser/GLTF Transform/Validator/Blender evidence in baseline/ |
| PIVOT-CONCEPT-006 | Three chibi characters, two town concepts, color/material board | DONE | Two inspected original boards: three characters/two towns/seven material studies, exact prompts/provenance |
| PIVOT-PLAN-006 | Reuse, animation feasibility, complexity and likely render/asset costs | DONE | concepts/v0.6/CONCEPT_REVIEW.md: options, prospective budgets, relative complexity, reuse/retarget/quality plan |
| PIVOT-REVIEW-006 | Visually inspect concepts, verify preservation, save GitHub and STOP for choice | DONE | Four-page PDF and decoded pages inspected, desktop/mobile document PASS, preservation2335files PASS; f6d9732 pushed/independently verified; final handoff tag checkpoint/v0.6-concepts-review |
| PIVOT-APPROVAL-006 | User selects character A/B/C and town T1/T2; recommend B+T1 | TODO | Mandatory STOP; concepts/v0.6/APPROVAL_PENDING.json. Previous v0.5 A/publication approvals do not select/publish v0.6 |
| PIVOT-PROTOTYPE-006 | One approved chibi, house/plaza, move/run/jump, three emotions, interaction/camera/fallback | BLOCKED | Requires new v0.6 concept approval; not authorized to begin yet |
| PUBLIC-RELEASE-006 | Publish redesigned showcase | BLOCKED | Separate updated-publication approval required; existing v0.5 stays live |

- PIVOT-AUDIT-006 DONE: current public exact082c661b HTTP200, fresh Low57/99012 and Medium/High133/195524 measured; both GLBs Transform inspection + Validator0/0; both actual Blender sources read-only. PIVOT-CONCEPT-006 IN_PROGRESS: character sheet delivered/visually inspected; two town/material boards and cost/reuse plan pending.

- PIVOT-CONCEPT-006 DONE: original three-character sheet + T1/T2 town/material sheet generated, saved with exact prompts/provenance/hashes and visually inspected. Seven-color/material samples included. PIVOT-PLAN-006/PIVOT-REVIEW-006 IN_PROGRESS; no production art replaced.


- Final concept delivery COMPLETE; supersedes earlier IN_PROGRESS checkpoint notes above. Actual approval, prototype and publication remain pending, not failed technical tasks. VERIFICATION_SUMMARY.json separates real v0.5 checks from v0.6 illustrations/budgets.

- Remote delivery VERIFIED: f6d9732ba999eacf7159c025df9d2a106a4db632 independently matches origin/main. Final proof/handoff tag checkpoint/v0.6-concepts-review follows; STOP for new user choice.

- PIVOT-APPROVAL-006 DONE: user "B + T1 là phương án hợp lý", concepts/v0.6/APPROVAL.json. PIVOT-PROTOTYPE-006 IN_PROGRESS; PUBLIC-RELEASE-006 remains separately gated. Subtasks: PROTO-ASSETS-006 original chibi/house/plaza sources+GLBs; PROTO-PLAY-006 adapted existing controller/camera/accessibility; PROTO-QA-006 actual render/physics/mobile/quality/Validator/build/media/package.

- PROTO-ASSETS-006 source preparation complete: new nari-v06.py/chibi_motion_v06.py and letter-plaza-v06.py Python syntax PASS. Actual exports/rig/structure/render acceptance pending; source checkpoint before Blender.

- PROTO-ASSETS-006 first actual outputs saved: nari-chibi.blend/GLB8,976tri/1,356,152B/28bones/20clips/10morphs; letter-plaza.blend/GLB1,641,068B/495source modules/27support pairs. Both Validator0/0. Runtime draft typecheck PASS; actual deformation/build/render/gameplay pending.

- First actual art reviewed: world/readable night/rounded head visible; rejected jagged clothing color boundaries and distant hero. Fix per-vertex color + physical collar/hem/cuffs and closer/lower hero. Vite export403 corrected with restricted new config; StrictMode exposed stale AnimationMixer cache, fixed binding/release in same effect. Final re-export/render pending.

- Geometry/controller check detects central porch/door column blocking entry before closed door. New T1 source clears two central entrance posts, retaining spanning crossbeams/outer supports; re-export and actual door/stair checks required.
