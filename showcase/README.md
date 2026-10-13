# Xem showcase v0.2 trong trình duyệt

Mở file trong ChatGPT/Codex hoặc trang mã nguồn GitHub sẽ hiện **mã HTML**. Đó là trình xem file, không phải một website đang chạy. Cách dùng ở đây là phục vụ `index.html` qua HTTP với kiểu nội dung `text/html`.

## Windows

1. Tải `downloads/showcase-v0.2-http.zip` và chọn **Extract All / Giải nén tất cả**.
2. Mở thư mục `Korean-Arena-Showcase-v0.2`, nhấp đúp **START_WINDOWS.cmd**.
3. Trình duyệt mặc định tự mở ứng dụng 3D. Giữ cửa sổ terminal mở trong lúc xem; nhấn Ctrl+C để dừng.

Cần Python 3 trên máy tính. Nếu chưa có, cài từ https://www.python.org/downloads/ hoặc Microsoft Store rồi chạy lại. Không cần Node, Blender, npm hoặc mạng sau khi đã tải gói.

## macOS / Linux

Giải nén gói, mở terminal trong thư mục `Korean-Arena-Showcase-v0.2`, rồi chạy:

```sh
python3 start.py
```

Trình duyệt tự mở bản render qua HTTP trên **chính máy đó**. Nếu không tự mở, sao chép địa chỉ mà terminal in ra vào Chrome/Edge/Firefox trên cùng máy. Nếu cổng 8080 đang được dùng, launcher tự chọn cổng trống. Không chạy launcher bên trong ZIP chưa giải nén.

## Xem online

Gói `downloads/showcase-v0.2-static.zip` chứa `index.html` tại gốc, sẵn sàng cho static hosting. Xem [DEPLOYMENT.md](DEPLOYMENT.md) để dùng GitHub Pages hoặc Cloudflare Pages. Chưa xuất bản công khai; cần người dùng chấp thuận trước. GitHub blob/raw là nơi xem/tải source, không phải URL của app.

Môi trường onboarding này không cung cấp URL browser preview/port forwarding cho người dùng. Server cloud chỉ dùng kiểm tra nội bộ; địa chỉ loopback của cloud không truy cập được từ máy bạn. GitHub API trả `Forbidden`; Git read/push vẫn hoạt động, nên bật Pages cần thực hiện qua giao diện GitHub.

## Nội dung và kiểm tra

HTML tự chứa khoảng 7.15 MiB: chính app React/R3F hiện có, JavaScript/CSS, hai GLB từ Blender, textures, sáu animation và ảnh fallback thật. Các GLB tải xuống giữ đúng checksum của `exports/v1/`. License dependencies nằm trong HTML. Không có model/khu học tập mới.

Kiểm tra browser HTTP và ảnh render được lưu trong `quality-reports/preview-access/`. Báo cáo phân biệt bản Vite production, gói HTML qua HTTP và đường dẫn con giống GitHub Pages. Mở file qua `file://` trong Chromium cloud vẫn bị chính sách quản trị chặn; hướng dẫn này dùng HTTP. GPU/điện thoại thật chưa được đo FPS; xem `PERFORMANCE_REPORT.md`.

Để đóng gói lại **HTML đã có** sau khi sửa hướng dẫn/launcher:

```sh
python3 Studio/scripts/package-showcase.py
```

Chỉ khi sửa app/export, dùng `npm --prefix Studio run showcase:build` rồi kiểm tra lại. Không tái tạo model để mở showcase.
