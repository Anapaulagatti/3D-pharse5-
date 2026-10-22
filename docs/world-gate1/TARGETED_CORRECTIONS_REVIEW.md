# Gate 1 — three targeted corrections

22 October 2026, Asia/Saigon. **Final Gate 1 approval remains withheld. Gate 2 is locked.** This changes only Jeju, the station precinct and local walking connections. No production artwork, whole-world rebuild, main merge or deployment.

## Revised in-engine evidence

- [Planning board](MASTERPLAN_BOARD.png) and [browser-friendly Phaser overview](MASTERPLAN_REVIEW.png).
- [Native full graybox, 4096×4608](GRAYBOX_NATIVE_4096x4608.png).
- [Jeju spatial plan at native 1:1, 1024×1536](JEJU_SPATIAL_NATIVE_1X.png): oreum, basalt, orchard, culture court and ferry landing in one actual Phaser view.
- [Station spatial plan at native 1:1, 2048×1130](STATION_SPATIAL_NATIVE_1X.png): building, entrance plaza, two platforms, track approach and pedestrian overpass with Juni on platform 2.
- Native details: [oreum](JEJU_OREUM_NATIVE_1X.png), [basalt](JEJU_BASALT_NATIVE_1X.png), [orchard](JEJU_ORCHARD_NATIVE_1X.png), [culture](JEJU_CULTURE_NATIVE_1X.png), [building/Juni scale](BUILDING_SCALE_NATIVE_1X.png), [preserved southwest Namsan](NAMSAN_SW_NATIVE_1X.png), [preserved southeast amusement](AMUSEMENT_SE_NATIVE_1X.png).
- [Playable ZIP](WORLD_GATE1_PLAYABLE.zip): extract and run `python3 start.py`; open its printed URL. WASD/arrows walk, Shift run, E inspect planning stops, mobile landscape joystick. No Node required to view. New exploration panels describe planned content, not finished quests.

All native images are direct Phaser Canvas exports at DPR1/zoom1. The overview board explicitly discloses its reduction to 25.88%; native evidence is not downsampled. Contours, track symbols and orchard circles are graybox planning geometry, not final art.

## 1. Jeju is now a distinct destination

The generic observatory and its old loop are removed. The island outline, bridge and ferry piers remain valid and unchanged; its internal plan is rebuilt only inside that footprint:

| Area | Reservation and purpose | Access |
|---|---|---|
| Northern oreum | 420×460 volcanic precinct with concentric contour guides, solid crater-core reserve and walkable rim route; eastern rim interpretation/lookout. | Bridge arrival branches to the rim or basalt trail. No actual terrain-height or climbing physics claimed. |
| Western basalt landscape | 260×370 lava/stone precinct with two solid formation reserves and a coastal exploration trail. | Connects bridge arrival to ferry arrival and orchard/culture routes. |
| Southeast tangerine orchard | 340×270 orchard precinct, six planning crowns in two rows, solid trunks and clear walkable aisles. Planned harvest/cultural interpretation. | Orchard trail links the oreum side to the ferry/culture junction. No farming economy implemented. |
| Southwest cultural exploration | 380×290 precinct with a 260×170 stone-culture pavilion pad, front court and western return path. Planned Jeju stone-wall and haenyeo interpretation. | Ferry landing → court, or orchard → court; E planning panel available. No invented finished exhibits or NPC quests. |

The mainland terminal leads via promenade and physical boarding pier to the proposed ferry link. Jeju's west-facing landing at (3240,4100) leads directly to the basalt/orchard/cultural choice at (3520,4100). The bridge's northern arrival at (3530,3570) provides the alternate oreum/basalt sequence. The two arrivals have distinct roles rather than duplicating one observatory stop.

The water crossing remains **planned, not operational**: its dashed line is not walkable and no teleport, vessel or travel-time benefit is counted. All 25 planning destinations are reachable through the existing physical bridge. Both piers remain attached to land and have public approaches.

## 2. Station, not a transit canopy

The full-sized existing civic building pad becomes the **railway station / ticket hall**, retaining its 560×210 ground footprint, 500px elevation reservation and 100px entrance guide. The old standalone canopy is removed. This reuses valid scale/placement work within the affected civic/transit precinct; it does not disturb the historic north or other districts.

The station has a 700×160 entrance-plaza reservation, two 100×400 side platforms, two recognizable tracks with southern terminal buffer stops, and an eastern off-map railway approach. A localized engineering/embankment reservation carries the approach and far platform on solid ground; the railway does not float on water or pass through the historic north. Modern works begin at y2090, south of the protected heritage belt ending y2080.

