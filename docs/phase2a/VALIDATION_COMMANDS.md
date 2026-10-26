# Executed validation

| Command | Result | Log |
|---|---|---|
| npm run typecheck | PASS | [log](validation-logs/typecheck.txt) |
| npm run assets:check | PASS | [log](validation-logs/assets-check.txt) |
| npm run lint | PASS | [log](validation-logs/lint.txt) |
| npm run test |68 PASS | [log](validation-logs/unit.txt) |
| npm run test:e2e |32 PASS | [log](validation-logs/e2e.txt) |
| npm run build | PASS | [log](validation-logs/build.txt) |

The full E2E run preceded the final landscape-resize handler; its targeted mobile/orientation regression subsequently passed [1 test](validation-logs/mobile-rotation.txt). Final typecheck/unit/lint were rerun. Source source-atlas bytes did not change during evidence/report preparation.

The portable compiled build [passed](validation-logs/portable-build.txt). The actual extracted package [passed](validation-logs/package-smoke.txt) all six identities, all four cosmetic presets, real movement, visited/position retention after reload and mobile touch controls with no missing requests or page errors. The final ZIP only adds evidence/documents to that tested runtime; every runtime/build file is byte-compared again after packaging.

[Protected hashes](protected-audit.json), [native actual Phaser readbacks](native-pixel-qa.json), [composition ownership](composition-qa.json), [package smoke data](package-smoke.json). Physical devices remain NOT TESTED.
