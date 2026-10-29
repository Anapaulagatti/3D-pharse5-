from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-identity-safeguard'
log=(D/'full-e2e.log').read_text();complete='69 passed' in log
status='PASS — 69 tests, clean full run' if complete else 'RUNNING — final status is not inferred from partial results'
audit=json.loads((D/'PROTECTED_AUDIT.json').read_text())
(D/'QA.md').write_text(f'''# Fictional identity safeguard — QA

| Check | Status | Evidence |
|---|---|---|
| Unit suite | PASS — 156 tests | unit.log; previous identity validation retained, three new safeguard tests |
| Full E2E suite | {status} | full-e2e.log and full-e2e/e2e-results.json |
| Focused identity and ordinary-world checks | PASS — two tests | focused-final.log; 36 nodes, six aliases and accessible labels |
| Typecheck and production build | PASS | build.log, including typecheck |
| Asset validation | PASS | build.log runs the existing assets:check without suppression |
| Lint and formatting | PASS | lint.log and format.log |
| Actual native Phaser fidelity | PASS — six draws, zero opaque-pixel mismatch | NATIVE_QA.json |
| Protected baseline | PASS — {audit['frozenAssetFilesUnchanged']} asset files exact; {audit['all26PublicNPCAssetFilesExact']} public NPC files exact | PROTECTED_AUDIT.json |
| Non-presentation NPC properties | PASS | fictional-identity.test.ts compares every property except names/occupation |
| Public personal identities | Six requested fictional names; no historical personal names in dialogue/menu/accessible labels | targeted unit and actual browser tests |
| Saves and world state | Existing IDs and storage unchanged | original reload/progress, lifecycle and ordinary-world tests |
| Offline package | See independently measured extraction/launch result | PACKAGE_PROOF.json and package-smoke.json |
| Commercial depiction / generation terms | UNVERIFIED — not legally certified | DEPICTION_REVIEW.md and current rights matrix |
| Detailed historical facts / real-person fact cards | Disabled; zero verified | preserved source records; no new factual claims |
| Physical Android / iPhone / hardware GPU | NOT TESTED | desktop browser evidence is not physical certification |
| Existing art and spatial diagnostics | WARN / FAIL retained | prior Forge 13 FAIL / 11 WARN, Creator limits and existing world issues are not erased |

The owner-directed fictionalization is not a name-only legal clearance claim. The public mapping removes original historical names; internal provenance and stable ID references remain intact. All six notices explicitly identify fictional characters and invented game narration, not historical people or quotations. No actor motion, collision, route, atlas, source artwork or world geometry changes.

During development, a new decision-status value initially failed the old single-status schema; it was resolved by an explicit owner-precaution decision type without claiming independent legal clearance. Rights-based fallback still requires its original independent-review status. An obsolete quotation-notice expectation was changed to require fiction. The new movement test also needed the same explicit canvas focus used by existing traversal harnesses. Current reports show actual final runs; no test, validator or failure threshold is suppressed.

Phase 3B is handoff only. No main merge, deployment, paid art call or separate website change.
''')
print('QA full-suite status:',status)
