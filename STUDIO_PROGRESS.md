# Studio progress

- Current milestone: 1 — recovery/audit, then 3 — art direction.
- Current task ID: PIPE-002.
- Last completed task: ENV-001 / audit existing implementation.
- Last verified checkpoint: 0f86ea8; three-direction concept/art checkpoint pushed to GitHub main.
- Last checkpoint time: 2026-10-13 17:24 Asia/Ho_Chi_Minh (UTC+07).
- Latest session: inspected clean checkout and tools; preserved the newly supplied master prompt as STUDIO_MASTER_PROMPT.md; created mandatory recovery records and AGENTS.md.
- In progress: GLB React loading, visual review and browser tests.
- Files: AGENTS.md, STUDIO_MASTER_PROMPT.md, STUDIO_TASKS.md, STUDIO_PROGRESS.md, STUDIO_DECISIONS.md, STUDIO_ASSETS.md.
- Assets / exported GLBs: Arena source GLB 3,417,560 bytes, optimized 3,377,440; mascot source 383,612 bytes, optimized 282,224. Both .blend sources and two 256px textures saved. Six mascot clips and LanternSway exported.
- Installed dependencies: Existing tools reused; @gltf-transform/core/extensions 4.5.1 declared directly (already installed transitively), for scene/clip parity and bounds analysis.
- Successful checks: clean Git status, tool versions, installed executable presence. Baseline TypeScript and Vite build passed in this session.
- Known limits: headless Blender, no physical-phone GPU/FPS testing, optional Blender Draco library absent. No external credentials needed.
- Exact next action: Inspect loaded GLB scene in browser, verify animation poses, fix visible defects, capture posters and transparent portrait.
- Recovery: read all four STUDIO records and AGENTS.md; inspect Git log/status and asset inventory. Continue unfinished task without rerunning setup.

## NEXT SESSION HANDOFF

**Current milestone:** 1 → 3.

**Current task ID:** PIPE-002.

**Last verified checkpoint:** de9c4e0 recovery checkpoint, verified remotely.

**Completed work:** Existing Studio preserved, new requirements and recovery files saved.

**Unfinished work:** Art exploration, real Blender arena/mascot, animation, GLB loading, export QA.

**Files to inspect:** STUDIO_MASTER_PROMPT.md, STUDIO_TASKS.md, preview/src/SceneView.tsx, Studio/scripts/.

**Known blockers:** None external. Initial Validator resource triangle count changed because optimization shared meshes; fixed the parity check to compare every scene node (same 9,786 mascot triangles), bounds and clips. Physical-device FPS remains unverified.

**Exact next command or action:** npm --prefix preview run dev; use Playwright to inspect actual GLBs. Run render-mascot.py for a transparent portrait after the pre-render checkpoint.

**Verification required:** Baseline build and remote checkpoint SHA.

**Remote GitHub save status:** de9c4e0 recovery checkpoint confirmed on origin/main; 0f86ea8 concept checkpoint pushed; modeling source checkpoint is being created before export.
