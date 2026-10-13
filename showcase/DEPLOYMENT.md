# Xuất bản showcase hiện có

Các gói đã chuẩn bị để review. **Chưa bật Pages, chưa chạy workflow và chưa xuất bản công khai.** Cần người dùng chấp thuận trước bước Publish/Deploy. Đẩy checkpoint Git không tự triển khai: workflow chỉ có `workflow_dispatch`, không có trigger `push`.

## GitHub Pages

Sau khi chấp thuận:

1. Mở repo `Anapaulagatti/3D-pharse5-` → **Settings → Pages**.
2. Trong **Build and deployment → Source**, chọn **GitHub Actions**.
3. Mở **Actions → Publish approved v0.2 showcase → Run workflow**, chọn `main` và chạy.
4. Đợi job `deploy` thành công, mở URL trong environment `github-pages` / output `page_url`.

URL dự kiến: `https://anapaulagatti.github.io/3D-pharse5-/`. Đây **chưa phải URL đã deploy/đã xác minh**. Dùng URL thực mà GitHub báo sau khi chạy thành công. Repository/settings/quyền account phải cho phép Pages; nếu lựa chọn này không khả dụng, dùng Cloudflare Direct Upload bên dưới. Không cần công khai toàn bộ source repo để dùng Direct Upload.

Workflow `.github/workflows/showcase-pages.yml` kiểm tra SHA/size của HTML đã lưu, chỉ đưa `index.html` và `.nojekyll` vào artifact. Không chạy Blender, không cài framework, không rebuild model, không đưa source `.blend` hay file cấu hình riêng vào website. HTML tự chứa nên không phụ thuộc đường dẫn root `/models/` và chạy được dưới `/3D-pharse5-/`.

Git read/push trong cloud hoạt động nhưng GitHub API `/repos/.../pages` trả `Forbidden`. Đã lưu cấu hình trong repo; chưa thể bật Pages hoặc chạy Actions qua API ở đây. Không suy ra rằng Git push đồng nghĩa quyền Pages API và không yêu cầu token trong chat.

## Cloudflare Pages — Direct Upload

Sau khi chấp thuận:

1. Tải `downloads/showcase-v0.2-static.zip`.
2. Cloudflare dashboard → **Workers & Pages → Create application → Pages → Direct Upload / Upload assets** (tên nút có thể thay đổi).
3. Chọn tên dự án; upload ZIP hoặc giải nén rồi kéo thư mục chứa `index.html` vào vùng upload.
4. Kiểm tra `index.html` nằm tại gốc site, rồi chọn **Deploy site**.
5. Mở URL `pages.dev` mà dashboard trả về để xem bản tương tác.

Static upload không có build command, preset framework, backend, biến môi trường hoặc API key của ứng dụng. Dùng gói `-static.zip`; không upload gói launcher local. Không cần cài CLI Cloudflare để chuẩn bị gói này.

## Phạm vi công khai và kiểm tra sau deploy

Site công khai chứa showcase, hai GLB tải được, textures/ảnh/animation đã nhúng và license dependencies. URL có thể chia sẻ cho bất kỳ ai. Cần chấp thuận rõ ràng của người dùng.

Sau deploy phải mở URL thực và kiểm tra `200 text/html`, Hanok + mascot, kéo/reset camera, ngày/đêm, sáu animation, giảm chuyển động, WebGL fallback, không có GLB/texture 404 hay lỗi console nghiêm trọng. Kiểm tra nội bộ trước deploy không chứng minh site công khai đã hoạt động. Dừng sau nhiệm vụ này và chờ phản hồi hình ảnh; không dựng district mới.
