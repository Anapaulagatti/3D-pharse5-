# CODEX MASTER PROMPT V2 — KOREAN PIXEL TOWN
# COMPLETE REMAINING GAME ROADMAP / 7 DELIVERY WORKSTREAMS / GATES 0–6
# Owner requested 2026-11-04. This is a single autonomous execution brief for a review candidate,
# NOT a waiver of separate approval gates for production, real-user data, multiplayer or advertising.

================================================================================
00. NHIỆM VỤ / MỤC TIÊU CUỐI
================================================================================
Bạn là Codex đảm nhiệm Lead Game Engineer, Phaser Programmer, Pixel Art Pipeline Engineer,
Gameplay/Economy Designer, Learning UX Engineer, QA Automation và Release Engineer cho
Korean Arena — Pixel Town trong dự án game độc lập.

**Không chỉ viết kế hoạch. Hãy kiểm tra trạng thái thật, sửa mã, tạo asset hợp pháp, chạy test,
đóng gói, tạo checkpoint và giao một candidate có thể chơi để chủ dự án nghiệm thu.**

Chủ dự án đi công tác khoảng hai ngày. Trong lần thực thi này, tiếp tục được nhiều workstream
liên tiếp mà không dừng để hỏi các chi tiết thiết kế nhỏ khi có thể suy ra từ bản build/roadmap.
Tuy nhiên KHÔNG tự diễn giải việc chủ dự án đi vắng thành quyền công khai, merge production,
truy cập/ghi dữ liệu thật, bật quảng cáo hay tự mở các dịch vụ trả phí.

Kết quả mong muốn là GAME playable trọn vòng lặp, không phải một danh sách tính năng hoặc
HTML dashboard phủ lên ảnh nền; đồng thời hoàn tất thiết kế/kiểm chứng phần còn lại trong
phạm vi được phép, ghi minh bạch các mục còn chờ chủ dự án phê duyệt.

TARGET REVIEW PAGE (không tự động overwrite khi chưa có approval exact-artifact):
  https://anapaulagatti.github.io/3D-pharse5-review/play/

GAME SOURCE REPOSITORY:
  https://github.com/Anapaulagatti/3D-pharse5-
REVIEW REPOSITORY:
  https://github.com/Anapaulagatti/3D-pharse5-review

KHÔNG NHẦM GAME REPO VỚI WEBSITE HỌC CHÍNH:
  Website TiengHanSoEasy / Boydeop/TiengHanSoEesy là dự án riêng;
  không sửa backend website, curriculum/FSRS/XP hay database người học trong prompt này.

================================================================================
01. RÀ SOÁT ROADMAP VÀ TRẠNG THÁI CHÍNH XÁC — BẮT BUỘC ĐẦU TIÊN
================================================================================
A. Trước khi sửa bất kỳ file nào:
  1. Xác định HEAD, commit, branch, dirty working tree, upstream, các PR mở,
     trạng thái Actions, URL Pages thực tế.
  2. Đọc AGENTS.md, docs/current/MISSION.md, docs/PRODUCT_ROADMAP.md,
     README.md, PIXEL_ART_BIBLE.md, STUDIO_TASKS.md, STUDIO_PROGRESS.md,
     STUDIO_DECISIONS.md, STUDIO_ASSETS.md, docs/RECOVERY.md và các tài liệu
     phê duyệt mới nhất; tìm cả docs, các nhánh/checkpoint liên quan 3B-D.
  3. Nếu có master roadmap chuẩn được đặt ở vị trí khác, tìm và đọc bản đó trước.
  4. So sánh trạng thái repo với owner feedback, không lấy README cũ làm bằng chứng
     rằng những tính năng đã triển khai gần đây chưa tồn tại.
  5. Lập ma trận: ORIGINAL GATE 0–6 vs GAME PHASE 1/1B/2A/2B/2C/3A/3B-A/B/C/D/E...
     vs trạng thái DONE / PARTIAL / NOT STARTED / BLOCKED / NOT TESTED.
  6. Không tự bịa tên các phase chưa có định nghĩa chính thức. Nếu chênh lệch
     giữa roadmap lịch sử và các phase mới, ghi rõ “source of truth” / override
     theo ngày và giữ bản đồ tương ứng.

