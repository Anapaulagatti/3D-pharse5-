# CODEX — PHASE 3B-D FINAL GAMEPLAY QUALITY PASS
# Farming Art/Sprite Pipeline + Hanok West Passage Collision
# Prompt độc lập, KHÔNG CẦN ẢNH ĐÍNH KÈM

VAI TRÒ
Bạn là kỹ sư gameplay Phaser + pixel-art technical artist + QA chịu trách nhiệm hoàn thiện đúng hai lỗi còn tồn tại trong bản Korean Pixel Town review hiện hành. Chủ dự án đã nghiệm thu hướng tương tác in-world nhưng KHÔNG chấp nhận chất lượng hình ảnh các luống trồng và một điểm đường đi không thể đi qua.

ĐÂY LÀ TIẾP NỐI CANDIDATE HIỆN TẠI, KHÔNG PHẢI REBUILD/RESTART, KHÔNG PHẢI PHASE 3B-E. Hãy tự tra cứu code, git history, tài liệu Art Skill, tilemap, collision và Phaser runtime. Chủ dự án KHÔNG gửi ảnh khoanh đỏ, KHÔNG yêu cầu bạn xin lại ảnh. Vị trí và triệu chứng được mô tả đầy đủ dưới đây. Bạn phải tái hiện lỗi bằng runtime và tự xuất bằng chứng từ game.

BỐI CẢNH ĐÃ DUYỆT
- Repo nguồn: Anapaulagatti/3D-pharse5-; repo review: Anapaulagatti/3D-pharse5-review.
- URL review hiện hữu: https://anapaulagatti.github.io/3D-pharse5-review/play/
- World/Map, nhà ga Hanbit dựng mới, hai cầu Jeju, cung điện, hanok phía tây, 12 nhân vật chơi, 26 NPC và cosmetics đã được nghiệm thu theo checkpoint tương ứng. Hệ thống in-world dialogue, shop, quest, farming logic đã có candidate.
- Bản review gần nhất cho thấy tại khu nông trại phía tây-bắc có SÁU luống trồng xếp thành HAI hàng × BA cột. Chúng đang hiển thị giống SÁU tấm nền hình chữ nhật màu nâu, phẳng, đồng đều, như ảnh background được đặt phủ lên map. Không cho thấy nghệ thuật đất/cây và sự phát triển tự nhiên giống phong cách Gate 1.
- Lỗi di chuyển cụ thể: một con đường lát đá hướng BẮC–NAM, nằm SÁT PHÍA TÂY (bên trái) của ngôi nhà hanok mái ngói xanh đen trong khu lịch sử/phía tây cung điện. Nhân vật đứng ở đoạn phía nam lối đi, gần nơi giao với đường lát đá ĐÔNG–TÂY trước mặt nhà; nhìn bằng mắt có lối đi đi lên, nhưng tiến lên phía bắc đến đoạn cạnh hông nhà thì bị chặn/khó qua. Có đoạn gấp ở phần đầu phía bắc, gần mép mái/tường và cây; đây là CHOKE POINT PHẢI SỬA. Không được hiểu nhầm với hai cầu Jeju, nhà ga hay lối vào cung điện.
- Không có ảnh tham chiếu mới: tự xác định đúng vị trí bằng dữ liệu bản đồ, object registry, world coordinates, camera spawn, asset metadata và test di chuyển trong Phaser.

