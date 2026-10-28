# Phase 3B architectural handoff

The 26-NPC artistic and gameplay foundation is approved. This handoff is ready after the final checkpoint verification; **Phase 3B implementation has not started**. No main merge or public deployment is authorized. Read the current authority at the top of AGENTS.md and docs/current/PROJECT_STATE.md.

| Contract | Preserved behavior and future constraint |
|---|---|
| Registry | `history.ts` composes 14 residents, six original modern visitors and six archive reconstructions through the existing NPCRegistry. The living `npcCatalog` remains 20; legacy `registered` remains 14. Canonical total is 26, archive count is six, verified historical claims are zero. |
| Identity | `identity.ts` and `identity-presentations.json` separate KO/VI display names from stable IDs, asset keys, animation and save references. All six historical names are retained. A future fictional migration requires separately reviewed identity and depiction decisions; renaming alone does not establish clearance. |
| Actor lifecycle | Existing NPCActorModel, state machine, world masks, collision, soft yield and dialogue services remain. One archive actor temporarily replaces a canonical host slot. Region exit restores living schedules. Limits remain four active actors, four loaded textures and two pending loads. |
| Native art | Approved 96×112 cells, anchor (48,100), 104 cells per NPC and exact atlas hashes remain frozen. All 26 identities have 2,704 registered native cells in total. |
| Dialogue | Neutral reconstruction graphs and beginner vocabulary work in KO/VI. Detailed biographies and contemporary real-person fact cards remain unverified and excluded. Any new factual content needs inspected claim/source evidence. Do not invent quotations or mark website lessons completed. |
| Persistence | Keep `korean-arena-npc-world-v1` and visit scheduling. Display names must never become save keys. Preserve player position, appearance, presets and visited state. Existing explicit QA entry behavior is distinct from a normal page reload. |
| Future gameplay | Lesson, quest and provider hooks remain typed but inert. No account, lesson system, inventory, reward, shop, economy or multiplayer implementation was added. |
| Release | Artistic development approval does not certify commercial rights. Applicable generation/account terms, reference-chain review, jurisdiction and concrete depiction issues require separate review. A 403 response is not a rights denial. |
| Validation | Preserve all existing tests and warnings. Rerun relevant actual Phaser, touch, lifecycle, native-readback and preservation checks when changing these contracts. Physical Android, iPhone, GPU, thermal and battery measurements remain NOT TESTED. |

The twelve playable characters, 28 cosmetics, 46 variants, Character Studio, world art, collision, camera and Scenic Tour are unchanged. Do not infer authorization to begin Phase 3B from the word “ready.”