B. Tài liệu xác minh đã biết (dùng làm điểm khởi đầu, không phải chân lý HEAD):
  - docs/PRODUCT_ROADMAP.md liệt kê 7 gate từ **Gate 0 tới Gate 6**:
      Gate 0: audit/recovery,
      Gate 1: kỹ thuật/pipeline,
      Gate 2: art/avatar/world,
      Gate 3: first delivery + Sign Repair + Courier Rush,
      Gate 4: outfit inventory/local social → backend an toàn có duyệt riêng,
      Gate 5: co-op/PvP phù hợp trình độ/advanced learning + ad adapter mặc định tắt,
      Gate 6: device/performance/accessibility/security/publication.
  - Lộ trình vận hành gần đây dùng Phase 1B, 2A/2B/2C, 3A và 3B-A/B/C/D.
  - Phase 3B-D đã có candidate world-interaction, farming, shop/inventory,
    Town Coins, quest và cleanup; user đang review chất lượng.
  - CÁC ĐIỂM ĐÃ CHỐT: thế giới Gate 1 style; nhà ga Hanbit dựng mới; hai cầu Jeju;
    cung điện / hanok đã sửa; 12 playable characters; 26 NPC; gameplay trực tiếp
    thế giới Phaser thay cho overlay hành động lớn.
  - Hiện ảnh owner review thấy **6 luống** đã có texture đất xới; còn tình trạng
    mảng nền cũ lộ ra, plot chưa phong phú, HUD chưa đủ, nhiều interior chưa vào,
    và lối đi/hitbox ở vài nơi vẫn khó.

C. Không nhận định “7 phase đều đã được quyết định cụ thể” nếu thực tế chỉ có
7 Gate 0–6. 7 nhóm thực thi phía dưới là *workstreams thực hiện* để tránh bỏ sót,
không ghi đè tên lịch sử của bất kỳ phase nào.

================================================================================
02. GIỚI HẠN AN TOÀN / BẢN QUYỀN / CHI PHÍ / NGHIỆM THU
================================================================================
  - GIỮ NGUYÊN phiên bản art/world canonical đã duyệt. Không tái tạo map tổng.
  - Giữ các source sprite được duyệt (Juni và 11 nhân vật khác), 26 NPC, atlas,
    animation/four-way, 24 cosmetics hiện được báo cáo trong review.
  - Không sử dụng, tái sinh hoặc copy-paste map cũ đã bị loại. Không xóa history Git.
  - Không dùng art/nhân vật chính thức Hay Day hoặc Pixels. Chỉ học cơ chế gameplay.
  - Tài sản phải là artwork gốc hoặc có bằng chứng license phù hợp sử dụng thương mại.
    Đổi tên nhân vật nổi tiếng không tự động xóa rủi ro likeness/trademark/trade dress.
    Mọi yếu tố chưa clear: giữ local review với nhãn cảnh báo, loại khỏi public artifact,
    hoặc thay bằng nhân vật/thiết kế độc lập được duyệt.
  - Không dùng API/tài sản/mô hình trả phí, không tạo billing/Cloudflare R2/Supabase
    projects mới, không bật Ads SDK, không cấp quyền account, không tự mua dịch vụ.
  - Không thao tác cơ sở dữ liệu production; không ảnh hưởng học viên thật.
  - Không gọi game local prototype là multiplayer thật, không giả lập người chơi là thật.
  - Không load test production, không phát hành commercial khi chưa được duyệt.
  - Phần tiếng Hàn mới do AI tạo: trạng thái PENDING_HUMAN_REVIEW cho tới khi có
    chuyên gia tiếng Hàn xác thực. Không mượn tài liệu/exam có bản quyền để sao chép.
  - Dùng English/Vietnamese dialog fallback hợp lý, hỗ trợ text accessibility.
  - Ghi PASS/FAIL/BLOCKED/NOT TESTED có evidence, KHÔNG làm PASS giả.
  - Không yêu cầu owner online giữa lúc làm để duyệt tiểu tiết; chỉ dừng tại
    các approval gate hợp pháp/kỹ thuật không thể bỏ qua.

================================================================================
03. SEVEN EXECUTION WORKSTREAMS — THỰC HIỆN LIỀN MẠCH THEO THỨ TỰ
================================================================================

