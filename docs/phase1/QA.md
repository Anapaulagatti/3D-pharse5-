# Phase1 QA — roster INCOMPLETE

**This is a technical-foundation review, not completed Phase1 acceptance. Only Juni is playable.** The user directive§4.2 explicitly allows a completed technical foundation with unfinished art honestly identified; the four-playable-character milestone remains unfulfilled.

|Deliverable|Status|Evidence / limit|
|---|---|---|
|A: approved world freeze|PASS|Baseline a183b1a; immutable checkpoint/branch;3082world/source files and224Juni files unchanged;91collision binaries and logical coordinates exact.|
|B: safe cleanup/current authority|PASS|Pre-delete committed inventory;517old build files/118124367bytes removed; exact historical instructions archived; no protected source/tools/tests removed. Root defaults to approved current world, V10 is explicit history only.|
|C: character architecture|PASS technical|Typed/runtime-validated4identity registry, transactional sprite manager, native clips/contact gating, one original controller, modal selection, versioned one-key storage. Unknown/corrupt/denied storage safely resolves Juni. No progress reset/account service.|
|C/D: four completed native characters|**FAIL / INCOMPLETE**|Juni144approved frames exact. Haneul pilot+targeted repair fail opposite-leg cycle and source registration. Bomi/Minjun only have original design references; no motion atlases. All3disabled, no placeholders or procedural hero substitution.|
|D: native gameplay art evidence|PARTIAL|Actual1xPhaser Juni, all4walk/run directions and emotes, scale beside approved environment, before/after world evidence. No genuine native four-character group/motion pack exists; no fake in-world collage supplied.|
|E: core checks|PASS|Typecheck, assets, lint,44unit/10files,build,20e2e.5current production checks;15historical regressions retained separately.|
|E: frozen pixels/rendering|PASS|6,868,992world pixels across6same-camera Canvas/WebGL pairs:0differences outside original Juni animation-time rectangle. Native integer camera/nearest preserved.|
|E: Juni bridge regression|PASS representative|BridgeA walk out/return,bridgeB run out/return:1839native foot samples0unsupported; genuine pose readbacks0unexplained changed Juni pixels. No position/pose/speed/collision overrides.|
|F: actual selectable/switchable new avatars|INCOMPLETE|Juni selection/reconfirmation works in-engine; async replacement/scene-lifetime ownership verified with unit-only fixtures.3new production avatars not available; no claim of live4avatar switching.|
|Physical Android/iPhone,hardware performance|NOT TESTED|844×390/DPR3Chromium touch emulation and browser Canvas/WebGL do not certify real devices or hardware FPS/memory.|

Initial failures are preserved: old preview server ownership caused7connection-refused tests, resolved by a fresh owned port; first bridge return driver allowed0.7px error, rounding into a blocked corner, fixed only in QA waypoint precision to0.3px. Neither issue caused map/controller changes. Native frame-source gait data remains8unique walk and8run frames per direction; short actual screenshots/videos observe real timing rather than injecting every frame. Complete motion counts and real coordinates are in input-gameplay.json.

[Actual check logs](checks.json) · [Initial checks](checks-initial.json) · [World/Juni hashes](preservation-qa.json) · [Native captures](native-captures.json) · [Bridge body/foot QA](bridge-regression/body-clearance.json) · [Art status](character-art-status.json) · [Source/provenance + raw matte/validator warnings](SOURCE_PROVENANCE.md).

Native source PNGs are exact canvas readbacks. Browser JPEGs are UI reviews. Native context crops preserve1:1; lossy videos are motion evidence and retain original duration. A green build/test never grants character artistic approval.

No map generation/art changes, original source overwrite, paid external provider call, main merge, deployment or separate learning-app change. No Phase2 implemented. Bakery and other inherited spatial/navigation questions remain frozen/separate; no whole-world gameplay-completion claim. STOP for review; finishing3native character animation packs remains a blocking Phase1 task.

Known device-usability item: sharp bridge corners still use the frozen native support envelope. Agent steering regression passes with precise real joystick input; comfortable physical-finger turning and device performance remain unverified. No map edit was made to conceal this limitation.

Final extracted portable ZIP:5production browser tests PASS plus9world entries and native-first-launch confirmation PASS. Actual native station canvas matches the development evidence with0world-pixel differences. [Final package browser report](package-final-e2e.json) · [Entry/native checks](package-smoke.json). Source checkpoint `checkpoint/phase1-foundation-sources-20261026`; review checkpoint `checkpoint/phase1-foundation-review-20261026`.
