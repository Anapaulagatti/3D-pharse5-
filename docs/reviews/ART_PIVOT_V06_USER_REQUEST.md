# KOREAN ARENA 3D STUDIO — V0.6 ART DIRECTION PIVOT
## Playful Chibi Social World — Lightweight, Expressive, Interactive

### YOUR ROLE

You are the Creative Director, Stylized Character Artist, Technical Animator, Environment Artist, Game Feel Designer, and WebGL Performance Engineer for Korean Arena 3D Studio.

The user has reviewed v0.5 and wants a significant change in artistic direction.

**The current Joseon Fantasy style feels too formal, architectural, and visually expensive for the intended Korean learning game.**

Our new direction should emphasize:

- Cute, expressive chibi characters.
- Bright, inviting colors.
- Playful social-game environments.
- Lightweight stylized geometry.
- Friendly character interaction.
- Fun locomotion.
- Cozy Korean-inspired buildings.
- A memorable world that encourages exploration.
- Excellent browser performance.

### 1. NEW CREATIVE DIRECTION

Create an ORIGINAL visual identity called:

**KOREAN ARENA — PLAYFUL HANGEUL TOWN**

Use broad inspiration from the approachable social-game aesthetics of Play Together and the modular, low-poly environment design principles common in Roblox experiences.

IMPORTANT:

Do not copy or recreate existing characters, avatars, copyrighted costumes, user interfaces, textures, animations, maps, or proprietary game assets.

These games are references for accessibility, readability, charm, and modularity — not templates to reproduce.

The result must have its own recognizable Korean Arena identity.

### 2. PRESERVE THE EXISTING PROJECT

Read all existing repository instructions, progress files, asset manifests, and v0.5 source code.

The existing v0.5 implementation already includes:

- A functional four-sided Hanok.
- A rigged character named Nari.
- Character locomotion.
- Facial expressions.
- Keyboard/touch controls.
- A camera system.
- Environmental interactions.
- Lighting modes.
- A working GitHub Pages showcase.

Do not discard these systems without justification.

Preserve the approved v0.5 assets, source files, and Git history.

Create a new recoverable v0.6 development checkpoint.

The public v0.5 showcase must remain available until the user approves the new design.

### 3. VISUAL DESIGN PRINCIPLES

Target appearance:

- Friendly, playful, polished.
- Rounded shapes.
- Strong silhouettes.
- Bright but harmonious colors.
- Low-poly or simplified geometry.
- Soft shading.
- Clear material separation.
- Minimal visual noise.
- Distinctive Korean architecture.
- Lightweight visual effects.
- Cute proportions.
- Warm social atmosphere.

Suggested palette:

- Celadon mint.
- Warm cream.
- Coral pink.
- Sky blue.
- Honey yellow.
- Soft lavender.
- Deep navy accents.

The world should be cheerful during the day and magical but readable at night.

Avoid photorealism, overly complex PBR materials, heavy shaders, and unnecessary geometry.

Do not make the project look like an unpolished collection of primitive cubes.

Simple geometry must still demonstrate excellent art direction.

### 4. CHARACTER REDESIGN — HIGHEST PRIORITY

Redesign Nari as an original, cute chibi Korean adventure character.

Suggested proportions:

- Approximately 2.5–3 heads tall.
- Relatively large head.
- Expressive face.
- Small but clearly articulated body.
- Short, functional arms and legs.
- Oversized, appealing eyes.
- Recognizable hairstyle.
- Simplified Korean-inspired clothing.
- Distinctive accessory or silhouette.

These are starting guidelines, not rigid requirements.

The new Nari must remain attractive from front, side, and rear views.

Produce three substantially different chibi character concepts:

A. Friendly Korean student explorer.

B. Playful Hangeul adventure messenger.

C. Original fantasy town resident inspired by Korean craft and architecture.

For each direction, show:

- Front view.
- Side view.
- Character silhouette.
- Color palette.
- Facial expression examples.
- Animation feasibility.
- Estimated complexity.

Recommend the strongest direction and STOP for user approval before fully remodeling the protagonist.

### 5. CHARACTER ANIMATION

The chibi style must NOT reduce animation quality.

The character should support:

- Idle breathing.
- Walking.
- Running.
- Jumping.
- Landing.
- Turning.
- Greeting.
- Dancing.
- Celebrating.
- Thinking.
- Surprised reaction.
- Happy reaction.
- Sad reaction.
- Interaction reaction.

Maintain:

- Articulated arms and legs.
- Proper foot contact.
- Recognizable walk/run cycles.
- Clear jump anticipation and landing.
- Smooth animation transitions.
- Expressive facial animation.
- Eye tracking and blinking.
- Cute squash-and-stretch where appropriate.
- Natural secondary motion.

Avoid stiff Roblox-style movement unless deliberately selected for a particular character.

The goal is playful responsiveness, not robotic animation.

Preserve or adapt the existing v0.5 rig, animation controller, and facial morph system where technically useful.

### 6. WORLD REDESIGN

Transform the existing Hanok environment into a compact, colorful Korean social-game neighborhood.

The world should resemble a miniature town where users might eventually learn, explore, meet friends, and play games.

Core environment:

**Hangeul Town Plaza**

Include:

- A cute Korean-inspired house.
- A small town square.
- A central character interaction area.
- Flower beds.
- Rounded trees.
- Lanterns.
- Benches.
- Decorative signs.
- Cozy paths.
- Small gardens.
- A few simple interactive objects.

The Hanok architecture must remain structurally recognizable.

Retain complete walls, properly supported roofs, connected floors, and believable doors/windows.

Simplify the building through strong shapes and stylized materials rather than removing its essential structure.

Use modular assets so future Korean learning districts can reuse doors, roofs, lamps, trees, paths, benches, and architectural pieces.

