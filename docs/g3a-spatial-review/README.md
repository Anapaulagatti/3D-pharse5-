# G3-A targeted spatial corrections — final approval withheld

[Verified direct PNG/ZIP links](NATIVE_LINKS.md) · [Revised registration and bakery comparison](REGISTRATION.md) · [Technical/visual PASS–FAIL](QA.md) · [Geometric comparison board](SITE_COMPARISON.png) · [Exact candidate JSON](proposal-v2-comparison.json)

The original waterfront bakery is rejected as the preferred registration: it cuts five approved route corridors and projects into amusement access/carousel space. The alternative southwest quay preserves those corridors and the carousel, but requires explicit new land allocation and a25.43s access spur. **It is a comparison candidate, not a resolved final site.** If the quay/pacing cost is unacceptable, defer bakery registration rather than shrink the building or divert the approved main network.

Maru is compared at a lower western plot with a clear retail-street envelope, a documented western Namsan-loop amendment and a corrected marker at the existing glass door. No approved source artwork, masterplan, protected station geometry, carousel, ferry terminal, Jeju bridge or Juni is changed.

## Working native rendering links

The previous PNG path was correct but the remote review branch had not contained the local renderer/evidence commits. The branch was fast-forwarded; both immutable URLs below were downloaded and verified **HTTP200 / image/png / byte-exact1280×900**:

- **Before:** [original native Canvas PNG](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/2934683df9246a39854be247d650d652561f89d5/docs/gate3a-pixel-audit/before-canvas-native.png)
- **After:** [original native corrected Canvas PNG](https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/2934683df9246a39854be247d650d652561f89d5/docs/gate3a-pixel-audit/after-canvas-native-backing.png)
- [URL/download verification](verified-rendering-links.json). These are direct image responses, not GitHub HTML file-preview pages.
- Lightweight native1:1 frontage crops (684×295, under400KB each, no resampling): [before](render-before-frontage-1x.png) / [after](render-after-frontage-1x.png). Full originals above remain unchanged.
- Local review copies: [before](render-before-native-1x.png) / [new corrected-engine after](render-after-native-1x.png).

Canvas's unwanted0.5px destination expansion and half-CSS-pixel centering remain fixed. Current Canvas readback matches **1,108,756** unobstructed source pixels exactly. The station's explicit0.5px pivot remains provisionally acceptable and was **not** a blur cause. [Remaining baked-in source softness](../gate3a-pixel-audit/REPORT.md) is preserved separately; native WebGL already reproduced it without additional filtering. No sharpening, artificial upscaling, recoloring or regeneration.

## Actual native Phaser placement screenshots

All images below are1280×900 backing-store PNGs captured at Phaser POST_RENDER, zoom1, DPR1. They are not browser-scaled review boards. Open/download at100% for native pixels.

| Placement | Native PNG |
|---|---|
| Current waterfront bakery / rejected preferred site | [Open](bakery-waterfront-1x.png) |
| Southwest quay bakery / conditional alternative | [Open](bakery-quay-1x.png) |
| Original Maru proposal | [Open](maru-original-1x.png) |
| Revised Maru with Juni at the glass-door approach | [Open](maru-revised-1x.png) |
| Namsan western access comparison | [Open](namsan-access-1x.png) |
| Protected station and corrected planters | [Open](station-1x.png) |
| Cafe, bookshop and learning envelopes | [Open](retail-1x.png) |

The geometry-only surroundings remain G3-A engineering placeholders. Pixel-exact source preservation and traversable paths do not establish final world composition, premium public realm or G3-B artistic approval.

[Pixel readback](native-pixel-proof.json) · [Exact routes/clearances](spatial-validation.json) · [Real keyboard traversal](traversal.json) · [Site-screening method/limits](site-scan.json)

WebGL hardware performance remains **UNRESOLVED**. Physical Android Chrome and iPhone Safari remain **NOT TESTED**. Existing [device checklist and report export](../gate3a-corrections/DEVICE_CHECKLIST.md) retained. No new FPS claim is based on screenshot/traversal runs.

[Targeted playable package](G3A_SPATIAL_COMPARISON.zip): extract, run `python3 -m http.server 4284 --bind 127.0.0.1`, open `http://127.0.0.1:4284/`. The new `registration-refined` option is candidate-only; the original candidate and approved default world remain available unchanged. No public site deployment.

**STOP: approve/request changes to the candidate land, bakery allocation/pacing, Maru allocation/door marker/local scenic-loop amendment and listed easements. G3-B remains blocked; no main merge, protected checkpoint rewrite or deployment.**
