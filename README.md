# Korean Arena — V9 southern world reconstruction

Vietnamese-first Korean learning pixel town, built with the existing Phaser foundation. **V9 is a playable review candidate awaiting user visual approval.** Work stays on `rebuild/pixel-social-rpg-v3`; `main` and the public website are preserved.

Read AGENTS.md, docs/current/V9_TOTAL_SOUTHERN_WORLD_RESET.md and the four STUDIO records. The approved historical north and Juni144-frame animation are protected independently. Superseded southern implementations were removed only after the pushed recovery tag documented in SOUTHERN_RESET_CLEANUP.md.

## Development

Node24+, Python3.12 with `tools/requirements.txt`, locked npm dependencies and Chromium are used. `bash tools/setup.sh` verifies stored artwork, types, lint, formatting, unit tests, build and actual browser tests. It never generates artwork or calls a provider. Optional external authoring tools are not setup/runtime dependencies.

```
npm ci
npm run build
npm run preview -- --host 0.0.0.0
```

Open `http://localhost:4201/3D-pharse5-/v9-world-review.html` **in a browser**. A source-file preview in chat displays HTML text and does not run the game. The server address is local/internal, not a public showcase URL.

Arrow keys/WASD or the analog joystick move Juni. Hold Shift/the Run button to run; E/Explore interacts, Space waves. Settings include native zoom, reduced motion and Canvas compatibility. The approved Academy lesson and palace gate remain functional.

## Current review sources

- PIXELS_WORLD_DESIGN_STUDY.md distinguishes observations, unavailable references and original design choices.
- assets-src/v9-world/plan/city.json and city.svg are editable V9 planning data.
- docs/v9-world contains actual engine evidence, an input-driven gameplay capture, a playable HTTP review ZIP and V9_CITY_REBUILD_REPORT.md. Graybox evidence is labeled separately from final illustrated candidate captures.
- assets-src/protected-north preserves exact north art/geometry; assets-src/library holds reusable original art with provenance and no rejected southern placements.
- assets-src/juni-animation preserves editable character sources; src/engine holds the approved shared movement/occlusion adapter.

No paid API, automatic publication, main merge or separate learning-app modification is authorized. The finished V9 package must stop for user visual review.
