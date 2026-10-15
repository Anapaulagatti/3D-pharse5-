# Verified toolchain

Environment: Codex cloud container, Debian13, Node24.19.0/npm11.9.0, Python/Pillow12.3.0; no DISPLAY or desktop GUI. Existing system Chromium, ffmpeg/ffprobe used. No host desktop installation claimed.

Phaser4.2.1 is npm latest stable (not alpha4/rc7). Verified actual Tiled loader, atlas, Arcade Physics static objects, four-direction sprite animation and WebGL/Canvas renderer in Chromium. No Phaser3 compatibility blocker exists, so Phaser4 retained. Official template inspected as reference only; its `node log.js` telemetry was not adopted.

Exact package.json/package-lock.json pin Phaser4.2.1, Zod4.6.7, TS5.9.3 (supported stable by TS-ESLint8 rather than newly released TS7), Vite8.3.4, Vitest5.0.4, Playwright1.64.1, ESLint10.12.0, TS-ESLint8.71.2, Prettier3.9.10, Node types24.19.2. npm package integrity/TLS left enabled. No provider credentials.

## Repeat locally

Node24+, Python3.12+ recommended; `python -m pip install -r tools/requirements.txt`, `npm ci --ignore-scripts`. Export editing: `npm run assets`; verification: `npm run assets:check`, `npm run typecheck`, `npm run lint`, `npm run format:check`, `npm test`, `npm run build`.

`npm run dev` starts Vite. Open its printed HTTP address with `/3D-pharse5-/`. Chromium test uses system executable if present; otherwise `npx playwright install chromium`; explicit path may be provided by PIXEL_CHROMIUM_PATH. `npm run test:e2e` starts/reuses production preview. Do not open source index.html in a raw file viewer.

## Native art editor options

Tiled1.12.2 upstream release inspected: https://github.com/mapeditor/tiled/releases/tag/v1.12.2 (GPL2+ authoring tool). LibreSprite1.3: https://github.com/LibreSprite/LibreSprite/releases/tag/v1.3 (GPL2 authoring tool). Neither executable is installed in this cloud/no GUI claimed. Use their official Windows/macOS installers or Linux AppImage locally if desired; open assets-src/plaza.tmj in Tiled, indexed PNGs in LibreSprite. Their program license does not license our original artwork.

Verified headless alternative is editable indexed PNG + palette/layout/Python integer-raster components + Phaser atlas exporter and Tiled-compatible JSON/object validation. Existing palette/map source edits survive re-export. No native GUI is needed to reproduce source→PNG/JSON→Phaser. No paid atlas service/sharp/pngjs/extra engine added.
