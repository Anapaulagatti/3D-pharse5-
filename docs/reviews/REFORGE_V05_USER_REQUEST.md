# KOREAN ARENA 3D STUDIO — V0.5 REFORGE MASTER PROMPT
## Structural Architecture Rebuild + Next-Generation Playable Character

### ROLE AND MISSION

You are the Principal 3D Character Artist, Character Animator, Environment Artist, Technical Director, and Senior React Three Fiber Engineer.

You are authorized to work within the existing Korean Arena 3D Studio GitHub repository.

This is not another decorative polish pass.

**The user has rejected the current level of architectural completeness, character design, animation readability, and visual engagement.**

Your mission is to rebuild the weakest foundations and create a genuinely compelling, playable 3D adventure prototype.

Target release:

**Korean Arena 3D Studio v0.5 — Joseon Fantasy Reforge**

Do not begin the next learning districts.

---

## 1. READ THE EXISTING PROJECT FIRST

Inspect:

- STUDIO_MASTER_PROMPT.md
- STUDIO_PROGRESS.md
- STUDIO_TASKS.md
- STUDIO_DECISIONS.md
- STUDIO_ASSETS.md
- ART_DIRECTION.md
- CAMERA_LANGUAGE.md
- COLOR_MATERIAL_SYSTEM.md
- PERFORMANCE_REPORT.md
- Studio/modeling/arena.py
- Studio/modeling/mascot.py
- All newer v0.3/v0.4 modeling and rigging scripts
- Current React Three Fiber scene implementation

Inspect the latest Git status, remote checkpoint, current publication status and existing assets.

Do not interrupt an active deployment.

Create a recoverable v0.4 checkpoint before starting the v0.5 redesign.

Develop v0.5 separately from the approved public release until the user authorizes publication.

---

## 2. NEW ART DIRECTION

The project must evolve into:

**JOSEON FANTASY ADVENTURE**

Combine:

- Recognizable Korean historical architecture.
- Charming Korean fantasy storytelling.
- Premium stylized 3D character design.
- Expressive, physically convincing animation.
- Rich environmental storytelling.
- Handcrafted materials.
- Modern indie game interaction quality.

Study high-level animation, silhouette, camera and interaction principles found in successful modern adventure games.

Possible design references:

- Genshin Impact — readable stylized character movement.
- Kena: Bridge of Spirits — expressive character animation and environments.
- The Legend of Zelda — environmental exploration and interaction.
- Animal Crossing — charm and emotional accessibility.
- Modern stylized action-adventure games — locomotion transitions and responsive controls.

These are quality references, NOT designs to copy.

Do not reproduce recognizable copyrighted characters, costumes, animation clips, environments, logos or distinctive visual assets.

Create an original Korean Arena identity.

---

## 3. REPLACE THE MAIN CHARACTER DESIGN

The current Ceramic Seed Spirit is no longer required to remain the main character.

Preserve it as an optional legacy companion asset.

Design a NEW MAIN PLAYABLE CHARACTER.

Preferred concept:

**A young fictional Joseon-era scholar, palace messenger, or Hangeul guardian.**

The character should be:

- Cute but not overly childish.
- Memorable and instantly recognizable.
- Fully capable of expressive movement.
- Designed for walking, running and jumping.
- Clearly articulated.
- Emotionally expressive.
- Culturally grounded.
- Suitable for a Korean learning adventure.

Create THREE genuinely distinct character concepts.

Evaluate:

1. Silhouette readability.
2. Originality.
3. Facial appeal.
4. Korean cultural identity.
5. Animation feasibility.
6. Costume complexity.
7. Web rendering cost.
8. Potential as a long-term game protagonist.

Present the three concepts for user approval before committing to the final character design.

If the user chooses a real Korean historical figure, ensure the depiction is original, respectful and historically informed. Do not copy modern portrayals.

---

## 4. CHARACTER MODELING REQUIREMENTS

Build an actual articulated humanoid 3D character.

Required body structure:

