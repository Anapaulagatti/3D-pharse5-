# Current refinement gate

The overall zoning has provisional user acceptance. The user requires approval of the refined masterplan before final buildings/map production; this is not completed-district visual approval or merge/publication permission. Read URBAN_PLANNING_REFINEMENT.md and PLAN.md first. Main/Pages stay unchanged. The future promotion sequence below remains in force and must be rerun against current refs after production/review gates.

## Previous audit / retained promotion policy

# Future main promotion — prepared policy, no PR/merge/deploy now

The latest user request explicitly makes district visual approval, gameplay tests and clean-clone verification prerequisites to preparing a PR targeting main. The current action is the zoning proposal only. There is no approval of the new district and no publication authorization. Therefore **no PR is opened yet**, no merge, no main push, no Pages settings write and no deployment run.

## Audit observed before this proposal

- Read-only HTTPS ls-remote: stable main = `33360ed1989e4db9fc3fc4e3686ca385e0b00908`; development = `d5701fc251913e28ad9cea6ae3404a88a553adbd`. Refreshed origin/main explicitly; an initially stale local tracking ref was not used for final conclusions.
- Actual main is an ancestor of the development baseline. No deleted tracked paths in `git diff --diff-filter=D origin/main...d5701fc`; approved main assets are retained. The broad multi-milestone difference needs a fresh review at promotion time, not just this small document diff.
- Development includes `AGENTS.md` and `docs/ART_SKILL_REGISTRY.md`; they will be part of the future merge. Do not omit handoff/registry or recoverable editable sources.
- Local and remote recovery/checkpoint refs were inspected; new pushed recovery `recovery/before-urban-zoning-20261016` peels to d5701fc. Existing tags must not be retargeted/deleted.
- GitHub API lists one active workflow: `385009969`, Verify pixel art review candidate, `.github/workflows/pixel-ci.yml`. It runs push(main/development)/PR checks, contents:read, no pages:write/id-token:write/deploy job. Workflow files are unchanged by this proposal.
- Pages API build_type=`workflow` (the reported legacy source metadata is main:/; it is not a branch-publishing setting). Public site remains old v0.5, HTTP200 / HTML SHA256`082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f`. No new site release is inferred from source commits.

## Re-run immediately before a future PR

1. Obtain explicit user visual approval of the completed district. Refresh main/development refs, inspect unknown upstream work and a full name-status/code/asset diff. Classify every deleted asset, license and source file; verify recovery tags via independent HTTPS clone. Never assume today's audit remains current.
2. Review source/runtime dimensions, assets, collisions, entrances, NPC placements, UI, quest/learning behavior and actual desktop/mobile gameplay evidence. Keep the separate learning application untouched.
3. Read full current Actions files/API and Pages settings again. Check push/PR/workflow_run/reusable/external deployment triggers and any Pages builds/deployments; ensure verification cannot publish. Do not change Pages settings or enable publication without explicit permission.
4. Update README/current docs to the actual visually approved district, with limitations and exact playback steps. Preserve historical recovery docs. Check registry and AGENTS in the PR tree.
5. Run full CI on the candidate. Fresh HTTPS clone at the exact SHA, frozen npm install, offline assets/type/lint/format/unit/build/browser checks, real rendered review. Resolve actual merge conflicts on the development branch after inspecting both sides, retaining current main and recoverable user work. A clean merge-tree today is not proof of a future merge.
6. Only then prepare a PR targeting main, explaining concrete behavior, scope, asset changes, evidence, warnings and independent verification. Do not mark incomplete art as approved. Request explicit **merge** authorization; visual approval alone is not that authorization.
7. On merge authorization, normal merge or fast-forward only, no force/history rewrite; retain development and all recovery tags. Confirm resulting refs/CI and unchanged public site unless publication was separately authorized.

Current proposal updates the stale README to the real accepted Juni/retained plaza baseline and explicitly pending district zoning. It does not describe the proposed 4096×3072 world as implemented or approved.
