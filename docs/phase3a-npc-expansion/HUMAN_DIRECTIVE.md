# CODEX MASTER PROMPT — PHASE 3A CONTINUATION
# APPROVE THREE ILLUSTRATED PILOTS → COMPLETE RESIDENT NPCS → HISTORICAL & MODERN CULTURAL NPCS
# Project: Tienghansoeasy.io.vn / Korean Arena
# Date: 2026-10-28
# Language: English for implementation. Korean dialogue with natural Vietnamese translation.

YOU ARE CONTINUING AN EXISTING, PARTIALLY APPROVED PROJECT. THIS IS NOT A NEW PROJECT OR A NEW NPC ENGINE.

REPOSITORY
- https://github.com/Anapaulagatti/3D-pharse5-
- Working branch: feature/phase3a-npc-art-rebuild
- Most recent three-pilot review evidence: docs/phase3a-art-rebuild/
- The user has reviewed the three newly illustrated pilot NPCs (Seoyeon, Minseo, Harin) and explicitly APPROVES their artistic direction and quality.
- In the user's screenshot the previous implementation reports a review checkpoint 2f15cd5. Resolve the authoritative commit and immutable tag from the actual repository; do not guess or silently reset. Start at the newest valid Phase 3A art-rebuild branch state and save a recoverable checkpoint.

HUMAN DECISION — EFFECTIVE IMMEDIATELY
1. APPROVE the illustrated *visual style* of Seoyeon, Minseo, and Harin as the binding NPC-quality baseline. Register an immutable, recoverable artistic approval reference that includes the exact approved artwork/source hashes and existing review evidence.
2. RETAIN the current NPC registry, dialogue, interactions, navigation, zone management, culling, persistence, camera integration, and the actual Phaser runtime. All remain functional and must not be restarted.
3. REJECT the old simplified/procedurally drawn artworks of the eleven unreworked residents. Replace those visuals using the SAME high-quality illustrated source-art → four-view → layer/rig → native atlas pipeline used successfully for the three new pilots.
4. ADD educational historical Korean characters as context-specific, chronologically grounded encounters; add attractive modern Korean cultural-celebrity *archetype* NPCs. Real modern celebrity likenesses/names may be used for in-game endorsement-like cameos ONLY after documented permission; otherwise use unmistakably original fictional people (details below).
5. Do not reopen already approved world/map art, Juni, the 12 playable characters, their 28 cosmetics and 46 variants, Character Studio, or existing protected collision and bridges. No main merge or public deploy.

PRIORITY AND EXECUTION ORDER
A. Verify baseline, register the approved pilot art, create preservation checkpoint.
B. Rebuild the 11 remaining original NPCs, yielding a complete premium-quality 14-resident roster.
C. Build a restrained historical encounter system; produce SIX original educational historical figures.
D. Build SIX original modern culture/celebrity-inspired NPCs, with a separate legal clearance registry.
E. Integrate time/zone-aware population, contextual Korean learning dialogue, actual gameplay, performance checks, deliver the review package and STOP for human review.
Complete this full scope in order without repeatedly stopping for approval of each intermediate character. However, if the premium illustration-generation capability is unavailable, STOP and report it instead of silently reverting to geometric drawing. Do not claim any art/legal/physical-device result that was not validated.

========================================================================
1. READ PROJECT AUTHORITY BEFORE CODING
========================================================================
Inspect these repository resources and their real implementation dependencies:
- docs/phase3a-art-rebuild/README.md
- docs/phase3a-art-rebuild/ART_PIPELINE.md
- docs/phase3a-art-rebuild/PILOT_REVIEW.md
- docs/phase3a-art-rebuild/JUNI_STYLE_COMPARISON.md
- docs/phase3a-art-rebuild/PROTECTED_AUDIT.md
- docs/phase3a-art-rebuild/QA.md
- assets-src/npcs/phase3a-art-rebuild/{seoyeon,minseo,harin}/
- docs/phase3a/NPC_ROSTER.md
- docs/phase3a/NPC_ZONES.md
- docs/phase3a/DIALOGUE_SYSTEM.md
- docs/phase3a/NAVIGATION.md
- docs/phase3a/PERFORMANCE.md
- docs/phase3a/PROTECTED_AUDIT.md
- assets-src/npcs/phase3a/registry.json
- tools/phase3a/art.py (REJECTED legacy visual-generation methodology; do not reuse it to draw faces/bodies)
- docs/phase1b/SOURCE_PROVENANCE.md
- assets-src/characters/phase1b-frontback-juni/juni-motion-template.json
- Approved playable character source/atlas files and checksums (READ-ONLY).

