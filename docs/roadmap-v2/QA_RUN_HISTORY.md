# Retained initial failures / changes, not a clean-PASS rewrite

- Initial typecheck: tuple spread from a heterogeneous point array; corrected explicit x/y, no runtime geometry change.
- Initial unit:210PASS/3FAIL because old frozen-source chain correctly rejected newly authorized main integration; added a separate exact V2 before/after amendment layer, retaining all old pins and separate current behavior checks. Native artwork untouched.
- New unit economy check found a negative/too-small margin for a new crop; new-only sale values corrected to cover seed cost plus bounded profit. Original radish/scallion balance unchanged.
- Initial room smoke: borrowed sprite remained in old UpdateList and shutdown destroyed it. Transfer now removes/flushes UpdateList as well as DisplayList.
- Second room smoke: NPC pool evicted an atlas still used by an actor. Pin all current render owners; normal bounded eviction only for unrendered owners.
- Story walk caught outdoor-population cancellation during interior loading. Pause source systems before handoff and wait for existing pending loads; source scene cannot repopulate/cancel while borrowing.
- Queued ScenePlugin.pause was not synchronous for an already-loaded NPC. Use public Systems.pause/resume for exact handoff and avoid same-update outside-population continuation on interior reload.
- Exit event propagated to resumed world and reopened the same door.400msdoor-return cooldown blocks that same event without changing movement/collision.
- Initial farm recorder missed sprout of the6second tutorial after camera-safe reposition under recording load; keep observed intro frames, enforce exact5phase evidence on the normal120second carrot instead. Growth not accelerated or thresholds changed.
- Added room shop button duplicated an old outside data selector (one closed dialog). Room-only shop uses distinct interior selector; outside ABI preserved.
- Initial lint found an unused preexisting QA-driver variable and browser sessionStorage alias in new harness; removed unused variable, made browser scope explicit. No rule suppression.
- Initial full77E2E was deliberately interrupted after inspection found the world-paused joystick guard also blocked indoor touch. Guard now allows active room input but still blocks dialogs/scenic mode; add genuine CDP touch regression, then fresh full suite on the frozen candidate. Original partial log/report retained. This was not an unexplained flaky PASS rerun.
