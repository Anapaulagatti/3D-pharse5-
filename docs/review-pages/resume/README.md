# Pages resume — workflow installed; game NOT DEPLOYED

Current actual destination: `Anapaulagatti/3D-pharse5-review`, default branch `main`. Initial owner commit `a4193fe5cee8ffdcb905edeefac79eae8081c911`; installed deployment-controls commit **`665cde44e5f9f010f045e986352b9dad39ca55b9`**. A successful actual Git push, not merely a dry run, proves Contents/workflow write works for this destination. See RESUME_PROOF.json. The original v0.5 repository/site received no writes.

## What changed from the earlier attempt

The repository now exists. GitHub web and normal Git transport work. `api.github.com` fails at proxyCONNECT with403 **before GitHub sends a repository-permission response**. The Pages hostname is also transport-blocked here. It would be incorrect to diagnose a missing App permission solely from this403. Do not reinstall an App or request aPAT merely on that assumption.

The real workflow is on the review repository's defaultbranch. It deploys an **existing compiled artifact commit**, with no npm/Vite/game/art build or source-game checkout. Test-only Playwright dependencies are installed AFTER deployment to open the realHTTPSsite, verify every assetURL with a boundedHEADpool, exercise all26actualNPCs/WASD/dialogue/clock/hostslots/native1×sampling, and check mobilelayout/touch/joystick. That hosted verification has NOT RUN; no live-gamePASS is claimed.

Only nonvisual deployment scripts and a PENDING review record were pushed. No sprite, video, compiledgame, fullrawrightsmanifest, privateauditrecord or canonicalart was uploaded. The compiled candidate remains local at `/workspace/review-pages-compiled`, commit **`ee0a928735d5bed527f2a3ce100b615274224061`**, with no remote configured. Its candidate branch is absent from GitHub.

## Exact candidate and exposure decision

Existing preparationcheckpoint `0e4b5016`; portalcheckpoint `f4576307`; compiledsource `6bdd46ab`. Exact candidate manifest:

`40c129fb774adf14e2bd9f707d2c50e5fe24d89d438d654172ed02e33b73018d`

All1367exportfiles were rechecked byte-for-byte against that unchanged manifest. Catalog contains26uniqueNPCidentities. Original0e's29localportalchecks/26nativecomparisons/desktop-mobileevidence remain applicable to identical bytes; they are historical test runs, not invented fresh hosted results. No portal, actor, world, collision, animation or Phase3B-A rebuild occurred.

One consolidated owner PUBLIC EXPOSURE decision is still required, covering the26individual review dispositions and other assetgroups. Commercialrelease staysBLOCKED_PENDING_REVIEW. Six qualified depiction concerns and unknown generationterms are retained in `../RIGHTS_REVIEW.md`; no new specific copied work was identified and no name-based clearance is inferred. Any specific unresolved infringement concern must be resolved or excluded before publicupload, including upload to the public compiled-artifact branch. Do not auto-fill `unresolvedSpecificConcern:false` to get a green workflow.

If a specific depiction cannot be approved, a separate sanitized export could omit that imagery and related videos/archiveactivations while preserving canonicalart. It would not prove26playableactors. A text-only public review landing is another limited alternative, not the requested fullgame. Neither substitute is silently adopted or falsely counted as26/26. The present fullcandidate stays unpublished pending the actual owner decision.

## Remaining owner steps (no tokens in chat)

1. In the review repository **Settings → Pages**, choose **GitHub Actions** if not already enabled. In **Settings → Environments → github-pages**, require ownerreview and restrict allowedbranch to `main`; protect writes to approvalrecords. These settings are not currently API-verified and are not claimed configured.
2. Review the candidate and complete the single documented exposure decision in `review-candidates/phase3b-a.json`. The named/date ownerdecision and exactmanifest must match. A publicpreview decision is separate from commercialclearance.
3. Once approved, run `receipt.py` and the complete `gate.py` locally against the compiledcandidate. Only if both PASS, push that exact existingcompiledcommit to the newreviewrepo's immutable `candidate/phase3b-a-40c129fb` branch. The current session has NOT done this because approvalisPENDING.
4. Retain the approvedrecord under `approved-releases/history/3b-a.approved.json` and select it through `approved-releases/current.approved.json`. Pushing approvedrecords on the reviewrepo `main` triggers the existingworkflow automatically. No otherpush or WIPbranch triggers publication. The required environmentownerreview happens before Pageupload.
5. Read the actual deployment `page_url` and the hosted `LIVE_QA.json`/screenshots. Announce one liveURL only after the actualHTTPSgame and controlsPASS. A repositoryURL, gitpush or workflowinstallation is not a playabledeployment.

For direct API/status and browser verification from this executionenvironment, its network/proxy must allow HTTPS/CONNECT to **`api.github.com:443`** and **`anapaulagatti.github.io:443`**. `github.com` already works. This is the concrete remaining transport gap; no hostnamealias/proxybypass is attempted. If hosteddeployment succeeds but localnetworkremainsblocked, retain honest verificationlimits rather than claiming the page opened here.

## GitHub App installation/authorization steps if Git permissions later fail

CurrentGitwriteincludingworkflow has already succeeded, so do not claim Contents/Workflows are missing now.

- GitHubaccount **Settings → Applications → Installed GitHub Apps → the actual App used by this workspace → Configure**. Under repositoryaccess, add **`3D-pharse5-review`** to selectedrepositories. For an organization, an owner must approve installation/repositoryaccess in the organization's GitHubApps settings. Reconnect/refresh the workspaceGitHubconnection after changing access.
- Inspect the App's requestedpermissions. This workflow's installation needs Contentswrite and Workflowswrite on the reviewrepo. RESTdispatch/status may require Actionswrite/read; RESTPagesconfiguration requires Pageswrite and appropriate repoadminauthority. Environment/settings administration can instead be done by the repoowner in the UI, avoiding broaderAppadministrationpermission.
- A user cannot add scopes that a third-party App does not request. Its maintainer must request an upgrade and the owner must accept it, or the owner performs the settings change in GitHubUI. Do not request personalaccesstokens/privatekeys in chat.
- After the APItransport is fixed, inspect a realGitHub403 and, where supplied, `X-Accepted-GitHub-Permissions` before naming a missingAPIpermission. A proxyCONNECT403 contains no such GitHubauthorizationdiagnosis. Original-game repositorywrite/adminpermissions are not needed by this compiled-onlypipeline.

## History and rollback

Each future approved compiled distribution retains all existing `phases/`snapshots/historylinks. Approvedhistoryrecords pin every snapshotmanifest. `history_gate.py` rejects deleting/changing a recorded snapshot during promotion or rollback. Retain compiledversionbranches and Git history, with no forcepush. For rollback prepare a new distribution selecting the old currentroot while retaining all snapshots, approve its exactmanifest, then update the samecurrentrecord. This is static packaging, not a game/art rebuild. The Pagesdestination remains the same reviewrepository.

Phase3B-B/C/DremainLOCKED. No main gameplaymerge, productionPagesoverwrite, commercialrelease, artregeneration or publicgamepublication occurred.
