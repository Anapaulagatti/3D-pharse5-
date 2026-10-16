# URBAN-PLAN-001 — quy hoạch khu phố để duyệt

**Trạng thái: CHỜ DUYỆT PHÂN KHU. Chưa dựng bản đồ cuối, chưa tạo artwork/NPC mới.** Yêu cầu đầy đủ: [URBAN_LOGIC_RESET.md](../current/URBAN_LOGIC_RESET.md). [Sơ đồ PNG](district-zoning-plan.png), [SVG chỉnh sửa được](district-zoning-plan.svg), [tọa độ nguồn](zoning-plan.json).

## Vì sao cần thay đổi

Bản chơi hiện tại có quảng trường, cầu, đường sách và học viện nối nhau, nhưng chỉ là dải 2048×768: phần lớn khám phá đi theo một chiều. Quy hoạch trước chia khu tương lai theo ô mở rộng, chưa giải quyết toàn bộ quan hệ mặt tiền–đường–sân, dòng nước và ranh tường. Biên sân/đất còn cứng; mương thẳng chưa tạo thành hệ thống cảnh quan. Việc từng đạo cụ có đường tiếp cận không chứng minh cả khu phố có logic đô thị. Đây là lý do sửa cấu trúc trước khi thêm trang trí.

Game và toàn bộ pixel assets hiện tại được giữ ở `recovery/before-urban-zoning-20261016` → `d5701fc251913e28ad9cea6ae3404a88a553adbd`. Không đóng băng mọi vị trí cũ cho bản tương lai: sau khi duyệt quy hoạch, có thể sắp lại chúng trong bản đồ ứng viên riêng, giữ bản gốc khôi phục được.

## Cấu trúc đề xuất

Một khu phố hư cấu **4096×3072 px**, không phải mô phỏng địa lý Seoul hay bản sao một game khác. Giữ Juni cao80px, tile32px, foot body16×8, walk60/run100. Không tăng tốc hay thu nhỏ avatar để làm thế giới có vẻ lớn. Camera theo người chơi, 3/4 nhẹ, zoom nguyên; sơ đồ nhìn toàn khu chỉ dùng để quy hoạch.

| Phân khu | Công năng và hình thái | Quan hệ đường / người dùng |
| --- | --- | --- |
| Cổng và ranh cung thành phía bắc | Cổng nghi lễ ba gian, tường đá liên tục, sân trước | Kết thúc trục thị giác; phía trong cung chưa mở, không giả làm lối ra chơi được |
| Quảng trường trung tâm | Không gian gặp gỡ thoáng, tượng Sejong lệch khỏi đường đi chính | Điểm đến ở phía nam; nhìn thấy cổng phía bắc và hai lựa chọn sang học viện/phố danh nhân |
| Học viện phía tây bắc | Giảng đường năm gian, hiên và sân học yên tĩnh | Cửa quay nam, lối tiếp cận riêng từ đường ngang; Sejong ở sân, bài học trong phòng đọc |
| Phố danh nhân phía đông | Xưởng thiên văn của Jang và nhà sử liệu/hiên chiến lược của Yi | Hai hình khối/công năng khác nhau; nối quảng trường và ngõ hanok; không dựng cảng giả cho bảo tàng |
| Phố sách và văn hóa phía tây | Hiệu sách, văn phòng phẩm, trà quán, xưởng thủ công | Hai mặt phố có ngõ nối; hàng hóa nằm ở hiên/hốc mặt tiền, có sân dịch vụ phía sau |
| Vườn và mặt nước ở giữa phía nam | Đình nghỉ mở, hồ mở rộng từ suối, bờ trồng cây và lối dạo | Nơi nghỉ khỏi chợ; hai cầu nối vòng khám phá, không đặt nhà chắn lối bờ nước |
| Ngõ hanok phía đông | Nhà sân U nhỏ, nhà góc L, nhà vườn và nhà mái thấp | Nhà nhỏ hơn công trình công cộng, dùng ngõ chung; sân riêng không trở thành đường xuyên nhà |
| Sân hội họa phía tây nam | Hanok thấp, sân vẽ ngoài trời, cây vườn | Saimdang thuộc sân xưởng, nối ngõ phía nam và cầu tây |

Hình chữ nhật trên sơ đồ là **đặt chỗ khối nền**, chưa phải mái hoàn thiện/collider. Mỗi nhà có mã, hình thái, cửa và điểm tiếp cận trong JSON; nhà nhỏ không phải bản thu nhỏ đổi màu của giảng đường. Giữ mái nằm ngang, mặt trước rõ, hiên và bậc có chiều sâu; không nghiêng chéo kiểu isometric. Dùng tham khảo hanok/cổng cung/giảng đường Hàn Quốc để nghiên cứu cấu tạo, không tuyên bố tái dựng lịch sử chính xác hoặc trộn các danh nhân khác thời thành người đương thời.

