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

## Pipeline asset v0.2 và phục hồi

Các model đã có trong Git; `predev` và `prebuild` chỉ đồng bộ exports vào `preview/public/` bị ignore. Không cần chạy Blender để mở preview.

Từ gốc repo:

```sh
bash Studio/scripts/recover-check.sh
npm --prefix Studio run assets:verify
npm --prefix preview run dev
```

`recover-check.sh` dùng lại dependencies nếu `npm ls --depth=0` hợp lệ, chỉ cài bằng lockfile khi thiếu. Kiểm tra read-only SHA-256/source/clip/Validator, build và 9 browser tests. Report/screenshot tạm vào `Studio/.cache/recovery-browser-reports`, không ghi đè art/report đã commit. Blender, Node, Chromium vẫn là điều kiện trên máy; CLI executable overrides ở phía trên.

Chỉ khi chỉnh model có lý do và đã lưu checkpoint, chạy script tương ứng, từ gốc repo:

```sh
blender --background --factory-startup --threads 4 --python Studio/modeling/arena.py
# hoặc chỉ dựng lại linh vật nếu thay đổi linh vật:
blender --background --factory-startup --threads 4 --python Studio/modeling/mascot.py
npm --prefix Studio run assets:pack
npm --prefix preview run build
npm --prefix preview run test:smoke
```

`assets:pack` giữ topology từng node, bounds và **sampler/keyframe animation chính xác** (`--weld false --resample false --compress false`, không join/flatten/simplify). Validator có thể báo ít tam giác serialized hơn khi dedup chia sẻ mesh; scene-instance counts được so sánh riêng. `assets:build` chỉ dựng GLB/source bị thiếu; không dùng `--regenerate` với art đã duyệt nếu không có lý do.

Để chụp poster linh vật nền trong suốt:

```sh
blender --background --threads 4 --python Studio/modeling/render-mascot.py
npm --prefix Studio run assets:pack
```

Cloud Cycles không có OpenImageDenoise nên render dùng 96 samples và tắt chức năng khử nhiễu không khả dụng. Đây là thiết lập render; không bỏ kiểm tra GLB hay checksum.

## v0.3 candidate recovery

Read the four STUDIO progress files and the latest user review gate first. Do not regenerate approved v0.2 .blend/GLB/PNG files or publish updated art without its required review/authorization. Use the existing checkout and pinned packages; no worktree or reinstall is needed when the snapshot already has them.

Production: `npm --prefix preview run build`, then `npm --prefix preview run preview -- --port 4173` for internal QA. Use `node Studio/scripts/verify-polish-v03.mjs <internal-http-url>`; set `STUDIO_POLISH_REPORT_DIR` when checking the extracted candidate so production proof is retained. A sandbox EPERM/socket denial requires supported execution permission for the same internal server/browser command, not a verification bypass. No cloud user-facing localhost preview is exposed.

Single-file candidate: `node Studio/scripts/build-showcase.mjs --candidate`, then `python3 Studio/scripts/package-polish-v03.py` and `python3 Studio/scripts/audit-polish-v03.py`. This writes showcase-v0.3/downloads/v0.3, preserving the published showcase/ artifact. Do not run the guarded Pages deployment for the candidate until the user approves updated publication.

Real browser video uses the pinned Playwright FFmpeg helper, stored in ignored Studio/.cache/playwright. If that helper alone is missing, run from preview: `PLAYWRIGHT_BROWSERS_PATH=../Studio/.cache/playwright node --use-system-ca node_modules/@playwright/test/cli.js install ffmpeg`. This is the official 2.2 MiB recording helper; it does not change application packages/lockfiles. TLS verification stays enabled. Then run `node Studio/scripts/capture-polish-v03.mjs <internal-http-url>` and `python3 Studio/scripts/finish-capture-v03.py`; inspect extracted video frames before recording visual acceptance. Native system ffmpeg/ffprobe are already installed. Live server/browser processes may need restart in a new cloud task.

## Resume v0.4 Big Update

Read current STUDIO task/progress/decisions/assets and the latest review first. Do not regenerate original assets or deploy unreviewed v0.4. Existing pinned npm dependencies/Blender/Chromium/ffmpeg suffice; no install or new API binding was required. Work in this checkout, no worktree.

Versioned assets are already saved. Read-only validation/metadata: `node Studio/scripts/pack-v04.mjs` verifies 43 baseline files, all native facial reset/limb channels and the new exports; do not rerun when only viewing. Build: `npm --prefix preview run build`. Internal production server: `npm --prefix preview run preview -- --port 4184 --strictPort`, then verify actual HTTP response and run `STUDIO_V04_REPORT_DIR=Studio/.cache/v04-recheck node Studio/scripts/verify-overhaul-v04.mjs <internal-http-url>` only for a new change/failure. No user-facing loopback preview link.

Candidate packaging: `node Studio/scripts/build-overhaul-v04.mjs --candidate`, `python3 Studio/scripts/package-overhaul-v04.py`, `python3 Studio/scripts/audit-overhaul-v04.py`. Writes only separate v0.4 outputs; Pages still pins reviewed v0.3. Native compositor movie: `node Studio/scripts/capture-overhaul-v04.mjs <internal-http-url>`, then `python3 Studio/scripts/finish-capture-v04.py`; inspect decoded frames before marking media inspected. Raw JPEG/timestamps and uncropped video retained. Final codec uses original VFR timing and omits only the asynchronous film-caption strip; no synthetic or accelerated motion. Do not re-run capture after review without reason.

The v0.4 browser harness is the relevant verification for the expanded twelve-clip UI; older six-clip smoke/recording reports remain historical. Restricted sandbox may require supported execution permission for internal Chromium/server sockets. Processes must restart in a new cloud instance; saved files/dependencies are distinct from live processes.
