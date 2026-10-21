# Gate 1 mới — Quy chuẩn hình ảnh + quy hoạch toàn thế giới

**CHỜ NGƯỜI DÙNG DUYỆT. Chỉ Gate 1; chưa triển khai Gate 2 hoặc Gate 3.**

Theo [chỉ đạo mới nhất](../current/FINAL_WORLD_MASTER_PROMPT.md), phố mẫu cũ là chuẩn chất lượng tham chiếu. Cách đánh số cổng trong chỉ đạo này thay thế quy trình trước. Không tự suy diễn rằng quy hoạch mới hay các lát cắt đã được duyệt.

## Hồ sơ để xem

- [Bộ quy chuẩn hình ảnh](STYLE_BIBLE.png) và [bản HTML có ảnh tham chiếu 1:1](style-bible.html): bắc truyền thống, nam hiện đại, vành đai chuyển tiếp, bờ biển/đảo. Phân biệt rõ ảnh tham chiếu với các cam kết cần chứng minh tại Gate 2.
- [Bảng phân khu và chú giải](MASTERPLAN_BOARD.png), [bản HTML](masterplan-board.html) và [quy hoạch trong Phaser](MASTERPLAN_REVIEW.png) — sơ đồ có thu nhỏ và ghi rõ, không phải ảnh final art. [Canvas quy hoạch](MASTERPLAN_ZONING.png).
- [Graybox toàn bản đồ native 4096 × 4608](GRAYBOX_NATIVE_4096x4608.png), xuất trực tiếp từ Phaser ở zoom1, DPR1; không nội suy hoặc dựng ảnh thay game.
- Crop gameplay zoom1 thật: [bắc](NORTH_NATIVE_1X.png), [chuyển tiếp](TRANSITION_NATIVE_1X.png), [nam](SOUTH_NATIVE_1X.png), [bờ biển/cầu](COAST_NATIVE_1X.png), [đảo](ISLAND_NATIVE_1X.png), [điện thoại ngang](MOBILE_LANDSCAPE.png). Desktop crop 1366 × 930; mobile 844 × 304, giữ một pixel nguồn trên một pixel canvas.
- [ZIP xem thử](WORLD_GATE1_PLAYABLE.zip): giải nén, chạy `python3 start.py`, mở URL được in ra. Không cần Node để xem. Phím WASD/mũi tên, Shift chạy, E xem điểm đến; điện thoại dùng cần cảm ứng. Trên máy phát triển: `npm run dev -- --port 4240` và `/3D-pharse5-/world-gate1.html`. `?overview` cho sơ đồ; đi bộ mặc định zoom1. Chỉ `?qa` có hook đặt điểm bắt đầu phục vụ kiểm thử/chụp ảnh.

## Logic khu vực và bố cục

Thế giới mới 4096 × 4608, khác phạm vi bản cũ; chưa tuyên bố tương thích tọa độ cũ. Nửa trên là di sản: cung điện ở trên cùng, học viện và sân trà ở tây, cơ sở văn hóa ở đông. Cung điện có ba cạnh tường và hai đoạn tường phía nam để chừa cửa chính rộng; lớp công trình phụ tạo thứ bậc, không đặt đường nhựa trong lõi. Khoảng đất ngoài các compound dành cho vườn đệm và địa hình, không phải các lô xây dựng bỏ quên.

Vành đai chuyển tiếp y1690–2080 là vườn, đá ấm và cửa mở. Trục đi bộ trung tâm không đứt; nhựa đường bắt đầu ở phía nam. Điểm cần chứng minh tại Gate 2 là cách đổi vật liệu và phối cảnh, không chỉ đổi màu nền.

Nam có hai mặt phố thương mại/công cộng tại y2160–2620; một tuyến đông–tây gắn cửa quán, nhà sách/học tập và civic hall với điểm chờ transit. Phía dưới là vườn giải trí có vòng dạo riêng ở tây, đồi tháp có tiếp cận cong ở đông. Nam cùng là chợ cảng, lối dạo bờ kè và terminal; tránh đặt tháp, vòng quay hay nhà ga thành các vật thể rời trên bãi cỏ.

Đảo là vườn quan sát ở đông nam. Lối đến rõ: đại lộ → điểm bờ cảng → cầu đi bộ vật lý → vòng dạo cong → đài quan sát. Cầu là quyết định quy hoạch mới để tạo kết nối liên tục có thể kiểm thử, thay vì tái sử dụng cơ chế/phân bố đảo cũ. Terminal phà dự kiến bám bờ, **chưa có tàu hoặc cơ chế phà vận hành**.

## Đường đi và ranh giới

Bốn cấp: trục chính 144–176px; tuyến thứ cấp 112–144px; tiếp cận cục bộ 80–100px; dạo vườn cong 88–100px. Rộng hơn hay hẹp hơn theo công năng, không trải cùng một nền khắp bản đồ. Các đầu lối phục vụ cửa vào, điểm ngắm cảnh, sân vườn hoặc kết nối tuyến khác. Ranh khu được xác định trong dữ liệu, tường cung điện là khối solid; viền cây, lan can và tường thấp ở các khu còn lại là ý định Gate 2, chưa giả vờ đã hoàn thành trong graybox.

