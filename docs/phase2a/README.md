# Phase2A Character Studio — six-character review

Four approved originals remain pixel-identical. Ara and Doyun are new playable review candidates. Character Studio supplies ten independently frame-registered free cosmetics, four suggested looks, local named presets, reset and additivev2 persistence. Phase2B remains locked; stop for human review.

- [Executed commands](VALIDATION_COMMANDS.md) · [protected hashes](protected-audit.json) · [extracted ZIP smoke](package-smoke.json)
- [Open visual review](REVIEW.html) · [QA](QA.md) · [architecture/contracts](ARCHITECTURE.md) · [memory/performance](PERFORMANCE.md)
- [Six original appearances, native](six-original-appearances-native.png) · [readable2× review](six-original-appearances-review-2x.png)
- [Juni vs Ara, same frame index](juni-vs-ara-native.png) · [Juni vs Doyun](juni-vs-doyun-native.png)
- [Ara walk](ara-walk-motion.png) / [run](ara-run-motion.png) · [Doyun walk](doyun-walk-motion.png) / [run](doyun-run-motion.png): source animations, not gameplay recordings
- [Catalog native1](catalog-1-native.png) / [native2](catalog-2-native.png) · [larger review1](catalog-1-review-2x.png) / [review2](catalog-2-review-2x.png)
- [Actual native pixel QA](native-pixel-qa.json) · [original4/world pixel QA](original4-native-pixel-qa.json) · [v1/preset/reload evidence](persistence-evidence.json)
- [Provenance](source-provenance.json) · [coverage](coverage.json) · [warnings](FORGE_WARNINGS.md) · [device handoff](DEVICE_REVIEW.md)

Actual Phaser videos and native evidence:

- [ara-default actual gameplay](ara-default-actual-gameplay.mp4) · [native gameplay poses](ara-default-actual-native-sheet.png) · [2× inspection](ara-default-actual-review-2x.png) · [full native front-walk](ara-default-walk-front-phaser-native.png)
- [doyun-default actual gameplay](doyun-default-actual-gameplay.mp4) · [native gameplay poses](doyun-default-actual-native-sheet.png) · [2× inspection](doyun-default-actual-review-2x.png) · [full native front-walk](doyun-default-walk-front-phaser-native.png)
- [review-ara-harbor actual gameplay](review-ara-harbor-actual-gameplay.mp4) · [native gameplay poses](review-ara-harbor-actual-native-sheet.png) · [2× inspection](review-ara-harbor-actual-review-2x.png) · [full native front-walk](review-ara-harbor-walk-front-phaser-native.png)
- [review-ara-sunlit actual gameplay](review-ara-sunlit-actual-gameplay.mp4) · [native gameplay poses](review-ara-sunlit-actual-native-sheet.png) · [2× inspection](review-ara-sunlit-actual-review-2x.png) · [full native front-walk](review-ara-sunlit-walk-front-phaser-native.png)
- [review-doyun-field actual gameplay](review-doyun-field-actual-gameplay.mp4) · [native gameplay poses](review-doyun-field-actual-native-sheet.png) · [2× inspection](review-doyun-field-actual-review-2x.png) · [full native front-walk](review-doyun-field-walk-front-phaser-native.png)
- [review-doyun-varsity actual gameplay](review-doyun-varsity-actual-gameplay.mp4) · [native gameplay poses](review-doyun-varsity-actual-native-sheet.png) · [2× inspection](review-doyun-varsity-actual-review-2x.png) · [full native front-walk](review-doyun-varsity-walk-front-phaser-native.png)

[Customized software WebGL native capture](custom-ara-webgl-native.png) is rendering smoke evidence only. [Mobile844×390](mobile-landscape-studio-browser.jpg) / [small667×375](small-landscape-studio-browser.jpg) are Chromium touch emulations, not real iPhone/Safari or Android evidence.

Run the extracted playable ZIP with `python3 start_review.py`, then open the local REVIEW.html. Full masters/layers/frames and large native screenshots are versioned in the immutable review checkpoint; the portable ZIP includes the compiled offline game, compact native crops and the two default-character recordings. Four cosmetic gameplay videos and larger source evidence link to the immutable Git checkpoint to keep the ZIP below100MB. All native PNGs are unmodified backing data or exact integer crops. Enlargements use nearest-neighbor. MP4s are lossy native-scale crops of actual browser recordings and begin with real Studio selection followed by gameplay; use PNGs for pixel judgment.

Checkpoint: `checkpoint/phase2a-character-studio-review-20261026`. Approved baseline: `checkpoint/phase1b-four-characters-approved-20261026` →51ac4b4f20f0af2f26d1566988580d92c0612356. New Phase2A human artistic approval remains pending.
