# Original station-platform appearance restored — review required

The rejected connector and all eight derived station-platform layers have been removed from the active Working V3 scene. The original unsplit canopy sprite is restored with its exact original position, pivot, depth and alpha behavior. No art was generated or repainted. Historical rejected assets remain recoverable but are not referenced by the current scene.

- [Native station frontage with Juni](restored-station-juni-native.png)
- [Unannotated native station screenshot](restored-station-native.png), actual Phaser output, 1280×900, zoom1, DPR1
- [BEFORE versus restored platform at 1:1](BEFORE_RESTORED_1X.png)
- [Original BEFORE crop](platform-before-1x.png) / [restored crop](platform-restored-1x.png)
- [Collision overlay at native resolution](collision-overlay-native.png)
- [Exact rollback record](restoration-diff.json), [pixel/hash QA](qa-report.json), [actual movement log](movement-test.json)
- [Playable review ZIP](G3A_PLATFORM_RESTORED_REVIEW.zip): extract and follow `START_REVIEW.txt`; package movement and asset loading verified
- [Collision-only proposal and limitations](COLLISION_PROPOSAL.md)
- [Versioned working plan](../../assets-src/gate3/production-plan-v3.1-restored.json)

Six native comparison regions have **zero differing pixels** against the committed BEFORE reference: whole station artwork, platform, entrance paving, tactile strip and both planter-adjacent pavement zones. The whole-station comparison excludes Juni's changing position/animation. The source PNGs are unchanged; screenshot crops are unscaled. The restored canopy source SHA256 remains `f67c9305e2060a1840cb616bd2e89f17471b6cbeac52097b0c0b1a751585b739`.

The accepted V3 `plan` and `registrations` are byte-equivalent after canonical JSON comparison; only wrapper engineering status changes in V3.1. Maru, western Namsan circulation, cafe easement, facade projections, public exclusions, bakery deferral and existing land reservations remain intact. Ground chunk image references are unchanged. Only the three rejected support-mask additions are rolled back to BEFORE collision data in chunk5-4. The station collider, entrance, canonical forecourt mask and corrected planters are untouched. All 1,352 protected asset hashes and historical checkpoint refs verify unchanged, including the approved forecourt checkpoint.

The overlay uses translucent red for actual blocked mask pixels, a yellow outline for the inherited8px strip, and cyan for the measured attempted movement/stop. It is an annotated technical derivative, separate from the unannotated screenshots.

| Review item | Result |
|---|---|
| Original station-platform appearance versus BEFORE |PASS / zero native ROI pixel differences |
| Approved forecourt, planters, architecture, Juni and protected assets |PASS / unchanged |
| Accepted Maru/Namsan/retail plan and registrations |PASS / exact preservation |
| Native integer placement / nearest sampling |PASS |
| Station-to-platform transfer |FAIL / real movement stops at2958,2690 |
| Collision-ownership opening |NOT IMPLEMENTED / proposal only |
| Existing complete network navigation |Not certified; inherited findings remain in prior route audit |
| Human review of restored presentation |PENDING |
| Physical Android Chrome / iPhone Safari |NOT TESTED |
| Hardware WebGL performance |UNRESOLVED |
| G3-B |BLOCKED |

No new connector, main merge, deployment, mass production or protected checkpoint modification. Stop for human review. Prior V3 opening/traversal claims describe the rejected historical candidate and do not certify this restored scene.
