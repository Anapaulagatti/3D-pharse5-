# Korean Pixel Town · Phase3B-D local review development

Current authority: [PROJECT_STATE](docs/current/PROJECT_STATE.md). Phase3B-C is an accepted development baseline; Phase3B-D adds farming, a small shop/economy and two Korean-gated quests on the same approved world. Changed public exposure is not approved automatically.

`npm ci`, `npm run dev`. Production `index.html` → `src/game/main.ts` → `src/gate3/main.ts` loads **only** `public/assets/gate3/palace-cleanup-world/manifest.json`, with explicit Phase3BC collision overrides. WASD/arrows, Shift run, E interact; mobile landscape joystick and touch actions. Twelve playable characters,26NPC identities and24activecosmetics are preserved.

Rejected V9/V10 maps are removed from this candidate branch; [cleanup manifest](docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json) lists exact paths, hashes and approved northern/provenance exceptions. Old historical commits such as458134c still show their original files; no history rewrite, branch/tag deletion or main merge was performed. Old verifier tests are archived, while active CI tests the canonical world.

[Gate1 source benchmark](docs/gate1/GATE1_SOURCE_AND_SKILLS.md), approved North native donors and old recovery tags remain source evidence. They are excluded from active gameplay/built asset closure. No world directory auto-selection or legacy start-page build copy is allowed.

Learning uses original beginner local-demo content, PENDING_HUMAN_REVIEW; no real website account/progress integration, paid services, ads, purchases with real money or production backend. Physical Android/iPhone/GPU testing remains NOT TESTED. Public Pages/v0.5 stay unchanged until the new exact manifest is explicitly approved. No Phase3B-E.