Investigate and use appropriate pinned art/animation skills, when available:
- Sprite Forge generate2dsprite:
  https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/generate2dsprite/SKILL.md
- Sprite Forge video2dsprite:
  https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/video2dsprite/SKILL.md
- Character Animation Creator:
  https://github.com/tachikomared/character-animation-creator-skill/blob/9ce98dffb98c84488fe7b99b62c49fabee20abd6/SKILL.md

Use a supported, high-quality illustrated source-image generation workflow, as demonstrably used for the accepted pilots. Record tool names, execution logs, source prompts/descriptions, hashes, inputs/outputs and licensing/provenance accurately. Do not invent unavailable skills or claim a built-in image-generation invocation happened without proof.

========================================================================
2. LOCK THE THREE USER-APPROVED PILOT NPCS
========================================================================
Artistic baseline: Seoyeon (서연, palace cultural guide), Minseo (민서, barista), Harin (하린, Jeju orchard keeper).
- Preserve their art master images, four-view turnarounds, pixel finishing, rigs, 104-cell sprite atlases, native size 96×112, foot anchor (48,100), and approved appearance.
- Maintain their original NPC IDs, professions, locations, dialogue and canonical routes.
- Do not beautify them again; use them as the explicit NPC quality benchmark beside Juni.
- If the older report still flags the 6-pixel Harin tangerine/foreground shoe occlusion, retain it as an explicitly documented legacy-foreground WARN, not secretly repair protected world art. Revisit under a separate bounded task only if it causes material gameplay failure.
- Do not remove honest historical Forge/gait warnings or treat a human artistic approval as a blanket QA/physical-device pass.

Create an immutable approval checkpoint named by actual date and source commit (avoid overwriting existing tags), plus an approval manifest of exact hashes.

========================================================================
3. REBUILD ALL ELEVEN REMAINING ORIGINAL NPC VISUALS
========================================================================
Preserve existing IDs/occupations/zones/registry and only replace their rejected artwork, rigs, registered clips and atlas references where necessary:

PALACE / TRADITIONAL AREA
- Daehyun (대현) — palace guard: elegant Joseon-inspired uniform, coherent military details, beautiful mature chibi face, layers of fabric, belt, headgear; not a flat block silhouette.

MODERN STOREFRONTS
- Jiho (지호) — bookstore worker: refined cardigan, eyeglasses where appropriate, book bag, strong unique facial identity and hair.

STATION / TRANSIT
- Eunji (은지) — station attendant: distinctive rail attendant uniform, cap, badge, shoes and clean seams.
- Junho (준호) — commuter: attractive contemporary Korean streetwear, layered jacket, bag, expressive modern facial features.

JEJU / CULTURAL HOUSE
- Seojun (서준) — Jeju cultural host: authentic-looking illustrated traditional-inspired outfit, refined face/hair, beautiful cloth depth.

FARM
- Nayeon (나연) — farmer: tasteful straw/cloth accessories, layered rural outfit, boots, expressive face.
- Cheolsu (철수) — seed specialist: unique older/younger visual characterization as appropriate, carefully constructed workwear, seed pouch.

NATURE / NAM SAN / AMUSEMENT
- Yejin (예진) — Namsan guide: modern outdoor outfit, map, light jacket and distinct hair silhouette.
- Sungmin (성민) — amusement attendant: attractive staff uniform, neat layered fabrics, ticket accessory; no real park logos.

COAST / FERRY
- Donghae (동해) — fisherman: coastal workwear, rope, sun-weathered character and shoes that visibly contact the ground.
- Soobin (수빈) — ferry staff: high-quality contemporary port uniform, clipboard, signature hairstyle, visually clear role.

