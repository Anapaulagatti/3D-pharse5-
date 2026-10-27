# Walk-front-only hotfix — candidate for human review

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
|Ara|[PNG](walk-front/ara-front-source-native.png) · [2x](walk-front/ara-front-source-2x.png) · [animated source](walk-front/ara-front-source-review.gif)|[video](walk-front/juni-vs-ara-front-phaser.mp4)|[video](walk-front/ara-front-gameplay.mp4)|[PNG](walk-front/ara-actual-native.png)|
|Doyun|[PNG](walk-front/doyun-front-source-native.png) · [2x](walk-front/doyun-front-source-2x.png) · [animated source](walk-front/doyun-front-source-review.gif)|[video](walk-front/juni-vs-doyun-front-phaser.mp4)|[video](walk-front/doyun-front-gameplay.mp4)|[PNG](walk-front/doyun-actual-native.png)|
|Sori|[PNG](walk-front/sori-front-source-native.png) · [2x](walk-front/sori-front-source-2x.png) · [animated source](walk-front/sori-front-source-review.gif)|[video](walk-front/juni-vs-sori-front-phaser.mp4)|[video](walk-front/sori-front-gameplay.mp4)|[PNG](walk-front/sori-actual-native.png)|
|Jiwon|[PNG](walk-front/jiwon-front-source-native.png) · [2x](walk-front/jiwon-front-source-2x.png) · [animated source](walk-front/jiwon-front-source-review.gif)|[video](walk-front/juni-vs-jiwon-front-phaser.mp4)|[video](walk-front/jiwon-front-gameplay.mp4)|[PNG](walk-front/jiwon-actual-native.png)|
|Nari|[PNG](walk-front/nari-front-source-native.png) · [2x](walk-front/nari-front-source-2x.png) · [animated source](walk-front/nari-front-source-review.gif)|[video](walk-front/juni-vs-nari-front-phaser.mp4)|[video](walk-front/nari-front-gameplay.mp4)|[PNG](walk-front/nari-actual-native.png)|
|Taeyang|[PNG](walk-front/taeyang-front-source-native.png) · [2x](walk-front/taeyang-front-source-2x.png) · [animated source](walk-front/taeyang-front-source-review.gif)|[video](walk-front/juni-vs-taeyang-front-phaser.mp4)|[video](walk-front/taeyang-front-gameplay.mp4)|[PNG](walk-front/taeyang-actual-native.png)|
|Yuna|[PNG](walk-front/yuna-front-source-native.png) · [2x](walk-front/yuna-front-source-2x.png) · [animated source](walk-front/yuna-front-source-review.gif)|[video](walk-front/juni-vs-yuna-front-phaser.mp4)|[video](walk-front/yuna-front-gameplay.mp4)|[PNG](walk-front/yuna-actual-native.png)|
|Hyunwoo|[PNG](walk-front/hyunwoo-front-source-native.png) · [2x](walk-front/hyunwoo-front-source-2x.png) · [animated source](walk-front/hyunwoo-front-source-review.gif)|[video](walk-front/juni-vs-hyunwoo-front-phaser.mp4)|[video](walk-front/hyunwoo-front-gameplay.mp4)|[PNG](walk-front/hyunwoo-actual-native.png)|

## Technical QA

| Check | Result | Evidence |
|---|---|---|
| Scope and preservation | PASS |[Audit](walk-front/audit.json):72 modified art files,64 changed cells;832 other cells exact, including64 approved walk-right poses. Entire world,UI,engine,persistence,cosmetics and original source/rig/clip files unchanged |
| Juni / Haneul / Bomi / Minjun | PASS |All baseline files exact; Juni also recorded as native runtime reference |
| Source registration and order | PASS |96×112,(48,100),60/100speed,44/64stride unchanged; no missing/reordered frames,8 distinct source walk-front poses per actor |
| Actual default Phaser readbacks | PASS |[216 captures](walk-front/readbacks.json),0 opaque-pixel mismatch;9 actors×3consecutive loops×8phases; integer camera,zoom1,nearest,one player; actual positiveY traversal |
| Independently extracted hotfix ZIP | PASS |[8 more native readbacks](walk-front/package-native-readbacks.json); every corrected actor moves positiveY>3strides,one sprite,normal controls,0pixel mismatch. All12 packaged atlases match current files |
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
