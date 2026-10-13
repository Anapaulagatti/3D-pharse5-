# Studio progress

- Current milestone: 1 — recovery/audit, then 3 — art direction.
- Current task ID: ARENA-001.
- Last completed task: ENV-001 / audit existing implementation.
- Last verified checkpoint: 0f86ea8; three-direction concept/art checkpoint pushed to GitHub main.
- Last checkpoint time: 2026-10-13 17:08 Asia/Ho_Chi_Minh (UTC+07).
- Latest session: inspected clean checkout and tools; preserved the newly supplied master prompt as STUDIO_MASTER_PROMPT.md; created mandatory recovery records and AGENTS.md.
- In progress: Blender arena and mascot source scripts.
- Files: AGENTS.md, STUDIO_MASTER_PROMPT.md, STUDIO_TASKS.md, STUDIO_PROGRESS.md, STUDIO_DECISIONS.md, STUDIO_ASSETS.md.
- Assets / exported GLBs: Three-direction concept sheet saved under concepts/. No production GLBs yet.
- Installed dependencies: none in this session; reuse pinned React/R3F/Drei/Three, Blender and CLI tools.
- Successful checks: clean Git status, tool versions, installed executable presence. Baseline TypeScript and Vite build passed in this session.
- Known limits: headless Blender, no physical-phone GPU/FPS testing, optional Blender Draco library absent. No external credentials needed.
- Exact next action: Run blender --background --factory-startup --threads 4 --python Studio/modeling/arena.py, then mascot.py; inspect failures and validate actual outputs.
- Recovery: read all four STUDIO records and AGENTS.md; inspect Git log/status and asset inventory. Continue unfinished task without rerunning setup.

## NEXT SESSION HANDOFF

**Current milestone:** 1 → 3.

**Current task ID:** ARENA-001.

**Last verified checkpoint:** de9c4e0 recovery checkpoint, verified remotely.

**Completed work:** Existing Studio preserved, new requirements and recovery files saved.

**Unfinished work:** Art exploration, real Blender arena/mascot, animation, GLB loading, export QA.

**Files to inspect:** STUDIO_MASTER_PROMPT.md, STUDIO_TASKS.md, preview/src/SceneView.tsx, Studio/scripts/.

**Known blockers:** None for implementation; physical-device performance remains unverified.

**Exact next command or action:** blender --background --factory-startup --threads 4 --python Studio/modeling/arena.py; then Studio/modeling/mascot.py.

**Verification required:** Baseline build and remote checkpoint SHA.

**Remote GitHub save status:** de9c4e0 recovery checkpoint confirmed on origin/main; 0f86ea8 concept checkpoint pushed; modeling source checkpoint is being created before export.
