# CODEX MASTER PROMPT — PHASE 3B-A
## LIVING NPC DAILY LIFE SYSTEM + COMMERCIAL IDENTITY / IMAGE RIGHTS SAFEGUARD
### Continue from the APPROVED 26-NPC Phase 3A checkpoint; do NOT restart character production

REPOSITORY: Anapaulagatti/3D-pharse5-
SOURCE BRANCH: feature/phase3a-fictional-identity-safeguard
REPORTED APPROVED COMMIT: 6dbee381fcf1adf79f3f96c931b7170cea2ba076
NEW REVIEW BRANCH: feature/phase3b-a-daily-life-rights-audit
ENGINE: Existing Phaser 4.2.1 / TypeScript / Vite
AUTHORIZATION: Phase 3B-A ONLY. Phase 3B-B/C/D are NOT authorized in this run.

============================================================
0. HUMAN DIRECTIVE AND IMMUTABLE APPROVALS
============================================================

The owner approves Phase 3A's 26-NPC roster, artistic quality, approved character animations, existing world and gameplay interactions as the development baseline. Phase 3B-A is now authorized.

The owner additionally wants a PRACTICAL COMMERCIAL-RIGHTS SAFEGUARD for the NPC roster: identify recognizable third-party likenesses, unlicensed source art, celebrity identifiers, historical depictions based on specific copyrighted expressions, costumes/logos, and source-generation license gaps. Prefer genuinely original fictional game characters wherever real-person commercial rights are unknown. A mere name change is NOT proof of legal clearance. Modify only specific, demonstrably risky artistic elements as needed, with isolated, reviewable art proposals; avoid remaking the entire roster.

DO NOT:
- Rebuild the approved world/map, Jeju bridges, palace, Hanbit Station, farm or other scenery.
- Regenerate the 12 playable characters, 28 cosmetics or Character Studio.
- Rebuild 26 approved NPC identities, their entire sprite sets, or the NPC engine from scratch.
- Change existing stable NPC IDs, saved keys, routes, collision or rendering scale.
- Begin shops, crop planting, harvesting, economy, inventory, Korean quiz gates, rewards, ads, multiplayer or AI-generated NPC conversations.
- Merge to main, deploy, or certify commercial/legal clearance.

Check the ACTUAL source branch, commit, working tree and historical checkpoints. Use the verified repository state if paths or refs have evolved. Preserve a non-destructive recoverable baseline, protected asset hash manifest and rollback plan BEFORE changes. If the reported commit is absent, identify the correct approved descendant; never invent a checkpoint or do a destructive reset.

============================================================
1. EXISTING ARCHITECTURE — READ BEFORE CODING
============================================================

Inspect these confirmed components and actual references:

src/npcs/manager.ts                    NPCManager, 7 zone bounds, actor activation, player proximity and dialogue
src/npcs/actor.ts                      NPCActorModel; current patrol/wait/greet/talk/return FSM
src/npcs/types.ts                      NPCDefinition + direction/animation/route schemas
src/npcs/catalog.ts                    14 original residents + 6 modern fictional visitors = 20 living NPCs
src/npcs/history.ts                    final 26-NPC runtime catalog + 6 fictional archive characters
src/npcs/identity.ts                   public presentation mapping, NOT save IDs
src/npcs/dialogue.ts                   existing Korean/Vietnamese authored dialogue flow
src/npcs/visits.ts                     current visitor eligibility and rotation (inspect actual implementation)
src/npcs/state.ts                      current FSM and persistent NPC records (inspect actual implementation)
assets-src/npcs/phase3a-finalization/identity-presentations.json
assets-src/npcs/phase3a-finalization/release-status.json
docs/phase3a-identity-safeguard/PHASE3B_HANDOFF.md
docs/phase3a-identity-safeguard/DEPICTION_REVIEW.md
docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md

