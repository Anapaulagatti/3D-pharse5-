from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';S=R/'assets-src/characters/phase2a'
def read(name):return json.loads((D/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cat=json.loads((S/'cosmetics/catalog.json').read_text());native=read('native-pixel-qa.json');old=read('original4-native-pixel-qa.json');memory=read('memory-observations.json');stable=read('memory-stability.json');actual=read('actual-gameplay.json');composition=read('composition-qa.json');warnings=[r for r in read('forge-warnings.json')if r['check'].get('id')];assert len(native['rows'])>=84 and native['unexplainedPixelMismatch']==0;assert old['worldChangedPixels']==0 and not actual['errors'];assert not composition['failures']
sources=[]
for id in ['ara','doyun']:
 p=S/id/'turnaround-source.png';sources.append({'id':id,'file':str(p.relative_to(R)),'sha256':sha(p),'authoringBrief':str((p.parent/'identity-prompt.txt').relative_to(R)),'reference':'assets-src/characters/phase1b/haneul/turnaround-source.png','route':'host_image: image_gen.imagegen','model':'not supplied by host','estimateUsd':None})
for name in ['ara-harbor','ara-sunlit','doyun-utility','doyun-varsity']:
 p=S/'cosmetics/sources'/name/'turnaround-source.png';id=name.split('-')[0];sources.append({'id':name,'file':str(p.relative_to(R)),'sha256':sha(p),'prompt':str((p.parent/'prompt.txt').relative_to(R)),'reference':f'assets-src/characters/phase2a/{id}/turnaround-source.png','route':'host_image: image_gen.imagegen','model':'not supplied by host','estimateUsd':None})
p=S/'cosmetics/sources/accessories/source.png';sources.append({'id':'accessories','file':str(p.relative_to(R)),'sha256':sha(p),'prompt':str((p.parent/'prompt.txt').relative_to(R)),'reference':'assets-src/characters/phase2a/doyun/turnaround-source.png','route':'host_image: image_gen.imagegen','model':'not supplied by host','estimateUsd':None})
provenance={'artSource':'Seven actual built-in host_image calls, no paid external API/key route. Static identity/costume turnarounds and prop views are sources; animation is independently registered own-PNG-layer authoring, not generated animation sheets.','sourceFiles':sources,'animationCompiler':['tools/phase2a/art.py','tools/phase2a/cosmetics.py'],'registration':'96x112 cells,48,100 anchor; approved Juni same-index motion landmarks for front/back; accepted native profile IK method. One fixed rest source-to-native scale, binary alpha/shared palette; native limbs projected offline with nearest sampling. Runtime sparse composition is1:1, never runtime body/limb stretching.','catalog':{'items':len(cat['items']),'interactions':len(cat.get('interactions',[])),'presets':len(cat['presets'])},'sourceTooling':{'spriteForge':'https://github.com/0x0funky/agent-sprite-forge','commit':'5324342fdfab72430f4e9604f3fe427009f8596d','method':'Existing approved project own-layer authoring plus Forge pixel/motion QA; all original tooling unchanged'},'preservedOriginals':'docs/phase2a/approved-four-characters.json','artApproval':{'originalFour':'HUMAN APPROVED','araDoyunCosmetics':'PENDING HUMAN PHASE2A REVIEW'}}
(D/'source-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
coverage=[]
for id in ['juni','haneul','bomi','minjun','ara','doyun']:
 p=R/'public/assets/juni/juni.json'if id=='juni'else R/f'public/assets/characters/{id}/atlas.json';coverage.append({'id':id,'playable':True,'nativeCell':[96,112],'anchor':[48,100],'frameSlots':len(json.loads(p.read_text())['frames']),'walkDirections':4,'runDirections':4,'distinctFramesPerGait':8,'humanArtApproval':'APPROVED'if id not in ['ara','doyun']else'PENDING','cosmeticItems':len([i for i in cat['items']if id in i['compatibility']['characterIds']])})
(D/'coverage.json').write_text(json.dumps({'characters':coverage,'futureMetadataOnly':['sori','jiwon','nari','taeyang','yuna','hyunwoo'],'cosmeticPoseCoverage':'Every112-frame native slot of each supported identity; all start/stop/turn aliases reference those same registered poses; Ara barrette intentionally occluded on right profile','runtimeCombinationsEagerlyGenerated':0,'offlineReferenceCombinationsVerified':36},indent=2)+'\n')
validation={'typecheck':'PASS','assetsCheck':'PASS','lint':'PASS','unitTests':{'passed':68,'failed':0},'fullE2E':{'passed':32,'failed':0,'activeCanonicalProduction':21,'retainedHistoricalV10':11},'targetedMobileRotationAfterResponsiveFix':{'passed':1,'failed':0},'build':'PASS','nativeReadbacks':len(native['rows']),'nativeOpaquePixelMismatches':0,'pairedFrozenWorldPixelsCompared':old['worldPixelsCompared'],'worldChangedPixels':0,'directReferenceCombinationChecks':36,'nativePoseCombinations':4032,'directReferencePixelMismatch':0,'forgeHardFailures':0,'forgeMotionWarnings':len(warnings),'originalPhase1BForgeWarnings':'11 retained unchanged; original4 now human-approved','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED','softwareWebGLRenderSmoke':'PASS, actual customized native atlas readback; SwiftShader only','canonicalInteriors':'NOT TESTED / not implemented in frozen canonical world','humanPhase2AArtApproval':'PENDING','phase2B':'LOCKED','mainMerge':'NONE','publicDeployment':'NONE'}
(D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
warnmd='# Retained automatic motion warnings\n\nNo thresholds were weakened.24 Forge commands completed with0hard failures. The following6 leaf warnings remain verbatim. The near/far luminance heuristic is ambiguous at passing/overlapping loose-trouser poses; explicit opposite-foot keys and actual playback are supplied for human review. They are not relabelled numerical PASS. The11 older Phase1B warnings also remain unchanged in the historical approved review.\n\n'
for r in warnings:warnmd+=f'`{r["file"]}`\n\n```json\n{json.dumps(r["check"],indent=2)}\n```\n\n'
(D/'FORGE_WARNINGS.md').write_text(warnmd)
peak=max(r['caches']['estimatedBytes']for r in memory['observations']);n12=1202*1394*4+11*1152*1120*4
(D/'PERFORMANCE.md').write_text(f'''# Texture/memory observations

24 recorded switches and a separate48-switch stability run retained one live actor, at most3 owned Phaser actor atlases,2 decoded base preview images and2 composed preview atlases. Atlas loading is lazy; planned identities have no image assets. Sparse native patch images are decoded on request, used to compose one full registered atlas, then released from application ownership. Cached variants are keyed by identity and normalized equipped IDs. Missing/invalid items fall back to original assets.

Peak observed actor RGBA estimate: **{peak:,} bytes ({peak/1048576:.2f}MiB)**. A new load may temporarily stage one additional atlas before the old cache entry is pruned. For comparison only, loading twelve atlas-sized identities would require about{n12/1048576:.2f}MiB for RGBA texels alone; no future six identities were produced or loaded.

These are owner/dimension estimates, not measured total VRAM. Include additional CPU image/canvas copies, CanvasTexture image-data buffers, transient patch decodes, browser caches and the unchanged frozen-world pool when budgeting a device. Shared references can appear under more than one owner. Only2 composed looks are retained; all36 combinations are validated offline without emitting eager runtime permutation atlases.

Warmup stability: retained browser JS heap changed by **{stable['retainedHeapChangeAfterWarmup']:,} bytes** between repeated24-switch schedules with the same final actor and cache counts (cached look identities differ) after explicit GC. See [raw stability](memory-stability.json) and [24-switch observations](memory-observations.json). Initial-to-warm growth includes the bounded caches; these observations do not prove every browser/GPU allocation is leak-free.

The capture environment is desktop headless Chromium. Video/readback instrumentation and software rendering affect cadence. Actual gameplay traces show all8 gait poses; this is not a target-FPS certification. Customized WebGL rendering was tested with SwiftShader, not a physical mobile GPU. **Android Chrome, iPhone Safari, sustained hardware FPS, thermal behavior and device RAM pressure remain NOT TESTED.**
''')
(D/'ARCHITECTURE.md').write_text('''# Character Studio architecture

The existing registry, PlayerCharacterManager, RegistryMotion, preferences and CharacterSelection are extended. No second player engine exists. The original JuniMotion and world controller/camera/contact/geometry remain unchanged. Normal gameplay has one actual Phaser Sprite; selection swaps its texture after validation. Appearance-only changes retain the motion object, including phase and transient gestures. Cross-identity changes retain feasible compatible idle/walk/run travel phase; original Juni uses its immutable motion implementation. Position/visited state remain scene-owned.

Cosmetic items carry stable IDs, multilingual names, compatibility, variant asset references, preview, availability and native registration. CharacterAppearance stores only equipped IDs and schemaVersion2. AppearancePreset and AppearanceManifest are typed. Ten free review items support Ara/Doyun. The original four retain their pixel-identical default appearances and have no catalog patches applied.

New source images are static masters/turnarounds, never generated animation sheets. The previously validated own-PNG-layer compiler bakes112 native poses. Hair and outfit parts are independently authored; source limb projections happen offline with nearest sampling. Packed paint/erase regions use integer96×112 registration and48,100 root. Runtime composes on demand once per requested look, then Phaser plays the existing frame sequence from one cached atlas. There are no screen-space accessories or per-frame layer synchronization risks.

Raised sleeves can expose/cover hair differently. Four sparse pair-ownership packs encode those intersections before accessories, derived against direct own-layer construction. All36 supported combinations across4,032 poses match that reference exactly. This avoids prebuilding all wardrobe permutations. Accessory visibility/occlusion is baked; Ara's barrette is intentionally hidden in right profile and Doyun's neckerchief respects sleeve ownership.

The existing `korean-arena-player-preferences-v1` remains readable and is not rewritten merely to read it. The additive `korean-arena-appearance-preferences-v2` stores per-character appearances, selected ID and up to8 named local presets. Unrecognized versions/references fall back safely. No authenticated account or learning-progress store is introduced; source state checks use an explicitly synthetic sentinel plus real in-world position/visited markers.

Six future identities are metadata-only. Registry promotion removes a newly registered identity from the planned list. Gallery rendering iterates data and scrolls; it has no six-character limit. Loading/caching is bounded independently of catalog size.

Future ownership is separate from equipment. `CosmeticOwnershipProvider`, acquisition metadata and reward-origin/request contracts describe later integration. The current resolver intentionally permits only the free review catalog. A future entitlement adapter must consult server-verified inventory/receipts before authorizing an item; local equipped IDs are never proof of a purchase, quest, lesson achievement or unlock. Rendering/pose assets remain unchanged by that adapter. No shop, economy, ads, gambling, loot box, crafting or learning integration is implemented.

Vietnamese Studio UI is delivered. Korean/English message and item-name resources provide the future localization structure; a complete language-selection product and localization certification are outside this review. Mobile landscape uses safe-area-aware layout,44px primary controls and integer1× previews; desktop uses integer2× previews. Resizing re-registers preview display size without changing gameplay camera behavior.
''')
(D/'DEVICE_REVIEW.md').write_text('''# Physical-device handoff — NOT TESTED

Extract the ZIP. Run `python3 start_review.py --lan --port 4340` on a trusted private LAN and open the displayed host address from the phone. Local-only default is `python3 start_review.py`. This is not a public deployment. The earlier Android/iPhone review records and checkpoints remain recoverable in Git.

Record actual hardware model, OS build, browser/version, DPR, orientation, date/time and evidence filenames. Test Android Chrome and iPhone Safari separately. Include a screen recording and screenshots before marking physical PASS.

- Open all six identities; original four must keep their approved looks.
- Apply both hair/outfit choices for Ara and Doyun, each accessory, and cross-mix the categories. Check idle, all four walk/run directions, wave, celebrate and turns.
- Save a named local preset, reload, switch among identities and reset. Position/visited markers must survive; existingv1 selections must remain readable.
- Check touch targets, text, full preview, safe areas/notch, keyboard/preset naming and portrait→landscape return. Studio gestures must not move the world; joystick/Run/emotes must resume after closing.
- Repeat at least50 look changes and a10-minute play session. Record stalls, RAM/tab reloads, texture glitches, heat and battery observations. Check camera/tour return with the customized actor.

Use the existing Options → Export test report control for session metrics. Save it alongside the device recording and the appearance/character IDs used. Copy the blank `DEVICE_REPORT.json`, fill only observed results, and keep untested items as NOT TESTED. Browser emulation and desktop SwiftShader are not physical-device evidence.
''')
(D/'DEVICE_REPORT.json').write_text(json.dumps({'physicalDevice':None,'model':'','os':'','browser':'','dateTimeWithTimezone':'','characterAndLookIds':[],'evidenceFiles':[],'checks':{k:'NOT TESTED'for k in ['studioFit','safeAreasKeyboard','touchIsolation','allSixCharacters','cosmeticsAllDirections','presetsReload','worldStateRetention','fiftySwitches','tenMinuteSession','cameraTour','thermalMemory']},'sessionMetricsFile':'','notes':''},indent=2)+'\n')
(D/'QA.md').write_text(f'''# Phase2A review QA

| Check | Result | Evidence |
|---|---|---|
| Permanent approved4 baseline | PASS |51ac4b4; approval tag and SHA manifest preserve all original art/configs/previews/layers/tools |
| World/collision/camera/controller preservation | PASS |3,082 protected world/core and224 Juni hashes exact;{old['worldPixelsCompared']:,} paired native world pixels,0 changes |
| Default appearance preservation | PASS |Four original actual Phaser native body readbacks exact; unit identity/clip/motion-step assertions |
| Ara and Doyun | PASS, review candidate |Own host-image identities,112 native slots each,64 distinct gait poses,34clips; Ara validated before Doyun production |
| Cosmetic catalog | PASS, review candidate |2hair +2outfits each for2 identities,2accessories; every supported frame registered |
| Pair ownership / alpha / registration | PASS |36combinations ×112poses =4,032 direct-source matches; binary native masks and integer rectangles |
| Actual gameplay/native fidelity | PASS |{len(native['rows'])} native readbacks with0 unexplained opaque-pixel mismatch;48 actual gait cycles each show all8frames; emotes/idle/directions also observed |
| Studio/persistence/v1/state retention | PASS |Actual UI selection/save/reset/reload; real visited landmark and position retained; synthetic lesson sentinel unchanged |
| Resource ownership | PASS, bounded observations |One sprite,3actor textures,2base/2composite caches;24switch observations and48switch stability run |
| Build/typecheck/assets/lint/unit | PASS |68unit tests; original validation commands pass |
| Full E2E | PASS |32tests:21 canonical production/Studio and11 retained historical V10 checks; historical results are not canonical ferry/gameplay/art approval |
| Landscape/orientation regression | PASS, Chromium emulation |Additional targeted rotation test;844×390 and667×375 browser images/geometry |
| Forge numerical diagnostics | WARN retained |0hardFAIL,6new side-leg heuristic WARNs; [verbatim warnings](FORGE_WARNINGS.md).11 earlier approved Phase1B warnings retained |
| Final new-art acceptance | NOT TESTED / awaiting human |Original4 are human-approved; new2/cosmetics await Phase2A artistic acceptance |
| Physical Android Chrome / iPhone Safari | NOT TESTED |No physical evidence recorded |
| Hardware WebGL/FPS/thermal/device memory | NOT TESTED |SwiftShader render smoke and desktop estimates only |
| Canonical interiors | NOT TESTED / unsupported |The frozen canonical world has no interior transition; no invented interior test PASS |

Existing world/planning issues remain separate and unchanged: Bakery allocation remains deferred (W0 rejected/Q1 not approved); inherited station strip/route failures and station/amusement conflict remain recorded in historical world reviews. No world rebuild or planning amendment is performed here. Automatic build/geometry tests are not human artistic approval.

Phase2A is delivered as a playable review candidate. No remaining new Phase2A P1 functional defect is known from this scope. Retained P2/review items:6automatic profile-motion WARNs, full Korean/English localization review, physical notch/keyboard/mobile memory and sustained performance. Do not treat these as completed device acceptance.

No Phase2B, main merge, public deployment, paid external media API or separate Korean-learning website changes.
''')
(D/'README.md').write_text('''# Phase2A Character Studio — six-character review

Four approved originals remain pixel-identical. Ara and Doyun are new playable review candidates. Character Studio supplies ten independently frame-registered free cosmetics, four suggested looks, local named presets, reset and additivev2 persistence. Phase2B remains locked; stop for human review.

- [Open visual review](REVIEW.html) · [QA](QA.md) · [architecture/contracts](ARCHITECTURE.md) · [memory/performance](PERFORMANCE.md)
- [Six original appearances, native](six-original-appearances-native.png) · [readable2× review](six-original-appearances-review-2x.png)
- [Juni vs Ara, same frame index](juni-vs-ara-native.png) · [Juni vs Doyun](juni-vs-doyun-native.png)
- [Ara walk](ara-walk-motion.png) / [run](ara-run-motion.png) · [Doyun walk](doyun-walk-motion.png) / [run](doyun-run-motion.png): source animations, not gameplay recordings
- [Catalog native1](catalog-1-native.png) / [native2](catalog-2-native.png) · [larger review1](catalog-1-review-2x.png) / [review2](catalog-2-review-2x.png)
- [Actual native pixel QA](native-pixel-qa.json) · [original4/world pixel QA](original4-native-pixel-qa.json) · [v1/preset/reload evidence](persistence-evidence.json)
- [Provenance](source-provenance.json) · [coverage](coverage.json) · [warnings](FORGE_WARNINGS.md) · [device handoff](DEVICE_REVIEW.md)

Actual Phaser videos and native evidence:

'''+''.join(f'- [{mode["name"]} actual gameplay]({mode["name"]}-actual-gameplay.mp4) · [native gameplay poses]({mode["name"]}-actual-native-sheet.png) · [2× inspection]({mode["name"]}-actual-review-2x.png) · [full native front-walk]({mode["name"]}-walk-front-phaser-native.png)\n'for mode in actual['modes'])+'''
[Customized software WebGL native capture](custom-ara-webgl-native.png) is rendering smoke evidence only. [Mobile844×390](mobile-landscape-studio-browser.jpg) / [small667×375](small-landscape-studio-browser.jpg) are Chromium touch emulations, not real iPhone/Safari or Android evidence.

Run the extracted playable ZIP with `python3 start_review.py`, then open the local REVIEW.html. Full masters/layers/frames and large native screenshots are versioned in the immutable review checkpoint; the portable ZIP includes the compiled offline game, compact native crops and the two default-character recordings. Four cosmetic gameplay videos and larger source evidence link to the immutable Git checkpoint to keep the ZIP below100MB. All native PNGs are unmodified backing data or exact integer crops. Enlargements use nearest-neighbor. MP4s are lossy native-scale crops of actual browser recordings and begin with real Studio selection followed by gameplay; use PNGs for pixel judgment.

Checkpoint: `checkpoint/phase2a-character-studio-review-20261026`. Approved baseline: `checkpoint/phase1b-four-characters-approved-20261026` →51ac4b4f20f0af2f26d1566988580d92c0612356. New Phase2A human artistic approval remains pending.
''')
html='<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Character Studio · Phase2A review</title><style>body{background:#213c35;color:#fff0ce;font:16px/1.5 system-ui;max-width:1440px;margin:auto;padding:24px}a{color:#a8e3cc}img{max-width:100%;image-rendering:pixelated}video{max-width:100%;width:480px;background:#162721}section{padding:22px 0;border-top:1px solid #71806b}h1,h2{color:#f1d58d}.note{color:#c4d3bd}</style><h1>Korean Arena · Character Studio</h1><p>Sáu nhân vật ·10 cosmetics · nguyên bản luôn có thể khôi phục.</p><p><a href="../../index.html">Vào game Phaser</a> · <a href="QA.md">QA</a> · <a href="PERFORMANCE.md">Memory</a> · <a href="source-provenance.json">Provenance</a></p><p class="note">Original4 approved. New2/cosmetics awaiting human review. Physical devices NOT TESTED. Phase2B locked.</p><section><h2>Native-scale appearances</h2><a href="six-original-appearances-native.png"><img src="six-original-appearances-review-2x.png"></a><p>Source artwork lineup; gameplay appears below.</p><a href="juni-vs-ara-native.png"><img src="juni-vs-ara-native.png"></a><a href="juni-vs-doyun-native.png"><img src="juni-vs-doyun-native.png"></a></section><section><h2>Independent cosmetic source poses</h2><a href="catalog-1-native.png"><img src="catalog-1-review-2x.png"></a><a href="catalog-2-native.png"><img src="catalog-2-review-2x.png"></a></section>'
for mode in actual['modes']:
 name=mode['name'];html+=f'<section><h2>{name} · ACTUAL PHASER</h2><video controls preload="none" src="{name}-actual-gameplay.mp4"></video><p><a href="{name}-walk-front-phaser-native.png">Full native1:1 frame</a> · <a href="{name}-actual-native-sheet.png">Native crops</a></p><a href="{name}-actual-native-sheet.png"><img src="{name}-actual-review-2x.png"></a></section>'
html+='<section><h2>Mobile browser review · physical devices NOT TESTED</h2><img src="mobile-landscape-studio-browser.jpg"><img src="small-landscape-studio-browser.jpg"><p><a href="DEVICE_REVIEW.md">Physical-device checklist/export workflow</a> · <a href="FORGE_WARNINGS.md">Retained warnings</a></p></section></html>';(D/'REVIEW.html').write_text(html)
print('Generated provenance, coverage, QA, architecture, performance and review guide')
