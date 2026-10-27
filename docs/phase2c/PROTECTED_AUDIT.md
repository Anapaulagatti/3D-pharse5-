# Protected baseline audit

PASS: 5453 approved art/source files and51 protected runtime files unchanged. Exact approved commit `8ef1980131cc743b304b21742cabc6ea4e9bb251`. Permanent non-overwritten approval reference `checkpoint/phase2b-twelve-characters-approved-20261027`. [Full baseline SHA256 manifest](approved-baseline.json), [audit results](protected-audit.json).

| Character | Approved native atlas SHA256 |
|---|---|
| juni | `10a0443213041c4dbf07ea7734d8bc10bc5624ec105d7af79ad8a49d806c50ce` |
| haneul | `b673dc4d40a4304841eaa275d5400e936a3a13c68ddc3e1e91d0eb093bde06cc` |
| bomi | `8b14bf937cd3ec2dd18bd292b5433f0f1b36686051b7a35b7ad922575ec16d26` |
| minjun | `136e1ec1aa742c038421eb067027bd15684f37dbee73d1c2e480477445a9cb1e` |
| ara | `987982ceb63263c64d5c2336ea259249cdf76d0978dd6d0d7f06fc7aaa6b097b` |
| doyun | `dd954385bc8f4b6be75ef1474cfb1ebc7581ae0dc53556eb535553e369b2e6ae` |
| sori | `0a44c110dcad4cb62af0e75a4f0b95169110ebf5a990825a8b64f2dd85c7bd1d` |
| jiwon | `2d5b0137be56261c1ecf27a4a4910fedfcb543a339b6973acb6b232c6103b0be` |
| nari | `f5fb4c87dfdf0be98fc1839e4ea1053148a8433e7b1cdfc672ea6b159f1fc6c9` |
| taeyang | `fd95706b4c235f316a37509f54b4be10e07fb9fef6fbed57fd0d7f1da1fc1394` |
| yuna | `53d9a5d285a9e16d2398ce95607479a5daf5e8257a7d0b0ad092ffc1d028ff66` |
| hyunwoo | `da3f8b90daf859db3ddeb8c38f69df3893a6ce3c15034d6780c8544b6def06a6` |

Default atlases, animation configuration/order, native anchors, gait speeds, identities and historical source/tools are exact. Walk-front hotfix and approved walk-right are untouched. Old10 cosmetic sources/catalog remain immutable; current derived revisions live under `public/assets/cosmetics/phase2c` with explicit provenance. World pixels, physical/contact collision, camera/tour, controller/manager, state and scene transitions are unchanged.

Authorized code changes are restricted to existing Studio/preferences/cosmetic renderer/types/localization plus a new SHA256 utility. Tests were extended for the newly authorized scope; no test was removed/skipped or historical art validator weakened. Old tests that asserted no wardrobe for the new6 were updated to assert real compatible items; frozen runtime/controller source protections remain exact. The missing-art test now asserts recovered default state rather than a transient optimistic selection.

Reproduce: `python3 tools/phase2c/protected.py`. Baseline hash list never changes to accommodate work. No main merge, history rewrite, historical tag overwrite, learning-site modification or deployment. Publication verifies all pre-existing remote references unchanged.
