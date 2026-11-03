# CODEX MASTER TASK — PHASE 3B-D + REJECTED-MAP REPOSITORY CLEANUP
# Project: Korean Pixel Town (3D-pharse5-)
# Owner decision: Continue to next gameplay phase AND remove rejected map artifacts from active repository trees.

READ FIRST
- Working source: https://github.com/Anapaulagatti/3D-pharse5-
- Public review: https://github.com/Anapaulagatti/3D-pharse5-review
- Current playable review: https://anapaulagatti.github.io/3D-pharse5-review/play/
- Derive the *actual* current HEAD, branch and latest Phase 3B-C candidate/checkpoint from Git, not an old screenshot SHA.
- Read AGENTS.md, docs/current/PROJECT_STATE.md, the current approved world/phase handoff, the latest Phase 3B-C manifest, navigation tests and the roadmap relevant to the working branch. Follow the latest owner decisions over superseded phase STOP instructions, but retain explicit safety and release gates.
- Treat 'Phase 3B-D' here as the owner's next scoped gameplay increment, NOT as proof that some older roadmap defines the same name. If the repository roadmap uses another label, map this work to its authoritative milestone in the handoff without rewriting existing phase history.

OWNER ACCEPTANCE / BASELINE
- Phase 3B-C candidate is considered visually/gameplay acceptable to continue development, NOT automatically released.
- Reported candidate: 26 NPC, 12 playable characters, 24 remaining cosmetics (4 broken hair accessories removed), 3 actual quests and tested walkable routes.
- Latest screenshot reports 181 unit tests PASS, 17/17 targeted E2E PASS, full E2E 71/72 with 3 review markers and physical devices NOT TESTED. Do not change these statuses to PASS until truly resolved.
- Preserve the approved Gate 1/Gate 3 artwork, world coordinates, new Hanbit station, both Jeju bridges, west hanok, palace, farm, camera, collision corrections, avatar/NPC atlases, 26 NPC IDs and save compatibility. Never regenerate or substitute old maps.
- Create a new recoverable source checkpoint from the actual Phase 3B-C candidate and store immutable asset hashes and a rollback reference before touching any file.
- Work on a fresh feature branch; do not force-push/rebase public history, merge main, overwrite the 26-NPC Pages build, touch the Korean-learning website production backend, or provision paid services.

============================================================
TASK 0 — CLEAN OUT REJECTED MAPS FROM ACTIVE REPOSITORY (MUST DO)
============================================================
The owner has repeatedly rejected earlier V6–V10 / experimental maps, but still finds map screenshots and source folders in GitHub. An example screenshot is a HISTORICAL commit (458134c...) under docs/v9-world; DO NOT mistake a historical Git tree for the current game HEAD. Ordinary deletion on the current branch will not erase snapshots in Git history. Git history rewrite is NOT authorized.

A. IDENTIFY the true canonical world.
- Find the production/review Phaser scene entrypoint and authoritative art/ground/collision/tileset manifests used by the latest APPROVED world.
- Record canonical file paths, content hashes, loading order, and runtime imports. Create an allowlist for the approved world and its necessary source assets.
- Confirm that nothing in runtime is accidentally falling back to old V9/V10 scenes, maps, atlases, thumbnails, JSON or legacy start pages.

B. INVENTORY obsolete content by evidence, not file name alone.
- Inspect docs/v9-world/, docs/v10-city/, assets-src/v10-city/, earlier southern-world prototypes, rejected screenshots/packages, legacy preview entrypoints and references on active development branches.
- Also inspect older world-related directories, scripts, CI workflows, docs navigation, preview gallery links, asset loaders and Pages build inputs.
- Classify each candidate as APPROVED_ACTIVE / REQUIRED_SOURCE_OR_ROLLBACK / CONFIRMED_REJECTED_UNUSED / UNCERTAIN.
- A candidate is CONFIRMED_REJECTED_UNUSED only with documented owner rejection, no active runtime/build/CI import, and no required rollback/source dependency. Do not delete an entire directory merely because its name contains v9/v10 or archive.

