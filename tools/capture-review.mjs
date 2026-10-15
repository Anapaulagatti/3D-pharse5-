import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const out = "quality-reports/pixel-v3.1/animation";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  headless: true,
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const context = await browser.newContext({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
  reducedMotion: "no-preference",
});
const page = await context.newPage();
const errors = [];
const missing = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
for (const style of ["A", "B", "C"]) {
  await page.locator("#direction").selectOption(style);
  await page.waitForFunction(
    (s) => window.__PIXEL_METRICS__?.style === s,
    style,
  );
  await page
    .locator("canvas")
    .screenshot({ path: `quality-reports/pixel-v3.1/engine-${style}.png` });
}
await page.locator("#direction").selectOption("B");
await page.waitForFunction(() => window.__PIXEL_METRICS__?.style === "B");
await page.locator("canvas").focus();
const frames = [];
const begin = performance.now();
async function record(ms, label) {
  const until = performance.now() + ms;
  while (performance.now() < until) {
    const index = frames.length;
    const at = (performance.now() - begin) / 1000;
    const buffer = await page.locator("canvas").screenshot({
      type: "jpeg",
      quality: 88,
      path: `${out}/${String(index).padStart(4, "0")}.jpg`,
    });
    const metrics = await page.evaluate(() => window.__PIXEL_METRICS__);
    frames.push({
      index,
      at,
      label,
      sha256: createHash("sha256").update(buffer).digest("hex"),
      metrics,
    });
    await page.waitForTimeout(100);
  }
}
await record(400, "idle");
for (const [key, label] of [
  ["ArrowDown", "down"],
  ["ArrowUp", "up"],
  ["ArrowLeft", "left"],
  ["ArrowRight", "right"],
]) {
  await page.keyboard.down(key);
  await record(700, label);
  await page.keyboard.up(key);
}
await page.keyboard.down("Shift");
await page.keyboard.down("ArrowDown");
await record(800, "run");
await page.keyboard.up("ArrowDown");
await page.keyboard.up("Shift");
await page.keyboard.press("Space");
await record(1000, "wave");
await record(600, "idle-return");
const sizes = await page.evaluate(() =>
  performance.getEntriesByType("resource").map((e) => ({
    name: e.name,
    bytes: e instanceof PerformanceResourceTiming ? e.decodedBodySize : null,
    transfer: e instanceof PerformanceResourceTiming ? e.transferSize : null,
  })),
);
const stats = await page.evaluate(() => window.__PIXEL_METRICS__);
writeFileSync(
  `${out}/capture.json`,
  JSON.stringify(
    {
      status:
        errors.length || missing.length
          ? "FAIL"
          : "PASS_CAPTURED_PENDING_VISUAL_REVIEW",
      frames,
      errors,
      missing,
      sizes,
      stats,
      method:
        "Actual compositor JPEG screenshots at original wall-clock intervals; native keyboard only. No animation retiming.",
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log(
  JSON.stringify({ frames: frames.length, duration: frames.at(-1).at, stats }),
);
