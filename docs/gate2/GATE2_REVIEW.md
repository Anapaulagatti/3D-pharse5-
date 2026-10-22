# Gate 2 artistic review — three playable slices

Gate 1 baseline `e0a5c0a` remains unchanged. Work is isolated on `art-gate/gate2-three-slices`. **Human artistic approval is pending. Gate 3 stays locked.** No whole-world rebuild, merge, public deployment or separate application change.

| Slice | Native Phaser capture | Enlarged review | Juni / architecture | Actual gameplay | Playable ZIP |
| --- | --- | --- | --- | --- | --- |
| A · Historical north | [1536×1024, 1:1](A_NATIVE_1X.png) | [2× nearest](A_REVIEW_2X.png) | [Native crop](A_ARCHITECTURE_1X.png) | [18.17s MP4](A_GAMEPLAY.mp4) | [A + transition](A_PLAYABLE.zip) |
| B · Modern street | [1536×1024, 1:1](B_NATIVE_1X.png) | [2× nearest](B_REVIEW_2X.png) | [Native crop](B_ARCHITECTURE_1X.png) | [21.37s MP4](B_GAMEPLAY.mp4) | [B + station + transition](B_PLAYABLE.zip) |
| C · Jeju coast | [1024×1536, 1:1](C_NATIVE_1X.png) | [2× nearest](C_REVIEW_2X.png) | [Corrected hall / Juni](C_ARCHITECTURE_1X.png) | [22.31s MP4](C_GAMEPLAY.mp4) | [C](C_PLAYABLE.zip) |

Extract a ZIP, run `python3 start.py`, open the localhost URL printed by the script. No dependency install. WASD/arrows move; Shift runs; E explores; Space greets. Mobile landscape has an analog joystick and run/explore buttons. Normal entry has no QA placement hook. These are independent exterior review scenes; the ferry and railway operation remain future features.

[Side-by-side Muneum comparison](MUNEUM_SIDE_BY_SIDE_1X.png) uses four 768×768 crops at equal pixel pitch: approved Muneum, historical A, modern B, Jeju C. View at actual size. B deliberately retains the approved Muneum foundation and support props at 1:1; it is not claimed as newly generated architecture. Its new architectural supporting study is the station. No rejected V6–V10 southern art/layout was used as a reference.

[Historical-to-modern native transition](TRANSITION_NATIVE_1X.png) · [2× review](TRANSITION_REVIEW_2X.png). The shared stonework, planted garden, walls, daylight and public sidewalk join the historical gate to contemporary storefronts. It is a playable art study, not an applied replacement of the approved full-world transition geometry. The closed compound remains private; its disconnected interior was removed from public collision space.

[Station / Juni native study](STATION_NATIVE_1X.png) · [2× review](STATION_REVIEW_2X.png). A recognizable station building, large entrance, clock/signage, forecourt, crosswalk and side canopy test the station/forecourt relationship. The retained approved masterplan still reserves platforms, tracks and pedestrian links; this supporting study does not build the rail system. The square1254px authoring output was uniformly finished to720px, without cropping, giving an approximately555px-wide station and120px doorway beside Juni’s80px body. Its conservative555×220px collision reservation is10px deeper than the approved560×210px building reservation: review a localized10px threshold allowance before integration. No reservation was silently changed.

## Jeju fit conflict — proposal only

**The approved720×1260px land reservation does not fit this artwork at native scale.** C remains a1024×1536px study with water margins and roughly910×1380px painted land. No artwork was shrunk to make it fit. The first generated cultural hall had an undersized doorway; visual Juni comparison caught it, the original is retained, and a targeted host edit enlarged the hall to roughly390px width with an approximately100px-tall doorway. Its approach and east-side route were corrected and rechecked.

[Localized proposal data](../../assets-src/gate2/plan/jeju-localized-proposal.json): place the study frame at[3180,3200], extend the world canvas from4096×4608 to4352×4864 for eastern/southern water margins, and preserve mainland/northern coordinates. The painted shoreline is approximate, not a final collision polygon. Align the upper arrival with a short connector from approved mainland shore[3160,3480] to study bridge endpoint[3180,3560]. Review moving the lower landing from[3240,4100] to[3180,4020]. These connector/landing changes are disclosed, **not applied** to the approved plan. Ferry gameplay is absent. Please judge this localized proposal alongside the native-scale scene.

## Explicit art judgments

These are the implementer’s review judgments, not human artistic approval. PASS means suitable for this slice review; no result unlocks production expansion.

| Criterion | A · Historical | B · Modern | C · Jeju |
| --- | --- | --- | --- |
| Architecture | PASS — tiled roofs, timber, gates, stone foundations, hanok and palace elements | PASS — four distinct full-size approved Muneum facades; station supporting study | PASS — corrected full-size cultural hall with readable entrance; volcanic setting |
| Materials | PASS — roof/timber/stone distinction | PASS — glass, brick, plaster, asphalt, shop detail | PASS — basalt, timber, roof tile, orchard, coastal vegetation |
| Depth | PASS — roof overhangs, steps, wall layering and native foreground masks | PASS — layered storefronts and Y-sorted street props | PASS — cliff terraces, stairs, canopy masks and hall layers |
| Lighting | PASS — warm upper-left daylight with lower-right cast shading | PASS — matching warm daylight and interior light | PASS — matching sun direction, cliff/contact shading |
| Composition | PASS — clear east axis and courtyard/frontage hierarchy | PASS — connected commercial sidewalk and crosswalk | PASS — arrival, oreum, orchard and culture are distinct connected areas |
| Scale | PASS — native Juni and retained approved historical colliders | PASS — native approved street; station10px depth allowance flagged | **FAIL for approved world reservation** — native hall/Juni proportion corrected; wider reservation proposal needs human review |
| Navigation | PASS — all3 destinations reached by real input | PASS — all5 destinations and courtyard reached | PASS — all5 destinations reached, including oreum; corrected hall-side route |
| Pixel clarity | PASS — native zoom1, nearest sampling; 2× copies use nearest only | PASS — original benchmark pixels retained | PASS —1024×1536 native art; no spatial downscale |

The artworks share a deliberately rich, dense style; whether that reaches the Muneum craftsmanship bar is your artistic decision. No successful build, route check or asset count substitutes for it.

## Technical QA and provenance

[Concise technical report](TECHNICAL_QA.md) · [generation/source manifest](generation-manifest.json) · [protected-source hashes](source-preservation.json) · [browser checks](browser-qa.json) · [video provenance](video-provenance.json) · [ZIP hashes](packages.json).

Original host outputs, exact prompts, references and finished sources are retained under `assets-src/gate2`. Five host image calls were used, including the Jeju correction; no paid provider API was called. The host exposes no actual model name or price, so those fields are null. New art is generated/finished artwork, not claimed as hand-drawn. The station authoring finish is explicit; A/B/C/transition retain1:1 spatial dimensions. Juni’s original atlas, identity, frame size, animation and foot anchor are unchanged.

**Stop: awaiting explicit Gate 2 human artistic approval and a decision on the localized Jeju/station fit proposals. Gate 3 remains locked.**
