# V8 Modern Korean City — review candidate

The rejected V7 southern street/site plan has been retired from the new playable entry, not covered with another road patch. V8 creates a continuous north–south civic boulevard, an east–west pedestrian avenue, subordinate local streets and four explicit street-facing urban blocks. The station moves east of the boulevard into a dedicated transport plot; its rear siding does not cut across the public axis. Namsan and Bora Bloom are independent campuses with separate entrances, circulation and destination courts. A continuous coastal promenade serves one mainland terminal and an explicit reciprocal ferry to a northwestern Jeju landing. There is no decorative or contradictory mainland–island bridge.

**This is a candidate for USER visual approval, not a final map lock or published game.** Work stays on `rebuild/pixel-social-rpg-v3`; no main merge, Pages deployment, separate-app edits, paid-provider calls or history rewrite.

## Sequence and recovery

Before edits, recovery/before-v8-southern-city-rebuild-20261020 was pushed and independently peeled to `ea8588f1c85b1a6481bd38eb68ab3a6a19d3f43a` (complete V7). Source history and all former entries/art remain intact. The first verified planning/graybox checkpoint is `73b8384a45dca1eb62a902a1b1c4a1644b225a4c`, pushed/read back before premium terrain production was complete.

`tools/plan_v8_city.py` created editable JSON/SVG/PNG, actual world dimensions4352×5312,12functional plots,38routes, frontage/entrance/function/boundary/architecture envelopes, district boundaries and ferry decision. Plan feasibility and then actual keyboard-controlled graybox travel across both complete city axes were checked BEFORE the material-generation call. Graybox screenshots are clearly labelled temporary surfaces, not final game art. Initial blocked-route receipts are retained; pavilion, ride and Jeju access was corrected instead of shrinking Juni or weakening collision. Final road construction consumes this new plan, not V7 southern road geometry or a traced reference bitmap.

## Preservation and spatial changes

`assets-src/v8-city/preservation.json` checks3,523earlier source/runtime/art/test/tool/lock files byte-for-byte against the V7 checkpoint. All273historical objects rooted north of2240 retain identity, position, scale and sort anchor. Every northern ground pixel y0–2239 is identical. Original approved PNGs, Juni144frames, lessons/dialogues, Academy interior, mobile controls and old reviews remain unchanged. V8 uses an isolated Phaser adapter entry, `v8-city-review.html`; default/older entries are preserved.

27retained landmark placements change. Exact before/after roots and retired active placements are in `assets-src/v8-city/relocations.json`; the separate old sources are retained for recovery, not deleted. Principal changes, in native world pixels:

| Site | V7 root | V8 root | Why |
| --- | --- | --- | --- |
| Bookshop |1664,2480|1728,2744|Frontage of northwest shopping block|
| Library/social hub |1664,2808|1728,3320|Southwest civic block, own court and local street|
| Station |2240,2832|2704,2720|Independent northeast transit plot; public boulevard remains open|
| Train |2600,3096|2992,2448|Aligned rear siding, behind station|
| Cafe |2848,2808|2704,3320|Southeast commercial block facing common public street|
| Tower |704,3008|640,2824|Northern park focal plaza, loop and woodland approach|
| Park pavilion |1136,2816|1120,2864|Accessible signed trail junction|
| Ferris wheel |3464,2992|3552,2768|Northern attraction anchor inside campus|
| Carousel |4000,2992|4032,3128|Eastern ride court off internal loop|
| Entertainment gateway |3712,3616|3744,3480|Shared southern campus arrival with open middle|
| Ferry terminal |2240,3616|2752,3592|Ticket/waiting frontage beside actual boarding route|
| Mainland pier |2240,3904|2528,3904|One clear promenade-to-boat boarding sequence|
| Island landing |2704,4288|1888,4400|Northwestern arrival connected to scenic loop|
| Island ferry |1760,5080|1776,4272|Alongside water-facing dock edge, corrected after visual inspection|

The rail/platform use1024px native sections cropped from preserved1312px original strips; originals are intact, no architecture is rescaled. Precise art extents, roots and plots are in SITE_FRONTAGES_AND_FOOTPRINTS.json. Every new placement has a stated site purpose. No obsolete collider counts, road hashes or landmark coordinates were frozen to satisfy old tests.

## Artwork, materials and actual Sprite Forge execution

Read AGENTS.md, docs/ART_SKILL_REGISTRY.md, the real upstream generate2dmap/generate2dsprite/generate2dmedia SKILL.md files at Forge `5324342fdfab72430f4e9604f3fe427009f8596d`, and proven Gwanghwamun/Juni production records. No toolchain reinstall, vendored provider SDK, new character generation or generic codeart map substitute.

One actual Codex host `image_gen` call made an original six-material atlas AFTER playable graybox verification: silver civic paving, blue boulevard brick, pearl sidewalk concrete, coordinated entertainment ceramic, maritime-blue coastal paving and natural park trail. Exact prompt/source/hash/provenance are in assets-src/v8-city/source/. Model and price were not exposed; neither is invented. Zero paid-provider API requests. `forge_doctor.py --host-tools image_gen` reports the available host route, optional missing tools and no video-generation route; FFmpeg/Chromium/Pillow/NumPy were reused.

