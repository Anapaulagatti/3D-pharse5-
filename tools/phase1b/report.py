from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';checks=json.loads((D/'checks.json').read_text());assert len(checks)==6 and all(q['status']=='PASS'for q in checks)
bridges=json.loads((D/'bridges-summary.json').read_text());assert len(bridges)==4 and all(q['gameplayExit']==q['contactAuditExit']==0 for q in bridges)
native=json.loads((D/'native-pixel-qa.json').read_text());assert native['worldChangedPixels']==0
proof=json.loads((D/'gameplay-evidence.json').read_text());assert not proof['errors']and len(proof['rows'])==32 and all(len(r['observedFrames'])==8 for r in proof['rows'])
progress=json.loads((D/'progress-switch-refresh.json').read_text());assert len(progress['rows'])==4 and not progress['errors']and all(r['after']['visited']and r['status']=='PASS'for r in progress['rows'])
warn=json.loads((D/'forge-warnings.json').read_text());assert not any(q['check']['status']=='fail'for q in warn)
contacts=[]
for id in ['juni','haneul','bomi','minjun']:
 q=json.loads((D/'bridges'/id/'body-clearance.json').read_text());contacts.append({'id':id,'bridgeA':q['summary']['A'],'bridgeB':q['summary']['B']})
samples=sum(r[k]['sampledNativeContacts']for r in contacts for k in ['bridgeA','bridgeB']);unsupported=sum(r[k]['unsupportedSampleCount']for r in contacts for k in ['bridgeA','bridgeB']);assert unsupported==0
rows=[['Four genuinely playable character packs','PASS','Original Juni144;3new112-slot atlases,64 distinct gait images each.'],['Four-direction walk/run in actual Phaser','PASS','All8 frames of all32 character/action/direction clips observed via real input.'],['Wave / celebrate / start-stop-turn','PASS','Native clips and actual emote recording; turn clips reuse authored directional poses.'],['Selection / switching / one player / persistence','PASS','Real UI switches, saved choice, exact position and nonempty existing visited marker preserved across refresh.'],['Mobile landscape browser input/UI','PASS','Chromium844×390/DPR3 touch emulation, all4 avatars; not physical devices.'],['Both Jeju bridge routes','PASS',f'16out/return legs;{samples} sampled poses,0unsupported contacts; source-body readback exact.'],['World / Juni / collision / camera preservation','PASS',f'3082world and224Juni manifest entries unchanged;{native["worldPixelsCompared"]} paired native world pixels,0changed.'],['Native1:1 rendering and sampling','PASS','Canvas and software-WebGL smoke;4player station readbacks exact, nearest textures/integer native camera.'],['Unit / E2E / build / lint / assets','PASS','50unit tests,23E2E tests (8production,15retained historical tests); all required commands pass.'],['Existing production interior transition','NOT TESTED','Canonical frozen outdoor world has no supported interior; historical V10 tests do not prove this requirement.'],['Physical Android Chrome / iPhone Safari','NOT TESTED','No recorded physical-device evidence.'],['Hardware/WebGL sustained performance','NOT TESTED','Software-rendered browser evidence is not device certification.'],['Final human character-art acceptance','NOT TESTED',f'Awaiting review.0final Forge FAIL;{len(warn)}auto-luminance leg-alternation WARNs remain documented, not relabelled PASS.']]
report={'status':'FOUR-CHARACTER PLAYABLE REVIEW CANDIDATE; HUMAN ART APPROVAL PENDING','scope':'Phase1B only; Phase2 LOCKED; no main merge or deployment','checks':rows,'bridgeContactSamples':samples,'unsupportedContactSamples':unsupported,'worldPixelComparison':native['worldPixelsCompared'],'worldChangedPixels':0,'forgeWarningCount':len(warn),'finalForgeFailCount':0,'contacts':contacts,'source':'SOURCE_PROVENANCE.md','technicalChanges':'TECHNICAL_CHANGES.md','native':'native-pixel-qa.json','protected':'protected-hashes.json','pipelineChecks':'checks.json'};(D/'QA.json').write_text(json.dumps(report,indent=2)+'\n')
md='# Phase1B QA — playable review candidate\n\nFour characters genuinely run in the accepted Phaser world. Human artistic acceptance is pending; Phase2 remains locked.\n\n| Item | Status | Evidence / limitation |\n|---|---|---|\n'+'\n'.join('| '+' | '.join(r)+' |'for r in rows)+'\n\nNative world evidence uses the same browser launch flags as the accepted Phase1 capture. An initial forced software-backend comparison differed by at most1RGB level; matching launch flags restored exact0changed pixels. No art, renderer or thresholds were changed to obtain that result.\n\nThe live driver still uses the accepted distance phase and60/100 movement speeds; original JuniMotion is byte-exact. Numerical frame uniqueness/contact/readback does not prove appealing anatomy or absence of perceived sliding: inspect actual-speed video and native sheets.\n\nNew character texture memory:3×1152×1120×4 =15,482,880decoded RGBA bytes (~14.77MiB), plus browser preview copies and original world/Juni resources. Four identity textures/previews are bounded caches, not a per-switch allocation stream. Real-device memory/performance remains unmeasured.\n\nCurrent warnings are below verbatim; prior failed iterations in forge-qa/, forge-qa-final/ and forge-qa-native/ are historical diagnostics, not final PASS reports. Final reports are forge-qa-release/. No validator thresholds were weakened.\n\n'
for q in warn:md+='**'+q['file'].split('/')[-2]+'**\n\n```json\n'+json.dumps(q['check'],indent=2)+'\n```\n\n'
md+='Detailed evidence: [checks](checks.json), [native readback](native-pixel-qa.json), [hashes](protected-hashes.json), [gameplay](gameplay-evidence.json), [nonempty progress + refresh](progress-switch-refresh.json), [bridge summaries](bridges-summary.json), [source provenance](SOURCE_PROVENANCE.md).\n';(D/'QA.md').write_text(md)
readme='''# Phase1B — four-character playable review

Juni, Haneul (하늘), Bomi (보미) and Minjun (민준) are now genuinely selectable and playable in the frozen canonical world. Three new native packs extend the accepted foundation. **Human artistic approval is pending. Phase2 remains locked.**

- [Download playable ZIP](PHASE1B_FOUR_CHARACTER_REVIEW.zip) — extract, run `python3 start_review.py`, open `REVIEW.html` / the local game.
- [Visual evidence](VISUAL_REVIEW.md) · [Offline review gallery](VISUAL_REVIEW.html) · [QA and all remaining warnings](QA.md).
- [Source/provenance](SOURCE_PROVENANCE.md) · [Technical changes and reload continuity](TECHNICAL_CHANGES.md) · [Physical-device checklist](DEVICE_REVIEW.md).

![Juni · Haneul · Bomi · Minjun, native source lineup enlarged4× nearest](lineup-review-4x.png)

![Four actual single-player Phaser renders, side by side2× nearest](four-gameplay-crops-2x.png)

The second comparison contains crops from four separate actual native Phaser station screenshots. It is not a fabricated four-player scene. [Original1:1 comparison](four-native-gameplay-crops.png).

Required checks pass, and protected world/Juni sources remain unchanged. Physical devices, sustained hardware WebGL performance and unsupported canonical interiors remain NOT TESTED. Final auto-luminance motion diagnostics retain11WARNs at overlapping/crossing-foot poses; inspect the complete values in QA.md and judge actual-speed movement. This is not automatic artistic approval.

No new world art, repeated cleanup, new character engine, Phase2 services, main merge or public deployment was performed. Earlier Phase1 reports, sources and checkpoints remain recoverable. Stop here for human review.
''';(D/'README.md').write_text(readme)
vis='''# Native visual review

Order throughout: **Juni · Haneul · Bomi · Minjun**. Native PNGs are unscaled Phaser backing images; review enlargements use integer nearest sampling. Source sheets are labelled separately from gameplay. Videos are actual browser recordings; H264 review copies are lossy and do not substitute for native pixel evidence.

![Source lineup4×](lineup-review-4x.png)

**Lossless atlas animations, source review only (not gameplay).** Columns: Juni/Haneul/Bomi/Minjun. Rows: front/back/left/right. The images animate in compatible browsers; [native walk](walk-four-directions-native-preview.png) and [native run](run-four-directions-native-preview.png) remain1×. [Pose-key provenance](motion-preview-provenance.json) explains the intended contact/crossing phases and retains all Forge warnings.

![Walk, four directions, source2× nearest](walk-four-directions-review-2x-preview.png)

![Run, four directions, source2× nearest](run-four-directions-review-2x-preview.png)

[Native source lineup1×](lineup-native-1x.png) · [Actual Phaser body readback lineup1×](actual-phaser-body-lineup-native.png) · [Actual scene crops1×](four-native-gameplay-crops.png)

![Actual Phaser crops2×](four-gameplay-crops-2x.png)

[Native-pixel gameplay focus crop, all four characters / walk / run / emotes](four-character-gameplay-native-crop-review.mp4) · [Uncropped UI review video](four-character-gameplay-review.mp4) · [Full recording](four-character-gameplay.mp4)

[Actual nonempty visited marker, four character switches and refresh — lightweight video](progress-switch-refresh-review.mp4) · [Full recording](progress-switch-refresh.mp4)

'''
for id in ['juni','haneul','bomi','minjun']:
 vis+=f'## {id.title()}\n\n![Desktop selection](selection-{id}-desktop.jpg)\n\n![Mobile landscape browser selection](selection-{id}-mobile-landscape.jpg)\n\n[Complete station frontage, native1:1]({id}-complete-station-frontage-native-1x.png) · [Native scene crop]({id}-station-native-crop.png) · [Both bridges, actual out/return gameplay](bridges-{id}-review.mp4) · [Full bridge recording](bridges-{id}.mp4)\n\n'
 if id!='juni':
  vis+=f'[Native atlas](../../public/assets/characters/{id}/atlas.png) · [Phaser JSON](../../public/assets/characters/{id}/atlas.json) · [Sources / masks / joints / provenance](../../assets-src/characters/phase1b/{id}/provenance.json)\n\n'
  for a in ['walk','run']:
   for d in ['front','back','left','right']:vis+=f'- [{a} {d}: eight native source frames]({id}-{a}-{d}-sheet-native.png) · [2× review]({id}-{a}-{d}-sheet-2x.png) · [Actual Phaser1× pose]({id}-{a}-{d}-native-1x.png)\n'
  vis+=f'\n[Wave native sheet]({id}-wave-sheet-native.png) · [Celebrate native sheet]({id}-celebrate-sheet-native.png) · [Wave actual Phaser]({id}-wave-native-1x.png) · [Celebrate actual Phaser]({id}-celebrate-native-1x.png)\n\n'
