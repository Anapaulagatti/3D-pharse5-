# Approved asset/runtime preservation

Approved Phase2A complete commit: `ed75734d0e0865274ca0b82bab2495d78878d24b`. Approval tag: `checkpoint/phase2a-six-characters-approved-20261026`. Branch starts exactly there; original Phase2A branch/checkpoints remain unchanged.

| Manifest | Files verified | Changed |
|---|---:|---:|
| `docs/phase2b/approved-six.json` |1340|0|
| `docs/phase2b/approved-runtime-code.json` |57|0|
| `docs/phase1/protected-world.json` |3082|0|
| `docs/phase1/protected-juni.json` |224|0|

The15 approved character-source snapshots remain exact. Unit tests compare all six identity records, animation definitions, scales, anchors and movement values against frozen source-derived records. The ten cosmetic assets/catalog, four suggested looks and v1/v2 preference implementation are unchanged. Original source layers and animation-generation tools are retained.

Runtime exceptions are limited to data-only new registrations and CharacterSelection's empty-future visibility, selected-card scrolling and neutral default-only caption. No second engine exists. Seven historical capture helpers had pre-existing formatting failures; only whitespace/formatting was normalized, with actual before/after syntax trees and source hashes checked: [normalization audit](formatter-normalization.json). No validator was ignored, weakened or deleted.

Actual native regression compared **6,868,992 world pixels,0 changes**, plus six original native actor readbacks with0 unexplained differences. Hanbit Station, Jeju bridges, palace/farm, world collision, main scene, controller, camera and Scenic Tour remain protected. [Source-reference comparison](protected-six-reference-comparison-native.png) is source art; [actual six-character native crops](six-native-gameplay-crops.png) are genuine Phaser captures.

[Machine hash report](protected-audit.json) · [approved six freeze](approved-six.json) · [approved runtime-code freeze](approved-runtime-code.json) · [native regression](approved-six-native-pixel-qa.json).
