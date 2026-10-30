# Regression follow-up

The first whole72 run was executed against the local Vite development server while additional captures ran. It is retained, including failures; it is not retrospectively rewritten as a clean72 PASS.

- Haneul's full Studio/movement/switch/reload case hit its existing120s timeout. The same unchanged test passed on the normal production preview in41.4s, with its original timeout unchanged. This supports a timing/load explanation; it is not physical-device performance certification.
- The mismatched-pose fallback test intercepted a hardcoded old `phase2c/.../mapping.json`. The repaired bob correctly uses an additive `phase3bb/...` variant, so the old interceptor no longer corrupted the requested mapping. The test now resolves the actual mapping from the current catalog and asserts the interception happened, before requiring the same default fallback. The standalone production-preview test passed. No fallback guard or assertion was removed.
- Initial unit failures were exact historical hash guards catching the authorized camera/catalog changes. Versioned amendments pin exact before/after SHA256s against the historical source commit; unrelated assets/tests remain checked. The current unit suite passed173/173. Old baseline files/checkpoints are not overwritten.

Current implementation does not alter the approved player/NPC atlases, collision assets, save schema or original movement speeds. Existing tests are retained with scoped preservation-reader and current mapping-path updates, rather than changing thresholds or suppressing known warnings.
