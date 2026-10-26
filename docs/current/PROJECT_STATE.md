# Current authority — Phase 1

Human directive: [PHASE1_DIRECTIVE.md](PHASE1_DIRECTIVE.md). Map development is frozen. The full current palace-cleanup world, fresh Hanbit, both bridges, western hanok/garden, NW farm and all other regions are artistically accepted as the gameplay baseline. This does not assert resolution of inherited non-art navigation/planning defects or physical-device tests.

Baseline SHA: `a183b1a69f08571acea1a35b4d70185ad95a2257`; checkpoint `checkpoint/world-art-approved-phase1-20261026`; archive branch `archive/world-art-approved-phase1-20261026`.

Verified accepted runtime: gate3-review.html → src/gate3/main.ts → public/assets/gate3/palace-cleanup-world/manifest.json. Verified production index.html now loads src/game/main.ts then this same scene/renderer/controller, with the character foundation. The existing root src/main.ts/V10 code is historical and must never be selected as the canonical world.

Juni's source/runtime atlas, proportions,144 frames, native96×112 cell/48,100 anchor, distance-driven motion and60/100 speed are protected. World assets, coords/collision and FoundationCamera/Tour remain frozen by SHA256 manifests in docs/phase1.

Current priority: player character registry, manager, selection, local preference persistence, native art quality and real desktop/mobile-landscape behavior. No authenticated account or gameplay progress reset. Haneul, Bomi, Minjun must have distinct authored art and complete animations before becoming selectable.

Future phases: NPC/dialogue/quests, Korean learning providers, inventory/economy and optional rewarded ads as documented contracts only. No Phase2 implementation, learning-website connection or changes to the separate Korean Arena learning application. No main merge or public deployment. Physical Android Chrome/iPhone Safari and hardware performance remain NOT TESTED without recorded evidence.

Cleanup: [dry-run manifest](CLEANUP_MANIFEST.md), [executed audit](../phase1/cleanup-executed.json). Exact old root authority records archived in docs/history/pre-phase1; historical valid code/assets/tests retained when referenced. Stop for human review after delivery; incomplete art must be reported explicitly.