CONFIRMED CONTRACTS FROM THE HANDOFF:
- Canonical roster = 26; living collection = 20 (14 residents + 6 fictional modern visitors); 6 archive figures are fictional era-inspired characters.
- Stable historical internal IDs remain npc-history-* solely for compatibility; public names are fictional, not claims of actual history.
- A selected archive figure replaces a host slot. Do NOT render an archive figure and its displaced modern/resident host simultaneously.
- At most FOUR active actors, FOUR loaded textures, TWO pending loads under the existing runtime/culling design (unless an explicit demonstrated problem requires a separately reviewed change).
- 96x112 native frames, foot anchor (48,100), 104 frame cells per NPC, original art hashes and movement registrations are locked.
- The archival six remain separate from present-day continuous-life scheduling; historic eras are NOT contemporaneous with modern town residents.
- `korean-arena-npc-world-v1` and other existing player/visitor/appearance preference keys must remain backward compatible. NPC display names must NEVER become save keys.
- Release permissions and authentic hardware testing remain UNVERIFIED / NOT TESTED. Do not erase these facts.

============================================================
2. PHASE 3B-A PRIMARY GOAL — EVERYDAY NPC LIFE
============================================================

Build a compact, believable, deterministic NPC DAILY LIFE system that gives the 20 present-day inhabitants different behaviors across a simulated game day, while keeping the six archive inhabitants within a coherent fictional historical/story setting.

Examples:
- Café staff greets guests in the morning, performs work near the café, and finishes duty later.
- Bookshop staff checks books, rests, then welcomes visitors.
- Hanbit station attendant conducts station duty; a commuter waits, departs or returns on a VALID safe route.
- Jeju orchard keeper tends trees and relaxes along orchard paths.
- Farmer inspects existing plots and returns to a resting spot; this is ONLY an animation/behavior, NOT farming gameplay.
- Namsan/amusement guides operate during appropriate hours; harbor residents make waterfront rounds.
- The six modern fictional guests have believable context-specific time windows and host-slot ownership; they are NOT always-on extra NPCs.

Do not make all 20 residents execute identical timed patrol loops. Scheduling must be individual, location-aware, role-aware and testable.

============================================================
3. GAME CLOCK & DETERMINISTIC SCHEDULER
============================================================

Create a single configurable game-world clock reused by NPC schedules.
- Distinguish game time from real current calendar time; no dependence on the user's OS timezone for simulation.
- Configurable game-day duration (pilot default: 30 real minutes = 24 in-game hours, unless existing project setting supersedes this). Provide safe developer speed-up for QA only.
- Provide morning / midday / afternoon / evening / night phases with configurable boundaries, not fragile if/else chains.
- Pause/visibility behavior must be explicit: clamp accumulated dt and avoid multi-hour instant NPC teleport or running thousands of missed frames after backgrounding/reloading.
- Support deterministic seed + game-day index for replayable activity choices. Seeded variation is allowed, nondeterministic route selection that breaks E2E is not.
- Persist clock schema version and last valid schedule checkpoint without corrupting older NPC persistence. Validate/tolerate old or malformed records and migrate safely.
- Safe resume on refresh, new session and zone travel. Do not move an actor to invalid coordinates while off-screen.
- Keep an unobtrusive player-facing time-of-day indicator if needed; do not create a new HUD framework. Include developer-only time controls behind QA gates.

Model schedule entries as data, NOT an enormous NPC-ID switch statement:
  npcId / scheduleId, applicable day phase, activity type, permitted zone, valid waypoint/anchor, priority, duration, optional contextual dialogue key, interruptions policy.
Validate that every reference resolves and every anchor is on the approved walkable layer.

============================================================
4. ACTIVITY MODEL AND BEHAVIOR GRAPH
============================================================

Extend the existing NPCActorModel/FSM in place (do not create a parallel controller).
Suggested high-level activities:
- COMMUTE_OR_REPOSITION (only on validated route), WORK, SHORT_BREAK, WALK_AROUND, SOCIAL_PAUSE, REST, GREET_PLAYER, TALK_PLAYER, RETURN_TO_SCHEDULE.
Map each activity onto existing approved idle/walk/greet/activity clips; DO NOT claim visual actions (e.g. sitting, watering, eating) that require non-existent art unless the appropriate approved animation/prop actually exists.

Requirements:
1. Event/activity priority: active player conversation > safety/route recovery > scheduled activity > ambient variation.
2. While TALK is active, suspend NPC movement and preserve schedule intent; resume to the current appropriate task after closing, rather than resuming an expired patrol.
3. NPCs must not snap across the world or traverse blocked ground to catch up with a schedule. For offscreen transitions, use a validated spawn/zone activation policy and document it.
4. No NPC-NPC stacking or permanent chokepoint occupancy.
5. Handle route failure with bounded retry, idling in place or returning to a verified safe anchor; never delete protected collision pixels or walk through scenery.
6. Stable interactions on keyboard/touch and responsive dialogue text regardless of time transitions.
7. Do not simulate impossible pathfinding to nonexistent interiors. If buildings lack interiors, schedule work at a valid outdoor service point.
8. Keep lighting/scene artwork immutable; time-of-day does NOT authorize recoloring the whole map.

