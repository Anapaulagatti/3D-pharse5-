# Korean Arena · Pixel Town — Phase1 foundation

The approved world is frozen. Current priority is character selection, not more map production. [Current authority](docs/current/PROJECT_STATE.md).

**Roster status: INCOMPLETE.** Juni is the original fully playable character. Haneul, Bomi and Minjun have distinct reference designs but lack accepted complete native animations; they are visibly unavailable in selection. This is a technical review handoff, not completed four-character Phase1 acceptance.

- Start: `npm ci`, then `npm run dev`; open the printed local URL. The default index loads the accepted `palace-cleanup-world`, never V10.
- Canonical bootstrap: index.html → src/game/main.ts → shared src/gate3/main.ts. One world controller; registry/manager in src/characters.
- Checks: `npm run typecheck`, `npm run assets:check`, `npm run lint`, `npm test`, `npm run build`, `npm run test:e2e`.
- [Review evidence, QA and playable ZIP](docs/phase1/README.md).
- [World/Juni freeze](docs/phase1/protected-world.json), [cleanup audit](docs/current/CLEANUP_MANIFEST.md), [future gameplay contracts](docs/phase1/FUTURE_ARCHITECTURE.md).

Historical prototypes remain only where valid tests/tools/docs depend on them. `v10-city-review.html` is an explicit historical test entry, not the production world. Exact old root instructions/README are archived in docs/history/pre-phase1 and the baseline checkpoint. No history rewrite, main merge, public deployment, separate learning-app change or Phase2 implementation.
