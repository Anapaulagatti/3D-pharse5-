# KOREAN ARENA — PROFESSIONAL ANIMATION & WORLD POLISH

You are the Lead Pixel Animator and Phaser Game Engineer.

Repository: `Anapaulagatti/3D-pharse5-`

## OBJECTIVE

Fix Juni's unacceptable static-image movement and improve the Gwanghwamun map's environmental composition.

Preserve Juni's approved design, the Korean architecture, functional gameplay and recoverable Git checkpoints.

## 1. UPGRADE THE ANIMATION TOOLCHAIN

Primary framework:
https://github.com/0x0funky/agent-sprite-forge

Evaluate and selectively integrate:

1. https://github.com/tachikomared/character-animation-creator-skill  
   **Priority:** Generate genuine action-by-direction frame strips from Juni's existing character reference using Codex image generation.

2. https://github.com/gykim80/perfectpixel-studio  
   **Secondary:** Reuse appropriate frame extraction, alignment, identity checks, palette processing and sprite-export techniques. Its API-dependent generation must remain disabled without explicit approval.

3. https://github.com/crsolver/claude-pxl  
   **Optional:** For deterministic environmental animation, lighting and small pixel-art effects.

4. https://github.com/GAlbanese09/spritebrew  
   **Reference only:** Evaluate its preview/export workflow. Do not integrate its AGPL code into the game without a separate licensing review.

Read the actual documentation and verify compatibility before installing anything.

Use only necessary tools. Keep external tools outside the production asset tree and avoid unnecessary dependencies.

Do not claim a skill was executed unless its real outputs and commands are documented.

## 2. MAKE JUNI TRULY ANIMATED

The current gameplay video shows static direction images sliding across the world. This must be replaced with real frame-by-frame animation.

Implement:

- Four-direction idle, walk and run.
- Alternating foot contacts and arm swings.
- Natural head and body weight shifts.
- Hair, clothing and accessory follow-through.
- Breathing, blinking and expressions.
- Smooth start, stop and turn transitions.
- Wave, celebrate and social emotes.

Use 6–10 visually distinct walk/run frames as an initial target, adjusting to motion quality.

Preserve Juni's face, hair, proportions, clothing, palette and recognizable identity in every frame.

Generate weak directions individually rather than repeatedly regenerating an entire sprite sheet.

Do not use static-frame translation, CSS bounce, simple scaling, camera motion or sprite mirroring as substitutes for genuine animation.

Keep each direction visually correct; no forward-facing eyes on a back-facing sprite.

Use correct frame registration, contact timing, alpha cleanup, pixel snapping and Phaser animation state management.

Synchronize animation cadence with player movement speed to minimize foot sliding.

Keep the native sprite dimensions suitable for Juni's proportions; never force a 64×64 cell if it crops or distorts the approved design.

## 3. MAP COMPOSITION AND PROP PLACEMENT

The Korean-inspired map artwork is acceptable, but some object placement feels random.

Perform a professional environment-layout pass:

- Keep main movement paths open and clearly readable.
- Remove or reposition isolated benches and decorative props in awkward central locations.
- Place benches near trees, scenic edges, courtyards or social seating areas.
- Place lanterns along paths, entrances and bridges.
- Group market props near stalls and building frontages.
- Keep palace landmarks, statues and gathering spaces as intentional focal points.
- Use meaningful clusters rather than random scattering.
- Respect Korean courtyard and plaza composition.
- Maintain balanced negative space and attractive visual hierarchy.

Review every prop's visual purpose, collision, interaction accessibility, player navigation and occlusion.

Use the existing Agent Sprite Forge map workflow where useful.

Do not regenerate approved architecture or redesign all three plaza concepts unnecessarily.

## 4. STRICT COST AND QUALITY RULES

No paid API calls, premium providers or billable generation without explicit user approval, even when API keys are present.

Prefer Codex's already available image-generation capability and non-billable local processing.

Do not silently run PerfectPixel's paid-provider generation or SpriteBrew's token-based generation.

If a tool cannot operate without a paid provider, report the limitation and use another legitimate animation workflow.

Do not fabricate source frames, tool execution logs, test results or runtime recordings.

## 5. REQUIRED VALIDATION

Deliver:

1. A real Phaser gameplay video demonstrating Juni walking and running in all four directions.
2. Real idle, emote, start/stop and turning animations.
3. A sprite contact sheet with visibly distinct frames.
4. A native-gameplay-scale preview and enlarged pixel-detail comparison.
5. Before/after map screenshots showing improved prop placement.
6. A concise toolchain report identifying which repositories and scripts were actually used.

Verify TypeScript, lint, unit tests, production build, browser gameplay, collision, mobile controls and sprite loading.

Run the animation at real gameplay speed, not only in an isolated viewer.

## 6. SAFETY AND CHECKPOINT

Preserve the existing playable game until the improvements are validated.

Create a recovery checkpoint, then commit and push tested changes on the current development branch.

Do not modify the separate Korean Arena learning app, expand to new districts, publish the unfinished game or trigger unwanted Pages deployment.

**EXECUTION PRIORITY:**

1. Validate the tools and select the best non-billable animation workflow.
2. Produce genuine animated Juni.
3. Integrate and verify the animations in Phaser.
4. Fix the awkward map prop placement.
5. Deliver playable video evidence and stop for visual approval.

START NOW. Do the implementation, not just a proposal.