ART PRODUCTION RULES
- Make ELEVEN separate original illustrated designs, not palette swaps, recolored heads, or copies of one silhouette.
- Each has four independently coherent directions: front/back/left/right, with strong consistent outfit/hair/accessory ownership and NO fake perspective from mirror-flipping.
- Quality benchmark = actual approved Seoyeon/Minseo/Harin and Juni at comparable native scale, camera zoom and ground context.
- High-quality portrait/source art must precede pixel finishing. Do not generate faces, hair, torsos, legs and clothes mostly from ImageDraw polygon/rectangle formulas. Pillow is allowed for rigging, alpha, palette/native finishing and packing.
- Keep existing compatible NPC animation contract: idle 2×4, walk 8×4, greet 8×4, activity 8×4 = 104 cells per resident; 96×112 cells; anchor (48,100), native nearest rendering.
- Walking must have alternating leg contacts, correct front/back gait, convincing rightward forward progression (not moonwalking), clear foot contact and no texture sliding.
- Prop gestures must suit each occupation.
- Output independently editable image sources, masks, joint/rig data, native atlas, atlas JSON, sprite-specific QA and source provenance.
- Process in bounded groups with internal acceptance checks: (1) Daehyun, Jiho, Eunji, Seojun; (2) Nayeon, Cheolsu, Yejin, Sungmin; (3) Junho, Donghae, Soobin. Continue automatically when each group meets the same baseline, without forcing the human to review eleven times.

Failure policy: if any output looks procedurally generic or significantly less detailed than the approved three, REJECT/REDO SOURCE ART instead of trying to fix it with sharpening, extra grain, or fake animation counts.

========================================================================
4. HISTORICAL NPC COLLECTION — LEARNING KOREA THROUGH TIME
========================================================================
Create SIX premium illustrated educational historical encounters, in CHRONOLOGICAL CONTENT GROUPS, grounded in publicly verifiable Korean historical records. These are not ordinary present-day residents. Their game appearances must be explicitly labeled as an interactive 'History Archive / 역사 이야기' or 'Historical Memory / 역사 속 인물' experience, never imply that figures from different centuries lived together in one palace.

INITIAL HISTORICAL CAST (verify facts and era labels in credible Korean references before writing dialogue):
H01. Queen Seondeok / 선덕여왕 (Silla period) — leadership, early Korean history, cultural literacy. Shown in a clearly labeled historical archive encounter, not as a resident of a Joseon palace.
H02. King Sejong / 세종대왕 (Joseon, 1397–1450) — Hangul history and basic Korean lettering; premium Joseon king silhouette and original, respectful illustration.
H03. Jang Yeong-sil / 장영실 (early Joseon) — technology, water clocks, astronomical tools, numbers and time expressions.
H04. Shin Saimdang / 신사임당 (Joseon, 1504–1551) — art, nature, drawing and colors; avoid reducing her identity solely to motherhood.
H05. Admiral Yi Sun-sin / 이순신 (Joseon, 1545–1598) — naval history, maps, directions, ships; do not fabricate heroic quotes or violent interactions.
H06. Yu Gwan-sun / 유관순 (20th-century independence movement) — courage, Korean independence history; respectful, non-sensationalized educational treatment, no anachronistic Joseon costumes.

Historical appearance design:
- Distinct historical period guides and historically reasonable Korean-inspired hairstyles and attire.
- Use primary/official history references to validate era, identity, significant event, clothing context and educational facts. Distinguish uncertain reconstructions from documented history.
- Do NOT trace or paste specific modern copyrighted paintings, museum photographs or statues; independently illustrate new character art using factual clothing and verified historical attributes.
- Do not imply that a fantasy dialogue is a verbatim quote of the historical person.
- No actual figure is presented as endorsing the game.
- Capture real Korean texts in Hangul with beginner-friendly Vietnamese translations and historical notes.

