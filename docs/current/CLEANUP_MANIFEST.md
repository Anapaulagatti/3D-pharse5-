# Dry-run cleanup manifest /2026-10-26

Created BEFORE removal. Baseline `a183b1a69f08571acea1a35b4d70185ad95a2257` at `checkpoint/world-art-approved-phase1-20261026` and `archive/world-art-approved-phase1-20261026`.

|Category|Scope|Decision|
|---|---|---|
|A — PROTECTED|All source art, runtime art, atlases, existing tests, tools, packages/licenses, world/collision/camera|KEEP exact; SHA256 manifests supplied|
|B — SAFE TO CLEAN|dist, dist-gate1, dist-gate2, dist-gate3, dist-world-gate1|Remove disposable ignored Vite outputs after this inventory is committed; regenerated from retained sources/configs|
|C — HISTORICAL/RECOVERABLE|Old V6–V10/runtime/review files and old instructions|Keep referenced code/assets/tests. Archive exact prior instruction records under docs/history/pre-phase1; replace active root instructions with concise current pointers. Old prototypes accessible only via explicit historical entrypoints.|
|D — UNCERTAIN|Unclassified files, .cache authoring/QA caches, tooling-cache|KEEP; no proven disposable ownership|

[Per-file inventory](../phase1/cleanup-inventory.json). No broad source-directory deletion. No Git history/tag rewrite. Protected source assets remain in active tree even where old native ownership chains reference historical namespaces.
