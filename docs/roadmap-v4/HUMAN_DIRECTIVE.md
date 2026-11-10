# CODEX MASTER PROMPT V4 — KOREAN PIXEL TOWN: JEJU PATH, HANGUL, INTERWOVEN QUESTS, DISTINCT INTERIORS
# COMPLETE REMAINING GAME ROADMAP / 7 DELIVERY WORKSTREAMS / GATES 0–6
# Owner updated 2026-11-10; supersedes earlier game V2/V3 prompts. Originally requested 2026-11-04. This is a single autonomous execution brief for a review candidate,
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
02B. OWNER REVIEW 10/11/2026 — P0 OVERRIDES, KHÔNG CẦN GỬI ẢNH
================================================================================
QUAN TRỌNG: Chỉ đạo này MỚI HƠN tất cả nhận xét “V2 đã khá ổn” trước đó.
Ảnh chủ dự án gửi trong chat là bằng chứng cho người soạn prompt, KHÔNG phải
tệp mà Codex được yêu cầu phải nhận. Vì vậy Codex PHẢI tự tìm đúng world
tile, collision polygon và scene/asset bằng mã nguồn, video replay, tọa độ
runtime và reference landmarks. Không được dừng vì “thiếu ảnh khoanh đỏ”.

NHỮNG LỖI MỚI OWNER KHẲNG ĐỊNH CÒN TỒN TẠI:
  P0-1. Một phần luống farm vẫn lộ nội dung/texture map cũ bên dưới.
  P0-2. HUD có nút xu/túi đồ/nhiệm vụ nhưng chưa được tích hợp tự nhiên,
        các chức năng còn mang cảm giác panel website tách khỏi game.
  P0-3. Người chơi chưa thể thực sự vào công trình từ cửa trong world;
        khẳng định “đã có 3 interior” trước đó không đủ chứng cứ.
  P0-4. Shop, nhiệm vụ và NPC trong nội thất chưa có bằng chứng tương tác
        end-to-end tại đúng bản Pages đang chạy.
  P0-5. TUYẾN ĐƯỜNG JEJU MỚI DO OWNER ĐÁNH DẤU MÀU ĐỎ vẫn đi không được.
  P0-6. Các câu hỏi tiếng Hàn hiện đang dùng **đáp án bằng tiếng Việt**;
        owner muốn người chơi PHẢI đáp bằng tiếng Hàn cho những câu hỏi
        đánh giá khả năng tiếng Hàn.
  P0-7. Nhiệm vụ cần NHIỀU TUYẾN ĐAN CHÉO nhau theo kiểu RPG MMORPG
        (cảm hứng cấu trúc nhiệm vụ như Võ Lâm Chi Mộng), không phải
        một chuỗi đơn tuyến, tuần tự hoặc lặp lại quá máy móc.
  P0-8. MỖI CÔNG TRÌNH VÀO ĐƯỢC phải có mỹ thuật nội thất riêng thật sự,
        phù hợp kiến trúc và công dụng; không thể dùng một phòng mẫu
        đổi biển hiệu/đổi màu cho tất cả.

LUẬT ƯU TIÊN:
- Các nhận xét P0-1...P0-8 có độ ưu tiên cao hơn kết quả unit test, báo cáo
  Codex trước đó hoặc lời nhận định chỉ dựa trên screenshot.
- Không được báo “READY” nếu những lỗi P0 này còn mở mà không báo rõ PARTIAL.
- Không sửa ngoài phạm vi tự nhiên của tuyến/map/giao diện được giao.
- Nếu source repo main cũ không khớp candidate đang chơi, PHẢI tìm đúng SHA,
  artifact, branch, manifest ở repo nguồn/review, không chép kết luận từ README.

================================================================================
02C. P0-5 — SỬA ĐÚNG TUYẾN ĐƯỜNG ĐỎ Ở JEJU, KHÔNG CẦN ẢNH
================================================================================
MÔ TẢ VỊ TRÍ THEO LANDMARK (đủ để tự tìm trong runtime):
- Bản review hiện tại hiển thị một cầu đá lớn nối đất liền tới đảo/khu Jeju.
- Tại ĐẦU CẦU PHÍA ĐẢO, nhân vật đi trên đoạn đường lát đá nằm ngang.
- Từ đây có nút giao nối vào đường lát đá chạy xuôi về Đông Nam/nam xuống
  bên phải một căn nhà hanok lớn mái ngói đen ở phía dưới khung hình.
