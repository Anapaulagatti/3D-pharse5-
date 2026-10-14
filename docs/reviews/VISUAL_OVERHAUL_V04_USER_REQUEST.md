# KOREAN ARENA 3D STUDIO — BIG UPDATE MASTER PROMPT
## v0.4 LIVING HANOK SHOWCASE OVERHAUL

### ROLE

You are the Lead 3D Art Director, Senior Technical Animator, Senior React Three Fiber Engineer, and Gameplay Presentation Designer for **Korean Arena 3D Studio**.

You are working directly inside the existing repository.

Your mission is to perform a **major quality upgrade** of the current Hanok Rooftop showcase and mascot, transforming it from a pleasant technical demo into a **visually rich, emotionally expressive, lively miniature game world**.

This is a **big update**, not a small patch.

Do not start new districts yet.

Focus on making the current golden vertical slice dramatically better.

---

## 1. CORE GOAL

The current showcase is aesthetically pleasing but still feels too static, too simple, and not emotionally engaging enough.

The user feedback is:

- The environment is still too sparse.
- The mascot animation is too weak and not obvious enough.
- The mascot must visibly move with **walking, running, jumping, greeting, reacting, celebrating, thinking**, and other lively motions.
- The mascot’s **arms, legs, body, ears, face, and posture** must move in expressive ways.
- The mascot must remain **cute**, charming, and readable.
- Changing the mascot state must also change the **facial expression**, not just the body pose.
- The environment must feel more detailed, more alive, and more immersive.
- The final result should feel like a small but premium indie game world.

Your job is to deliver a **big upgrade** that makes the showcase feel alive and captivating.

---

## 2. PROJECT RULES

You are authorized to work directly in this repository.

You may:
- modify existing source files;
- improve React Three Fiber scenes;
- edit animation logic;
- improve 3D assets;
- update Blender source files;
- export new GLB files;
- improve materials, lighting, camera, and interactions;
- add new polished interactions;
- add new visual polish systems;
- update documentation and progress files;
- commit checkpoints using the authorized workflow.

You must:
- preserve the existing artistic identity;
- preserve recoverability;
- continue using STUDIO_TASKS.md, STUDIO_PROGRESS.md, STUDIO_DECISIONS.md, and STUDIO_ASSETS.md;
- keep the existing Hanok × Celadon × Hanji aesthetic direction;
- maintain reduced-motion accessibility and fallback behavior;
- keep performance realistic for the browser.

You must NOT:
- start Hangul Garden or other future districts;
- replace the entire art direction with something unrelated;
- destroy previous working checkpoints;
- claim success without visually verifying the real rendered output;
- add meaningless complexity that hurts performance.

---

## 3. BIG UPDATE TARGET

Create:

**Korean Arena 3D Studio v0.4 — Living Hanok Showcase**

This version must feel:
- more alive;
- more expressive;
- more detailed;
- more premium;
- more emotionally engaging;
- more game-like;
- more memorable.

The viewer should immediately feel:
- “this world is alive”;
- “this mascot has personality”;
- “I want to click around and explore”;
- “this could become a real Korean learning game”.

---

## 4. MASCOT UPGRADE — TOP PRIORITY

The mascot is the emotional heart of the experience.

The current mascot is cute, but it needs a major upgrade in **movement clarity, expression, and personality**.

### Required mascot improvements

#### 4.1 Character performance quality
Upgrade the mascot into a highly expressive, readable animated character.

It must support:
- clearer body language;
- more readable silhouettes;
- stronger posing;
- more visible motion arcs;
- better anticipation and follow-through;
- more obvious action timing;
- stronger idle life;
- more personality.

#### 4.2 Facial expression system
When the mascot state changes, its face must change too.

Implement an expressive face system that supports:
- eye shape changes;
- blink behavior;
- eye direction / eye attention;
- eyebrow-like expression if stylistically suitable;
- mouth shape changes;
- cheek expression changes if appropriate;
- happy / excited / thoughtful / sad / greeting / celebratory expression changes.

Expressions must be clearly different across states.

#### 4.3 Full-body motion language
The mascot’s movement must not be limited to a subtle bounce.

Its body must visibly support:
- arm movement;
- leg movement;
- ear movement;
- torso lean;
- head tilt;
- body squash and stretch where appropriate;
- small secondary motion;
- springy return to idle.

Keep it cute, polished, and tasteful.

#### 4.4 New animation set
Implement or improve a complete readable animation set.

Required animations:

