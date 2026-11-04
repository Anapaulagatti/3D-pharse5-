# Living Pixel Seoul — roadmap and approval gates

Authoritative: docs/reviews/unified-v4/KOREAN_ARENA_PIXEL_UNIFIED_MASTER_V4.md. Gates0–2 only execute now. Everything below Gate3 is a design commitment/backlog, not shipped functionality. No public replacement, ads, paid API, real accounts or separate Korean Arena production changes.

| Gate | Deliverable | Approval boundary |
| --- | --- | --- |
|0| Audit, previous pixel checkpoint/tag, independently restored3D archive2738hashes | Required before removal; no further3D deletions needed |
|1| Retained Phaser/TS/Vite, tool/skill matrix, headless PNG/Tiled pipeline, build/unit checks | Reuse exact packages/lock |
|2 NOW| One original cohesive Central Plaza, modular kit, layered avatar2hair/2outfits/accessory, four-way distinct run/idle/walk/social emotes, actual Phaser evidence and HTTP ZIP | STOP for visual approval |
|3| First Delivery, Sign Repair and Courier Rush, reviewed Korean overlays and visible base/cosmetic rewards | Only after visual approval; human Korean review before validated release |
|4| Outfit inventory/local social proof, then safe backend presence | Separate approval; backend/security/moderation tests before real players |
|5| Weekly co-op, proficiency-matched fair PvP, advanced learning, optional disabled ad adapter | Each separate approval, never pay-to-win |
|6| Physical-device performance/load, learning accuracy, accessibility/privacy/security and publication | Separate publication approval |

## Gameplay-first loops

The Lost Letters: language fragments vanished; restoring streets reveals personal stories. Players should enjoy exploration, manipulation, timing, choices and social collaboration independently of lessons. Korean becomes a useful skill rather than a worksheet gate. Free courses/SRS/TOPIK I/II/EPS-TOPIK prep remain directly reachable, not locked by quests, ads or purchases. No official endorsement claims or copied exam materials.

30–90seconds: identify a sound, rotate syllable tiles, restore one sign; immediate visual/audio-option feedback and a helpful retry.3–5minutes: courier route/café order/sign forge with alternate contexts.10–15minutes: a complete story/social session with closure. Weekly: optional cooperative town restoration, no missed-day penalties. Long term: mastery, achievements, friendships, outfits and optional fair ranks. Adaptive hints and SRS use reviewable learning evidence; cosmetic XP/Town Coins remain separate from mastery and formal scores. No punishing streaks, required grind or essential progression locks.

## Gate3 First Delivery — planned10–12minute vertical slice

1.0–1: Mira shares an intriguing damaged postcard and a choice of whom to help; original dialogue, no false live-player presence.
2.1–3: freely explore courier/café/garden; collect three letter fragments by observation, with map/text/contrast hints available.
3.3–4: introduce only Hangul needed for this delivery; accessible HTML text and optional original/appropriately licensed reviewed audio. All content pending human Korean review until signed off.
4.4–6: **Sign Repair**: drag or keyboard-place initial/vowel/final components into syllable blocks, preview/undo, see the sign relight. This is manipulation with meaning, not a chain of quizzes.
5.6–8: decode a Korean address using the repaired sign and a clue; alternative hint path, no punitive timer.
6.8–10: **Courier Rush**: plan/navigate a parcel route with meaningful landmarks and optional timing; reduced-speed/no-time mode, same essential learning/rewards.
7.10–12: deliver to a distinct recipient, visible window/sign/garden restoration, already granted base cosmetic reward, story mystery. Town Coins cannot change mastery/ranks/exam access. No ads in this gate.

## Social/server boundaries — design only

Local avatars/NPCs are labelled demo; no invented online counts. Eventual ProfileProgressAdapter separates local prototype storage from Supabase profiles/progress; RoomAdapter separates local events from Cloudflare Worker/Durable Object WebSocket rooms. Do not provision services yet. Start with a measured provisional24-player room cap, position updates10Hz, interest-radius filtering, bounded payloads and idle disconnects; revise only after load/device tests. Reconnection uses authenticated short-lived session/resume IDs and authoritative state snapshots; never trust local rewards.

Server validates identity, movement bounds/speed, interactions, reward grants, inventory/economy and ranked results; idempotent event/reward IDs and replay rejection. Per-IP/session rate limits, message byte ceilings, room concurrency/budget caps, egress monitoring and a kill switch prevent uncontrolled costs. No secrets in clients. PvP matches Korean proficiency with compatible assists; cosmetics/ad views never improve competitive stats. Before public chat: report/block/mute, moderation queue/escalation, spam filtering, retention/privacy/age-appropriate safeguards and tested abuse response. Accessibility includes keyboard, captions/text alternatives, reduced motion, high contrast and non-timed alternatives.

## Rewarded ads — Gate5 disabled design contract

No ad SDK/provider is installed or invoked. Future RewardedAdProvider exposes availability, requestOffer and show(userExplicitOptIn, offerId), returning proof-for-server or cancelled; disabled provider always reports unavailable. A clearly marked development stub may simulate outcomes only after that gate is approved. DISABLED is the default. Real provider/consent/privacy/policy checks, fraud prevention, receipts and server-verified idempotent cosmetic grants need separate approval.

Base rewards are granted first and available without ads. Optional offer adds cosmetic-only Town Coins/decorations, never mastery, exam privileges, ranked scores, essential resources or progression. No forced ads, hidden preselection, dark patterns, paid advantages, gambling, NFTs or blockchain. Ads are optional support for future hosting expansion; revenue/cost coverage cannot be promised. Budget limits and provider kill switch required.

## Learning content and validation

35games are specified in UNIFIED_V4_MINIGAMES.csv. First two implementations are Sign Repair/Courier Rush after Gate2 approval. Each uses original lawful content with provenance, NFC text and status PENDING_HUMAN_REVIEW until an identified qualified reviewer signs off; automated schema checks do not substitute for language review. Formal TOPIK/EPS practice is separate and accessible directly. Microgames can contribute practice evidence; mastery/formal scores require validated assessment rules, never ad/cosmetic multipliers.
