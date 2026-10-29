from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3b-a';p=json.loads((D/'PROTECTED_AUDIT.json').read_text());perf=json.loads((D/'PERFORMANCE.json').read_text());log=(D/'full-e2e.log').read_text()if(D/'full-e2e.log').exists()else'';e2e='PASS — 72/72 clean full run'if re.search(r'\b72 passed\b',log)else'RUNNING — see actual full-e2e.log; partial output is not completion'
def w(n,s):(D/n).write_text(s.strip()+'\n')
w('README.md',f'''# Phase 3B-A — NPC daily life and rights safeguard

Continue from owner-approved `6dbee381fcf1adf79f3f96c931b7170cea2ba076` and verified descendant `4d816228`. Branch: `feature/phase3b-a-daily-life-rights-audit`. The restarted environment required a separate worktree and recovery of unpublished code; [RECOVERY.md](RECOVERY.md) records that limitation honestly. New remote foundation: `435af733`; earlier lost local wave IDs are not claimed recovered.

Implemented through the existing NPCActorModel/FSM/Registry: one deterministic 30-minute world day, 20 individual contemporary schedules, six separate selected era-story routines, individual visitor windows/quiet slots, current-intent dialogue recovery, safe pause/reload/background behavior and bounded cache/persistence. All original entity IDs, art, route coordinates, collisions, native scale, world, twelve characters, 28 cosmetics, Studio and camera/tour remain protected.

The private build includes 26 actual actors and a 26-row rights inventory. All remain blocked from commercial publication pending applicable generation terms and independent IP review. Names, artistic acceptance and successful tests are not legal clearance. No copied specific third-party depiction was substantiated in the limited supplied-input review; no new art or automatic replacement candidate was generated. Generic period fashion is retained; residual royal/naval/photo associations remain review items.

[Native review/gallery and real videos](REVIEW.html) · [Individual schedule table](NPC_DAILY_SCHEDULES.md) · [Clock](DAILY_CLOCK.md) · [FSM/persistence](STATE_MACHINE_AND_PERSISTENCE.md) · [QA](QA.md) · [Protected audit](PROTECTED_AUDIT.md) · [Rights audit](COMMERCIAL_RIGHTS_AUDIT.md) · [Review queue](RIGHTS_REVIEW_QUEUE.md) · [Release gate](RELEASE_GATE.md).

[Private playable ZIP](PHASE3BA_PRIVATE_REVIEW.zip): extract, run `python3 start_review.py`, open the printed localhost review URL. No Node installation or network is needed for gameplay. Fresh storage uses the original Character Studio; choose a character and enter the world. Developer links position Juni at existing validated approaches; they do not represent ordinary visitor availability. [Integrity/extraction/runtime proof](PACKAGE_PROOF.json) records actual measured results.

Current unit suite: 171 passed. Full E2E: {e2e}. Browser/mobile emulation is not physical certification. Physical Android, iPhone, hardware GPU, thermal and battery testing remain NOT TESTED. Shared-browser frame timing has visible outliers and is not a production performance guarantee.

Phase 3B-A only. No shops, planting/harvest gameplay, inventory, economy, quizzes/rewards, ads, AI dialogue, multiplayer, main merge, public deployment or separate learning-site change. STOP for consolidated human review; do not start Phase 3B-B/C/D or Phase 4.
''')
w('QA.md',f'''# Phase 3B-A validation

| Check | Result | Evidence |
|---|---|---|
| Fresh unit suite | PASS — 171, including original156 | unit.log; old test files unchanged |
| Fresh full E2E | {e2e} | full-e2e.log and full-e2e/e2e-results.json |
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
| Source preservation | PASS — {p['protectedAssetFilesUnchanged']} original asset files; {p['originalTestFilesUnchanged']} original test files unchanged | PROTECTED_AUDIT.json |
| Historical fixture recovery | PASS — 28 missing prior files restored at approved SHA256 | ARCHIVAL_RECOVERY.json; no regeneration |
| Independent private ZIP | See final extraction/launch evidence | PACKAGE_PROOF.json / package-smoke.json |
| Commercial rights / creation terms | UNKNOWN / BLOCKED_PENDING_REVIEW | RIGHTS_MATRIX.json, actual source attempts; no license invented |
| Physical Android/iPhone / hardware GPU | NOT TESTED | no physical evidence |
| Prior art diagnostics / world planning | WARN / FAIL retained | earlier Forge/Creator limits, world issues and source warnings unchanged |

Initial full run exposed a real integration regression: nesting a second summary inside Options broke existing strict menu selectors. It was interrupted, preserved as initial-options-regression-e2e.log, and fixed in the new report UI using a separate button/panel. Original assertions were not weakened; existing settings/Juni/Doyun checks then passed and the full suite restarted. The new test now also checks that Options retains one summary.

A clean worktree initially lacked28 historical PNG fixtures referenced by protected manifests; exact source copies were recovered from the preserved old worktree and checked against expected hashes. They are versioned for reproducible validation and never used as new scene artwork or rejected quality references. package.json is hash-protected and remains byte-identical; release tools use Node/Vite commands without changing frozen scripts or validators.

Technical PASS does not grant artistic replacement approval or commercial clearance. Zero source pixels, actor registrations, routes or collision data are changed. No art candidate is automatically promoted.
''')
w('PROTECTED_AUDIT.md',f'''# Protected content audit

Base: `{p['base']}`; approved art/identity reference: `{p['approved']}`. BASELINE.json was recorded before recovery edits to tracked source. Exactly {p['checkedFiles']} preexisting tracked files checked; {p['unchangedFiles']} remain byte-identical. Every authorized code/authority exception has before/after SHA256 and purpose in PROTECTED_AUDIT.json.

- {p['protectedAssetFilesUnchanged']} preexisting NPC/player/cosmetic/world asset files unchanged.
- {p['originalTestFilesUnchanged']} original test source files unchanged; 15 unit and3 E2E cases are additive.
- All26 IDs, native96×112/48,100 registration, 104cells/actor, atlas pixels/JSON and NPCDefinition route/speed/footprint remain.
- Twelve playable characters,28cosmetics/Studio, world masks, collision, camera, tour and old storage contracts protected.
- package.json, lockfile and preservation validators unchanged.
- Zero image-generation calls, actor-art edits, world-art edits or silent candidate promotions.
- 28 prior historical fixture files copied at their already-approved hashes and versioned; see ARCHIVAL_RECOVERY.json. These are exact recovery dependencies, not authored replacement art.

No historical tag or branch is overwritten. The original older checkout was preserved; recovery used a separate worktree. Rollback uses the approved base and removal of only the additive life-clock key if desired. No destructive reset or blanket checkout is required.
''')
w('NAVIGATION_AND_PERFORMANCE.md',f'''# Native navigation and browser performance

All26 approved patrol rings and approaches were independently checked against actual canonical chunk masks plus logical solids, using conservative29×9 contact and critical entrance/bridge/reservation overlap checks. Schedules reference only existing route indices. Movement follows adjacent ring segments through the original footprint/occupied query; no new interior, diagonal shortcut, platform transfer or ground edit is claimed. The station8px strip and other unrelated spatial decisions remain unchanged.

Actual videos cover palace, modern street, station, farm, Jeju, nature/leisure and coast. Continuous original WASD crosses the Jeju bridge and reaches the village. Archive selection shows a fictional story-local routine and restores the living host; visitor conversations preserve their host slot. Normal source-frame, depth and nearest-neighbor rendering are unchanged.

Measured shared cloud Chromium Canvas RAF intervals: {perf['frameSamples']} samples, p50 {perf['p50Ms']:.2f}ms, p95 {perf['p95Ms']:.2f}ms, maximum {perf['maxMs']:.2f}ms. Median RAF rate {perf['observedMedianRAFPerSecond']:.2f}/s is a browser observation, not certified device FPS. Outliers remain a WARN; recording/concurrent shared-host load affects the sample.

During the ordinary accelerated full day: observed active peak {perf['peakActiveActors']}, loaded NPC textures peak {perf['peakLoadedTextures']}, pending-load snapshot peak {perf['peakPendingLoads']}; policy hard caps remain4/4/2. Snapshot intervals can miss shorter load peaks. Estimated peak decoded NPC texture bytes {perf['peakNPCDecodedTextureBytesEstimate']:,} cover NPC atlases only, not all game/browser/GPU memory. Cache loads {perf['cacheLoadsStart']}→{perf['cacheLoadsEnd']}, evictions {perf['cacheEvictionsEnd']}; no eager26-atlas preload. Normal time, quiet slots and culling reduce activity relative to the60× stress recording.

Clock checkpoint remains26 entries, FSM history32 transitions, actor records26; no per-role timer or missed-frame simulation queue is introduced. Inactive models retain their validated position. Actual normal-speed clips, reload/freeze tests and full-day traces complement the source caps.

Physical Android Chrome, iPhone Safari, hardware WebGL/GPU, thermal/battery and long physical-device sessions are NOT TESTED. Browser emulation and software rendering do not certify them. These are remaining review items, not waived by a successful build.
''')
w('VISUAL_REVIEW.md','''# Real Phaser visual review

Open REVIEW.html or the root review page in the extracted private ZIP. Twelve actual gameplay videos show morning café work, palace shift, farm/orchard inspection, commuter repositioning, evening station/harbor, park afternoon, a complete60× ordinary day, mobile touch/return, independent archive behavior and continuous mainland–Jeju walking.

The day recording starts at midnight and reaches the next day without intervening seeks. Ordinary visitor eligibility is enabled; trace identities include multiple residents and fictional visitors. Scene clips use QA to choose an initial phase/validated approach, then run at normal clock rate1. No actor position, walking speed, collision, source pixels or world coordinates are overridden.

Eight genuine canvas readbacks are available at native1:1, plus literal native body/context crops and lightweight gameplay JPGs. PNGs are the pixel-fidelity evidence; encoded MP4s are actual-motion evidence, not lossless pixel proof. All source/native originals remain immutable. Nighttime means the simulated clock phase, with approved scene lighting unchanged as required.

No new sprite art was generated. No concrete copied third-party expression was established in the limited documented input/roster review, so no candidate pack or candidate side-by-side is applicable. Remaining historic royal/naval/photo associations remain qualified NEEDS_REVIEW items; this is not a legal finding of independence. Any future substantiated candidate must be separately versioned and accepted before adoption.

Device screenshots are Chromium landscape667×375 with real simulated touch interaction, not claimed physical Android/iPhone tests. The report's frame timing is shared-host/browser evidence only. No main merge or site deployment.
''')
print('Review docs generated. Full E2E:',e2e)