WORKSTREAM 1 — BASELINE, CHECKPOINT, REGRESSION AND ORIGINAL ART PIPELINE
----------------------------------------------------------------------------
1.1 Xác định artifact review hiện tại và version đang chạy trên URL Pages.
    Không suy ra từ screenshot rằng đã deploy đúng commit.
1.2 Tạo checkpoint trước can thiệp; ghi Git SHA, asset manifest, hash các atlas,
    và rollback notes. Không force-push; tách source candidate khỏi production.
1.3 Điều tra hai trạng thái plot của screenshot user: bản trước có ô crop mặc định,
    bản mới là đất xới. Xác định tầng bitmap tĩnh còn lộ phía dưới sprite/overlay.
1.4 Inspect Art Skill pipeline: docs/SPRITE_FORGE_USAGE.md và toolchain thực tế.
    Kiểm tra bộ kỹ năng phù hợp:
      generate2dmap, generate2dsprite, codeart2d, video2dsprite, generate2dmedia.
    Dùng skill thực sự khi hỗ trợ và có quyền truy cập; log invocation/commands/output;
    nếu không sẵn có, dùng deterministic authored native pixel art thay thế.
    KHÔNG claim “dùng skill” nếu chỉ đọc danh sách.
1.5 Thiết lập art constraints: scale/palette/outline/highlight/lighting/shadows,
    integer scaling, nearest-neighbor for sprites, registration/hitbox anchors.
    Không đổi phong cách painterly Gate1 đã chốt.
1.6 Audit các issue regressions trước: camera jerk/input diagonal, collisions,
    sprites bị cut, vật cản che chân, clipping/water/building seams.

Deliverables: baseline report, checkpoints, protected hashes, art source registry,
exact commands, rollback tested or marked not tested.

WORKSTREAM 2 — FARMING NATIVE TILE/SPRITE + RICH SEED PROGRESSION
----------------------------------------------------------------------------
2.1 Thiết kế lại **6 luống hiện tại** theo phong cách natural pixel farm:
    - Sáu luống vẫn ở đúng khu farm canonical; có thể mở rộng từng luống VỪA ĐỦ
      nếu tổng thể đẹp hơn, không phá lối đi hoặc cây/công trình được duyệt.
    - Xóa phần art crop cũ còn sót tại chính các ô trồng; không để dấu cũ
      lộ qua overlay và không tạo texture hình chữ nhật phẳng.
    - Mỗi luống có ô/cell hợp lý: tile đất, rìa đất, luống xới, shadow, decorative
      crop, soil moisture; không xóa toàn bộ base map để dựng lại.
    - Ground base không phải một ảnh động nguyên khối chồng map; từng plot/cell
      độc lập có hit area, world coordinates, local state và visual frames.
    - Transition giữa đất/lối đi/cỏ/hàng rào mượt, không seam, không texture blur.
2.2 Thực hiện finite state machine:
    LOCKED (nếu có) → EMPTY → TILLED → SOWN → SPROUT → EARLY_GROWTH
    → MID_GROWTH → MATURE/READY → HARVESTED → EMPTY/TILLED.
    Tưới nước là moisture state / cooldown, không làm mất crop stage.
    Lưu timestamps chống reload / tab-switch bypass; không thu hoạch trước giờ.
2.3 Mỗi hành động phải là Phaser in-world:
    Approach → hoe → select seed → sow → water → visibly grow → harvest.
    Art phải đổi có hình rõ qua mọi stage; tool animation, dust/water/harvest effect
    ngắn, âm thanh chỉ khi license/setting cho phép. Có reduced motion.
2.4 Nội dung hạt giống: **ít nhất 12 loài/mặt hàng trồng** nếu repo cho phép,
    tránh khoe một danh sách vô dụng; ví dụ radish, cabbage, green onion,
    carrot, rice, chili, sweet potato, soybean, pumpkin, cucumber, tomato,
    strawberry, flowers. Cân nhắc địa lý và tính phù hợp thẩm mỹ Hàn Quốc.
    Mỗi loại: id ổn định, tên VI/KO được review, icon riêng, sprite stage riêng
    hoặc variation có khác biệt nhận dạng, rarity/type, growth time, water policy,
    seed cost, sale value, quest unlock, source license.
    Không đủ nguồn art hợp pháp thì giảm số loài và báo PARTIAL, không chế bằng clone.
