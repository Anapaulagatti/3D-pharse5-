# Save-compatible per-cell farming

Keep six original bed IDs/world rectangles. Each bed has six44×44cells in2rows×3columns, at48px horizontal pitch. Legacy bed ID maps to its bottom-centre cell; other IDs are-C1/-C2/-C3/-C4/-C6.36unique states in the existing economy.plots dictionary; no competing farming/character engine.

farmCellSchema1 is additive. Six legacy crop/timer/cycle states migrate only to their one matching cell, never cloned to six cells.30new cells start empty; balances, inventory, quests, XP, shop stock and transactions are retained. Migration does not write on read. Existing crop IDs/prices/yields/growMs/introMs remain unchanged. Occupancy is the existing stage/crop; wateredAt gives independent visual moisture; growth stage derives from persisted timestamps and resumes after leaving/reload.

Empty→Eprepare(free/no seed spent)→Eplant(one seed)→Ewater→sprout→young→growing→mature→Eharvest. Harvest animation/tool/particles reuse original world feedback and return tilled-looking soil. Root crop IDs and bound quest-cell references stay stable. Legacy direct model planting remains compatible; actual UI now exposes preparation visibly. Atomic receipts/harvest guard unchanged.

North-row interactions use the existing walkable northern aisle; south-row interactions use the approved southern approach, with per-column anchors and existing34px reachability checks. Tapping a cell never performs work from across the garden. Every cell has its own Zone, root, material layer, crop sprite, wetness, timing and transaction state. No action HTML panels and no full-bed image swaps.