============================================================
5. ACTIVITY PLANS FOR THE 20 PRESENT-DAY NPCS
============================================================

Author individual schedules for all 14 original residents:
- Seoyeon (palace guide): opening cultural orientation, short public courtyard patrol, visitor greetings, end-of-day standby.
- Daehyun (palace guard): entrance checks, safe perimeter rounds, patrol break, evening post.
- Minseo (café): prepare/open, café frontage duties, short midday break, closing.
- Jiho (bookstore): organizing books, visitor discussion, short break, closing.
- Eunji (station): morning station duty, assisting travelers, rotation break, evening duty.
- Junho (commuter): waits, travels ONLY validated pedestrian routes, pauses, returns. No train boarding into unsupported interiors.
- Harin (Jeju orchard): inspecting tree rows, orchard break, afternoon route, home-side rest.
- Seojun (Jeju host): host greeting, cultural presentation, courtyard rounds, rest.
- Nayeon (farm): farm-side inspection, lunch break, checking plots, evening rest. No harvest/inventory.
- Cheolsu (farm): seed discussion near farm service area, short rounds, break, wind-down.
- Yejin (Namsan): visitor guidance and scenic path walking, breaks, later standby.
- Sungmin (amusement): staff arrival, attraction-side greeting, scheduled pause, closing. No ride activation.
- Donghae (harbor): shore observation, safe harbor patrol, pause, home-side standby.
- Soobin (terminal): morning terminal help, visitor guidance, closing; never blocks pier/bridges.

For SIX original fictional modern visitors:
- Load their exact definitions/host-slot metadata from `src/npcs/catalog.ts` and actual source files.
- Give each a unique, plausible occupation-context visit window; maintain existing overlap/rotation rules.
- Their visit eligibility must never increase the normal active NPC cap or displace an active dialogue target.
- Do NOT reintroduce the real celebrities that inspired any older planning notes, and do not depict them as endorsed guests.

For SIX fictional archive figures:
- Their stories occur in a separate historical-memory/era context.
- Make a small self-contained *era-appropriate* schedule or activity variation only while selected in the archive mode.
- Never have a Silla or Joseon character commute to a modern train station/café or show a modern job routine.
- Preserve archive selection, host replacement and fictional identity disclaimers.
- Do not add unverified biographies, achievements, quotes, fact cards or real-person likeness.

============================================================
6. PLAYER EXPERIENCE AND VALIDATION
============================================================

Add minimal enjoyable signs of NPC life:
- Contextual idle/work animation that uses available source clips.
- Appropriate greetings based on game time when existing dialogue supports it.
- Optional short non-intrusive status label on interaction: e.g. 'Đang làm việc', 'Đang nghỉ', 'Sắp đóng cửa' / Korean equivalent.
- No permanent intrusive floating labels; do not hide the native map.
- After dialogue, NPC picks up the correct schedule with natural motion.
- If an NPC is resting or off duty, provide a reasonable interaction response only when physically present; don't teleport a resident for a dialogue.

QA must include accelerated full-day simulation, normal-speed gameplay snippets, source-to-schedule validation, player approach/interaction, touch/keyboard, zone entry/reentry, refresh persistence, background/resume, archive selection, and daytime/nighttime frames.

Preserve the actual runtime limits (4 active / 4 textures / 2 pending) and verify no new unnecessary GPU uploads, runaway timers or unsaved NPC state growth. Report hardware tests as NOT TESTED unless actual phones were used.

============================================================
7. PARALLEL SAFEGUARD — COMMERCIAL RIGHTS & FICTIONALIZATION AUDIT
============================================================

**This is a technical and asset-provenance risk review, NOT a legal opinion or a blanket legal clearance.**
Do not waste the entire Phase 3B-A on endlessly scraping blocked websites. Produce documented evidence, practical risk reduction and a reviewable release gate.

