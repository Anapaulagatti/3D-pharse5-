# GitHub Pages review handoff — NOT DEPLOYED

Owner selects GitHub Pages, using a **separate** repository named `Anapaulagatti/3D-pharse5-review`. This supersedes the previous provider-neutral authenticated-server recommendation. No Cloudflare resource existed or was changed. Existing portal checkpoint `f4576307` is preserved; no portal/game rebuild or artwork generation was performed locally.

## Current concrete result

`.cache/review-pages-candidate/` is a locally prepared, playable public-preview **candidate**, derived from the already tested `.cache/review-portal-ready/`. It is not approved for public exposure. `PREPARATION_QA.json` pins its exact whole-site manifest checksum. The approved compiled Phaser JS/CSS, textures, native frames,26IDs/12characters/28cosmetics, routes and collision are byte-identical. Only exported presentation/decision metadata and a Pages-specific startup wrapper differ. Original portal source, accepted checkpoints and the old verification workflow remain unchanged.

The wrapper is necessary because the two project Pages sites share the `github.io` origin and browser storage. Both normal review play and QA use `korean-pixel-town-pages-review:`-prefixed records, while source game save keys remain unchanged. QA retains its additional separate namespace. Existing production keys/data are not migrated, deleted or reused. Fresh review visitors use the original Character Studio. This is an additive deployment wrapper, not another game engine or a map/UI rebuild.

Native/source/provenance/rights audits remain available from Phase3B-A. Public naming does not clear likeness or image rights. Commercial release remains `BLOCKED_PENDING_REVIEW` even if the owner separately approves this public development preview.

## Exact blockers

1. Current `gh api user`, target-repository and production-Pages requests all return `Forbidden`. Repository existence, authenticated owner identity, creation permission, Pages plan/settings and current live site could not be verified. No repository was created and no settings were changed. See `ACCESS_PROBE.json`.
2. No explicit public-preview publication decision has been received for this exact candidate. `bootstrap/exposure-approval.json` remains PENDING for all26individual NPCs and the other asset groups. Renaming or changing a commercial flag is insufficient.
3. Six qualified depiction-review concerns remain open. No concrete copied third-party source was established by the limited prior audit; this does not certify absence of copying. See `RIGHTS_REVIEW.md`. Any specifically disputed depiction must be excluded or independently resolved before publication. Deleting only an atlas from this26-actor build would produce broken textures; it is not a safe exclusion. No hidden removal, art substitution or count inflation was performed. The complete candidate stays unpublished until those decisions are resolved.

## One-time owner setup

Authenticate GitHub in the execution environment, or perform the following in an owner-controlled terminal. Do not send tokens/private keys in chat.

