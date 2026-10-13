# 3D Studio — Repo cần dùng và setup riêng

> Không `git clone` mã nguồn Three.js/R3F/Drei vào project. Những repo này là mã nguồn tham khảo; cài **package** từ npm trong `preview/` của 3D Studio. Không chạy các lệnh sau trong Korean Arena thật.

## A. Bắt buộc

| Repo chính thức | Vai trò | Cách dùng |
|---|---|---|
| https://github.com/mrdoob/three.js | 3D engine | `pnpm add three` |
| https://github.com/pmndrs/react-three-fiber | React renderer | `pnpm add @react-three/fiber` |
| https://github.com/pmndrs/drei | Loader, helpers, controls, staging | `pnpm add @react-three/drei` |
| https://github.com/vitejs/vite | Preview website tách biệt | Scaffold Vite React TypeScript |

### Lệnh Windows PowerShell

Giải nén thư mục `korean-arena-3d-studio` trước rồi **mở terminal trong thư mục đó**:

```powershell
node --version
pnpm --version

pnpm create vite preview --template react-ts
cd preview
pnpm install
pnpm add three @react-three/fiber @react-three/drei
pnpm add -D @types/three
pnpm dev
```

**Kiểm tra tương thích:** R3F 9 dùng React 19, R3F 8 dùng React 18; dùng stable phù hợp React của **preview**. Không chọn alpha chỉ vì mới.

## B. Dành cho 3D thật: rất nên cài

| Tool | Link | Mục đích |
|---|---|---|
| Blender | https://www.blender.org/download/ | Dựng mesh, UV, rig, keyframes, export `.glb` |
| Blender source | https://github.com/blender/blender | Tham khảo mã nguồn; **không cần clone** |
| glTF Transform | https://github.com/donmccurdy/glTF-Transform | `inspect`, tối ưu GLB, texture compression |
| gltfjsx | https://github.com/pmndrs/gltfjsx | Chuyển GLB thành component R3F khi có nhu cầu |
| glTF Validator | https://github.com/KhronosGroup/glTF-Validator | Validate glTF/GLB, có thể dùng web validator |

Dưới `preview/` nếu Codex cần tối ưu model:

```powershell
pnpm add -D @gltf-transform/cli
pnpm exec gltf-transform inspect ../assets/models/hanok-arena.glb
pnpm exec gltf-transform optimize ../assets/models/hanok-arena.glb ../exports/hanok-arena.optimized.glb --texture-compress webp
```

Đọc `pnpm exec gltf-transform optimize --help` trước khi chọn thông số nén; không dùng Draco/meshopt nếu runtime chưa hỗ trợ decoder. Kiểm chứng animation, UV, material sau khi nén.

Chuyển GLB thành component khi thật sự cần:

```powershell
pnpm dlx gltfjsx ../exports/hanok-arena.optimized.glb --types
```

### Blender

Cài từ website chính thức. Codex có thể viết `bpy` script tạo geometry/mesh/animation, nhưng chỉ được nhận là có file `.blend` hay `.glb` khi thật sự đã tạo và kiểm thử trên máy.

## C. Tùy chọn, cài SAU khi có scene đẹp và đã profiling

- https://github.com/pmndrs/react-postprocessing — bloom/subtle grading khi hardware đủ mạnh.
- https://github.com/pmndrs/postprocessing — effect system.

```powershell
pnpm add @react-three/postprocessing postprocessing
```

Không cần physics engine, navigation mesh, complex shaders, WebGPU alpha, animation library mới, hoặc MMORPG stack ở bản đầu.

## D. Nguồn asset hợp lệ

- https://polyhaven.com/ — HDRI/textures/models CC0; nên dùng chủ yếu cho generic background/lighting.
- https://polyhaven.com/license — quy định CC0.
- https://ambientcg.com/ — kiểm tra license theo asset trước khi dùng.
- https://kenney.nl/assets — kiểm tra quyền của pack cụ thể.

Không lấy ảnh/model ngẫu nhiên từ Google, Pinterest, Sketchfab rồi coi là miễn phí. Không mặc định mọi asset từ Quaternius là CC0; kiểm tra điều kiện cấp phép của từng phiên bản/pack.

## E. Image generation trong Codex

Tham khảo: https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md

Codex có thể dùng image generation nếu skill/tool khả dụng trong môi trường đang chạy. Kiểm tra trước; nếu không có, tiếp tục với procedural 3D/Blender và ghi rõ thiếu phần 2D generated art, không nói rằng đã tạo ảnh.

Mục đích image generation: concept sheet, environment illustration, 2D fallback poster, seamless texture ideas, cut-out sprite. **Không** coi ảnh render thành GLB có mesh/rig.

## F. Không thêm vào repo Korean Arena hiện tại

Toàn bộ lệnh ở file này chỉ áp dụng cho **thư mục Studio**. Sau này muốn tích hợp, chỉ lấy `exports/`, manifest và component API snapshot; không copy package-lock/node_modules hoặc tài liệu nghiên cứu.
