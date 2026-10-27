from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';defs=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs'];baseline=json.loads((D/'approved-baseline.json').read_text());audit=json.loads((D/'protected-audit.json').read_text());TAG='checkpoint/phase3a-living-npc-world-review-20261027'
def put(n,s):(D/n).write_text(s.strip()+'\n')
def load(n):
 p=D/n;return json.loads(p.read_text())if p.exists()else{}
stability=load('stability.json');perf=load('performance-observations.json');source=load('source-qa.json');nav=load('navigation-qa.json');native=load('gameplay/native-pixel-qa.json');log=Path('/tmp/phase3a-locked-e2e.log');e2e='PASS'if log.exists()and'60 passed'in log.read_text()else'PENDING';stats=load('e2e/e2e-results.json').get('stats',{})if e2e=='PASS'else{}
put('README.md',f'''# Korean Arena · Phase3A Living NPC World

Review candidate:14 authored inhabitants in7home zones,within the approved canonical world. Human Phase3A artistic acceptance is PENDING. Phase3B remains LOCKED.

[Playable ZIP](PHASE3A_LIVING_NPC_WORLD_REVIEW.zip) · [visual gallery](REVIEW.html) · [14 actual native NPCs](fourteen-actual-native.png) · [2× nearest review](fourteen-actual-review-2x.png) · [QA](QA.md) · [device handoff](DEVICE_REVIEW.md).

## Authority and recoverability

Human approved Phase2C12characters/28cosmetics/46variants/12looks/Studio/world. Exact review32d7d4743dfe5bd6cb1bc3bfb7eb2525b268af2d; accepted source/receipt `{baseline['approvedCommit']}`. New immutable approval reference `checkpoint/phase2c-fashion-studio-approved-20261027`. Fresh baseline116unit/53E2E passed before implementation; all required command logs in baseline-logs/. Physical-device status and historical WARNs were not promoted to PASS.

Branch `feature/phase3a-living-npc-world`. Four-context pilot `checkpoint/phase3a-four-context-pilot-20261027` (a492d22): actual Seoyeon/Minseo/Harin/Eunji,20native captures,all4walking directions,interaction/return. Only then expanded. Fourteen-resident checkpoint `checkpoint/phase3a-fourteen-residents-20261027` (62644cd),followed by coordinated costume/placement/UX/QA polish. Final review reference `{TAG}`. No historical reference overwritten.

## What is implemented

-14 independent native actor identities;104cells each/1,456total. Four-direction idle and8distinct walk frames,greeting and occupation gestures. Approved Juni motion landmarks guide rhythm; no playable face,costume or atlas pixels were copied.
- Typed/runtime-validated NPC Registry,deterministic finite-state actors,verified local waypoints,canonical collision queries,occupancy/yielding,proximity selection and structured Korean/Vietnamese dialogue.
- Native96×112 registration,48,100foot anchor,integer sprite/camera phase and nearest rendering. Consistent depth and contact shadows. Existing player engine remains the only player engine.
- Zone activation/camera culling/lower offscreen tick rate,at most4active NPCs/4resident NPC textures/2loads. All14records remain available; deactivation freezes intended activity without teleporting.
- Separate NPC-only local state; existing v1/v2 character/appearance,world position,visited markers and progress survive. No new accounts or fabricated learning completion.

## Play locally

Extract ZIP,run `python3 start_review.py`,open `http://127.0.0.1:4378/REVIEW.html`. The actual compiled game runs locally/offline without Node or external APIs. Compact evidence is included; large full traversal/stability recordings and full PNGs may resolve online at the immutable review tag. `--lan` is explicit opt-in for testing on your own LAN,not public deployment.

Choose any of the original12players and original28cosmetics as before. Walk toward a resident; use E,the proximity button or Explore. Read Korean/Vietnamese,choose a topic,advance and close. Residents resume their activity. Normal gameplay has no NPC placement markers. Explicit `?qa&npcReview=npc-...` URLs only select separately documented mask-validated QA approach spawns; they do not alter approved map metadata or normal spawn.

[NPC roster](NPC_ROSTER.md) · [zones](NPC_ZONES.md) · [navigation](NAVIGATION.md) · [dialogue](DIALOGUE_SYSTEM.md) · [performance](PERFORMANCE.md) · [protected audit](PROTECTED_AUDIT.md).

No world regeneration,collision rewrite,map enlargement,approved character/cosmetic/Studio edit,shop/economy/inventory/farming/rewards/quizzes/account sync,paid AI/image API,main merge or public deployment. Stop for human Phase3A review.
''')
lines=['# NPC roster','','14 fictional Korean town residents; names/roles from the human brief. All are separate from the12playable identities. Native source art and new NPC appearances await human artistic review.','','| ID | Name VI / KO | Occupation | Home zone | Activity |','|---|---|---|---|---|']
for n in defs:lines.append('| '+n['id']+' | '+n['names']['vi']+' / '+n['names']['ko']+' | '+n['occupation']+' | '+n['homeZone']+' | '+n['idleBehavior']+' |')
lines+=['','Each has an own authored head/hair silhouette,face details,occupational palette and costume construction. Korean-inspired hanbok/guard clothing,café apron,book-themed cardigan,railway uniform/travel bag,orchard workwear,cultural host,farm apron/seed pouch,outdoor jacket,amusement vest,fisherman clothing and marina blazer are distinct. Seven residents received additional garment construction details during consolidated polish,not palette-only identity substitution. Traditional costumes are historically inspired,not a certified period reconstruction.','','All14support idle2×4,walk8×4,greet8×4 andactivity8×4 =104native cells each. NPC running is deliberately absent. Source: [authoring recipe](../../tools/phase3a/art.py),[registry](../../assets-src/npcs/phase3a/registry.json),per-NPCdesign/clips/native turnarounds under assets-src/npcs/phase3a/. Runtime textures are separate public/assets/npcs/phase3a/. No original player pixels are changed or re-exported.','','[Source QA](source-qa.json) · [actual84native readbacks](gameplay/native-pixel-qa.json) · [full visual/gameplay gallery](REVIEW.html).']
put('NPC_ROSTER.md','\n'.join(lines))
lines=['# Canonical NPC zones and registrations','','World4352×4864,canonical manifest palace-cleanup-world. Position numbers come from approved world targets/regions/farm metadata plus explicit local native registration,then mask and actual-image validation. No structure,reservation or historical masterplan was moved.','','| NPC | Home | Spawn/interaction home | Declared route | QA player approach |','|---|---|---|---|---|']
for n in defs:lines.append('| '+n['names']['vi']+' | '+n['homeZone']+' | '+str(tuple(n['spawn']))+' | '+' → '.join(str(tuple(p))for p in n['route'])+' | '+str(tuple(n['reviewSpawn']))+' |')
lines+=['','Exactly2residents per zone: palace,modern,station,Jeju,farm,nature-leisure,coast. Nature-leisure covers two approved areas (Namsan and amusement),one resident each. Farm bindings use the actual northwestern farm,not an invented interior. Café/bookshop interactions are outdoors; no unsupported interiors are assumed.','','Final spatial QA moved Harin onto the west orchard approach to avoid tangerine foreground-foot overlap; moved Jiho to the bookshop’s western frontage to avoid protected Namsan projection; placed Donghae on the stone coastal promenade and Soobin on the terminal-side sidewalk instead of an asphalt standing position. These are new NPC registration changes only; approved scenery/coordinates are immutable. The local offset selected by the whole contact-field check is explicit in [binding proof](navigation-source-qa.json).','','Station attendants stay on public entrance/waiting paving,not tracks/platforms. Palace actors stay clear of the courtyard axis/main stairs. Jeju house steps and both bridges,dock access,farm plots,Namsan/tower and attraction approaches remain unoccupied by registered patrol contacts. [Critical clearance proof](navigation-qa.json).','','[Review-only placement overlay](npc-placement-map-review.png). The overlay never enters runtime artwork. Bakery allocation and other historical world-planning issues remain outside this NPC-only phase; no old reservation is silently changed.']
put('NPC_ZONES.md','\n'.join(lines))
put('NAVIGATION.md','''# NPC navigation and collision

No new global collision world is introduced. Registered local paths reuse the actual canonical WorldCache.walkable query and original mask/logical-solid sources. Offline read-only QA verifies the complete29×9native contact envelope at every integer position along each edge and the QA approach. Runtime checks contact edges/center and sweeps each movement in≤1px increments. The static world is immutable; no paving/image patch compensates for a blocked route.

Routes are small explicit waypoint loops selected for each workplace. Actor FSM: IDLE,LOOK_AROUND,PATROL,MOVE_TO_WAYPOINT,WAIT,GREET,TALK,RETURN_TO_ACTIVITY. Transitions are validated and history is bounded32entries. Actual distance drives a44px walk stride; facing matches motion. Arrival pauses and role activities are deterministic. Blocked motion waits/retries without teleporting or crossing obstacles.

NPCs yield near the player (24px) and other active NPCs (26px). Their contact is deliberately soft: they never add hard solids to approved player paths or alter player speed/collision. Current patrols are separated and critical contact reservations remain clear. This is not a full crowd simulation or a claim that the old player collision system was redesigned.

Inactive actors keep models/positions/direction/phase/waypoint/timers in memory. Off-zone simulation freezes. Re-activation reuses that state and never duplicates an ID. Separate local state validates positions against declared segments; malformed/off-route data falls back only that NPC to its valid home. Reload restores position/phase/waypoint/conversation count and starts safe activity,never a stuck TALK lock.

[Navigation QA](navigation-qa.json) validates14patrols,actual approaches and critical palace/café/bookshop/station/house/bridge/dock/plot/tower/carousel clearances. [Actual gameplay](gameplay/actual-gameplay.json) observes all14approaches and directional movement. [12re-entry cycles/60dialogues](stability.json) verify stable ownership and no off-zone activity drift.

## Cross-zone integration

[Actual continuous traversal](cross-zone-actual.mp4): mainland promenade → northern Jeju bridgeA → orchard approach → cultural courtyard. One canonical scene,original player keys and original analog joystick for fine alignment; no position/speed/physics/clock override. [Trace](cross-zone-actual.json),[read-only path plan](cross-zone-route.json).

The initial QA shortest-path planner hugged mask boundaries and underrepresented the existing native walking footprint. It was corrected to use the exact union of the original directional walking contact offsets,clearance-weighted planning and verified axis shortcuts. This changed the QA harness only,not approved collision or scenery. Fine alignment uses the original joystick rather than moving coordinates by script. No broader bridgeB or whole-world route certification is inferred from this bridgeA test.
''')
put('DIALOGUE_SYSTEM.md','''# Contextual Korean/Vietnamese dialogue

42 authored nodes (3perNPC),all present in the shipped registry. Every resident has welcome/context/care content,2simple topic choices and an optional next link. Text is authored and deterministic; no AI API,quiz,reward or shop action is invoked.

Nodes carry stable ID,NPC ownership,KO/VI content,locale-aware hint/choice labels,next references,conditions and future topic/hook metadata. Startup validation rejects duplicates,missing/cross-owned links,unreachable nodes and cycles. A defensive8-step cap closes invalid runtime sequences and releases movement safely.

Approach a resident and press E,use the proximity button or the supported Explore control. Eligible visible actors require a valid canonical-ground line and≤92px range. Closest distance and stable ASCII ID resolve priority; a14px hysteresis window prevents near-equal targets flickering. Current routes keep residents apart. TALK pins the selected actor and only one modal can open.

The panel shows VI/KO name,occupation,Korean text,Vietnamese translation,topic choices,Next and Close/Return,plus a native preview from the resident’s actual atlas. It uses its own scoped classes,44px controls and safe-area insets,not the legacy HUD footer’s pointer policy. Keyboard Enter follows focused choices/next; Escape/close always release the lock. Touch/keyboard events stay inside the modal. Movement/analog state is reset through the existing host pause/reset mechanism; no player controller is replaced. Closing returns the NPC to its prior valid activity.

Korean wording was manually checked for polite register,grammar and location/occupation context; translations retain the meaning. These are short beginner-friendly introductions,not authenticated lesson content. Native Korean editorial/human acceptance remains part of final review; automatic Hangul/text-integrity checks do not grant linguistic or artistic approval.

Future NPCLearningContextProvider accepts only an authenticated learning context/curriculum identifiers. No provider is connected now; no lesson completion is invented. Future content should use a beginner curriculum when verified data is absent. Quest/shop IDs are null; equipped cosmetics,owned inventory and future server authorization remain separate. The existing Korean-learning website is untouched.

NPC-only storage: korean-arena-npc-world-v1. Existing korean-arena-player-preferences-v1,korean-arena-appearance-preferences-v2 and world/progress stores are unchanged. [Real landmark visit→NPC dialogue→reload proof](extra-evidence.json) is separate from test sentinels and does not claim external learning-account verification.
''')
put('VISUAL_REVIEW.md','''# Human visual review

[Accessible local HTML gallery](REVIEW.html) · [14 actual native actors](fourteen-actual-native.png) · [2× nearest review](fourteen-actual-review-2x.png) · [review-only placement map](npc-placement-map-review.png).

All native actor cells are96×112,unresampled. Scale pairs show Juni and each resident from the same genuine Phaser backing capture. Each resident has an unannotated full native scene,actual Korean/Vietnamese dialogue image,complete native4direction source walk sheet and real gameplay recording in the gallery. SOURCE sheets are explicitly labeled; they are not passed off as gameplay. JPEGs prove UI layout; lossy MP4s prove motion/timing; native PNGs remain pixel authority.

Inspect14distinct identities/costumes,contact at paving/soil,head/hair/hand ownership,front/back readability and the appropriate surroundings. Check that palace guards/guides preserve historic identity; modern workers belong to storefront/transit paving; orchard/farm residents stay on accessible paths; coastal staff stand on public stone/sidewalk surfaces; no critical entrance is blocked. Seven occupational outfits received additional native garment construction details. No approved player art is copied or modified.

Pilot proof precedes expansion:20native captures/4contexts. Final full coverage:84actual native captures across14residents (4walking directions,occupation activity,greeting),plus complete104-cell source validation and extended real video. This proves source/render agreement and actual behavior,not artistic acceptance.

Mobile evidence: [667×375approach](mobile-667x375-approach.jpg),[dialogue](mobile-667x375-dialogue.jpg),[844×390approach](mobile-844x390-approach.jpg),[dialogue](mobile-844x390-dialogue.jpg). These are desktop browser emulations,not Android/iPhone hardware. Safe-area behavior is implemented; real notched-device acceptance is NOT TESTED.

[Continuous mainland→Jeju bridgeA→orchard→house video](cross-zone-actual.mp4) · [12zonecycles/60dialogues video](stability-actual.mp4) · [media provenance](media-provenance.json). Original recordings are unretimed; review copies preserve1280×900 dimensions. Large recordings may link online from the compact ZIP.

TECHNICAL REVIEW CANDIDATE — ARTISTIC APPROVAL PENDING. Human review must judge character craftsmanship,natural motion,costume authenticity,placement and dialogue. No completed asset count,hash,build or automated test grants visual approval. Phase3B remains locked.
''')
put('PROTECTED_AUDIT.md',f'''# Protected baseline audit

[Approved SHA256 manifest](approved-baseline.json) · [audit report](protected-audit.json).

Accepted Phase2C `{baseline['approvedCommit']}`; original review32d7d47. Permanent approval tag checkpoint/phase2c-fashion-studio-approved-20261027.6382acceptedasset/source/toolfiles are frozen,including12player atlases,all28cosmetics/46variants,the complete canonical world and historical source/generation tools.

Exactly6additive NPC integration blocks are permitted in src/gate3/main.ts: imports,QA-entry helper,manager field,creation/shutdown host,interaction priority and update. Removing those marked blocks reproduces the accepted scene byte for byte. Player movement,collision,camera,tour and existing UI logic are not rewritten. All other approved src files,including Character Studio/preferences/appearance rendering,are exact. [Approved scene snapshot](approved-main.ts.txt).

| Player | Approved atlas SHA256 |
|---|---|
'''+''.join('| '+id+' | `'+sha+'` |\n'for id,sha in baseline['baseAtlases'].items())+'''
Original artworks/checkpoints/tags remain recoverable. NPC art/data/tools live in separate directories. World overlays are docs-only,never new ground assets. No historical plan,reservation,station pivot,bridge,forecourt or source image is silently edited.

Preservation regression tests retain their original assertions and now invoke the stronger Phase3A audit recognizing only exact removable integration hooks. No test is deleted/skipped and no old motion threshold is weakened. Source-based and actual-control NPC checks were added.

Reproduce `python3 tools/phase3a/protected.py`. New NPC provenance and all original protected hashes are provided; no source hash is updated to bless an unauthorized change. No main merge,force-push,protected checkpoint overwrite,learning-site edit or deployment.
''')
# Report raw measurements only; do not convert atlas ownership dimensions into totalGPU memory.
if stability:
 samples=stability['samples'];heaps=[s['heap']for s in samples if s.get('heap')];resource=f'Initial observed load: {stability["initialLoadMs"]}ms.12realzonecycles and60actualdialogues;{len(samples)}resource snapshots. Observed JS heap range{min(heaps):,}–{max(heaps):,}bytes; this is JS heap only.'