- Ở phía Đông đường có khu vườn cây có quả/quýt, tường đá thấp, đèn/lan can;
  phía Tây có sườn mái/ngôi nhà hanok, bên trên là cảnh đá biển và mỏm đá.
- Tuyến owner vẽ đỏ bắt đầu ở đoạn cầu/phía ngay sau cầu, chạy ngang qua
  nút giao lát đá rồi RẼ XUÔI theo đường cong dọc mép hanok/vườn về phía
  trước nhà và tiếp đến khu vực lối vào. Hiện nhìn như đường đi nhưng
  collider/pathing chặn hoặc nhân vật không qua được liên tục.
- Đây KHÔNG PHẢI lối dọc phía tây hanok trên đất liền đã từng sửa trước đó;
  cũng KHÔNG phải cầu Jeju bị lệch hình ảnh ở các phiên bản cũ. Lỗi này mới,
  nằm trên bản Pages review mới, phía ĐÔNG đầu cầu và đi xuống mép hanok Jeju.

YÊU CẦU KỸ THUẬT:
1. Chạy game/capture tọa độ runtime tại 4–6 waypoint từ đầu cầu tới đoạn
   cong quanh mái hanok và gần cửa. Ghi điểm world (x,y) do engine đo được;
   KHÔNG tự bịa số pixel từ screenshot.
2. Dùng debug collision overlay, player feet collider, world bounds, static
   layers, polygon collider, navmesh / A* (nếu có), depth/occluder mask.
   Xác định chính xác blocker: tường đá, mái/footprint hanok, planter, đường
   lát đá, điểm nối path, hitbox NPC, bridge transition hay wrong collision layer.
3. Tạo một walkable corridor liên tục giữa waypoint, nới clearance vừa đủ
   cho nhân vật và animation 4 hướng; không tạo mép đi cắt qua nước,
   xuyên tường nhà, lan can đá, cây, hàng rào hoặc cliff.
4. Nếu mỹ thuật đường cong quá hẹp so với collider, điều chỉnh cục bộ
   path/layer/props xung quanh (được phép dịch một vài viên đá/cây decor).
   Không đập lại map Jeju hay ảnh nhà hanok/cầu đã chốt.
5. Test nhân vật đi cả 2 chiều: cầu→hanok, hanok→cầu; đứng/yên/rẽ tại
   góc; giữ W+D/S+D và chuyển hướng giữa đường; đi bộ/chạy; đường không
   có snap camera; NPC đi qua không gây bottleneck vô lý.
6. Tự lưu video liên tục có collision overlay ở bản debug và video không
   overlay ở bản game; in tọa độ waypoint thực, collider đã sửa và QA.
7. Nếu mỏm đá không nên cho đi qua về mặt mỹ thuật, thay đổi cục bộ lối
   đi NHƯNG phải giữ khả năng nối cầu→cửa hanok hợp lý. Không được gọi
   lỗi “có chủ ý” chỉ vì cần tránh chỉnh collider.

DONE KHI: Có thể dùng WASD/arrow thực sự đi liền mạch qua toàn tuyến
không cheat teleport, không noclip và không mouse warping.
Bằng chứng tối thiểu: traversal demo cả 2 chiều + ảnh overlay collision
và PASS đường đi trong E2E kiểm thử trực tiếp.

================================================================================
02D. P0-6 — CÂU HỎI PHẢI TRẢ LỜI BẰNG TIẾNG HÀN (HANGUL)
================================================================================
Không được nhầm “câu hỏi bằng tiếng Hàn” với “đáp án Việt”.
Điểm owner yêu cầu: BÀI KIỂM TRA NĂNG LỰC TIẾNG HÀN PHẢI YÊU CẦU
người chơi chọn/nhập ĐÁP ÁN TIẾNG HÀN.

