# Phase2B — focused locomotion correction review

Six character designs preserved. Corrected motion is a **review candidate**, not human-approved. Phase2C remains LOCKED. No main merge or public deployment.

Open [visual review](REVIEW.html) for six synchronized Juni comparisons and separate unretimed actual Phaser recordings. Download [playable review ZIP](PHASE2B_MOTION_CORRECTION_REVIEW.zip), extract, run `python3 start_review.py`, open `REVIEW.html`. The package contains the real compiled canonical Phaser world and twelve playable characters, with existing cosmetics and persistence. Use WASD / Shift; the existing mobile joystick remains unchanged.

Only Sori, Jiwon, Nari, Taeyang, Yuna and Hyunwoo motion pixels changed: front/back/right walk/run and matching starts/stops,66 cells each. All left clips, idle/emotes and character designs remain exact. Juni, Haneul, Bomi, Minjun, Ara, Doyun, cosmetics, world, UI, controller, camera, collision and progress code are byte-identical.

The old right-foot stance moved along with positiveX travel. The repair changes limb construction and support trajectory, **not clip reversal or runtime speed**. Front/rear corrections add real knee articulation and appropriate own-foot heel/sole views using Juni's actual phase indices. Related runs showed the same source defects and are repaired. See [diagnosis](MOTION_DIAGNOSIS.md).

Evidence:1,008 exact native opaque-pixel readbacks,42 actual clips (Juni plus6),126 sampled consecutive loops. Source contact tracking rejects the old right motion (34px walk/48px run drift), corrected keyposes are within1px. Actual sampled support drift is1–8px from8-pose hold/phase sampling; this is not continuous subpixel foot locking. Visual naturalness remains for human review.

- [QA and unresolved items](QA.md)
- [Native/source/gameplay evidence index](VISUAL_REVIEW.md)
- [Exact changed frame/pixel hashes](frame-change-manifest.json)
- [Protected-asset verification](protected-audit.json)
- [Actual motion and contact evidence](actual-motion-qa.json)
- [Original Forge thresholds and retained warnings](FORGE_WARNINGS.md)
- [Source provenance](source-provenance.json)

Review references: `checkpoint/phase2b-motion-before-20261027` (bcdbf17 baseline); `checkpoint/phase2b-motion-corrected-review-20261027` (new review). Original rejected review and all historical checkpoints preserved. Checkpoint IDs and package hashes are recorded in the handoff receipt.

Physical Android Chrome/iPhone Safari, hardware WebGL performance and human artistic motion acceptance remain NOT TESTED / PENDING. No Phase2C work authorized.

Recovery validation completed:93/93 unit tests,46/46 full E2E (0skipped/0flaky),1,008 retained native frame comparisons reproduced. Independent extracted ZIP:12 characters,4 preserved cosmetic presets,reload/progress,mobile-landscape touch;6 additional native package readbacks exact. All6 actual gameplay videos are included in the portable package as compression-only derivatives; original videos are preserved separately. See [recovery QA](QA.md) and [package checks](package-native-readbacks.json).
