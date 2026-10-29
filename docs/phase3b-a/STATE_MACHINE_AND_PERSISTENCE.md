# In-place actor FSM and persistence

NPCActorModel remains the only behavior controller. ActivityIntent adds schedule ID, high-level activity, context, a route index and KO/VI status. It does not change NPCDefinition, route coordinates, speed, footprint, source frames, animations or identity/save keys.

Priority is TALK/GREET, then safe route recovery, then the latest schedule intent, then ambient variation. TALK holds exact position. A time change can replace intent while speaking; after close RETURN_TO_ACTIVITY resumes the current task rather than an expired patrol. Existing authored dialogue IDs, choices, vocabulary and future inert hooks remain intact.

Actors traverse the original adjacent cyclic route segments until the selected existing anchor. No direct diagonal shortcut, position assignment, impossible interior, train boarding, ferry use, obstacle deletion or world-art edit is introduced. Inactive actors are not position-simulated; their retained record is validated by the existing NPCStateStore on load. Invalid positions return to the original declared spawn through the existing validation policy.

WORK/SOCIAL_PAUSE use existing activity clips, movement uses existing distance-based walk frames, and breaks/rest use available idle/turning. No claim of new sitting, watering, eating or harvesting art is made. After three blocked attempts a five-second backoff keeps the actor at its safe current position. Existing soft yielding and occupancy radii remain; no new solid is added around NPCs.

The existing `korean-arena-npc-world-v1` and `korean-arena-npc-visits-v1` contracts remain. Legacy visitor API calls without game time still behave as before. Ordinary runtime supplies game minute/day/seed and individual visit windows, including deterministic quiet slots. A visitor in conversation retains its host slot past its time window. Archive selection replaces its canonical host and competing visitor using the original layer.

The new clock key is additive. Current-entry checkpoint storage is capped at 26; FSM transition history remains 32; no per-schedule timer handles or growing daily logs are stored. Actor/texture/loading caps remain 4/4/2. Source controls, collision, Character Studio, world, twelve players and 28 cosmetics are protected.
