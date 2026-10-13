# Studio → Korean Arena: EXPORT CONTRACT (sau này, không tích hợp hiện tại)

**Đây là hợp đồng xuất file, không phải hướng dẫn sửa repo Korean Arena.** Codex chỉ xuất asset và preview. Chủ project sẽ tự quyết định khi nào tích hợp.

## Final export shape

```text
exports/
  v1/
    models/
      arena-hero.glb
      mascot-base.glb
      learning-alley.glb
      celebration.glb
    posters/
      arena-desktop.webp
      arena-mobile.webp
      mastery-map.webp
      victory.webp
    textures/
      ...
    asset-manifest.json
    integration-notes.md
    performance-report.md
    licenses.md
```

Không ép phải có mọi file ở v1 nếu chưa được dựng thật; thiếu phải ghi trong manifest.

## Asset naming / transforms

- Files: lower-kebab-case, UTF-8, stable names.
- Mesh scale convention: 1 unit = ~1 meter equivalent, central origin at world floor, Y up. Document exceptions.
- Export `.glb` with stable mesh/animation names (`Idle`, `Celebrate`, `Ready`, `GentleLoss` where available).
- Freeze appropriate transforms before export; keep Blender source file separately.
- Record animation length, camera framing/origin, texture decoder requirements and color space.

## Assets and licensing

Per exported asset record:

```json
{
  "id": "mascot-base",
  "type": "glb",
  "file": "models/mascot-base.glb",
  "version": "1.0.0",
  "origin": "original-procedural",
  "license": "project-owned-original",
  "source_url": null,
  "source_file": "../../assets/source-blend/mascot-base.blend",
  "dimensions": null,
  "file_bytes": null,
  "animations": ["Idle"],
  "dependencies": [],
  "checksum_sha256": null,
  "verified": false
}
```

Populate real fields after export; never fake asset size, GLB existence or validation status.

## Preview contract

- Independent Vite preview uses DEMO fixtures only.
- Preview route/select lets reviewer switch hero, mastery, mascot, celebration, desktop/mobile, reduced motion, low quality.
- No Supabase, login, SEO, TOPIK exam code, rewards, API keys, user records or QR support implementation in Studio.

## Future integration handoff

Provide a proposed rendering API only, for example:

```ts
type SceneQuality = 'low' | 'medium' | 'high';
type ArenaVisualProps = {
  mode: 'idle' | 'matchmaking' | 'win' | 'lose';
  quality?: SceneQuality;
  reducedMotion?: boolean;
};

type MasteryVisualNode = {
  id: string;
  label: string;
  state: 'locked' | 'current' | 'completed';
};
```

The real application owns the data and may change this contract when integration begins. Studio does not assume knowledge of existing production props or package versions.

## Performance acceptance targets (targets, not guarantees)

- hero scene GLB compressed target: <= 4 MB; mascot GLB target: <= 1 MB.
- assets should stream/lazy-load; no WebGL required for core UX.
- mid-range mobile: aim for 30 FPS, desktop: aim for >= 50 FPS in representative scenes, measure not assume.
- mobile low mode target: modest pixel ratio 0.75–1.25 and simplified effects.
- all scenes: poster fallback; reduced motion: no looping decorative movement.
- GLB passes Khronos validation, and render/animation parity is checked after optimization.

## Final acceptance

- Include actual files, not paths to nonexistent files.
- Preserve original editable `.blend` or procedural script where it exists.
- Export with license/provenance manifest and screenshots.
- Do not touch the production Korean Arena repository.