else:resource='Final stability measurement pending.'
put('PERFORMANCE.md',f'''# NPC performance and memory

{resource}

[Long-session raw observations](stability.json) · [loading/cadence/tour observations](performance-observations.json) · [all-region gameplay traces](gameplay/actual-gameplay.json) · [cross-zone trace](cross-zone-actual.json).

## Bounded ownership

All14definitions/state records stay available; relevant home zones activate only up to4nearest NPCs. A talking actor is prioritized within that same cap. At most4native NPC textures and2concurrent loads; no duplicate IDs/keys. Each768×1456RGBA atlas estimates4,472,832bytes;4resident atlases estimate17,891,328bytes per texture owner. Browser-decoded image and GPU ownership are separate and must not be summed as measured totalGPU memory. Fourteen eager atlases would estimate62,619,648bytes,which the runtime does not preload.

Camera culling hides offscreen actors/shadows. Visible simulation ticks around50ms; offscreen active simulation is coarser250ms. Inactive zones freeze models; no full-world NPC pathfinding runs per frame. Bounded histories,retry/backoff,request cancellation and shutdown cleanup prevent repeated entry creating orphan actors. The source asset pool shares one cache across residents and never removes player/Studio/world keys. Dialog previews reuse loaded native atlases without another portrait decode.

The world’s existing64MiB chunk budget and character/composite cache policies remain unchanged. NPC estimates are separate,not a new claim about total browser/GPU memory.

## Measurement limits

Actual environment: systemChromium,headless desktop,Canvas; shared cloud host with possible concurrent QA/encoding. Frame/update intervals and browser RAF callback cadence are reported as observations,not certified presentation FPS. JS heap fluctuates with garbage collection; bounded counts and one extended session do not prove indefinite leak freedom.

Software SwiftShader WebGL uploads/rendering passed native readback for2residents. This is not hardware FPS,GPU-memory,thermal or Android/iPhone certification. Browser landscape667×375/844×390 validates functional layout/input only. Physical Android Chrome,iPhone Safari,notch hardware and sustained device performance: NOT TESTED.

ScenicTour is separately checked to return to the exact original player position,with NPC simulation suspended appropriately. Historical renderer/performance/motion warnings remain recorded in earlier reports and are not erased by Phase2C approval.
''')
put('QA.md',f'''# Phase3A QA

Current full final regression: **{e2e}**. Final report counters: `{json.dumps(stats,ensure_ascii=False)}`. Do not treat a running validation as PASS. Human artistic/linguistic acceptance remains pending.

| Area | Status | Evidence / scope |
|---|---|---|
| Accepted Phase2C pre-implementation baseline |PASS|116unit/53E2E,all required commands;baseline-logs |
| Typecheck/assets/lint/format |See final logs|npm run typecheck/assets:check/lint/format:check |
| Unit |PASS recorded|131tests including15NPC cases; no skips |
| Full E2E |{e2e}|60tests: original53 plus7NPC/cross-zone/re-entry cases |
| Build/portable build |See final logs|Actual existing Phaser4.2.1 bootstrap |
| NPC source art/animation |PASS technical|14identities/7zones/1456cells/448walkframes;8distinct/direction;native raster stance≤1px |
| Pilot before expansion |PASS technical|4actual contexts,20native readbacks,realinteraction/4directions |
| Final native actual renders |PASS technical|84captures,0unexplained opaque-pixel mismatch |
| Canonical navigation/clearances |PASS scope|14routes/approaches;criticaldoors/bridges/docks/plotsclear |
| Actual all14 approaches/dialogue/return |PASS scope|Original controls in canonical scene;not graybox |
| Cross-zone exploration |PASS scope|One uninterrupted mainland→northern Jeju bridgeA→orchard→house traversal |
| Re-entry/dialogue stability |PASS observed|12realcycles/60dialogues,reload,oneplayer,boundedNPCownership |
| Real visited/progress preservation |PASS scope|Actual palace discovery→NPCdialogue→reload;external learning account NOT integrated |
| Mobile landscape browser |PASS functional|667×375/844×390,Korean/Vietnamese,44px controls,joystick return |
| SoftwareWebGL |PASS smoke|2actual native readbacks,nearest;not hardware performance |
| World/characters/cosmetics/Studio |PASS hashes|6382frozenfiles;scene outside6additive hooks byte-identical |
| Independent ZIP |PENDING until package proof|CRC/SHA,extracted runtime and actual input test required |
| NPC artistic/linguistic acceptance |PENDING HUMAN|No automatic art approval |
| Physical Android/iPhone/hardwareGPU/thermal |NOT TESTED|No unsupported device PASS |
| Historical technical/motion warnings |WARN retained|Earlier approved-baseline reports remain untouched |

The first expanded full suite had59PASS/1FAIL in the new cross-zone QA harness. The path hugged original collision boundaries and used insufficient control alignment. The harness now uses the exact existing walking-contact offsets,clearance-weighted verified paths and original analog fine alignment. No collision/scenery/speed override fixed the test. Subsequent full regression and actual traversal are recorded separately; tests were not skipped or removed.

Final visual inspection also corrected two coastal NPC standing positions onto existing paved public surfaces. All14actual native captures/navigation checks were regenerated after that adjustment. Scoped dialogue classes removed inherited HUD pointer interference; safe-area insets prevent asymmetric-notch positioning errors. Physical notch/device acceptance remains untested.

[Source QA](source-qa.json) · [navigation](navigation-qa.json) · [native readbacks](gameplay/native-pixel-qa.json) · [stability](stability.json) · [extra/mobile/WebGL/realvisited](extra-evidence.json) · [protected audit](protected-audit.json) · [device workflow](DEVICE_REVIEW.md).

No farming/shops/crafting/inventory/rewards/quizzes/economy/account synchronization,paid AI/image APIs,Phase3B,main merge or deployment. Existing unrelated world planning/performance issues are retained,not silently repaired or certified by this NPC phase.
''')
print('Required9 Phase3A documents generated; finalE2E',e2e)
