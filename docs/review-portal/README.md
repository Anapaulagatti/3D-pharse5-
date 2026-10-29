# Korean Pixel Town — One-link Development Review

**NOT DEPLOYED.** This is a tested private portal candidate, not a live URL or owner acceptance of Phase3B-A. The current game snapshot is verified commit `47107da9a859ffcc6670f99705cee7dc44d6b34a`; original branch HEAD before this task was `bc7c5916bd53fe023245da15c882c05465686796`. Work branch: `feature/one-link-review-portal`. See QA.md for this task's fresh results; never substitute the earlier171/72 counts for a new run.

## What the single entry provides

Actual compiled Phaser game at `play/`; original Character Studio and normal saves; 26 public fictional identities/native96×112 thumbnails/individual schedules; bounded scenario links with a collapsible REVIEW ONLY clock/intent panel; four byte-identical sprite comparisons against approved3A; four opt-in actual3B-A checkpoint videos; concise rights/QA; locally copyable bug report; explicit current vs immutable archived snapshots.

No new gameplay engine or normal NPC rules. Existing NPCManager/actor/clock and host-slot replacement are reused. Four actors/four textures/two pending remain. The browser-only review bridge is injected into the dedicated review build, never into the default game. Scenario links isolate `korean-arena-*` local/session records under `review-only-v1:`; normal play uses original keys. This is convenience isolation, not authentication/security. Studio selection and progress are never cleared. Clock controls are private-build+explicitQA only; game simulation and layer ordering remain unchanged.

## Reproduce (Node24, Python3.12 + Pillow12.3.0)

```bash
npm ci --cache /workspace/.npm-cache
npm run assets:check
npm run typecheck
npm run lint
npm run format:check
npm test
npm run build
npm run test:e2e
node tools/review-portal/build.mjs
node tools/review-portal/smoke.mjs
```

A writable npm cache is required in this cloud sandbox; use a normal writable cache on another machine. The original attempt using `/home/agent/.npm` failed; the writable-cache `npm ci` succeeded without lockfile changes. No dependencies, versions or validators are weakened. Existing browser test configuration uses installed Chromium; CI installs it via Playwright.

Default canonical Vite base remains `/3D-pharse5-/`. `VITE_REVIEW_BASE` permits a reviewed static base override. The dedicated portal game uses `./` so nested snapshot and custom review paths resolve all lazy chunks/assets. Example:

```bash
VITE_REVIEW_BASE=/3D-pharse5-review/ REVIEW_OUT=.cache/review-portal-final node tools/review-portal/build.mjs
```

Output must be inside repository `.cache/`. Use a fresh output directory for a new build; snapshots are never silently overwritten. `review-portal/phase.json` records the explicit reviewed gameRef/phase/slug. The builder refuses a nonempty output directory to prevent stale/private files leaking into a new export. The builder validates the full SHA and compares all existing game/player/NPC/world/assets paths to that commit. For a future phase, first checkpoint the completed game and review the phase adapter; do not simply reuse a stale build. The manifest records both game and portal SHAs, dirty status and actualUTC build time. The portal displays Vietnam time. Dirty candidates cannot be promoted.

## Private hosting: one-time owner setup

Use an owner-controlled HTTPS domain and server, with **all paths including assets protected**. No such host/account/domain is available or selected here, so no remote live URL is claimed. `serve.py` is an authenticated loopback origin; it refuses missing/short credentials, verifies the full export manifest at startup, serves only allowlisted paths, disables directory listings and protects GET+HEAD. It has no login database/backend/telemetry. Do not expose its HTTP port directly.

1. Choose/provision a private staging hostname/server. Keep old GitHub Pages and main unchanged.
2. Copy the generated private release to the server outside any public webroot. Keep original manifests/licenses. Set `REVIEW_USER` and a unique `REVIEW_PASSWORD` of at least16characters in the server's secret manager/environment; do not commit them or paste them into chat.
3. Start under a process manager, with the selected release as root:

```bash
python3 tools/review-portal/serve.py --root /srv/korean-review/releases/REVIEW_ID --port 4490 --base /3D-pharse5-review/
```

For a hostname-root deployment, rebuild with `VITE_REVIEW_BASE=/` and use `--base /` instead. The default candidate is tested under `/3D-pharse5-review/`.

4. Apply a real owner-controlled TLS hostname using `templates/Caddyfile.example`, proxying only to127.0.0.1:4490. Restrict server administration/firewall appropriately; no public static bypass or CDN mirror of this directory.
5. Check anonymously that `/`, `/play/`, manifests, snapshots, JS and sprites all return401; then authenticate and run desktop/mobile review, lazy assets, video playback and return/save checks. Do not send owner a link until remoteTLS/auth checks genuinely pass.
6. Report just the verified stable review URL and current phase/SHA. Credentials should be delivered via the owner's existing private secret channel.

**Remaining owner decision:** choose the access-controlled hosting provider/hostname (and provision access). This is needed because the directive explicitly withholds public exposure approval for uncleared assets. It is not a commercial release request.

