# Korean Arena — V10 clean-room graybox

Current work is on `rebuild/southern-city-cleanroom-v10`. V9's southern map is rejected. The new masterplan and playable graybox are **awaiting user approval before final artwork**. Main and the public website are unchanged.

Start with [the review index](docs/v10-city/README.md), [masterplan](docs/v10-city/V10_NEW_URBAN_MASTERPLAN.png), [actual Phaser graybox](docs/v10-city/V10_GRAYBOX_OVERVIEW.png), [geometry comparison](docs/v10-city/V9_V10_GEOMETRY_COMPARISON.png), [workspace audit](docs/v10-city/V10_CLEAN_WORKSPACE_AUDIT.md) and [source graph](docs/v10-city/V10_SOURCE_DEPENDENCY_GRAPH.md).

Download/extract [V10_GRAYBOX_REVIEW.zip](docs/v10-city/V10_GRAYBOX_REVIEW.zip), enter Korean-Arena-V10-Graybox and run `python3 start.py` (Windows `py start.py`). Python3 required; Node is unnecessary to view. Open the printed local HTTP URL. WASD/arrows walk, Shift runs, E interacts; landscape touch joystick is retained. This is a spatial review, not final southern art or a public deployment.

## Development

Node24+, Python3.12/Pillow12.3.0 and installed Chromium. No API keys/services required.

```sh
npm ci --ignore-scripts
npm run dev
# Vite development:4200, base /3D-pharse5-/
```

```sh
bash tools/setup.sh
# Stored assets/preservation, typecheck, lint, format,12unit tests,build,15browser cases
```

`npm run preview` serves the production build on4201. `npm run assets:check` validates stored assets only; setup never authors images. Optional Forge authoring uses the recorded pin, outside production dependencies. Do not regenerate approved artwork. Existing actor scripts remain preserved tools, not setup steps.

New outdoor runtime root is public/assets/v10-city; editable plan/source is assets-src/v10-city. Protected north, Juni144frames, shared physics/joystick/mobile/Academy and source artwork remain unchanged. Old V9 coordinate-specific tests are retained under tests/archive/v9 and are not counted as current tests. Recovery tag recovery/before-v10-cleanroom-20261021 preserves the exact pre-V10 state.

Build has the documented main-chunk size warning. Physical-phone/TiledGUI/WindowsGUI testing and user visual approval remain outstanding. No final artwork, main merge, website release or paid API is authorized before the current approval gate.
