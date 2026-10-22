# Gate2.5 — implementation, validation and remaining acceptance

Existing artwork/visual foundation and the localized Jeju planning amendment are approved. This report does not convert automated results into human approval of cinematic composition, integration or mobile UX. Gate3 is locked.

| Item | Result | Evidence and limit |
| --- | --- | --- |
| Four-stop Jeju tour | PASS implementation/emulation | Coast→oreum→orchard→house, all authored stops50%; smoothstep2s travel,2.1s hold. Actual four-stop recording, Juni unchanged. Source1024×1536 remains native. |
| Tour controls and coexistence | PASS emulation | Pause/manual drag/pinch/Resume restores50%; Skip; Return native1×; keyboard and joystick intent cancel automatic control; existing Follow/Scenic/Overview retained. |
| Reduced motion | PASS emulation | Static landmark selector, explicit Next and immediate native return; no automatic motion. |
| Reusable tour architecture | PASS limited proof | One additional short Muneum tour; no new artwork, no additional full tours. |
| Working Jeju masterplan | PASS authorized amendment |4352×4864, source frame[3180,3200,1024,1536], immutable Gate1 and mainland/north/station geometry retained. |
| Bridge and landing physical access | PASS technical geometry | Actual normal-input crossing and approaches to both piers and exact island boarding point; source/world registration checked; sea samples blocked. Technical shore/connector, not final bridge art. |
| Three independent sources | PASS native source registration | Muneum→original bakery→station. Full dimensions1536×1024/1024×1024/720×720 kept. Binary ownership only, no source RGB resampling/new art. |
| Join walking, Y-sort, occlusion | PASS emulation | Both joins traversed through normal input; native scene screenshot, explicit depth diagnostic, original foreground ownership clipped to avoid double rendering. |
| Perspective/light/scale | PASS preservation; human judgment PENDING | Native translations keep source proportions/baked lighting; no new light direction or distortion introduced. Final visual compatibility remains a human review. |
| Chunk loading/cache | PASS bounded prototype | First2 chunks plus adjacent station prefetch;3 resident ground textures, one request, no repeat requests or pending chunks at end; Overview waits for required loads. |
| Final seamless production boundaries/materials | FAIL / incomplete | Source envelopes leave unpainted nonwalkable top/bottom margins. Road/sidewalk pattern families differ and are not an authored modular pavement kit. Native close-ups make this explicit. No claim of full-world seam readiness. |
| Pixel sampling | PASS sampled behavior |144 source-terrain pixels per permitted zoom1,½,⅓,¼ match independent nearest rendering exactly; actual camera origin pixel-aligned. This is a sample, not every pixel/object. |
| Tiny text/fine detail at reduced zoom | FAIL for fine-text reading |50% tour improves composition over25% overview, but downsampling cannot preserve every fine pixel/text detail. Use native1× for detailed art evaluation. Overview is orientation only. |
| Tour controls at common landscape ratios | PASS emulation |844×390 plus740×360,932×430(DPR2),960×432; buttons within screen. Real browser bars/cutouts untested. |
| Physical Android Chrome | NOT TESTED | No accessible connected device. Handoff package/checklist prepared. |
| Physical iPhone Safari | NOT TESTED | No accessible connected device. Safari/thermal/battery/sustained hardware performance are not inferred from Chromium. |
| Human cinematic/visual/mobile UX approval | PENDING | Requires direct review; successful builds and route checks do not approve art or usability. |

## Exact integration decisions and localized correction proposals

The district uses Muneum at[0,190], bakery at[1488,0], station at[2464,267], with48px overlap per join. The first trial placed the station atY280. Its upper gold road line was at worldY852–856 versus bakeryY839–846. Translating only the station13px north aligns the line atY839–843. The final recording/screenshots use the corrected position; no facade/door pixels are changed. Station entry is now[2824,697]. Source station scene/reservation remain unchanged.