HISTORICAL PLACEMENT AND TIME-TRAVEL COHERENCE
- Reuse existing visually suitable palace, traditional buildings, bookshop/library, garden, coastal museum/learning spots WITHOUT rebuilding the world.
- Place encounters as short-lived archive/educational appearances spawned on already verified walkable cells, triggered by context or a museum/archives NPC interaction.
- A historical exhibit may teach multiple centuries; the NPC's label MUST show dynasty/era/date; never depict temporally incompatible historical figures as literally contemporaneous.
- Respect entrances, NPC footprints, reachability and pedestrian collision; do not create new walls, roads or scene overlays that obscure approved map art.
- NPC dialogue tasks are educational teasers; do not create fictional claims of completed lessons on the main site.

Useful source starting points (verify current pages, cite exact sources in deliverable):
- National Institute of Korean History, Our History Net:
  https://contents.history.go.kr/front/newEh/list.do?code=eh_age_30&type=eh_ty_010
- Sejong:
  https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n305800
- Jang Yeong-sil:
  https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n310300
- Shin Saimdang:
  https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_30&levelId=kc_n306500
- Admiral Yi Sun-sin:
  https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n309000

For Queen Seondeok and Yu Gwan-sun, independently retrieve authoritative Korean historical references and include links in the historical fact-check register. Do not invent factual details if a source cannot be verified.

========================================================================
5. MODERN FAMOUS KOREAN FIGURES — RESEARCH, RIGHTS AND ORIGINAL NPCS
========================================================================
The user explicitly wants a recognizable Korean-modern-culture atmosphere and references to famous Korean personalities.

RESEARCH REFERENCE POOL (NOT YET A LICENSE TO USE THEIR LIKENESS):
- K-pop / music: IU (아이유), BTS (방탄소년단), Jennie (제니).
- Football: Son Heung-min (손흥민).
- E-sports: Lee Sang-hyeok / Faker (페이커).
- Television / variety: Yoo Jae-suk (유재석).
- Acting / Korean dramas: Byeon Woo-seok (변우석) or other well-established current actors.
- Literature: Han Kang (한강), when relevant to bookshop/literature study.

Research and verify relevant identities, roles, contemporaneity and public profile using reputable up-to-date sources. Do not invent personal facts, endorsements, brand deals, team affiliations, quotes or biographies. References above are research anchors, not unverified rankings and not an instruction to copy a real face.

LEGAL / ARTISTIC HARD GATE
South Korea has specific protections against unapproved commercial exploitation of famous people's identifying names, likenesses, voices and other identifiers. Copyright also applies to third-party photos, logos, music and performances.

Before ANY real-person contemporary NPC is made publicly playable or marketed with that person's real name/face/voice/identifiable stage costume:
- Require actual written authorization/license covering game use, artwork, territories, distribution and monetization where applicable.
- Independently check third-party rights in photos, branding, clubs, labels, music, uniforms, game/team logos, signatures, performance costumes and audio.
- Record proof, scope, status and expiry in a rights manifest. A vague claim that 'AI generated it', 'changed the hair', 'pixelated it', or 'only resembles them a little' IS NOT clearance.
- Never falsely imply a celebrity endorsed or collaborated with the game.
- If a license is missing, DO NOT use that person's name/image/voice in an in-game character who is recognizably that individual. No near-identical 'disguised' lookalikes.
- Public facts can be used to inform separate, accurately sourced learning content where appropriate, but avoid appropriating identities for commercial endorsements.

DEFAULT IMPLEMENTATION WHEN RIGHTS ARE NOT DOCUMENTED:
Create SIX distinct, ORIGINAL contemporary fictional Korean-culture NPCs — high-quality designs informed by general professions and modern Korean culture, NOT copies of the celebrity reference people:
M01. Indie K-pop singer / songwriter: custom face, original hairstyle and stage-casual outfit; music-related Hangul vocabulary; no identifiable BTS/BLACKPINK/IU styling, lyrics, logos, songs or choreography.
M02. Football player / youth coach: totally original face, invented team colors and badge, football vocabulary and directions; no national-team jersey or Son likeness.
M03. Professional e-sports coach / gamer: custom face, original glasses/outfit/gaming accessory; teach teamwork/strategy vocabulary; no Faker/T1 persona or logo.
M04. K-drama actor / theater performer: original visual identity and fictional roles; teach emotions, greetings and everyday conversation; no iconic film stills/costumes/voice.
M05. Variety-show presenter / creative content host: independently illustrated personality and outfit; numbers, introductions and conversational politeness.
M06. Contemporary novelist / café book-club host: fully original identity; books, reading and adjectives; do not turn real authors into commercial endorsers.