QUY TẮC NỘI DUNG:
1. Khi đang chơi vòng nhiệm vụ đánh giá tiếng Hàn, phương án trả lời
   đúng/sai hiển thị bằng HANGUL và/hoặc cách diễn đạt Hàn phù hợp.
   Ví dụ minh họa (chỉ để hiểu định dạng, không là ngân hàng QA đã duyệt):
     NPC: “사과” nghĩa là gì? → Nếu muốn kiểm tra Hàn→Việt thì đó là
     bài dịch nghĩa, KHÔNG được giả làm bài trả lời bằng tiếng Hàn.
     Bài theo yêu cầu owner: “Quả táo tiếng Hàn là gì?”
       A. 사과    B. 바나나    C. 물    D. 집
     Hoặc “Bạn muốn mua một quả táo, chọn câu nói đúng”:
       A. 사과 하나 주세요.   B. 학교에 가요.   C. 감사합니다.  D. 잘 자요.
   Thay các câu trộn tiếng Việt ở nút chọn bằng lựa chọn Hangul.
2. Hướng dẫn/đề bài tiếng Việt vẫn có thể dùng làm scaffolding cho
   người mới. Nút TRẢ LỜI, đáp án/kết quả đánh giá phải cho người
   chơi thật sự nhận diện/sử dụng tiếng Hàn.
3. Bổ sung lựa chọn typing Hangul khi phù hợp, chấp nhận NFC/NFD
   chuẩn hóa Unicode, xử lý whitespace/dấu câu được phép, không chấm
   sai vì lỗi font/IME. Trên mobile hiển thị bàn phím phù hợp hoặc
   mode chọn Hangul (không bắt buộc gõ từ đầu).
4. Ngân hàng câu hỏi phù hợp trình độ: mới học bảng chữ cái, cơ bản,
   trung cấp phù hợp progress; tránh câu trả lời mơ hồ, hai đáp án cùng đúng.
5. Sai: giải thích ngắn gọn, gợi ý phù hợp, tạo câu tương đương độ khó
   hoặc retry có giới hạn chống lặp, không trừ seed/xu/XP chính thức.
   Đúng: cho qua bước, tiến quest và reward đúng MỘT LẦN.
6. Không cho một nút “bỏ qua/hoàn thành” để lách điều kiện nhiệm vụ
   vốn được thiết kế có câu hỏi; nhưng có trợ năng, hint, luyện tập lại,
   không buộc khóa truy cập bài học miễn phí.
7. Tách chế độ “dịch Hàn→Việt” hợp lệ khỏi các nhiệm vụ owner muốn
   “trả lời bằng tiếng Hàn”; không được thay toàn bộ bài luyện dịch
   bất chấp mục tiêu sư phạm. Báo cáo rõ taxonomy mỗi loại câu hỏi.
8. Lưu item ID, difficulty, language direction, hangul choices, correct IDs,
   distractor rationale, copyright/provenance và review status.
   Nội dung tiếng Hàn mới phải là PENDING_HUMAN_REVIEW cho tới khi
   giáo viên/biên tập có thẩm quyền kiểm chứng, không giả HUMAN_APPROVED.
9. Kiểm chứng E2E ít nhất 30 mục với lựa chọn Hàn, bao gồm đúng/sai,
   ký tự Hangul, đổi câu cùng cấp, quest unlock, refresh và mobile emulation.
10. Game vẫn có nhiệm vụ giải đố biển hiệu/kéo chữ Sign Repair, Courier Rush
    và hành động tương tác: không biến toàn bộ game thành quiz popup.

DONE KHI: từ một nhiệm vụ farm/giao hàng, người chơi thấy câu hỏi dẫn
bằng Việt/Hàn, trả lời bằng chữ Hàn; câu trả lời đúng mới hoàn thành
bước yêu cầu; sai hiện feedback Hàn/Việt thích hợp và được thử lại.
Không có đáp án bằng tiếng Việt ở những mục đánh giá Hangul.

================================================================================
02E. P0-7 — NHIỆM VỤ ĐAN XEN NHIỀU TUYẾN, CÓ NHÂN VẬT & CÂU CHUYỆN
================================================================================
Học cảm giác nhiệm vụ liên kết, đan xen của RPG xã hội (ví dụ user nhắc
Võ Lâm Chi Mộng); KHÔNG sao chép câu chữ, NPC, địa danh, kịch bản, UI
hoặc game assets từ trò khác.

