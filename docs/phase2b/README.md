# Phase2B — twelve playable characters

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
