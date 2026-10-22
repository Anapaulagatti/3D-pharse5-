# Final visual polish — verification and approval boundary

| Scope | Result | Evidence / remaining limit |
| --- | --- | --- |
| Missing gray district terrain | PASS implementation | Missing-pixel mask is completely filled. Rear paved courtyard and lower low-garden/pavement continuation only. Full native before/after evidence. |
| Approved buildings/entrances/coordinates | PASS preservation | Original upper pixels and facade protection masks compare exactly. No source facade resize/blur/recolor. Spawn, entrance coordinates and district3184×1214 stay fixed. |
| West split foreground | PASS correction | Reuse original whole tree/planter at unchanged native dimensions/x/y/sortY;6,764 tree and13 planter alpha pixels restored. Bikes/lamps remain exact whole originals, not claimed as newly redrawn. |
| East cut painted tree/border | PASS localized implementation; human review PENDING | Sliced road-overhanging tree replaced within the repair band by low complete stone planters/flowers. Existing upright tree, upper streetside assets and buildings retained. |
| Curbs, paint and paving joins | PASS localized implementation; human review PENDING | Two narrow public-realm treatments continue road edges/pavement/stone beds; intact grates/bollards protected. No large prop hiding joins. Human review must assess final material/shadow/vegetation rhythm. |
| Navigation / depth | PASS emulation | Both joins crossed through normal input in both directions; no placement hook in video. Full original foreground Y-sort/softening retained; physical support contacts and local new-bed keepouts amended. New background continuation is not a blanket expansion of all walkable areas. |
| Chunk architecture | PASS bounded prototype |3 native1:1 nonoverlapping windows, adjacent station prefetch, one station request, no repeated loads during route/camera cycles. No full-world streaming-readiness claim. |
| Jeju compositions | PASS distinct framing; human approval PENDING | Coast source viewportY260 versus oreumY0 at844×390; all authored stops50%. Original Jeju art/entrance/Juni unchanged. |
| Tour UI collapse/restore | PASS emulation |2.4s idle collapse; landmark-labelled restore remains visible; scene tap restores; expanded controls outside artwork in tested gutters. Titles, Pause/Resume, Skip and Return reachable. |
| Controls/accessibility | PASS emulation | Real touch joystick and paused pinch; Resume50%; movement intent cancels; reduced motion static selection/no automatic collapse; keyboard focus keeps controls expanded. |
| Landscape UI | PASS emulation |844×390 and740×360,932×430(DPR2),960×432; bounds checked and toolbar rectangles outside artwork. Real safe areas/browser bars remain untested. |
| Fine detail at reduced zoom | LIMIT / not native inspection |50% can lose tiny text/detail by downsampling. Follow and native PNGs remain1:1; no claim that overview/tour preserves every source pixel. |
| Physical Android Chrome / iPhone Safari | NOT TESTED | No accessible connected hardware. Retained original device procedure and concise new checklist/export workflow. No fabricated FPS, memory, thermal or battery PASS. |
| Human final visual/UX approval | PENDING | Native comparisons and videos are provided for explicit approval. Automated PASS is not artistic acceptance. |

## Local source and object inventory

Exactly3 built-in host image edits supplied the missing-background continuation and west/east public-realm repair sources. Prompts/references/original outputs and binary masks are retained under `assets-src/gate25-polish`. Host model/price are not exposed and are recorded as null; no external paid provider API was invoked.

The wide new-background output2033×774 was finished to3184×1214 with nearest sampling **only for newly authored terrain**. The two new repair outputs1024×1536 were finished to512×768 before selective compositing. Existing facade pixels were never resampled. The compositor accepts only the missing-region mask and localized west/east repair bands, plus the small same-tree tip clearance; all changes outside those masks are rejected. Facade/source originals remain recoverable and byte-identical.

West: restore original tree `gate1-5` and planter `gate1-4` alpha; retain whole original lamp/bike sprites and source positions; locally continue lower stone garden bed/flowers/pavement and road-edge paint. East: remove sliced lower painted tree across road, including its stray tip; replace with restrained complete low planted bed; continue curb/paint/paving/stone boundaries, retain original upright streetside tree/bench/lamp and protected grates/bollard. No new oversized decoration is used.

The three runtime windows are[0,0,1512,1214], [1512,0,976,1214], [2488,0,696,1214]. They partition the existing district at native scale; original building positions and approved source files are unchanged. The collision raster inherits previous routes with localized original-support and new-bed keepouts. It is not a generalized modular terrain/Tiled collision pipeline.

## Actual verification

- 7 principal browser cases cover bidirectional district crossing, four-stop tour/composition and idle restore/pause, Skip/movement cancellation, reduced motion and3 additional landscape sizes.3 further checks cover real touch/pinch/resume/cancel, actual report download and5 Overview/Follow cache cycles.
- Native PNG crops compare byte-for-byte to corresponding Phaser screenshot pixels. All original source pixels aboveY787 outside missing regions compare exactly; conservative facade/door masks also compare exactly.219 retained files match hashes, except the intentionally extended review catalog. Original Gate1/working masterplans, Juni and Jeju artwork/entrance are untouched.
- TypeScript, ESLint, formatting,18 existing tests, actor/Juni/northern preservation checks and dedicated Vite build pass. ZIP CRC/manifest and extracted-package runtime checks are recorded separately.
- Actual forward-crossing footage is about17.4s; tour footage about20.6s, with original CDP timestamps, normal-entry Phaser and real controls. No QA teleport or still-image replacement. Reverse traversal is checked in the route log after recording stops.

During the40.31s visible district traversal sample,2,390 raw update intervals averaged16.87ms, p95 histogram18ms, p99 21.5ms, maximum197.4ms,5 intervals over50ms. This includes loading/screenshots/capture overhead in cloud Chromium Canvas, not hardware FPS. Ground textures total15,461,504 RGBA8-equivalent bytes (~14.7MiB); exposed JS heap snapshot78,807,719bytes (~75.2MiB). CPU collision arrays/canvas/decoded images/browser overhead add memory, and texture dimensions are not measured GPU residency. Physical sustained performance, thermal/battery behavior, Safari and full-world streaming remain NOT TESTED.

[Browser/route/video data](browser-qa.json) · [touch/cache/export checks](controls-qa.json) · [native/provenance checks](evidence-checks.json) · [source retention](preservation.json) · [foreground alpha inventory](foreground-restoration.json) · [package hashes](package.json) · [extracted runtime checks](package-qa.json) · [phone checklist](MOBILE_CHECKLIST.md).

Remaining approval: human judgment of join continuity/materials/shadows/density and cinematic/mobile UX; actual Android/iPhone reports. No claim of final production integration or physical mobile acceptance. **STOP and request explicit approval; Gate3 remains locked. No full-world generation, main merge or public deployment.**
