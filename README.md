# Current delivery — Gate2.5 final visual polish

[Polish review](docs/gate25-polish/README.md): localized margins/seams and tour UI/composition only. Approved art/Juni/coordinates/checkpoints retained. Physical-device acceptance NOT TESTED; STOP for explicit human approval. Gate3/merge/deployment locked. Earlier deliveries below remain historical.

# Current delivery — Gate2.5 validation

[Review package](docs/gate25/README.md). Visual foundation and localized Jeju planning amendment approved; tour, three-source district and device handoff only. Physical acceptance NOT TESTED; Gate3/merge/public deployment remain locked. Earlier deliveries below remain recoverable history.

# Gate2 five-task acceptance review

[Open current review and playable package](docs/gate2/acceptance/README.md). One new building, localized fit, one independent join and mobile camera prototype. Final human acceptance pending; Gate3 remains locked. No merge/deployment. Earlier reports below are historical.

# Gate 2 playable art review

Current delivery: [three slices, videos, native captures and playable ZIPs](docs/gate2/GATE2_REVIEW.md). Gate1 baseline is approved; Gate2 human artistic approval is pending. Gate3 remains locked. Jeju native reservation conflict and station fit allowance are disclosed proposals, not applied plan changes.

Current Gate 1 delivery: [three targeted corrections](docs/world-gate1/TARGETED_CORRECTIONS_REVIEW.md). Final approval withheld; Gate 2 locked.

Current final Gate 1 review (22 October): [revised masterplan and graybox](docs/world-gate1/FINAL_MASTERPLAN_REVIEW.md). Art direction provisionally approved; final plan pending, Gate 2 locked.

# Current review: final-world Gate 1 (style + masterplan)

Latest authority: [master prompt](docs/current/FINAL_WORLD_MASTER_PROMPT.md). [Review pack](docs/world-gate1/GATE1_REVIEW.md) · [style bible](docs/world-gate1/STYLE_BIBLE.png) · [zoning](docs/world-gate1/MASTERPLAN_REVIEW.png).

Only the new `world-gate1.html` entry represents this Gate 1. `npm run dev -- --port 4240` then open `/3D-pharse5-/world-gate1.html`; `?overview` shows labelled scaled planning, normal entry stays zoom1. Production preview build: `npx vite build --config world-gate1.vite.config.ts`. Root app/old entries remain historical unchanged baselines, not the new final world. Gate 2 and Gate 3 are locked pending user approval; no deployment or main merge.

---

# Current review: Gate1 Korean street quality sample

V10 final artwork was rejected. Only one new playable street is under review; the full V10 plan/north/Juni remain preserved and Gate2 is locked.

- [Gate1 art review and seven-category critique](docs/gate1/GATE1_ART_REVIEW.md)
- [Actual Phaser native image](docs/gate1/GATE1_STREET_NATIVE.png), [equal-scale north comparison](docs/gate1/GATE1_NORTH_VS_SOUTH.png), [gameplay video](docs/gate1/GATE1_GAMEPLAY.mp4)
- [Playable ZIP](docs/gate1/GATE1_PLAYABLE.zip): extract, `python3 start.py` (Windows: `py start.py`)
- [Sources, executed skills and reproducibility](docs/gate1/GATE1_SOURCE_AND_SKILLS.md)

Development sample: `npm run dev -- --port 4230`, `/3D-pharse5-/gate1-street.html`. Production sample: `npx vite build --config gate1.vite.config.ts`, then `python3 tools/gate1_package.py`. Existing default world entry/build remains the unchanged approved graybox and is not the Gate1 sample. No main merge or deployment. Await explicit visual approval before any full-world production.

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