2.5 Unlock progression:
    - Start: 1–2 seed cơ bản.
    - Quest/challenge milestone/level unlock thêm theo thứ tự đã thiết kế.
    - Shop hiển thị khóa + điều kiện, không bán vật phẩm khóa trước.
    - Seed unlock phải theo account/local prototype profile không mất khi reload.
    - Tránh tình huống bí nhiệm vụ vì thiếu seed hoặc thiếu xu.
2.6 6 luống phải trồng song song độc lập; cắt/thu hoạch không đổi đồng loạt.
    Không nhận reward trùng khi double-click, refresh hoặc thao tác gần đồng thời.
2.7 Demo review cho phép tùy chọn tăng tốc growth **CHỈ TRONG REVIEW MODE**,
    có nhãn TEST SPEED; tiến độ thực không dùng timer demo nếu deploy công khai.
2.8 E2E 3 loại cây, crop unlock, repeated farming cycle, cross-scene persistence,
    reload, locked seed denial, insufficient inventory, harvest exactly once.

Deliverables: native crop atlas + provenance, exact before/after native crops gallery,
3-minute uninterrupted farming gameplay, plot-state schematic, test report.

WORKSTREAM 3 — REAL-GAME HUD / INVENTORY / CHARACTER & INTERACTION UX
----------------------------------------------------------------------------
3.1 Thay HUD website button style bằng sprite/icon UI game coherent:
    - Coin / wallet icon and Town Coins
    - Backpack/inventory icon
    - Quest journal / task icon
    - Hotbar seed / hoe / watering can / interaction
    - Contextual action hint (E / click / tap)
    - Optionally map, help, settings (sound, motion, control)
    - Feedback toasts for seed unlocked, +crop, +coin, quest progress.
3.2 HUD responsive desktop/tablet/mobile, không che world quá nhiều;
    keyboard focus, touch hit areas, safe-area, readable labels, contrast.
3.3 Inventory: grid/stack/quantity, category tabs (seeds, crops, tools, quest),
    selected tool, item tooltip, locked items clearly differentiated.
3.4 Journal: current quest plus clear chain/steps, NPC destination, short hints;
    no large modal required for ordinary gameplay. No remote instant-complete.
3.5 NPC talk UI: lightweight dialogue, choices, portrait optional only if licensed,
    forward/back/cancel, reopen, input lock/unlock. Respect collision and trigger range.
3.6 Player camera/movement: no one-frame snapping on WASD combinations,
    input smoothing vs physics consistent; no wall phasing. Root anchor checks.
3.7 Keep local UI route behavior safe; production learning website untouched.

Deliverables: native sprite HUD preview, screenshots for 3 sizes, E2E and accessibility checks.

WORKSTREAM 4 — ENTERABLE INTERIORS, SHOPS, TOOL MERCHANTS & SMALL QUESTS
----------------------------------------------------------------------------
4.1 Implement **at least 3 fully playable interiors**; target up to 5 if art/time
    allow and all access/collision tests pass. Candidate types:
    seed/farm tool shop, merchant grocery/market, bookstore/learning shop,
    delivery/harbor warehouse, community workshop.
    Choose actual buildings from canonical map; provide building registry keyed
    by real world coordinates. Do not invent door on inaccessible geometry.
4.2 Interior must be a real Phaser scene/map room with wall/floor/counter/NPC,
    proper lighting/tile art from authorized pipeline, entry/exit transitions,
    persistent player location, spawn safe distance; not a JPG interior with buttons.
4.3 Door triggers require proximity + E / tap, loading fallback, no teleport exploit.
    Exit leads to valid world position and restores camera/input; no spawn trap.
4.4 Seed shop: browse locked/unlocked, price, qty, buy, stock error.
    Merchant: sell crops, NPC deliveries, receipt and atomic inventory update.
    Bookstore: optional approved learning/review minigame hook, not copying textbook.
    Workshop: basic equipment/decoration unlock or meaningful in-world task.
4.5 Introduce 2–3 new interactions per interior, limited to scope that makes
    gameplay loop richer, not hundreds of filler buttons.
4.6 NPC schedule/routine respected. If an NPC is both outdoors and indoors,
    no duplication of actor / conflicting dialogue state.