Do NOT build all future districts in this milestone.

### 7. MAKE THE WORLD FUN

Add lightweight interactive activities suitable for a social-game prototype.

Examples:

- Walk and run around the plaza.
- Jump onto safe platforms.
- Approach an NPC.
- Wave to a character.
- Interact with a lantern.
- Open a house door.
- Sit on a bench.
- Trigger a playful celebration.
- Discover a small hidden object.

Every interaction must have immediate and readable feedback.

Prioritize a few delightful interactions over many incomplete ones.

Do not implement multiplayer, Supabase, learning APIs, or backend gameplay in this standalone 3D Studio.

### 8. GAME FEEL

Improve responsiveness and animation quality.

Required:

- Fast movement response.
- Smooth acceleration and deceleration.
- Reliable jump controls.
- Clear landing feedback.
- Stable character orientation.
- No obvious foot sliding.
- Smooth camera follow.
- Appropriate collision behavior.
- Small, restrained visual effects.

A cute world with responsive movement is more valuable than a complicated environment with sluggish controls.

### 9. LIGHTWEIGHT ASSET STRATEGY

Use Blender and the existing Three.js / React Three Fiber / Drei stack.

Prefer:

- Low-poly geometry.
- Reusable mesh components.
- Instancing.
- Shared materials.
- Texture atlases.
- Efficient animation clips.
- GLB exports.
- Compressed textures where supported.
- Selective shadows.
- Limited postprocessing.
- Simple procedural foliage.
- Minimal expensive transparency.

Do not install unnecessary rendering frameworks.

Use glTF Transform and glTF Validator to inspect and optimize final assets.

Do not assume lower polygon counts automatically guarantee better performance.

### 10. PROVISIONAL PERFORMANCE TARGETS

Measure the current v0.5 baseline first.

Then aim for the following initial goals for the primary hero scene:

- Environment geometry: approximately 40,000 triangles or fewer.
- Main character geometry: approximately 10,000 triangles or fewer.
- Combined optimized character/world GLB transfer size: approximately 4 MB or less where feasible.
- Medium-quality draw calls: preferably below 100, including relevant shadow passes.
- Most textures: 512–1024 pixels or smaller where appropriate.
- Lazy-loaded assets and animation systems.
- Mobile quality mode with reduced geometry/shadows.
- Reduced-motion support.
- Reliable 2D fallback.

These are optimization targets, not absolute constraints.

If exceeding a target delivers a substantial visual benefit, document the tradeoff.

Measure actual CPU/GPU performance when suitable hardware testing is available.

Do not invent FPS results.

### 11. SHOWCASE PRESENTATION

Create a welcoming game-style preview.

The opening view should prioritize:

- Nari.
- A colorful Hanok.
- A small lively town square.
- Clear movement controls.
- A prominent Play/Explore action.
- Immediate visible character motion.

Provide:

- Character concept comparison.
- Day/night preview.
- Low/medium/high quality.
- Camera controls.
- Animation preview.
- Character expression preview.
- Interactive plaza demo.

Avoid an overly technical showcase interface.

Keep development metrics accessible in a secondary panel, but make the main experience feel like a small game.

### 12. ART DIRECTION APPROVAL GATE

This is mandatory.

Before fully replacing the current v0.5 visual assets:

1. Create three new chibi character concepts.
2. Create two town-environment style concepts.
3. Show a color/material board.
4. Estimate implementation complexity.
5. Explain what can be reused from v0.5.
6. Compare likely asset and rendering costs.
7. Recommend one cohesive design direction.

Present the concepts to the user.

**STOP and wait for approval.**

Do not immediately spend resources remodeling the entire game.

### 13. APPROVED PROTOTYPE GATE

After user approval, create a small vertical slice containing:

- One approved chibi character.
- One redesigned Korean house.
- One plaza area.
- Walking.
- Running.
- Jumping.
- Three expressive emotional animations.
- One environmental interaction.
- A working camera.
- Mobile fallback.

This is the first v0.6 prototype.

Do not expand into a complete town yet.

### 14. QUALITY ASSURANCE

Produce real rendered evidence:

- Character front/side/rear.
- Walk sequence.
- Run sequence.
- Jump sequence.
- Three facial expressions.
- Plaza overview.
- Building from four sides.
- Day/night comparison.
- Desktop/mobile.
- Low/medium/high metrics.
- Before/after comparisons with v0.5.

A successful build does not automatically mean the visuals are good.

Assess character appeal, gameplay feel, originality, architectural coherence, and visual clarity.

### 15. SAVE AND RESUME

Maintain:

- STUDIO_TASKS.md
- STUDIO_PROGRESS.md
- STUDIO_DECISIONS.md
- STUDIO_ASSETS.md

After every completed subtask:

- Save source files.
- Save editable Blender assets.
- Save exports.
- Update documentation.
- Run relevant tests.
- Commit recoverable progress.
- Verify GitHub persistence when available.

Never rely only on conversation history.

Preserve v0.5 as a rollback option.

### 16. PUBLIC RELEASE POLICY

Do not overwrite the existing public v0.5 website automatically.

Prepare v0.6 separately.

Request user approval before publishing the redesigned version.

### 17. FINAL GOAL

The finished direction must deliver:

**A colorful, lightweight, expressive, cute Korean social-adventure world with original characters, responsive gameplay, and excellent browser usability.**

Success is not measured by realism or polygon count alone.

Success is measured by how charming, memorable, interactive, responsive, accessible, and efficient the experience feels.

START NOW:

Audit v0.5, register this art-direction pivot, prepare the character and environment concept alternatives, save a checkpoint, and present the concepts for approval.

Do not begin full-scale remodeling before the approval gate.