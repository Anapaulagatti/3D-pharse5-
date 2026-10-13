# Studio — công cụ 3D

Kho `3D-pharse5-` là Studio độc lập. `Studio/` chứa package xử lý model; `preview/` chứa app Vite/React/R3F. Cài package phát hành qua npm, không clone mã nguồn các framework vào kho.

| Công cụ | Package hoặc ứng dụng | Phiên bản đã kiểm tra | Nguồn chính thức |
|---|---|---|---|
| Three.js | `preview`: `three` | 0.186.1 | https://github.com/mrdoob/three.js |
| React Three Fiber | `preview`: `@react-three/fiber` | 9.8.1 | https://github.com/pmndrs/react-three-fiber |
| Drei | `preview`: `@react-three/drei` | 10.7.9 | https://github.com/pmndrs/drei |
| React / React DOM | `preview`: `react`, `react-dom` | 19.3.0 | https://react.dev/ |
| Blender | Ứng dụng desktop, ngoài npm | 4.3.2 | https://www.blender.org/download/ |
| glTF Transform | `Studio`: `@gltf-transform/cli` | 4.5.1 | https://github.com/donmccurdy/glTF-Transform |
| gltfjsx | `Studio`: `gltfjsx` | 6.5.3 | https://github.com/pmndrs/gltfjsx |
| glTF Validator | `Studio`: `gltf-validator` | 2.0.0-dev.3.10 | https://github.com/KhronosGroup/glTF-Validator |

Validator được ghim vào bản phân phối npm chính thức của Khronos có hậu tố `dev`; React, R3F và Drei dùng bản stable. React 19 tương thích R3F 9 và Drei 10. `npm ls` kiểm tra peer dependencies mà không dùng `--legacy-peer-deps` hoặc `--force`.

## Cài đặt

Node 22.12+ (đã thử Node 24.19.0), npm và Blender có trong PATH. Blender được cài như ứng dụng desktop bình thường, không cài bằng npm. Máy cloud hiện có Blender 4.3.2; không có DISPLAY nên chỉ kiểm tra chế độ nền. Trên máy của bạn, tải ứng dụng từ website chính thức và đặt `BLENDER_BIN` nếu executable không có trong PATH.

Linux/cloud, từ gốc repo:

```sh
bash Studio/scripts/setup.sh
cd preview
npm run dev
```

Windows PowerShell, từ gốc repo:

```powershell
cd Studio
npm ci
# Nếu Blender không nằm trong PATH, chỉnh đường dẫn này theo bản đã cài:
$env:BLENDER_BIN = 'C:\Program Files\Blender Foundation\Blender 4.3\blender.exe'
npm run check:tools
cd ../preview
npm ci
npm run build
npm run dev
```

Cả hai package có `package-lock.json`. Dùng `npm ci` để cài đúng lockfile; không trộn npm/pnpm lockfiles. Tài liệu `REPOS_AND_INSTALL.md` đính kèm giữ nguyên các ví dụ pnpm ban đầu; bản setup này dùng npm với lockfile đã kiểm tra.

## Xử lý model thật

Chạy từ `Studio/`:

```sh
npm run inspect -- ../assets/models/your-model.glb
npm run validate -- ../assets/models/your-model.glb ../quality-reports/your-model-validation.json
npm exec -- gltf-transform optimize --help
npm exec -- gltf-transform optimize ../assets/models/your-model.glb ../exports/your-model.optimized.glb --compress false --texture-compress false --simplify false --flatten false --join false --instance false --palette false
npm run validate -- ../exports/your-model.optimized.glb
npm run gltfjsx -- ../exports/your-model.optimized.glb --types --output .cache/YourModel.tsx
```

Ví dụ chỉ dùng đường dẫn model sau khi file đó thực sự tồn tại. Chọn compression riêng khi runtime đã có decoder; kiểm tra lại material, UV, tên node và animation sau tối ưu. Blender cloud thiếu thư viện Draco tùy chọn; xuất GLB thường đã kiểm tra thành công.

`npm run check:tools` tạo `.blend` và GLB kiểm thử trong `Studio/.cache/smoke/`, inspect, optimize, validate và sinh TSX. Các fixture bị Git ignore và không phải asset thành phẩm. Script nguồn được lưu để tái tạo.

## Kiểm thử trình duyệt

Từ `preview/`:

```sh
npm run test:smoke
```

Cloud dùng `/usr/bin/chromium`. Nếu máy khác chưa có browser cho Playwright, chạy `npm exec -- playwright install chromium`; hoặc đặt `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` tới Chromium của bạn. Test tự khởi động và dừng Vite, chụp ảnh vào `quality-reports/`, và kiểm tra 3D/controls/mobile/fallback/reduced motion/context loss. Chromium SwiftShader chỉ xác minh chức năng; không đại diện FPS trên thiết bị thật.

Không cần backend, biến bí mật hoặc API key. Chỉ tải dependencies qua registry npm. Thực hiện công việc trong checkout này; mỗi cloud task đã được cô lập, không cần tạo Git worktree.
