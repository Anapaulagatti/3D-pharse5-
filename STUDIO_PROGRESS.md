# Studio progress

- Current milestone: public GitHub Pages deployment of completed v0.2, authorized by the user; no world expansion.
- Current task ID: PREVIEW-ONLINE-001 (IN_PROGRESS). PAGES-PREP-001 DONE; network runtime activation/public verification pending.
- Last completed task: PAGES-PREP-001 / exact approved static artifact, public-content/privacy/provenance audit and subpath browser verification.
- Last verified remote checkpoint before this delivery: 644a34e01f90a3350167d965f07b6989d057096a. The following authorized deployment checkpoint will be pushed/compared with origin/main.
- Last checkpoint date/time: 2026-10-13 13:06:25 UTC.
- Latest authorization: user explicitly approved PUBLIC GitHub Pages deployment using this repo and completed showcase. Do not ask that approval again. Preserve source/.blend/GLB/textures/animations/checkpoints; do not regenerate assets or create districts. STOP after verified deployment for visual feedback.
- Deployment artifact: EXACT existing showcase/index.html (7,493,366 bytes; SHA-256 9105a93b022e6751831ba66ae4d353317c43179aa3f045824a329ffdcfc76c17) plus empty .nojekyll. JS/CSS inline, seven approved GLB/PNG assets embedded and addressed through Blob URLs. No app/asset rebuild.
- Base path: the published artifact is the saved standalone build, independent of Vite development root asset paths. Actual /3D-pharse5-/ HTTP rendering passes with only one HTTP document request; no root-relative JS/CSS/GLB/texture fetches or CDN requirement for these models. Original Vite/source configuration preserved.
- Workflow: .github/workflows/showcase-pages.yml now supports workflow_dispatch and push on main ONLY when deployment/HTML files change. This push trigger is authorized; docs-only checkpoints do not redeploy. Official configure-pages v5 reads existing site metadata, upload-pages-artifact v3 and deploy-pages v4 publish the strict site artifact.
- Artifact helper: Studio/scripts/prepare-pages-site.py validates saved v0.2 hash/size, dependency notices and known credential patterns, refuses unexpected/private files in output. An isolated unexpected .env fixture blocked staging and remained intact. Only index.html/.nojekyll enter the site.
- Private-content audit: known credential-pattern matches zero; current runtime GitHub credential values absent (never printed/copied), no external script/CSS or source maps, no .env/.git/.blend/source/progress/cache files copied to published directory. Original seven model/texture/poster assets have project-owned-original provenance; no restricted third-party art. Bundled framework license notices retained.
- Current verification: seven actual rendered artifact HTTP checks passed on repository prefix, including pointer-drag camera, reset/POI, real day/night, six different static poses and advancing animation, reduced-motion freeze, exact approved GLB download hashes, 390x844 layout and desktop/mobile WebGL PNG fallbacks. Zero JS/console errors, failed requests or missing resources. Actual desktop and mobile fallback images inspected.
- Evidence: quality-reports/pages-deployment/artifact-audit.json, http-verification.json, approved-artifact screenshots. Existing nine-test/21-HTTP baseline remains in quality-reports/preview-access/ and was not rerun unnecessarily. Read-only assets:verify passed for seven original exports, both GLBs Validator 0/0; no approved asset/source modifications.
- Corrected blocker diagnosis: active restricted network uses package_managers preset and originally had no custom egress hosts. api.github.com and anapaulagatti.github.io are absent from preset. API GET/POST fail with proxy Forbidden; public-site HTTPS CONNECT fails 403 and reports HTTP status 000. This is not a site HTTP 404 or proof of GitHub account permission denial.
- Network draft: successfully saved exactly api.github.com and anapaulagatti.github.io as custom allowed domains, preserving presets and install/start/secret/repo settings. requires_publish=true; user must Review/Save and Publish environment to apply. Draft save does not change running network or publish the website. No new token requirement or credentials were added.
- Pages enablement: once API host is reachable, reuse existing injected auth and inspect/enable site via supported API. Official configure-pages v5 auto-enable option requires a token other than GITHUB_TOKEN; no unsupported enablement or invented secret was added. If direct API remains unusable, owner sets repo Settings → Pages → Source GitHub Actions and runs Publish approved v0.2 showcase on main.
- Expected default URL: https://anapaulagatti.github.io/3D-pharse5-/ — NOT yet publicly verified; actual configured page_url is authoritative after deployment. The workflow push can attempt deployment without cloud API dispatch; GitHub run status cannot yet be read through the blocked API.
- Limits: public-host access/status/rendering cannot be verified while proxy blocks it. No successful public deployment claim. Physical GPU/phone FPS remains unverified. All local artifacts, sources and model checkpoints preserved.
- Recovery: read AGENTS/four STUDIO files and git status/log, retain installed modules/approved HTML/assets. Live internal test server is temporary, not a user preview link. Do not reinstall/regenerate completed art to recover deployment.

## NEXT SESSION HANDOFF

**Current milestone:** Authorized v0.2 GitHub Pages deployment; network/Pages runtime status verification remains.

**Current task ID:** PREVIEW-ONLINE-001 IN_PROGRESS. PAGES-PREP-001 DONE; PAGES-NET-001 blocked until saved network draft activated. WORLD-001/WORLD-002 remain behind visual-feedback gate.

**Last verified checkpoint:** Prior remote 644a34e; following deployment checkpoint must be independently compared after push and recorded in final handoff.

**Completed work:** Preserved exact approved HTML/models/source/checkpoints; strict two-file site preparation + content/provenance/secret-pattern review; scoped authorized push/manual deployment workflow; seven repository-subpath render checks and mobile fallback; saved required API/site network domains.

**Unfinished work:** Apply saved network allowlist in cloud; inspect workflow/Pages account status, enable Source=GitHub Actions if needed, deploy and verify actual public URL/rendering; then STOP for feedback.

**Files to inspect:** .github/workflows/showcase-pages.yml, Studio/scripts/prepare-pages-site.py, showcase/DEPLOYMENT.md, quality-reports/pages-deployment/artifact-audit.json and http-verification.json, showcase/build-info.json.

**Known blockers:** api.github.com/site host CONNECT denied until environment Review/Save/Publish. Git read/push usable, GH_TOKEN present; no API account-permission diagnosis possible yet. configure-pages auto-enable with default GITHUB_TOKEN unsupported; manual Pages Source UI provided as fallback. No public URL verified yet.

**Exact next command or action:** After network runtime changes, retry gh api repos/Anapaulagatti/3D-pharse5-/pages and inspect deployment runs. If needed, owner sets https://github.com/Anapaulagatti/3D-pharse5-/settings/pages Source=GitHub Actions, then runs https://github.com/Anapaulagatti/3D-pharse5-/actions/workflows/showcase-pages.yml on main. Use actual returned page_url; no renewed public approval needed.

**Verification required:** On reachable public URL, run STUDIO_HTTP_TARGET_SCOPE=public STUDIO_HTTP_REPORT_DIR=quality-reports/pages-live node Studio/scripts/verify-preview-http.mjs public=<actual-url>, inspect screenshots and update status only after success. Current internal prefix checks do not prove public deployment. Do not build a district.

**Remote GitHub save status:** Prior 644a34e independently verified. Authorized deployment changes will be pushed and checked. GitHub source checkpoint, Actions execution, public site verification and environment network publication remain distinct.