## Pages investigation and future optional public path

`PAGES_INSPECTION.json` records actual API/old-site attempts: GitHubCLI Forbidden and transportCONNECT403. Current Pages source/settings/current published artifact could NOT be independently inspected. The repo's verification-only `pixel-ci.yml` and existingv0.5reference are retained. No repo/settings/workflow/Pages changes occurred. `3D-pharse5-review` is a proposed repo name, **not an existing/verified address**.

Standard Pages/noindex/private repo does not create access control. All26NPC publication decisions and whole-runtime rights remain unresolved. `REVIEW_EXPOSURE=public` fails before output; canonical `--mode public` still fails independently. Public-preview exposure must be decided separately from commercial release, for the exact artifact and each affected asset. Merely setting a boolean/input/fictional name is insufficient.

The disabled `templates/pages-review.yml.example` documents the manual-dispatch pattern; it is not installed in `.github` and contains a mandatory failure with no deploy permissions/job. After a separately reviewed exposure gate/receipt and owner approval, create a dedicated review repo; put the workflow in its DEFAULT branch; configure protectedgithub-pagesenvironment+requiredreviewer; permit contents:read, with pages:write/id-token:write on deploymentjobonly; use configure-pages@v5/upload-pages-artifact@v4/deploy-pages@v4. Explicitly promote one full checkedSHA. No PAT is needed for normal same-repo PagesActions. A feature-only workflow is not dispatchable. Do not merge gameplaymain to enable it.

## Snapshots, promotion and rollback

Static directories require noSPA fallback. Root is current; `play/` current game; `phases/<slug>/<gameSHA>-<portalSHA>/` immutable complete snapshot; portalhistory links these. Every export file has aSHA256/origin/terms/exposure entry. Manifest excludes itself to avoid circular hashing; snapshot manifest is independently preserved.

Use `promote.py CANDIDATE NEW_RELEASE_DIR` to verify hashes and prepare a new private release directory; it refuses dirty sources, path overlap or an existingdestination. Keep prior release directories. Use `--previous PREVIOUS_RELEASE_DIR` to automatically retain older immutable snapshot directories and their history entries and verify a new aggregate manifest before switching a live host. If hashes conflict, stop rather than overwrite. A protected staging process manager/symlink switch is an explicit human promotion; no automatic upload/push trigger exists. Rollback switches the authenticated origin to a retained previous release, with no save deletion or Git reset. The old Pages site is outside this process.

## Privacy/export boundary

Allowlist actualruntime assets, sanitized public NPC rights summary, names/roles/schedules, native crops, selected gameplay videos, projectlicense notices and build/QA metadata. Exclude source masters/prompts, fullrawrights inventory, account/API tokens, rawprivateauditrecords, `.env`, Git, originalsourcearchives, unrelatedreviewpages and learnerrecords. The existing game rights report keeps its26publicstatuses but its privatebundle uses a build-time sanitized inventory. This does not modify approvedsourceauditfiles or suppress any releasegate. No browseraccount or externallearningbackend is created. See export-manifest.json in the candidate.

The manifest deliberately marks public exposure NOT_APPROVED and upstreamterms incomplete for runtime assets rather than inventing an MIT blanket permission. Case-by-case concerns for six era-inspireddepictions remain open. LOW_CONCERN is not clearance. RealAndroid/iPhone/GPU remain NOTTESTED.

## Copy/paste next-phase update request

> Phase [NAME] is ready for review at checkedcommit [FULL_SHA]. Update the existing private review portal only; preserve its URL, earlier snapshots, approvedart and saves. Run tests and exact-artifact exposure/privacy gates, prepare a new immutable candidate, then promote only to the already authorized access-controlled host. Show currentvsarchived status and honestQA/rights/hardware results. No public exposure, commercial release, gameplaymainmerge or nextphase unless separately authorized. Reply with the one verifiedreviewURL after remotechecks; otherwise state NOTDEPLOYED and the exact remainingstep.

## Final local handoff

Verified candidate: `.cache/review-portal-ready/` built from clean portal-source `6bdd46abdb3c731c30d0036ee055a862eb27e091`; actual game `47107da9a859ffcc6670f99705cee7dc44d6b34a`. `FINAL_HANDOFF.json` pins its complete manifest checksum and final29portalchecks/26nativeactors/4videoplaybacks. All171unit+72E2Eare fresh. Checkpoint `checkpoint/review-portal-private-candidate-20261029` is local only; no GitHubpush/merge/Pagesdeployment occurred. Export remains PRIVATE ONLY, NOT DEPLOYED.

An incremental localGitbundle is prepared at `.cache/review-portal-source.bundle` for recovery against the existing `bc7c5916` repository, with checksum in `SOURCE_BUNDLE.json`. It is not served by the revieworigin and contains no deploymentcredentials. Do not publish it to a publichost as a workaround for the exposuregate.