PHẢI THIẾT KẾ QUEST GRAPH (DAG hoặc state graph có điều kiện rõ) thay
cho một hàng danh sách nhiệm vụ rời rạc:
- MAIN STORY: Bí ẩn các mảnh thư, khôi phục biển hiệu/địa chỉ, khám phá thị trấn.
- FARM/DELIVERY: Gieo trồng, thu hoạch, giao đơn, mở hạt giống và công cụ.
- MERCHANT/SHOP: Quản lý hàng hóa, đặt hàng, thu gom đồ, thương nhân liên hệ.
- HISTORICAL/CULTURE: Thăm khu hanok/cung điện, NPC có câu chuyện văn hóa
  hư cấu phù hợp quyền hình ảnh, đồ vật/ký hiệu Hàn đúng bối cảnh.
- JEJU/EXPLORATION: Qua cầu, khám phá vườn quýt, hỗ trợ người dân/đảo,
  giải nhiệm vụ trên đường và quay về cửa hàng/nơi giao hàng.

CẤU TRÚC THẬT:
1. Một nhiệm vụ có thể mở 2–3 nhiệm vụ phụ cùng lúc, cho người chơi chọn.
2. Một nhiệm vụ phụ có thể cung cấp vật phẩm/thông tin cần để quay lại
   tuyến chính hoặc giúp mở tuyến phụ khác.
3. NPC A → địa điểm B → việc ở C → NPC D, có nhận–làm–đối thoại–nộp
   rõ ràng; không phải cùng một nút hoàn thành ngay ở bảng quest.
4. Ít nhất 3 chuỗi nhiệm vụ dài xuyên 2+ khu vực, có 2 điểm
   phân nhánh và 2 điểm hội tụ, đi qua 4+ NPC, ít nhất 2 công trình,
   khu farm và Jeju. Có một tuyến tùy chọn không chặn tiến trình chính.
5. Giai đoạn đầu có nhiệm vụ giới thiệu ngắn giúp người chơi không
   bị ngợp; sau đó mở dần, hiển thị nhiệm vụ chính/phụ/theo khu.
6. Quest prerequisite và unlock quy định bằng ID ổn định, versioned JSON
   hoặc dữ liệu cấu hình rõ, không hardcode vào text UI dễ hỏng.
7. Nhật ký hiển thị nhiều nhiệm vụ đang hoạt động; chọn 1 nhiệm vụ
   theo dõi, map hint/waypoint có thể bật tắt; tiến độ cập nhật khi
   hành động trong world, lưu khi qua nội thất/đổi scene/reload.
8. Hỗ trợ quest board/notice, NPC dialogue choices, điều kiện vật phẩm,
   nhiệm vụ phát hiện khi người chơi vô tình làm trước; không mất event.
9. Có kết quả câu chuyện nhìn thấy (khôi phục biển hiệu, giao hàng tới nhà,
   thay cảnh nhỏ, NPC lời thoại mới, mở cửa hàng, hạt mới).
10. Reward đúng một lần, không farming dupe, không softlock khi hết xu/seed,
    không ép điểm danh hoặc grind bắt buộc.
11. Gắn câu tiếng Hàn vừa đủ trong quest chain: học cụm từ từ tình huống,
    trả lời Hangul theo 02D, có gợi ý/giảm độ khó hợp lý. Luồng không
    khóa học miễn phí/TOPIK/EPS của website chính.
12. Bắt buộc có **quest dependency map** dễ đọc: các nhánh, prerequisite,
    NPC, location, unlock, reward và thời điểm hội tụ.
13. Số quest mục tiêu: không chỉ đếm title; ít nhất 12 quest HOẠT ĐỘNG
    end-to-end trong review, thuộc ≥4 tuyến, với ≥2 nhánh và ≥2 hội tụ;
    nếu chưa thể đạt số này, báo PARTIAL + bằng chứng thiếu, không
    tạo stub quest rỗng để đủ số.

GỢI Ý CHUỖI CHƠI (chỉ triển khai nếu hợp roadmap, đừng thay dữ liệu đã có):
  - Chuyện 1: NPC vườn → hạt đầu tiên → gieo/tưới → thu hoạch → shop giao đơn.
  - Chuyện 2: Shop yêu cầu bưu thiếp → bookstore giải tiếng Hàn → ghép biển
    Sign Repair → thư địa chỉ → Courier Rush giao tới công trình khác.
  - Chuyện 3: NPC Jeju cần đồ cung cấp → qua cầu bằng tuyến 02C →
    gặp dân đảo → nhận đơn hàng quýt → quay về merchant để mở tier cây mới.
  - Khi một nhánh xong, một nhánh khác nhận ảnh hưởng, không phải 3
    tuyến hoàn toàn độc lập vô nghĩa.