QUY TẮC BẤT DI BẤT DỊCH
1. Trước khi chỉnh sửa: xác minh repository, HEAD, branch, working tree, candidate đang triển khai, commit và manifest hiện hữu. KHÔNG checkout checkpoint lịch sử làm HEAD nếu không có căn cứ. Tạo nhánh hotfix tách biệt và snapshot có khả năng rollback; không xóa lịch sử Git.
2. KHÔNG sửa ảnh nền toàn bản đồ, KHÔNG tái tạo Gate 1/Gate 3, KHÔNG đổi art/map/collision ngoài hai vùng thực sự có liên quan và các dependency tối thiểu.
3. Giữ nguyên 12 playable characters, 26 NPC, các hoạt ảnh đã duyệt, dữ liệu gameplay, shop, mission, XP, coin logic và toàn bộ những cải tiến movement/camera đã đạt. Không đưa map cũ bị loại vào code hay bundle. Không thêm tóc/phụ kiện đầu đã loại bỏ.
4. KHÔNG dùng CSS/HTML rectangle, Canvas phẳng hoặc tấm PNG lớn phủ lên terrain như cách sửa thay thế cho art của ruộng. KHÔNG trích lại ảnh ruộng cũ/cắt-dán để giả lập độ chi tiết. Không tự nhận 'đã dùng Skill' nếu không có asset provenance.
5. Không sử dụng artwork không rõ quyền; không sao chép sprite/art cụ thể từ Hay Day/Pixels. Chỉ tham khảo gameplay loop, sáng tạo asset độc lập theo chuẩn mỹ thuật dự án.
6. Giữ gameplay trực tiếp trong Phaser: WASD/arrow/touch, tiếp cận plot/NPC, tương tác trong tầm. HUD gọn; không phục hồi menu lớn thực hiện hành động từ xa.
7. KHÔNG gắn dữ liệu thật/production vào test; không dùng secret không cần thiết, không thêm dịch vụ trả tiền. Không làm sai lệch trạng thái NOT TESTED của thiết bị vật lý chưa thử.

A — ART SKILL DISCOVERY & ROOT CAUSE (LÀM THẬT, KHÔNG CHỈ AUDIT)
A1. Tra cứu quy trình vẽ đã sử dụng cho map Gate 1 và Juni: Art Skill Registry/README/art bible/asset-generation scripts/atlas packaging (nếu có), source asset, native resolution, palette, lighting/shadow, camera/projection, pixels per unit, animation conventions, asset license/provenance. Nêu đường dẫn file đúng trong repo, không bịa tên skill hay đường dẫn.
A2. Truy nguồn sáu mảng ruộng màu nâu: tìm asset, render layer, depth, crop/plot objects, background tiles, các lệnh drawRect/fillRect/generated textures, scale/resampling. Chứng minh nó được vẽ như thế nào. Phân biệt nền địa hình phải giữ với phần overlay gameplay cần thay.
A3. Chọn pipeline mỹ thuật CÓ THẬT đã được duyệt: nếu repo có Art Skill/asset workflow thì tái sử dụng đúng; nếu không có tool/generator, thực hiện sprite authoring theo đúng quy ước kỹ thuật và mô tả trung thực. Không gọi tên một skill chung chung rồi để asset placeholder.
A4. Khóa local edit ROI theo tọa độ của sáu luống, crop sprite và lối đi cạnh hanok; tạo baseline/pixel diff cho protected art ngoài ROI. Không gây seamless/cutout ở mép ruộng, không phủ mất hàng rào, lối đi, cây, shadow, nhân vật.

B — FARMING PHẢI LÀ GAME OBJECT VÀ ART NATIVE, KHÔNG PHẢI 6 TẤM BACKGROUND
B1. Mỗi luống hiện có giữ nguyên VỊ TRÍ, hình học và lối đi đã chốt. Tách thành lớp: ground/soil tile, border/rim (nếu có), tilled soil overlay, seed/crop sprites độc lập, wetness indicator, interaction hint, effects. Không làm mất chi tiết art chung quanh. Mỗi plot phải có ID ổn định, occupancy, crop type, timing, moisture, stage, collision/interaction region riêng.
B2. Nếu mỗi luống lớn chứa nhiều ô canh tác con, hãy xác định grid của nó theo địa hình và thiết kế logic mỗi ô có trạng thái riêng; không được coi toàn luống 1 ảnh lớn hoặc thay một PNG cho cả sáu luống. Bảo đảm tỷ lệ đồ họa tự nhiên so với Juni và NPC, không có 6 tấm nâu phẳng như UI panel.
B3. Tối thiểu các trạng thái hiển thị khác nhau và dễ nhận biết bằng mắt (số frame thực tế tùy workflow, nhưng KHÔNG bỏ stage):
    EMPTY: đất có texture native liền mạch với map;
    PREPARED/TILLED: đất xới có đường luống/furrow;
    SEEDED: dấu hạt/lỗ gieo rất nhỏ;
    SPROUT: mầm nhỏ;
    YOUNG: cây non;
    GROWING: cây lớn hơn rõ rệt;
    MATURE/READY: cây trưởng thành có hình thu hoạch rõ;
    HARVESTED: animation nhặt/nhổ + đất trở lại trạng thái trống/phù hợp.
    WATERED là thuộc tính độc lập với crop stage, phải có wet soil overlay/particles ngắn nhưng không biến luống thành màn hình màu xanh.
