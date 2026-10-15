# KOREAN ARENA — PIXEL PRODUCTION & REPOSITORY CLEANUP
## Unified Master Prompt for Codex

You are the Lead Pixel Artist, Character Animator, Phaser Engineer, and GitHub Maintainer for Korean Arena.

**Repository:** `Anapaulagatti/3D-pharse5-`  
**Development branch:** `rebuild/pixel-social-rpg-v3`

Verify the latest remote commit before making changes.

## MISSION

Complete three tasks in order:

1. Use Agent Sprite Forge to significantly improve chibi character animation.
2. Create expressive Korean historical NPCs matching the current pixel art style.
3. Remove obsolete 3D and rejected 2D files, leaving one clean, maintainable pixel game repository.

Execute the work, not just a plan. Preserve recoverable checkpoints throughout.

## 1. PRESERVE THE CURRENT ART DIRECTION

The current chibi avatar, buildings, trees, and Pixel Town aesthetic are provisionally accepted.

Keep the existing:

- Cute chibi proportions and recognizable character identity.
- Hairstyles, outfits, accessories and facial expressions.
- Korean-inspired environment.
- Phaser, TypeScript and Vite foundation.
- Functional movement, collisions, customization and UI.

Do not redesign the town or regenerate acceptable artwork unnecessarily.

Focus on making the characters feel alive.

## 2. AGENT SPRITE FORGE — USE THE ACTUAL SKILLS

Official repository:
https://github.com/0x0funky/agent-sprite-forge

Inspect and verify all five skills:

- `generate2dsprite` — character masters, sprites, expressions and accessories.
- `video2dsprite` — action animation, looping, timing and frame registration.
- `generate2dmap` — modular pixel maps, props, tiles and collisions.
- `generate2dmedia` — media-route diagnostics and capability checks.
- `codeart2d` — deterministic pixel drawing and animation when appropriate.

Check installation, dependencies and execution capability using the repository's documented tools.

**Actually use the relevant pipelines. Do not claim a skill was used merely because it was installed.**

For each workflow, record the real command, source assets, outputs, validation results and any unavailable capabilities.

Do not reinstall working tools unnecessarily.

### Cost restrictions

No paid API calls, video-generation providers or billable services without explicit user approval.

Even if API keys are configured, report the intended provider and cost before any billable generation.

Prefer existing assets, available authorized tools and deterministic sprite workflows.

If image-to-video is unavailable, improve animation through authored frames and supported registration, timing and pixel-QA tools instead.

## 3. CHIBI ANIMATION OVERHAUL

The current avatar looks good but its animation still lacks professional game feel.

Preserve its visual identity while improving:

- Idle, breathing and natural blinking.
- Four-direction walking.
- Four-direction running with a genuinely distinct gait.
- Acceleration, stopping and turning.
- Clear alternating steps and arm movement.
- Foot placement without sliding.
- Body weight shifts and anticipation.
- Hair, clothing and accessory follow-through.
- Waving, celebrating, thinking and social emotes.
- Distinct expressions coordinated with actions.
- Smooth transitions back to idle.

Apply suitable animation principles, consistent body proportions, reliable frame registration, pixel-perfect edges and stable palettes.

Use Sprite Forge's applicable animation, loop-selection, retiming, finishing, QA and export tools where they work.

**Animations must look convincing at normal gameplay speed, not only in isolated frame previews.**

Capture real Phaser footage showing the character walking, running, stopping, turning, greeting and changing expressions.

## 4. HISTORICAL KOREAN NPCs

Replace outdated generic demo NPCs with original chibi pixel interpretations of:

- **King Sejong (세종대왕):** Hangul and language learning.
- **Jang Yeong-sil (장영실):** Inventions and problem-solving.
- **Shin Saimdang (신사임당):** Art, culture and nature.
- **Admiral Yi Sun-sin (이순신):** Strategy and historical adventures.

These are educational guest characters in a fictional world, not a claim that they lived in the same era.

Each NPC needs:

- Recognizable, historically informed original design.
- Distinct hairstyle, clothing and accessories.
- Four-direction sprites.
- Expressive idle, walking, blinking and greeting animations.
- At least two facial expressions.
- One interactive educational dialogue.
- One small Korean-learning quest concept.

