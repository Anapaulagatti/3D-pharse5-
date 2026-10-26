# Future gameplay contracts — not implemented

Phase1 stores only versioned character preferences, never an authenticated account or learning progress. `src/platform/contracts.ts` declares interfaces only: no service instances, routes, SDKs, quiz/reward logic or decorative controls.

`PlayerAccount -> PlayerProgress + preferences.selectedCharacterId`: avatar choice changes only the latter. Lessons, level, XP, inventory, wallet and quests have independent ownership; a future server adapter replaces local preferences without migrating/resetting learning data. No connection to the separate learning website is made.

NPC Registry references character/art, dialogue and quest IDs. Dialogue Engine drives conversations; Quest State Machine owns objective/quiz/reward state. Inventory, Currency Wallet, Farming Plots, Crafting/Gathering and Shops expose future ports. Existing map/farm scenery is frozen; no timers, harvest, shop or NPC simulation exists yet.

Required future sequence:
`ACTIVE -> OBJECTIVE_DONE -> QUIZ_PENDING -> QUIZ_PASSED -> REWARD_GRANTED`.

Incorrect Korean answers stay QUIZ_PENDING and request a DIFFERENT question (exclude previous IDs) at the same appropriate level. KoreanQuestionProvider must prioritize verified progress from the main learning site only when an authorized integration exists. Missing/unverified progress uses beginner curriculum. LessonProgressProvider and answer verification remain external ports. RewardEligibility requires a verifiable quiz receipt and idempotency key before granting rewards; no client boolean can grant a reward.

Ads are optional. Base rewards never require an ad. Ad availability, cancellation or failure cannot block ordinary quest completion. A validated provider receipt may grant only the additional amount up to the designed2x total. A client claiming it watched a video is insufficient; backend/provider receipt verification and replay prevention are required. No ad SDK or monetization is installed in Phase1.

PlayerCharacterManager owns one active sprite and pose instance; scene owns movement, collision, visited locations and camera. Loading a replacement atlas validates all required native frames BEFORE destroying the previous sprite. Transition/shutdown guards reject unsafe replacements. Completed characters use common controller60/100px/s; Juni retains the exact original JuniMotion class. Future atlas-specific RegistryMotion consumes actual distance and authored clips, never moves the actor. New identities cannot become playable until their measured native scale/contact envelopes and complete animations are verified against the frozen world. Current3new identities remain incomplete; this is not a four-character production acceptance.