B4. Asset mới phải là sprite/tile art theo chuẩn Gate 1: palette/tone/ánh sáng, rim lighting, contact shadow, phối cảnh nhìn từ trên hơi nghiêng, edge antialiasing/pixel fidelity, scale 1:1 (nearest-neighbor khi phù hợp). Có sprite sheet/atlas hoặc component native riêng; tài liệu nguồn và license/provenance cho từng asset mới. Không sử dụng hình của tựa game khác.
B5. Render pipeline: stage sprite đổi trực tiếp IN-WORLD, depth sort đúng chân nhân vật và cây, sprite không bị scale méo, z-index không che người/đường, không rung khi camera di chuyển. Không tạo ảnh tĩnh 'demo growth' hay video thay cho state trong runtime.
B6. Tương tác thật: nhân vật đi tới ô đất còn trống; phải ở interaction range và reachability hợp lệ; trang bị/chọn hạt; play animation cúi/gieo hoặc overlay hand/tool animation; hạt trừ đúng một lần; crop sprite mọc trong ô đó. Tưới bằng thao tác trực tiếp và visual wetness. Thời gian tăng trưởng theo từng giống/cấu hình, timer tiếp diễn khi rời farm hoặc tải lại trang; có thời gian phù hợp để test review (test-speed chỉ bật qua debug/test config tách biệt, không làm méo economy). Thu hoạch tại chỗ, biến đổi hình ảnh, cập nhật inventory và quest, chống double-harvest.
B7. Giữ loại hạt, crop IDs, công thức, shop và quest đang có; không đổi balance tùy tiện. Nếu hiện chỉ đủ art cho một giống thì tạo art native chuẩn cho giống đó và báo rõ phạm vi; không giả vờ mọi giống đã có sprites.
B8. Yêu cầu visual độc lập: gieo ở một ô không thay đổi toàn bộ sáu luống; một ô có cây non cạnh ô trống hoặc cây trưởng thành phải hiển thị khác nhau cùng lúc. NPC/player di chuyển qua hành lang giữa luống không kẹt. State persist cho từng ô và khôi phục sau reload.