Assign all SIX unique Korean and Vietnamese-readable names, NPC IDs beginning with npc-modern-*, differentiated faces, 4-view sprites, detailed costume masters, occupation gestures and original dialogue. Confirm no collision with existing 14 NPC IDs or 12 player identities.

If proper permissions are *actually provided in the repository* for a celebrity, a separately labeled optional licensed-appearance variant can be prepared under a feature flag disabled by default and with clear rights records. Do not invent licenses and do not delay the six original fictional NPCs while seeking permission.

ADDITIONAL REQUIREMENT — REAL FAMOUS PEOPLE MUST STILL BE DISCOVERABLE EDUCATIONALLY:
Create a separate read-only, factual 'Contemporary Korean Icons / 현대 한국 인물' learning index associated with existing culture NPC dialogue (not marketing or endorsement content). Include source-verified, neutral, short Vietnamese/Korean factual profile cards about at least SIX notable real people selected across music, sport, e-sports, TV and literature from the reference pool. For example: IU, BTS as a group, Jennie, Son Heung-min, Faker and Han Kang. The project owner wants learners to encounter the NAMES and CULTURAL CONTRIBUTIONS of famous modern Koreans, not just invented generic jobs. This textual educational index can factually discuss public figures with responsible attribution, but do not insert their real faces, voices, proprietary photos, idol logos or character likenesses without rights clearance. Do not turn them into quest sponsors or imply endorsement. Legal review remains advisable before commercial publication; ordinary factual biography and unauthorized commercial persona merchandising are different use cases. Save the verified factual cards in MODERN_KOREAN_ICONS_FACT_SHEETS.md and their data registry; each card should link to trustworthy published references and mark the date checked.

For modern-cultural plausibility, place only in already existing modern storefront/station, Namsan/amusement, community/coast zones; do not spawn modern performers inside the historical palace as if they belong to its original period.

Reference source starting points (verify and document accessed date):
- Korean government overview of celebrity publicity protection (2022):
  https://www.korea.kr/news/policyNewsView.do?newsId=148903034
- Korea Intellectual Property Office explanation (2022):
  https://www.kipo.go.kr/ko/kpoBultnDetail.do?aprchId=BUT0000029&menuCd=SCD0200618&ntatcSeq=19495
- Korea Herald 2026 modern celebrity advertising recognition:
  https://www.koreaherald.com/article/10788157
- Soompi September 2026 star-reputation context:
  https://www.soompi.com/article/1874165wpp/september-star-brand-reputation-rankings-announced-5

Important: this project can be monetized later; a free demo is not automatically exempt from publicity/copyright restrictions. Build rights-safe original art by default.

========================================================================
6. ONE CONSISTENT ART BIBLE ACROSS THREE ERA-SENSITIVE NPC GROUPS
========================================================================
ONE unified hand-crafted Korean Arena pixel-chibi direction across:
(1) 14 original residents, (2) 6 historical educational characters, (3) 6 modern fictional cultural characters.

Same illustration quality, facial rendering sophistication, pixel cluster detail, lighting logic and scale as approved Juni + approved Seoyeon/Minseo/Harin. Era-specific visual differences must come from researched hair, clothing, accessories and props — NOT from changing the entire rendering style.

Mandatory consistent technical contract unless existing reviewed engine explicitly requires otherwise:
- Native pixel art dimensions: 96×112 cell.
- Registered foot anchor: (48,100).
- Four independent directional views.
- Consistent alpha/nearest/integer registration.
- No in-frame world background; environment remains original map scene.
- Clear contact shadows managed by existing runtime, no copied environment cutouts.
- NPC animation: compatible 104-cell contract for each additional actor if the existing NPC runtime requires it.
- Source masters + authored layers/rig + complete export provenance preserved for subsequent edits.
- Source-view alignment, phase-consistent feet, correct gait direction, natural start/stop as supported by current NPC engine.