1. Inspect whether `3D-pharse5-review` exists. If absent, create it **private**, initially containing no game art. Preparation artifacts in a public repository are not access-controlled staging. Standard Pages sites can be publicly accessible even when their source repo is private.
2. Confirm the account/plan supports GitHub Pages from this private repo. If it does not, stop before changing visibility or publishing; a public-artifact-only alternative requires a separate reviewed exposure decision. Do not silently make the source/artifact repository public.
3. Copy the contents of `docs/review-pages/bootstrap/` into that new repository's **default branch**. The workflow must actually be at `.github/workflows/review-pages.yml` on that default branch. A feature-only workflow is not dispatchable. This is the review repo's branch, not a gameplay-main merge.
4. Enable Actions and Pages → Build and deployment → **GitHub Actions** in the review repo only. Configure the `github-pages` environment with the owner as required reviewer, prevent self-approval where supported, and restrict it to the review default branch. Protect that branch/approval record from unreviewed writes. If these controls are unavailable on the plan, report that limitation rather than claiming protected promotion.
5. If the original game repository is private, its cross-repo checkout needs a narrowly scoped read-only source deploy key. Store it as `PIXEL_SOURCE_DEPLOY_KEY` in the review repo; add the public key read-only to the original source repo. The optional workflow input uses this key only for source checkout. A default review-repoGITHUB_TOKEN cannot read another private repo. No broad PAT is required.
6. Enable write permission for the archive job to **this review repo only**. All other preparation/verification jobs are contents:read; archive alone uses contents:write; deployment alone has pages:write/id-token:write. No original-source repo or old Pages deployment permission is requested.
7. Manually dispatch `prepare`. It checks out the explicitly pinned source, runs existing validation, compiles the existing portal code without art generation, prepares the candidate and carries forward previous immutable snapshots. This is normal reproducible deployment compilation, not rebuilding the portal design. Its artifact is private, retained30days pending review. No Pages artifact is uploaded.
8. Download/review that run's actual artifact, check its exact manifest and complete the individual NPC and group decisions. Record a named/date owner decision `APPROVED_PUBLIC_PREVIEW` and that exact manifestSHA256 only after review. Rebuilding changes timestamps/hashes: a local approval cannot silently approve a different Actions artifact. Do not auto-fill pending reviews or mark unknown generation terms verified.
9. Only after that explicit approval, dispatch `publish` with the successful prepare runID. The gate verifies all files, source lineage,26individual reviews and asset-group decisions. It first saves the approved generated site into `pages-snapshots` with ordinary fast-forward Git history. The deploy job then waits for the required environment review and uses configure-pages@v5/upload-pages-artifact@v4/deploy-pages@v4. There is no push-triggered deployment and no force-push.
10. Obtain the actual `page_url` from the deployment output/API; verify remoteHTTPS, all lazy asset URLs,26NPCreview, actual gameplay controls, native rendering, clock/host slots, mobile emulation, bug report and return/save behavior. Only then report that one real live URL. No proposed URL is represented as verified here.

## Exclusions and exposure decisions

Raw prompts/source masters, full sensitive audit records, `.env`, tokens, private account data, learner records and noncanonical old review pages are not exported. No factual celebrity cards/photographs/voices/logos were added. The gate checks source/manifest hashes and rejects missing/unmanifested files. An approval file is a human decision record, not a legal license or proof that every assertion in it is true; required human/environment review remains essential.

A specifically unresolved depiction cannot be made publishable by merely setting `unresolvedSpecificConcern:false`. Supply the actual independent review and resolution, or request an isolated public-safe asset/registry candidate. That latter change is not performed under this no-rebuild task. The six concerns and all commercial blocks remain visible in the owner's review package.

## Same URL, history and rollback

`review-source.json` pins the first source `f4576307` and its verified existing build lineage `6bdd46ab`. Future phase releases require an expressly reviewed new fullSHA/config; no nextphase development is authorized here. The actual PagesURL remains attached to this same review repository.

Prepare reads the durable `pages-snapshots` branch, verifies its manifest and retains prior `phases/<slug>/<gameSHA>-<portalSHA>/` directories plus history links. A conflicting immutable snapshot fails; nothing is overwritten. The next complete artifact is approved with prior snapshots already included. Artifact30dayretention is not the long-term history mechanism: approved snapshots are also in the review repository's Git history.

Rollback within artifact retention may select an earlier successful prepare run, with a matching owner approval receipt. For older releases, restore the exact retained approved generated site from `pages-snapshots` Git history into a new candidate and repeat manifest/owner checks. Do not force-push, delete snapshots, or reset gameplaymain. Monitor actual Pages/repository size quotas before later phases; no automatic deletion of historical versions is authorized.

## Tests and stop

See `QA.md`, `PREPARATION_QA.json`, `PORTAL_SMOKE.json`, `EXTRA_SMOKE.json` and `RIGHTS_REVIEW.md`. Source checkpoint's171unit/72E2E results are historical here, not rerun counts. Current task tests the derived artifact and unchanged compiled bytes, save isolation, gate and workflow structure. Real GitHub-hosted Actions/deployment/remotePages and physicalAndroid/iPhone/GPU are NOTTESTED. No Phase3B-B, gameplaymainmerge, originalPagesoverwrite, paidartAPI or publicpublication occurred.
