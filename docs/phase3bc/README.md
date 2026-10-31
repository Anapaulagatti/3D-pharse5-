# Phase3B-C · private review candidate

Owner directive: [HUMAN_DIRECTIVE.md](HUMAN_DIRECTIVE.md). Base `5ced846ca7df9ec3d8996ba0cfd256c55ec0afc7`; source branch `feature/phase3b-c-quests-accessibility`. Recoverable before reference: `checkpoint/phase3bc-before-20261031`.

The currently public26 release remains unchanged: artifact `74235a6e7075b77840d2e9fdf36dce678288cd05`, manifest `db9d4bb68f31c819d79ec95efaad1befce257086e64c41a5c93c2ba6fe7deb2f`. Source-main, productionv0.5, private historical checkpoints and approved art are not publication targets.

Implementation extends the existing NPC manager/dialogue/character compositor, not a parallel actor engine. Three quests: Harin's Jeju collection, Minseo→Jiho book delivery, Cheolsu's practice planting tray beside farm bed4. Existing six world beds remain planted; the tray is a reversible gameplay indicator, not a repaint or a fictional claim that an existing planted plot was empty. Prepare→sow→water is immediate tutorial progression, not a production farming economy.

Four head-mounted items are retired: ara-shell-barrette, kr-hair-ornament, kr-fashion-cap, kr-garden-hat. Active compatible catalog24:10hair/10outfits/4other accessories. Sources/28 historical definitions remain versioned. Saved v1 character choices and v2 appearances/presets survive; normalization ignores retired equipment. Native compositing remains for unaffected cosmetics; no separate floating attachment engine exists. No hairstyle/base/atlas re-export.

Quest state, items, Town Coins, game XP and immutable reward receipts share one atomic local save `korean-arena-quests-v1`. Correct Korean answer is required; wrong answers rotate to a different original beginner question of the same difficulty. No website learning history is asserted, synchronized or modified. No authenticated account/economy/ad provider. RewardedAdAdapter is disabled. Korean educational content requires human review. This local demonstration is not an authoritative server economy; multi-tab last-writer behavior is not certified.

Public update is **PENDING exact manifest approval**. No deploy/main merge/Phase3B-D authorized. See consolidated REVIEW.html and final QA/package records when generated. Real Android/iPhone and hardwareGPU remain NOT TESTED.