Check EVERY one of the 26 NPCs and any historical/modern public-facing reference for:
A. Original generation prompts, source masters, turnarounds, provided reference images, rig outputs, third-party assets, animation props and final atlases.
B. The generation tool/provider and TERMS AT TIME OF CREATION (the model name/plan where provable; commercial permission, third-party restrictions). If unverified, record UNKNOWN rather than asserting permission.
C. Any recognizable living public figure: facial likeness, names, stage names, voice, distinctive hairstyle + outfit + emblem combinations, brand/fandom/stage logos, catchphrases, endorsement suggestions, recognizability through multiple identifiers.
D. Historical figures: distinguish public-domain historical facts/names from copyrighted modern portraits, banknote illustration uses, protected photographs, films, costumes, television character design, statues and source-specific drawings.
E. Copyrighted expressive designs, game/media characters, third-party pixel artwork; suspicious copied artwork identified from concrete source evidence. Similar style alone is NOT proof of infringement.
F. Trademark/design marks in clothing, props, dialogue, signage and promotional screenshots.
G. Project-owned assets versus borrowed artwork; downstream licenses; source URL/license file and actual source provenance where available.

Use official evidence and record source URLs, date accessed, evidence IDs, permission/terms excerpts and unknowns. HTTP 403 means transport failure, NOT refusal of permission and NOT confirmation of any license. No fabricated research results. Inspect source material only where access and terms permit; if official sources are blocked, use lawful alternative official pages, archived authorized documents or request human supplied PDFs rather than repeated unbounded network retries.

OFFICIAL POINTS OF REFERENCE (verify currency and apply legal counsel before launch):
- Korean unfair competition statute: https://law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1025179229
- Korea Intellectual Property Office enforcement statement dated 2026-03-05: https://www.kipo.go.kr/ko/kpoBultnDetail.do?aprchId=BUT0000029&keyword=&menuCd=SCD0200618&ntatcSeq=20800&pageIndex=&searchCondition=&sysCd=SCD02
- Official KIPRIS trademark/design search: https://www.kipris.or.kr/
- Korea Copyright Commission AI assisted-work registration guidance: https://www.copyright.or.kr/eng/doc/etc_pdf/Guide_to_Copyright_Registration_for_Generative_AI-Assisted_Works.pdf
- Korean Ministry of Culture name/title copyright FAQ: https://www.mcst.go.kr/site/s_policy/copyright/netizen/netizen02.jsp

Keep classification on two independent dimensions:
  RISK: LOW_CONCERN / NEEDS_REVIEW / CONCRETE_CONCERN
  PUBLICATION: DEV_ONLY / BLOCKED_PENDING_REVIEW / LICENSE_DOCUMENTED / LEGAL_REVIEWED
Never label an NPC 'copyright-free' or 'commercial cleared' solely because it has a fictional name, is AI-generated or passed automated tests.

Audit matrix per NPC MUST include:
  stable ID, public KO/VI name, historical/modern/fictional status, creator/tool provenance, source-art references, explicit licenses/terms and evidence, potential recognizable-person indicators, distinctive costume/prop/logo indicators, current risk rationale, recommended action, human review needed, release gate, before/after hash if modified.

============================================================
8. TARGETED FICTIONALIZATION / VISUAL DISTINCTIVENESS FALLBACK
============================================================

The six archive historical game characters ALREADY have fictional display names and dialogue; preserve them:
- Han Yeonhwa / 한연화 (internal npc-history-seondeok)
- Baek Junseo / 백준서 (internal npc-history-sejong)
- Nam Gyeongu / 남경우 (internal npc-history-jang)
- Yun Hwayeon / 윤화연 (internal npc-history-saimdang)
- Kang Muyeong / 강무영 (internal npc-history-yi)
- Seo Daeun / 서다은 (internal npc-history-yu)

Review their known residual concerns from `docs/phase3a-identity-safeguard/DEPICTION_REVIEW.md`, especially the royal robe/headwear and naval-commander silhouette. Do NOT automatically erase authentic generic historical fashion just because it evokes an era. Distinctiveness must be based on actual combined appearance and concrete comparison, not arbitrary pixel-change percentages.