4.7 Test entry/exit all interiors, open/close shop, purchase, sell, restore scene,
    NPC interaction, accessibility, camera and UI states.

Deliverables: interior registry/map list, native screenshots, walkthrough video,
shop test records.

WORKSTREAM 5 — QUEST, ECONOMY, KOREAN LEARNING & SINGLE-PLAYER COMPLETENESS
----------------------------------------------------------------------------
5.1 Connect physical loop:
    movement → explore → meet NPC → accept quest → real-world action
    → answer appropriate Korean question/review → grant base reward once
    → buy/unlock → continue playing.
5.2 Quest chains (at least 8 interconnected steps / 15–30-minute review play):
    tutorial movement; seed first; till/sow/water; harvest; delivery;
    sell crop; unlock new seed; enter shop; visit orchard/Jeju; one follow-on task.
    Add alternate NPC/optional side tasks if stable.
5.3 For quest completion, ensure teaching question does not become spam:
    - user instruction previously asks correct answer before completing eligible quest;
    - wrong answer substitutes another equivalent difficulty question,
      without farming penalty/reward duplication; preserve learning dignity.
    - reconcile with repo roadmap “manipulation before quiz”: Sign Repair and
      Courier Rush are mini-games involving meaningful action, not a quiz-only wall.
    - No arbitrary quest grind gating free education access.
5.4 Implement Gate3 First Delivery vertical slice if missing:
    lost fragments → repair syllable sign with draggable/keyboard tile pieces
    → locate address → Courier Rush → deliver → visible area restoration.
    Small story closure and reward; optional reduced/no timer assist.
5.5 Korean learning provenance: each item ID, Korean NFC, VI explanation,
    expected accepted answers, grade/topic, rights/source record,
    review flag PENDING_HUMAN_REVIEW until qualified human signs.
    Do not assert official TOPIK/EPS exam equivalence. Do not copy exam banks.
5.6 Economy:
    - Town Coins ≠ FSRS/mastery/XP formal exam scores.
    - Economy table seed cost, sell reward, quest reward, unlock cost if any,
      sustainable early game, anti-softlock grants and no double spending.
    - No cash/nft/token, paid boosts, unfair competitive advantage.
    - Purchases & reward transactions idempotent; low-resource and race cases.
5.7 Persistent save schema versioning and migrations, local demo storage (clearly
    marked), back up before schema evolution, rollback, corrupt-save recovery.
    Do not sync Supabase without separate explicit authorization.
5.8 Localization VI primary, Korean review pending, English optional;
    accessibility instructions legible and navigable.

Deliverables: playable end-to-end quest flow, economy/unlock balancing spreadsheet
or JSON tables, reviewed-content registry, QA evidence.

WORKSTREAM 6 — SOCIAL, ADVANCED GAMEPLAY, FUTURE ADS: DESIGN/ISOLATED SAFE PROTOTYPES
----------------------------------------------------------------------------
6.1 Read original roadmap Gate4/5 before coding. The user asks to handle
    remaining scope, but real multiplayer and monetization REQUIRE distinct approval.
6.2 Implement **local-only** safe interfaces/prototypes when feasible:
    - Local cosmetic wardrobe / profile demo / emote / social proof demo
      explicitly labeled NOT LIVE PLAYERS.
    - Co-op quest architecture or mocked deterministic 2-player session
      behind disabled feature flag; no fake public online counts.
    - PvP prototype only if separate modes available; proficiency-fair rules,
      no pay-to-win; NO real matchmaking/ranked service without approval.
    - Advanced learning hooks, practice history adapter contract, minimal
      UI; do not write real website/production records.
6.3 Backend readiness design (do not provision):
    ProfileProgressAdapter, RoomAdapter, game server-authoritative state;
    authenticated sessions, idempotent reward IDs, movement validation,
    event bounds, rate limits, abuse moderation, reporting/mute/block.
    Document estimated connection/CPU/storage budgets and kill switches.
    Gate 4/5 live multiplayer remains BLOCKED_UNTIL_OWNER_APPROVAL.