Chấm vàng là điểm tiếp cận/đích quy hoạch, không nhất thiết là vị trí cửa trên mặt đứng cuối. Các khối màu là diện tích công trình/cảnh quan dự kiến, không phải mô hình cao độ hay artwork thay thế. Cấm coi các vùng trống của graybox là quyết định giữ bãi cỏ trống trong bản final. Gate 2 phải kiểm chứng tỷ lệ mặt đứng, ngưỡng cửa, độ dày biên và mật độ đồ đạc bằng art thật trước khi nhân rộng.

## Bằng chứng reset và nguồn

Nguồn mới duy nhất cho hình học là [plan.json](../../assets-src/world-gate1/plan.json), viết độc lập bằng tọa độ literal ở nhiệm vụ này. Không đọc layout, road network, prop grouping hoặc coastal/island sketch V1–V10 để làm đầu vào. Không gọi generator/build helper cũ. Phố mẫu cũ và ảnh bắc chỉ xuất hiện trong style bible, không làm nền runtime.

Đồ thị runtime: `world-gate1.html → src/world-gate1/main.ts → geometry.ts → plan.json`; ngoài Phaser/CSS chỉ dùng technical Joystick và atlas Juni gốc. [Kiểm toán nguồn + SHA256 + bảo toàn 214 file cũ](source-and-navigation.json) ghi các import thực tế. [Browser QA](browser-qa.json) lưu request thực: không có map/art nam cũ, không dùng ảnh chụp làm scenery. Nguồn/code/art cũ vẫn tồn tại như hồ sơ lịch sử an toàn, không bị xóa recovery evidence; root app cũ không được trình bày thành bản final mới.

Không tạo mỹ thuật mới, không gọi imagegen hoặc paid provider. Hình graybox và màu quy hoạch được vẽ bằng mã theo yêu cầu block-plan. Đã đọc Forge `generate2dmap` và `codeart2d` tại pin `5324342fdfab72430f4e9604f3fe427009f8596d`; **không tuyên bố đã chạy Forge bundle/nav/export/verifier** trong nhiệm vụ này. Dùng bộ kiểm tra hình học riêng và Phaser thật, có báo cáo thực bên dưới. Không dùng art/model từ Pixels.xyz.

## QA và giới hạn

[QA tổng hợp](validation.json), [browser QA](browser-qa.json), [kiểm tra đường cong render thực](rendered-route-audit.json), [nguồn + navigation](source-and-navigation.json), [kiểm thử ZIP](package-verification.json).

- Build ứng dụng cũ và build preview riêng thành công; typecheck, lint và format kiểm tra riêng pass; 12 unit tests cũ pass.
- 16/16 đích đến liên thông trên lưới 16px với khoảng chân 16px; 17 tuyến centerline, gồm spline Phaser thật, không xuyên solid/nước. Chưa chứng minh toàn bộ bề rộng lòng đường đáp ứng collider/art cuối.
- 10 tình huống browser pass: entry thường không có teleport hook; bàn phím tốc độ thường; E tại cửa; chặn công trình; qua vùng chuyển tiếp; qua cầu bằng di chuyển thật; dừng ở mép nước; CDP touch ngang; không lỗi trang/HTTP hoặc nạp art nam cũ; Canvas DPR1, texture Juni NEAREST scaleMode=1 và CSS pixelated.
- Atlas Juni 144 frame giữ nguyên byte, thân khoảng 80px, zoom1/nearest. Controller preview là điều khiển graybox riêng ở 60/100px/s, không phải bản thay thế state machine/gestures/physics đầy đủ của game cũ; code gameplay gốc được giữ nguyên. Không tuyên bố hoàn thiện Y-sort, tương tác NPC, nội thất, art occlusion hay gesture integration của thế giới final.
- Screenshot native giữ đủ pixel; sơ đồ thu nhỏ chỉ để xem quy hoạch. Crop style bible dùng cửa sổ 1:1 từ ảnh gốc, không phải art mới. Tương quan phối cảnh bắc–nam còn phải giải quyết ở Gate 2.
- Cảnh báo build gốc: chunk JS lớn hơn 1600kB; preview riêng khoảng 1.39MB JS. Lần lint đầu quét nhầm build output (4917 lỗi từ bundle), đã sửa ignore `dist-*/**` rồi chạy lại; không tắt quy tắc kiểm tra source.
- Phép thử sampling đầu kiểm tra context sau khi vẽ text thấy `imageSmoothingEnabled=true`; đây không phải trạng thái draw sprite. Đã đổi sang kiểm tra NEAREST của nguồn texture thật, vì `CanvasRenderer.js:850` đặt smoothing theo nguồn tại mỗi draw. Không thay ngưỡng hay sửa báo cáo cũ thành pass.
- Browser Chromium Canvas/phần mềm; mobile landscape được giả lập, chưa kiểm thử điện thoại vật lý. Không coi test pass là duyệt mỹ thuật. Không claim GitHub CI.

## Điểm dừng bắt buộc

Chỉ giao Gate 1. Gate 2: một mẫu bắc, một mẫu nam, một mẫu đảo/bờ biển bằng Phaser thật — **CHƯA LÀM**. Gate 3: toàn thế giới — **CHƯA LÀM**. Chưa merge main hoặc deploy.

**Bạn có duyệt Gate 1 — quy chuẩn hình ảnh và quy hoạch này — để chuyển sang Gate 2 gồm ba lát cắt mỹ thuật không?**
