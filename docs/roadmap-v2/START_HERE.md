# Chơi thử candidate V2

Trạng thái: **READY_FOR_OWNER_REVIEW**. Đã hoàn thành bản chơi cục bộ; **PENDING_OWNER_APPROVAL** cho đúng bản public mới. Không nói đã hoàn tất mọi tính năng roadmap.

Tải `ROADMAP_V2_PLAYABLE_REVIEW.zip` (~201MB), giải nén rồi chạy:

```bash
python3 start-review.py
```

Mở `http://127.0.0.1:4483/review/`. Python3 là điều kiện duy nhất; không cần npm, tài khoản hoặc Internet. Launcher kiểm hash toàn bộ tệp trước khi phục vụ và không liệt kê thư mục. Để xem lại game nền hiện đang public, mở https://anapaulagatti.github.io/3D-pharse5-review/play/ — **đó là bản1a cũ, chưa có các bổ sung V2**.

1. Chọn Juni/nhân vật đã duyệt; vào thế giới bình thường. WASD/phím mũi tên, Shift chạy, E tương tác. Điện thoại giả lập xoay ngang dùng joystick và nút tương tác; I túi, J nhật ký;1/2/3 công cụ.
2. Gặp Cheolsu tại farm để nhận quest/hạt thật. Đến ô đất, làm đất → chọn hạt → gieo → tưới → chờ cây lớn → thu hoạch. Nhật ký chỉ theo dõi, không xử lý farm từ xa.
3. Hoàn thành quest đầu mở cà rốt/bắp cải; mua/bán ở Minseo và hoàn thành quest chợ để mở thêm8loài. Mỗi36ô có state/timestamp riêng; cây chưa tưới không tự lớn. Thời gian thường45–300giây; crop giới thiệu của quest có một chu kỳ ngắn, không phải chế độ tăng tốc toàn game.
4. Đi tới cửa Minseo `(717,2605)`, Jiho `(1128,2605)`, Eunji `(1418,2605)`. E/tap để vào phòng Phaser thật, đi bên trong, giao dịch/tìm mảnh/ghép bảng/giao sách. Ra cửa dưới để quay về đúng vị trí ngoài trời. Refresh để thử lưu/khôi phục trong phòng.
5. Làm chuỗi8bước liên kết: ghé shop → lấy3mảnh tại workshop/bookshop/shop → ghép책 → nhận tuyến → tìm địa chỉ → giao tại bookshop → trả lời tiếng Hàn. Thử trả lời sai/ghép sai rồi sửa; thưởng cơ bản chỉ một lần. Tuyến giao hiện không giới hạn thời gian để dễ tiếp cận.
6. Gallery có video farm6phút10giây từ khởi đầu bình thường và video nội thất2phút19giây. Video không audio/không tăng tốc; PNGnative1:1 dùng soi pixel. Ảnh DPR2/3 được ghi rõ là ảnh bố cục trình duyệt.

Review riêng `?qa&entry=farm`/`?qa&entry=retail` dùng kho localStorage riêng; không ghi đè tiến độ chơi bình thường. Không đồng bộ website học tiếng Hàn. Art crop/nội thất mới và tiếng Hàn **chờ người duyệt**; thiết bị Android/iPhone/GPU vật lý **NOT TESTED**.

Một quyết định owner cuối cần duyệt đúngmanifest744tệp và cách lưu lịch sử trong Git trước khi cập nhật Pages. Xem OWNER_REVIEW.html. Không có yêu cầu duyệt từng vật trang trí hay26giấy phép mới.
