# V4 toolkit readiness

Verified2026-10-15 in actual cloud instance. Existing packages reused, no dependency/lock changes or unrelated installations.

| Tool | Observed status / proof |
| --- | --- |
| Node24.19.0 / npm11.9.0 | Version commands and npm ls pass |
| Phaser4.2.1 / TS5.9.3 / Vite8.3.4 | Retained exact lock; typecheck and production build executed |
| Vitest5.0.4 | Original5unit tests pass |
| Playwright1.64.1 / Chromium154 | Installed; real browser flows and V4 visual checks recorded at Gate2 |
| Python3 / Pillow12.3.0 | Import/version smoke passes; original pixel PNG/atlas pipeline executed |
| ffmpeg7.1.5 | Version available; actual capture encoding verified at Gate2 |
| Tiled GUI | Not installed, no GUI session; no claim tested |
| Tiled headless replacement | Versioned orthogonal JSON exported, collisions/source checked, loaded by actual Phaser at Gate2 |
| LibreSprite GUI | Not installed; no claim tested |
| Editable replacement | Per-layer/frame RGBA PNG + deterministic raster exporter, atlas/source equality check; smoke-tested |
| Lint/format/CI | Existing ESLint/Prettier/read-only GitHub workflow retained; final Gate2 results recorded separately |
| Backend/ad provider | Intentionally absent; later approved gates only |

The active branch already excludes Three/R3F/Drei/GLB/Blender toolchain. Frozen showcase-v0.5 is a release hold, not the active app. No further obsolete files were deleted. Independent fresh HTTPS archive clone2738hashes PASS at Gate0. package-lock unchanged. Asset setup must validate without regenerating sources.
