import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const out = "quality-reports/pixel-reset-v2/motion";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: "/usr/bin/chromium",
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
const errors = [],
  missing = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
const cdp = await context.newCDPSession(page);
const frames = [];
let phase = "idle",
  accept = false;
let origin;
cdp.on("Page.screencastFrame", (e) => {
  cdp
    .send("Page.screencastFrameAck", { sessionId: e.sessionId })
    .catch(() => {});
  if (!accept) return;
  if (origin === undefined) origin = e.metadata.timestamp;
  const n = frames.length;
  const buffer = Buffer.from(e.data, "base64");
  writeFileSync(`${out}/${String(n).padStart(4, "0")}.jpg`, buffer);
  frames.push({
    index: n,
    at: e.metadata.timestamp - origin,
    label: phase,
    sha256: createHash("sha256").update(buffer).digest("hex"),
  });
});
await cdp.send("Page.startScreencast", {
  format: "jpeg",
  quality: 80,
  maxWidth: 1280,
  maxHeight: 1000,
  everyNthFrame: 2,
});
accept = true;
const segments = [];
for (const style of ["A", "B", "C"]) {
  phase = style + "-transition";
  await page.locator("#direction").selectOption(style);
  await page.waitForFunction(
    (s) => window.__PIXEL_METRICS__?.style === s,
    style,
  );
  await page.locator("canvas").focus();
  phase = style + "-idle";
  const start = await page.evaluate(() => window.__PIXEL_METRICS__);
  const wallStart = performance.now();
  await page.waitForFunction(
    (n) => (window.__PIXEL_METRICS__?.frameCount ?? 0) > n + 135,
    start.frameCount,
    { timeout: 30000 },
  );
  const end = await page.evaluate(() => window.__PIXEL_METRICS__);
  const wallSeconds = (performance.now() - wallStart) / 1000;
  segments.push({
    style,
    phase,
    start,
    end,
    wallSeconds,
    actualCloudFramesPerSecond:
      (end.frameCount - start.frameCount) / wallSeconds,
  });
  for (const [key, label, count] of [
    ["ArrowDown", "walk-down", 20],
    ["ArrowRight", "walk-right", 20],
    ["ArrowUp", "walk-up", 20],
    ["ArrowLeft", "walk-left", 20],
  ]) {
    phase = style + "-" + label;
    await page.keyboard.down(key);
    const frame = await page.evaluate(
      () => window.__PIXEL_METRICS__.frameCount,
    );
    await page.waitForFunction(
      ({ n, count }) => window.__PIXEL_METRICS__.frameCount >= n + count,
      { n: frame, count },
      { timeout: 15000 },
    );
    await page.keyboard.up(key);
    segments.push({
      style,
      phase,
      metrics: await page.evaluate(() => window.__PIXEL_METRICS__),
    });
  }
  phase = style + "-emote";
  await page.keyboard.press("Space");
  const f = await page.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await page.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount >= n + 55,
    f,
    { timeout: 15000 },
  );
  segments.push({
    style,
    phase,
    metrics: await page.evaluate(() => window.__PIXEL_METRICS__),
  });
}
accept = false;
await cdp.send("Page.stopScreencast");
writeFileSync(
  `${out}/capture.json`,
  JSON.stringify(
    {
      status:
        errors.length || missing.length
          ? "FAIL"
          : "CAPTURED_PENDING_VIDEO_REVIEW",
      frames,
      segments,
      errors,
      missing,
      method:
        "Actual CDP compositor JPEG frames and original Chrome timestamps, native keyboard only. No injected poses or speed-up. Real cloud FPS sample includes screencast overhead; not physical-device performance.",
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log(
  JSON.stringify({
    frames: frames.length,
    seconds: frames.at(-1)?.at,
    segments: segments.length,
  }),
);
