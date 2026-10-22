# Gate2.5 reconstruction — review candidate, NOT artistically approved

The previous polish is **REJECTED**. This replaces its collage-like environmental layout in a new derived scene `district-reconstruction`; the rejected scene and every original source remain recoverable. Gate3 stays locked. No merge, public deployment, new building or full-world integration was performed.

The two runtime boundaries were confirmed as **X1512 and X2488**, full height Y0–1214, from the rejected scene's actual chunk metadata. [Diagnosis](diagnosis.json) records 11 defects, severity, world rectangles and proposed treatment; [annotated map](SEAM_DEFECT_MAP.jpg) labels them. This is wider composition reconstruction, not narrow ownership-edge strips.

## Environmental construction and ownership

A shared cream-paved rear/service promenade, north sidewalk, fixed-width asphalt band, continuous gold road edges, three crossing approaches and connected lower public garden were authored as one environment. The previous long red/cream divider and incompatible eastern garden stacks were removed. The red plaza opens into the cream promenade; low stone beds use one cap/edge grammar. Upper-left daylight and down/right shadows guide the environment. Building coordinates, entrances and protected architecture are unchanged.

| Asset group | Treatment / provenance |
| --- | --- |
| Ground and background landscape | Two built-in host edit calls, clean environment only; [prompts and original outputs](../../assets-src/gate25-reconstruction/provenance.json) retained. Host dimensions2032×774 then2030×775; nearest-neighbor finishing to3184×1214 affects ONLY the newly authored environment. |
| Approved buildings | Original ground RGB restored through [explicit final mask](../../assets-src/gate25-reconstruction/architecture-protection-final.png) and [polygon envelopes](../../assets-src/gate25-reconstruction/architecture-envelopes-final.json). **1,684,029 masked pixels identical**, no facade resampling. Original model/price unavailable; no external paid API was called. |
| Obsolete landscape/props | Ten old derived foreground placements removed, including wrong tree/planter, bikes, benches and lamps; old scene assets retained. Background vegetation remnants replaced by complete planted beds or paved space. No oversized prop hides a seam. |
| Blue crates | Complete source-derived three-crate silhouette, original position, owned contact shadow, alpha sprite with root depth762. Adjacent garbage bin/trunk excluded. |
| Sixteen sidewalk bollards | Each separated from the new environment with own silhouette/shadow, native position, Y-depth818 and measured foot collision. Underpainting uses neighboring same-Y pavers only beneath removed alpha. Reassembly reproduces the authored plate exactly. |
| Runtime ground | **Three** native disjoint windows:1512×1214,976×1214,696×1214. Offline full-canvas authoring plate is never loaded into Phaser. No overlapping ownership. |
| Collision | Protected building projection with8px clearance, station exterior threshold retained,61 conservative garden reserves, crate foot solid and sixteen pole foot solids. Entrances/spawn/targets unchanged and connected. |

Original source artwork, historical northern Korea, Jeju cultural-house approach, Juni atlas/animation, camera/tour/mobile TypeScript and approved Gate1 planning are unchanged. [244-file snapshot verification](preservation.json) allows only the catalog change among existing snapshot files. Main remains33360ed; approved Gate1/checkpoint remains e0a5c0a.

## Evidence and actual execution

[Native full district](AFTER_NATIVE_1X.png) is an actual Phaser export at3184×1214, without debug overlays, camera zoom1; review JPEGs are explicitly resized copies. Native crops preserve the exported PNG pixels exactly. Normal-entry landscape captures show actual play framing. See [review index](README.md) for all before/after pairs and native sections.

- [Actual 1× camera pan](NATIVE_CAMERA_PAN.mp4): desktop mouse drags traverse both joins first at Y0–900, then Y314–1214. No player placement/zoom cheats. The two passes expose full height, including lower foreground. [Camera states](camera-pan.json).
- [Actual mobile-layout walk video](DISTRICT_CROSSINGS.mp4) and PLAYER screenshots: real keyboard input in Chromium touch emulation, no QA placement/speed changes. Forward walk is recorded; reverse walk also executed and recorded in the [test log](browser-qa.json). These are not physical-device recordings.
- [Preserved Jeju tour video](JEJU_TOUR.mp4): existing four stops at50%, title/control collapse/restore, Pause, Skip, Return and reduced-motion checks. Jeju artwork and UX source unchanged.
- [Foreground input test](foreground-qa.json): player above/below the selected pole, actual foot collision; paired gameplay screenshots supplied. Visual interpretation remains human review.

## PASS / FAIL / NOT TESTED

| Check | Result / limits |
| --- | --- |
| Protected facade RGB, source preservation, Juni/native scale | **PASS** within explicit mask; mask completeness still needs visual review |
| Three native chunks / no ownership gaps or overlaps / no duplicate IDs | **PASS**; exactly-once coverage and source reassembly |
| Unchanged entrances and primary route connectivity | **PASS** geometry plus actual walk to entry targets |
| Both joins forward/reverse with normal input | **PASS** desktop Chromium mobile-layout test |
| Poles/crates own alpha, Y-depth and collision | **PASS** ownership/state/input tests; see actual screenshots |
| Camera exposes full height, no missing asset requests or browser exceptions | **PASS** recorded pan and emulated walk; not a lifetime loading guarantee |
| Four-stop tour, reduced motion, controls at740×360/844×390/932×430/960×432 | **PASS** Chromium emulation; physical safe areas/browser chrome unverified |
| TypeScript, lint, formatting, asset preservation, unit tests, dedicated build | **PASS**;18 tests /5 files; dedicated review build only |
| Extracted playable package | See [package QA](package-qa.json) and [ZIP integrity](package.json) |
| Previous polish artistic acceptance | **FAIL — rejected by the user**, retained as history |
| Independent human visual inspection / final A–F art acceptance | **NOT TESTED / pending explicit review**; no self-approval |
| Physical Android/iPhone,15-minute memory/thermal/battery acceptance | **NOT TESTED**, no actual recorded devices available |
| Full-world performance, arbitrary streaming, tilemap integration | **NOT TESTED / unauthorized** |

[Separate visual inspection](VISUAL_INSPECTION.md) records this author's observations of unannotated gameplay/native crops, independently of the geometry assertions. No second reviewer participated. Human A–F judgments remain pending; neither filled pixels nor passing tests establish them.

## Practical limits and handoff

The environment is still painted background art, not a tilemap-ready material kit. Trees in inaccessible garden reserves are baked scenery; the collision reserves are conservative. Extracted foreground uses explicit roots but does not make every rear tree interactable. Newly authored background pixel cadence can differ from the retained source facades after nearest finishing; inspect native crops rather than approving from a small JPEG.

The existing three-chunk bounded cache is preserved, including adjacent prefetch. The whole collision mask is resident; this is not arbitrary full-world streaming. Painted gradients/contact shadows and architectural masks need per-asset authoring before broader reuse; no broader integration occurred. Device memory/performance cannot be certified here.

Use [mobile checklist](MOBILE_CHECKLIST.md), the retained Android/iPhone procedure, and **Options(···) → Export test report** on each actual phone. Attach model/OS/browser and real screen recording to exported JSON. Do not convert emulation results to physical PASS.

**STOP: explicit human artistic review is required. Gate3, merge, deployment and full-world production remain locked.**