- Head.
- Neck.
- Torso.
- Shoulders.
- Upper arms.
- Forearms.
- Hands.
- Pelvis.
- Thighs.
- Lower legs.
- Feet.
- Facial controls.
- Costume attachments.

The exact topology and bone hierarchy must support real character animation.

Do not create disconnected decorative limbs that cannot perform convincing movement.

Use Blender with an appropriate armature and skinning workflow.

Required:

- Proper skeleton.
- Correct skin weights.
- Functional shoulder, elbow, hip, knee and ankle joints.
- Clean joint deformation.
- No obvious mesh separation.
- No broken animation when viewed from the side or rear.
- Secondary motion for suitable clothing or accessories.
- Editable Blender source.
- Exportable GLB with named animation clips.

Use IK or appropriate animation tools during authoring when beneficial.

A complex professional rig is preferable only when it creates visibly better movement. Do not add unnecessary bones.

---

## 5. FACIAL RIG AND EXPRESSIONS

Build an expressive face system.

The character must visibly display:

- Neutral.
- Happy.
- Excited.
- Curious.
- Thinking.
- Confused.
- Sad.
- Surprised.
- Determined.
- Celebrating.

Implement appropriate controls using:

- Shape keys / morph targets.
- Facial bones.
- Eyelid controls.
- Eyebrow controls.
- Mouth shapes.
- Eye direction.
- Blinking.

Expressions must be different enough to recognize without reading the selected animation label.

Facial animation must coordinate with body animation.

Examples:

Happy:
- smiling eyes;
- raised cheeks;
- joyful mouth;
- energetic body posture.

Thinking:
- focused eyes;
- slightly tilted head;
- appropriate brow and mouth expression;
- thoughtful hand gesture.

Sad:
- lowered gaze;
- changed eyebrow shape;
- visibly disappointed mouth;
- reduced body energy.

Celebration:
- bright expression;
- active arm motion;
- energetic body movement.

Do not reuse one static face for every action.

---

## 6. PROFESSIONAL CHARACTER ANIMATION

Create a complete locomotion and expression system.

### Essential locomotion

- Idle
- Walk
- Run
- WalkStart
- WalkStop
- RunStart
- RunStop
- JumpStart
- JumpAir
- JumpLand
- TurnLeft
- TurnRight

### Emotional actions

- Greeting
- Happy
- Thinking
- Sad
- Celebration
- Surprised
- Curious
- InteractionReaction

### Quality expectations

Walking must demonstrate:
- alternating leg movement;
- actual foot placement;
- clear arm swing;
- body weight shift;
- readable gait.

Running must demonstrate:
- a clearly faster gait;
- longer stride;
- stronger arm swing;
- body lean;
- believable acceleration and stopping.

Jumping must demonstrate:
- anticipation crouch;
- takeoff;
- airborne pose;
- landing;
- recovery.

Avoid foot sliding, moonwalking, mesh intersections and floating feet.

Animation transitions should be smooth and responsive.

Use appropriate crossfades, animation states, transitions and root-motion or in-place movement handling.

Do not count slight rotation or vertical bobbing as walking or running.

**All important movements must remain recognizable when viewed at normal gameplay camera distance.**

---

## 7. INTERACTIVE CHARACTER CONTROLLER

Create a small standalone playable prototype within the Studio preview.

Required:

- Keyboard movement on desktop.
- WASD or arrow keys.
- Shift to run.
- Space to jump.
- Camera following or controlled orbit.
- Responsive direction changes.
- Character orientation aligned with movement.
- Ground contact.
- Basic collision with architectural structures.
- Mobile-friendly touch controls or an equivalent accessible alternative.

Keep the movement system lightweight.

The goal is a polished playable character vertical slice, not an open-world engine.

Expose animation and facial-expression controls in a dedicated review panel.

---

## 8. HANOK STRUCTURAL REBUILD — NON-NEGOTIABLE

The current architecture reads as a roof and pavilion rather than a complete building.

Rebuild the main structure as a believable four-sided Korean Hanok.

Use reliable Korean architecture references such as:

https://hanok.seoul.go.kr/front/eng/info/infoHanok.do?tab=2

### Required structure

