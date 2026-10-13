# Xuất bản showcase hiện có

Người dùng đã **chấp thuận công khai showcase v0.2 lên GitHub Pages**. Không hỏi lại quyền này. Site chỉ gồm HTML đã hoàn tất và `.nojekyll`; không tái tạo model/app hay công khai nguồn Blender. Workflow hỗ trợ chạy thủ công và tự chạy khi file deployment thay đổi trên `main`; checkpoint chỉ sửa tài liệu không redeploy. Việc có workflow/checkpoint không chứng minh site đã xuất bản: cần URL thực trả `200 text/html` và kiểm tra render.

## Mạng cloud để điều khiển/kiểm tra deployment

Hiện proxy mạng chặn `api.github.com` và `anapaulagatti.github.io` vì hai hostname chưa có trong allowlist. Lỗi CONNECT `403 Forbidden` không phải bằng chứng về quyền tài khoản GitHub; HTTP status của site chưa nhận được. Không gọi đó là site 404 hoặc deployment thành công.

**Kết quả mới sau push:** API/site đã truy cập được. Pages GET/POST hiện trả lỗi origin `403 Resource not accessible by integration`; workflow run `38402363567` thất bại ở `configure-pages` với `Not Found`, deploy skipped. Site đích thực sự trả `404 Site not found`. Cần owner bật Source GitHub Actions theo bước dưới; public deployment chưa thành công.

Đã lưu bổ sung chính xác hai hostname này vào bản nháp môi trường, giữ nguyên preset `package_managers`. Trong **Environment settings**, review/save bản nháp và chọn **Publish environment** để áp dụng. Việc này cho cloud truy cập API/site; không tự bật GitHub Pages hoặc công khai website. Chưa yêu cầu API key/token mới; Git HTTPS auth và biến GH_TOKEN hiện có được giữ nguyên.

## GitHub Pages

Quyền công khai đã có. Nếu Pages chưa bật, dùng tài khoản có quyền quản lý repo:

1. Mở repo `Anapaulagatti/3D-pharse5-` → **Settings → Pages**.
2. Trong **Build and deployment → Source**, chọn **GitHub Actions**.
3. Mở **Actions → Publish approved v0.2 showcase → Run workflow**, chọn `main` và chạy nếu job từ lần push deployment chưa chạy hoặc đã thất bại trước khi bật Pages.
4. Đợi job `deploy` thành công, mở URL trong environment `github-pages` / output `page_url`.

URL dự kiến: `https://anapaulagatti.github.io/3D-pharse5-/`. Đây **chưa phải URL đã deploy/đã xác minh**. Dùng URL thực mà GitHub báo sau khi chạy thành công. Repository/settings/quyền account phải cho phép Pages; nếu lựa chọn này không khả dụng, dùng Cloudflare Direct Upload bên dưới. Không cần công khai toàn bộ source repo để dùng Direct Upload.

Workflow `.github/workflows/showcase-pages.yml` dùng `actions/configure-pages@v5` để đọc Pages đã cấu hình, rồi chạy `Studio/scripts/prepare-pages-site.py`. Script kiểm tra SHA/size, credential patterns, license notices và danh sách output chỉ gồm `index.html`/`.nojekyll`; có file lạ thì dừng, không xóa file để che lỗi. Không chạy Blender/npm build, không đưa `.blend`, `.env`, source map hoặc file cấu hình riêng vào website. HTML tự chứa JS/CSS và GLB/PNG dưới Blob URL nên không phụ thuộc `/models/` tại gốc domain; đường dẫn `/3D-pharse5-/` đã được kiểm tra qua HTTP.

Git read/push trong cloud hoạt động. GET/POST Pages API hiện bị proxy mạng chặn; chưa kiểm tra được quyền API thực. `configure-pages` có tùy chọn enablement nhưng tài liệu v5 yêu cầu token khác GITHUB_TOKEN để tạo site; không thêm token hoặc bật tùy chọn sai quyền. Nếu API vẫn không cho tạo site sau khi mạng đã áp dụng, bật Source **GitHub Actions** thủ công tại `https://github.com/Anapaulagatti/3D-pharse5-/settings/pages` rồi chạy workflow tại `https://github.com/Anapaulagatti/3D-pharse5-/actions/workflows/showcase-pages.yml`.

Nếu Actions bị tắt, kiểm tra **Settings → Actions → General → Actions permissions** để cho phép workflow và official GitHub actions. Workflow đã khai báo `contents: read`, `pages: write`, `id-token: write`; không cần thêm API key vào artifact. Nếu màn hình Pages không cho bật với loại repository/account hiện tại, ghi lại thông báo GitHub; không đổi toàn bộ repo thành public hay đăng sang nhà cung cấp khác khi chưa được chỉ định.

## Cloudflare Pages — Direct Upload

Đây là phương án thay thế đã chuẩn bị từ trước; yêu cầu hiện tại chỉ cho phép GitHub Pages. Không tự chuyển nhà cung cấp:

1. Tải `downloads/showcase-v0.2-static.zip`.
2. Cloudflare dashboard → **Workers & Pages → Create application → Pages → Direct Upload / Upload assets** (tên nút có thể thay đổi).
3. Chọn tên dự án; upload ZIP hoặc giải nén rồi kéo thư mục chứa `index.html` vào vùng upload.
4. Kiểm tra `index.html` nằm tại gốc site, rồi chọn **Deploy site**.
5. Mở URL `pages.dev` mà dashboard trả về để xem bản tương tác.

Static upload không có build command, preset framework, backend, biến môi trường hoặc API key của ứng dụng. Dùng gói `-static.zip`; không upload gói launcher local. Không cần cài CLI Cloudflare để chuẩn bị gói này.

## Phạm vi công khai và kiểm tra sau deploy

Site công khai chứa showcase, hai GLB tải được, textures/ảnh/animation đã nhúng và license dependencies. Quyền công khai v0.2 đã được người dùng cấp. Toàn bộ assets này có provenance project-owned-original; không có model/texture/HDRI/paid font bên thứ ba. Chỉ publish file allowlist; nguồn, tiến độ, cache và private files được giữ trong repo/workspace.

Sau khi URL thực truy cập được, chạy kiểm tra browser công khai:

```sh
STUDIO_HTTP_TARGET_SCOPE=public STUDIO_HTTP_REPORT_DIR=quality-reports/pages-live node Studio/scripts/verify-preview-http.mjs public=https://anapaulagatti.github.io/3D-pharse5-/
```

Sau deploy phải mở URL thực và kiểm tra `200 text/html`, Hanok + mascot, kéo/reset camera, ngày/đêm, sáu animation, giảm chuyển động, WebGL fallback, không có GLB/texture 404 hay lỗi console nghiêm trọng. Kiểm tra nội bộ trước deploy không chứng minh site công khai đã hoạt động. Dừng sau nhiệm vụ này và chờ phản hồi hình ảnh; không dựng district mới.
