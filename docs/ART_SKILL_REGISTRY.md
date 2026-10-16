# Korean Arena — Mandatory Art & Animation Skill Registry
_Last recorded: 2026-10-16. Scope: this standalone Phaser 2D pixel game only._

## Read-first contract (every new Codex session/task)
1. Read **AGENTS.md**, this registry, **STUDIO_TASKS.md**, **STUDIO_PROGRESS.md**, **STUDIO_DECISIONS.md**, and **STUDIO_ASSETS.md** before changing art, animations, world layouts, or NPCs.
2. For EVERY art/animation/map task, load the applicable external **SKILL.md** files below, not just their names. Verify tool availability/version and match the task to a pipeline. If the tool is missing, report it truthfully.
3. Consult the real project production records: `docs/gwanghwamun/FORGE.md`, `docs/juni-animation/TOOLCHAIN.md`, `docs/juni-animation/REVIEW.md`, and source manifests in `assets-src/gwanghwamun/` / `assets-src/juni-animation/`. Reuse their successful approaches instead of reinventing or blindly regenerating approved art.
4. Before work: verify branch, preserve remote recoverability, respect user-approved Juni animation and Gwanghwamun art/layout as the current baseline. After work: record exact commands, installed/inspected versus ACTUALLY EXECUTED skills, asset provenance, run metrics/warnings, visual review artifacts, tests, commit and recovery tags.
5. **No paid API, tokens, provider generation or billable calls without explicit fresh user approval, even if API keys exist.** No automatic Pages/game publication. Do not touch the separate Korean Arena learning-app repository.
6. Keep external skill/tool repositories in reproducible, pinned tooling caches or documented development environments, **not** vendored into production assets. Check licenses before copying any code or art. Setup/build must never regenerate source artwork or contact a paid provider.

## Tool registry (inspect pinned revision before upgrading)

| Source / pinned reference recorded in last review | Actual role | What has truly been used |
| --- | --- | --- |
| [Agent Sprite Forge](https://github.com/0x0funky/agent-sprite-forge) @ `5324342fdfab72430f4e9604f3fe427009f8596d` | Main image/sprite/map/processing pipeline; read all five SKILL.md when relevant: `generate2dsprite`, `video2dsprite`, `generate2dmap`, `generate2dmedia`, `codeart2d` | **Executed:** image-route diagnostics, prop extraction, map/Tiled/nav verification, sprite/PNG clean/finish, palettes, animation clip/export/QA; **not executed:** paid video generation or complete video-to-sprite action synthesis. |
| [Character Animation Creator Skill](https://github.com/tachikomared/character-animation-creator-skill) @ `9ce98dffb98c84488fe7b99b62c49fabee20abd6` | Use `SKILL.md` for character-reference-grounded action/direction strips, targeted frame repairs, source manifests, visual QA | **Executed:** 23 host-image-generation calls for Juni (20 initial + 3 revised); action/direction strip assembly, validation and preview scripts; resulting 144 authentic sprite frames. |
| [PerfectPixel Studio](https://github.com/gykim80/perfectpixel-studio) @ `a1385cc99eb4b6983c945adb8cca7b2b71f53d0f` | Optional QA/animation reference, 8-way/palette/segmentation techniques; `skill/perfectpixel/skills/perfectpixel/SKILL.md` | **Inspected only**, QA concepts evaluated; `ppgen` **not** installed/executed because media generation requires provider API credentials. |
| [claude-pxl](https://github.com/crsolver/claude-pxl) @ `21fee41f7ecce00bc868d7567f24ffd0f3acc8fa` | Optional deterministic ambient scene FX, e.g. lanterns and water, only if source art quality is preserved | **Inspected only**; not executed in Juni deliverable. |
| [SpriteBrew](https://github.com/GAlbanese09/spritebrew) @ `5ac9fdbe38793be6c2b8485c397262a27820144d` | **Reference only** for preview/sheet export design | **No code integrated**. AGPL-3.0; provider/token costs. Do not vendor without separate licensing/authorization review. |

Pinned revisions document reproducibility, **not** a claim that newer revisions are automatically compatible.

## Approved reusable pipeline
- **New characters/NPCs:** official Forge `generate2dsprite` for attractive reference-grounded, original character masters; ensure four-direction consistent art, palette, silhouette and game-size legibility. Create truly distinct features, don't copy older rejected procedural actors.
- **Animation:** Character Animation Creator per-action/per-direction imagegen strips (when available under authorized route); targeted re-edits, not full rerolls. Forge `video2dsprite` *processing only* for existing PNG frame sequences when video route is unavailable. Register anchors/feet, clean alpha, finish pixel palette, export frames/JSON and play **real sprite-frame cycles** inside Phaser. Video synthesis only when a safe, explicitly approved route exists.
- **District/maps:** Forge `generate2dmap` and `generate2dsprite` for original authentic Korean buildings/foliage/props; layered semantic map and Tiled export, map bundle/navigation/collision/read-back checks. Build prop placement around real uses (doorways, seating, pathways, gardens); never random obstruction in the plaza or central roads. Distinguish original concept renders from real native Phaser screenshots.
- **Runtime QA:** genuine normal-speed input-driven video and playable preview; geometry, direction, motion, alpha, reachability, occlusion/Y-sort, mobile touch, Canvas fallback, build/test/CI. Preserve actual failures/warnings; do not claim tool execution just because it is installed or its reference is read.

## Current acceptance and next work
- **User accepted as working baseline:** Juni/B identity and current 144-frame animation, Gwanghwamun pixel assets and reorganized plaza props. Small known idle/wave motion warnings are documented, not silently erased.
- **Next requested scope:** expand the plaza into one navigable, Seoul-inspired Korean district, with four distinct historically informed educational NPC buildings/interiors/courtyards, original historical guests, pathways and local learning interactions. Take **Pixels.xyz as high-level inspiration for connected neighborhoods/exploration**, never copy proprietary art, maps, names, business mechanics or assets. Keep the world fictional and historically respectful.
- Keep the game playable and recoverable after each checkpoint, review the district at native scale. Do not automatically publish unfinished game.

## Living Seoul first-slice execution / current handoff (2026-10-16)

Read docs/living-seoul/REVIEW.md and TOOLCHAIN.md. Actual3hostimage calls; Forge prop extract/finish/palette/bundle/nav/linked portals/Tiled/HTTP diagnostic used.8approvedterrain/Juni144frames reused; no new Creator animation or historical NPCs produced. First2048×768connected map +Academy interior/letter station complete for visual review; other footprints/guests remain planned. Preserve raw18unownedsourcepixelsWARN and room marker portal-reset keyboardFAIL; actual Phaser interactions and linked reachability verified. Mandatory skill reads remain required for all later work. No paid routes, website release or remaining-area mass production before first-slice review.

## Latest scope — urban zoning gate (2026-10-16)

Latest docs/current/URBAN_LOGIC_RESET.md overrides earlier expansion-first scope: produce and approve zoning BEFORE final map artwork/assembly. Current docs/urban-zoning is planning only. Actual generate2dmap +generate2dsprite SKILL.md read at pinned Forge5324342; no new image/API/extraction/map-bundle/nav/Tiled execution claimed. Existing approved Juni and source assets/runtime retained; planned NPC positions are not produced sprites. After zoning approval, use the real layered-map/prop/terrain/navigation/export workflow and inspect Phaser; do not convert this diagram into generic code-drawn game art. Main/Pages unchanged; PR only after finished district review/testing/clean clone, merge separately authorized.
