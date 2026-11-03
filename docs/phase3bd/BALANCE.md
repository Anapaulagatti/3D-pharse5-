# Local review economy — configurable, not commercial balancing

| Crop/item | Seed cost | Normal watered growth | Produce yield | Sell/unit | Net/cycle |
|---|---:|---:|---:|---:|---:|
| Radish / 무 |4|45seconds|2|3|+2coins|
| Scallion / 파 |6|90seconds|3|3|+3coins|
| Jeju postcard collectible |12|—|1owned maximum|not resellable|coin sink|

Six managed front rows derive directly from the current six farm-plots.json entries. Existing planted scenery/terrain is immutable; gameplay crop sprites/furrows are separate scene objects inside the cultivated rectangles, approached from original aisle anchors. No new field, empty-grass relocation or collider change.

Nayeon's one-time introductory quest gives one radish seed; its first correctly staged crop grows in6seconds and rewards18coins/20gameXP only after the Korean answer. Minseo's first scallion market quest offers a one-time10second crop at its actual plant objective, then22coins/20gameXP after harvest/sale/return/question. Subsequent crops use45/90seconds. Failed/repeated actions cannot re-arm the intro boost. Existing three quests remain free and offer25/20/20coins and15/15/20gameXP; other education/exploration is never locked behind farming.

Seeds cannot be sold back, produce cannot be bought for resale, postcard cannot be resold. Profit comes only from actual seed→plant→water→elapsed growth→one harvest→sale. Shop seed stock is50pertype in this small local review, collectible stock5; no automatic restocking or offline auto-harvest. Inventory12distinctstacks,99units/stack, postcard1; wallet1million cap. Every mutation commits wallet/stock/items/plot/counters/receipt atomically or preserves all previous values.

Wall-clock timestamps persist in the existing quest save. Growth is clamped to nonnegative elapsed and at most24hours, with no spoilage or forced long tutorial wait. Reload/resume never creates repeated harvests. Clock changes/client storage are not trusted as server ownership: local review only. Receipt ledger4096entries refuses further operations rather than forgetting replay protection; multi-tab refreshes reread storage, but this is not a certified distributed database.

No real-money currency, Korean mastery/SRS/test-score mutation, Supabase learner write, ad SDK, paid API, live auth or multiplayer. RewardedAdAdapter remains DISABLED. Korean content remains PENDING_HUMAN_REVIEW.
