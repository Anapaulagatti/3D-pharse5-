# Living Seoul — master plan / first connected review slice

Latest authority: `docs/current/LIVING_SEOUL_DISTRICT.md`. The final sentence sets the first delivery gate: master plan, then **one connected playable expansion**, with evidence before the remaining areas are mass-produced.

## Whole-neighborhood plan (planned, not generated)

A fictional Seoul-inspired neighborhood, not a reconstruction of Seoul or another game's map. Coordinate system: world pixels, Y south. Planning envelope 4096×2304; develop only occupied, tested chunks. Roads bend around courtyards, with a broad civic promenade, a smaller book alley and garden shortcuts. Walking speed remains60/run100; Juni remains80px tall, collider16×8. Native32px terrain, camera integer1×/2×, follow exploration, no fit-whole-world camera.

| Area | Planning footprint | Entrance / purpose / connections | State |
|---|---|---|---|
| Gwanghwamun | 0,0–1024,768 | Existing gate, Sejong statue, stream bridge; east book-alley link at y540–640 | Preserve all original source pixels/placements |
| Academy + library | 1024,0–2048,768 | South-facing hall; courtyard door at(1536,434), route approach(1536,490); reading kiosk at east garden | **First playable expansion** |
| Invention workshop/observatory | 2048,0–3072,768 | Scientific court and roof instruments, approach from southwest | Future, no art/NPC production yet |
| Art hanok/botanical garden | 0,768–1024,1536 | Painting courtyard, winding garden paths, stream overlook | Future |
| Market/residential alleys | 1024,768–3072,1536 | Small shops, homes, cafés and resting corners, connections north and west | Future |
| Museum/strategy pavilion | 3072,768–4096,1536 | Naval-history exhibits and map terrace, east/south approach | Future |
| Namsan-facing park/residential edge | 1024,1536–3072,2304 | Secondary loop joining garden, market and museum; seasonal exploration | Future |

Each future historical guest belongs to their building: Sejong/Academy, Jang/workshop, Saimdang/art garden, Yi/museum. They are educational guests from different eras, not represented as contemporaries. A plan marker is not an animated NPC or delivered activity.

## First build: Plaza → Book Alley → Academy courtyard → reading room

Outdoor extent **2048×768**, twice the existing traversable map area, not a blank fourfold enlargement. The west1024×768 is copied without moving approved objects. Ground continues east into a curved book lane, academy front court, library kiosk and garden resting loop. Existing bridge remains functional. Main routes at least64px, entrances48px or wider. Benches flank gardens; onggi flank timber walls; lamps mark lane turns; books/stationery cluster at the kiosk. Trees use trunk-only footprints and opaque pixel occlusion.

New art: one original, reference-grounded academy hall; a small shared-style prop kit for the reading room/library courtyard; generated wooden floor material. Reuse approved trees, walls, lanterns and garden props without regenerating them. All layers, source images, extraction metadata, collisions, entrances and Tiled export stay editable. Art generation uses host image_gen only; paid APIs forbidden even if keys appear.

One lightweight interior, lazy-loaded on entry, links reciprocally to the academy entrance. A Vietnamese-first Hangul matching station works independently of unreleased NPC art: ㄱ/giyeok, ㄴ/nieun, ㅁ/mieum. Persist only completion locally with schema validation and storage-failure fallback. It is an explicitly limited letter-name introduction, not pronunciation certification or a full Korean course. No replacement with rejected historical sprites, no fabricated four-NPC animation claim.

Review evidence: full actual map overview, native/detail desktop and mobile Canvas screenshots, normal-speed real-input exploration video crossing the old/new boundary and entering/exiting the room, activity/reload test, reachability/collision/depth/pause/reduced-motion checks, static review ZIP. Mobile is emulation, not physical-device performance certification. No website publication.

## Milestone boundaries

- A: master layout, source/recovery checkpoint, route/scale review.
- B: connected outdoor slice; actual Forge validation/nav/Tiled + Phaser evidence.
- C partial: Academy only, reachable reciprocal entrance and reading room.
- D deferred: four premium historical guests and their animation pipelines, after this spatial/art review.
- E partial: one original letter matching activity, minimap and local progress. Other activities/quests deferred.

Stop after this first review package. Preserve old town, plaza-review entry, all approved animation assets, source/history and separate learning application. Do not cleanup, expand remaining districts, promote main or deploy Pages.
