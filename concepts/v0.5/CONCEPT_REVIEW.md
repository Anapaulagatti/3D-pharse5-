# Gate A — Ba hướng nhân vật v0.5

**ĐÃ DUYỆT A — Nari.** Người dùng: “nếu bạn đề xuất là A thì hãy chọn A”. Xem APPROVAL.json. Phần so sánh bên dưới được giữ như hồ sơ thiết kế ban đầu.

![Ba concept nhân vật Joseon Fantasy](character-concepts.png)

Đây là hình thiết kế gốc tạo bằng image_gen từ mô tả riêng, không dùng ảnh tham chiếu của trò chơi khác. Hình không phải model 3D, rig, ảnh chụp ứng dụng hay bằng chứng chuyển động. Tên là tên làm việc của nhân vật hư cấu; trang phục là diễn giải fantasy lấy cảm hứng Joseon, không tự nhận phục dựng lịch sử.

## A — Nari, người đưa thư hanji — đề xuất

Một người đưa thư trẻ, nhanh nhẹn, đưa những lá thư giấy đến ngôi nhà học trong sân Hanok. Áo jeogori màu ngà, lớp áo ngắn men ngọc, quần baji xanh mực, nơ coral, búi tóc thấp với ghim giấy gấp và túi thư nhỏ sát hông. Dáng áo ngắn tạo tam giác phía trên; chân và khuỷu tay dễ đọc khi chạy hoặc nhảy. Tính cách cởi mở, tò mò và có chút tinh nghịch.

- Điểm nhận diện: ghim hanji lệch, nơ coral nhỏ và túi thư phẳng; không cần vũ khí hay hiệu ứng liên tục.
- Diễn xuất: nhìn sang người chơi rồi vẫy chào; giữ túi khi bắt đầu chạy; mở lá thư khi suy nghĩ; mừng bằng bước nhún có chân trụ rõ ràng.
- Sản xuất: ưu tiên khối thân liên tục có skin weights, vai/khuỷu/gối/cổ chân thực; áo ngắn và tay gọn giảm nguy cơ xuyên vải. Hạ độ phồng quần so với tranh để gối và nhịp chân vẫn rõ ở camera gameplay.
- Rủi ro cần xử lý: dây túi xuyên vai khi giơ tay; túi che bàn tay; chân bị quần quá rộng che khuất. Túi gắn vào pelvis, chuyển động phụ có giới hạn; giảm chi tiết dệt nhỏ khi dựng model.

**Lý do đề xuất:** công việc đưa thư tạo động cơ khám phá tự nhiên; trang phục hỗ trợ đi/chạy/nhảy và nhận diện từ xa, đồng thời có chi phí rig/vải thấp nhất trong ba hướng. Đây là đề xuất, không phải quyết định thay người dùng.

## B — Yun, học giả tập sự

Một học giả trẻ với chiếc mũ vải góc cạnh lấy cảm hứng jeongjagwan, áo dài màu ngà có nẹp men ngọc và tà xẻ, thắt lưng xanh mực, hai cuốn sách nhỏ. Silhouette cao và thẳng, mũ rộng hình chữ nhật; vẻ điềm đạm và tập trung khác rõ với A.

- Điểm nhận diện: mũ xếp vải, tà áo dài và sách; kết nối trực tiếp với hành trình học tiếng Hàn.
- Diễn xuất: ngừng lại quan sát cửa sổ; nghiêng đầu, nhíu mày, đưa tay lên cằm; vui mừng từ sự rụt rè ban đầu.
- Sản xuất: tà áo phải chia thành các vùng skinning có kiểm soát, có xẻ trước/bên để bước chân đọc rõ. Sách được cất vào đai trong locomotion thay vì khóa một tay ở mọi animation.
- Rủi ro: áo dài che bước chân; khuỷu tay xuyên tay áo; cần thêm xương tà áo và kiểm tra từ sau/bên. Không dùng mô phỏng vải nặng ở runtime.

