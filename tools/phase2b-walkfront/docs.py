from pathlib import Path
import json
D=Path('docs/phase2b-motion');W=D/'walk-front';ids=['ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']
s='''# Walk-front-only hotfix — candidate for human review

**Walk-right: HUMAN APPROVED / UNCHANGED. Walk-front: candidate, human approval pending. Phase2C LOCKED.**

Baseline: `checkpoint/phase2b-motion-corrected-review-20261027` (`cc27eda`). Before-hotfix reference: `checkpoint/phase2b-walkfront-before-20261027` (64a2ac8, identical production assets to cc27eda). New review: `checkpoint/phase2b-walkfront-hotfix-review-20261027`.

Changed exactly: **Ara, Doyun, Sori, Jiwon, Nari, Taeyang, Yuna, Hyunwoo**. All eight are active roster entries. The latest directive explicitly permits Ara/Doyun walk-front amendments; their earlier approval is preserved for every other pose and original source file.

## What changed

Only `walk-front-0` through `walk-front-7` for each actor:64 native frames and their8 atlas containers. No timing adjustment was needed. No walk-right, walk-back, run, idle, gesture, start/stop, clipJSON, atlasJSON, anchor, speed, stride or runtime code changed.

The prior retargeting transferred Juni's sole/hand endpoints but used midpoint elbows and a generic narrow sleeve mask. This restricted the forearm fold, lost the native sleeve silhouette and produced stiff front stepping. A rigid whole torso also missed the small difference between shoulder and hip transfer.

The hotfix uses own native garment/limb pixels with connected-component ownership, excluding neighboring hands from leg layers and clothing fragments from arm layers. It keys the elbow arcs and knee folds from Juni's actual eight poses; keeps Juni's actual contact/lift order and original phase indexing; projects own shoes toward camera and foreshortens the lifted heel; uses bounded1px differential shoulder/hip transfer. Head/hair first47RGBA rows remain pixel-identical at every phase. No copied Juni anatomy, blurred layers, generated identity or new image API.

The approved Juni cycle is not replaced with an idealized0/4 sinusoid. Its original support pattern and small bodyDeltaX/bodyDeltaY variations are retained. Rhythm is still44px per stride at60px/s, with8 distance-driven poses. All frame exports remain96×112, anchor(48,100), binary alpha and nearest sampling.

## Evidence

[Playable hotfix ZIP](walk-front/WALK_FRONT_HOTFIX_REVIEW.zip): extract, run `python3 start_review.py`, open `REVIEW.html`. The compiled Phaser engine/world are unchanged; the eight atlas runtime files are updated. Twelve characters and existing Studio/wardrobe remain present.

[Visual review page](walk-front/REVIEW.html) shows source-only before/after plates and separate actual Phaser comparisons. Phase-aligned videos use actual captured game contexts at matching0–7 indices for3 consecutive cycles, displayed at nominal gait timing. They are not represented as simultaneous unretimed recordings. The separate gameplay videos are unretimed real WASD/Studio recordings at native canvas registration. PNGs are fidelity authority; MP4 is review media.

| Character | Native Juni / before / after source | Actual Juni comparison | Unretimed Phaser gameplay | Native runtime8 poses |
|---|---|---|---|---|
'''
for id in ids:s+=f'|{id.title()}|[PNG](walk-front/{id}-front-source-native.png) · [2x](walk-front/{id}-front-source-2x.png) · [animated source](walk-front/{id}-front-source-review.gif)|[video](walk-front/juni-vs-{id}-front-phaser.mp4)|[video](walk-front/{id}-front-gameplay.mp4)|[PNG](walk-front/{id}-actual-native.png)|\n'
s+='''
## Technical QA

| Check | Result | Evidence |
|---|---|---|
| Scope and preservation | PASS |[Audit](walk-front/audit.json):72 modified art files,64 changed cells;832 other cells exact, including64 approved walk-right poses. Entire world,UI,engine,persistence,cosmetics and original source/rig/clip files unchanged |
| Juni / Haneul / Bomi / Minjun | PASS |All baseline files exact; Juni also recorded as native runtime reference |
| Source registration and order | PASS |96×112,(48,100),60/100speed,44/64stride unchanged; no missing/reordered frames,8 distinct source walk-front poses per actor |
| Actual default Phaser readbacks | PASS |[216 captures](walk-front/readbacks.json),0 opaque-pixel mismatch;9 actors×3consecutive loops×8phases; integer camera,zoom1,nearest,one player; actual positiveY traversal |
| Four existing cosmetic presets | PASS technical / visual review |[32 actual readbacks](walk-front/preset-readbacks.json),0 mismatch against independently composed current base+unchanged patches; original cosmetic files unchanged |
| Asset validation | PASS |[log](walk-front/logs/assets.log) |
| Full unit suite | PASS |[102 tests](walk-front/logs/all-unit.log), including9 new hotfix guards |
| Typecheck / lint / formatting | PASS |[typecheck](walk-front/logs/typecheck.log), [lint](walk-front/logs/lint.log), [format](walk-front/logs/format-check.log) |
| Physical Android/iPhone, hardware performance | NOT TESTED |Desktop Chromium evidence only; no physical-device certification |
| Human walk-front quality | PENDING |Review rhythm,weight,arm/leg readability,clothing/foot overlap and approach feeling directly; technical PASS is not art approval |

Two historical unit artifact guards now use the explicit authorized front-only amendment instead of asserting complete Ara/Doyun atlas-file identity. Historical manifests were not overwritten. The replacement audit checks every frozen file and all104 untouched cells per actor; no runtime validator, Forge threshold or production engine changed.

The four preset outfits retain their earlier authored paint/erase pose patches; those garments were not reauthored. Their native regression images are supplied for inspection and should not be mistaken for newly authored wardrobe locomotion. This review targets the eight default walk-front clips. Other historical direction/run WARNs remain recorded and were not reopened.

[Before hashes](walk-front/before.json) · [exact cell/file deltas](walk-front/audit.json) · [actual media provenance](walk-front/media-provenance.json). Original sources,previous checkpoints and approved right-motion pixels remain recoverable. No map/Studio redesign, Phase2C, main merge or deployment.

**STOP for human walk-front approval.**
'''
(D/'WALK_FRONT_FIX.md').write_text(s)
for n in ['QA.md','VISUAL_REVIEW.md']:
 p=D/n;text=p.read_text();prefix='''> **Current walk-front hotfix:** walk-right is HUMAN APPROVED and pixel-identical. Only8 walk-front cells each for Ara,Doyun,Sori,Jiwon,Nari,Taeyang,Yuna,Hyunwoo changed. See [current hotfix and QA](WALK_FRONT_FIX.md) and [visual review](walk-front/REVIEW.html). Walk-front awaits human approval; Phase2C LOCKED.
>
> The report below is the preserved cc27eda recovery review; its counts/artifacts describe that earlier checkpoint.

'''
 if not text.startswith('> **Current walk-front hotfix:'):p.write_text(prefix+text)
