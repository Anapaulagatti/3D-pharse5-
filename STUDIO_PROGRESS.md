# Studio progress

Current milestone: REFORGE-005 — Joseon Fantasy Reforge IN_PROGRESS. User explicitly APPROVED A — Nari; no re-approval needed. Public v0.5 deployment NOT authorized. Public v0.4 preserved.
Current task: REFORGE-GATE-C-005 IN_PROGRESS. Gate A/B DONE; D/E TODO. Gate C is NOT accepted while deformation/browser checks remain.

Last verified remote checkpoints:03cc02b2134c7b1d9362a13a08a8c34fc98eed40 (verified Gate B) and572d53f6fe14b09491338f6377e763cfa0438006 (actual Nari draft1 + visible defects), both origin/main matched after push. v0.4 recovery tag checkpoint/v0.4-pre-reforge-005→9cc1381.75 protected source/art/deployment/lock hashes unchanged at Gate B.

Gate B: actual full four-sided Hanok graybox Blender/GLB2,142,648bytes/51,596triangles/11primitives, Validator0/0, source419modules/209support pairs. Actual33 views including24-angle orbit/mobile; front/rear/sides/roof/connection/interior inspected. Source/displayCSS and roof-framing fixes verified. REVIEW.md and6s manually-stepped360MP4 retained. Low12draws/51,908tri incl1.45m proxy, medium24/103,816incl shadows. Not final art.

Gate C actual files: Studio/modeling/nari-v05.py; assets/v0.5/source-blend/nari-messenger.blend; exports/v0.5/models/nari-messenger.glb; gate-c/rig-authoring.json. Continuous voxel-unioned body, genuine28bone armature/normalized≤4skin weights,20native clips,10morphs (Neutral basis+9emotions/Blink), editable NLA and analytic limb IK. Current GLB2,173,544bytes/24,308triangles/6primitives. Source/export now uses native bone-heat body weighting after manual underarm wedges found. Latest correction needs actual review/Validator.

Important failed visual history: initial-render/ shows hip/vest grabbed by arm weights; corrected-render/ and rig-review/ have actual20static/20live/10face automated pass but human-rejected underarm white wedges. Both reports explicitly say AUTOMATED_PASS_VISUAL_DEFORMATION_REJECTED. Do NOT count them as visual acceptance. Latest bone-heat fix untested. Source currently solves body with Root/accessory/Finger bones excluded from heat, then normalizes/limits4; torso garments and accessories retain explicit weights. Blender solve succeeded (685weights limited). Export temporarily roots meshes (saved authoring source remains parented) removes17initialValidator warnings; plainGLB no Draco dependency.

Controller code implemented in preview/src/reforge/physics.ts and Nari/App/Scene/types/style: fixed1/60kinematic capsule, world movement matched to in-place stride (.8148walk/2.4375run), acceleration/stop/heading, stairs/floor/collision/door and physics jump, native clip scheduler/crossfades/one-shots, keyboardWASD/arrows/Shift/Space/E, pointer/keyboardDPad, perspective follow/orbit/obstruction, pause/OS reduced motion/offscreen logic, basic WebGL/context-loss fallback. Actual6pure physics tests PASS (closed door, staircase+opened entry, raised floor, rear wall,0.472mjump+landing,release stop). Browser play-review first W movement passed then Run wait timed out; state/path suggests short Run window before door but not yet proven. Driver now resets and uses clear Shift+D runway plus50–100ms polling and bounded actual clip event history. All real native/mobile/camera/pause/OS checks must finish; do not claim them done.

Current runtime: isolated ?candidate=v05, existing default v0.4 App/public artifact unchanged. Existing internal Vite preview4186 session53015 serves preview/dist; must restart if lost, no user-facing loopback URL. Latest build before current bone-heat export/event trace; rebuild required. No dependencies installed/locks changed. Existing toolchain reused.

Remaining Gate D: full art Hanok (not graybox), roof tiles/joinery/lattice/ground/plum/props/lanterns/banner/water where relevant; original procedural texture grain/materials; day/evening/night currently UI exists but Scene lighting still fixed! Ambient life/contact-shadow/effects controls/interactive tree+lantern, smooth focus/preset transitions and finished camera. Default local candidate still architecture mode until final art hero. Optional legacy companion asset preserved; no new districts/audio/backend.

Remaining Gate E: current new GLB/rig proof, actual final desktop/mobile/OS/fallback/quality/console/resource checks, measured costs (no hardwareFPS), genuine gameplay video≥5swalk+5srun+jump/greet/face/enter or circle, before-after and final PNG/video review, versioned standalone/static review package/privacy/provenance/subpath checks and checkpoint. Do not modify workflow/staging/showcase-v0.4 inputs or publish v0.5 until explicit approval.

## NEXT SESSION HANDOFF

**Current milestone:** REFORGE-005; A/B complete, C IN_PROGRESS, D/E TODO.

**Current task ID:** REFORGE-GATE-C-005 — fix actual humanoid deformation and verify playable controller.

**Last verified checkpoint:**03cc02b verified Gate B;572d53f remotely verified draft1. Current recovery checkpoint follows in history.

**Completed work:** A approval, full verified graybox, real rig/weights/morphs/20clips draft, isolated R3F review/controller/input/camera code,6physics checks. Prior actual images and failures retained truthfully.

**Unfinished work:** Bone-heat current model actual pose inspection, full native play/OS/mobile run, then Gate D art/life/lighting and Gate E production/media/package. Current callbacks/code may still contain defects; inspect actual browser outcomes.

**Files to inspect:** source nari-v05.py; gate-c/rig-authoring.json, validator-current.json (preceding manual-weight model, must recheck), rig-review/verification.json (REJECTED), play-review/failure.json, physics-verification.json; verify-reforge-character/play/physics.mjs; preview/src/reforge/*; STUDIO_TASKS and original request.

**Known blockers:** No user-decision blocker. Need resolve visible underarm skin distortion and actual native browser acceptance. Public v0.5 release not authorized; target hardware FPS unmeasured.

**Exact next command or action:** Run Validator on latest Nari, npm --prefix preview run build; inspect a few actual Happy/Greeting/Thinking/side/rear renders first to see whether bone-heat removed wedges. Do not rerun all72images before checking key defects. Run updated native play driver with STUDIO_V05_PLAY_REPORT_DIR=.../play-pass-2 (preserve failed first output). Continue fixing until Gate C accepted, then checkpoint and Gate D/E. Do not stop for another A choice.

**Verification required:** Actual rendered anatomy/side/rear deformation and foot contact,20clips/10distinct expressions, real native keyboard/touch world movement/run/jump/collision/door/camera/one-shotreturn/pause/OS/offscreen/fallback, then final art and production/package/video checks. No conceptual or automated-only acceptance.

**Remote GitHub save status:**03cc02b and572d53f pushed+origin matched. Current recovery checkpoint must be committed/pushed and compared. No Pages deployment triggered; publication inputs preserved.
