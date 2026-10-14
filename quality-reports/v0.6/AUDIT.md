# ART-PIVOT-006 — audit and concept-gate evidence

The user reviewed v0.5 and explicitly requested a Playful Hangeul Town art pivot. This delivery stops at sections4/12: audit, three characters, two towns, materials, cost/reuse recommendation and a recoverable checkpoint. Section13 prototype is pending concept approval; section16 publication is pending separate approval.

## What was inspected

- Existing instructions/master, four progress records, art/camera/material/performance standards, Git history/status and release manifest. Clean starting main5578f5f matched origin and `checkpoint/v0.5-public-verified` independently.
- Current `preview/src/reforge` App/Scene/Nari/World/physics/footPlacement/assets/types and old packaging/optimization/QA scripts. Existing React19.3/R3F9.8/Drei10.7/Three0.186/Vite8 stack retained. No dependency or setup configuration change needed under the onboarding skill.
- Both current actual Blender sources opened read-only with Blender4.3.2: world761mesh objects/3NLA tracks, Nari28bone armature/20NLA tracks/10morphs plus Basis. Source hashes unchanged. `baseline/blender.json` records packed images and actual source structure.
- Both current actual GLBs read with glTF Transform and freshly checked with glTF Validator: **0errors/0warnings**. World75,514tri/60primitives/5,714,488B; Nari23,794tri/6primitives/2,923,840B/28joints/20clips/10morphs. `baseline/assets.json` and two native Validator reports retain hashes and facts.
- Exact public HTML082c661b/13,543,219B returned HTTP200 and rendered in Chromium, rather than being accepted as raw source. Fresh Low57draws/99,012tri; Medium/High133draws/195,524tri including relevant passes. Native day/night/Nari PNGs actually opened and inspected. Raw sumGLB8,638,328B differs from HTML/wire transfer; this is not a load-time benchmark.

## Why pivot without discarding working systems

Current hero prioritizes the large roof while Nari is small. Existing Nari is formal and long-limbed; face remains less readable than a large-eyed chibi at courtyard scale. Low night has readable architecture but dark roof/character. Keep controller, camera, doors, accessibility, animation state machine and export/validation pipeline; redesign only separate v0.6 topology/material/layout after approval. Shorter-leg retargeting, collision dimensions, IK foot offsets and floor constants require adaptation rather than blind reuse. Existing20clips do not include Dance; body turning to camera does not prove eye tracking.

## Concept evidence and limits

- `concepts/v0.6/nari-chibi-directions.png`: three original concepts, each front/side/silhouette/three expressions/palette; native image_gen output actually viewed. A student/backpack, B paper messenger, C artisan cap/apron.
- `concepts/v0.6/town-and-material-directions.png`: T1 open Letter Plaza and T2 garden-loop Craft Court plus seven material/color studies; actual image viewed. One house per alternative. Proposed hex palette and complexity/budget/reuse plan in `CONCEPT_REVIEW.md`/`palette.json`.
- Exact generation prompts and provenance JSON saved; **no external reference images/game assets downloaded**. Image generation is illustration, not a model, texture export, game animation, structural proof or performance measurement. Illustrated foliage/woodgrain density must be reduced for real-time production.
- Review HTML embeds five unchanged PNGs, no external request; desktop and390px layout checked. Downloadable four-page PDF rasterized and **all four actual PDF pages opened**; first print draft split text, corrected print-only image height/margins. PNG artwork unchanged.
- Medium70–95draw/B+T1 2.6–3.7MB budgets are forecasts; no v0.6 runtime/GLB exists to measure. Physical desktop/mobile CPU/GPU/FPS unmeasured; no30/60FPS claim. No v0.6 production build/locomotion/GLB QA is claimed or run before approval; unchanged application source does not need a rebuild for this concept-document gate.

## Preservation and release

`preserved-v05.json` protects **2,335** existing tracked files, excluding only five evolving session records. Verification checks every file/hash: sources, art, GLBs, maps, animations, all old evidence/packages/artifacts, package locks, deployment workflow/staging scripts included. Changes are additive concepts/reports/docs/downloads and permitted five records. Current public artifact082c661b stays unchanged; no workflow dispatch or release input modification. `pages-unchanged.json` checks latest Actions source is still v0.5 4a29565/run38573493700. Recovery tag remains5578f5f.

Final review recommendation **B+T1**, user approval **PENDING**. Preserve the generated boards on resume; do not regenerate them, remodel Nari, build a full town, start future districts or publish v0.6 automatically.