## C — Dam, người giữ sân đèn lồng

Một người giữ sân có dáng chắc và thân thiện, mũ tre rộng với vành tròn lấy cảm hứng satgat, áo xanh mực, vai áo men ngọc và quần coral ngắn. Đèn hanji nhỏ gắn sát đai. Khối mũ tròn và vai rộng tạo silhouette thấp, khỏe; tính cách bao dung, vui nhộn, chào đón người mới.

- Điểm nhận diện: vành tre rộng, khối chân chắc và đèn lồng nhỏ; dễ liên hệ với sân đêm.
- Diễn xuất: mở bàn tay mời vào nhà; cúi kiểm tra đèn; tiếp đất có trọng lượng; vui mừng bằng động tác tay và chuyển trụ rõ.
- Sản xuất: mũ là mesh cứng gắn đầu; vành cần đủ cao để không che mặt ở camera; đèn có chuyển động phụ ngắn và bị giới hạn.
- Rủi ro: mũ che mặt trong góc cao hoặc va cửa; đèn xuyên tay; tốn thêm silhouette/texture/material nếu không gom atlas. Bản model sẽ giảm hoa văn nhỏ và độ rộng mũ khi cần.

## So sánh sản xuất

Điểm 1–5 là đánh giá art/production sơ bộ từ concept, **không phải kết quả benchmark, user test hay chất lượng rig đã được đo**. Điểm cao ở độ phức tạp trang phục và chi phí web nghĩa là dễ sản xuất/nhẹ hơn.

| Tiêu chí | A · Nari | B · Yun | C · Dam |
|---|---:|---:|---:|
| Silhouette đọc ở kích thước nhỏ | 5 | 4 | 5 |
| Tính riêng của thiết kế | 4 | 4 | 4 |
| Sức hút khuôn mặt | 5 | 4 | 5 |
| Bản sắc văn hóa Hàn | 4 | 5 | 4 |
| Khả năng đi/chạy/nhảy rõ | 5 | 3 | 4 |
| Độ đơn giản của trang phục | 5 | 3 | 3 |
| Chi phí render/animation trên web | 5 | 3 | 3 |
| Tiềm năng nhân vật chính lâu dài | 5 | 4 | 4 |
| Tổng sơ bộ /40 | **38** | **30** | **32** |

| Ước lượng ban đầu, chưa đo | A | B | C |
|---|---|---|---|
| Hình học mục tiêu | 18–24k tam giác | 22–28k | 20–26k |
| Xương deform mục tiêu | 28–34 | 32–38 | 30–36 |
| Material draw mục tiêu | ≤4 | ≤4 | ≤4 |
| Phụ kiện phụ | Dây/ghim/túi, giới hạn nhỏ | Tà áo và mũ vải | Mũ cứng, đèn sát đai |

Tỷ lệ cuối dự kiến khoảng4.75–5 đầu, chiều cao gameplay1.45m. Tranh có thể có nhiều nếp vải/hoa văn hơn model thực; chỉ giữ những chi tiết đọc được ở camera gameplay. Cả ba hướng phải đạt cùng yêu cầu giải phẫu/khớp và biểu cảm, không chọn cách ghép các chi rời để thay thế skinning.

## Quyết định cần từ người dùng

Chọn **A, B hoặc C**, kèm điều chỉnh nếu muốn. Gate A chưa được thông qua chỉ vì có hình concept hoặc điểm đề xuất. Sau khi chọn, ghi nguyên phản hồi và trạng thái APPROVED vào hồ sơ trước khi dựng nhân vật cuối. Không công bố v0.5 từ bước này.

Kế hoạch Hanok và các gate kế tiếp: [ARCHITECTURE_REBUILD_PLAN.md](../../docs/v0.5/ARCHITECTURE_REBUILD_PLAN.md). Audit và checkpoint: [AUDIT.md](../../quality-reports/v0.5/AUDIT.md).
