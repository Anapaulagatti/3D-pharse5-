# Immutable snapshot and rollback

Approved artifact:20674e77c1495474115f5cab16a78b7f6b52d8f8, retained on `candidate/contemporary20-bb2c88af` in the separate reviewrepository. No forcepush or historicalsource/tag deletion.

Declared immutable snapshot: `phases/3b-a/contemporary20-e0f9db0d/`.
Snapshot manifest SHA256: `9abfcea015e3da66df25a56ab9a872d62bfd7bcdc1984894a69cd829829f1215`.
Root approved manifest SHA256: `bb2c88af58107885cdb12d4097621743274f610a6a9188dd5643aa03cb0ea2b8`.

Ownerapproval retained at `approved-releases/history/phase3b-a-contemporary20-20261030.approved.json`. To redeploy/roll back to this already approved exactversion, run the existingworkflow with `operation=deploy` and that immutableapprovalpath, through the same protectedenvironment. If restoring the currentselector after a later release, select this preservedreceipt and commit it as current; do not overwrite the historyrecord or compile/repaint assets. Every retained previouslyapproved snapshot must pass history_gate.py. New content or expandedNPCscope requires separate explicitownerapproval.

This preserves the earlier26canonicalsource/game, Gatecheckpoints and originalv0.5. A rollback cannot silently reintroduce the sixexcludedhistorical-inspiredactors or extraart/media.
