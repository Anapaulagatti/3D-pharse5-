# Phase 3B-A validation

| Check | Result | Evidence |
|---|---|---|
| Fresh unit suite | PASS — 171, including original156 | unit.log; old test files unchanged |
| Fresh full E2E | PASS — 72/72 clean full run | full-e2e.log and full-e2e/e2e-results.json |
| Targeted NPC/daily-life/clock checks | PASS — 10 | focused-e2e.log |
| Existing Options/character regression | PASS — 2 | settings-regression.log |
| Typecheck / asset checks / ordinary build | PASS | typecheck.log and build.log; existing checks unmodified |
| Lint / formatting | PASS | lint.log and format.log |
| Native Phaser pixel readback | PASS — 8 real draws, zero unexplained mismatch | NATIVE_QA.json |
| All26 unchanged patrols and approaches | PASS — conservative29×9 contact and critical reservations | navigation-qa.json |
| Seven home zones and actual interaction | PASS | eight normal-speed scene clips and ACTUAL_PHASER_EVIDENCE.json |
| Complete actual accelerated day | PASS — all5phases and midnight; ordinary eligibility | full-day video/trace; no NPC review override |
| Archive lifecycle and Jeju bridge | PASS — actual original WASD, no position/speed override | archive-story and jeju-bridge videos/trace |
| Landscape touch | PASS — browser667×375 | mobile-touch video/native screenshots; not a physical phone |
| Private/public rights gate | PASS — private allowed, public intentionally BLOCKED with zero files emitted | RELEASE_GATE_PROOF.json |
| Source preservation | PASS — 9083 original asset files; 36 original test files unchanged | PROTECTED_AUDIT.json |
| Historical fixture recovery | PASS — 28 missing prior files restored at approved SHA256 | ARCHIVAL_RECOVERY.json; no regeneration |
| Independent private ZIP | See final extraction/launch evidence | PACKAGE_PROOF.json / package-smoke.json |
| Commercial rights / creation terms | UNKNOWN / BLOCKED_PENDING_REVIEW | RIGHTS_MATRIX.json, actual source attempts; no license invented |
| Physical Android/iPhone / hardware GPU | NOT TESTED | no physical evidence |
| Prior art diagnostics / world planning | WARN / FAIL retained | earlier Forge/Creator limits, world issues and source warnings unchanged |

Initial full run exposed a real integration regression: nesting a second summary inside Options broke existing strict menu selectors. It was interrupted, preserved as initial-options-regression-e2e.log, and fixed in the new report UI using a separate button/panel. Original assertions were not weakened; existing settings/Juni/Doyun checks then passed and the full suite restarted. The new test now also checks that Options retains one summary.

A clean worktree initially lacked28 historical PNG fixtures referenced by protected manifests; exact source copies were recovered from the preserved old worktree and checked against expected hashes. They are versioned for reproducible validation and never used as new scene artwork or rejected quality references. package.json is hash-protected and remains byte-identical; release tools use Node/Vite commands without changing frozen scripts or validators.

Technical PASS does not grant artistic replacement approval or commercial clearance. Zero source pixels, actor registrations, routes or collision data are changed. No art candidate is automatically promoted.