h='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Walk-front hotfix review</title><style>body{background:#213c35;color:#fff0ce;font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:20px}a{color:#a8e3cc}img{max-width:100%;image-rendering:pixelated}video{width:768px;max-width:100%;image-rendering:pixelated}section{border-top:1px solid #71806b;padding:20px 0}summary{cursor:pointer;padding:8px}</style><h1>Walk-front · bản sửa giới hạn</h1><p>Walk-right: ĐÃ DUYỆT, KHÔNG THAY ĐỔI. Walk-front: chờ duyệt. Phase2C LOCKED.</p><p><a href="../../../index.html?entry=transition">Vào game Phaser</a> · <a href="../WALK_FRONT_FIX.md">Phạm vi và QA</a></p><p>Video đối chiếu: ảnh Phaser thật ghép cùng pha,3 vòng liên tiếp. Video gameplay riêng giữ nguyên tốc độ ghi. Ảnh trước/sau là source-only native1:1, không phải ảnh gameplay.</p>'''
for id in ids:
 h+=f'<section><h2>Juni ↔ {id.title()}</h2><video controls loop preload="none" src="juni-vs-{id}-front-phaser.mp4"></video><p><a href="{id}-front-gameplay.mp4">Gameplay nguyên tốc độ</a> · <a href="{id}-actual-native.png">8 pha native trong Phaser</a> · <a href="{id}-full-phaser-native.png">Ảnh toàn canvas native</a></p><details><summary>Juni / trước / sau — source-only</summary><a href="{id}-front-source-native.png"><img loading="lazy" src="{id}-front-source-2x.png" alt="Juni before after native frames"></a><p><a href="{id}-front-source-review.gif">Xem animation source cùng pha</a></p></details></section>'
h+='<p>NO Phase2C / main merge / deployment. STOP for human walk-front review.</p></html>'; (W/'REVIEW.html').write_text(h)
