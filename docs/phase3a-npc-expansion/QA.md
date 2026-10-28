# Phase3A expansion QA —technical scope20;overall incomplete

|Check|Status|Evidence|
|---|---|---|
|Original unit suite plus9new tests|PASS140|logs/final-unit.log;original131unchanged|
|Full E2E|PASS63|logs/final-e2e.log;original60unmodified +3new|
|Focused new6movement/population/mobile tests|PASS3|logs/final-new3-focused.log|
|Typecheck/assets/lint/build/format|See actual exit logs|logs/final-*.log;no test suppression|
|Native17×104cells|PASS structural|per-NPC native-qa JSON;binaryalpha,0bright-key residue,bounds,connectedmajorparts,distinct clips,packing|
|34independent shoe raster tracks|PASS≤1px|profile-raster-qa.json;nominal44px stance;not an art certificate|
|544own-head comparisons|PASS0changedpixels|head-stability.json|
|Actual canonical before/after native crops|PASS287 /0unexplained mismatch|native-render-qa.json;old11before,new17after|
|Actual5column Phaser comparisons|PASS340sprite readbacks/68captures|inspector-native-qa.json;3walking loops/direction;separate from navigation|
|Actual softwareWebGL native crops|PASS2/0mismatch|extra-evidence.json;SwiftShader only|
|All20patrols/approaches/entrances|PASS scoped|navigation-qa.json;conservative29×9contact,no world edits|
|Real urban entry/re-entry/cache|PASS3roundtrips|urban-stress-qa.json;sampled3active/4loaded;hard4/4/2unchanged|
|Original controls/Studio/persistence/mobile|Regression evidence +new mobile|full/focused E2E,extra-evidence.json;real landmark discovery/reload|
|Third-party art heuristics|FAIL/WARN RETAINED|68Forge:29FAIL/36WARN/3PASS;34Creator square-contract diagnostics|
|Protected baseline/source/test hashes|PASS|protected-audit.json;all7141frozenfiles and approved3manifest|
|Playable ZIP CRC/runtime/extraction|BUILT;see package proof/smoke|package-proof.json,package-smoke.json|
|Requested26total/historical6/index6|FAIL / SOURCE BLOCKED|actual20;0history;0verified icon profiles;14official CONNECT403results|
|Physical Android/iPhone/hardwareGPU|NOT TESTED|no device certification claimed|
|Artistic/anatomy/dialogue/legal acceptance|PENDING HUMAN|No build/framecount/technicalPASS substitutes|

Initial evidence/test-driver issues remain logged:one ViteHMR interrupted capture,one new fixture left Studio open,one test read the world pause snapshot before the next actual frame,and one urban harness shared an E2E-owned preview server. Fixture/drivers were corrected without modifying original tests,production collision or art. Final independently owned preview drives stable real traversal. Failed diagnostic logs are retained,not erased.
