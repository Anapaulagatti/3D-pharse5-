# Exact working-plan changes

Historical source: `assets-src/gate25/world-plan-v1.json` (unchanged). New plan: `assets-src/gate3/production-plan-v3-working.json#/plan`. The machine patch round-trip exactly reconstructs the working plan.

- add `/buildings/15`: explicit new record; see plan-diff.json for all values.
- replace `/buildings/6/rect/2`: `390` → `415`
- add `/contentAllocations`: explicit new record; see plan-diff.json for all values.
- add `/paths/29`: explicit new record; see plan-diff.json for all values.
- replace `/paths/9/points/4/0`: `540` → `700`
- replace `/paths/9/points/5/0`: `500` → `700`
- add `/publicExclusions`: explicit new record; see plan-diff.json for all values.
- add `/registrationEasements`: explicit new record; see plan-diff.json for all values.
- replace `/reviewState/gate3`: `"LOCKED"` → `"G3-A_FINAL_REVIEW_PENDING / G3-B_BLOCKED"`
- replace `/reviewState/revision`: `"Gate2.5 working version1 / localized approved Jeju expansion"` → `"G3-A working version3 / controlled finalization; final acceptance pending"`
- replace `/stage`: `"GATE2.5 APPROVED LOCALIZED PLANNING AMENDMENT / WORKING V1"` → `"G3-A WORKING V3 / accepted amendments only; final registration review pending"`
- add `/workingAmendment`: explicit new record; see plan-diff.json for all values.

All land rectangles, platform reservations, tracks, rail keepouts, overpass reservation, heritage buildings, protected main routes, tower, carousel, wheel, ferry and Jeju geometry remain unchanged. The rejected/deferred bakery sites are not active allocations. The station ownership/support detail is a separately marked engineering proposal, not a silently accepted planning amendment.
