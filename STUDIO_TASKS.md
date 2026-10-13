# Studio task checklist

Statuses: TODO, IN_PROGRESS, DONE, BLOCKED. DONE requires outputs and verification. Milestones follow the persistent-progress prompt (nine milestones).

Current user gate: public GitHub Pages deployment of existing v0.2 is COMPLETE and verified. STOP for the user's visual feedback. Do not continue WORLD-001/WORLD-002.

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
| 9 Handoff | SAVE-001 | Verify remote checkpoint and session-end recovery instructions | DONE | 80bfc2a matched remote main; install/start draft confirmed saved; final handoff commit follows |

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
| VISUAL-REVIEW-001 | User reviews the rendered showcase before new districts | BLOCKED | Waiting for user's visual feedback; verified public site https://anapaulagatti.github.io/3D-pharse5-/ and local HTTP package available |

| Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|
| PAGES-PREP-001 | Production artifact/subpath/privacy/provenance audit without model rebuild | DONE | prepare-pages-site.py, artifact-audit.json, seven approved-artifact HTTP render checks including mobile fallback; HTML SHA unchanged |
| PAGES-NET-001 | Allow API/public hostname in cloud network | DONE | Saved api.github.com + anapaulagatti.github.io preserving presets; origins reachable. Direct integration Pages administration is restricted; owner enabled Source and Actions successfully published the site |
| PAGES-LIVE-001 | Public mascot/camera/lighting/animations/mobile-fallback render verification | DONE | quality-reports/pages-live/ deployment.json, public http-verification.json and actual inspected screenshots; zero critical console/resource errors |