vis+='## Preserved world\n\n[Native Canvas/WebGL comparison report](native-pixel-qa.json). Current palace, station and bridge reference entries match accepted Phase1 world pixels exactly under the same camera/browser configuration; original comparison images remain unchanged in docs/phase1.\n\n[QA / exact warning values](QA.md) · [Physical-device review](DEVICE_REVIEW.md).\n';(D/'VISUAL_REVIEW.md').write_text(vis)
parts=['<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Phase1B native review</title><style>body{font:16px system-ui;background:#f6f3eb;color:#183c34;max-width:1100px;margin:24px auto;padding:16px}a{color:#125f72}img{image-rendering:pixelated}figure{margin:18px 0}.scroll{overflow:auto;background:#23232d;border-radius:8px;padding:12px}video{width:100%;max-width:960px}.ui{max-width:100%}li{margin:8px 0}</style><h1>Four-character native review candidate</h1><p>Human character-art approval pending. Phase2 locked. <a href="../../index.html">Play actual Phaser game</a> · <a href="QA.md">QA / warnings</a> · <a href="DEVICE_REVIEW.md">Physical device checklist</a></p><h2>Native comparisons</h2><p>Juni · Haneul · Bomi · Minjun. Source lineup and separate actual single-player renders are explicitly distinguished.</p><div class="scroll"><img src="lineup-review-4x.png" alt="Source sprites4x nearest"></div><p><a href="lineup-native-1x.png">Source1:1</a> · <a href="four-native-gameplay-crops.png">Actual Phaser crops1:1</a></p><div class="scroll"><img src="four-native-gameplay-crops.png" alt="Four separate actual Phaser crop images, native1x"></div><h2>Actual gameplay</h2><video controls preload="metadata" src="four-character-gameplay-native-crop-review.mp4"></video><p><a href="four-character-gameplay.mp4">Full uncropped UI/gameplay recording</a>; the embedded480×520 focus copy is unscaled: gameplay sprites stay native1× and dialog previews retain their original integer2× size. H264 is lossy review evidence; native PNGs prove pixels.</p><video controls preload="metadata" src="progress-switch-refresh-review.mp4"></video><p>Actual visited marker and exact position survive switches and reload.</p>']
parts+=['<h2>Lossless atlas motion previews</h2><p>Source review only, not gameplay. Columns Juni/Haneul/Bomi/Minjun; rows front/back/left/right. PNG source colors are lossless,2× integer nearest. See real Phaser video above.</p><div class="scroll"><img src="walk-four-directions-review-2x-preview.png" alt="Animated native-source walk comparison"></div><div class="scroll"><img src="run-four-directions-review-2x-preview.png" alt="Animated native-source run comparison"></div>']
for id in ['juni','haneul','bomi','minjun']:
 parts+=[f'<h2>{id.title()}</h2><img class="ui" src="selection-{id}-mobile-landscape.jpg" alt="Landscape Chromium touch emulation, not physical device"><p><a href="{id}-complete-station-frontage-native-1x.png">Complete actual station frontage, native1:1</a> · <a href="{id}-station-native-crop.png">Native scene crop</a></p><video controls preload="metadata" src="bridges-{id}-review.mp4"></video><p><a href="bridges-{id}.mp4">Full bridge recording</a></p>']
 if id!='juni':
  parts+=['<p>Authored native source sheets, not concept gameplay.</p>']
  for a in ['walk','run']:
   for d in ['front','back','left','right']:parts+=[f'<p>{a} / {d}: <a href="{id}-{a}-{d}-native-1x.png">Actual Phaser pose</a></p><div class="scroll"><img src="{id}-{a}-{d}-sheet-native.png" alt="Eight native source frames"></div>']
parts+=['<h2>Stop for human review</h2><p>No physical-device PASS, no automatic artistic approval, no Phase2, main merge or public deployment.</p></html>'];(D/'VISUAL_REVIEW.html').write_text('\n'.join(parts))
print('QA/gallery ready;',samples,'contact samples;32actual directional clips×8observed frames; final warnings',len(warn))
