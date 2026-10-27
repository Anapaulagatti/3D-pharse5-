# Animation compatibility and source ownership

Approved native96×112 frame registration, foot anchor48,100, phase names/order, walk60/run100 speeds and character identities are immutable. Juni’s packed source has144 cells; other actors112. No approved atlas is re-exported.

## Foundation before expansion

The original old outfit patches were authored against older front-walk poses. Reapplying those full-body patches could paint old arms/legs over the newly approved motion. Derived patches now use each actor’s approved pose ownership, preserving native head/face and current arm, knee, contact/lift order. Four old outfit variants ×8 front-walk cells were rebound. Hair/accessories were checked for body leakage and bind to the current base hash; obsolete front garment interaction cells are explicitly empty. Original source textures/catalog remain recoverable unchanged.

Actual canonical Phaser foundation:10 single-item looks plus4 old suggested combinations ×14 clips =196 native readbacks,0 mismatch. [Gate](foundation-gate.json), [readbacks](foundation/native-pixel-qa.json). Expansion followed checkpoint5d79429 and a Juni/Sori three-item pilot,28 actual clips,0 mismatch ([pilot](pilot-gate.json)).

[Original patch versus corrected outfit source sheets](REVIEW.html) are explicitly SOURCE ONLY. They reproduce original patches on the current approved base to expose the stale-pose ownership issue; they are not before gameplay footage. Final current gameplay is independently captured.

## Current native pipeline

Each sparse paint/erase variant records the base PNG SHA256, content revision and per-cell offsets. Before use the renderer hashes the loaded base image and requires both variant and mapping bindings to match. Cache keys include base digest and all applicable patch/interaction revisions. Invalid/missing assets or pose mismatch restore approved defaults safely.

Composition order: approved base → non-accessory item patches → before-accessory ownership corrections → accessory patches → any declared after-accessory corrections. Native integer offsets and binary alpha, smoothing disabled; no frame rescaling. Existing Canvas composition and Phaser manager/controller remain the only engines.

Hair follows approved head displacement, including raised run/gesture poses. Head matching spans ±9vertical pixels, covering the approved −7…+5 range. Long hair is behind body/hands and restored over garment shoulders only where appropriate. Hats clear the old hair footprint while preserving the face; round glasses disappear from the rear. Garment masks preserve foreground hands. Festival skirt correctly occludes lifted shoes behind fabric while preserving support soles below the hem. Default footwear is intentionally retained where it carries approved contact anatomy.

## Coverage and evidence

- 46 variants /5,248 registered native cells; no absent mapping keys. Explicit null is intentional hidden geometry, not an export omission.
- 192 compatible appearance combinations /21,760 composed source frames checked offline, including supported start/stop/turn cells. No eager runtime permutation generation.
- All12 curated looks: actual idle4 +walk4 +run4 +wave +celebrate =168 clips. Every claimed new variant appears on both compatible actors. All8 walk/run phases observed; idle2. Default front/right comparisons add24 clips:192 final native captures,0 unexplained opaque-pixel mismatch.
- Actual movement recordings include direction changes and start/stop transitions through the unchanged controller. Exhaustive individual transition-cell coverage is source-side; no claim that every transition frame was separately captured by the camera.
- Existing character-motion E2E covers default movement; all12 default atlases and motion registrations remain exact. No old right/back/run cycle was rewritten.
- [Actual final readbacks](gameplay/native-pixel-qa.json), [source QA](source-qa.json), [all12 gameplay videos](REVIEW.html), [phase-aligned Juni reference source front](walk-front-approved-reference-source-native.png), [right](walk-right-approved-reference-source-native.png), [back-run](run-back-approved-reference-source-native.png).

Native RGB readback proves renderer/source agreement, not artistic acceptance. The complete attire, silhouette, timing, hair/hat fit and garment aesthetics remain for human review. Historical Forge motion WARNs remain in their original Phase2A/B reports; thresholds were not weakened.
