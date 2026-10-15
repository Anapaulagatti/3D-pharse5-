# KOREAN ARENA — UNIFIED PIXEL SOCIAL LEARNING RPG MASTER v4
## One concise, executable prompt for Codex Desktop / App

Act as Game Director, Senior Pixel Artist, Phaser Engineer, Multiplayer Architect and Korean Learning Designer. Work **ONLY** in `Anapaulagatti/3D-pharse5-`, pixel branch `rebuild/pixel-social-rpg-v3` (verify actual HEAD; `2554327` is only a previous review checkpoint). Do not change the separate Korean Arena main app.

### 1. Product goal
Build **Living Pixel Seoul**, a FREE, original, top-down/three-quarter 2D **social Korean-learning RPG**. Players create/customize avatars, explore a shared town, meet friends, chat/emote, do stories and minigames, co-op, fair PvP, and learn from zero Hangul through TOPIK I/II and EPS-TOPIK. **The gameplay must be fun independently of the lessons; Korean becomes the skill that helps players succeed.** Serious courses/SRS/exam practice remain free and directly accessible, never locked behind story progress. No blockchain, NFTs, paid advantages or gambling.

### 2. Safe 3D-to-2D migration
Audit Git, `STUDIO_*.md`, existing Phaser code, tests and active deployment. Verify the entire old 3D history/assets are backed up in a remote Git branch/tag **and perform a recovery test** before removing obsolete GLB/Blender/Three.js/R3F/Drei files and dependencies **from the active pixel branch only**. Keep archived branches, passed 2D code/tests and the existing public v0.5 Pages release untouched. No force-push. Document deletions and exact rollback steps.

### 3. Install and verify the toolkit
Use **Phaser + TypeScript + Vite**, Vitest, Playwright, editable pixel sprite/atlas pipeline, Tiled-compatible JSON maps, lint/typecheck/CI. Inspect before installing; add missing free, compatible dependencies with lockfile. Detect Tiled and LibreSprite; use tested CLI/headless replacements if GUI apps cannot run in Codex. Discover existing `SKILL.md` skills; optionally inspect/test `0x0funky/agent-sprite-forge` for 2D sprites/maps **only if useful**, with licenses and any paid API requirements checked first. Never silently invoke paid APIs. Write `INSTALLATION_MATRIX.md` and `SKILL_REGISTRY.md` with installed, smoke-tested, unavailable and deferred status; never claim a tool works without proof.

### 4. Final art direction: ONE unified style, NOT A/B/C
Previous minimalist and painterly pixel proposals are **rejected**. Create **ONE** original, coherent social-town aesthetic inspired by the **visual discipline and playable-world feel** of Pixels.xyz. **Never copy Pixels.xyz sprites, map, UI, logo, characters or proprietary assets.** Study user-provided screenshots as references only.

First write `PIXEL_ART_BIBLE.md`: tile/sprite sizes, projection, player-to-building scale, camera zoom, pixel density, palette, shading/outline, shadows, layers, colliders, sorting, animation timing and atlas budgets. Enforce a **consistent pixel grid** throughout. Nearest-neighbor, crisp DPR1/2, integer zoom when possible; no blurred downscaled AI paintings, isolated illustrated backdrops, mismatched pixel density or decorative assets dwarfing avatars. Render Korean lesson/exam text with accessible HTML fonts, NOT tiny pixel Hangul.

