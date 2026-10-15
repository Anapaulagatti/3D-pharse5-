# Optional future Korean Arena integration — NOT IMPLEMENTED

This standalone Phaser repo does not edit or connect to the separate production Next.js/Supabase project. No tables/migrations/auth/deployments run there. Future contracts require owner review: IdentityAdapter (guest→explicit account claim), ProgressService (versioned attempt/mastery events, no coin-as-mastery), PresenceTransport (room-scoped authenticated authoritative movement), FriendsRepository/ChatService (preset-only until moderation verified), RewardLedger (idempotent server grants).

SupabaseAuth/Postgres and Cloudflare Worker/Durable Object WebSocket Hibernation are later integration targets, not installed/deployed services. Gate5 must first verify a local authoritative room with two real browser clients/reconnect/rate limiting/negative auth. No real online player or revenue claims.

Direct TOPIK/EPS main-app entry may later be linked with approved routing; no examination is implemented by this art proof. HTML Hangul remains Unicode/NFC with Vietnamese guidance. No game score is official certification. No credentials/real learner data required.