- Proper stone foundation.
- Correctly grounded timber columns.
- Structural crossbeams.
- Purlins and rafters.
- Visible roof-support connections.
- Complete roof surfaces.
- Roof underside and eave construction.
- Real front facade.
- Real rear facade.
- Real left-side wall.
- Real right-side wall.
- Proper doors.
- Traditional lattice windows.
- Connected floors.
- Stairs and thresholds.
- Coherent openings.
- Solid roof-to-building construction.

The building may feature an open veranda or daecheong area where historically appropriate, but it must not appear unfinished or structurally unsupported.

### Architectural integrity rules

- No floating roof components.
- No unexplained gaps between roof and columns.
- No disconnected beams.
- No unsupported wall sections.
- No roof clipping through architecture.
- No fake one-sided facade.
- No missing back wall disguised by camera framing.
- No missing sides disguised by lighting.

The full exterior must withstand a 360-degree camera inspection.

Create a simplified furnished interior visible through a door or windows where feasible.

Maintain stylized visual appeal without sacrificing believable structure.

---

## 9. DETAIL AND MATERIAL REBUILD

Increase visible environment detail substantially.

Prioritize geometry, textures and composition over unnecessary decoration.

### Architecture

- Detailed roof tiles.
- Layered eaves.
- Timber joinery.
- Window lattice.
- Sliding door panels.
- Roof ornaments.
- Decorative brackets.
- Door handles.
- Threshold construction.
- Weathered but refined wood variation.

### Environment

- Garden planting.
- More convincing plum blossoms.
- Rocks and stone paving.
- Ceramic vessels.
- Small furniture.
- Lantern structures.
- Floor height transitions.
- Garden walls or railings.
- Small environmental storytelling objects.

### Materials

Use a stylized physically based material workflow.

Improve:

- Wood grain and roughness.
- Roof tile surface response.
- Hanji translucency where feasible.
- Ceramic glazing.
- Stone texture variation.
- Metal accents.
- Fabric appearance.

Do not rely only on flat solid colors.

Use efficient procedural or appropriately licensed texture sources.

---

## 10. GAME-QUALITY WORLD ANIMATION

Create environmental life that is visible but coherent.

Required systems:

- Wind-reactive foliage.
- Falling flower petals.
- Swaying lanterns.
- Gentle fabric or banner motion.
- Warm light flicker.
- Water ripples where relevant.
- Interactive doors.
- Dynamic character shadow.
- Ground contact shadows.
- Subtle ambient particles.

Each effect must serve atmosphere, readability or interaction.

Do not use excessive particle density or uncontrolled postprocessing.

---

## 11. GAME FEEL AND VISUAL EFFECTS

Add a small, polished feedback system.

Examples:

Movement:
- landing dust;
- footstep effects;
- subtle body follow-through.

Interaction:
- click response;
- small highlight;
- object reaction;
- short character gesture.

Celebration:
- strong silhouette;
- expressive pose;
- carefully timed particles;
- optional camera reaction.

Jumping:
- anticipation;
- airborne movement;
- landing response.

Use animation principles:

- Anticipation.
- Squash and stretch where stylistically suitable.
- Follow-through.
- Overlapping action.
- Arcs.
- Clear staging.
- Timing.
- Secondary motion.

Visual effects must reinforce animation rather than conceal weak animation.

Provide controls to disable or reduce effects.

---

## 12. PRESENTATION AND CAMERA

Create a more immersive showcase.

Required modes:

1. Full environment hero view.
2. Third-person character gameplay.
3. Mascot/hero close-up.
4. Architecture inspection.
5. Animation review.
6. Day/evening/night lighting.

The default view should show an attractive, complete environment composition.

Camera behavior should:

- smoothly follow the character;
- avoid clipping through roofs or walls where feasible;
- frame full-body motion;
- provide a clear sense of scale;
- respect input controls;
- reduce motion when requested.

Avoid aggressive camera shake or constantly moving cinematic cameras.

---

## 13. QUALITY AND PERFORMANCE

Maintain browser suitability.

Use:

