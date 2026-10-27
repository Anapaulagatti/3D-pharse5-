from core import *
import subprocess
base=json.loads((D/'approved-baseline.json').read_text());audit=json.loads((D/'protected-audit.json').read_text());s=json.loads((D/'long-session.json').read_text());cat=json.loads((S/'catalog.json').read_text());approved=base['approvedCommit'];tag='checkpoint/phase2c-fashion-studio-review-20261027';approval='checkpoint/phase2b-twelve-characters-approved-20261027'
def put(n,t):(D/n).write_text(t.strip()+'\n')
put('README.md',f'''# Korean Arena · Phase2C Fashion Studio

TECHNICAL PASS — ARTISTIC APPROVAL PENDING. Phase2B is human-approved and locked; Phase3 is locked. This is a review candidate, not an artistic-acceptance claim.

[Playable ZIP](PHASE2C_FASHION_STUDIO_REVIEW.zip) · [visual gallery](REVIEW.html) · [QA](QA.md) · [native default/customized12](twelve-default-fashion-native.png) · [enlarged2×](twelve-default-fashion-review-2x.png) · [device handoff](DEVICE_REVIEW.md).

Branch `feature/phase2c-fashion-studio`. Approved source `{approved}` (`checkpoint/phase2b-walkfront-hotfix-review-20261027`), preserved as `{approval}`. Intermediate checkpoints: `checkpoint/phase2c-foundation-20261027` (5d79429), `checkpoint/phase2c-fashion-catalog-20261027` (f3954af). Final review reference: `{tag}`. Exact commit can be resolved from the annotated tag; tags are never overwritten.

## Delivered

- Existing12 approved identities, native atlases, motion order/anchors/speeds preserved. Frozen world, collision, camera, tour, controls and unrelated engine remain byte-identical.
- Existing10 item IDs remain; their original sources are immutable. Derived paint/erase revisions bind to approved poses and repair old front-walk garment ownership before expansion.
- 18 newly authored designs (6hair/6outfits/6accessories);28 total items,46 character-specific variants,12 complete curated looks. Availability is truthful, not universal.
- Existing Studio extended with Vietnamese/Korean names, animated native previews, visible loading/selection, per-item equipment, reset, save/apply/enter/cancel, named local preset rename/delete and bounded persistence. No competing engine or UI framework.
- Current v1/v2 stores remain readable. Progress, visited markers and world position survive switches and reload. Up to12 personal presets, names trimmed to32characters; existing names/looks are not evicted by a full list. Curated presets remain protected.
- Lazy requested-only atlas composition, deterministic pose/revision-bound keys, base cache2, composite cache2, character textures3. No eagerly generated runtime permutation library.

## Review locally

Extract the ZIP and run `python3 start_review.py`. Open `http://127.0.0.1:4342/REVIEW.html`. The actual compiled game and assets work locally without Node or an external service. Five representative videos and actual native sheets are included; individual crops, remaining per-character videos and full authoring evidence link to the immutable Git checkpoint. Use `--lan` only when intentionally testing on your own LAN device. LAN HTTP works without SubtleCrypto via a verified SHA256 fallback.

Choose a character, select a suggested fashion look or individual compatible items, inspect all directions/actions, enter the world, move, then reopen Studio. Save a named preset, rename/delete it, cancel an uncommitted draft and reload. The12 original appearances always remain available through Reset.

[Catalog](COSMETIC_CATALOG.md) · [matrix](COMPATIBILITY_MATRIX.md) · [animation](ANIMATION_COMPATIBILITY.md) · [performance](PERFORMANCE.md) · [protected audit](PROTECTED_AUDIT.md) · [visual review](VISUAL_REVIEW.md).

No map rebuild, character regeneration, shops/economy/learning integration, paid API, main merge or public deployment. Stop for human Phase2C review; Phase3 remains locked.
''')
put('ANIMATION_COMPATIBILITY.md','''# Animation compatibility and source ownership

Approved native96×112 frame registration, foot anchor48,100, phase names/order, walk60/run100 speeds and character identities are immutable. Juni’s packed source has144 cells; other actors112. No approved atlas is re-exported.

## Foundation before expansion

The original old outfit patches were authored against older front-walk poses. Reapplying those full-body patches could paint old arms/legs over the newly approved motion. Derived patches now use each actor’s approved pose ownership, preserving native head/face and current arm, knee, contact/lift order. Four old outfit variants ×8 front-walk cells were rebound. Hair/accessories were checked for body leakage and bind to the current base hash; obsolete front garment interaction cells are explicitly empty. Original source textures/catalog remain recoverable unchanged.

Actual canonical Phaser foundation:10 single-item looks plus4 old suggested combinations ×14 clips =196 native readbacks,0 mismatch. [Gate](foundation-gate.json), [readbacks](foundation/native-pixel-qa.json). Expansion followed checkpoint5d79429 and a Juni/Sori three-item pilot,28 actual clips,0 mismatch ([pilot](pilot-gate.json)).

[Original patch versus corrected outfit source sheets](REVIEW.html) are explicitly SOURCE ONLY. They reproduce original patches on the current approved base to expose the stale-pose ownership issue; they are not before gameplay footage. Final current gameplay is independently captured.

## Current native pipeline

Each sparse paint/erase variant records the base PNG SHA256, content revision and per-cell offsets. Before use the renderer hashes the loaded base image and requires both variant and mapping bindings to match. Cache keys include base digest and all applicable patch/interaction revisions. Invalid/missing assets or pose mismatch restore approved defaults safely.

Composition order: approved base → non-accessory item patches → before-accessory ownership corrections → accessory patches → any declared after-accessory corrections. Native integer offsets and binary alpha, smoothing disabled; no frame rescaling. Existing Canvas composition and Phaser manager/controller remain the only engines.

Hair follows approved head displacement, including raised run/gesture poses. Head matching spans ±9vertical pixels, covering the approved −7…+5 range. Long hair is behind body/hands and restored over garment shoulders only where appropriate. Hats clear the old hair footprint while preserving the face; round glasses disappear from the rear. Garment masks preserve foreground hands. Festival skirt correctly occludes lifted shoes behind fabric while preserving support soles below the hem. Default footwear is intentionally retained where it carries approved contact anatomy.

## Coverage and evidence

- 46 variants /5,248 registered native cells; no absent mapping keys. Explicit null is intentional hidden geometry, not an export omission.
- 192 compatible appearance combinations /21,760 composed source frames checked offline, including supported start/stop/turn cells. No eager runtime permutation generation.
- All12 curated looks: actual idle4 +walk4 +run4 +wave +celebrate =168 clips. Every claimed new variant appears on both compatible actors. All8 walk/run phases observed; idle2. Default front/right comparisons add24 clips:192 final native captures,0 unexplained opaque-pixel mismatch.
- Actual movement recordings include direction changes and start/stop transitions through the unchanged controller. Exhaustive individual transition-cell coverage is source-side; no claim that every transition frame was separately captured by the camera.
- Existing character-motion E2E covers default movement; all12 default atlases and motion registrations remain exact. No old right/back/run cycle was rewritten.
- [Actual final readbacks](gameplay/native-pixel-qa.json), [source QA](source-qa.json), [all12 gameplay videos](REVIEW.html), [phase-aligned Juni reference source front](walk-front-approved-reference-source-native.png), [right](walk-right-approved-reference-source-native.png), [back-run](run-back-approved-reference-source-native.png).

Native RGB readback proves renderer/source agreement, not artistic acceptance. The complete attire, silhouette, timing, hair/hat fit and garment aesthetics remain for human review. Historical Forge motion WARNs remain in their original Phase2A/B reports; thresholds were not weakened.
''')
put('PERFORMANCE.md','''# Performance and memory

## Observed desktop session

[Raw long session](long-session.json): actual Chromium Canvas,60 genuine character switches,100 cosmetic preview/apply operations,82 resource snapshots, one active player throughout. Repeated presets, cancel, return and reload preserved position, real visited state and a learning-progress sentinel. This is not physical-device certification.

| Measurement | Observed |
|---|---|
| Character switch UI latency | median296ms /p95381ms /max432ms |
| Cosmetic preview→apply latency | median337ms /p95495ms /max596ms |
| Active/resident character textures | ≤3; unique keys |
| Base image cache | ≤2 |
| Composed atlas cache | ≤2 |
| Maximum resident character texture estimate |20,107,056bytes |
| Maximum base image estimate |11,863,312bytes |
| Maximum composite image estimate |13,404,704bytes |
| Observed JS heap range |65,941,976–123,818,877bytes |
| Final JS heap after reload |72,379,084bytes |

UI latency includes loading, decode, composition, UI scheduling and upload orchestration. Synchronous Canvas draw-loop samples are separately recorded in resource snapshots (bounded60samples); they exclude network/decode and do not measure GPU completion. JS heap is not decoded-image memory. Estimates are per-owner width×height×4, may include duplicate ownership of shared resources and must not be summed as measured GPU memory. Heap fluctuation and one bounded session do not prove indefinite leak freedom.

## Architecture

Only selected actors and requested compatible appearances load. Character image previews decode lazily; category thumbnails use lazy loading. Base and composite caches are independently bounded2 each; existing Phaser asset manager bounds resident character textures3. Selecting a new combination does not eagerly generate other combinations. Revision and actual-base-digest keys invalidate affected results without a global cache flush; selective character invalidation is available. Temporary composition canvases are released on failure/abort; stale UI jobs are aborted/token-guarded. Atlas/PNG owners retain only bounded completed resources.

New sparse asset directory is about4.4MiB on disk; that is compressed/source size, not total decoded memory. No12-base preload or huge prebuilt permutation atlas is introduced. Existing world chunk cache/budget is unchanged.

## Renderer and mobile status

Canvas native gameplay and actual SwiftShader WebGL upload/render smoke both passed independent native pixel readback. [WebGL evidence](webgl-evidence.json) explicitly identifies software rendering; observed cadence there is not hardware FPS. No GPU, thermal, sustained Android/iPhone memory or performance acceptance is claimed.

667×375 and844×390 landscape browser checks confirm native96×112 preview, reachable primary controls, no horizontal overflow and isolated touch gestures. Action selection collapses to a44px native control on small screens; it does not change the gameplay camera. Physical Android Chrome/iPhone Safari remain NOT TESTED. [Device handoff](DEVICE_REVIEW.md).
''')
put('PROTECTED_AUDIT.md',f'''# Protected baseline audit

PASS: {audit['frozenAssetFiles']} approved art/source files and{len(audit['unchangedRuntimeFiles'])} protected runtime files unchanged. Exact approved commit `{approved}`. Permanent non-overwritten approval reference `{approval}`. [Full baseline SHA256 manifest](approved-baseline.json), [audit results](protected-audit.json).

| Character | Approved native atlas SHA256 |
|---|---|
'''+''.join('| '+id+' | `'+h+'` |\n'for id,h in audit['baseAtlases'].items())+'''
Default atlases, animation configuration/order, native anchors, gait speeds, identities and historical source/tools are exact. Walk-front hotfix and approved walk-right are untouched. Old10 cosmetic sources/catalog remain immutable; current derived revisions live under `public/assets/cosmetics/phase2c` with explicit provenance. World pixels, physical/contact collision, camera/tour, controller/manager, state and scene transitions are unchanged.

Authorized code changes are restricted to existing Studio/preferences/cosmetic renderer/types/localization plus a new SHA256 utility. Tests were extended for the newly authorized scope; no test was removed/skipped or historical art validator weakened. Old tests that asserted no wardrobe for the new6 were updated to assert real compatible items; frozen runtime/controller source protections remain exact. The missing-art test now asserts recovered default state rather than a transient optimistic selection.

Reproduce: `python3 tools/phase2c/protected.py`. Baseline hash list never changes to accommodate work. No main merge, history rewrite, historical tag overwrite, learning-site modification or deployment. Publication verifies all pre-existing remote references unchanged.
''')
put('VISUAL_REVIEW.md','''# Human visual review

[Accessible HTML gallery](REVIEW.html) · [actual12 default/custom native](twelve-default-fashion-native.png) · [2× nearest enlargement](twelve-default-fashion-review-2x.png) · [18 source design cards](eighteen-catalog-source-native.png).

All actual native crops are96×112, unresampled. Larger sheets assemble those crops at1:1;2× review copies use nearest-neighbor only and are clearly named. JPEGs are UI/layout evidence and MP4s are lossy timing evidence; neither replaces native PNG inspection. Full native game screenshots for all12 are retained in gameplay/ with `-phaser-native.png` names. Source-only before/after and Juni phase sheets are explicitly labeled; they are not presented as gameplay.

Review the12 curated looks through front/back/left/right idle, walk, run, wave and celebrate. Check bob/long-hair/head attachment, front-hand occlusion, wrap collar and goreum readability, skirt depth over lifted shoes, cap/hat edges, bags turning with the torso and glasses intentionally hidden from behind. Compare actual default front/right videos with customized videos; no base gait was changed.

Original10 foundation evidence precedes expansion; new first3-item Juni/Sori pilot was inspected before remaining recipes. During QA we corrected raised-pose shirt leakage, head-search limits, foreground hand ownership, hair ornament placement near the face, hat/hair clearance and festival lifted-shoe depth. All corrected pixels are additive derived cosmetics; original sources remain untouched.

Current status: TECHNICAL PASS — ARTISTIC APPROVAL PENDING. No human has accepted these18 designs yet. Historical Forge/run-flight warnings remain recorded in earlier reports; automated pixel/alpha coverage is not anatomy or artistic proof. Physical devices and hardware performance NOT TESTED. Human review may still identify garment silhouette, palette or attachment refinements.

UI evidence: [full12 gallery](studio-full-gallery.jpg), [hair](studio-hairstyle.jpg), [outfit](studio-outfit.jpg), [accessory](studio-accessory.jpg), [preset management](preset-management-desktop.jpg), [667×375](studio-667x375.jpg), [844×390](studio-844x390.jpg).

All12 customized gameplay videos,12 default comparison videos and real preset/stress workflow are linked in the gallery. Raw recordings are real input in the canonical world; transcoding preserves dimensions and timing. See [media provenance](media-provenance.json). No static animation is substituted for gameplay.

STOP: review the playable package and provide human Phase2C artistic acceptance before Phase3. No main merge or deployment.
''')
# Generated final QA uses actual test result counters; never hard-codes a running suite as PASS.
e2e=D/'e2e/e2e-results.json';stats=json.loads(e2e.read_text()).get('stats',{})if e2e.exists()else{}
status='PASS'if stats.get('expected')==53 and stats.get('unexpected')==0 and stats.get('skipped')==0 else'PENDING'
put('QA.md',f'''# Phase2C QA

TECHNICAL PASS — ARTISTIC APPROVAL PENDING. Final full E2E status: {status}; actual report counters `{json.dumps(stats,ensure_ascii=False)}`. Re-run this generator after the suite completes; do not treat a running suite as PASS.

| Area | Result | Evidence / limit |
|---|---|---|
| Typecheck |PASS| npm run typecheck |
| Asset preservation/validation |PASS| npm run assets:check; protected audit5453files |
| Lint /format |PASS| npm run lint /npm run format:check |
| Unit |PASS|116tests /17files,0skipped |
| Full E2E |{status}|53tests, original suites plus7new Phase2C cases |
| Production /portable build |PASS|npm run build; separate relative-base Vite artifact |
| Original10 foundation |PASS technical|196 actual native captures,0mismatch |
| New pilot |PASS technical|28 actual clips,0mismatch |
| Final all12 looks/defaults |PASS technical|192 native captures,0mismatch |
| Catalog and exhaustive source composition |PASS technical|28items /46variants /5248registeredcells;192looks /21760frames |
| Actual WebGL native readback |PASS software smoke|SwiftShader; not hardware performance |
| Long session |PASS observed|60actualswitches,100preview/apply,one sprite,bounded caches |
| Persistence /migration /reset /cancel |PASS|v1/v2 readable,local presets+world/visited/progress retained |
| Mobile landscape browser |PASS layout/input|667×375,844×390; native preview+touch isolation |
| Independent ZIP |See package-proof/package-smoke|CRC/SHA+extracted runtime validation required |
| Native art and animation aesthetics |PENDING human|No technical result grants artistic approval |
| Android Chrome /iPhone Safari physical |NOT TESTED|No recorded physical-device evidence |
| GPU/thermal/sustained mobile memory |NOT TESTED|No hardware certification |
| Historical Forge motion warnings |WARN retained|Earlier Phase2A/B reports not rewritten or weakened |

The first full E2E run was52PASS/1FAIL: a missing-texture test waited for an optimistic selected button after the app had already correctly recovered defaults. The test was corrected to assert recovered default selection, one player, unchanged position and original atlas; final complete suite rerun is recorded separately. No retry/skip hides that failure. See logs/e2e-first-run.log and final logs.

[Source QA](source-qa.json) · [protected](protected-audit.json) · [foundation](foundation-gate.json) · [pixel readbacks](gameplay/native-pixel-qa.json) · [UI geometry](ui-probe.json) · [long session](long-session.json) · [WebGL](webgl-evidence.json) · [performance](PERFORMANCE.md) · [device workflow](DEVICE_REVIEW.md).

All12 approved base assets, animations, world/collision/controller/camera/tour remain immutable. Bakery and earlier world planning/performance decisions are not resolved or altered by this character-only phase. No economy, NPC, quest, learning integration, paid API, Phase3, main merge or public deployment.
''')
print('Required8 Phase2C docs written; fullE2E:',status)
