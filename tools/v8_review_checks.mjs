import { chromium } from "playwright";
import fs from "node:fs/promises";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const errors = [],
  rows = [];
const p = await browser.newPage({
  viewport: { width: 1440, height: 1140 },
  reducedMotion: "reduce",
});
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
await p.goto(base + "v8-city-review.html");
await p.waitForFunction(() => window.__V3_WORLD__?.candidate === "v8-city");
const before = await p.evaluate(() => ({
  qa: !!window.__SEOUL_TEST__,
  s: window.__SEOUL__,
  m: window.__PIXEL_METRICS__,
}));
if (
  before.qa ||
  before.m.animationFrames !== 144 ||
  before.s.totalProps !== 481
)
  throw Error("normal boot mismatch");
await p.locator("canvas").focus();
await p.keyboard.down("ArrowDown");
await p.waitForTimeout(900);
await p.keyboard.up("ArrowDown");
const after = await p.evaluate(() => window.__SEOUL__);
if (after.y - before.s.y < 10) throw Error("normal entry not moving");
rows.push({ kind: "normal-entry", before, after });
await p.close();
for (const dpr of [1, 2, 3]) {
  const c = await browser.newContext({
    viewport: { width: 1440, height: 1140 },
    deviceScaleFactor: dpr,
    reducedMotion: "reduce",
  });
  await c.addInitScript(() => {
    window.__DRAWS__ = [];
    const get = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (...args) {
      const ctx = get.apply(this, args);
      if (ctx?.drawImage && !window.__DRAWS__.some((r) => r.canvas === this)) {
        const r = { canvas: this, nearest: 0, smoothed: 0 };
        window.__DRAWS__.push(r);
        const draw = ctx.drawImage.bind(ctx);
        ctx.drawImage = function (...a) {
          r[ctx.imageSmoothingEnabled ? "smoothed" : "nearest"]++;
          return draw(...a);
        };
      }
      return ctx;
    };
  });
  const q = await c.newPage();
  q.on("pageerror", (e) => errors.push(e.message));
  await q.goto(base + "v8-city-review.html?qa&renderer=canvas");
  await q.waitForFunction(() => window.__SEOUL__?.ready);
  await q.evaluate(() => window.__SEOUL_TEST__.place(2112, 3008));
  await q.waitForTimeout(150);
  const sample = await q.locator("canvas").evaluate((c) => ({
    native: [c.width, c.height],
    css: getComputedStyle(c).imageRendering,
    draws: window.__DRAWS__
      .filter((r) => r.canvas === c)
      .map(({ nearest, smoothed }) => ({ nearest, smoothed })),
  }));
  if (
    sample.css !== "pixelated" ||
    sample.draws.some((r) => r.smoothed > 0 || !r.nearest)
  )
    throw Error("pixel filtering failure");
  rows.push({ dpr, ...sample });
  await c.close();
}
await browser.close();
if (errors.length) throw Error(errors);
await fs.writeFile(
  "docs/v8-city/quality/readiness-sharpness.json",
  JSON.stringify(
    {
      status: "PASS",
      rows,
      errors,
      limits:
        "Actual native drawImage nearest filtering; no post-render smoothing-flag inference, no physical device claim.",
    },
    null,
    2,
  ),
);
console.log(
  "V8 normal-entry readiness,144frames and DPR1/2/3 nearest asset draws PASS",
);
