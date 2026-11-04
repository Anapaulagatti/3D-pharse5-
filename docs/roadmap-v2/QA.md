# QA · consolidated local V2 candidate

## Results and exact scope

|Check|Result|Evidence|
|---|---|---|
|Clean clone, dependency install|PASS after cache-path correction;138packages, unchangedlockfile|CLEAN_NPM_CI_SECOND.log; initial denied-cache log retained|
|Type/assets/lint/format/build|PASS clean core; final source checks separately retained|CLEAN_TYPECHECK/ASSETS/LINT/FORMAT/BUILD.log; FINAL_SOURCE_*.log|
|Unit|Clean core222PASS; final223PASS includes strict corrupt-room position check|CLEAN_UNIT.log and FINAL_FREEZE_UNIT.log|
|Full E2E, first clean-clone run|73/77PASS;4FAIL retained|CLEAN_E2E.log, e2e-clean/e2e-results.json|
|Four failures after exact corrections|4/4PASS; not represented as one clean77PASS run|E2E_DOOR_FINAL.log, e2e-door-final/e2e-results.json|
|Farming main actual normal-start|PASS, no inventory/time/position fixtures|farm/FARM_QA.json, FARM_FINAL_QUALIFIED.log|
|Physical3crop lifecycle/two quest unlocks|PASS radish/scallion/carrot; strict5carrotstages; adjacentyoung/mature; exactly-once harvest, realshoptransactions/reward/reload|farm/FARM_QA.json; uninterrupted actual video|
|Three rooms/sign/courier|PASS physical8orderedsteps, correct+incorrectsign/undo, shopbuy/lockedrice, Korean retry/base reward once, roomreload and safeexit|STORY_QA.json; focused first-farm-completed/100coin setup fixture explicitly recorded|
|Native and DPR/mobile browser|PASS3viewports/DPR1/2/3; actualCDPtouch withHaneul, dialog isolation/controlresume, nooverflow, native1×/nearest|DEVICE_QA.json; browser emulation only|
|World navigation|PASS5groups/actualkeys:6farmapproaches,hanokmouthN↔S,stationplaza,bothJejubridgesroundtrip|NAVIGATION_QA.json; no new worldcollisions or ghostmode|
|Protected artwork|PASS10671originalart/sourcefiles unchanged;12oldcropframesbyte-exact|PROTECTED_AUDIT.json, NATIVE_ART_AUDIT.json|
|New code-art numeric checks|PASSalpha/anchor, palette/outlineSKIPPED|ART_QA.json; no all-Forge-heuristics or artistic PASS claim|
|Future live services|Disabled contracts tested; no service provisioned|src/roadmap/contracts.ts; tests/unit/roadmap-v2.test.ts|
|PhysicalAndroid/iPhone/GPU|NOT TESTED|No physical-device evidence exists|
|New art / Korean / commercial acceptance|PENDING HUMAN REVIEW / not certified|ART_PIPELINE.md, EDUCATIONAL_CONTENT.json, ASSET_EXPOSURE.json|
|New V2 public deployment|NOT DEPLOYED; exact new exposure and history-retention approval required|Existing public1a6e5a58 unchanged|

## Why four full-suite tests failed

Three cases immediately clicked a visible door during the valid400msreturncooldown. The product now hides the button until interaction is available; cooldown/movement/collision were not relaxed. Fourth mobile fixture lacked hasTouch:true, so CSS correctly hid its joystick; the fixture now genuinely uses a touch-capable context and CDP touch. All4 reran PASS. The full core73 tests are retained from the clean-clone bab63f0d run; subsequent app differences are the exact door-visibility condition nativehoeicon/ĐấtHạtlabel presentation, and a strict numeric interior-save guard backed by a new negative test. Final223unit and focused4Phaser checks bind those changes. No clean77singlerun claim.

## Main farming evidence

Actual Studio choosesJuni at the normal world spawn, walks toCheolsu and earns starterseed, prepares/plant/waters onecell, waits real growth, harvests, answers and gets one reward. It then demonstrates independent cells/mixedwatering/reload, physically walks toMinseo, buys/sells, accepts marketquest, buys unlockedcarrot/scallion, grows3species, harvests/sells/scoring and completes the second unlock. No direct state writes/teleports or time acceleration. A strict120second carrot sequence provides sown/sprout/young/growing/mature; its youngcell at(416,619) is beside the retained mature radish at(464,619). Earlier6secondintro/45secondradish recording timing overruns are retained, not called absent art or silently clean PASS.

## Limitations

Native PNG readback/crops evaluate texels; H264 videos are lossy review media with unchanged time/dimensions. New code-authored interiors/crops require art review and are not claimed equivalent to a human-approved painted Gate1 scene. All Korean drafts are PENDING_HUMAN_REVIEW; local gameXP/Town Coins never certify mastery or write production learning records. LocalStorage/wallclock are not secure server authority; malformed durations/order/receipts are checked, but real anti-cheat/accounts are out of scope. Performance samples are2.2second cloudChromiumCanvas observations, not guaranteed60FPS or mobilehardware certification. JS chunk warning remains. Original diagnostic FAIL/WARN and interrupted run are listed in QA_RUN_HISTORY.md.

Final ZIP/HTTP extraction proof is recorded in PACKAGE_PROOF.json after freeze, separately from the ZIP self-hash to avoid a hash cycle. Existing public run41852211445 verified1a6e5a58/331cd300; it is a rollback baseline, not this changed V2.
