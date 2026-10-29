# Exact boundary of the change

Baseline: bc7c5916 (47107da9 is the verified game review snapshot). New branch feature/one-link-review-portal.

Only three preexisting files change:

- AGENTS.md: prepend latest owner portal-only authority; historical instructions retained.
- docs/current/PROJECT_STATE.md: prepend current review task and link; no game state migration.
- vite.config.ts: `base: process.env.VITE_REVIEW_BASE ?? "/3D-pharse5-/"`. Default behavior and rights gate retained; verification workflow unchanged.

All preexisting source/game/art/atlases/schedules/dialogues/IDs/collision/save implementation/tests are byte-identical.23274existingfiles unchanged. See PROTECTED_AUDIT.json for exactbefore/afterhashes of the three permitted files.

Additive files: review-portal static UI/config; src/review/bridge.ts only injected by dedicated review build; allowlisted assembly, authenticatedloopbackserver, immutableprivatepromotion and testtools; reviewdocs/evidence. No module from the newreviewbridge is imported into canonical gameentry.

The dedicatedbuild validates existingrights inventory before compilation, then sanitizes its bundled report to only26publicnames/IDs/statuses. Fullrawprovenance/audit data stays in immutable repositorysources. This does not change src/rights/runtime.ts or contract, grant rights, disable sourcevalidation or enable publicrelease.

No liveworkflow installed, no hostingresource created, no mainmerge, no oldPagesreplacement, no sourceartgeneration, no nextphase. Disabledworkflowtemplate is documentationonly. Currentrights/hardware/ownerreviewblockers remain explicit.