- Idle
- Walk
- Run
- Hop / Jump
- Greeting
- Happy
- Thinking
- Celebration
- Disappointed / Sad
- Curious Look
- Click / Interaction Reaction
- Return to Idle

Each animation must be visibly distinct.

The user must be able to tell the difference clearly from normal viewing distance.

#### 4.5 Behavioral animation logic
The mascot should behave like a tiny character with awareness.

Examples:
- Idle breathing and subtle movement by default.
- Looks toward the viewer or camera from time to time.
- Waves when selected or greeted.
- Small hop when clicked.
- Celebration when triggered.
- Thinking pose when that mode is selected.
- Sad / disappointed reaction when selected.
- Smooth transition back to idle.

Do not let the mascot feel mechanically looped or lifeless.

---

## 5. ANIMATION QUALITY RULES

Animation quality matters more than animation count.

Use real principles of animation:
- anticipation;
- squash and stretch;
- follow-through;
- overlapping action;
- arcs;
- staging;
- timing;
- ease in/out;
- appeal.

Do not create stiff robotic motion.

Avoid tiny almost-invisible movement.

Every important state must read clearly in under 2 seconds.

The motion must be **cute, readable, and premium**.

---

## 6. ENVIRONMENT BIG UPGRADE

The Hanok Rooftop Arena currently works, but it still feels too simple.

Add more carefully art-directed detail while preserving performance.

### 6.1 Hanok architecture
Improve:
- roof edge ornamentation;
- roof tile richness;
- decorative ridge details;
- timber beams and joints;
- lattice windows;
- wooden trim variation;
- subtle Korean architectural patterns;
- better entrance framing;
- more handcrafted feeling.

### 6.2 Courtyard detail
Improve:
- stone tiling variation;
- cleaner but richer floor composition;
- better platform details;
- small ceramic vessels;
- ornamental props;
- miniature railings;
- better steps and bridge details;
- decorative edge treatments;
- more interesting pedestal design for mascot display.

### 6.3 Garden and props
Improve:
- plum tree complexity and shape;
- blossom density and variation;
- better plant clusters;
- small ground foliage;
- paper ornaments or ribbons if suitable;
- decorative lantern placement;
- storytelling props that make the scene feel inhabited.

### 6.4 Background and depth
Improve:
- skyline composition;
- silhouette layering;
- depth cues;
- atmosphere;
- subtle haze if appropriate;
- stronger composition behind the hero scene.

Do not add noise for the sake of noise.

Only add detail that contributes to visual richness and storytelling.

---

## 7. MAKE THE WORLD FEEL ALIVE

The whole scene must feel alive even before the user clicks anything.

Implement subtle ambient motion such as:
- lantern sway;
- lantern light flicker;
- foliage sway;
- drifting petals or hanji fragments;
- tiny ambient particles;
- soft environmental movement;
- subtle light response;
- occasional mascot ambient behavior.

These must be controlled and elegant.

Avoid clutter, chaos, or overuse of particles.

---

## 8. LIGHTING AND MOOD UPGRADE

Lighting must become a major strength of the scene.

Create three clearly beautiful moods:

### Day
- soft and welcoming;
- readable forms;
- clean light;
- visible detail;
- attractive celadon material response.

### Evening
- warm golden atmosphere;
- cinematic but gentle;
- rich warm/cool contrast;
- beautiful highlights.

### Night
- magical but still readable;
- strong lantern focal points;
- environment should not disappear into darkness;
- warm pools of light;
- better subject separation;
- premium atmosphere.

The scene must feel intentionally lit, not merely illuminated.

Do not rely on heavy bloom.

---

## 9. MATERIALS AND SURFACES

Upgrade material quality across the scene.

Improve:
- celadon ceramic shading;
- wood warmth and variation;
- roof tile richness;
- stone material readability;
- hanji paper quality;
- lantern material glow;
- subtle surface differentiation.

Materials should feel stylized but believable.

---

## 10. CAMERA AND PRESENTATION UPGRADE

The current presentation feels too much like a viewer and not enough like a game showcase.

Improve camera composition:

- stronger hero angle;
- better default framing;
- scene occupies more meaningful visual space;
- important details are more visible;
- less dead empty space;
- better close-up mode for the mascot;
- smoother camera transitions;
- clearer focus presets;
- elegant orbit experience.

Optional:
- a gentle showcase camera mode;
- a brief cinematic intro framing;
- a polished “hero framing reset”.

Do not make camera movement too aggressive.

---

## 11. INTERACTIVITY UPGRADE

Add meaningful polished interactions.