6.4 Ads: only **RewardedAdProvider DISABLED adapter** by default, no SDK,
    no network ad call, no runtime real ads, no paid provider.
    Document opt-in offer for future optional cosmetic-only x2 bonuses;
    grant base quest reward first, then optional separately approved bonus.
    No multiplication of formal mastery/XP/TOPIK or essential learning items.
    Real ad provider, consent/privacy, anti-fraud, policy review, receipts
    and server verification require distinct owner approval.
6.5 Never convert this local game into public multiplayer while user away.
6.6 Web-game integration is DEFERRED by owner decision. At this stage only document
    safe data contracts for later learning progress/FSRS sync; no access to
    TiengHanSoEasy production users, database, curriculum or live feature flags.

Deliverables: architecture docs, interface tests, disabled flags verified,
clear BLOCKED/PENDING/NOT IMPLEMENTED status where appropriate.

WORKSTREAM 7 — FULL QA, PERFORMANCE, RIGHTS, RELEASE CANDIDATE, HANDOFF
----------------------------------------------------------------------------
7.1 Run clean clone on candidate branch (use actual project scripts):
    npm ci, assets:check, typecheck, lint, format:check, unit, build, Playwright E2E.
    Avoid regenerating locked native art during setup.
7.2 Real browser route coverage:
    - world, all 6 plots, minimum 3 crop types and 2 unlock chains;
    - NPC talk and quest state, shop buy/sell, entry/exit all interiors;
    - collision narrow routes incl. western hanok north–south paved path,
      intersection west of hanok, farm/market, station plaza, two Jeju bridges;
    - WASD diagonal/start/stop/turn, keyboard + mouse + touch emulation;
    - persist across reload, idempotency and anti-tamper-negative tests;
    - missing asset, network, console, camera, hitboxes, NPC overlap;
    - backpack / quest / coin HUD and accessibility/reduced-motion.
7.3 Device: emulator desktop/mobile (DPR 1/2/3 where available) vs real
    Android/iPhone clearly NOT TESTED unless physically performed.
    Measure actual CPU/frame timing/FPS from tested hardware; no fake 60 FPS guarantee.
7.4 Commercial rights and privacy:
    precise asset manifest: original/licensed/unknown/rejected;
    26 NPC and character likeness review; sound/fonts/visuals;
    Korean educational content human-review gate; permission for public review
    only for allowed assets. Redesign or exclude disputed source art, not merely rename.
7.5 Cleanup actual tracked obsolete map files ONLY after dependency audit
    + reproducible restore. Do not rewrite Git history or remove recovery tags.
    Keep current approved world and high-quality station; distinguish archived
    rejected worlds so later prompts never accidentally re-import them.
7.6 Release candidate and backup:
    exact SHA / code diff / artifacts / ZIP verified offline and over HTTP,
    manifest SHA256, protections, rollback SHA, no hidden production data.
7.7 Github Pages review:
    - Inspect current published version and exact approval manifest.
    - If new public artifact requires owner approval / GitHub protected
      environment review, prepare exact approval packet and STOP at gate;
      do not repurpose old approval for a new artifact.
    - If release procedure and exact artifact already approved, deploy to
      current Pages review repo only, verify live HTTPS /play/ and cache-bust.
    - Do NOT touch separate production website, game production, paid services.
7.8 Archive one consolidated review package (not hundreds of loose screenshots):
    - START_HERE.md with playable link/offline ZIP startup
    - WORLD + FARMING + INTERIOR + QUEST short gameplay clip
    - before/after asset comparison
    - QA MATRIX per route and phase/gate
    - licenses, Korean review pending list
    - open issues, blockers and minimal rollback steps.

================================================================================
04. EXACT ACCEPTANCE CRITERIA — OWNER'S NON-NEGOTIABLE CHECKLIST
================================================================================
A01 — Six farm plots: every old crop-image remnant removed, beautiful native pixel art,
       visually integrated landscape, independent cells and no obvious background patch.
A02 — Planting: actual physical character approach/interaction; visible soil preparation,
       seed, watering, at least 3 visibly distinct growth sizes, mature and harvest.
A03 — Rich seeds: 12 target varieties (or transparently fewer if licensing/art blocker),
       icons/stages/prices, at least 2 quest-based unlocks, shop lock enforcement.
A04 — Visual game HUD: functional pixel icons bag, quest, Town Coins, hotbar;
       resize/focus/touch, no giant dashboard-driven gameplay.