Require real side-by-side comparisons (at native resolution and same ground/context): JUNI vs ACCEPTED THREE vs NEW RESIDENT vs HISTORICAL vs MODERN. A beautiful portrait alone is not sufficient.

========================================================================
7. HISTORICAL DIALOGUE & LEARNING-READY INTEGRATION
========================================================================
This game supports Korean language learning. Make every dialogue useful, friendly and appropriately placed:
- A1 beginner Korean baseline: greetings, people, occupations, numbers, colors, places, food, directions, shopping, simple verbs.
- Some historical NPCs introduce verified history through short, age-appropriate cultural conversations; preserve clear Korean text and correct Vietnamese translation.
- Avoid overly complex Korean honorific usage, ungrammatical phrasing and machine-translation artifacts. Review with linguistic QA.
- Keep historical facts and sources separate from invented game dialogue.
- Each new NPC: 3–5 concise interaction topics, at least 6 useful beginner vocabulary items across topics, and contextual translations. No duplicate boilerplate across twenty-six NPCs.
- Include future `learningTopicTags` and data identifiers compatible with later integration into tienghansoeasy.io.vn, but DO NOT fabricate course completion, user knowledge, external account connections or sync.
- The eventual mission → Korean question → retry-with-same-level → completion → optional rewarded-ad ×2 loop belongs to later gameplay phase. Keep typed, non-breaking hooks where existing architecture allows; DO NOT build shop/economy/ad systems inside this artwork/NPC phase.

========================================================================
8. SPAWN, PATHFINDING AND PERFORMANCE BUDGET
========================================================================
With 14 residents + 6 history + 6 modern = 26 total NPC definitions (no duplicates).
Do NOT display 26 simultaneously.

- Keep active resident count and loaded resident texture budgets at or below the measured, existing Phase 3A production baseline unless profiling proves a safe improvement. Prior review documents at most 4 active NPCs / 4 resident textures / 2 simultaneous loads; extend *availability* in the registry without expanding runtime load indiscriminately.
- Implement deterministic spawn priority, per-zone pools and optional historical/archive activation and contemporary visiting schedules using existing mechanisms.
- History encounters should swap/activate only in safe, already-walkable positions; no new permanently colliding actors that block the palace or bridges.
- Modern cultural NPCs appear in selected appropriate zones or visit rotations, not everywhere. Avoid duplicates of same actor in multiple places simultaneously.
- Never modify approved world tiles, collision masks, station, Jeju bridge positions, palace architecture, terrain art or character-navigation mechanics.
- Check all 26 approach routes, dialogue open/close, resumption, idle loops, occupancy/yielding, cross-zone re-entry and reload.
- Demonstrate source/texture lifecycle bounds, avoid retained textures or re-created objects upon repeated zone entry.
- Keep normal gameplay free of QA-only spawn markers; special review spawns must be explicit and disabled in production.
- Preserve correct camera depth, native raster sharpness and UI safe areas.
- Do not assert Android/iPhone or GPU PASS without actual physical tests.

========================================================================
9. HUMAN REVIEW DELIVERABLES, AUTO QA, VERSION CONTROL
========================================================================
Create a fresh review area, WITHOUT deleting earlier review history:
`docs/phase3a-npc-expansion/`