A 400×100 pedestrian-overpass reservation joins both platforms to the entrance plaza. The graybox uses an explicit walkable crossing mask above the otherwise blocked rail bed. This proves the 2D pedestrian connection; it does not claim finished stairs, bridge elevation animation, running trains, ticketing or rail simulation. Six new unit checks and real-keyboard browser checks cover rails, crossing, platforms and Jeju collision.

## 3. Measured exploration pacing

Juni remains at **60 world px/s walking, 100 running**, unchanged native size. The audit separates three quantities so a better signed route is not misreported as a smaller world:

1. [Collision-aware distance matrix](exploration-pacing.json): all pairs before (18 stops) and after (25 stops), 16px grid, 8 directions, no diagonal corner cutting, using the actual land/solid/rail/overpass rules. Times are distance÷speed estimates, not measured browser wall time.
2. Authored itinerary lengths: the previous roads forced a café→central avenue→Namsan dogleg and market→promenade→terminal dogleg. Collision-clear public ground already permitted shortcuts, but those connections were not represented by clear paths.
3. [Actual before/after keyboard traces and timing](walking-input-timing.json): unchanged source at commit 21554fa served from a separate detached baseline worktree, compared with the revised graybox. One QA placement at each start; all subsequent travel is real normal-speed keyboard input, no Shift or teleport.

| Recommended itinerary | Before: measured distance / time | After: measured distance / time | Correction |
|---|---:|---:|---|
| Café → southwest Namsan | 2503px / 41.71s | 1291px / 21.54s | Local café–garden passage to the existing hill approach, instead of detouring through the central avenue. |
| Market → ferry terminal | 1816px / 30.27s | 1564px / 26.07s | Diagonal market–waterfront connection instead of the promenade dogleg. |

Eight-direction keyboard traces are slightly longer than ideal diagonal polylines. Observed speeds were 59.94–60.01px/s. Raw position/time samples and configured speed are retained. The first connection cuts roughly 48% of the measured signed-route time; the second roughly 14%.

**Honest limits:** the collision-grid minima for café→Namsan (1093.7px/18.23s) and market→terminal (1562px/26.03s) are unchanged: players could previously walk unsignposted public ground. The correction makes shorter exploration routes legible and usable without guessing a cross-grass route; it does not falsely claim that land itself became shorter.

Jeju now has successive oreum, basalt, orchard and cultural purposes instead of one generic destination. Nearest-stop walking gaps for those areas are about 3.58–9.44s on the grid; these are planning/interpretation stops, not claims of completed gameplay activities. Cultural pavilion↔oreum is about 19.74s minimum, and station↔mainland boarding is about 30.85s. Mainland↔Jeju pier travel on foot still uses the bridge and takes about 27.31s minimum; no operating ferry shortcut is invented. The longest all-pairs regional journey is about 77.11s walking; the approved world extent and protected northern geometry are not compressed to conceal that distance.

## Preservation and QA

[Source/navigation audit](source-and-navigation.json) asserts the historic northern buildings, zones, boundaries and paths unchanged; the southwest Namsan and southeast amusement building/zone/route definitions unchanged; original island/bridge/piers unchanged; full-sized commercial reservations unchanged; and 214 original code/art/lock files byte-identical. Original build also checks the existing 336-file protection contract. No legacy southern layouts/art are imported.

[Browser QA](browser-qa.json), [rendered-path audit](rendered-route-audit.json), [QA summary](validation.json), [package verification](package-verification.json), [reproduction](REPRODUCE.md). Relevant checks include 25 reachable destinations, 25 rendered centerlines, rail-bed exclusion, real keyboard crossing of the station overpass, E exploration at all Jeju features and both platforms, shoreline/bridge/collision, native nearest sampling and mobile landscape CDP touch.

One initial curved cultural return trail grazed the pavilion's expanded collider at four sample points; the report is retained in `logs/initial-jeju-curve-diagnostic.log`. The western bend was moved outward and the route rechecked. No collider-clearance threshold was weakened. The original app's known large-chunk build warning remains. Chromium Canvas/mobile emulation does not establish physical-device performance. No GitHub CI or art-quality approval is claimed.

Muneum remains mandatory for BOTH traditional and modern craftsmanship. No new production artwork or Gate 2 samples were created. The north's architectural identity and all approved protected geometry remain intact.

**Do you approve these targeted corrections and grant final Gate 1 approval before Gate 2?**
