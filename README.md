# Korean Arena 3D Studio — DỰ ÁN ĐỘC LẬP

Đây là **workspace 3D riêng** cho Codex. Không phải một phần của repo Korean Arena đang ở Phase 3. Không cần truy cập, clone, cài dependency vào, hay sửa bất cứ tệp nào ở Korean Arena thật.

## Cách dùng

1. Giải nén thư mục này tại một nơi khác với Korean Arena hiện tại; ví dụ `D:\Projects\korean-arena-3d-studio`.
2. Mở thư mục **riêng** này bằng VS Code/Codex.
3. Đọc `REPOS_AND_INSTALL.md` để biết cần cài gì (có thể cho Codex tự setup bên trong thư mục này).
4. Copy toàn bộ `CODEX_MASTER_PROMPT.md` vào Codex và giao nhiệm vụ làm theo từng gate.
5. Chạy bản demo độc lập của 3D Studio, xem scene và asset trực tiếp tại local preview của Studio.
6. **Không** đưa bất cứ file nào vào Korean Arena thật cho đến khi bạn tự quyết định việc tích hợp sau này.

## Tài liệu

| File | Mục đích |
|---|---|
| `CODEX_MASTER_PROMPT.md` | Master prompt Codex: art direction → original assets → Blender/GLB → preview → QA → export |
| `REPOS_AND_INSTALL.md` | Link repo chính thức và lệnh cài trong **Studio riêng** |
| `ART_DIRECTION.md` | Concept độc quyền, thế giới 3D, mascots, ánh sáng, vật liệu, màu, độ khác biệt |
| `EXPORT_CONTRACT.md` | Chuẩn đặt tên, metadata, GLB/texture/poster, manifest để sau này mang sang web |
| `ASSET_MANIFEST.csv` | Template kiểm soát nguồn/license/phiên bản cho từng asset |

## Cấu trúc dự kiến

```text
korean-arena-3d-studio/
├── CODEX_MASTER_PROMPT.md
├── REPOS_AND_INSTALL.md
├── ART_DIRECTION.md
├── EXPORT_CONTRACT.md
├── ASSET_MANIFEST.csv
├── concepts/             # concept/moodboard tự tạo
├── assets/
│   ├── source-blend/    # file .blend gốc, mesh/rig có thể chỉnh sửa
│   ├── models/          # GLB working builds
│   ├── textures/        # texture bản có quyền dùng
│   ├── posters/         # fallback 2D / hero images
│   └── animations/      # nguồn animation
├── preview/             # Vite React/R3F được Codex dựng **trong Studio này**
├── exports/             # bản giao hàng cuối cùng, không chứa dependency npm
└── quality-reports/     # ảnh/chụp màn hình/báo cáo hiệu năng
```

## Điều kiện bất di bất dịch

- Không truy cập repo Korean Arena, không cần chờ Claude, không làm song song trên cùng file.
- Không đưa `node_modules`, source các framework clone về, hay toàn bộ preview app vào bản export để tích hợp.
- Không yêu cầu người dùng mua asset.
- Ảnh AI 2D không phải mesh/GLB 3D. Deliverable phải có **model 3D thực** hoặc geometry Three.js rõ ràng.
- Korean Arena hoàn toàn miễn phí; QR ủng hộ là việc của web chính, không thuộc Studio 3D.

## Bản nền tảng đã thiết lập trong `3D-pharse5-`

Kho này giữ tài liệu gốc và cấu trúc thư mục phía trên, đồng thời thêm `Studio/` cho glTF Transform, gltfjsx, Validator và các script kiểm tra Blender. Dependencies giao diện nằm trong `preview/`.

```sh
# Từ gốc repo, với Node 22.12+, npm và Blender trong PATH:
bash Studio/scripts/setup.sh
cd preview
npm run dev
```

Hướng dẫn Windows, phiên bản package và xử lý GLB: [Studio/README.md](Studio/README.md). Kết quả kiểm tra và ảnh demo thực tế: [quality-reports/SETUP_REPORT.md](quality-reports/SETUP_REPORT.md).

## Living Hanok v0.3 — đã xuất bản

