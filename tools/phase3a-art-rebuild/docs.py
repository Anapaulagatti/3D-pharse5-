"""Generate the six requested review documents,with explicit source/inspector/world evidence scopes."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';S=R/'assets-src/npcs/phase3a-art-rebuild';TAG='checkpoint/phase3a-illustrated-three-pilots-review-20261028';IDs=['seoyeon','minseo','harin'];audit=json.loads((D/'protected-audit.json').read_text());native=json.loads((D/'native-render-qa.json').read_text())
def put(n,s):(D/n).write_text(s.strip()+'\n')
put('README.md',f'''# Phase3A · Three illustrated NPC pilots

**ARTISTIC APPROVAL PENDING.** Original14procedural NPC artworks at4ed5a53 are HUMAN REJECTED. This candidate replaces only Seoyeon,Minseo,Harin. Elevenremaining illustrations remain unchanged/rejected and their rebuild is LOCKED. Phase3B LOCKED. No merge or public deployment.

[Playable pilot ZIP](PHASE3A_ILLUSTRATED_PILOTS_REVIEW.zip) · [visual review](PILOT_REVIEW.md) · [gallery](REVIEW.html) · [native actual-world comparison](juni-before-after-world-native.png) · [same-phase Phaser inspector comparison](juni-before-after-inspector-native.png) · [QA](QA.md).

Branch `feature/phase3a-npc-art-rebuild`. Before checkpoint `checkpoint/phase3a-npc-art-before-rebuild-20261028` at `{audit['baseline']}`; original rejected review4ed5a53 and all previous references retained. Final review reference `{TAG}`.

Extract ZIP,run `python3 start_review.py`,open `http://127.0.0.1:4388/REVIEW.html`. No Node or network required for actual play. The package includes the canonical world,12approvedplayers/28cosmetics/Studio and retained14NPC engine/data. Only3newillustratedpilot visuals are under review;elevenlegacy NPCs may still be encountered and are NOT approved. Use the3pilot links to focus review.

The supplemental Phaser clip inspector compares actual Juni,BEFORE and AFTER at native scale. It is an asset review utility,not a new player/NPC engine and not canonical gameplay/navigation evidence. Frozen Harin12pxvertical patrols cannot display a complete44pxstride in one heading;routes were preserved. Full8frame source loops and inspector playback complement the3genuine world recordings.

[Pipeline](ART_PIPELINE.md) · [Juni comparison](JUNI_STYLE_COMPARISON.md) · [protected hashes](PROTECTED_AUDIT.md) · [exact human directive](HUMAN_DIRECTIVE.md).

Technical checks do not establish artistic acceptance. Raw third-party FAIL/WARNs are retained,including control runs on approved Juni. One existing tangerine foreground edge clips6native shoe pixels in one Harin capture;the exact source ownership is documented,not hidden or relabelled a renderer fault. Physical devices/hardware GPU NOT TESTED. STOP for human3pilot artistic approval before any of the remaining11.
''')
put('ART_PIPELINE.md','''# Actual illustrated-source workflow

## Confirmed provenance and tools

[Phase1 source record](../phase1/SOURCE_PROVENANCE.md),[Phase1B source record](../phase1b/SOURCE_PROVENANCE.md),[approved Juni native reference](../../assets-src/characters/phase1/juni-style-reference.png). Juni is treated as immutable verified artwork;we do not assert an undocumented original creation method. Phase1B explicitly records independent built-in image-generated turnarounds,native finishing and authored PNG-layer animation. That confirmed workflow is the basis here.

Pinned skills read and applicable stages actually executed:

- [Sprite Forge generate2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/generate2dsprite/SKILL.md):doctor,master prompt jobs,actual host-image illustrations,selected-master keying/registration,and unmodified frame diagnostics.
- [Sprite Forge video2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/video2dsprite/SKILL.md):read;capability/FFmpeg doctor executed. AIvideo route unavailable. No `sprite_set run` or generated motion video is claimed. Explicitly authorized Phase1B own-layer rigging provides motion instead.
- [Character Animation Creator](https://github.com/tachikomared/character-animation-creator-skill/blob/9ce98dffb98c84488fe7b99b62c49fabee20abd6/SKILL.md):key-clean diagnostic,unmodified sheet/motion diagnostics. Its square-cell assumptions are not silently substituted for requested96×112. All results and limitations retained.

[Doctor](tooling/doctor.json),[doctor log](tooling/doctor.log),[video doctor](tooling/video-doctor.log),[executed diagnostic commands](tooling/execution-manifest.json),[raw Forge FAIL/WARN values](tooling/all-forge-warnings-and-failures.json),[verbatim selected-master warnings](tooling/selected-master-warnings.json). Tool clones remain pinned in `/workspace/tooling-cache`;no third-party tool source or AGPL dependency is added to the game. `master_still approve` means internal technical selection/preparation,not HUMAN artistic approval.

## Primary artwork

Seven actual `image_gen.imagegen` calls:3independent identity masters,3independently illustrated four-view source boards,1small illustrated prop board. [Exact prompt/source/reference/SHA provenance](../../assets-src/npcs/phase3a-art-rebuild/run-manifest.json). Route `host_image`. Host model/cost not exposed. No external paid image/video API,key or paid agent was used. Video-generation capability was not invented.

Juni and approved Bomi are style/proportion references,not pixel donors. No player face/costume/atlas pixels and no rejected procedural NPC bodies enter the new assets. Original generated files and copied raw masters remain immutable. Front/back/left/right are separately illustrated views in each board,not mirrored completed sprites. The high-resolution boards are NOT claimed to be native logical grids or animation sheets.

## Deliberate native finish and rig

- Inspect source ownership boundaries:explicit row splits627/640/612 avoid one view leaking into its neighbor. Remove saturated chroma alpha while preserving plum/jade/brown fabrics.
- One fixed source-to-native scale per identity,using the maximum rest-view extent so no view is enlarged above the80pxpeer envelope. Premultiplied/area BOX finish,binary alpha,shared96colour palette,no dither. No dynamic per-frame bbox fitting,upscaling,global sharpening or blur.
- Eight explicit own-palette eye-cluster retouches per identity. Static per-direction own-head translations align eye/neck landmarks without resizing heads or moving feet. Exact edits in each `native-retouches.json`;source originals retained.
- Author actual native PNG alpha masks,joints and ownership. Correct stray A-pose hands in leg masks and trouser pixels in forearms. Where a far arm is hidden,derive that arm from the SAME view's own illustrated visible sleeve/hand;not from torso,player or rejected art. Small under-arm torso recovery clones the same identity's illustrated garment only within an authored silhouette. Explicit recovery records remain in `rig.json`.
- Reuse the protected Phase1B pure PNG affine helpers. Front/back use actual approved Juni same-index foot/hand/bob landmarks. Profiles use the previously accepted44pxstance/Hermite swing logic with opposite arm swing. Only numeric direction-of-motion signs change;completed directional artwork is not mirrored. Own shoes provide lift/foreshortening. Round once at raster placement to avoid the diagnosed1.5pxdouble-rounding drift;independent resulting stance≤1px.
- Greeting and occupational activity have8distinct cells in every direction. Guidebook,espresso mug and tangerine derive from the separately illustrated prop board and are baked at the actual wrist,with back-view body occlusion. They are not floating runtime overlays.
- Export104cells/actor into the unchanged768×1456layout;keep original96×112frame names,atlas JSON,48,100anchor,clip timing,data,engine,movement and collision. Only3derived atlas/preview/provenance groups change.

[Native structural/raster audit](art-technical-qa.json),[literal own-head stability](head-stability.json),[actual world readbacks](native-render-qa.json),[supplemental inspector readbacks](inspector-native-qa.json). No successful count or automated check grants art approval.

Reproduce with Python3,Pillow12.3.0,NumPy2.3.5,SciPy1.17.0: `prepare.py` → `native_retouch.py` → `props.py` → `rig.py` → `animate.py --export` → `audit.py`/`head_qa.py`,all under `tools/phase3a-art-rebuild/`. These operate only on the3newsource namespaces and9authorized derived image/provenance files. Do not execute the rejected `tools/phase3a/art.py` for new production.
''')
put('JUNI_STYLE_COMPARISON.md','''# Juni versus BEFORE versus AFTER

All columns use native96×112cells and scale1;the new figures were not enlarged to manufacture detail. Review enlargements use integer nearest-neighbor only. Juni and the12approved playable actors remain byte-identical.

## Canonical-world native evidence

![Juni BEFORE AFTER actual world native1:1](juni-before-after-world-native.png)

[Readable3×copy](juni-before-after-world-review-3x.png). Crops contain genuine ground/lighting and may include nearby actors at the edge;full screenshots remain linked below. BEFORE is an actual Phaser replay of the exact rejected checkpoint PNG at its original texture URL,using the unchanged engine/data/world. AFTER uses only the3newatlas replacements. No rendered pose,position,physics,camera or clock was forced.

## Same-phase native Phaser clip inspection

![Actual Phaser inspector native](juni-before-after-inspector-native.png)

[Readable3×copy](juni-before-after-inspector-review-3x.png). These are actual Phaser-rendered sprites at the same normalized animation phase/scale,with approved Juni alongside old/new NPC cells. Neutral QA backdrop;this is SUPPLEMENTAL clip inspection,not world-navigation proof. [36pixel-exact sprite readbacks](inspector-native-qa.json).

Assess faces/eyelids/brows,hair volume and highlights,collars/cuffs/folds,footwear,silhouette,palette,source identity and animation continuity. We consider the illustrated source substantially closer to the approved family;human review must decide whether it meets Juni's craftsmanship. No PASS based solely on104cells or technical checks.
''')
text=['# Three-pilot artistic review','','**Human ARTISTIC APPROVAL PENDING. Elevenremaining NPC rebuilds andPhase3B LOCKED.**','','[Play ZIP](PHASE3A_ILLUSTRATED_PILOTS_REVIEW.zip) · [Juni native comparisons](JUNI_STYLE_COMPARISON.md) · [QA](QA.md) · [pipeline/source provenance](ART_PIPELINE.md).','']
parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Three illustrated NPC pilots</title><style>body{background:#1d1b24;color:#f4e7cc;font:17px system-ui;max-width:1152px;margin:24px auto;padding:16px}a{color:#9ddbc0}img,video{max-width:100%;height:auto}img.pixel{image-rendering:pixelated}section{margin:32px 0;padding:16px;background:#292630}h1,h2{color:#ffdc8c}video{display:block;width:100%}</style><h1>Seoyeon · Minseo · Harin</h1><p>THREE illustrated pilots only. HUMAN ART APPROVAL PENDING. Elevenremaining rejected NPC artworks are unchanged;their rebuild andPhase3B are LOCKED.</p><p><a href="PHASE3A_ILLUSTRATED_PILOTS_REVIEW.zip">Playable ZIP</a> · <a href="QA.md">QA and retained FAIL/WARNs</a> · <a href="ART_PIPELINE.md">Source/tool provenance</a> · <a href="../../tools/phase3a-art-rebuild/clip-inspector.html">Supplemental Phaser clip inspector</a></p><h2>Actual canonical world · native1:1</h2><img class="pixel" src="juni-before-after-world-native.png"><p><a href="juni-before-after-world-review-3x.png">Integer3×review copy</a></p><h2>Same-phase Phaser asset inspector · native1:1</h2><img class="pixel" src="juni-before-after-inspector-native.png"><p>Supplemental neutral atlas inspector,not canonical gameplay. <a href="juni-before-after-inspector-review-3x.png">Integer3×review copy</a></p>']
for id,ko,role in [('seoyeon','서연','Palace cultural guide'),('minseo','민서','Café barista'),('harin','하린','Jeju orchard keeper')]:
 source=f'../../assets-src/npcs/phase3a-art-rebuild/{id}';pub=f'../../public/assets/npcs/phase3a/npc-{id}'
 text +=[f'## {id.title()} · {ko} — {role}','',f'![Illustrated master review]({id}-master-review.jpg)','',f'[Original master]({source}/master-source.png) · [Original four-view source]({source}/turnaround-source.png) · [Native turnaround]({id}-native-turnaround.png) · [Readable3×turnaround]({id}-native-turnaround-review-3x.png) · [Complete104cell atlas]({pub}/atlas.png) · [Frame registrations]({pub}/atlas.json) · [Own masks/joints]({source}/rig.json).','',f'[AFTER full native world screenshot with Juni](gameplay/after-{id}-with-juni-phaser-native.png) · [BEFORE full native](gameplay/before-{id}-with-juni-phaser-native.png) · [Actual AFTER gameplay video](gameplay/after-{id}-actual.mp4) · [Actual BEFORE replay](gameplay/before-{id}-actual.mp4).','',f'![Native actual-world dialogue](gameplay/after-{id}-dialogue.jpg)','',f'[Front8phase source motion]({id}-walk-front-source-motion.webp) · [Back]({id}-walk-back-source-motion.webp) · [Right]({id}-walk-right-source-motion.webp) · [Left]({id}-walk-left-source-motion.webp). These animated source previews are labelled SOURCE,not gameplay. Full normalized3loop/direction actual Phaser atlas playback is [separately recorded](supplemental-clip-inspector-actual.mp4). Canonical world recordings show original patrols,real approach/dialogue/return.','']
 parts.append(f'<section><h2>{id.title()} · {ko} — {role}</h2><img src="{id}-master-review.jpg" width="384"><p><a href="{source}/master-source.png">Original master</a> · <a href="{source}/turnaround-source.png">Original four-view source</a> · <a href="{pub}/atlas.png">104cell atlas</a> · <a href="{source}/rig.json">Authored masks/joints</a></p><img class="pixel" src="{id}-native-turnaround.png"><p><a href="{id}-native-turnaround-review-3x.png">Integer3×turnaround</a></p><h3>Actual canonical AFTER gameplay</h3><video controls preload="none" src="gameplay/after-{id}-actual.mp4"></video><p><a href="gameplay/after-{id}-with-juni-phaser-native.png">Full native1:1 AFTER with Juni</a> · <a href="gameplay/before-{id}-with-juni-phaser-native.png">BEFORE native1:1</a> · <a href="gameplay/before-{id}-actual.mp4">Actual BEFORE replay</a></p><img src="gameplay/after-{id}-dialogue.jpg"><p>Full8phase source motion,not gameplay: <a href="{id}-walk-front-source-motion.webp">Front</a> · <a href="{id}-walk-back-source-motion.webp">Back</a> · <a href="{id}-walk-right-source-motion.webp">Right</a> · <a href="{id}-walk-left-source-motion.webp">Left</a></p></section>')
text+=['## Review limits','',f'{native["actualCaptures"]}actual canonical before/after captures;0unexplained source/render mismatch. One Harinwalk-left0 has6shoe-edge pixels covered by the unchanged `c/tangerine-3`ground-containing foreground plate atworldx3787,y4075–4080. Exact matching source/depth ownership is in [native QA](native-render-qa.json);[close inspection](tooling/harin-native-occlusion-investigation.png). This P2existing ownership edge is not fixed by shrinking art,moving NPCs or repainting protected Jeju.','', 'Harin frozen patrol has12pxvertical legs and88pxtotal length,while its accepted animation stride is44px. Some heading/frame combinations never occur on this short route. All32walk cells are source-validated;full8phase/direction playback is in the clearly labelled Phaser inspector. Actual canonical movement remains separately recorded;no route was extended for evidence.','', 'Automated Forge FAIL/WARNs and square-cell tool limitations are retained. Human must judge source quality,face identity,anatomy,garments,foot contact,occlusion and perceived gait. Physical devices/hardware performance NOT TESTED. STOP before remaining11.']
put('PILOT_REVIEW.md','\n'.join(text));parts.append('<section><h2>Supplemental actual Phaser clip inspector</h2><video controls preload="none" src="supplemental-clip-inspector-actual.mp4"></video><p>Three complete normalized loops for front/back/right/left of all3pilots. NOT canonical-world gameplay or collision evidence. Frozen short routes remain unchanged.</p></section><p>One existing Jeju foreground ownership edge clips6shoe pixels in one recorded pose;see QA. Third-party heuristic FAIL/WARNs retained. Physicaldevices NOTTESTED. HUMAN ART APPROVAL PENDING;11remaining/Phase3B LOCKED.</p>');put('REVIEW.html','\n'.join(parts))
put('PROTECTED_AUDIT.md',f'''# Preservation and rollback

Baseline `{audit['baseline']}`;beforecheckpoint `checkpoint/phase3a-npc-art-before-rebuild-20261028`;rejected4ed5a53 and all previous checkpoints retained. [Exact frozen manifest](protected-baseline.json),[current audit and9before/after hashes](protected-audit.json).

**{audit['unchangedFiles']}existing source/runtime/asset/tool/test files unchanged.** Allappsrc including NPC Registry/FSM/navigation/dialogue/population/persistence/culling/assets/camera/player engine are byte-identical. All14NPC IDs,names,occupations,spawns,route points,interaction radii,frame registrations/clip timings unchanged. Approved world,masks,geometry,collision,12players/28cosmetics/Studio/speeds/progress code unchanged.

Only9existing derived asset files change: `atlas.png`, `preview-native.png`, `provenance.json` forSeoyeon/Minseo/Harin. All3oldatlases remain recoverable;exact baseline copies serve the labelled BEFORE inspector. Elevenother rejected NPC illustrations remain byte-identical and await the human pilot gate.

New own illustrated masters,raw generation prompts,turnarounds,native finishes,retouches,PNGmasks,joints,occlusion patches,frames and build/QA tools are separate under `assets-src/npcs/phase3a-art-rebuild`, `tools/phase3a-art-rebuild` and this documentation directory. The review clip utility lives under tools and does not enter production gameplay. No original player or source illustration is re-exported.

`AGENTS.md` and `docs/current/PROJECT_STATE.md` record the explicit rejection,new3pilot authorization and review STOP. No historical source/tag/checkpoint overwrite,no main merge,no publicdeployment,no separate learning-site changes. Reproduce `python3 tools/phase3a-art-rebuild/audit.py`.
''')
put('QA.md',f'''# Three-pilot QA

**Technical results are scoped. Human artistic approval PENDING.** Original14procedural artworks remain HUMAN FAIL. This review is only3newillustratedpilots,not an acceptance of11legacy visuals.

| Area | Status | Evidence / limitation |
|---|---|---|
| Typecheck/assets/lint/format/unit/build |See final logs|Existing commands,131unit tests;no original test removed/relaxed |
| Full E2E |PASS|60tests,0skipped/0flaky;first integrated illustrated candidate |
| Final focused E2E |See report|7existing NPC cases after final subpixel-to-native shoe placement correction;engine/data unchanged |
| Protected source/world/players/engine |PASS|{audit['unchangedFiles']}frozenfiles;only9authorized derived image/provenance exceptions |
| New primary illustrations |DELIVERED / PENDING HUMAN|7actual builtin calls;3masters/3fourviewboards/1propboard;no code-painted bodies |
| Native registration/source/alpha/ownership |PASS structural|312cells,96×112/48,100;all16clips/actor distinct;binaryalpha;connectedmajoranatomy;bounds;atlas/source exact |
| Profile world stance |PASS raster scope|6independent actual shoe-pattern tracks,≤1nativepixel phase-sampled drift;not a human gait approval |
| Own face/hair stability |PASS literal pixel scope|96sourcehead comparisons,0changedpixels after known fixed pose translation |
| Canonical native before/after |PASS visible pixels / WARN occlusion|{native['actualCaptures']}realcaptures;0unexplained mismatches;6pixels clipped by pre-existing foreground edge |
| Supplemental Phaser native inspector |PASS|36actualsprite readbacks,0mismatch;12direction clips≥3loops;not world-navigation proof |
| Existing patrol/interaction/collision |PASS exercised scope|Actual3approaches/dialogue/close/resume;60fullregression;routes/collision unchanged |
| Independent playable ZIP |PENDING package proof|Must verifyCRC/SHA and test independently extracted actual game/inspector |
| Third-party gait heuristics |FAIL/WARN retained|Exact diagnostics unchanged,including same FAILs on approved Juni;see below |
| Creator square-cell diagnostics |LIMITATION / WARN|Requested96×112 differs from tool96×96assumption;actual reports retained;rectangular audit separate |
| Source key choice |WARN retained|Raw selected-master key-overlap warnings remain;native bright-key residue0 and binaryalpha verified |
| Elevenremaining artwork rebuild |LOCKED / NOT DONE|Await explicit human approval of these3pilots |
| Physical Android/iPhone/GPU/thermal |NOT TESTED|Desktop browser proof is not device certification |
| Artistic/anatomy/dialogue acceptance |PENDING HUMAN|No build,framecount or hash establishes art acceptance |

## Exact retained third-party results

[All Forge FAIL/WARN envelopes with verbatim id/value/threshold/frames](tooling/all-forge-warnings-and-failures.json). Unmodified requested Forge commit checks all12pilotwalk directions AND4approved Juni control directions. Juni front/left/right also receive `leg_alternation`FAIL;Juni left also has `identity_head_ratio`FAIL. These control failures are NOT used to rewrite the pilot statuses. Auto-luminance leg ownership and geometry-derived identity estimates need human interpretation against the actual source/foot/face proof. No threshold,suite or source reference is weakened.

The new independent [literal head control](head-stability.json) proves0face/hair pixel changes despite matcher residual warnings. [Raster stance](art-technical-qa.json) measures the actual own-shoe pixels and preserves forward travel. Actual gameplay and source/inspector clips remain the visual authority. Front/back follow approved Juni's same-index phases,including its inherited irregularities;no claim of perfect anatomy/motion is made.

[Executed commands/tool return codes](tooling/execution-manifest.json). Creator's square diagnostics are retained,not represented as rectangular PASS. Source-selected master warnings are recorded in `master-prepare.log`/`master-prepared/master.json` for each identity. No unavailable AI-video workflow was claimed.

## P2 existing foreground ownership edge

AtHarinworldroot `(3770,4082)`,walk-left0,sourcepixels `(65,93..98)` are occluded atworld `(3787,4075..4080)` by the unchanged `c/tangerine-3`image,sortY4165>NPCdepth4082.05. All6actualRGBs equal that foreground's exact opaque sourcepixels. This is an existing ground-containing rectangular ownership edge,not runtime interpolation or source blur. [Exact pixel ownership](native-render-qa.json),[native closeup](tooling/harin-native-occlusion-investigation.png). World/route/position are explicitly frozen,so no scenery edit,shoe shrink,overlay or relocation was used to conceal it. Remains for human/local integration decision.

## Evidence coverage

Canonical videos use actual original controls and ambient NPC FSM;BEFORE replays only exact baseline PNG bytes at original texture URLs. No pose/position/clock/physics override. Harin12pxvertical patrols cannot expose all44pxstride phases in one heading. Initial capture requests for impossible heading/frame combinations were corrected in the QA harness only. A supplemental atlas inspector exposes the entire8frame loops using actual Phaser,clearly labelled as non-world proof. Source and live coverage are never conflated.

The final shoe bake replaced double banker's rounding (initial1.5pxmeasured drift) with single half-up native placement of the continuous offline target. Runtime sprites/cameras remain native integers;no renderer code changed. Final independent source stance≤1px;freshbuild/focusedcases and extracted ZIP exercise finalassets. Previous full60regression remains separately recorded.

[Native source audit](art-technical-qa.json),[world readbacks](native-render-qa.json),[inspector readbacks](inspector-native-qa.json),[actual AFTER trace](after-capture.json),[actual BEFORE trace](before-capture.json),[media provenance](media-provenance.json),[protected audit](protected-audit.json). No shops/economy/quests/rewards/learning integration,remaining11NPCart production,Phase3B,mainmerge or publicdeployment.
''')
print('Six requested docs and labelled world/source/inspector gallery generated;humanart approval PENDING')
