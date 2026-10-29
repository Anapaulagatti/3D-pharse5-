# Controlled private review and public-release gate

`assets-src/rights/npc-inventory.json` is independent of entity IDs and saves. Shared `src/rights/contract.ts` validates complete unique 26-ID coverage, exact source/hash records, independent risk/publication states, and commercial-approval evidence consistency. `tools/rights-gate.mjs` is used by Vite preflight.

Commands:

- `node tools/rights-gate.mjs` — approved private-review preflight.
- `npm run build` — ordinary project validation and explicitly marked private-review output.
- `node tools/rights-gate.mjs --public` — strict public preflight; currently expected to fail.
- `npx vite build --mode public` — public Vite profile, also required to fail before emission.

`package.json` is itself a historically protected file, so it remains byte-identical. No scripts, dependencies, lockfiles or validator expectations are weakened to add convenience commands. Vite mode/build environment controls the release profile. Query parameters and localStorage do not confer any publication approval.

All 26 required actors are BLOCKED_PENDING_REVIEW. A public build fails with exact asset IDs, statuses and the review-queue path. It never deletes actors, substitutes sprites or pads counts. Included unresolved factual/reference records also block public emission. Excluded modern fact cards and old noncanonical historical fixtures remain blocked; public mode has only the canonical game entrypoint, not legacy review pages.

Fictional names, human artistic approval and AI generation do not establish commercial rights. Approval requires documented applicable creation/account terms plus independent review/publication status. This structural gate cannot authenticate invented evidence or replace counsel. Nor does it clear unrelated world/player/music/font assets for eventual commercial distribution.

The private Settings rights report is collapsible without introducing a nested Options summary; original menu selection/accessibility contracts remain. QA clock tools and the report are private-build controlled. No public deployment is authorized.

No specific copied third-party depiction was established by the limited input/roster review, and generic historical fashion is not automatically erased. Zero art candidates were generated. Residual royal/naval/historical-photo associations remain NEEDS_REVIEW and blocked from publication. If a substantiated concern requires a redesign, preserve the approved pack, create a versioned isolated candidate and obtain specific human art acceptance before adoption.