Examples:
- click mascot → greeting / hop / expression change;
- switch state → body + face both change;
- click lantern → subtle glow pulse;
- click garden area → drifting petals;
- choose “run” or “walk” demo state for mascot;
- choose “emotion” presets and see visible facial differences.

Every interaction must produce a clearly visible response.

---

## 12. UI/SHOWCASE IMPROVEMENT

The page itself is elegant, but the experience can be more engaging.

Improve the showcase UI where appropriate:

- make state selection clearer;
- expose the most visually interesting actions;
- make it easier to test animations;
- make it easier to compare expressions;
- make interaction affordances clearer;
- highlight the mascot as the star.

Do not bloat the interface.

The page should still feel clean and premium.

---

## 13. ACCESSIBILITY AND REDUCED MOTION

Reduced-motion support must remain.

Rules:
- when reduced motion is ON, large or constant motion should be minimized;
- the scene must still look beautiful in reduced-motion mode;
- when reduced motion is OFF, animations must be clearly visible and expressive;
- never silently break accessibility support.

Respect browser and system behavior.

---

## 14. PERFORMANCE REQUIREMENTS

Do not destroy performance.

Maintain a reasonable browser budget.

Optimize:
- geometry reuse;
- draw calls;
- material reuse;
- texture sizes;
- animation update efficiency;
- light/shadow costs;
- mobile rendering;
- fallback behavior.

Add detail intelligently, not recklessly.

Prefer high visible value per performance cost.

---

## 15. VISUAL VERIFICATION IS MANDATORY

Do not stop at code changes.

You must visually inspect the rendered result and verify that the upgrade is actually visible.

Required verification outputs:

1. Day scene screenshot
2. Evening scene screenshot
3. Night scene screenshot
4. Mascot close-up screenshot
5. Full arena hero screenshot
6. Screenshot showing a visibly different expression state
7. Screenshot showing a visibly different action state
8. Mobile viewport screenshot
9. If tooling allows, short animation capture or visual evidence of motion

You must confirm:
- mascot movement is clearly readable;
- different states visibly look different;
- facial expression changes are obvious;
- walking/running/jumping are visibly distinct;
- environment detail is noticeably richer;
- lighting is improved;
- scene feels more alive;
- no critical rendering issues are introduced.

---

## 16. CHECKPOINT SYSTEM

Continue using the persistent progress system.

You must maintain and update:
- STUDIO_TASKS.md
- STUDIO_PROGRESS.md
- STUDIO_DECISIONS.md
- STUDIO_ASSETS.md

After every meaningful subtask:
- save source files;
- save generated assets;
- preserve Blender files;
- run checks;
- create a recoverable Git checkpoint;
- document the next step.

If the session ends unexpectedly, the next session must resume from the latest verified checkpoint.

---

## 17. EXECUTION PLAN

Work in this order:

### Phase A — Audit and planning
- inspect the current v0.2/v0.3 state;
- identify weak points in mascot animation, environment detail, lighting, and presentation;
- convert this big update into a concrete checklist.

### Phase B — Mascot overhaul
- improve rig / animation readability;
- implement clearer body motion;
- implement expression system;
- add walk / run / jump and stronger state differences.

### Phase C — Environment detail pass
- enrich hanok, courtyard, props, plants, and skyline.

### Phase D — Ambient life pass
- lantern motion, foliage motion, particles, environmental liveliness.

### Phase E — Lighting and material polish
- improve day/evening/night;
- improve celadon, wood, stone, hanji.

### Phase F — Camera and interaction polish
- better framing, interaction reactions, smoother transitions.

### Phase G — QA and visual review
- verify performance;
- verify reduced motion;
- verify fallback;
- verify visuals;
- prepare screenshots and evidence;
- checkpoint everything.

Do not skip directly to deployment.

---

## 18. DEFINITION OF DONE

This big update is complete only when:

- the mascot has clearly expressive full-body animation;
- walking, running, jumping, and reaction animations are obvious;
- facial expressions visibly change with state;
- the mascot remains cute and appealing;
- the hanok environment is noticeably richer and more detailed;
- the scene feels alive through ambient motion;
- lighting is more beautiful and readable;
- the presentation is more captivating;
- the result feels like a polished miniature game world rather than a simple technical demo;
- visual verification evidence is saved;
- progress files and checkpoints are updated.

---

## 19. STOP CONDITION

Do NOT start Hangul Garden or other districts.

Complete this **Big Update v0.4** first.

When the upgraded showcase is ready, STOP and present:
- what changed;
- which files changed;
- which animations were improved or added;
- what environment details were upgraded;
- what screenshots/evidence were created;
- what still remains for future work.