## Mạng đường, ranh giới và mặt nước

Trục chính rộng160px từ cổng xuống quảng trường. Đường ngang128px nối học viện với phố danh nhân. Hai nhánh96px tại x1376 và x2720 đi xuống hai cầu, nối đường trở về phía nam y2816. Ngõ64px và đường vườn nhỏ hơn làm các lựa chọn phụ, không thay thế đường chính. Chiều rộng tính là khoảng đi bộ **sau khi** trừ bậc, biển, cây, bàn ghế; công đoạn art phải giữ được khoảng trống này.

Tường cung thành chạy liên tục từ mép tây đến cổng và từ cổng đến mép đông ở y448. Cổng là chỗ ngắt có chủ đích; phía bắc là vùng đóng/dự trữ. Không rải các đoạn tường trang trí giữa sân hay gọi đây là thành bao quanh toàn khu phố.

Suối đi từ mép tây sang mép đông, đổi hướng nhẹ theo vườn và mở thành hồ ở giữa. Dành64px lòng nước và24px bờ mỗi bên. **Chỉ hai điểm vượt tại (1376,2304) và (2720,2304)**; cầu dài144px phủ cả bờ, deck rộng96px nối đúng đường. Nước không cụt sau nhà, không tự cắt ngang đường khi thiếu cầu. Đường vườn phía bắc hồ đi vòng đình, không xuyên qua khối đình. Đầu vào/ra tại mép thế giới thể hiện dòng tiếp tục, không giả thành sông có nguồn đã được mô phỏng.

Ghế ở hốc nghỉ nhìn ra sân/hồ; đèn theo ngã rẽ, cửa và đầu cầu; chum ở sân phục vụ nhà/trà quán; biển ở mép mặt tiền; hàng chợ ở vịnh bán hàng. Cây lớn nằm rìa sân/vườn; giữ tầm nhìn vào cửa, không dùng tán che lỗi đặt chỗ. Quy tắc chi tiết: [placement-rules.md](placement-rules.md).

## Cảm giác khám phá

Từ điểm đến quảng trường, người chơi có thể rẽ sang học viện hoặc phố danh nhân. Vòng dài: quảng trường → xưởng/bảo tàng → cầu đông → ngõ phía nam → sân hội họa → cầu tây → phố sách → học viện → quảng trường. Các góc khám phá có lý do: hiên đọc sách, sân dụng cụ thiên văn, vịnh trà, sân vẽ và mép hồ. Không đặt nhiệm vụ bắt quay lại trên một hành lang duy nhất.

Trục cổng–đường ngang dài864px, ước tính14.4s đi bộ. Vòng hai cầu dài5504px, khoảng91.7s đi/55.0s chạy **chưa tính dừng**. Đây là tính toán trên tim đường, chưa đo nhịp chơi trong game; sau duyệt phải kiểm tra quãng đi có thú vị, không nhồi khoảng trống để tăng thời gian.

Bốn vị trí NPC chỉ là ký hiệu quy hoạch; không dùng lại hình khách lịch sử đã bị từ chối để giả là hoàn tất. Sejong thuộc sân học viện; Jang thuộc sân xưởng; Yi thuộc hiên sử liệu; Saimdang thuộc sân hội họa. Giữ đối thoại/quest hiện tại; chỉ mở rộng khi đã duyệt phần tương ứng.

## Kiểm chứng và bước tiếp theo

Kiểm tra vùng đi bộ sơ bộ trên lưới16px:19điểm tiếp cận công trình/NPC đều nối được,0khối nền chồng nhau, không đặt NPC trong khối nhà. Đây **không phải** Forge nav hay kiểm chứng collision cuối. Sơ đồ được mở và xem trực tiếp; chưa có ảnh Phaser của bản đồ đề xuất, vì chưa được phép lắp bản đồ trước duyệt.

Sau khi bạn duyệt phân khu: (1) chốt hình khối/mặt tiền và phong cách tại tỉ lệ Juni; (2) dùng pipeline Forge thực để tạo/chiết props và terrain nguồn, layered bundle, collision/Tiled; (3) lắp bản ứng viên riêng, duyệt một vòng đi bộ hoàn chỉnh; (4) kiểm tra collision, occlusion, cửa, touch/mobile, reduced motion, chụp và quay Phaser; (5) chỉ sau duyệt hình ảnh/gameplay và clean-clone mới chuẩn bị PR vào main. Không merge hay deploy khi chưa có lệnh riêng.

**Cần quyết định lúc này:** duyệt hoặc sửa cấu trúc phân khu, vòng hai cầu, ranh cung thành và quan hệ cửa–sân–đường trên sơ đồ. Không yêu cầu duyệt artwork chưa được tạo.