Policy:
- Keep an approved asset unchanged when no identifiable third-party concern is substantiated; document unknowns and keep the release gate pending.
- When there is a concrete identifiable risk or a strong unresolved recognizable-real-person impression, design an ORIGINAL fictional replacement concept: a clearly distinct face, hairstyle/silhouette, garment motif, palette, headwear/accessory and/or prop as appropriate. Change enough meaningful identifying elements to create an independent character; changing just a tiny accessory or 10% of pixels is NOT sufficient by itself.
- Preserve character occupation, era coherence, Korean Arena Gate-1/Juni-quality pixel craftsmanship, 96x112 native frame registration and compatible 104-cell animation quality. Never use a simple Pillow-rectangle character generator.
- For any affected NPC, make a VERSIONED CANDIDATE art pack and a controlled in-game replacement preview. Keep the approved Phase 3A assets untouched and recoverable. Restrict edits to that NPC's owned art/atlas + safe display/dialogue presentation. No world, player, or registry-ID changes.
- Stage visual alternatives behind QA/review switches. Do NOT silently replace artwork already human-approved. Provide source/after/nearby-Juni real Phaser comparisons. Ask for human artistic acceptance of only the affected candidate.
- Modern NPCs must be fictional original people, not thinly disguised IU/BTS/Jennie/Faker/Son Heung-min or any identifiable celebrity. If an NPC is readily identifiable as a real performer/player based on name, face, signature costume and context together, propose an independent redesign and remove implied endorsements. Do not make a 'lookalike with a changed name'.
- Avoid showing/licensing third-party reference photos in the shipped game or deliverable package unless their usage rights are documented.
- No new commercial hero images, marketing posts or celebrity-backed promotions in this task.

IMPORTANT: This prompt authorizes the INVESTIGATION and the creation of targeted candidate redesigns IF justified. It does NOT authorize automatic adoption of an altered approved NPC sprite without specific human art approval. Development may continue with baseline assets, but flagged material must be blocked from public release.

============================================================
9. RELEASE SAFETY GATE, NOT AN ASSUMED LICENSE
============================================================

Implement a validated, machine-readable rights inventory separate from gameplay entity IDs, plus a development-only report/UI.
- `approvedForDevelopment` is separate from `approvedForCommercialRelease`.
- Any `BLOCKED_PENDING_REVIEW` record must prevent that specific asset/factual-card/celebrity-reference from being included in PUBLIC RELEASE builds, not from the local/private review ZIP.
- Do not let a local user query parameter bypass commercial-release gating. Keep `DEV_ONLY` access behind controlled build configuration, not a public URL flag.
- Ensure the gate does not silently substitute sprites, corrupt dialogue, break stable IDs or delete actors. A release build should FAIL validation with actionable output if it requires an uncleared asset and no approved replacement exists.
- Where legally permitted original assets can be documented, attach actual evidence. For unresolved claims, report exactly what an IP lawyer/art lead must review.
- Do not treat this as automated legal certification; a lawyer familiar with Korean + intended distribution jurisdictions must review commercial use before launch.
- AI output copyrightability/ownership and service commercial-use terms are separate questions; do not assume one resolves the other.

============================================================
10. INTERNAL EXECUTION WAVES — ONE CONTROLLED REVIEW
============================================================

WAVE 3B-A1 — CLOCK + FIRST FOUR LIVE SCHEDULES
Implement clock and deterministic scheduler. Demonstrate Seoyeon, Minseo, Harin, Eunji using actual Phaser gameplay. Preserve approved world and art; verify movement/talk/return and 4-active cap. Save checkpoint.

WAVE 3B-A2 — ALL 20 CONTEMPORARY SCHEDULES + 6 ARCHIVE-SAFE BEHAVIORS
Create full living schedules and modern visitor visitation windows; add small era-themed scripted routines for selected archive actors ONLY. Add persistence, safe culling, dialogue interruption, developer time controls and mobile UX. Save checkpoint.

WAVE 3B-A3 — RIGHTS AUDIT + TARGETED CANDIDATES + FINAL QA
Audit 26 assets and all public real-person identifiers; populate machine-readable rights matrix. If specific problems are found, prepare small independent fictional redesign candidates, not silent replacements. Implement strict public-release validation. Run all tests and produce offline playable PRIVATE REVIEW ZIP + evidence.

Do not pause for routine micro-approvals between waves; stop only if essential capabilities/assets are unavailable or a concrete human-only decision is needed. Final human art/rights review is still required before any candidate is adopted or any public deployment.