KIỂM CHỨNG:
- Trace 3 hành trình thực với event log theo NPC/scene/quest transitions.
- Trigger quest progress bằng action trong world, không bằng test direct mutation.
- Test resume/reload, decline/accept, complete out-of-order, wrong question,
  already-harvested, insufficient items, duplicate dialogue, reward exactly once.

================================================================================
02F. P0-8 — NỘI THẤT MỖI CÔNG TRÌNH PHẢI THẬT SỰ KHÁC NHAU
================================================================================
NHẮC LẠI: Owner nói vẫn CHƯA VÀO ĐƯỢC CÔNG TRÌNH.
Không chấp nhận “có asset interior trong repo” hoặc “3 phòng tồn tại trong
file ZIP” là bằng chứng sử dụng được ở Pages.

Trước khi dựng:
1. Inventory ALL building entrances trên canonical world, kiểm tra door anchor,
   door/collision và phân loại:
   - ENTERABLE NOW (có vai trò gameplay, nằm trong scope)
   - FUTURE/LOCKED (có nhãn rõ và lý do)
   - SCENIC ONLY (không hứa vào được).
2. Với mỗi ENTERABLE NOW, phải dựng nội thất tương ứng, khác phong cách và
   công năng. Không dùng một scene trống/generic template rồi đổi màu.

MINH HỌA CÁCH THIẾT KẾ — chọn địa điểm thực có trong world; không
giả định mọi tòa bên dưới đã có cửa:
- Seed/Grocery shop của Minseo (hoặc merchant thực tế):
  quầy gỗ hàng hóa, sọt, túi hạt, bảng giá pixel, kệ thực phẩm/đồ;
  có NPC đứng quầy, click/in-range E, mua bán cập nhật Coins/Inventory.
- Hiệu sách Jiho:
  kệ sách cao, bàn học, cửa sổ đèn ấm, biển Hangul/hộp chữ,
  NPC học giả, giải đố tiếng Hàn/Sign Repair; không giống shop hoa quả.
- Workshop Eunji:
  bàn đồ nghề, giá cuốc/bình tưới, dụng cụ cơ khí/nông nghiệp,
  nhiệm vụ sửa công cụ/nâng cấp tiện ích; ánh sáng và sàn phù hợp xưởng.
- Hanbit Station:
  sảnh vé/đồng hồ/bản tin/tủ đồ, NPC phụ trách thư/chuyến hàng,
  giao nhận hoặc courier; nhất quán mỹ thuật nhà ga đã khóa.
- Hanok/culture building ở Jeju:
  chiếu sàn/gỗ, bàn thấp, rèm/đèn, vật dụng truyền thống, màu vật liệu
  khác hoàn toàn nhà ga/cửa hàng hiện đại, NPC kể chuyện/quýt Jeju.
- Palace/cultural building nếu được phép mở: sân/hiên, sàn gỗ/mành,
  bố cục trang nghiêm, câu chuyện học lịch sử có nguồn; không dựng đồ
  nội thất tùy tiện sai thời đại.

YÊU CẦU THỰC THI:
3. Ít nhất 3 tòa đã cam kết enterable phải vào được ở build trên trình duyệt,
   từ vị trí nhân vật đi bộ tới cửa rồi E / tap. Một khi đủ QA, ưu tiên
   mở rộng các công trình có vai trò ở các phase tiếp theo theo roadmap.
4. Scene transition: fade/camera, actor spawn không kẹt collider; exit gần
   cửa trả lại đúng outdoor coordinate và camera, bảo toàn quest/inventory.
5. Interior thật gồm floor/walls/perspective, vật trang trí theo chức năng,
   props có chiều sâu, occlusion, đúng tỉ lệ nhân vật, collision phù hợp.
6. Không dùng JPG/render phẳng làm entire fake room; không phủ HTML form lên
   background mà gọi là gameplay. Popup shop chỉ là panel khi nhân vật
   ĐÃ thật sự đứng ở quầy bên trong phòng.
7. Tạo ít nhất hai tương tác đặc thù cho MỖI công trình enterable, gồm
   một hành động đóng góp thực cho quest/economy/learning.
