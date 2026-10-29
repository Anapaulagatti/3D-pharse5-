# CODEX MASTER PROMPT — ONE-LINK LIVE REVIEW AFTER EVERY PHASE
# Korean Pixel Town | Tienghansoeasy.io.vn

REPOSITORY: https://github.com/Anapaulagatti/3D-pharse5-
CURRENT FEATURE BRANCH: feature/phase3b-a-daily-life-rights-audit
CURRENT PHASE: Phase 3B-A — completed for human review, NOT yet owner-approved.
REPORTED CHECKPOINT: 47107da9 (verify against Git; don't assume SHA is valid).
ENGINE: Phaser 4.2.1, TypeScript, Vite 8, Node >=24.
CURRENT VITE BASE: /3D-pharse5-/. Do not break default behavior.
CURRENT WORKFLOW: .github/workflows/pixel-ci.yml — verification-only, no deployment.
CURRENT README: existing Github Pages hosts old v0.5; preserve unless specifically approved to replace.

OWNER REQUEST
Stop giving me dozens of separate ZIP / PNG / video / GitHub file URLs to review every phase. I want ONE live link that loads the actual playable game on desktop and mobile, shows what changed, lets me review NPC behavior/characters, and presents a short QA+rights summary. The same URL must work for future phases, with historical snapshots/rollback.

SCOPE AND NON-NEGOTIABLES
- This task ONLY builds a reusable live review platform and optional authorized preview deployment. Do NOT begin Phase 3B-B/C/D, Phase 4, main gameplay merge or commercial release.
- Read AGENTS.md, docs/current/PROJECT_STATE.md, docs/phase3b-a/HUMAN_DIRECTIVE.md, docs/phase3b-a/README.md, docs/phase3b-a/RELEASE_GATE.md and rights audit first. Verify actual branches/commits and environment.
- Preserve approved map, Jeju, palace, station, textures/frames, all 26 NPC stable IDs, 12 playable characters, 28 cosmetics, animation, dialogue, collision, camera, Character Studio, save keys and existing game rules. No artwork regeneration or broad refactor.
- Existing actor caps remain 4 active, 4 textures, 2 pending. The six fictional archive NPCs are NOT simply simultaneous residents of the modern town; preserve replacement/host-slot logic.
- No unstated production, login, ads, economy, shops, farming, quizzes or Korean-learning backend feature.

WARNING: PUBLIC DISPLAY AND COPYRIGHT
GitHub Pages on standard plans is accessible publicly. 'Development preview', a noindex tag, unlisted URL or a private source repo DOES NOT create password protection or grant image/likeness rights. Commercial clearance remains BLOCKED_PENDING_REVIEW for Phase 3B-A. Do not publicly publish uncleared or specifically disputed depictions without a separate explicit human exposure decision and documented asset-specific review. If a safe public preview is not available, offer a truly access-controlled staging alternative or a sanitized demonstrator using only safe-to-publish assets; STOP before publishing questionable content. Never claim to have obtained legal clearance. Keep PREVIEW_PUBLIC_EXPOSURE approval distinct from COMMERCIAL_RELEASE approval.

PART A — INVESTIGATE CURRENT PAGES SETUP
1. Inspect existing Pages source, currently published old v0.5 artifact, workflows and permissions. Inspect the actual current 3B-A review branch and available build artifacts.
2. Prefer a dedicated GitHub Pages review destination such as a separate repo '3D-pharse5-review' to avoid overwriting the existing Pages and main game. The repo name is a proposal, NOT a verified or live address. If repo creation/settings or deployment authorization require owner action, provide the exact one-time steps and STOP at the relevant gate. Do not create a fake live URL.
3. If the owner explicitly chooses the EXISTING Pages site instead, document its baseline and rollback and obtain an explicit decision to replace old v0.5 before touching it.
4. Do not force-push, rewrite history or change main gameplay. If adding a workflow_dispatch workflow, remember that GitHub Actions manual dispatch requires the workflow file to be in that repository's DEFAULT branch. A feature-branch-only workflow is not sufficient. Do not quietly merge feature code into main just to enable Actions.
5. Prefer an explicit human-promoted GitHub Pages build based on a checked commit SHA, rather than auto-publish on every work-in-progress push. Use least-privilege GitHub permissions and avoid unnecessary PAT tokens. Pages Actions may use configure-pages@v5, upload-pages-artifact@v4, deploy-pages@v4 with required permissions/environment when supported. If using a deployment branch, publish only generated, reviewed static files.

PART B — THE SINGLE REVIEW PORTAL
Build a lightweight responsive, accessible portal without inventing a second game engine.
Homepage: 'Korean Pixel Town — Development Review'. Show current phase, verified short SHA, real build date and statuses:
  ARTISTIC REVIEW: PENDING / APPROVED (grounded)
  TECHNICAL QA: PASS / FAIL with numbers from current run
  COMMERCIAL RELEASE: BLOCKED_PENDING_REVIEW
  PHYSICAL ANDROID/iPHONE/GPU: NOT TESTED until physically tested
Large mobile-friendly sections:
  [CHƠI THỬ] — real compiled Phaser game (not a video)
  [26 NPC] — roster and details, native sprites and schedules
  [LỊCH SINH HOẠT] — Phase 3B-A deterministic clock, individual intents and allowed QA time controls
  [THAY ĐỔI PHASE] — concise change log with 3-5 relevant before/after visuals
  [QA & QUYỀN HÌNH ẢNH] — status for each NPC/assets, evidence and blockers
  [GÓP Ý] — copyable bug report containing phase/SHA/browser/steps (Pages has no backend).
On mobile: easy controls, landscape/portrait support, readable text, responsive safe-area, no dozens of huge media loads. Lazy-load videos/gallery assets; keep a clean portal. Include a button to return from gameplay to review without wiping saves.

PART C — DEPLOY THE REAL GAME CORRECTLY
Use actual Vite production build, not a hand-made mock. Keep Vite's current base '/3D-pharse5-/' for canonical build; make review deployment base configurable via a reviewed environment variable if the chosen review repo has a different path. Check every JS/CSS/image/texture/audio/atlas path and dynamically loaded asset. No 404, broken sprite, blank canvas, stale cached assets, mixed-content errors or runtime console exceptions. Use content-hash caching and version manifest.
Make QA-only scenario links that place the reviewer at validated NPC areas and demonstrate the scheduler, without granting rewards, changing real player progress, or enabling cheats for production. Respect active NPC limits and prevent archive NPC and their displaced host from appearing together. Show real NPC intent, clock, zone, animation state and pause/speed controls labeled 'REVIEW ONLY'. Do not change existing normal game logic to force a demonstration.

PART D — REVIEW-ASSET AND PRIVACY GATE
Read docs/phase3b-a/COMMERCIAL_RIGHTS_AUDIT.md, docs/phase3b-a/RIGHTS_REVIEW_QUEUE.md, docs/phase3b-a/RELEASE_GATE.md, docs/phase3a-identity-safeguard/DEPICTION_REVIEW.md and original art source/provenance.
Produce an export manifest for the exact review dist: filename/hash, origin and known license/generation terms, public-preview decision, likeness/brand/third-party risks, missing evidence and status. Don't equate renamed historical identities with commercial permission. Do not auto-replace their approved artwork. Exclude secrets, login tokens, private account information, actual learner records and internal sensitive audit records from static Pages files. Public display decisions must be explicitly justified; noindex is NOT access control.

PART E — ONE LINK, MANY PHASES
Create stable routes/paths supported by actual static hosting, e.g.:
  /                current review homepage
  /play/           current playable build
  /phases/3b-a/    immutable Phase 3B-A review snapshot and evidence
  /history/        previous phase/commit selection and rollback
Use static directories or hash routing if needed, not an unsupported SPA fallback. On new Phase completion:
  1) finish feature and tests; 2) prepare a review-only candidate tied to an actual SHA;
  3) perform asset rights/public-exposure gate; 4) obtain human publication approval;
  5) deploy one stable URL; 6) preserve earlier snapshot; 7) report one short note.
Do not auto-deploy incomplete feature branches or block the owner with dozens of individual files. Site should clearly show current vs archived versions.

PART F — ACCEPTANCE & DELIVERABLES
Run npm ci, npm run assets:check, npm run typecheck, npm run lint, npm run format:check, npm test, npm run build, npm run test:e2e, then real preview-base route and asset smoke tests. Use Node 24 and required Python/Pillow versions as in existing CI. Don't suppress checks to make PASS. Test desktop + emulated mobile; explicitly label physical device tests NOT TESTED.
Deliver:
- docs/review-portal/README.md and reproducible build + setup + rollback instructions.
- Portal source and reviewed deployment workflow/staging method; minimal permission requirements.
- A concise actual QA report and manifest for review artifacts and rights/exposure.
- One verified final URL ONLY after site is truly deployed and checked; otherwise mark NOT DEPLOYED and give the exact remaining manual step, not an invented Pages link.
- An easy copy/paste message template for the owner to request an update after each next Phase.

STOP CONDITION
Stop when portal candidate is ready and, if explicitly authorized and rights-gated, the preview has been actually deployed and tested. Do not merge main gameplay, overwrite the old Pages site, declare Phase 3B-A approved, authorize commercial release, or begin next development phases.