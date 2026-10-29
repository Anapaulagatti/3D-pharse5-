# Deterministic NPC clock

The single `NPCWorldClock` in `src/npcs/clock.ts` uses a configurable day duration: default 1,800,000 real milliseconds = 24 game hours, initially 09:00. Seed 20261029 plus game-day index and entry ID select deterministic anchor variation. It does not use the user's calendar or timezone.

Boundaries are an exported data table: night 00:00–05:00, morning 05:00–11:00, midday 11:00–14:00, afternoon 14:00–18:00, evening 18:00–22:00, night 22:00–24:00. `phaseAt` accepts a boundary configuration. The existing footer shows game time; world lighting and artwork never change.

Tick clamps finite dt to 0–200 ms, pauses while the host is blocked or the document hidden, and performs no calendar catch-up. Visibility transitions clear actor elapsed accumulation. A frozen browser cannot produce thousands of missed actor steps. Saved game time resumes on reload; offscreen NPCs retain valid route positions rather than teleporting to an imagined destination.

Additive key `korean-arena-npc-life-v1` stores version 1, day, minute, seed and at most 26 schedule-entry IDs. Invalid/wrong-version/nonfinite records safely fall back. QA rate is not persisted. No old NPC, visitor, player, appearance, progress or visited key is migrated/reset.

Only an explicit QA URL in a compiled private-review build mounts Settings clock controls and `__NPC_LIFE_QA__`. Rates clamp to 0–60×. Ordinary query parameters cannot enable the API. Public-build permissions are decided by the Node/Vite asset gate, never a URL or localStorage value.

The six archive inhabitants do not follow contemporary time. While selected, an eight-second local story sequence chooses existing work/walk/break/social/rest entries. Blocked gameplay pauses that elapsed interval. Their seed variation ignores modern day index; the footer explicitly identifies story-local time. Leaving or changing the story resets only its elapsed interval, never a sprite's world coordinates.
