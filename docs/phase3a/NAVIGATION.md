# NPC navigation and collision

No new global collision world is introduced. Registered local paths reuse the actual canonical WorldCache.walkable query and original mask/logical-solid sources. Offline read-only QA verifies the complete29×9native contact envelope at every integer position along each edge and the QA approach. Runtime checks contact edges/center and sweeps each movement in≤1px increments. The static world is immutable; no paving/image patch compensates for a blocked route.

Routes are small explicit waypoint loops selected for each workplace. Actor FSM: IDLE,LOOK_AROUND,PATROL,MOVE_TO_WAYPOINT,WAIT,GREET,TALK,RETURN_TO_ACTIVITY. Transitions are validated and history is bounded32entries. Actual distance drives a44px walk stride; facing matches motion. Arrival pauses and role activities are deterministic. Blocked motion waits/retries without teleporting or crossing obstacles.

NPCs yield near the player (24px) and other active NPCs (26px). Their contact is deliberately soft: they never add hard solids to approved player paths or alter player speed/collision. Current patrols are separated and critical contact reservations remain clear. This is not a full crowd simulation or a claim that the old player collision system was redesigned.

Inactive actors keep models/positions/direction/phase/waypoint/timers in memory. Off-zone simulation freezes. Re-activation reuses that state and never duplicates an ID. Separate local state validates positions against declared segments; malformed/off-route data falls back only that NPC to its valid home. Reload restores position/phase/waypoint/conversation count and starts safe activity,never a stuck TALK lock.

[Navigation QA](navigation-qa.json) validates14patrols,actual approaches and critical palace/café/bookshop/station/house/bridge/dock/plot/tower/carousel clearances. [Actual gameplay](gameplay/actual-gameplay.json) observes all14approaches and directional movement. [12re-entry cycles/60dialogues](stability.json) verify stable ownership and no off-zone activity drift.

## Cross-zone integration

[Actual continuous traversal](cross-zone-actual.mp4): mainland promenade → northern Jeju bridgeA → orchard approach → cultural courtyard. One canonical scene,original player keys and original analog joystick for fine alignment; no position/speed/physics/clock override. [Trace](cross-zone-actual.json),[read-only path plan](cross-zone-route.json).

The initial QA shortest-path planner hugged mask boundaries and underrepresented the existing native walking footprint. It was corrected to use the exact union of the original directional walking contact offsets,clearance-weighted planning and verified axis shortcuts. This changed the QA harness only,not approved collision or scenery. Fine alignment uses the original joystick rather than moving coordinates by script. No broader bridgeB or whole-world route certification is inferred from this bridgeA test.
