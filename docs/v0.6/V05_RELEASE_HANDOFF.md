# Studio progress

REFORGE-005 — Joseon Fantasy Reforge and PUBLIC-RELEASE-005 are COMPLETE. Gates A/B/C/D/E DONE. STOP for VISUAL-REVIEW-005; do not start Hangul Garden, another district, further art or a new deployment without the user's next task.

Public showcase: https://anapaulagatti.github.io/3D-pharse5-/?release=082c661b (canonical root also serves exactv0.5). HTML13,543,219B, SHA082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f. Actions38573493700/deployment7066939380 succeeded from source4a29565fcbe59773597feb5e0ab81d9689845c93. Actual public8HTTP/WebGL/face/Greeting/keyboard/mobile/context-loss checks passed; all7public PNGs opened,0critical console errors/0missing resources. See quality-reports/v0.5/pages-release/deployment.json and VISUAL_REVIEW.md.

Authorization: user approved recommended A — Nari (“nếu bạn đề xuất là A thì hãy chọn A”), then explicitly authorized completion AND publication (“tiếp tục hoàn thành những task còn lại và xuất bản bản v.05”). No duplicate approval needed. Current stop follows successful release.

Preservation: v0.4 recovery tag checkpoint/v0.4-pre-reforge-005→9cc1381. Original public v0.4 standalone cd238a4c, Blender/model/map/ZIP assets and old staging script remain unchanged.74protected baseline files unchanged; only explicitly authorized Pages workflow updated. Gate B graybox and Gate C functional Nari source/GLBs remain preserved. Intermediate rejected art/test/media passes are retained in versioned reports and Git.

Delivered: complete solid supported four-sided Hanok, genuine skinned Nari28joints/20skeletal clips/10facial morphs, responsive keyboard/touch physics controller and stairs/doors/interior, original packed256px PBR maps, roof/joinery/lattice/courtyard/plum/lantern/banner/basin/details, three readable lighting modes, three environmental wind clips/flicker/ripples/particles, meaningful character/lantern/tree reactions, effect controls/OS reduced motion/pause/offscreen/WebGL fallback, five view modes and smooth focus/orbit/follow. No new learning district/backend/audio service. Original legacy Ceramic Seed Spirit is an optional unchanged embedded GLB download.

Final data: world5,714,488B/75,514tri/60primitives/3windclips; Nari2,923,840B/23,794tri/6primitives/1skin28joints/20clips/10morphs. Validator0errors/0warnings, normalized≤4skin weights, embedded PBR images. Exact source/asset hashes and provenance in exports/v0.5/asset-manifest.json. All final Blender sources remain editable. Actual final source images in gate-d/final-layer-review; rig74PNG and human-reviewed10faces/20poses/4views/live galleries in gate-e/final-static-character and gallery.

Verification: production/typecheck PASS; GLB/texture/skin/provenance/privacy/public two-file allowlist PASS; native9Lowplay checks and6full-world physics checks PASS;12access/world/quality/OS/offscreen/real context-loss/WebGL-unavailable checks PASS;8exact extractedHTTP checks PASS; final public8checks PASS. Real video185native compositor frames/86s with ≥5swalk/≥5srun/jump/land/greet/cheer/entered threshold and Idle facial changes, decoded frames actually opened. Original timestamps/VFR preserved, no speedup/interpolation. Video and source frames in quality-reports/v0.5/capture and joseon-reforge-v05-gameplay.mp4. Before/after gallery and VERIFICATION_SUMMARY.json record practical limits.

Measured cloud counts: Low57draws/99,012tri; Medium/High133draws/195,524tri including shadows. Low removes normal-map/environment/point-light/shadow features and reduces foliage; higher profiles preserve source presentation. Cloud SwiftShader is visibly slow; physical desktop/phone GPU FPS remains unmeasured (QA-004). No30/60FPS claim or commercial-finished-game claim.

Static delivery: showcase-v0.5/index.html directly imports Reforge, four verified embedded original assets, inline JS/CSS/licenses, no external assets/APIs/source maps. Public allowlist index.html/.nojekyll. downloads/v0.5 contains static and HTTP-launcher ZIPs, safely extracted/exact-byte checked and actually rendered via included launcher. Source preview remains existing Vite app with ?candidate=v05; default legacy source viewer preserved. No dependencies/locks changed. For any later session use current sources/exports, do not regenerate approved outputs or reinstall working packages.

Release method: .github/workflows/showcase-pages.yml stages only pinned082c661b via Studio/scripts/prepare-reforge-pages.py. It uses existing configured GitHub Actions Pages source. Documentation/report/test-harness changes do not redeploy. Current runtime HTTPS proxy is required for Playwright public requests; automatic QA now reuses it without exposing credentials. Direct-socket failure retained separately; TLS verification was never disabled.

## NEXT SESSION HANDOFF

**Current milestone:** REFORGE-005 + PUBLIC-RELEASE-005 COMPLETE; VISUAL-REVIEW-005 awaiting user feedback. STOP.

**Current task ID:** VISUAL-REVIEW-005; no implementation authorized until user feedback/new task.

**Last verified checkpoint:** Published source4a29565fcbe59773597feb5e0ab81d9689845c93 independently origin matched; Gate E59b377ba8a4dff4d9dd5fc7de939ecf580867ea9. Final evidence checkpoint is tagged checkpoint/v0.5-public-verified after this documentation commit; read git log/remote tag for its exact SHA.

**Completed work:** All approved concepts/gates/source/GLBs/PBR/controllers/lights/life/render/media/packages/public release and actual public visual verification as above.

**Unfinished work:** Only user's visual feedback. QA-004 physical hardware profiling remains outside available cloud hardware; no FPS claim. No pending v0.5 release fix or permission blocker.

**Files to inspect:** quality-reports/v0.5/REVIEW.md, VERIFICATION_SUMMARY.json, pages-release/deployment.json/VISUAL_REVIEW.md/render, capture/media-report.json, final source manifest, STUDIO_TASKS/ASSETS/DECISIONS, exact showcase-v0.5/build-info. Prior failures remain truthful historical records.

**Known blockers:** None for delivered publication. No new district or artwork should begin autonomously.

**Exact next action:** Give the verified public link and wait for user's visual review. Do not rerun already-passed expensive checks, change deployment inputs or regenerate approved assets without a concrete new task.

**Verification required:** None remaining for this release; future changes require relevant checks and their own checkpoint.

**Remote save status:** Source4a29565 and Gate E59b377b were pushed and independently matched. Final report/tag save follows, with branch/tag exact SHA verified before final handoff. Site artifact remains082c661b and docs-only save must not redeploy.
