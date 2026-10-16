# Living Seoul — compact royal-to-modern review

The preceding Stage B final polish is complete at97c7d6b, checkpoint/stage-b-final-polish-verified-20261016 (independent clean clone and CI38891178821 PASS). This separately authorized next task is a visual/gameplay candidate; the old town, main, public website, approved source images and Juni144frames remain intact. No full modern district, new NPCs, paid APIs or publication.

## View and play

Download **playable-review.zip** in this folder. Extract the ENTIRE `Korean-Arena-Seoul-Refinement-Review` folder. Run `python3 start.py` (Windows `py start.py`). Python3 is required, Node is not. Open the printed HTTP URL ending `/3D-pharse5-/refinement-review.html`. Do not use file:// or an HTML source viewer. Ctrl+C stops the server. If your browser uses a slow software GPU, add `?renderer=canvas` to that URL. Cloud localhost is not a public preview address; no public deployment was made.

WASD/arrows walk, Shift or Run runs at the original speed; E/Explore interacts. Open the outer gate, follow the stone path north through the open inner gate to the main hall and hanji display. Step outside the outer threshold before closing. Academy to the west has south/east entrances; its hall doorway opens the existing reading room, the desk starts the retained three-letter-name lesson, and the south exit returns to the court. East: invention exhibits and museum frontage; southwest: ONE modern book-and-tea corner. Wave, celebration/social gesture,1×/2×/3×camera, evening, pause, OS reduced-motion and mobile touch remain available. Brand link opens the preserved original town; `production-review.html` retains the previous Stage B world.

## Actual visual evidence

- `quality/review-board.png`: real Phaser district overview, palace and modern corner, clearly labelled overview/thumbnail scale and nearest-neighbour2×detail crops.
- `quality/after-*-native.png`: actual native1×Phaser palace/academy/workshop/museum/modern/opening/garden/occlusion, not concept renders.
- `quality/{palace,academy,workshop,museum}-comparison.png`: native before/after. Academy/workshop/museum use translated-equivalent camera positions. Palace compares the previously empty outer court with the new reachable main-hall destination, not a falsely identical camera pose.
- `quality/palace-avatar-detail-3x.png`: exact screenshot crop, not a new drawing.
- `quality/mobile-native.png`, `mobile-interface.png`, `room-native.png`, `lesson-interface.png` and `evening-native.png`: actual rendered layouts and retained learning flow. Mobile is emulated, not physical-phone performance evidence.
- `quality/gameplay-walkthrough.mp4`: final continuous real keyboard/mouse journey through palace, hanji court, Academy shortcut/room/lesson, workshop service entrance, museum and modern corner. Original `gameplay-original.webm` retained. No QA placement, teleport, injected character frames, sped-up footage or frame duplication.

Final original recording:94.861s,4677actual decoded frames, **49.30FPS average VFR**, target capture60. Runtime across capture/finalization was **58.48FPS**, measured independently from actual Phaser frame-count delta; p50/p95rAF16.7/16.8ms, p99see capture.json. Original-to-H264 relative timestamps match within2ms and frame count is identical. This satisfies a genuine30+FPSaverage capture, but is not a constant60FPS recording. DOM dialogs are outside the canvas video and supplied as separate interface screenshots. Verify raw details in quality/video-verification.json.

## What changed

2304×1920candidate is37.5%less area than the ACTUAL4096×1728playable baseline; original4096×3072plan retained as reference. Whole compound translations keep accepted roofs/native pixel size and relative wings. Straight ceremonial avenue remains; organic public/service/book/garden routes connect distinct destinations. Normal walk60/run100 unchanged. Representative total travel91.56→54.35s,40.6%less; the museum leg is1.55s longer, disclosed in TRAVEL.md.

Palace outer seven wall segments/gaps move together unchanged. The old closed inner reserve becomes a real court, one distinct open inner gate, royal main hall, gardens/lanterns/banners and original hanji interpretation. Only the new hall shifts32pxnorth after native inspection to leave Juni fully readable on its terrace. No claim of faithful historical reconstruction. Academy adds low scholar-garden returns and an east shortcut; workshop has an open timber equipment boundary/service gap; museum and book-cafe keep welcoming open frontages. One modern corner establishes the cultural transition, not an entire new city district.

Five actual host-image calls and pinned Forge processing created11new native props with the existing192palette; retained generated terrain/verges were reassembled under an editable semantic mask.149placements/124statics. Editable source/layers/props/Tiled/bundles/nav and exact command/failure receipts remain in assets-src/world-refinement. Old L-workshop is separated into pixel-exact ownership crops so hall and deep wing sort independently; strict full-RGBA reconstruction proves every approved pixel unchanged. See FORGE.md.

## Performance and limits

The old per-frame canvas GPU readback was a measured CPU hotspot. Cached alpha masks/spatial candidates preserve exact opaque-cue pixels; no repeated source reads during movement. Camera follows the displayed integer root and culling includes viewport size. Canvas is the practical smooth option on this cloud machine. Explicit software-GPU WebGL remains slow; matched before/after/reference measurements and all raw experiments are disclosed in PERFORMANCE.md. No universal60FPS or physical-phone claim. Prior tiny side-idle/wave visual warnings remain inherited; no new animation art was produced. Seamless/Wang tiles are not certified.

Final production/types/lint/format/unit/browser/source/nav/road/portable/CI/clean-clone results are recorded in verification.json and the immutable verified checkpoint tag AFTER observation. Numeric checks are not user artistic approval. Initial composition/capture/road failures are retained and explained; thresholds were not relaxed.

**STOP for visual/gameplay approval before a full modern district or remaining NPCs.** No main merge or automatic publication.

Final visual audit closed two painted gaps at the inner-gate wall joins using TWO instances of the existing approved wall PNG. All147previous transforms,124static colliders/anchors/portals and all source images remain unchanged;149placements now. Strict source-alpha coverage checks all1440closed-wall-foot pixels at row432, excluding ONLY the64pxpassage. Before74px/75pxvisual gaps retained in inner-wall-before-join-fix.json, final zero gaps proven in inner-wall-join-proof.json and actual Phaser screenshot. Source8d7 also passed independent12unit/21browser before this final visual correction; that is retained as historical evidence, not claimed to cover the later change.

Final recording was made again after the joins were fixed. First transcode rounded PTS by13.667ms under the encoder default; unchanged2msprecision check rejected it. Explicit encoder1/1000timebase and MP4timescale1000now preserve every timestamp exactly (0error), same4677frames and no FPS filter. Raw failure log retained. Runtime capture metric includes recorder stop/Blob serialization; unrecorded benchmark timings are separate and exclude that work.

Final root suite:12unit/21browser PASS with0skipped/unexpected/flaky. A late cue snapshot failure was diagnosed by actual per-frame traces, not retried blindly: both algorithms settle to identical974pixels onframe3after QA placement. Four actual engine frames now replace a fixed120mswait, retaining exact count and full screenshot equality. See raw failure/trace/root reports.