Different source canvas heights cannot produce a rectangular painted district while simultaneously retaining every native building pixel without extensions. Missing painted coverage is explicitly blocked outside the image envelopes, not filled by invisible paths, oversized props or falsely labelled production art. Proposal for a later **separately authorized** localized art pass: fill only those nonwalkable boundary strips with compatible background context, and author narrow pavement/asphalt transition pieces in the48px join bands (aroundY760–1000) where needed. Preserve all facades/Juni and current physical entrance registration. No such new artwork was generated in Gate2.5.

No walkable pixel falls outside source image coverage. Full-resolution connected-component checks put all three entrances in the spawn component; seam-specific clearance only removes artificial isolated-scene edge blocking over visible sidewalk. Conservative station bench keepouts remain. The district is a controlled spatial prototype, not a replacement for the approved world coordinates.

## Loading, rendering and memory

The scene uses independent native ground chunks, adjacent prefetch and a retained bounded3-texture cache. The native review image is an exported screenshot, not a giant runtime background. The global collision PNG and CPU raster remain resident for this small district; foreground textures are eagerly loaded. It is **not** chunked collision streaming, a Tiled terrain kit, a generalized LRU world streamer or a full-world memory guarantee.

During the final normal-input district recording, the station request→ready was approximately45ms. Three grounds total12,559,360 RGBA8-equivalent bytes (~12.0MiB). Active texture inventory including collision image, Juni/default textures and foregrounds was35,512,532 RGBA8-equivalent bytes (~33.9MiB). Chrome's exposed JS heap snapshot was60,981,063bytes (~58.2MiB). These are not total measured GPU/browser residency; decoded images, CPU RGBA walk data (~14.7MiB), canvas buffers and browser overhead can coexist. Texture memory is a dimensions estimate, not physical-device instrumentation.

The24.19s visible district sample recorded1,412 raw update intervals: mean17.13ms, p95 histogram19ms, p99 25.5ms, maximum240.9ms,8 intervals over50ms. The sample includes initial loading, screenshots and real CDP capture overhead; spikes are disclosed, not a stable hardware FPS claim. A separate18.83s emulated12-cycle camera session recorded mean17.17ms, p95 17.5ms, p99 24ms, maximum266.2ms. Its station load took64.5ms, with no repeated requests, player teleport or reported browser errors. These are short cloud observations; long thermal/battery/memory-pressure acceptance is NOT TESTED.

## Evidence and reproducibility

- Six main browser cases: full recorded tour; Skip/movement cancel; one reusable Muneum demo; reduced motion; three-chunk movement; Jeju bridge/landing traversal. Eight further cases: real touch/pause-pinch/resume, joystick cancellation,12 cache/mode cycles, diagnostics download,3 further landscape ratios and depth/softening diagnostic.
- Four distinct nearest-sampling checks; native source/dimensions/alpha/coverage tests; working-plan bridge/landing/sea checks;201 retained files hash-checked, with only the explicitly extended runtime catalog exempted. Juni, all prior artwork/masks, accepted entrance and original Gate1 plan remain exact.
- TypeScript, ESLint, formatting,18 existing tests, actor/Juni/north preservation checks and the dedicated Vite build pass. Package CRC, manifest and extracted runtime results are linked separately.
- Actual video uses normal-entry Phaser Canvas with real controls, retained CDP timestamps and no QA placement, static-image substitution or time compression. Video/JPEGs are lossy; native PNGs/crops are the pixel evidence. The depth-only QA placement is labelled separately.
- [Main browser/video results](browser-qa.json), [mode/cache/touch cases](modes-qa.json), [nearest samples](zoom-probes.json), [source/collision report](collision-source-report.json), [plan/preservation](plan-and-preservation.json), [emulated exported session](emulated-session-export.json), [package hashes](package.json), [extracted package runtime](package-qa.json), [device procedure](DEVICE_TESTING.md).

Physical-device reports remain `NOT TESTED`; the package supports reproducible LAN testing and exports client/viewport/raw-update/chunk diagnostics without falsely identifying a physical device. Human review must assess comfortable movement, recognizable architecture, attractive tour composition, overview orientation, easy return and district exploration.

**STOP. No new artwork, operational train/ferry, whole-world production, Gate3, main merge, public deployment or separate application changes. Await explicit human approval for Gate3.**