Actual Forge `extract_terrain_tiles.py --strict-qc --edge-policy isolated` extracted six new128px materials; new imagery alone received shared96-color no-dither pixel finishing. Approved old art was not downsampled or globally filtered. Existing original grass/stone/sand/basalt/water and native props were reused. Masks specify geometry; final material pixels come from source imagery. No seamless/Wang certification is claimed.

Actual `map_bundle.py hash/validate`, linked `map_nav.py check`, `export_tiled.py export --embedded-variant`, `compose_layered_preview.py` and `build_scene_preview.py` executed. Full command/stdout/stderr/exit receipts: assets-src/v8-city/commands.json. Human-readable summary: quality/tool-execution-summary.json. Editable native ground/masks,32px reusable atlas, separate props, complete Tiled source and runtime collision adapter are retained. Runtime Tiled collision rectangles match source geometry exactly. Setup validates stored files only and never calls Forge or a generator.

The unchanged upstream Forge browser verifier ran over HTTP (host file:// restriction is known):43routes/95assets, Y-sort and keyboard checks passed, no external requests/errors. This is a Forge diagnostic marker, not the Phaser/Juni gameplay evidence. Real Phaser evidence is separate.

## Runtime and visual review

Actual final Phaser composition:481placements,96prop kinds (94unchanged source PNG kinds plus2native rail/platform crops),586source/runtime collision rectangles,38authored routes.33,057strict samples test full unchanged8×4half-feet plus route shoulders; no blocked samples. Both linked world/room navigation reports pass. New four-case browser coverage includes continuous boulevard/cross-avenue, actual station frontage/platform access, Namsan entrance/full loop, full attraction circulation, waterfront boarding, reciprocal ferry, full Jeju loop, genuine analog mobile movement, DPR3, reduced-motion/portrait pause and accessible controls. The initial test sampler wrongly discarded corners on sparse urban polylines and attempted a diagonal through the station; that test defect was fixed by preserving authored vertices, not by changing physics. Original diagnostic is retained.

Native actual Phaser overview4352×5312, browser overview2176×2656, five native regional review boards, nine native gameplay camera captures with Juni, mobile landscape and matched-source before/after boards are saved here. The building-hidden actual Phaser diagnostic shows the new street/block plan independently of landmark art. Overview reductions and2xdetail use explicitly labelled integer nearest sampling; native crops have no resampling or image filters. QA placements are used only for still framing, never walkthrough traversal evidence.

The first island berth placed the boat partly on land; visual inspection rejected that placement and moved it to1776,4272 in water west of the dock. A preliminary capture was interrupted and is labelled diagnostic, not spliced into final proof. The delivered walkthrough must be recorded from the corrected normal production entry using real joystick/sprint/actions, no QA hooks/placement, fake animation or time changes. Video verification metrics are recorded after capture/encoding.

## Warnings and limits

Compose retains the same seven inherited northern forest edge-canopy clipping WARN IDs: v3-288,v3-296,v3-366,v3-303,v3-311,v3-314,v3-318. No off-canvas roots or empty props. Two compose-only footprint checks are SKIPPED because source bundle collision, not optional placement footprints, supplies physical validity; the independent strict foot/shoulder checker and actual Phaser traversal cover collision separately. Exact raw values/thresholds/files are in quality/tool-execution-summary.json and source audit.json, not relabelled allPASS. Original Juni right-idle/small-wave weak-motion warnings remain in the preserved animation report; no new animation approval is claimed.

Pixels public site/docs/game entry were inspected; live play showed an application-update service notice, so live roaming was NOT observed. Reference study distinguishes official text, supplied gameplay imagery and actual access limits. No proprietary Pixels artwork/layout/economy was copied. This is fictional educational geography, not a historical reconstruction.

Cloud Chromium/emulated mobile and software WebGL are not physical-phone/Safari/hardware-GPU certification. Short uncaptured performance samples are recorded separately; no universal60FPS guarantee. Trains/rides remain scenic artwork, not newly implemented gameplay. Public localhost in this environment is internal, not a user preview URL.

## Verification and checkpoint

Production build/typecheck/source checks, lint/format and12unit tests passed. Four new production browser cases passed before the final decorative boat correction; exact final full-suite/independent install/build/source-parity and remote checkpoint facts are to be recorded ONLY after actual completion in verification.json and the immutable checkpoint annotation. Do not infer CI success from a queued run.

The actual allowlisted ZIP must be HTTP-verified after the final build, including five-district desktop/mobile source-pixel parity, portrait, reciprocal ferry, retained Academy lesson/return, basalt retry/completion and base-town four guests. Security scan excludes editable/private/3D paths and checks token/private-key markers; original notices remain. All editable sources stay in Git, not the portable runtime.

Final checkpoint SHA, exact ZIP/video hashes and actual CI/independent results will be added after verification. No main merge or website deployment. STOP for USER visual approval after the complete handoff; do not declare the map final or expand gameplay.
