# CODEX MASTER PROMPT — KOREAN ARENA 3D STUDIO (100% STANDALONE)

> Copy ALL text in the fenced prompt into Codex **when the currently opened folder is `korean-arena-3d-studio`**, not the real Korean Arena application folder.
>
> This is not the Claude Phase 5 prompt, not a patch for Korean Arena, and not a request for Codex to integrate into the real app. Codex is producing an independently testable visual art product plus portable exports.

```text
YOU ARE THE FULL 3D ART TEAM FOR KOREAN ARENA — STANDALONE STUDIO ONLY.

ROLE
Act as an exceptionally strong game art director, visual world builder, Blender procedural artist, 3D modeler, material artist, animation/rigging specialist, React Three Fiber engineer, web performance specialist, and QA reviewer.

Your task is to CREATE a distinctive, high-quality, cohesive ORIGINAL 3D art library and a standalone preview application for a Vietnamese-first Korean-learning game called Korean Arena.

The current Korean Arena application is at an EARLIER DEVELOPMENT PHASE. It is being written by a different AI and is NOT YOUR WORKSPACE.

ABSOLUTE FOLDER ISOLATION
- Work ONLY inside the folder opened for this task: korean-arena-3d-studio/.
- Do NOT open, search, inspect, modify, import, run, migrate or install into the production Korean Arena repository.
- Do NOT ask for the production repository, current Claude files, real user data or application API credentials.
- Do NOT create branches/worktrees of the production repository.
- Do NOT modify an existing production app or ask the other AI to change its code.
- Do NOT make the Studio preview dependent on any backend, Supabase, Cloudflare Worker, TOPIK exam engine, auth, game rating, payment or learning state.
- Use fictional/demo data ONLY within this Studio, clearly labeled DEMO.
- Export portable optimized GLB, poster images, technical notes, manifest and optional visual-only React source when finished.
- The owner will decide if and when to integrate those outputs. No integration is part of your job.

READ FIRST
1. README.md
2. REPOS_AND_INSTALL.md
3. ART_DIRECTION.md
4. EXPORT_CONTRACT.md
5. ASSET_MANIFEST.csv

If files are absent, create equivalent documents WITHIN THIS FOLDER; never navigate to the real Korean Arena repo to find them.

PRODUCT VALUES
- Korean Arena is completely free; optional donation QR is handled by the real app, not the Studio.
- Art should make learning inviting, not distract users from exam writing and learning.
- No paid cosmetics, no paid models, no paywalls, no monetization implementation.
- Copyright-aware and original. Do not imitate the exact characters, architecture/compositions, UI, logo, assets or palette of any named existing game.
- Cultural motifs should be treated with attention and care: recognizable Korean hanok/Seoul inspirations, but not inaccurate faux-Hangul text, generic East-Asian mashup or borrowed IP.

====================================================
A. PRE-FLIGHT: ENVIRONMENT AND DEPENDENCY AUDIT
====================================================

1. Confirm exact current workspace path and that it is NOT inside Korean Arena main app.
2. Inspect existing files. Do NOT overwrite a user's existing art or source file.
3. Check Node, pnpm, Git, optional Blender executable, current React/version if any, and which Codex image generation tools/skills are ACTUALLY accessible.
4. Install the minimum stable toolchain in this STUDIO ONLY. Follow REPOS_AND_INSTALL.md.
5. Build a standalone Vite + React + TypeScript preview under preview/ (do not create Next.js or clone a framework repository).
6. Use Three.js, React Three Fiber and Drei. Choose compatible stable versions, not alpha/experimental unless required and documented.
7. Install glTF-Transform CLI only if GLB assets exist. Use gltfjsx only if converting GLB into reusable React components is useful. Install postprocessing only after a measured visual benefit.
8. If Blender is unavailable, favor meaningful procedural geometry in Three.js/Blender scripts. Do not claim you authored .blend, GLB, rigged animations or generated images until files have been truly created.
9. Record dependencies/reasons in DEPENDENCIES.md.

Never use `git clone` of Three.js, R3F, Drei, Blender, glTF-Transform or random sample projects inside Studio. Install official packages instead.

====================================================
B. CREATIVE DIRECTOR: CREATE A UNIQUE WORLD
====================================================

Art title: THE LIVING HANGEUL DISTRICT.

Art vocabulary: Hanji Origami × Celadon Ceramic × Miniature Seoul × Gentle Magic.

Narrative:
- Korean letters are symbolic building blocks that gradually assemble a warm, lived-in miniature neighborhood.
- Distinct places represent learning activities, not just decorative random buildings.
- The world feels handcrafted: tactile paper surfaces, celadon ceramic highlights, warm lantern glow, tiny precise wooden details and layered urban silhouettes.
- Strong silhouettes and coherent materials matter more than particle counts and polygons.

Reference ART_DIRECTION.md, but interpret it creatively. Generate 3 genuinely different art compositions for the same world before locking a direction. Document why you chose the final approach using a decision matrix:
1. originality / recognizability;
2. mobile readability;
3. Korean visual identity accuracy;
4. performance and polygon budget;
5. technical editability;
6. asset-reuse potential.

Suggested palette (non-binding because production brand may differ):
- Ink Navy #15243A
- Hanji Cream #F5EFE1
- Celadon Jade #72BEAC
- Terracotta Coral #E57B69
- Oxidized Brass #CFAC67
- Sky Haze #AFC7E0

Design system artifacts to create:
- ART_BIBLE.md with full aesthetic rationale, rules and do-not-do list;
- COLOR_MATERIAL_SYSTEM.md with values, material recipes and lighting;
- CAMERA_LANGUAGE.md for desktop, tablet and mobile compositions;
- 3 concept visuals/screenshots generated with the available image-generation tool OR original procedural scene captures, clearly labeled;
- selected final design direction.

If Codex image generation tool is available, USE it for legitimate image outputs: original moodboards, hand-crafted texture references, mascot expression sheets, poster backgrounds and transparent 2D fallbacks. Use the official image generation skill guidance and actually save the generated files. If unavailable, create original visuals with code/Blender and state the limitation. Never fake output by adding a filename only.

Image generation is NOT a 3D modeling engine. A generated image that looks three-dimensional does NOT satisfy GLB/mesh/rig deliverables.

====================================================
C. MASCOT: OUR ORIGINAL JAW-DROPPING CHARACTER
====================================================

Design exactly THREE distinctive directions, not generic animal mascots:
1. Celadon syllable spirit: offset ceramic body, gently floating round tile shoulders, glowing throat core.
2. Hanji seed courier: folded paper-shell figure, clever origami anatomy, warm interior ink glow.
3. Lantern-ink familiar: translucent lantern body, asymmetric bell silhouette, expressive eyes built from few shapes.

For each, demonstrate:
- readable 48-pixel silhouette;
- expressions/face variations;
- 3/4 full-body view;
- low-poly construction feasibility;
- rig or procedural animation strategy;
- compatibility with the final environment's materials.

Choose ONE standout mascot by scoring the above. Save the selection rationale. Build it in REAL 3D as Blender mesh/rig/animations with `.blend` + `.glb` exports if Blender is available, or as reproducible procedural Three.js geometry plus exported GLB where feasible.

Animation states:
- IdleBreathing (understated)
- ReadyFocus
- Cheer
- GentleLoss (encouraging, never humiliating)
- LevelUpPulse

Avoid copyright-fringing mascot traits. No copying Duolingo's owl, Pokémon outlines, existing brand mascots or prior Korean-learning-game characters.

QUALITY BAR:
The mascot should be iconic when isolated on an ivory background, recognizable from 48px, and charming through form/gesture rather than detail density.

====================================================
D. HERO SCENE: HANOK ROOFTOP ARENA
====================================================

Build a genuine 3D scene that runs interactively in the Studio preview:
- miniature Korean-inspired hanok rooftop courtyard above layered Seoul skyline;
- original central dueling dais composed of playful orthogonal syllable blocks;
- modular tiled eaves and wooden structural framing;
- glazeware celadon accents, a few hanji lanterns, two-to-three sculpted plant props, crafted steps;
- one finished mascot, convincingly lit;
- a readable scene composition at desktop wide and mobile portrait sizes;
- subtle idle animation and gentle pointer/touch parallax with bounded camera;
- quality modes high/medium/low; static poster fallback.

Deliver 3 distinct lighting studies:
1. golden blue-hour sunset;
2. cool moonlit studio elegance;
3. late-afternoon cozy light.

Choose one final hero lighting preset; the others may remain as preview toggles only if efficient.

NO heavy glow soup, generic cyberpunk neon alley, excessive sparkles, bloom washing out color, photoreal skyscraper dump or 200 MB textures.

No HTML text, mock CTA or exam controls baked into scene textures. Leave negative space for a FUTURE DOM overlay if integration happens later.

====================================================
E. MASTERY WORLD: LIVING LEARNING ALLEY
====================================================

Create an attractive mini-world with 6 architectural nodes:
- Hangul Atelier: jamo-inspired pottery/wood construction studio;
- Vocabulary Café: warm, collectible café, mugs and subtle tea/coffee motif;
- Listening Metro: tiny subway portal with soundwave lamp motif;
- Grammar Library: folded hanji books and carved shelves;
- TOPIK Pavilion: calm and focused ceremonial test hall (no exam data);
- EPS Workshop: practical work-study classroom with clear equipment motifs.

Build transitions between:
- LOCKED: dim, incomplete architecture;
- AVAILABLE: softly lit and reachable;
- COMPLETE: hand-crafted finish, warm lantern accent.

These states use MOCK DEMO fixtures, not real learning metrics. Store state in the preview or local typed fixtures only.

Preview controls should allow switching any node's state to demonstrate behavior. Later Korean Arena can map its own mastery model to this exported visual system.

====================================================
F. MICRO-ANIMATIONS AND CELEBRATION
====================================================

Build restrained premium motion:
- scene idle
- mascot ready/focus
- win animation with ceramic light pulses + controlled paper lantern particles
- losing response that feels kind and motivating
- level-up alignment/pulse (1–2 seconds)
- environment day/night shift if low cost

Reduced motion MUST disable nonessential movement and replace animated rewards with calm static state.

No screen flashes, forced camera spins, loud sound, animation that blocks action or background effects requiring another installed physics engine.

Audio is optional; do not import copyright music or SoundCloud/YouTube audio.

====================================================
G. REAL 3D ASSET PRODUCTION PIPELINE
====================================================

PREFERRED:
Concept → procedural modeling/Blender → mesh/UV/material/rig → GLB export → validator → glTF Transform optimization → preview testing → fallback screenshot → manifest.

For every actual 3D asset:
- preserve editable source (.blend or script);
- export .glb with explicit units, Y up, known origin and stable mesh names;
- validate exported model and inspect polygons/materials/textures;
- optimize meshes/textures only after preserving animation and visual parity;
- avoid enormous material counts/draw calls;
- store checksum, license, version and optimized size in manifest.

Use glTF Transform `inspect` and `optimize` for real GLBs. Before compression, evaluate decoder dependencies and check optimized GLBs still animate correctly.

If image-generation can create a beautiful *rendered mascot* but not a mesh, treat it as concept/fallback art ONLY. The technical portion must remain real geometry.

Create ASSET_MANIFEST.csv and export machine-readable asset-manifest.json with truthful files. Do not list uncreated files as produced assets.

====================================================
H. STANDALONE INTERACTIVE PREVIEW
====================================================

Build a complete standalone Vite/React/TypeScript preview under `preview/`:
- scene selector: Hero / Mascot / Mastery Map / Celebration / Asset Gallery;
- camera orbit limited and reset button;
- controls: quality Low/Med/High, lighting preset, reduced motion, mobile/desktop framing;
- toggle mascot animation state and mastery-node status;
- loading UI, asset failures and WebGL-unavailable fallbacks;
- typography for demo controls in Vietnamese;
- smooth but restrained motion;
- asset gallery with names, file sizes/versions and license links where available;
- meaningful first render even when asset loading fails.

All controls are DEMO ONLY. There is no user progress, real exam, PvP score, auth, QR, billing or data persistence.

Use semantic HTML over the canvas for accessible labels and controls. Korean glyphs must be real correct text, not hallucinated AI-generated signage. Do not depend on copyrighted fonts.

====================================================
I. PERFORMANCE / ACCESSIBILITY BUDGETS
====================================================

Aim for the following provisional budgets and MEASURE them:
- Hero optimized GLB <= 4 MB if possible;
- Mascot optimized GLB <= 1 MB if possible;
- small props lean, efficient reuse/instancing;
- mobile textures mostly <= 1024px; do not include 4K unless justified;
- idle scene targets 50–60 FPS on a representative desktop, >=30 FPS on a mid-range phone if tested;
- low mode disables costly postprocessing, shadows/resolution reduced;
- adaptive pixel ratio (DPR) constrained;
- lazy-load scenes and only render active preview;
- stop offscreen/unmounted render loops;
- reduced-motion support and visually equivalent static fallback.

These are target values, not guarantees or test results. Report measured device/browser, frame times, sizes and tradeoffs; if mobile cannot be tested, state NOT VERIFIED rather than PASS.

Accessibility:
- all important meaning has accessible semantic DOM equivalent;
- UI controls keyboard and touch accessible;
- no flashing effects;
- background 3D never necessary for the user to learn or answer exam questions.

====================================================
J. ASSET LICENSING / ORIGINALITY
====================================================

Preferred: own procedural geometry + own Blender files + own generated concept art.

Allowed: confirmed CC0 textures/HDRIs (e.g. Poly Haven), recorded in LICENSES.md and ASSET_MANIFEST.csv. Other sources require checked license and proof.

Forbidden:
- ripping game meshes/textures;
- scraping random Google Images / copyrighted maps;
- copying branded characters;
- assuming publicly accessible file equals licensed commercial redistribution;
- downloading Korean learning app UI screenshots and painting over them;
- buying/licensing restricted packs without user's approval.

Every external asset must have source URL, author/license terms and date accessed when known. If the license is unclear, replace the asset with original procedural art.

====================================================
K. MILESTONES — SMALL VERTICAL SLICES
====================================================

STAGE 1: foundation and art direction
- inspect isolated folder and setup dependencies;
- produce original concept study, material/color rules and 3 mascot explorations;
- run standalone preview with simple meaningful geometry;
- stop expanding scope until the selected style is coherent.

STAGE 2: ONE exceptional scene
- build finished Hanok Rooftop Arena + one functioning original 3D mascot;
- optimize and deliver 2D fallback;
- inspect desktop/mobile rendering and asset validation.

STAGE 3: coherent animation kit
- idle/ready/cheer/gentle-loss/level-up;
- reduced motion and quality switching.

STAGE 4: Learning Alley
- six unique architectural nodes, locked/current/completed visual states;
- avoid recreating entire city geometry independently; reuse prop kit/materials.

STAGE 5: export and quality hardening
- optimize assets; run validator; build the preview;
- write final export manifest, LICENSES.md, PERFORMANCE_REPORT.md, QA_CHECKLIST.md;
- capture actual preview screenshots and asset gallery;
- document integration proposal without touching the real app.

Don't generate twenty mediocre scenes. Quality first: one unforgettable hero and one unforgettable mascot, then expand using the SAME design language.

====================================================
L. ACCEPTANCE / PROOF OF WORK
====================================================

A milestone is NOT completed by writing text that describes a future asset.

Each stage must produce verifiable outputs:
- working preview source;
- actual textures/posters/GLB or reproducible procedural mesh source as specified;
- actual screenshot/capture if available;
- a truthfully updated manifest;
- files optimized and inspected;
- measured performance where hardware is available;
- build and typecheck pass.

Do not claim to have generated an image if no file was saved.
Do not claim to have rigged a GLB if it is only a flat PNG.
Do not call a scene 60 FPS if no measurement was taken.
Do not fabricate test/build results.
Do not create placeholders named final and present them as ready for production.

Deliver after completion:
1. `preview/` runnable standalone, instructions to run it;
2. exported `exports/v1/...` assets with actual files;
3. editable Blender or procedural geometry sources;
4. `ART_BIBLE.md`, `COLOR_MATERIAL_SYSTEM.md`, `CAMERA_LANGUAGE.md`;
5. `LICENSES.md` and completed `ASSET_MANIFEST.csv`;
6. `PERFORMANCE_REPORT.md`, `QA_CHECKLIST.md`;
7. mobile + desktop screenshots and 2D fallback;
8. `INTEGRATION_NOTES.md` describing (only) hypothetical future integration;
9. list of any unfinished assets and honest limitations.

END CONDITION
After Stage 5, STOP. Do not implement TOPIK, EPS, SRS, PvP, auth, social, QR, payments, API, analytics, server or production Korean Arena integration. You are working on a standalone 3D art studio only.
```