============================================================
11. ACCEPTANCE TESTS & REAL EVIDENCE
============================================================

Run repository commands that actually exist (inspect package.json):
- Typecheck, assets:check, lint, format:check, unit tests, E2E tests, production build.
- Preserve the previous 156 unit + 69 E2E baseline unless a clear legitimate migration is demonstrated; do NOT alter existing assertions solely to make results green.

Add tests for:
1. Clock phase boundaries, midnight rollover, pause/resume, accelerated QA time.
2. Deterministic schedule seed/replay and corrupted-save migration.
3. 20 living NPC schedule existence, valid anchored routes, unique stable IDs.
4. Six archive actors do not join modern daily-life clock as contemporaneous inhabitants.
5. Host-slot replacement remains correct and 4/4/2 caps hold.
6. Player dialogue interrupts/resumes schedule safely.
7. No path through water, walls, roofs, rail platform collisions or narrow Jeju bridge blockages.
8. Long-session game day loop, repeated zone activation, refresh, background/resume without duplicates.
9. Existing Korean/Vietnamese dialogue, Character Studio, 12 playable characters, 28 cosmetics unaffected.
10. Rights matrix covers every 26 NPC IDs, includes provenance evidence/UNKNOWN flags, and gates unresolved public-release assets.
11. Public-facing fictional aliases remain correct in KO/VI, UI, accessibility and dialogue.
12. No release build can falsely infer clearance from the names being fictional or from tool-generated assets.
13. Candidate sprite art changes are isolated, hash-documented and NEVER auto-promoted as approved.

REQUIRED REAL REVIEW EVIDENCE:
- Native Phaser videos: morning café, palace shift, farm/orchard work, Hanbit commuter, evening station/harbor.
- A complete accelerated day-cycle recording demonstrating changing behaviors of several NPCs.
- Mobile landscape interface screenshot + actual responsive interaction.
- Scene coverage for all seven home-zone types, Jeju bridge traversal and archive selection.
- Rights audit CSV/JSON with evidence, red/yellow/green descriptive risk labels (not claims of legal clearance).
- Side-by-side native 1:1 comparisons for any targeted artistic redesign candidates.
- Independent playable ZIP and real integrity/launch logs.
- FPS/frame timing, texture/cache count and NOT TESTED flags for actual Android/iPhone.

============================================================
12. DELIVERABLES & STOP CONDITION
============================================================

Create/maintain:
  docs/phase3b-a/README.md
  docs/phase3b-a/DAILY_CLOCK.md
  docs/phase3b-a/NPC_DAILY_SCHEDULES.md
  docs/phase3b-a/STATE_MACHINE_AND_PERSISTENCE.md
  docs/phase3b-a/NAVIGATION_AND_PERFORMANCE.md
  docs/phase3b-a/VISUAL_REVIEW.md
  docs/phase3b-a/QA.md
  docs/phase3b-a/PROTECTED_AUDIT.md
  docs/phase3b-a/COMMERCIAL_RIGHTS_AUDIT.md
  docs/phase3b-a/RIGHTS_REVIEW_QUEUE.md
  docs/phase3b-a/RIGHTS_MATRIX.json
  docs/phase3b-a/RELEASE_GATE.md
  docs/phase3b-a/ART_REDRAW_CANDIDATES/ (only where substantiated, not mandatory)

Provide:
- Verified source commit + new recoverable Phase 3B-A review checkpoint.
- Complete game clock/schedule system and 20 contemporary schedules.
- Six safe fictional archive behaviors in their own context.
- 26/26 rights/provenance inventory entries and specific remaining questions.
- Any risk-based original fictional NPC redesign *candidates*, kept separate from approved assets.
- Measured QA, real Phaser gameplay recordings and independently verified private review ZIP.
- Exact PASS / FAIL / WARN / NOT TESTED separation.

FINAL STOP:
**PHASE 3B-A: DELIVER FOR HUMAN REVIEW.**
Do not start Phase 3B-B, -C, -D or Phase 4.
Do not merge into main or deploy.
Do not claim commercial rights are settled merely because an audit or rename was performed.
Preserve all approved character art unless the owner separately approves a specific replacement candidate.

The goal is a believable living world AND a professionally managed commercial asset-rights process — without wasting the previous artwork effort.