C — SỬA CHÍNH XÁC LỐI ĐI KHOANH ĐỎ MÀ KHÔNG CẦN ẢNH
C1. ĐỊNH VỊ: ở phía TÂY ngôi nhà hanok phía tây của cụm cung điện. Con đường LÁT ĐÁ CHẠY THEO HƯỚNG BẮC–NAM giữa mặt hông phía trái ngôi nhà và vùng cây/bụi phía tây. Đầu nam nối với lối ĐÔNG–TÂY phía trước nhà, đầu bắc đi lên gần khu sân/cây. Người chơi hiện đứng dưới điểm thắt, cố đi lên bị chặn hoặc phải canh pixel. Đây là tuyến chính xác cần debug.
C2. Trước sửa, tạo collision-debug overlay chỉ dùng development gồm: world-space coordinates, camera offset, player FOOT collider, tile collision grid, physics bodies, polygon blockers, nav masks, depth/occlusion, interactive zones và pathfinding footprint. Dùng thực tế Phaser hoặc automation input để tái hiện BLOCKED, ghi tọa độ/đối tượng gây chặn. Không được chỉ nhìn ảnh rồi nới hitbox đại trà.
C3. Kiểm tra nguyên nhân có thể: collision layer trùng lặp, body dựng từ ảnh nhà/roof thay vì base-wall, offset của body so với tile origin, phantom body của cây/hàng rào, collider bao luôn lối đá, feet-size/anchor sai, pathfinding mask khác Arcade/Matter physics, camera/input/diagonal normalization, clipping do foreground depth. Chứng minh một hoặc nhiều nguyên nhân thật trước khi sửa.
C4. Sửa tối thiểu ở data/collider/chỉ số body: giữ solid wall, cột, thân cây và ranh nhà là vật cản; chỉ mở chính phần đường nhìn thấy có thể đi, bảo đảm clearance cho toàn bộ hình hộp CHÂN nhân vật cộng safety margin phù hợp. Nếu thực sự không đủ bề rộng art, chỉ đề xuất và thực hiện chỉnh cảnh cực nhỏ trong ROI, có đối chiếu nguồn. Không xuyên qua tường hoặc trượt vào cây để 'PASS'.
C5. Kiểm tra hành trình đi THỰC TẾ qua nút thắt: từ phía nam đi lên bắc, từ bắc xuống nam, đi từ hướng tây/đông vào điểm nối (nơi thật sự kết nối), dừng rồi đi lại, đổi hướng trái-phải liên tục, giữ W+D / W+A, Shift-run, đi cạnh mép tường và hàng rào, với Juni và ít nhất một nhân vật khác; tốc độ và collider thống nhất. Không được sửa bằng teleport hoặc ghost mode.
C6. Mở rộng kiểm tra có mục tiêu: các hành lang xung quanh farm, lối vào NPC liên quan quest, shop, góc hàng rào cạnh nhà, hai đầu cầu Jeju; sửa CHỈ các điểm fail được tái hiện. Không làm mới art hay đổi vùng đã duyệt.
C7. Đặt runtime regression test với mốc tọa độ world/path corridor, đường đi có thể test từ nhiều góc/điểm spawn. Thêm test kiểm tra collision semantics (passable/solid) và test camera không snap. Nếu vị trí không thể nhận diện đơn trị, thực hiện scene-index/search theo 'western hanok', gửi ra danh sách tọa độ ứng viên kèm video debug rồi chọn chính đối tượng khớp mô tả; không yêu cầu người dùng upload ảnh.

D — QA GATE BẮT BUỘC (KHÔNG TỰ ĐÁNH DẤU PASS)
D1. Gameplay real Phaser, không test thuần state-machine: truy cập /play/, chọn nhân vật, điều khiển đến farm, gieo 1 ô, tưới 1 ô, để 1 ô khác trống, tăng thời gian bằng test clock có kiểm soát, nhìn giai đoạn 1/2/3/tốt nghiệp, thu hoạch, kiểm tra inventory/coin/quest và refresh restore. Không dùng hook thao tác thẳng dữ liệu thay cho walkthrough gameplay trong test chính.
D2. Tối thiểu 6 tình huống kề nhau: empty + sprout, young + mature, watered + dry; đảm bảo không render cùng một hình; kiểm tra không có mảng hình chữ nhật nâu phẳng phủ map. E2E xác nhận 1 plot độc lập với 5 plot còn lại. Không harvest trùng, không nhân đôi reward.
D3. Path test tại choke point Tây Hanok: đủ 2 hướng Bắc↔Nam, walk/run, stop-start, diagonal input, mỗi loại nhân vật đã chọn; kết quả dựa trên toạ độ cuối cùng qua đoạn chặn, collision events và frame trace, không chỉ số unit tests PASS.
D4. So sánh screenshot native 1:1 BEFORE/AFTER với bản đã duyệt và ảnh gameplay được tạo tự động từ runtime (không dùng ảnh do user cung cấp). Pixel diffs ngoài ROI bằng 0 hoặc thay đổi đã chứng minh liên quan; giữ toàn bộ protected map/NPC/ga/cầu/cung điện không đổi. Kiểm tra shader, DPR/zoom, pixel crispness, map seams, camera.
D5. Unit + integration + Phaser E2E + browser desktop/mobile emulation + offline refresh. Ghi rõ NOT TESTED nếu chưa test Android/iPhone vật lý. Mọi FAIL trước phải được sửa nguyên nhân rồi rerun, không gộp số lần rerun thành một chuỗi PASS sạch.
D6. Lưu video gameplay thật (không phải mock): player đi→gieo→tưới→các stage→thu hoạch; và video nhân vật đi xuyên suốt hành lang Tây Hanok trong cả hai hướng. QA ảnh/video phải có đường dẫn hiện hữu, giải nén ZIP kiểm tra file tồn tại.

