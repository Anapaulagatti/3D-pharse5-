# Studio task checklist

Statuses: TODO, IN_PROGRESS, DONE, BLOCKED. DONE requires outputs and verification. Milestones follow the persistent-progress prompt (nine milestones).

Current task: REFORGE-GATE-D-005 IN_PROGRESS; Gates A/B/C DONE. User approved A — Nari; Gate A DONE. Continue v0.5 gates B–E, preserving public v0.4; no new districts or public v0.5 release.

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
| REFORGE-GATE-D-005 | Architecture/material/environment/lighting/game-feel polish | IN_PROGRESS | Preserve graybox/functional rig; separate art exports, textures/life/lighting/face-shadow/camera/effects next |
| REFORGE-GATE-E-005 | GLB/build/browser/gameplay/video/accessibility/mobile/performance proof | TODO | Actual rendered evidence required; no v0.5 completion claim yet |
| REFORGE-RELEASE-005 | User-reviewed candidate and separate publication authorization | BLOCKED | Preserve live v0.4; no approval to publish v0.5 |


Gate D source preparation: separate full-art Hanok and Nari --art outputs prepared; C source/GLBs remain untouched. Original deterministic256px PBR map generator with checksum-verified cache; art roof rolls/endcaps, supported lanterns/banner, low courtyard borders/pavers, wind crowns, planters/bench/basin and separate historic backdrop. Full-art rafters21vsgraybox29 fund detail. Nari ART uses .33decimation, updated warped normals, separate skinned skin surface and original cloth UV/maps. Python syntax passes. Outputs NOT generated/validated/visually accepted yet; checkpoint before Blender.

Gate D first actual art export retained as recovery, NOT final acceptance: Hanok4,726,520B/75,514tri/60primitives/3windclips; Nari2,616,680B/23,794tri/8primitives/20clips. Validator0errors but23/2tangent warnings. Found skin separation selection retains some unwanted faces; correct edit selection and export tangents before acceptance. Runtime PBR/lighting/world interactions and source refinements underway; build/render pending. Low combined geometry target may require selective detail/budget refinement.

User explicitly authorizes completion AND v0.5 public release: "tiếp tục hoàn thành những task còn lại và xuất bản bản v.05". Gates D/E must pass before publication. Source draft e075ef4 remotely verified. Preserve exact v0.4 standalone/sources; deployment configuration may now be versioned to v0.5 only after accepted candidate. Prior no-publication text is superseded by this authorization. Browser approval failed due temporary usage limit, not safety denial; no execution/bypass. Reset time passed and native visual check now running successfully.

Actual Gate D first visual review: four sides/roof/connections/interior and readable night seen. Rejected hero framing (clipped plinth) and double-linearized sRGB map colors (tile pixel5,11,22 instead of target41,60,85). New v2-named maps preserve all first-pass maps, remove double-linearization; widen hero fit16.2. Low/Medium face images identical: remaining chin patch is geometry/specular reflection, not received-shadow. ART-only gentle head smooth and matte skin/specular adjustment pending. Portable tangent pass exposed zero tangent vectors at degenerate UV/caps; mathematically valid orthonormal fallback and lossless weld planned, not a waived validator assertion. No final acceptance/publication yet. User now explicitly authorizes release after completion/verification.
