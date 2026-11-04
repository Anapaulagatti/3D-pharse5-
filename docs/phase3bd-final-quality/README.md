# Final farming art + western hanok review · 2026-11-04

READY_FOR_OWNER_REVIEW · NOT_DEPLOYED. Phase3B-E remains locked.

Build source `b865b6591e7255ec08d5bcaa4c81db26f050e5a4`; evidence source `3081575e1adcf4116477d6f9ef47190c85f243eb`. Branch `feature/phase3bd-farm-art-hanok-quality`, base `09fefd14a0bd2343c5f735090d74ccd787052ebf`.

## Play and inspect

Extract `PHASE3BD_FINAL_QUALITY_REVIEW.zip`, run `python3 start-review.py`, then open `http://127.0.0.1:4483/quality-review/`. Follow Play candidate for the actual Phaser world. The portal is a review index; farming itself uses actual world interactions.

[Native comparisons and five silent gameplay videos](review-assets/index.html). [QA](QA.md), [protected hashes](PROTECTED_AUDIT.json), [exact runtime pixel diff](RUNTIME_PIXEL_DIFF.json), [offline package proof](PACKAGE_PROOF.json), [tool/provenance record](../../assets-src/farming/phase3bd-final-quality/PROVENANCE.json).

Six existing beds now contain36 independently saved cells. Original illustrated component art, fixed native registration,16×16soil parts and40×44crop frames replace the rejected whole-bed overlays. Radish and scallion show seed/sprout/young/growing/mature states, independently wet/dry. Prepare, sow, water and harvest occur directly in Phaser. Legacy six-cell saves migrate additively without duplicating rewards or resetting progress.

Western hanok: old anchor reservation blocked native stone paving near `(534,1377)`. Only `[520,1094,34,284]` is amended in derived passability. Walls/margins remain blocked; original world PNGs and original navigation-mask file unchanged. Juni and Haneul each completed9 real crossing/join legs with walk/run/diagonal/stop inputs.

Fresh213unit and73E2E PASS, no flaky final results. Native source readback8captures exact; screenshot differences outside farm interiors and documented dynamic actors zero. See retained prior driver failures/interrupted suite in QA, not discarded reruns. Forge retains FAIL for2tiny seed/sprout components below64px threshold and WARN for10safe-frame margins. PhysicalAndroid/iPhone/GPU NOT TESTED; human art and Korean-content approval pending.

## Frozen public candidate · approval pending

Artifact `1a6e5a58a8fb515730e553a30980d2ffb7274da6`,4975manifest files; manifest SHA256 `331cd300478f879bab11e9541803dd7c47ba1caaab339263f37150ae6c0d0ce4`.

ZIP SHA256 `8c4df6649aab84d9bbb5f9b4012e5269bbe4b28c7fcae283098a336e9598abeb`,808634415bytes. It is deliberately not committed to Git because of GitHub file-size limits; all source/component art/evidence are versioned and artifact files are pinned individually.

Existing Pages still serves prior artifact `5b5ce278596520efd520f6af63266e57c49c3fd8`,manifest `d170ee180c4743ab8bee4b4a952c7bf1b7f69c2c8083e1b2eb84cf6846beea58`. Rollback tag `checkpoint/pages-5b5ce278-before-final-quality-20261104`. Old snapshots retained byte-exact.

No new Pages run: exact new owner exposure approval required by HUMAN_DIRECTIVE.md E2. Prepared workflow: https://github.com/Anapaulagatti/3D-pharse5-review/actions/workflows/review-pages.yml . Protected environment review remains mandatory. Do not infer live PASS from local/CI evidence. No production/main merge or Phase3B-E.