**Avatar:** immediately recognizable **while idle**: cute face, hair, outfit and signature accessory. Create true 4-direction idle/walk/**distinct run** cycles, blink, wave, celebration and social pose; no sped-up walk masquerading as a run. Demonstrate 2 hairstyles, 2 outfits, one accessory on consistent layered sprites with correct four-way registration.

**World:** genuine modular playable Tiled/Phaser tilemap, NOT a picture. 2D-drawn building volume (hanok roof/eaves, front/side walls, foundations, recessed doors, steps, contact shadows); trees with layered leaf clusters, readable trunks, highlights/shadows; coherent paths, curbs, grass, flowers, signage, lanterns, stalls and seating. Detail must remain readable and visually balanced with character scale. Authentic but original Korean cultural motifs; no copied location imagery.

### 5. One social town hub, not a whole MMO yet
Make **Central Plaza / Living Pixel Seoul** with collision-safe roads, a courier station, quest board, Korean-style house, café/social meeting place, Hangul puzzle station, TOPIK entrance, PvP sign/portal, outfit corner and landscaped zone. Show room for player gatherings, chat bubbles, emotes and NPC activity. Landmark inspiration may include Bukchon, Gyeongbokgung, Hongdae, Myeongdong, Jeju and Seoul Subway, but **stylize originally**. Simulated people must be labelled demo NPCs, not real connected users.

### 6. Gameplay-first progression
Story: **The Lost Letters** — language fragments have vanished and the player helps restore a living town. First 10–12-minute playable quest **“The First Delivery”**: intriguing NPC intro → freely explore → find letter fragments → learn only the Hangul required → **repair a sign by manipulating syllables** → decode a Korean address → navigate and deliver a parcel → visible town restoration → earn cosmetic currency, unlock a story mystery. NO chain of generic worksheets.

Design satisfying loops: **30–90 sec** micro-interaction, **3–5 min** minigame, **10–15 min** quest/social session, **weekly** cooperative town restoration/event, **long-term** mastery, outfits, achievements, friendships and optional fair ranks. Rotate mechanics, contexts and story choices; offer helpful hints, adaptive difficulty and SRS reviews, avoiding punishing streaks or grind. Separate cosmetic XP/currency from validated Korean mastery and formal exam scores.

### 7. Mini-games: backlog of 35, build only 2 first
Create a documented 35-game design backlog (objective, learning outcome, mechanics, feedback, difficulty, solo/co-op/PvP, accessibility):
- **Hangul (7):** Letter Catch; Syllable Forge; Sign Repair; Batchim Bridge; Sound Detective; Tile Hop; Glyph Maze.
- **Vocabulary (7):** Courier Rush; Market Orders; Café Service; Item Hunt; Fishing Words; Memory Market; Inventory Craft.
- **Grammar (7):** Sentence Builder; Particle Switch; Dialogue Branch; Grammar Locksmith; Word-Order Rails; Story Repair; Verb Tense Forge.
- **Listening/speaking (7):** Subway Directions; Audio Detective; NPC Echo; Announcement Rescue; Rhythm Listening; Conversation Relay; Picture-from-Sound.
- **Multiplayer/exams (7):** Spelling Duel; Meaning Match Arena; Listening Duel; Team Relay; Co-op Sign Rescue; TOPIK Time Trial; EPS Safety Simulation.
Implement **Sign Repair and Courier Rush first**, with original reviewed Korean content. TOPIK I/II and EPS-TOPIK formal prep must remain separate, serious, directly accessible and based on lawful original/validated practice, with no false claim of official endorsement.

### 8. Avatar, multiplayer, social and PvP architecture
Prepare systems for layered outfit inventory, emotes, friendship, chat, party, co-op, room presence and PvP matchmaking. **Prototype locally first** and identify mock features plainly. Design adapters for the eventual Supabase profile/progress database and Cloudflare Worker/Durable Object WebSocket rooms; do not invent live players or promise full MMO. Plan room limits, reconnection, interest management, anti-cheat, rate limiting and cost safeguards. Server must authorize persistent rewards, results, economy and ranked PvP. Match PvP by Korean proficiency; ad views or cosmetics must never confer competitive advantage. Public chat requires reporting/block/mute, moderation, privacy and age-appropriate safeguards **before** open deployment.

### 9. Optional rewarded ads are for server funding
The owner wants ads **only to help pay future hosting and server expansion**. Game/learning/PvP remain fully accessible without ads. Create a `RewardedAdProvider` interface, **DISABLED by default**, plus a clearly marked development stub. Real ad provider, consent, policy checks, anti-fraud and server-verified reward grants require separate approval. Optional rewards may increase **cosmetic-only Town Coins/decorations**, paid on top of an already granted base reward. **Never** double educational mastery, ranked scores, exam privileges or essential progression; no forced ads, dark patterns, NFTs or pay-to-win.

### 10. Build gates, proof and recovery
**Gate 0:** audit current pixel branch; verify archived 3D remote restore; save checkpoint.
**Gate 1:** verify/install only missing toolkit/skills; clean obsolete active-branch 3D; build/typecheck/test PASS.
**Gate 2 — DO THIS NOW:** write art bible; implement ONE cohesive avatar, modular hanok/tree/paths, Central Plaza, actual Phaser idle/walk/run/emote/outfit demo. Capture **real engine output**: gameplay overview, idle close-up, house/tree details, 1×/2×, mobile, outfits, real animation video, rejected-vs-new comparison. Verify files represent what actually runs. **STOP FOR USER VISUAL APPROVAL.** Do not produce another A/B/C concept set.
**Gate 3 (after approval):** playable First Delivery, Sign Repair and Courier Rush, learning overlays and visible rewards.
**Gate 4:** cosmetics + safe social proof-of-concept; real multiplayer only after backend/security testing.
**Gate 5:** co-op, fair PvP, advanced learning integration and optional ad adapter, each separately approved.
**Gate 6:** real-device performance/load, content accuracy, accessibility, security and publication review.

At every gate preserve editable source PNGs/tilemaps, provenance/licenses, art QA, playable package, automated build/typecheck/lint/unit/Playwright results and actual screenshots. Measure performance; never invent FPS, a completed multiplayer backend or ad revenue. Update `STUDIO_TASKS.md`, `STUDIO_PROGRESS.md`, `STUDIO_DECISIONS.md`, `STUDIO_ASSETS.md`; commit/push **verified recoverable GitHub checkpoints** and a `NEXT SESSION HANDOFF`. No new public deployment, paid service or changes to the separate Korean Arena app without explicit authorization.

**START EXECUTING NOW.** Make one **original, visually coherent, lively, pixel-perfect social Korean-learning town that actually plays like a game**, with the quality discipline of Pixels.xyz but none of its copied assets. Complete Gates 0–2 and stop for my visual approval before scaling content.