C. PERFORM REAL DELETION of CONFIRMED_REJECTED_UNUSED files from the ACTIVE WORKING BRANCH.
- Use git rm for those confirmed files (not merely hiding them in an HTML menu or moving another duplicate into a new active folder).
- Remove obsolete imports, index references, auto-discovery patterns, package/preview entries and obsolete build copies that point to them.
- If an old file is a recovery/source dependency, keep it in clearly marked non-runtime archival material and explicitly exclude it from current world imports, review navigation, game bundles and public release manifests; list the reason why it was not deleted.
- Never remove approved world tiles, station/bridge/palace assets, collision masks, currently used atlases, approved captures needed for verification, legally required notices, recovery checkpoints, or required project history.
- Do NOT delete repository branches/tags, rewrite Git history, use filter-repo/BFG, purge Git LFS globally, or erase remote backups as part of this task. If owner later requests removal from the HISTORICAL Git web UI, explain that it is a separate high-risk history rewrite decision.

D. PREVENT REINTRODUCTION.
- Make approved map loading explicit; never auto-select maps merely because they are found in a directory.
- Add a CI regression check detecting references to known rejected runtime map IDs/entrypoints and unexpected old map content entering the built artifact.
- Check source AND the playable ZIP AND the published-review package, not only unit test fixtures.
- Generate docs/cleanup/REJECTED_WORLD_CLEANUP_<date>.md and a machine-readable manifest listing exact removed paths, bytes, prior SHA256, rejection evidence, retained exceptions, all reference changes, and the after-build verification.

TASK 0 ACCEPTANCE:
- No confirmed rejected old map is still tracked in the current active candidate branch or included in runtime/Pages builds.
- Exactly the approved canonical map is loaded during gameplay and at startup, including restart/reload.
- No regression in camera, collision, station, bridges, NPC schedules, pathing or current 3 quests.
- Historical commits may still show old files: document this accurately, do not claim historical Git removal.
- If unknown dependencies prevent deletion, stop deletion of ONLY those ambiguous files, provide the blocking path/dependency, and continue safe work; never delete indiscriminately.

============================================================
TASK 1 — COMPLETE PHASE 3B-C TECHNICAL CARRYOVER
============================================================
- Review the 3 outstanding Phase 3B-C markers and the 1 initially failed full E2E. Fix only reproducible defects in the current candidate, rerun relevant scenarios, and report PASS/FAIL/NOT TESTED truthfully.
- Keep the removed hair accessories removed. No replacement hair overlays.
- Verify that players and NPCs can enter the intended locations with adequate real player-body clearance, that camera start/stop/directional combinations do not jerk, and that the 3 existing quests still complete with Korean question gating and idempotent rewards.
- Preserve local save migration and prevent reward duplication on refresh/retry.

============================================================
TASK 2 — PHASE 3B-D: FARMING, SHOPS AND A REAL ECONOMY LOOP
============================================================
Implement a coherent small vertical slice, not a huge unfinished catalog. Build on the existing Phase 3B-C quest manager, Daily Life NPCs, 26-NPC roster and actual farm/store placements. Do not invent existing integrations or alter the approved world geometry.

A. FARMING CORE (in the already approved farm area)
- Derive the available plots from the CURRENT farm layout, not from an obsolete screenshot or other unrelated farming games.
- Provide selectable plots, till/plant/water/growth/harvest interactions, and at least TWO original crops with distinct growth periods and outputs.
- Show visible states with existing lawful assets or limited newly created art consistent with Gate 1. Do not repaint terrain/world.
- Persist timestamps/state; account for resume/reload/offline elapsed time with deterministic caps, no real-money mechanics and no unfair mandatory waiting in the introductory quest.
- Prevent duplicate harvesting, lost items, negative stock and invalid plot interactions.

B. SHOPS AND INVENTORY
- Integrate at least ONE existing shopkeeper as a real buy/sell NPC with contextual dialogue and a simple mobile-friendly store UI.
- Support buying seeds, selling produce and purchasing a limited list of non-competitive cosmetic/decorative goods if matching approved art exists.
- Reuse/extend inventory architecture; item IDs, stack limits, display names, prices, transaction ledger, replay-safe/idempotent transaction IDs and rollback on failed purchases.
- Make shop prices/rewards explicit configurable constants, not hard-coded all over the UI.
- Do not generate an entire new town, market or player-gated premium store.

C. ECONOMY BOUNDARIES
- Keep Town Coins and cosmetic/game XP separate from Korean mastery, SRS, formal tests and the website's real learning scores.
- Earn coins from legitimate mission/farm transactions; spend only if balance and inventory allow; zero/negative quantity, duplicate claim and multi-click races must be rejected.
- Document a small balancing table (seed cost, yields, harvest time, sell value, mission base reward) with rationale and simulations to detect infinite-profit exploits.
- Local review only: do not connect live Supabase learner records or enable real-money purchases.

