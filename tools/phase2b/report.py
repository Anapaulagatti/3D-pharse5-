from pathlib import Path
import json,hashlib,collections,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b';ids=['sori','jiwon','nari','taeyang','yuna','hyunwoo'];old=['juni','haneul','bomi','minjun','ara','doyun']
def read(n):return json.loads((D/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=read('native-pixel-qa.json');reg=read('approved-six-native-pixel-qa.json');memory=read('memory-stability.json');warnings=read('forge-warnings.json');protected=read('protected-audit.json');commands=read('validation-commands.json');bridge=read('bridge-regression/body-clearance.json')
assert native['captures']==85 and native['unexplainedPixelMismatch']==0 and reg['worldChangedPixels']==0
assert all(r['result']=='PASS'for r in commands)
assert all(s['representativeTraversal']=='PASS'for s in bridge['summary'].values())
assert '40 passed' in Path('/tmp/phase2b-e2e.log').read_text()
sources=[];files={}
for id in ids:
 root=R/f'assets-src/characters/phase2b/{id}';sources.append({'id':id,'master':str((root/'turnaround-source.png').relative_to(R)),'masterSHA256':sha(root/'turnaround-source.png'),'prompt':str((root/'identity-prompt.txt').relative_to(R)),'promptSHA256':sha(root/'identity-prompt.txt'),'art_source':'host_image','route':'image_gen.imagegen','model':'not supplied by host','estimateUsd':None,'styleReference':'assets-src/characters/phase1b/haneul/turnaround-source.png','identitySource':'Own independently generated four-direction static turnaround, not a generated animation sheet or recolor','nativeFrames':112,'coreClips':34,'runtimeAlias':'social-front maps to the8 wave/greeting poses;35 runtime clip keys, no extra native frames','movement':{'walk':60,'run':100,'walkStride':44,'runStride':64},'native':[96,112],'anchor':[48,100]})
 for p in list(root.rglob('*'))+list((R/f'public/assets/characters/{id}').rglob('*')):
  if p.is_file():files[str(p.relative_to(R))]=sha(p)
for p in (R/'tools/phase2b').glob('*'):
 if p.is_file():files[str(p.relative_to(R))]=sha(p)
(D/'source-provenance.json').write_text(json.dumps({'sourceCalls':6,'sources':sources,'pipeline':'Existing accepted Phase2A native own-PNG-layer pipeline. One fixed source-to-native area reduction and shared96-color binary-alpha finish per identity, offline nearest limb projection and approved Juni same-index front/back motion landmarks. Phase2B profile forearms corrected to oppose their near leg. One native atlas in actual gameplay; no runtime skeleton or loose accessories.','spriteForge':{'repository':'https://github.com/0x0funky/agent-sprite-forge','commit':'5324342fdfab72430f4e9604f3fe427009f8596d','doctor':'forge-doctor.json','commands':72},'approvedSources':'Unchanged, approved-six.json and protected-audit.json','files':files,'finalHumanArtApproval':'PENDING'},indent=2)+'\n')
coverage=[{'id':id,'status':'PLAYABLE','humanArtApproval':'APPROVED_PHASE2A','defaultAssets':'IMMUTABLE'}for id in old]+[{'id':id,'status':'PLAYABLE_REVIEW_CANDIDATE','humanArtApproval':'PENDING','nativeFrames':112,'authoredClips':34,'runtimeClipKeys':35,'fourDirectionGaits':8,'distinctFramesPerGait':8,'actualEightFrameGaitCycles':8,'wardrobe':'DEFAULT_ONLY; existing incompatible items hidden'}for id in ids]
(D/'coverage.json').write_text(json.dumps({'characters':coverage,'playable':12,'plannedOnlyRemaining':0,'newCosmetics':0,'approvedCosmeticsPreserved':10,'suggestedLooksPreserved':4},indent=2)+'\n')
peak=max(s['cache']['estimatedBytes']for s in memory['samples']);warncounts=collections.Counter(r['check']['id']for r in warnings['warnings']);contacts=sum(s['sampledNativeContacts']for s in bridge['summary'].values())
validation={'requiredCommands':commands+[{'name':'test:e2e','result':'PASS','passed':40,'failed':0,'canonicalWorldStudio':29,'retainedHistoricalV10':11}], 'unitPassed':85,'nativeCaptures':85,'nativePixelMismatch':0,'worldNativePixelsCompared':reg['worldPixelsCompared'],'worldChangedPixels':0,'originalNativeBodyReadbacks':6,'sixtySwitches':'PASS','bridgeRepresentatives':{'A':'Nari,walk,out/return','B':'Hyunwoo,run,out/return','samples':contacts,'unsupportedFootSamples':0},'forgeHardFailures':0,'newForgeWarnings':dict(warncounts),'historicalWarningsRetained':17,'hardwareWebGLPerformance':'NOT TESTED','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','humanArtApproval':'PENDING','phase2C':'LOCKED','mainMerge':'NONE','publicDeployment':'NONE'}
(D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
(D/'PERFORMANCE.md').write_text(f'''# Performance and cache observations

Actual production-browser observations cover initial load, all12 gallery previews,60 committed identity switches (five complete rotations), gameplay, reload and Studio reopen. One live player Sprite persisted. The existing limits remained:3 Phaser actor atlases (+1 temporary staging load),2 decoded base preview atlases and2 composed cosmetic atlases. Twelve-card portraits are small separately lazy-loaded PNGs; only the selected preview loads a full atlas. The initial world requested only Juni's full atlas, not all12.

Peak observed actor RGBA estimate: **{peak:,} bytes ({peak/1048576:.2f}MiB)**. These are dimensions/owner counts, not total VRAM. Include CPU decoded image copies, canvas buffers, browser caches and the unchanged world pool in a real-device budget. A temporary incoming atlas can coexist before LRU eviction. The unchanged compositor remains lazy/bounded; no wardrobe permutations were eagerly built.

Retained browser JS heap changed by **{memory['retainedHeapDelta36To60']:,} bytes** between switch36 and60 after explicit GC. This observational growth includes whole-app state; it is not a zero-growth claim or hardware leak certification. [Raw stages and counts](memory-stability.json) include preserved old Ara preset data before/after reload.

Six new canonical station tests, mobile joystick and the two representative bridge traversals use the actual game. [BridgeA](bridge-regression/body-clearance.json) was walked by Nari out/return; bridgeB was run by Hyunwoo out/return. No speed, camera, collision or position override was used. All12 were switched through the real Studio UI. These are functional observations, not sustained target-FPS certification.

Native WebGL was exercised with desktop SwiftShader. **Physical Android Chrome, iPhone Safari, hardware WebGL FPS, thermal behavior and real device RAM pressure remain NOT TESTED.** The world/camera/tour implementations are unchanged. No unverified physical-device PASS is claimed.
''')
checks=protected['checks'];(D/'PROTECTED_AUDIT.md').write_text('''# Approved asset/runtime preservation

Approved Phase2A complete commit: `ed75734d0e0865274ca0b82bab2495d78878d24b`. Approval tag: `checkpoint/phase2a-six-characters-approved-20261026`. Branch starts exactly there; original Phase2A branch/checkpoints remain unchanged.

| Manifest | Files verified | Changed |
|---|---:|---:|
'''+''.join(f'| `{r["manifest"]}` |{r["verifiedFiles"]}|{len(r["changed"])}|\n'for r in checks)+f'''
The15 approved character-source snapshots remain exact. Unit tests compare all six identity records, animation definitions, scales, anchors and movement values against frozen source-derived records. The ten cosmetic assets/catalog, four suggested looks and v1/v2 preference implementation are unchanged. Original source layers and animation-generation tools are retained.

Runtime exceptions are limited to data-only new registrations and CharacterSelection's empty-future visibility, selected-card scrolling and neutral default-only caption. No second engine exists. Seven historical capture helpers had pre-existing formatting failures; only whitespace/formatting was normalized, with actual before/after syntax trees and source hashes checked: [normalization audit](formatter-normalization.json). No validator was ignored, weakened or deleted.

Actual native regression compared **{reg['worldPixelsCompared']:,} world pixels,0 changes**, plus six original native actor readbacks with0 unexplained differences. Hanbit Station, Jeju bridges, palace/farm, world collision, main scene, controller, camera and Scenic Tour remain protected. [Source-reference comparison](protected-six-reference-comparison-native.png) is source art; [actual six-character native crops](six-native-gameplay-crops.png) are genuine Phaser captures.

[Machine hash report](protected-audit.json) · [approved six freeze](approved-six.json) · [approved runtime-code freeze](approved-runtime-code.json) · [native regression](approved-six-native-pixel-qa.json).
''')
(D/'QA.md').write_text(f'''# Phase2B — TECHNICAL PASS / ARTISTIC REVIEW PENDING

| Check | Result | Evidence |
|---|---|---|
| Phase2A freeze before production | PASS | Approval tag at ed75734; freeze committed first at44d65a8 |
| Twelve stable free identities | PASS | Six completed packs promoted through existing registry; planned-only list now empty |
| Approved six / wardrobe / world | PASS | Byte-exact source hashes and identity snapshots;0 changed paired world pixels |
| New native packs | PASS, review candidates |6×112 poses,34 authored clips each,8 distinct frames per four-direction walk/run |
| Social compatibility | PASS | One additional runtime `social-front` alias to the8-frame greeting; no extra native frame slots or new input binding |
| Native registration/rendering | PASS |85 actual readbacks,0 opaque-pixel mismatch; integer placement, nearest sampling,96×112/48,100 |
| Locomotion and gestures | PASS, review candidates |48 real gait cycles show all8 frames; idle/wave/celebrate, stop/direction changes and shared native transition graph tested |
| Opposing profile arms | PASS |New six only; forearm-owned pixel changes,0 front/back or outside-owned-region changes; pairs re-recorded after correction |
| Production typecheck/assets/lint/format/unit/build | PASS |85unit tests; [commands/logs](VALIDATION_COMMANDS.md) |
| Full E2E | PASS |40tests:29 canonical production/Studio,11 retained historical V10; historical routes are not evidence of canonical success |
| Existing cosmetics/presets/v1/v2 | PASS |Approved asset/config bytes unchanged; actual existing Studio regressions and old Ara preset retained after60 switches/reload |
| Player/state/cache ownership | PASS, observations |One active Sprite;3 actor/2 base/2 composite cache bounds,60 switches through all12 |
| Working canonical bridges | PASS, representatives |Nari A walk +Hyunwoo B run, both out/return;{contacts:,} sampled native contacts,0 unsupported; correct source-body readbacks |
| Mobile landscape | PASS, Chromium emulation |12-entry scroll gallery,667×375 and844×390, full native preview, touch joystick, orientation/reopen |
| Forge diagnostics | WARN |{len(warnings['warnings'])}new numerical warnings: {dict(warncounts)};0hardFAIL. [Verbatim values/thresholds](FORGE_WARNINGS.md) |
| Physical Android / iPhone | NOT TESTED |No recorded physical-device evidence |
| Hardware FPS/thermal/VRAM | NOT TESTED |Desktop heap/dimension estimates and SwiftShader only |
| Final artistic acceptance | PENDING |No invented human approval for the new six; Phase2C locked |

The initial profile-arm same-phase defect was corrected in the six new packs. Before-correction sources/reports are retained under history and earlier wave checkpoints. Current native/gameplay evidence uses corrected packs. The first bridge recorder used a screenshot-only native mode that hid the joystick; that harness failure is archived. Actual out/return traversal was then recorded with normal controls at zoom1/native backing resolution. No world collision patch was made.

No remaining new P1 functional defect is known in this scope. P2/review items: numerical gait/seam warnings and human review of costume/face/loop quality; physical-device and sustained performance validation. Palette-specific/outline-specific Forge checks were skipped when no matching palette/outline color was supplied, not silently marked PASS.

Inherited map issues remain unchanged and separate: Bakery placement (W0 rejected/Q1 deferred), station strip/route/planning defects and station/amusement conflict. Canonical interiors remain unsupported; no interior transition PASS is invented. No map regeneration, new gameplay systems, learning backend, Phase2C, main merge or public deployment.
''')
(D/'DEVICE_REVIEW.md').write_text('''# Physical-device handoff — NOT TESTED

Extract the ZIP and run `python3 start_review.py` locally. For an actual device on a trusted private LAN, use `python3 start_review.py --lan --port 4341` and open the host LAN address from that phone. This is a private review procedure, not public deployment.

Record model, OS/browser version, DPR, orientation/date, source checkpoint and actual screenshot/video filenames. Test Android Chrome and iPhone Safari separately.

- Browse all12 cards, select the final row, rotate and reopen; check full previews,44px primary actions, safe areas and keyboard.
- Walk/run all four directions for each new identity; inspect start/stop/turn, greeting and celebration, face/costume registration and shadows.
- Apply approved Ara/Doyun looks, preserve named presets, switch through all12 at least60times, reload and verify position/visited markers.
- Test joystick isolation, Run/emotes and Scenic Tour return; walk working bridges, nearby building obstacles and play at least10minutes.
- Record actual stalls, reloads, thermal/RAM/FPS observations. Do not infer PASS from desktop estimates.

Use Options → Export test report for session metrics. Save that export with a filled `DEVICE_REPORT.json`, videos and appearance IDs. Keep unobserved categories NOT TESTED. There is no authenticated account or learning backend in this phase.
''')
(D/'DEVICE_REPORT.json').write_text(json.dumps({'model':'','os':'','browser':'','DPR':None,'checkpoint':'checkpoint/phase2b-twelve-characters-review-20261026','physicalEvidenceFiles':[],'checks':{k:'NOT TESTED'for k in ['allTwelve','newLocomotion','gallerySafeAreas','orientationKeyboard','joystick','presetsReload','sixtySwitches','bridges','tenMinuteSession','thermalMemoryFPS']},'sessionExportFile':''},indent=2)+'\n')
(D/'DEFECT_REGISTER.md').write_text('''# Phase2B remaining review items

| Item | Status | Scope |
|---|---|---|
| New profile arm/leg same phase | RESOLVED |New six only; corrected forearm phase, source pixel isolation and current actual playback verified |
| Native screenshot-mode joystick hidden in first bridge capture | RESOLVED harness issue |Normal-control route recording and source-contact audit pass; old attempt archived |
| New-source human artistic acceptance | PENDING |Six identities, facial/costume appeal and loop feel require human review |
|18 new Forge numerical warnings | WARN / P2 review |11leg auto-luminance +7seam flags; raw thresholds unchanged, internal geometry/playback analysis supplied |
|17 previously approved-roster warnings | RETAINED |Historical11 Phase1B +6 Phase2A diagnostics do not authorize altering approved assets |
| Android Chrome / iPhone Safari hardware | NOT TESTED |Use real-device handoff |
| Sustained hardware performance/thermal | NOT TESTED |Desktop observations are not certification |
| Existing world planning/route issues | INHERITED, UNCHANGED |Bakery unplaced, station strip and station/amusement decisions remain separate |

No new Phase2B P1 functional defect remains known from the executed scope. This statement is not full-world acceptance or Phase2C authorization.
''')
(D/'VALIDATION_COMMANDS.md').write_text('# Executed checks\n\n'+''.join(f'- `{" ".join(r["command"])}` — {r["result"]}, [log]({r["log"]})\n'for r in commands)+'''- `npm run test:e2e` —40PASS, [log](validation-logs/e2e.txt).29 canonical production/Studio checks and11 retained historical V10 checks.\n\nThe final default-only caption removes an inherited approval implication from newly authored characters; targeted Phase2B UI/persistence tests were repeated after rebuilding. See [targeted regression](validation-logs/targeted-final.txt). All gameplay art, renderer and motion bytes stayed equal across that text-only UI change. Extracted package smoke and all-file SHA/CRC verification are supplied separately.\n''')
(D/'VISUAL_REVIEW.md').write_text('''# Phase2B visual review

**Source artwork/comparison boards** are explicitly separated from **actual Phaser captures/videos** below. Native PNGs are authoritative for pixels; MP4 is lossy real browser recording. Review at1:1 before enlarging. Six previously approved identities remain unchanged; the six new identities await human acceptance.

## Source artwork

[All12 side by side, native](twelve-character-lineup-native.png) · [nearest2×](twelve-character-lineup-review-2x.png)

[Protected six, approved/current source pixels](protected-six-reference-comparison-native.png) · [actual six-character Phaser crops](six-native-gameplay-crops.png)

[New profile arm correction before/after, source only](profile-forearm-before-after-source-native.png) · [pixel isolation/phase targets](profile-arm-correction.json). Original approved character pixels were not altered.

'''+''.join(f'''### {id}

Source: [native turnaround]({id}-turnaround-native.png) · [walk vs Juni, all four views] (juni-vs-{id}-walk-native.png) · [run vs Juni, all four views](juni-vs-{id}-run-native.png) · [animated walk]({id}-walk-motion.png) · [animated run]({id}-run-motion.png) · [wave]({id}-wave-motion-native.png) · [celebrate]({id}-celebrate-motion-native.png)

Actual Phaser: [full native1:1]({id}-default-walk-front-phaser-native.png) · [native gameplay poses]({id}-default-actual-native-sheet.png) · [readable2×]({id}-default-actual-review-2x.png) · [actual gameplay video]({id}-default-actual-gameplay.mp4)

'''for id in ids).replace('] (','](')+'''
## Actual canonical world and interface

[New Hyunwoo software WebGL, native](hyunwoo-software-webgl-native.png) · [native pixel QA](native-pixel-qa.json)

[Desktop gallery top](studio-desktop-top.jpg) / [bottom](studio-desktop-bottom.jpg)

[Mobile844×390 top](mobile-844x390-gallery-top.jpg) / [bottom](mobile-844x390-gallery-bottom.jpg) · [small667×375 top](mobile-667x375-gallery-top.jpg) / [bottom](mobile-667x375-gallery-bottom.jpg). These are actual Chromium touch-emulation screenshots, not physical devices or native-art pixel references.

[Actual bridge traversal: Nari A +Hyunwoo B](bridge-regression/world-traversal-review.mp4) · [body/contact audit](bridge-regression/body-clearance.json). Four continuous legs, two explicit initial review spawns, original movement speed/collision/camera. Not every identity/route combination was tested.

[Verbatim retained warnings](FORGE_WARNINGS.md) · [QA](QA.md) · [source provenance and hashes](source-provenance.json) · [performance](PERFORMANCE.md).
''')
(D/'README.md').write_text('''# Phase2B — twelve playable characters

**TECHNICAL PASS / ARTISTIC REVIEW PENDING. Phase2C remains locked.**

Six approved original identities, ten cosmetics and the world stay unchanged. Sori, Jiwon, Nari, Taeyang, Yuna and Hyunwoo add independent native artwork and complete packs through the existing registry/Studio/movement interfaces. No second engine or new wardrobe catalog exists.

- [Visual gallery: native artwork and actual Phaser videos](VISUAL_REVIEW.md) · [browser review page](REVIEW.html)
- [QA](QA.md) · [executed commands](VALIDATION_COMMANDS.md) · [coverage](coverage.json)
- [Protected source/world audit](PROTECTED_AUDIT.md) · [source provenance](source-provenance.json) · [remaining defects](DEFECT_REGISTER.md)
- [Performance/cache observations](PERFORMANCE.md) · [verbatim motion warnings](FORGE_WARNINGS.md) · [real-device handoff](DEVICE_REVIEW.md)
- [Playable ZIP](PHASE2B_TWELVE_CHARACTER_REVIEW.zip) · [package integrity](package-proof.json) · [extracted package gameplay smoke](package-smoke.json)

Extract and run `python3 start_review.py`, then open the local REVIEW.html. The actual compiled game runs offline. The ZIP includes compact native evidence and two gameplay recordings; four further character videos, bridge video, large native images and complete authoring sources link to the immutable review checkpoint to stay below100MB. Original sources/layers/tools and all historical checkpoints are recoverable in Git.

Approved Phase2A: `checkpoint/phase2a-six-characters-approved-20261026` → `ed75734d0e0865274ca0b82bab2495d78878d24b`. Final review: `checkpoint/phase2b-twelve-characters-review-20261026`. Earlier wave checkpoints are retained; current corrected evidence supersedes pre-opposing-arm drafts.

85unit and40full E2E checks pass, plus targeted final UI regression.85 native readbacks have0 mismatched opaque pixels.60 identity switches retain bounded caches, one Sprite and real world state/presets. Numerical motion warnings are retained; physical Android/iPhone and hardware performance remain NOT TESTED.

No Phase2C, main merge, public deployment, map rebuild, new gameplay systems or separate learning-website changes. Stop for human artistic acceptance.
''')
h='<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase2B twelve-character review</title><style>body{background:#213c35;color:#fff0ce;font:16px/1.5 system-ui;max-width:1440px;margin:auto;padding:24px}a{color:#a8e3cc}img{max-width:100%;image-rendering:pixelated}video{max-width:100%;width:480px;background:#162721}section{border-top:1px solid #71806b;padding:20px 0}</style><h1>Korean Arena ·12 nhân vật</h1><p>TECHNICAL PASS / ARTISTIC REVIEW PENDING. Physical devices NOT TESTED. Phase2C locked.</p><p><a href="../../index.html">Vào game Phaser</a> · <a href="QA.md">QA</a> · <a href="VISUAL_REVIEW.md">Native review index</a> · <a href="FORGE_WARNINGS.md">WARN</a></p><section><h2>Source artwork · not gameplay</h2><a href="twelve-character-lineup-native.png"><img src="twelve-character-lineup-review-2x.png"></a><p><a href="protected-six-reference-comparison-native.png">Six approved source comparisons</a></p></section>'
for id in ids:h+=f'<section><h2>{id} · actual Phaser</h2><video controls preload="none" src="{id}-default-actual-gameplay.mp4"></video><p><a href="{id}-default-walk-front-phaser-native.png">Full native1:1</a> · <a href="{id}-default-actual-native-sheet.png">Native crops</a> · <a href="juni-vs-{id}-walk-native.png">Source walk vs Juni</a> · <a href="juni-vs-{id}-run-native.png">Source run vs Juni</a></p><img src="{id}-default-actual-review-2x.png"></section>'
h+='<section><h2>Actual bridge traversal</h2><video controls preload="none" src="bridge-regression/world-traversal-review.mp4"></video><p><a href="bridge-regression/body-clearance.json">Contact audit</a></p></section><section><h2>Studio mobile browser · hardware NOT TESTED</h2><img src="mobile-844x390-gallery-top.jpg"><img src="mobile-844x390-gallery-bottom.jpg"><img src="mobile-667x375-gallery-bottom.jpg"><p><a href="DEVICE_REVIEW.md">Physical-device checklist</a></p></section></html>';(D/'REVIEW.html').write_text(h)
print('Consolidated Phase2B reports generated; human art approval remains pending')