E — TRIỂN KHAI REVIEW VÀ ROLLBACK
E1. Giữ bản GitHub Pages hiện có làm rollback, tạo checkpoint nguồn và manifest SHA256 artifact mới. Không ghi website học tiếng Hàn chính thức, không merge/deploy production. Không xóa/rewrite Git lịch sử.
E2. Chuẩn bị artifact và public review đúng quyền asset; không mặc định tên hư cấu giải quyết bản quyền. Tôn trọng GitHub protected environment, không vượt qua approval. Chỉ cập nhật https://anapaulagatti.github.io/3D-pharse5-review/play/ sau khi workflow/manifest được chủ dự án duyệt đúng bản; nếu chưa có quyền thì báo 'READY_FOR_OWNER_APPROVAL' cùng URL workflow, không tự nhận 'DEPLOYED'.
E3. Sau deploy thật, fetch HTTPS URL, kiểm chứng asset hash/build ID, network/console, smoke test farming/path trên URL đang chạy, xử lý cache stale bằng versioned assets hoặc cache invalidation phù hợp. Không tuyên bố live chỉ dựa vào commit/CI.

F — BÀN GIAO NGẮN, ĐỦ BẰNG CHỨNG
Báo cáo theo thứ tự:
1. Kết luận: READY_FOR_OWNER_REVIEW / BLOCKED, và DEPLOYED hay NOT_DEPLOYED.
2. Nhánh, base SHA, commit SHA, checkpoint, rollback reference.
3. Danh sách file đã thay + Art Skill/asset pipeline được dùng thật; nguồn và quyền asset.
4. Farming: mô hình per-cell/per-plot, sprite atlas & states, timer/persistence, ít nhất 2 crop stages khác nhau đồng thời.
5. Lối Tây Hanok: tọa độ world trước/sau, collider thực gây tắc, chỉnh sửa nhỏ nhất, hướng đi đã test thực tế.
6. Matrix QA: unit/integration/E2E, native 1:1, desktop/mobile emulation/thiết bị thật; PASS / FAIL / WARN / NOT TESTED.
7. Link video BEFORE/AFTER, clip farming và clip đi hai hướng tại Tây Hanok; links ZIP/artifact đã kiểm chứng.
8. Manifest SHA256, GitHub Actions run và URL Pages nếu triển khai được; các blocker/known issues còn lại.

ĐIỀU KIỆN CHẤP NHẬN ĐẶC BIỆT
- KHÔNG ĐẠT nếu 6 luống đất vẫn là sáu hình chữ nhật màu nâu phẳng, chỉ được thay thế bởi một 'background mới'.
- KHÔNG ĐẠT nếu nhấn nút gieo chỉ đổi số liệu, còn cây không thực sự thay sprite/stage trong Phaser.
- KHÔNG ĐẠT nếu điểm đi dọc HÔNG TÂY HANOK vẫn chắn người chơi.
- KHÔNG ĐẠT nếu sửa path bằng cách vô hiệu collision toàn bộ nhà/tường/cây.
- KHÔNG ĐẠT nếu có thay đổi map/NPC/nhà ga/cầu/cung điện ngoài ROI không được giải trình.
- KHÔNG ĐẠT nếu không có bằng chứng thao tác thật hoặc chỉ trả một danh sách unit tests.

Hãy tự kiểm tra và sửa hoàn chỉnh trong một đợt, không xin lại ảnh khoanh đỏ, không dừng chỉ để 'audit' hoặc hỏi phê duyệt lắt nhắt. Chỉ dừng khi có blocker quyền/phát hành thực sự, hoặc khi đã bàn giao candidate cho chủ dự án nghiệm thu. Không bắt đầu Phase 3B-E.