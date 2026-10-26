# Front/back motion correction — human review candidate

Only Haneul, Bomi and Minjun front/back walk/run are corrected:32 native frames each. Juni supplies same-index locomotion landmarks, not costume/face pixels. Original identity artwork, source layers and historical animation packs are immutable. Their own image layers are articulated offline; there is no runtime skeleton, character redesign or controller change.

Open [visual review](REVIEW.html). Sheets are native96×112 cells;2× copies use nearest-neighbor. APNGs are source comparisons at100ms/frame for inspection, **not gameplay**. Actual input-driven Phaser recordings and POST_RENDER native PNGs are separate. Download the focused playable ZIP, extract and run `python3 start_review.py` for the canonical world with the corrected atlases.

- [Juni four-cycle reference](juni-reference-native.png)
- [Haneul corrected](haneul-corrected-native.png) · [same-index comparison](juni-vs-haneul-native.png) · [motion APNG](juni-vs-haneul-motion.png)
- [Bomi corrected](bomi-corrected-native.png) · [same-index comparison](juni-vs-bomi-native.png) · [motion APNG](juni-vs-bomi-motion.png)
- [Minjun corrected](minjun-corrected-native.png) · [same-index comparison](juni-vs-minjun-native.png) · [motion APNG](juni-vs-minjun-motion.png)
- [QA](QA.md) · [machine mapping/source QA](source-qa.json) · [scope/pixel QA](scope-and-pixel-qa.json) · [actual gameplay trace](gameplay-qa.json)

The explicit [pose recipe](../../assets-src/characters/phase1b-frontback-juni/juni-motion-template.json) records screen-left/right shoe soles, hand endpoints, body bounce and observed support/flight phase for each source index. Knees/elbows are connected projected joints adapted to each character's own clothing proportions. It is a locomotion retarget, not an identical silhouette or copied Juni pixels. Juni's observed cycle has asymmetries and consecutive support-side poses; those are retained rather than replaced by a generic symmetric sine gait. Phase labels are observations, not a claim that each source sequence is a textbook evenly spaced contact/down/passing/up cycle.

Front walk, back walk, front run and back run each follow the corresponding Juni template for all three identities. The stronger run body displacement and airborne poses now follow Juni's actual index sequence. Screenshots/tests establish integration and preservation; final foot-contact appeal, loop smoothness and artistic acceptance remain for human review. No Phase2, main merge or deployment.

Actual recordings use this order for each identity: front walk → back walk → front run → back run, separated by review-entry reloads. Comparison source sheets use exact same indices; separately observed gameplay screenshots can have different indices, recorded in gameplay-qa.json. Large full-native captures are kept in the review checkpoint; the portable ZIP includes native crops and links to the full screenshots.

Four-column actual-gameplay comparisons: [front walk](actual-comparison-walk-front.mp4), [back walk](actual-comparison-walk-back.mp4), [front run](actual-comparison-run-front.mp4), [back run](actual-comparison-run-back.mp4). These1.2-second real-time excerpts compare corresponding clips; phase synchronization is not claimed. They retain the full canvas height at native scale so no moving feet are cropped. See comparison-recordings.json for the recorded excerpt times.
