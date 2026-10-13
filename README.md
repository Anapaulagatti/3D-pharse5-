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

Demo hiện có sân hanok và linh vật gốm dạng hình học thủ tục, điều khiển góc nhìn/chất lượng/ánh sáng, giảm chuyển động, khung điện thoại và fallback SVG. Đây là nền tảng để phát triển theo master prompt; chưa hoàn thành các giai đoạn sản xuất art, animation và `exports/v1/`. Manifest giữ trống vì chưa có asset thành phẩm.