- Optimized GLB exports.
- Texture compression where supported.
- LOD or selective detail reduction where beneficial.
- Reusable materials.
- Geometry instancing.
- Animation optimization.
- Bounded particle systems.
- Lightweight shadow configurations.
- Low/medium/high quality profiles.

Set provisional budgets, measure them, and refine based on observed performance.

Aim for smooth interaction on ordinary desktop hardware and a usable reduced-quality mode on mobile.

Do not claim stable 30 or 60 FPS without actual target-device measurements.

Do not sacrifice readability or accessibility for visual effects.

---

## 14. MANDATORY VISUAL PROOF

A passing build is not proof of game-quality visuals.

Save actual rendered screenshots or videos proving:

### Architecture

- Front view.
- Rear view.
- Left view.
- Right view.
- Roof perspective.
- Roof-to-column connections.
- Interior view where available.

### Character

- Front view.
- Side view.
- Rear view.
- Walk sequence.
- Run sequence.
- Jump sequence.
- Different facial expressions.
- Celebration sequence.
- Interaction reaction.

### Environment

- Daylight.
- Evening.
- Night.
- Ambient animation.
- Mobile view.
- Reduced-motion view.

Create before/after comparison with the earlier version.

When possible, provide a short real-time gameplay video that includes:

- 5 seconds of walking;
- 5 seconds of running;
- jumping and landing;
- greeting;
- facial expression changes;
- entering or walking around the Hanok environment.

Do not replace actual rendered evidence with concept images.

---

## 15. DEVELOPMENT GATES

### Gate A — Character concept approval

Deliver three original character concepts with descriptions and a recommended direction.

Stop for the user's concept approval before committing to an expensive final character build.

### Gate B — Architecture graybox

Build the full four-sided Hanok structure.

Demonstrate a 360-degree inspection with no floating roof.

Validate basic scale and spatial coherence before detailed materials.

### Gate C — Playable character

Complete:
- model;
- rig;
- walking;
- running;
- jumping;
- facial expressions;
- real-time controller.

Verify that motion is readable.

### Gate D — Art polish

Complete:
- detailed architecture;
- environment dressing;
- improved materials;
- lighting;
- environmental animation;
- gameplay visual effects.

### Gate E — Production verification

Validate:
- GLB structure;
- animation clips;
- browser rendering;
- performance;
- accessibility;
- mobile fallback;
- production build.

Preserve a stable checkpoint after every completed gate.

---

## 16. CHECKPOINTS AND CREDIT RECOVERY

Maintain:

- STUDIO_TASKS.md
- STUDIO_PROGRESS.md
- STUDIO_DECISIONS.md
- STUDIO_ASSETS.md

After every meaningful completed task:

1. Save source files.
2. Save Blender files.
3. Save GLB exports.
4. Save review evidence.
5. Update progress.
6. Run appropriate verification.
7. Commit through the authorized GitHub workflow.
8. Verify remote persistence when available.

Never depend on chat history alone.

At session start, resume the latest unfinished verified task.

Do not repeatedly regenerate approved artwork.

---

## 17. RELEASE AND STOP CONDITIONS

Do not replace the existing public v0.3/v0.4 release until the user has reviewed and approved the new candidate.

Prepare v0.5 as a separate recoverable version.

Do not begin Hangul Garden, Vocabulary Café, Grammar Library, or other districts.

This milestone is complete only when:

- the new character is visibly superior to the previous mascot;
- the character can walk, run and jump convincingly;
- facial expressions are genuinely distinct;
- a playable character controller works;
- the Hanok is architecturally complete;
- the structure is convincing from all four sides;
- the roof no longer appears disconnected;
- materials and environmental detail are significantly improved;
- gameplay interactions and effects feel responsive;
- actual rendered evidence supports these claims;
- source assets remain editable;
- tests and export validation pass;
- work is saved remotely.

**Priority order: Architecture integrity → Character design → Playable animation → Game feel → Visual polish → Performance.**

Start by auditing the repository and preparing the character concept and architectural rebuild plan.

Do not claim the project is complete based on file generation or automated tests alone.