# Local candidate architecture and explicit limits

## Protected foundation

One canonical world manifest, unchanged source images/masks/building registrations. Existing PlayerCharacterManager and JuniMotion/RegistryMotion remain the only player engine. One player Sprite is transferred between Scene display/update lists; the original NPC actor is borrowed with the same model/atlas, never a second public identity. The source world pauses before asset handoff, pinning all active NPC textures within the existing4texture/2load limits. Both update and display ownership are removed before scene reassignment; the old queue is flushed so shutdown cannot destroy borrowed actors.

Three entrances derive from canonical targets: cafe717,2605; bookshop1128,2605; learning1418,2605. No facade changes. Indoor floor/solid bounds are explicit room data. Indoor objects use original native component props, actual player movement and context/range checks. Exact world return coordinates/camera are retained; additive local interior-save supports reload. Rendering remains1:1 nearest. New indoor art is independently code-authored, not painted Gate1-equivalent art acceptance; human quality review remains PENDING.

## Farming and progression

Six native approved beds/36cells, unchanged IDs/footprints. Existing radish/scallion frames copied byte-exact into a new extended atlas; ten independent authored native crop sets. Each phase has stable root20,40 in40×44; separate16×16material owners, no new whole-bed scene plate. Existing base assets stay immutable.

Radish/scallion initially available. First farm quest completion unlocks carrot/cabbage. Market quest completion unlocks remaining8crops. Both buying and sowing check the same unlock predicate; possessing an injected locked seed is insufficient. New item stock is migrated additively, without refilling exhausted old stock. Old6plot/current36cell saves and all previous quest receipts remain readable. First upgrade write backs up the original save; invalid saves block writes and can be exported/restored from validated backup. Harvest/sales/rewards remain idempotent within a single atomic local snapshot. A one-use emergency seed is available in person from Cheolsu only when no seeds/crops remain.

Local save is **not server authority**. Validation rejects malformed crop durations, ordering and receipts; machine clock/localStorage tampering cannot be prevented reliably offline. No real economic balance, authenticated ownership, production mastery or formal exam scores are claimed.

## Physical learning loop

Existing first seed / market quests are retained. Added carrot task and eight-step first-delivery quest: seed-shop visit → workshop fragment → bookshop fragment → seed-shop fragment → repair책by piece order → workshop route start → seed-shop address → bookshop delivery → Korean retry/correct answer → exactly-once reward. The sign accepts mouse/touch buttons, native drag/drop and1/2/3/Backspace/Enter. Courier route is deliberately untimed, an accessibility assist with equal rewards; it is not live competitive/ranked play. Fragments visually disappear as acquired; restored sign persists via quest state.

Korean examples are original local beginner drafts, NFC, statusPENDING_HUMAN_REVIEW. No officialTOPIK/EPS equivalence or textbook/exam-bank source. Town Coins/gameXP never write website mastery/FSRS/student records.

## Gate4/5 boundaries · not live services

LIVE_FEATURES disables multiplayer/matchmaking/ranked/chat/ads/learningSync. ProfileProgressAdapter/RoomAdapter/LearningEvidence contracts separate local prototype state from any future authorized backend. LocalRoomSimulation is explicitly TEST_ACTOR_A/B, not live players, with pure boundary/speed/rate/replay checks and bounded256receipts. No network adapter is instantiated. Disabled ad provider cannot request an ad or grant a bonus. Existing cosmetic wardrobe remains separate from economy.

Future server proposal: provisional24actors/room,10Hz movement, interest filtering, short authenticated sessions, authoritative movement/inventory/reward checks, idempotency and replay rejection; bounded payloads/rates, report/mute/block/moderation and retention/privacy review required before public social features. No provisioning, billing or production load tests. At24actors and10Hz, worst unfiltered peer deliveries5520/s; filtering/rate caps must be measured before approval. Kill switches must disable room admission, chat, rewards and provider calls independently. Advanced learning/FSRS sync remains DEFERRED.

## Publication/history storage

New candidate is local-only until exact manifest owner approval. Existing Pages1a6e5a58/331cd300 remains a verified playable rollback, run41852211445. Its997.56MBsite is already near the1GBbudget. This candidate package includes current game + selected review evidence once, without duplicating all historical websites. Existing immutable artifact branches/tags/checkpoints retain previous versions; no historical asset is erased or overwritten. A future publication packet must explicitly approve this retention approach and update the history gate transparently, never bypass it.
