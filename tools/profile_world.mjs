import { chromium } from "playwright";
import fs from "node:fs/promises";
const browser = await chromium.launch({
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const rows = [];
try {
  for (const [id, renderer, size, point] of [
    ["desktop-civic", "canvas", [1440, 1140], [2176, 3056]],
    ["desktop-coast", "canvas", [1440, 1140], [2560, 4760]],
    ["mobile-leisure", "canvas", [844, 390], [3408, 3912]],
    ["software-webgl-station", "webgl", [1440, 1140], [1376, 3960]],
  ]) {
    const c = await browser.newContext({
      viewport: { width: size[0], height: size[1] },
      deviceScaleFactor: 1,
      reducedMotion: "no-preference",
    });
    try {
      const p = await c.newPage();
      await p.goto(
        "http://127.0.0.1:4201/3D-pharse5-/v9-world-review.html?qa&renderer=" +
          renderer,
      );
      await p.waitForFunction(() => window.__SEOUL__?.ready);
      await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), point);
      await p.waitForTimeout(1200);
      const data = await p.evaluate(async () => {
        const values = [];
        let last = performance.now();
        await new Promise((resolve) => {
          const end = last + 8000;
          function next(t) {
            values.push(t - last);
            last = t;
            if (t < end) requestAnimationFrame(next);
            else resolve();
          }
          requestAnimationFrame(next);
        });
        return {
          frameDeltasMs: values.slice(1),
          renderer: window.__PIXEL_METRICS__.renderer,
          props: window.__FULL_WORLD__.activeProps,
          totalProps: window.__FULL_WORLD__.totalProps,
          viewport: [
            window.__PIXEL_METRICS__.width,
            window.__PIXEL_METRICS__.height,
          ],
        };
      });
      const sorted = [...data.frameDeltasMs].sort((a, b) => a - b),
        median = sorted[Math.floor(sorted.length * 0.5)],
        p95 = sorted[Math.floor(sorted.length * 0.95)];
      rows.push({
        id,
        ...data,
        medianFrameMs: median,
        p95FrameMs: p95,
        medianRafHz: 1000 / median,
      });
      console.log(id, median, p95);
    } finally {
      await c.close();
    }
  }
  const report = {
    method:
      "Actual Chromium requestAnimationFrame deltas,8s percase after warmup. No screenshot/video capture or concurrent local browser suite during sampling.",
    hardware:
      "Cloud CPU; SwiftShader for forced WebGL. Functional mobile viewport emulation, not physical mobile GPU measurements. No universal60FPS claim.",
    browser: browser.version(),
    rows,
  };
  await fs.mkdir("docs/v9-world/quality/performance", { recursive: true });
  await fs.writeFile(
    "docs/v9-world/quality/performance/profile.json",
    JSON.stringify(report, null, 2),
  );
} finally {
  await browser.close();
}
