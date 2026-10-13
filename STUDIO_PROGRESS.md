# Studio progress

- Current milestone: existing v0.2 preview accessibility task completed; STOP for the user's visual review. No district expansion.
- Current task ID: PREVIEW-ACCESS-001 (DONE). WORLD-001/WORLD-002 remain TODO behind the explicit visual-feedback gate.
- Last completed task: PREVIEW-ACCESS-001 / real browser HTTP rendering, portable viewing package, static deployment preparation.
- Last verified remote artifact checkpoint: 806f9607597aa650730c0afa0ede10da0f74209e; local HEAD independently matched origin/main after push. Final handoff documentation follows in git log.
- Last checkpoint date/time: 2026-10-13 12:36:14 UTC.
- Latest request: make existing v0.2 viewable, visually inspect it, run production build and save a checkpoint; stop afterward. Do not build Hangul Garden, regenerate models, change art direction, install unrelated dependencies or publish publicly without approval.
- Diagnosis: ChatGPT/Codex file viewer displays source rather than hosting HTML. The actual Vite endpoint returns 200 text/html and renders correctly. This onboarding UI exposes no user-facing browser preview/port-forwarding capability. GitHub API Pages read returns Forbidden; native Git works. Raw GitHub fetch returned 404, not a working website.
- Implementation: added Python standard-library HTTP launcher and Windows command launcher, ZIP packaging script, static ZIP, deployment guide and manual-only Pages workflow. Added inline empty favicon to both HTML entries to eliminate a confirmed favicon.ico 404. No changes to preview/src, modeling, approved assets, exports or lockfiles.
- Current HTML: showcase/index.html, 7,493,366 bytes, SHA-256 9105a93b022e6751831ba66ae4d353317c43179aa3f045824a329ffdcfc76c17. Its compiled app/styles and seven embedded assets are unchanged; HTML only gained the favicon declaration.
- Download packages: downloads/showcase-v0.2-http.zip (2,916,077 bytes), showcase-v0.2-static.zip (2,910,445 bytes), package-manifest.json. Archive integrity/entries/checksums verified; actual extracted HTTP launcher tested. The local archive also includes its linked deployment guide.
- Production build: npm --prefix preview run build PASS (typecheck + Vite). Standalone rebuilt only for the favicon header; no modeling/Blender/image generation. Existing ~1 MB lazy 3D chunk warning remains.
- Browser tests: fresh full suite 9 passed, 0 failed, 0 skipped, 0 flaky; JSON in quality-reports/preview-access/dev-tests.json. Initial five-second cloud readiness timeout is documented in INITIAL_DIAGNOSIS.md; allow 15 seconds for software shader startup, retaining the same rendering assertions.
- Rendered HTTP checks: 21 passed across Vite production, extracted ZIP served by its launcher and /3D-pharse5-/ nested path. Camera pointer drag changes the image; reset/POI, day/night, six distinct poses, live animation, reduced-motion freeze, 390x844 layout, two checksum-matching GLB downloads and PNG WebGL fallback work. All three actual 3D runs: 0 page/console errors, failed requests or missing resources. Root/nested standalone requires only the HTML HTTP response.
- Visual inspection: viewed actual package/production day, night, mascot, camera and fallback screenshots. Curved roofs/timber/plum garden and jade mascot render; materials and warm night lighting are visible. Screenshots and report are in quality-reports/preview-access/, including VISUAL_REVIEW.md and http-verification.json.
- Model preservation: assets:verify passed for all seven approved exports; both GLBs Validator 0 errors/0 warnings. No asset/source regeneration or topology/animation changes.
- Preview method for the user: download HTTP ZIP, extract fully; Windows run START_WINDOWS.cmd, macOS/Linux run python3 start.py in the extracted folder. Python 3 is required; launcher opens a browser on that same computer. No Node/Blender/npm/internet needed afterward.
- Online method: static ZIP and .github/workflows/showcase-pages.yml prepared. Pages workflow has workflow_dispatch ONLY. Nothing deployed or enabled publicly; optional online publishing awaits explicit user approval and account UI access.
- Limits: no shareable cloud preview URL; file:// blocked by managed Chromium. Actual Linux/Python HTTP serving and Chromium rendering verified, native Windows .cmd/GUI auto-open not executed here. Cloud uses SwiftShader; physical GPU/phone FPS remains unverified (QA-004).
- Recovery: reuse node_modules, HTML, ZIPs and saved models. Read AGENTS/four STUDIO files and inspect Git/outputs. Do not run model/art generation or reinstall working packages to view. Live processes do not survive environment restoration.

## NEXT SESSION HANDOFF

**Current milestone:** v0.2 preview access complete; waiting for user visual feedback.

**Current task ID:** PREVIEW-ACCESS-001 DONE. Optional public deployment PREVIEW-ONLINE-001 awaiting explicit approval; no automatic deployment.

**Last verified checkpoint:** 806f9607597aa650730c0afa0ede10da0f74209e, full HTTP package/code/QA checkpoint independently matched origin/main. Final handoff documentation follows.

**Completed work:** Valid served production and self-contained HTML; metadata/favicon fix; local HTTP launchers; two downloadable ZIPs; manual-only Pages config and Cloudflare upload guide; production build, 9 smoke tests, 21 rendered HTTP checks, real screenshot inspection; approved assets unchanged.

**Unfinished work:** User visual feedback; optional approved public deployment and verification of the real URL; physical-device FPS. Further districts must wait.

**Files to inspect:** downloads/showcase-v0.2-http.zip, showcase/README.md, showcase/DEPLOYMENT.md, .github/workflows/showcase-pages.yml, quality-reports/preview-access/http-verification.json, VISUAL_REVIEW.md and dev-tests.json.

**Known blockers:** No cloud preview exposure. GitHub Pages API Forbidden while Git authentication works; enabling/running deployment currently needs GitHub account UI. Public approval not supplied. Physical target hardware unavailable. No secret missing for local HTTP viewing.

**Exact next command or action:** Give the user HTTP ZIP and opening instructions, then STOP for feedback. To view locally on the user's computer, extract and run python3 start.py (Windows launcher invokes py -3/python). Do not hand them a loopback link from the cloud. If publication is approved, follow DEPLOYMENT.md, then inspect the actual returned public URL.

**Verification required:** Already passed local HTTP rendering/controls/resources/fallback. A public site must be verified only after it is really deployed; native Windows/macOS launching and physical-device performance are not claimed tested.

**Remote GitHub save status:** 806f960 full HTTP package/code/QA checkpoint was pushed and independently verified against origin/main. Final handoff documentation follows; compare newest local/remote on recovery. Manual workflow has no push trigger and no public deployment was executed. No environment/network/dependency configuration changes were needed.
