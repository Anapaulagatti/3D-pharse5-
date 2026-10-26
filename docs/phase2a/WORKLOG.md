# Phase2A working log — implementation ongoing

Human directive authorizes full Phase2A; do not stop at the previous Phase1B approval gate. Phase2B/main merge/deploy remain forbidden. No subagents.

- Approved4 baseline51ac4b4, permanent approval tag checkpoint/phase1b-four-characters-approved-20261026. Freeze committed first at b86ae0f on feature/phase2-character-studio. SHA manifest871 source/runtime/tool files plus frozen definition snapshots and4 identity records; all unchanged. World3082/Juni224 hashes exact.
- New Ara authored and inspected in native8-direction gait sheets and actual Phaser8-clip pilot BEFORE Doyun was generated. docs/phase2a/ara-first-validation.json records order and0 opaque readback mismatches.
- New Doyun authored112 frames,34clips,64 unique gait frames, native source sheets inspected. Needs final actual in-engine evidence/QA alongside cosmetics.
-7 real builtin host-image generations:2 independent identities,4 alternative hair/outfit static turnarounds,1 accessory prop sheet. No animation sheets generated, no external paid API. Raw sources copied under assets-src/characters/phase2a; original generated_images retained.
- New2 defaults have112-frame own-layer packs; four front/back gait clips use the immutable Juni template; profiles use validated PNG-layer contact IK. Original4 pixels/configs/source/tools never re-exported.
- Catalog10 items:2 hair +2 complete outfits EACH for Ara and Doyun; Ara shell barrette and Doyun linen neckerchief. All112 source poses covered; barrette intentionally hidden in right profile. Sparse native erase/paint packs, not loose runtime accessories.
- Four tiny raised-sleeve/hair interaction packs fix non-commuting pair occlusion. All36 combinations /4032poses now match direct own-layer construction at0 pixels difference. Initial152-pixel failure retained under history/composition-before-occlusion and resolved. composition_qa.py output includes source asset hashes.
- Existing CharacterSelection is upgraded Studio; existing Manager reuses one actual Phaser sprite via setTexture; same-identity cosmetic changes retain motion object. RegistryMotion.step unchanged; new adopt method handles feasible cross-identity phase retention. Existing JuniMotion/camera/contact/world remain exact.
- Additive v2 AppearancePreferences preserves v1 key. Typed appearance/cosmetic manifests, source patch compositor at load, caches base2/composite2 and Phaser actor3 (+1 staging). Gallery uses only tiny previews; no full-atlas eager preload. Future6 slots metadata-only; current6 playable.
- UI prototype tested at1280x900,844x390,667x375. Latest CSS hides optional emote preview buttons and repetitive gallery status on small landscape to fit full native preview and direction selector; gameplay mobile emotes unchanged. Needs final refreshed screenshots/mobile touch QA.
- Current typecheck PASS;68unit tests PASS. One archive hash test needed20s timeout for cold IO; no comparison/validator threshold changed.

Remaining authorized work:
1. Actual Studio E2E tests: item selection/reset/save/local presets/reload/v1 migration/invalid refs/asset404 fallback/switch6/world x,y+visited retention/mobile gesture isolation/tour/cache stress.
2. Finish source provenance for7host generations, internal visual gates for all10items, memory instrumentation/report; Forge pixel QA/new2 side motion diagnostics with honest WARNs. Physical Android/iPhone/hardware performance NOT TESTED.
3. Actual Phaser native evidence and gameplay videos for new2 and4 cosmetic look examples; capture all8 gaits and emotes; source/corrected/native comparisons. Original4/world native regression readbacks, optional new2 bridge clearance tests using old tools if useful.
4. Run all required commands typecheck/assets:check/lint/test/test:e2e/build; fix failures. Prettier already run src/characters/main/new tests/new mjs; rerun for changed files as needed.
5. Build fresh portable compiled game (tools/phase1b/build_review.mjs pattern), package only canonical runtime assets +new cosmetics/previews +compact review evidence; keep ZIP<100MB (old source-heavy ZIP92MB would exceed with new assets, so link full original/new sources in immutable Git checkpoint instead). Use new tools/phase2a package path; do not overwrite old artifacts.
6. Updated authority state, architecture/contracts, coverage/provenance/protected hashes/QA and performance reports; record inherited world issues, original11Forge WARNs, physical-device/interiors limitations.
7. Source/review recoverable checkpoints, push ONLY new feature branch plus new tags; verify immutable native/media/ZIP links HTTP200 and SHA256, all historical refs and main unchanged. STOP after complete review package for human acceptance; no Phase2B.

Tools: new tools/phase2a/art.py,cosmetics.py,composition_qa.py,freeze-identities.mjs,ara_pilot.mjs,studio_probe.mjs. Old source/tool files must remain exact.
Local Vite4320 via exec session4940; old previous-task package server4330 may still run and is NOT the new package. Use new package port4340. Chromium/usr/bin/chromium; video env PLAYWRIGHT_BROWSERS_PATH=/tmp/phase1b-playwright with /tmp/phase1b-playwright/ffmpeg-1013/ffmpeg-linux -> /usr/bin/ffmpeg.