D. NPC QUEST EXTENSION
- Integrate farming and shopping into at least TWO new multi-step quests that use the approved NPCs and existing map locations.
- Preserve the established loop: talk -> accept -> perform actual activity -> return -> answer an appropriate Korean question correctly -> claim base reward.
- Wrong answer -> helpful feedback + DIFFERENT question at equivalent level, not instant success, and never punish with purchased retry.
- Prefer actual website learning history only when an authorized LearningProgressAdapter exists. Otherwise use a clearly identified original/local beginner curriculum demo; do not falsely claim learner-account synchronization.
- Korean educational content must retain PENDING_HUMAN_REVIEW until a qualified human validates it; demo mechanics may still be reviewed without calling curriculum quality PASS.
- Preserve player freedom: exploration, beginner learning materials and other education content must not be locked behind farming/economy grind.

E. OPTIONAL ADS = DISABLED
- Retain only an optional RewardedAdAdapter interface behind a DISABLED default. Do not load any ad SDK, charge money or double Korean mastery/exam progress. Base rewards remain attainable without ads.

============================================================
TASK 3 — QA + REVIEW RELEASE
============================================================
Before packaging, validate:
1. Approved map/asset hashes stable outside explicitly scoped new art.
2. All 26 NPCs, 12 player characters, current 24 cosmetics, three previous quests and collision hotfix remain operational.
3. Rejected map references gone from active runtime and builds; no legacy world loaded after reload or direct URL navigation.
4. Farm: plant/water/harvest, reload/offline resume, full inventory, limited plots, repeated clicks and invalid item cases.
5. Shop: buy/sell, insufficient coins, full inventory, bad quantities, concurrent clicks, persistence and idempotency.
6. At least two new quests fully playable with correct/incorrect Korean answers, reward accounting, no duplicate rewards.
7. Desktop keyboard and mobile emulation navigation/interactions; no camera jerk or blocked entrances.
8. Typecheck, lint, unit, E2E, production build, local packaged ZIP smoke, game screenshot and playback/video evidence.
9. Real Android/iPhone and GPU hardware marked NOT TESTED if unavailable; never fabricate 60Hz or physical-device PASS.
10. Security: no production data writes, no secrets in public build, no paid external APIs, no ads, no live auth/multiplayer.

Create ONE consolidated owner review page, with direct Play links and a concise PASS/FAIL/NOT TESTED table, plus:
- Current source SHA/branch, exact new artifact manifest SHA256 and file count.
- Old-map cleanup manifest and removed-path count, with retained-path explanations.
- Farm/shops/economy quick-play guide and the two new quests.
- Screenshots/video of ACTUAL Phaser runtime and collision visualization.
- Explicit carried-over Phase 3B-C issues and what is resolved/unresolved.
- Reproducible local runnable review ZIP, exact GitHub Pages candidate and rollback snapshot.

DEPLOYMENT RULE:
- Implement all achievable changes in one controlled continuation on a branch.
- Keep existing live 26-NPC GitHub Pages build untouched until the owner reviews/approves the NEW exact manifest. Do not use the previous approval for a changed payload.
- After approval, use the existing GitHub Actions environment-review protection and verify actual playable HTTPS, including content/version/asset checksum; do not claim DEPLOYED before confirmation.
- Do not begin Phase 3B-E, unrelated website phases, multiplayer, production integration or the full ads system.

FINAL HANDOFF FORMAT:
1) Phase 3B-D: READY_FOR_OWNER_REVIEW / BLOCKED (not automatically RELEASED)
2) Exactly what changed in gameplay
3) Exact deleted rejected-map paths; exceptions and why
4) Canonical approved-world paths and proof no old asset is loaded
5) Tests with actual pass/fail counts
6) Artifact SHA, branch, commit, playable ZIP, rollback checkpoint
7) Public review URL ONLY if actually deployed/verified, else PENDING_OWNER_APPROVAL
8) Remaining blockers and next actions

Important: Do the requested cleanup rather than producing only another diagnosis. But never sacrifice the approved map, source recovery, Git history, or genuine required dependencies to achieve an artificial deletion count.