[**Xem bộ ảnh trước/sau và hướng dẫn review**](quality-reports/v0.3/REVIEW.md) · [Video chuyển động thật 42 giây](quality-reports/v0.3/living-hanok-motion.mp4) · [Tải gói tương tác v0.3](downloads/v0.3/living-hanok-v0.3-review.zip).

**Xem v0.3 tương tác online:** [https://anapaulagatti.github.io/3D-pharse5-/](https://anapaulagatti.github.io/3D-pharse5-/). GitHub Actions đã triển khai đúng HTML đã duyệt; 11 kiểm tra browser công khai đạt, và ảnh render thật đã được xem. [Bằng chứng triển khai](quality-reports/v0.3/pages-release/VISUAL_REVIEW.md). Nguồn và assets v0.2 giữ nguyên. Gói ZIP vẫn dùng được qua START_WINDOWS.cmd hoặc python3 start.py. Chưa đo FPS phần cứng/điện thoại thật; dừng chờ phản hồi, không có district mới.

## Golden slice v0.2.0 — bản lưu

Website hiện dùng v0.3 ở phần trên. Source/artifact/ZIP và [bằng chứng website v0.2 trước đây](quality-reports/pages-live/VISUAL_REVIEW.md) vẫn được giữ để khôi phục.

**Xem bản tương tác qua HTTP trên máy cá nhân:** tải [showcase-v0.2-http.zip](downloads/showcase-v0.2-http.zip), giải nén; Windows mở `START_WINDOWS.cmd`, macOS/Linux chạy `python3 start.py` trong thư mục đã giải nén. Trình duyệt tự mở app. Cần Python 3; không cần Node/Blender. Mở HTML trong ChatGPT/Codex/GitHub chỉ hiện source. Xem [hướng dẫn từng bước](showcase/README.md); [gói static](downloads/showcase-v0.2-static.zip) và [cấu hình Pages](showcase/DEPLOYMENT.md) vẫn được giữ để khôi phục/triển khai.

Preview hiện tải **GLB thật từ Blender**: mái hanok cong, khung gỗ/hanji, sân gốm, vườn mận, cầu, đèn giấy có animation và skyline thu nhỏ. Linh vật Ceramic Seed Spirit có sáu clip: Idle, Happy, Thinking, Celebration, Disappointed, Greeting. Có điểm khám phá, camera reset, day/evening/night, Low/Med/High, giảm chuyển động, khung điện thoại, thông tin/tải asset và fallback bằng ảnh render thật (SVG dự phòng nếu ảnh lỗi).

Nguồn `.blend` ở `assets/source-blend/`, script tái tạo ở `Studio/modeling/`, bản xuất/manifest ở `exports/v1/`. Không cần tái tạo model để chạy app:

```sh
cd preview
npm run dev
```

Kiểm tra hoặc phục hồi dependencies **chỉ khi thiếu**, không dựng lại art:

```sh
bash Studio/scripts/recover-check.sh
```

Build/TypeScript và 9 kiểm thử trình duyệt đã đạt. Hai GLB có 0 lỗi/0 cảnh báo Validator; topology, bounds và toàn bộ sampler animation được giữ sau tối ưu. Sáu pose khác nhau và raw/optimized Celebration render giống từng pixel trong kiểm tra deterministic. Xem [QA_CHECKLIST.md](QA_CHECKLIST.md) và [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md) cho phạm vi và giới hạn đo đạc.

## Tiếp tục sau gián đoạn

Đọc [STUDIO_PROGRESS.md](STUDIO_PROGRESS.md), [STUDIO_TASKS.md](STUDIO_TASKS.md), [STUDIO_DECISIONS.md](STUDIO_DECISIONS.md), [STUDIO_ASSETS.md](STUDIO_ASSETS.md) và `AGENTS.md` trước khi làm. Yêu cầu mới nhất được lưu trong `STUDIO_MASTER_PROMPT.md`. Kiểm tra Git status/log và tiếp tục task chưa xong; không khởi động lại setup hoặc tạo lại concept/model đã có.

Đây là bản đầu của arena + mascot, chưa phải toàn bộ thế giới. Sáu khu học tập và benchmark GPU/FPS trên thiết bị thật còn nằm trong checklist. Không có tích hợp vào Korean Arena production.
