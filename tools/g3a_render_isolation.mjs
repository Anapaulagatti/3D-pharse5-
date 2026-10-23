import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
for (const renderer of ["auto", "canvas"])
  for (const size of [
    [1280, 1000],
    [640, 550],
  ]) {
    const p = await b.newPage({
      viewport: { width: size[0], height: size[1] },
      deviceScaleFactor: 1,
    });
    await p.goto(
      `http://127.0.0.1:4271/gate3-review.html?scene=district&entry=station&profile&renderer=${renderer}`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
    await p.waitForTimeout(1000);
    await p.evaluate(() => window.__GATE3_PROFILE__.reset());
    await p.waitForTimeout(4000);
    rows.push({
      renderer,
      viewport: size,
      case: "native-detail-viewport-area",
      ...(await p.evaluate(() => ({
        state: window.__GATE3__,
        profile: window.__GATE3_PROFILE__.snapshot(),
      }))),
    });
    if (size[0] === 1280)
      for (const layer of ["none", "ground", "foreground", "all"]) {
        await p.evaluate((layer) => {
          window.__GATE3_PROFILE__.layer(layer);
          window.__GATE3_PROFILE__.reset();
        }, layer);
        await p.waitForTimeout(2000);
        rows.push({
          renderer,
          viewport: size,
          case: "layer-isolation",
          layer,
          ...(await p.evaluate(() => ({
            state: window.__GATE3__,
            profile: window.__GATE3_PROFILE__.snapshot(),
          }))),
        });
      }
    await p.close();
  }
await fs.writeFile(
  "docs/gate3a-corrections/render-isolation.json",
  JSON.stringify(
    {
      recording: false,
      sourceResolutionChanged: false,
      notes:
        "Layer-isolation GL calls include camera compositing; mixed production batches cannot be attributed additively. Smaller viewport changes field of view at native scale, not artwork resolution. This experiment is not a mobile acceptance result.",
      rows,
    },
    null,
    2,
  ),
);
await b.close();
