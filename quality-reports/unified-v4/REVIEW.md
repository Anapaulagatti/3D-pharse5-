# Living Pixel Seoul — unified V4 Gate2 review

**PLAYABLE REVIEW CANDIDATE — NOT VISUALLY APPROVED.** All prior minimalist and painterly A/B/C rejected. One original town, one consistent native pixel kit, no copied reference game assets/map/UI. Artwork is openly code-drawn native raster, no image model. Beauty/cohesion/readability remain the user's review decision.

![Actual Phaser2× Central Plaza](render/gameplay-2x.png)

[Actual1×overview](render/overview-1x.png) · [idle3×](render/idle-closeup.png) · [actual outfits](ACTUAL_OUTFIT_COMPARISON.png) · [rejected-vs-new](REJECTED_VS_UNIFIED.png) · [mobile](render/mobile.png).

## What actually runs

One32×24tilemap with modular Korean-style roofs/eaves, wall/window/door bays, shaded side walls, foundation/steps, shared tree/ground/prop pixel density. Courier, café/social area, culture hanok, quest board, puzzle sign, TOPIK entrance, PvP sign, outfit corner and gardens are present.64props/65colliders, all10landmark approaches reachable. Buildings/trees are separate sorted/collidable sprites on the tilemap, not a single painted backdrop. Stations for later systems clearly explain that they are not open features. Mira is explicitly a local demoNPC, not a connected player.

Avatar32×48 with body/outfit/hair/accessory common registration; two hairstyles, two constructed outfits and satchel toggle affect the actual player. Four-direction idle/blink/walk/run, wave/celebration/social pose. Run uses separately authored frames, not faster walk:6+of8poses differ in each direction; actual gait contact sheet ACTUAL_GAIT_FRAME_REVIEW.png shows larger steps/airborne phases/side lean. Default2× gives a visibly readable86px idle silhouette while retaining a shared door/building/prop scale; source frame48px has transparent top padding.1×map/3×inspection available. Compare readability yourself; the new character is intentionally balanced with town scale, not claimed larger than the rejected version.

## Actual rendered proof

[Gameplay movie22.87s](living-pixel-seoul-gameplay.mp4),288raw CDP compositor frames/original Chrome timestamps; native keyboard/UI, no teleports/pose injection/playback speed-up. Includes natural idle, individual social emotes, outfit/hair change and four-way walking/running. Final decoded wave/celebrate/pose plus frame sequences184–191walk,216–223run,240–247run-left inspected. Raw frames/metrics preserved in motion/capture.json, with clear source/runtime identities. Capture overhead/software renderer is not physical-device FPS evidence.

Actual native camera navigation: [house detail](render/house-detail-gameplay.png) / [tree detail](render/tree-detail-gameplay.png). [Natural blink](render/natural-blink.png) was reached by normal runtime then retained with Pause UI. No animation frame assignment. Outfit screenshots use actual UI combinations. Source sheets/modules are editable originals, separately labelled; screenshots contain real running Phaser output.

Initial renderer refinement and helper failures in ITERATION_LOG.md, first render in render-attempt-1. Final images have the quieter stone court/brick accents/landscape details/longer Korean roof ridge and corrected accessible boards. No old concept image is relabelled actual gameplay.

## Verified checks

- Gate0 fresh HTTPS remote3D recovery2738file hashes PASS at f1f13f2; old pixel2554327 preserved,1923old art/evidence/package files and exact lock unchanged.
- Toolkit/version/type/build PASS; original5unit tests and3adapted native browser flows PASS,21.62s/no failures/skips/flaky. Native controls/collision/dialogue, distinct run keys, layer registration/outfit persistence, emote returns, OS reduced motion/pause, touchDPR1/2, loaded-sessionoffline and genuine WebGL-unavailable Canvas fallback.
- SourceQA:28files/hashes,152frames/layer6layers, source/atlas equality, binary alpha/palette/gutters, run-difference and all station/NPC reachability. See asset-qa.json. Geometry checks do not establish artistic approval.
- Source00139ca [remote CI38681323177 SUCCESS](https://github.com/Anapaulagatti/3D-pharse5-/actions/runs/38681323177). Final review checkpoints use the same JS/art; HTML title changed only. Read-only CI has no deploy job.
- Exact extracted static package HTTP/browser PASS desktop/mobileDPR2,1:1nativeCSS canvas, actual movement, no missing resources/critical console errors. Included Python entry point actually launched. Windows GUI/browser auto-open itself not tested; use printed URL.
- Publicv0.5 live HTML unchanged SHA082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f. No public replacement or separate Korean Arena changes.

## View and play

Download [living-pixel-seoul-v4-review.zip](../../downloads/unified-v4/living-pixel-seoul-v4-review.zip), unzip, open terminal in Living-Pixel-Seoul-V4, run `python3 start.py` (Windows `py start.py`), open printed HTTP address. Python3 required, no Node to view. Do not open HTML through a source-text viewer. Cloud has no public preview port.

WASD/arrows walk, Shift run, E near Mira, Space wave. Buttons offer all emotes, touch movement/run, hair/outfit/accessory,1×/2×/3×camera, pause/reduced motion. No account, cloud service, live players, quest completion, ad SDK or full learning system.

ZIP474,901bytes/SHA256e904884782658a717d15fc87c4e076bcbcece94ef8a4d129451a49269e6f7eef; full manifest downloads/unified-v4/package-manifest.json. Build1,666,980bytes; original pixel data174,461bytes. Dist-only allowlisted HTML/JS/CSS/PNG/JSON/SVG/license text; no source/private-key/provider-token markers/old3D shipped. No claim that an automated marker scan substitutes for a broad security certification.

Full future roadmap docs/UNIFIED_V4_ROADMAP.md;35minigame designs docs/UNIFIED_V4_MINIGAMES.csv. First Delivery/Sign Repair/Courier Rush come after visual approval. Human Korean content review, physical-device tests, real backend/moderation/ranked anti-cheat, optional disabled cosmetic-only ad adapter and publication remain later gates. GUI Tiled/LibreSprite unavailable; tested editable PNG/TiledJSON alternatives retained.

**STOP: please review this ONE town's coherence, idle readability, architecture/trees and movement. Do not expand content or publish until new user approval.**
