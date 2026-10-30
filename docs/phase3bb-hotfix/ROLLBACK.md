# Review rollback

Original source/checkpoints remain unchanged. Before this task: checkpoint/phase3bb-before-hotfix-20261030 -> ddd52849566fb3c1734570d6ff8562fbf7ef4026.

The approved20 artifact remains20674e77c1495474115f5cab16a78b7f6b52d8f8, exact root manifestbb2c88af58107885cdb12d4097621743274f610a6a9188dd5643aa03cb0ea2b8. Its old snapshot is retained byte-for-byte in the new candidate at phases/3b-a/contemporary20-e0f9db0d/, including snapshot manifest9abfcea015e3da66df25a56ab9a872d62bfd7bcdc1984894a69cd829829f1215.

No force push or tag replacement. The new immutable compiled candidate is a separate root Git history with no canonical private ancestors or configured remote, pending exact owner publication approval. Promote only that pinned payload through the existing receipt/hash/history gates and protected github-pages environment.

After an authorized new release, retain both approved history receipts. To return to20 without discarding new snapshots, prepare a new composite export with the original20 root bytes plus all previously approved immutable snapshots; do not rewrite historical asset manifests. Bind the exact rollback export in a reviewed receipt and use the same workflow/environment. Do not bypass history_gate.py or quietly delete newer approved snapshot history. Before any first new release, old20 remains current and requires no rollback action.

Productionv0.5 is in a separate destination and is never touched.
