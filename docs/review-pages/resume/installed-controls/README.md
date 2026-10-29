# 3D-pharse5-review

## Deployment status: NOT DEPLOYED

This repository contains deployment controls only. The compiled Phaser Review Portal and artwork have NOT been pushed here. Owner public-exposure approval remains PENDING. No Phase3B-B/C/D is authorized.

The workflow deploys an existing, pinned compiled-site commit: no npm install, Vite rebuild, NPC/art generation or gameplay-source checkout. Both manual deployments and automatic updates require an exact manifest and completed individual exposure records, then the protected github-pages environment. Commercial release remains BLOCKED_PENDING_REVIEW.

### First owner setup

1. In Settings → Pages, select GitHub Actions. In Settings → Environments → github-pages, require owner review, restrict to main and protect approved-releases records. API/settings access must actually work; these settings are not claimed configured by this commit.
2. Review the pending candidate record under review-candidates. Resolve each specific depiction concern or exclude it in a functioning public-safe subset; do not treat fictional names or a boolean as clearance. One consolidated owner decision may cover all individual records. Do not publish artwork while this record is PENDING.
3. Only after explicit public-exposure approval, push the matching already-compiled artifact commit to an immutable version branch in this review repository. Verify the branch and exact manifest; no source rebuild is needed.
4. Commit the signed-off record to approved-releases/current.approved.json and retain an immutable copy under approved-releases/history/<phase>.approved.json. A push of an approved record starts the same Pages workflow automatically. The protected environment still requires owner review before upload.
5. Confirm the actual deployment page_url and playable HTTPS site, desktop/mobile controls, all26NPCs, clock, snapshots and console before announcing a live link. This repo README or a successful Git push is not a playable deployment.

### History and rollback

Each compiled release must include the earlier immutable phases directories and history links. history_gate.py rejects removal or modification of a recorded snapshot manifest. Retain all compiled version branches and their Git history; never force-push. For rollback, prepare a new compiled distribution whose current root selects the older approved snapshot while retaining ALL existing phase snapshots, obtain approval for its exact manifest, and promote via the same receipt workflow. No gameplay rebuild or production-site change is required.

### Safety boundary

The project path is /3D-pharse5-review/. Normal and QA saves are isolated from the existing v0.5 project site, which shares the github.io origin. The original game's repository, Pages workflow and artwork are untouched. No tokens or private source/audit materials belong in this repository. A noindex tag is not access control.

### Current access diagnosis and authorization

Repository existence and actual Git/workflow write have been verified. REST requests fail at proxy CONNECT to api.github.com before GitHub can evaluate repository permissions; the Pages hostname is also blocked from this execution environment. Do not diagnose this as a missing App scope from the403 alone. For direct verification, allow HTTPS/CONNECT to api.github.com:443 and anapaulagatti.github.io:443 in the environment's network/proxy settings. github.com/Git transport already works.

If Git/App permissions later fail: GitHub Settings → Applications → Installed GitHub Apps → the actual workspace App → Configure → add this review repository to selected repositories. An organization owner must approve organization installation/access. Refresh the workspace connection afterward. Contents/Workflows write already worked here; optional REST dispatch needs appropriate Actions access and Pages settings APIs need Pages/admin authority. The owner may configure Pages/environment in GitHub UI instead of granting broader App administration access. A third-party App's maintainer must request any new permission before an owner can accept it. Do not paste personal access tokens or private keys into chat.

Public exposure is still PENDING. The compiled candidate is local-only and pinned by its exact manifest; no game/art branch was pushed. The6qualified depiction-review questions remain open, and unknown upstream generation terms are not cleared by fictional names. Resolve specific concerns or choose a separately reviewed sanitized subset; do not represent a reduced/blocked subset as26playableactors. Commercial release remains independently blocked. Phase3B-B/C/D remain locked.