Use Vietnamese-first dialogue with suitable Korean vocabulary.

Maintain the same pixel scale, shading, outline style and animation standards as the player.

Avoid copying modern portraits or copyrighted game assets.

Build one NPC first, validate visual quality and reusability, then produce the remaining three.

## 5. COMPLETE GITHUB CLEANUP

The repository contains thousands of obsolete historical assets.

Perform a real cleanup after the improved assets are verified.

### Mandatory backup

Before deleting files:

1. Inspect Git branches, tags, workflows and active dependencies.
2. Commit and push all current working files.
3. Create verified recovery tags for the current pixel project and historical 3D project.
4. Test recovery from the remote repository.
5. Document recovery steps in `docs/RECOVERY.md`.

Never force-push or rewrite history.

### Delete obsolete files

Remove unused:

- Three.js, React Three Fiber, Drei and 3D-only dependencies.
- Blender, GLB, old 3D sources and showcases.
- Rejected 2D experiments and superseded character designs.
- Unused sprite sheets, maps, textures and generated assets.
- Duplicate production asset folders.
- Historical review screenshots, videos, ZIP files and render attempts.
- Temporary QA outputs, stale reports and abandoned scripts.

Trace imports, sprite atlases, dynamic asset paths, tilemaps and build scripts before deleting anything.

**Never delete the latest chibi sources, current environment, new historical NPCs, required animation frames, active development tools or license information.**

Keep one current review package and store future temporary artifacts outside tracked Git files when possible.

Update `.gitignore`.

### Target structure

```text
src/
public/assets/
assets-src/
tools/
tests/
docs/
.github/workflows/
README.md
AGENTS.md
PIXEL_ART_BIBLE.md
STUDIO_TASKS.md
STUDIO_PROGRESS.md
STUDIO_DECISIONS.md
STUDIO_ASSETS.md
CLEANUP_REPORT.md
package.json
package-lock.json
vite.config.ts
```

Adapt this structure to actual code dependencies.

### GitHub main branch

Prepare the cleaned Pixel RPG to become the primary repository project.

The existing `main` branch currently contains old 3D work.

Promote the cleaned 2D source to `main` only if it can be done safely without automatically deploying the unfinished game.

Inspect GitHub Pages and Actions triggers first.

If promotion would unexpectedly replace the public website, stop at that boundary and ask for approval.

Keep the old projects recoverable through verified Git tags.

## 6. VALIDATION

From a fresh clone of the cleaned repository, run:

- `npm ci`
- TypeScript checks and lint.
- Unit tests.
- Production build.
- Playwright browser tests.
- Sprite atlas and animation checks.
- Four-direction movement and collision tests.
- NPC interactions.
- Outfit and expression changes.
- Mobile, reduced-motion and rendering fallback checks.
- Missing asset and console-error checks.

All core features must still work after cleanup.

Do not invent test results or FPS measurements.

## 7. REQUIRED DELIVERABLES

Provide:

1. A real before/after Phaser animation video.
2. A player and historical NPC comparison board.
3. An actual in-game screenshot containing the upgraded characters.
4. A playable review build.
5. A Sprite Forge usage report identifying skills and tools actually executed.
6. `CLEANUP_REPORT.md` with before/after file counts, deleted directories, retained assets and verified recovery tags.
7. The final GitHub commit and CI status.

Update all four `STUDIO_*` progress files and push verified checkpoints after meaningful milestones.

## 8. STRICT BOUNDARIES

Do not:

- Modify the separate main Korean Arena learning application.
- Rebuild approved environments unnecessarily.
- Create additional learning districts.
- Implement unrelated gameplay, multiplayer or advertising features.
- Buy services or invoke paid APIs.
- Publish the unfinished game without authorization.
- Destroy Git recovery history.

## EXECUTION ORDER

**Gate A:** Verify Sprite Forge and preserve Git backups.

**Gate B:** Improve the chibi animation and prove it in Phaser.

**Gate C:** Create and validate the four historical NPCs.

**Gate D:** Clean obsolete repository files and consolidate project structure.

**Gate E:** Run full validation, push verified checkpoints and prepare the review package.

After completion, STOP for user review.

**Success means: expressive game-quality animation, memorable historical NPCs, and one clean GitHub repository containing the latest working Korean Arena pixel game.**

START NOW.