Minimum files:
- README.md — what changed, exact branch/commit/checkpoint, gameplay instructions.
- STYLE_BIBLE.md — precise shared Juni/pilot visual rules + artistic reference gallery.
- NPC_ROSTER_26.md — all 26 identities, IDs, zones, role, type, era, rights status and source paths.
- HISTORY_FACT_CHECK.md — era/date facts, cited historical sources, source-to-dialogue mapping, uncertainty notes.
- MODERN_RIGHTS_MATRIX.md — named research references vs actual in-game fictional NPCs, clearance status, no implied endorsements.
- MODERN_KOREAN_ICONS_FACT_SHEETS.md — six or more sourced, neutral and bilingual educational fact cards about real contemporary Koreans; no unlicensed likenesses.
- ART_PIPELINE.md — actual art generation workflow, tools/skills genuinely used, per-character original sources, rig provenance, immutable hashes.
- DIALOGUES_KO_VI.md — approved Korean/Vietnamese examples with language review checks.
- PERFORMANCE.md — capped active actors/textures, memory, FPS capture method/environment, known limitations.
- PROTECTED_AUDIT.md — independent verification all approved baseline files remain unchanged.
- QA.md — PASS/FAIL/WARN/NOT TESTED, specific open issues, unmodified unit/E2E assertions.
- REVIEW.html — visual review overview with easy links, no false evidence labels.

Visual media:
- One 26-character native 1:1 roster sheet (native assets; review enlargements must use integer nearest sampling).
- A separate historical timeline roster (6) and modern original culture roster (6).
- At least one side-by-side actual Phaser comparison per wave, anchored to Juni and three approved pilots.
- Actual world screenshots and meaningful gameplay video of representatives in each zone.
- Source master, four-view turnaround, full atlases and animation evidence for every new NPC.
- Record if a preview is SOURCE animation rather than actual Phaser gameplay.
- A downloadable, independently runnable, extracted-package-tested playable ZIP (the approved world + all 12 players + 28 cosmetics + original 14 residents + rotating 12 new characters).
- Full tool logs and reproducible paths; links must exist and open. Do not state 'uploaded/published' unless verification succeeds.

Automated QA:
1. Baseline source/hash preservation, including exact approved three pilot assets, 12 playable atlases and canonical world.
2. Existing tests unmodified/unsuppressed; run real tests after each group and report final counts from logs.
3. Atlas dimensions, presence, frame registration and alpha integrity on every new sprite.
4. 4-direction gait and continuous foot contact; compare to approved Juni phase behavior and correct right/left facing.
5. Actual Phaser readback matches expected native pixels; no canvas scaling blur.
6. All collision/nav/interactions for old and new NPCs.
7. No regressions to dialogues/persistence/Character Studio/mobile touch.
8. Asset ownership and runtime memory/culling bounds.
9. Historical factual accuracy and modern likeness/legal matrix complete. Automated tests cannot certify artistic or legal approval.
10. Physical device/performance status honestly NOT TESTED unless tested on real hardware.

Rollback/branch policy:
- Preserve all previous approved milestones and the user's three-pilot checkpoint.
- Create a new feature branch if necessary, never force-push or overwrite protected approval tags.
- Do not commit huge duplicate ZIP artifacts repeatedly or delete originals without written evidence and a recoverable checkpoint.
- Do not merge to main or deploy without explicit human approval.

========================================================================
10. STOP CONDITION AND REQUIRED FINAL REPORT
========================================================================
At the end of the work, return a CONCISE Vietnamese summary containing:
- Three user-approved pilot artwork sources locked: exact checkpoint/commit.
- Eleven rebuilt resident NPCs: 11/11 with visual previews.
- Historical educational figures: 6/6 with era/date/source validation.
- Modern-original culture NPCs: 6/6; list separately any real celebrity licensed cameos (default 0 unless written permission exists).
- Total NPC definitions = 26; actual simultaneous activation cap and loaded textures reported from code/profile.
- Actual independent gameplay ZIP download link, visual gallery link, screenshot/video links.
- Unit/E2E/build/asset verification results including source log references.
- All remaining warnings/failed tests/open issues; device status accurately identified.
- Full preservation audit of world, Juni, 12 players, 28 cosmetics, three approved pilots.
- Confirm no main merge and no deployment.

Final acceptance rule: The new NPCs must look like they came from the same high-quality artist/pixel-art pipeline as Juni and the approved three, while their era, clothes and personality are credible. A technical sprite count is NEVER a substitute for attractive visual artwork.

DO THE ACTUAL WORK in this continuation. DO NOT simply restate a plan, create placeholder assets, or send a report claiming that an unexecuted step is complete. STOP only for a genuine tool/rights blocker or after the full review candidate is ready.
