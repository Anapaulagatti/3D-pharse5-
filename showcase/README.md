# Mở showcase thực tế

Tải **index.html** trong thư mục này về máy, giữ đuôi `.html`, rồi mở bằng Chrome hoặc Edge trên máy tính. Nếu trình duyệt mở trang mã nguồn GitHub, chọn **Download raw file** trước. Không cần Node, Blender, package hoặc mạng sau khi tải.

File khoảng 7.15 MiB chứa chính app React/R3F trong `preview/`, JavaScript/CSS, hai GLB thật từ Blender, textures và ảnh dự phòng. Có sân hanok, linh vật, sáu animation, camera/điểm khám phá, ánh sáng ngày/chiều/đêm, chất lượng và tải model GLB. Các nút tải xuất đúng bytes của `exports/v1/`, với tên `arena-hero.glb` và `mascot-base.glb`. Giữ nguyên toàn bộ file; không chỉ sao chép phần HTML trước script. License dependencies được nhúng trong HTML.

Nếu trình duyệt công ty chặn file cục bộ, dùng bản app trong `preview/` hoặc phục vụ thư mục này qua HTTP. Từ gốc repo, với Python:

```sh
python3 -m http.server --bind 127.0.0.1 --directory showcase 8080
```

Mở địa chỉ HTTP mà terminal in ra trên chính máy đang chạy lệnh. Giao diện onboarding cloud không cung cấp đường dẫn preview tương tác cho người dùng.

## Phạm vi kiểm tra

- Nội dung HTML đã được kiểm tra trong Chromium 154 ở trang `about:blank` khi mạng offline, không có server: 3D thật, giao diện desktop/390×844, sáu clip, playback/pause, POI/chất lượng/ánh sáng, tải hai GLB đúng checksum, hai PNG fallback, 0 request bên ngoài và 0 lỗi JavaScript.
- Điều hướng `file://` trong Chromium cloud bị chính sách quản trị chặn (`ERR_BLOCKED_BY_ADMINISTRATOR`). Không thay đổi chính sách và không tính kiểm tra đó là đạt. Cách mở file trực tiếp trên Chrome/Edge cá nhân chưa được xác minh trong môi trường này.
- Ảnh từ chính HTML: `quality-reports/showcase-desktop.png`, `showcase-mascot.png`, `showcase-mobile.png`, `showcase-fallback.png`; chi tiết: `quality-reports/showcase-offline.json`.
- Tốc độ GPU/điện thoại thật vẫn chưa được đo; xem `PERFORMANCE_REPORT.md`. Nếu thiếu WebGL, file hiển thị ảnh render thật và giữ các điều khiển.

## Tạo lại sau khi sửa app

Từ gốc repo, dùng dependencies đã có trong `preview/`; không tái tạo model:

```sh
npm --prefix preview run typecheck
npm --prefix Studio run showcase:build
npm --prefix Studio run showcase:verify
```

`showcase:build` kiểm tra checksum của bảy export trước khi nhúng, dùng Vite/plugin-react đã ghim trong preview và chỉ tạo `index.html` + `build-info.json`. Build offline thay đường dẫn asset bằng Blob URL; preview phục vụ qua HTTP vẫn dùng đường dẫn thông thường và lazy loading. Khi cập nhật app/export, cần build lại bản HTML này. Không đặt bản app đóng gói vào `exports/v1/`, vốn là gói asset để tích hợp.