8. Các scene phải phân biệt được bằng silhouette, bảng màu, sàn, đồ vật,
   ánh sáng và vai trò NPC; chúng có thể chia sẻ tileset kỹ thuật nhưng
   không được giống nhau về mặt bố cục/thẩm mỹ.
9. Trong building không có NPC giả lặp đôi ngoài trời; quản lý presence
   nếu cùng một NPC lịch sinh hoạt. Về ngoài đúng cửa, không teleport.
10. Test DESKTOP + mobile emulation, keyboard/touch, vào/ra lặp lại,
    save/load khi trong nhà, UI focus lock, camera bounds, scene resources.
11. Video chơi một mạch (KHÔNG cắt ghép) đi ngoài đường → vào cửa
    → đi trong phòng → tới NPC/quầy → giao dịch/giải nhiệm vụ
    → ra cửa → về world. Lặp lại cho từng interior.
12. Nếu công trình hiện chưa có cửa hợp lệ, tạo trigger/sửa cục bộ chân
    cửa theo art lock; KHÔNG tự phá façade, diện mạo hoặc map đã duyệt.

DONE KHI: owner vào một building và thấy một phòng MỚI có không gian,
mỹ thuật và gameplay RIÊNG; không phải cùng một menu giống nhau.
Phải có gallery side-by-side cho tất cả interior, video từ world
vào phòng tới interaction rồi ra, và log thật sau giao dịch.

================================================================================
02G. P0-1/P0-2 — LUỐNG ĐẤT VÀ HUD: NÂNG CHẤT LƯỢNG ĐẾN MỨC KHÔNG CÒN LỘ MẢNG CŨ
================================================================================
FARM:
1. Chụp ảnh native 1:1 toàn 6 luống tại Empty/Tilled/Sown/Sprout/Mature/
   Harvested, đọc actual Phaser draw order và underlying world bitmap.
2. Kiểm tra alpha, depth layers, seams, offsets/pixel snapping, crop/shadow
   overlap; truy ra các pixel lộ từ textures/nền cũ.
3. Không vá bằng một rectangle màu nâu phủ lên ground hoặc ghép screenshot.
   Dựng soil layers/tilekit phù hợp Art Bible; chỉnh ground nền cục bộ khi
   bắt buộc, bản đồ lớn ngoài farm GIỮ NGUYÊN.
4. Được tăng diện tích các ô trồng vừa phải, nhưng không lấn lối đi farm,
   NPC paths, cây chủ đạo hoặc collision; nếu nới thì cập nhật cell/collider
   và overlay cùng nhau. Không che hạt/cây ở tile biên.
5. Mỗi cell độc lập; khi plot ở stage khác nhau KHÔNG còn ghost crop cũ.
6. Có kiểm thử screenshot khi di chuyển camera, DPR1/2, zoom 1/2, đổi
   crop và reload; đếm difference ngoài ROI farm phải =0 (trừ HUD được phép).

HUD:
7. Tách presentation game HUD khỏi các nút website do `index.html` chèn:
   kiểm tra actual engine composition, scale, anchor, UI camera hoặc DOM
   overlay chuyên cho accessibility có skin game, z-index/focus/keyboard đồng bộ.
8. Coin icon, backpack, quest journal, seed/tool hotbar phải nằm nhất quán,
   không bị layout lệch do viewport; có pixel icons đúng art skill/quality.
9. HUD không chỉ đổi CSS: bấm túi phải hiện vật phẩm/số lượng thật;
   quest log phải có active chains/waypoint; coin phải cập nhật thực khi
   mua/bán/giao nhiệm vụ; hotbar thay đổi action/crop tool thật.
10. Test màn hình nhỏ, mobile safe area, scale, overlay không che 2/3 game,
    close/back/escape, controller input nếu có, screen reader/focus.
11. Cần screenshot HUD in-game tại ít nhất desktop + mobile emulation,
    liên kết data state và gameplay event; không dàn dựng bằng mock UI.

================================================================================
02H. P0 RELEASE GATE: CHỨNG CỨ QUAN TRỌNG HƠN TEST PASS ĐƠN THUẦN
================================================================================
Phải có 5 video kiểm chứng **không cắt** ở đúng candidate SHA:
  V01: farm till→seed→water→grow→harvest với hai luống khác state,
       không lộ texture cũ.
  V02: main Jeju bridge→junction→curve beside hanok→entrance→bridge,
       cả hai chiều, walking/running, collision debug ảnh đi kèm.
  V03: world door→interior A→transaction→exit.
  V04: world door→interior B→learning/question answers in Hangul→exit.
  V05: quest chain A↔B interleave; NPC handoff, shop, Jeju trip,
       Korean incorrect/correct answer, unlock/reward.

