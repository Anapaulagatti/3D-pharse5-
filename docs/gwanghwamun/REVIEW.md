# Gwanghwamun Plaza — visual review

**Recommended: B — Ginkgo Commons. Plaza approval is pending.** Juni/B is the provisional player; Bori/A and Nari/C remain future avatars. No new action clips or NPCs were made.

| Plaza | Visual direction |
|---|---|
| A — Royal Stone Promenade | Formal north/south axis, pale granite, civic terraces and restrained ornamental water. |
| B — Ginkgo Commons | Intimate reading pavilion/tea hall, asymmetrical garden pockets, golden ginkgo, seated Sejong and courtyard rill. Recommended for human scale and social spaces. |
| C — Hanji Lantern Court | Warm dusk, offset cultural stage, fan-shaped gathering paving, festival lanterns and creative street furniture. |

[One comparison board](world-review-board.png) labels generated concepts separately from actual Phaser pixels. Raw concepts remain in assets-src/gwanghwamun/concepts. The board's central engine image is pasted at native1024×768, not a painted concept used as a background.

## View the playable proof

Download [playable-review.zip](playable-review.zip), extract **Korean-Arena-Gwanghwamun-Review**, run `python3 start.py` (Windows: `py start.py`), then open the printed HTTP URL ending `/3D-pharse5-/plaza-review.html`. Python3 required, no Node required to view. Opening HTML in a source viewer or via file:// is not the viewing method. Ctrl+C stops the server.

WASD/arrows or touch pad move; Shift/Run accelerates; E or prop click opens a landmark note. Camera1×/2×/3×, evening, pause and OS reduced-motion support remain. Gallery below the engine shows the3 source concepts. Brand link opens the preserved previous town; character-review.html still shows Bori/Juni/Nari. This is an offline/local art proof, not multiplayer or a public release.

Package4,434,956bytes, SHA256 **55fba6719cadd45c6a24b5d48b9f2c040b7c1accf09ce803150c5e8e26715d16**. Exact extracted Python launcher was browser-tested: native day, evening and mobileCanvas PNGs byte-identical to the inspected root build. Details: [package-verification.json](package-verification.json).

## Actual engine evidence

- [Native1× day](phaser-native-day.png), [evening](phaser-evening.png), [2× detail](phaser-detail.png), [Juni beside the gate](phaser-scale.png).
- [Behind foliage](behind-tree.png), [in front of foliage](front-tree.png), [water collision](water-collision.png).
- [Mobile Canvas](mobile-canvas.png), [mobile page](mobile-page.png), [review page](review-page.png).
- [33-second Phaser recording](plaza-playthrough.mp4). Actual keyboard traversal, ambient movement, bridge/occlusion and camera/UI. Four STATIC Juni views translate through the controller; this is **not** a new walk/idle animation demonstration. MP4 encoding25fps is not a measured gameFPS claim.

Actual source:12 generated/Forge-finished prop types,32 placements,8 extracted32px terrain variants,1024×768 world,33 exact exported solid rectangles. Juni80px body/root40,96 remains unchanged. Gate336px and tea hall210px maintain a readable miniature relationship. Phaser reuses existing movement/acceleration/input/physics/UI with optional scene layout/asset configuration; old town/actors/content/lock are preserved. An existing fillAlpha=0 bug in the evening overlay was fixed: rendered evening/day mean-channel ratio0.836889, visible and readable.

Full root setup verification passed: source checks, type/lint/format,8unit tests, production build,9browser flows including the preserved game and character review. Additional mobile test uses actual emulated CDP touchStart/touchEnd, genuine WebGL-unavailable Canvas and OS preference changes. Assets/Tiled/native pixels are checked offline during assets:check. Final clean-checkout/CI outcome and exact source SHA are recorded in annotated checkpoint/gwanghwamun-concepts-20261015 after verification; do not infer an unobserved CI result from this sentence.

## Quality boundaries for this review

These are review candidates, not approved production artwork. Source concepts are richer and higher-resolution than the intentionally small reusable proof kit. The playable proof still has visible hard tile transitions and a straight decorative rill; organic edge/autotile polish remains a visual decision. No seamless/Wang-proof claim. Standalone gate is fully framed even though conceptB's northern roof meets its source-image edge. Generated source sign-like marks are not used in runtime signage.

The Forge tree pack retains a103px unowned tiny-fragment warning in high-resolution source extraction; first-pass magenta-fringe warnings were resolved with documented radius3 despill. Two low-contrast earth variants failed the default terrain threshold and were excluded; the curated8-variant atlas passes unchanged strict contrast/variant/border gates. All warnings/skips are preserved in FORGE.md and raw manifests. Tiled exporter read-back and actual Phaser import pass; native Tiled editor GUI import is untested. Mobile is Chromium emulation/DPR2, not physical-phone performance testing. Source concepts, still-direction movement and ambient texture motion are not video-generated character clips.

Recovery before work: recovery/before-gwanghwamun-world-20261015 ->6ff6df0f5671c98291d9b0b6b719ee2e96a6d64c, pushed and independently peeled before editing. Original town remains active, no deletion/cleanup/main promotion/Pages deployment. Stop for the user's plaza review.