A05 — Interiors: at least 3 functioning enterable mapped buildings with indoor
       art/NPC/transactions/objectives, safe enter/exit and persistence.
A06 — Quest game loop: farm→deliver→shop→unlock, Korean prompt at appropriate
       stage and correct/incorrect/retry handling, reward exactly once.
A07 — Collision: physically traverse western hanok narrow path (including
       mouth/intersection), farm/market, important district links, station and
       both Jeju bridges without tiny one-pixel alignment requirements.
A08 — Legacy cleanup: no active ref to rejected map; tracked deletions safe,
       dependency graph and rollback preserved.
A09 — Regression: 12 players + 26 NPC + approved scenery + art locks preserved.
A10 — Learning & legal: no unreviewed Korean falsely PASS, no copyrighted
       likeness/asset silently shipped publicly.
A11 — Advanced/social/ads: disabled defaults and explicit approval gates,
       no live user data / paid resources created.
A12 — Delivery: exact tested candidate + ZIP + playable URL if authorized,
       SHA256 manifest + QA + screenshots/video + full rollback.

Mark each PASS / FAIL / PARTIAL / BLOCKED / NOT TESTED with links to source evidence.
Automatic QA alone cannot override poor visual experience. The owner is final
art/playability reviewer on return.

================================================================================
05. HOW TO WORK WITHOUT FRAGMENTING THE PROJECT
================================================================================
- Work in the current verified source branch or isolated feature branch;
  do not guess current branch names from old examples.
- Finish workstreams 1→7 sequentially, with checkpoints between;
  dependent technical steps can be reordered if you document why.
- For large scopes, prioritize a coherent vertical slice playable end-to-end.
- Never mark unfinished work complete merely because time/budget runs out.
- Avoid requiring the owner to repeatedly reply while away; choose small
  reversible decisions and register them in `DECISIONS_PENDING.md`.
- Only ask approval at an unavoidable gate: changed public artifact,
  live backend, multiplayer, ads, new billable service, privacy/legal publication,
  real-user writing. Continue unrelated safe local work where feasible.
- Do not produce a promise to run for two days in the background; deliver
  everything accomplished in the active execution context with honest blockers.
- Do not announce future task execution as completed.

================================================================================
06. OUTPUT CONTRACT — SINGLE CONSOLIDATED HANDOFF
================================================================================
Return in Vietnamese, once the available execution is complete:

1. **Status:** READY_FOR_OWNER_REVIEW / PENDING_OWNER_APPROVAL / BLOCKED.
2. **Roadmap reconciliation:** actual seven Gates (0–6) + current 3B subphases,
   state of each, and which source is authoritative.
3. **Change log** by seven workstreams with evidence, not just marketing phrases.
4. **Gameplay:** what the player can physically do in real Phaser world.
5. **Farming:** exact crops/seeds, growth stages, unlock chain and plot mechanics.
6. **HUD & interiors:** playable building list, transactions and quest states.
7. **Collision:** corrected world positions, walkable clearance and traversal evidence.
8. **Quality:** PASS/FAIL/PARTIAL/BLOCKED/NOT TESTED and browser/device details.
9. **Rights/learning:** licenses, NPC likeness status, human Korean review gates.
10. **Source:** branch, verified commit, build artifact, SHA256 manifest,
    protected files hashes, regression test counts and failed tests.
11. **Review:** URL `/play/` (if published and verified), ZIP local HTTP launcher,
    actual screenshots/video, approval link if Pages is waiting for review.
12. **Recovery:** precise rollback procedure and prior approved checkpoint.
13. **Pending decisions:** brief owner-only checklist after return (no more than
    essential approvals), separated from work safely completed already.

FINISH CONDITION:
- The owner sees a polished native pixel town with growing farm plots,
  enough seeds unlocked through actual gameplay, game-like icons, NPC quest
  chains and meaningful enterable buildings, without walking hitbox traps;
- The owner can test the correct build in one place;
- The game, protected assets, production website and real student data remain safe;
- No public/commercial/social/ads approval is fabricated.

START NOW. First verify current HEAD and reconcile docs/PRODUCT_ROADMAP.md
with the actual latest Phase 3B-D checkpoint. Then execute WORKSTREAM 1→7.