Bắt buộc cung cấp:
  - World coordinates/path trace do runtime xuất, không tự đoán từ ảnh.
  - Building registry mapping door positions→scene keys→exit positions.
  - Quest graph JSON / rendered chart & replay event log.
  - 30+ Korean questions test coverage/records for answer direction.
  - 6-plot native pixel atlas review, crop state screenshots.
  - HUD inventory/quest/coin consistency tests.
  - FULL TEST RUN với thất bại và rerun tách biệt; không gộp 73/77 + 4 retry
    thành “77/77 clean” nếu chưa có full clean run.
  - Commit/artifact+SHA256/manifest protected world hashes, rollback SHA,
    browser-based playable review URL, device test status NOT TESTED nếu đúng.
  - Ranh giới công khai: asset chưa rõ quyền, nội dung Hàn chưa human-approved
    phải không bị gắn nhãn clear hay tự phát hành commercial.

REVIEW HANDOFF PHẢI NÓI RÕ:
  - Nếu Pages hiện chưa được owner duyệt đúng artifact mới, chuẩn bị
    manifest chính xác và chờ approval; không tái dùng approval cũ.
  - Nếu cần chỉnh branch/workflow review, không đụng main/website prod,
    không xóa historical tags/commit.
  - Owner có thể mở `/play/` và thử được nội dung, không phải đi tìm nhiều ZIP.

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
4.1 Implement **at least 3 distinctly art-directed fully playable interiors**
    actually enterable from world doors in the Pages build (see 02F); target up to 5 if art/time
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
5.2 Quest chains (at least 12 functioning quests across >=4 interwoven storylines;
    see 02E for 2 branches/2 convergences; 15–30-minute review play):
    tutorial movement; seed first; till/sow/water; harvest; delivery;
    sell crop; unlock new seed; enter shop; visit orchard/Jeju; one follow-on task.
    Add alternate NPC/optional side tasks if stable.
5.3 For quest completion, require HANGUL answers where Korean competence is
    assessed (see 02D), not Vietnamese multiple-choice options; prevent spam:
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
7.2 Real browser route coverage (INCLUDE EXACT JEJU RED PATH 02C and all
    door→distinct room→NPC/service→exit interactions; require Hangul answers 02D):
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


ADDITIONAL OWNER ACCEPTANCE — A13 TO A20 (BECAUSE NEW FEEDBACK IS MATERIAL):
A13 — JEJU RED PATH: continuous bidirectional walk from bridge junction down the
      curve beside island hanok to its approach; no wall/water noclip.
A14 — HANGUL ANSWERS: Korean assessment choice options and typed responses
      in Hangul; VI instructions only as scaffolding; error retry same grade.
A15 — QUEST GRAPH: 12 fully functional quests in >=4 storylines with 2+
      branch points and 2+ convergence points; four NPCs and two scenes;
      in-world transitions, idempotent rewards and recoverable progress.
A16 — BUILDING UNIQUENESS: distinct architecture-specific rooms for every
      committed enterable building; 3 minimum; no generic tinted-room clone.
A17 — ENTERABILITY: owner can walk outdoors into a valid door trigger and
      reappear indoors, approach NPC/shop, transact, leave back to outdoors.
A18 — FARM CLEANLINESS: 6-plot ground ROI no ghost old map textures across all
      crop stages; independent 36 cell states if current build supports 36.
A19 — HUD INTEGRATION: responsive pixel HUD backed by real inventory,
      quest, currency and hotbar logic, no dead website buttons.
A20 — EVIDENCE: 5 uninterrupted videos V01–V05, native 1:1 before/after,
      exact tested SHA + browser Pages URL/ZIP, clean/failed test records.
A13–A20 are hard acceptance gates, NOT optional extras.
Do NOT mark COMPLETE if any hard gate lacks runtime evidence.

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


FINAL OWNER OVERRIDE 2026-11-10: Sửa 02B→02H trước khi báo hoàn tất.
Không yêu cầu owner gửi ảnh khoanh đỏ; Codex tự truy vết scene, camera và runtime coordinates.