import { chromium } from "playwright";
import fs from "node:fs/promises";
const phase = process.env.POLISH_PHASE ?? "after";
if (!["before", "after"].includes(phase)) throw Error("Choose before or after");
if (phase === "before") {
  try {
    await fs.access("docs/stage-b-polish/quality/before/capture.json");
    throw Error(
      "The accepted baseline capture is immutable; use the recovery checkpoint in a separate clone.",
    );
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
  }
}
const out = `docs/stage-b-polish/quality/${phase}`;
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const ctx = await browser.newContext({
  viewport: { width: 1440, height: 1140 },
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
});
const page = await ctx.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
await page.goto(
  (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4200/3D-pharse5-/") +
    "production-review.html?qa",
);
await page.waitForFunction(() => window.__SEOUL__?.ready);
const observations = [];
for (const [id, x, y] of [
  ["academy", 672, 960],
  ["workshop", 3312, 860],
  ["museum", 3552, 1360],
  ["gate", 2048, 832],
  ["plaza", 1920, 1328],
  ["academy-edge", 850, 1210],
]) {
  await page.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
  await page.waitForTimeout(400);
  await page.locator("canvas").screenshot({ path: `${out}/${id}-native.png` });
  observations.push({
    id,
    world: await page.evaluate(() => window.__SEOUL__),
    metrics: await page.evaluate(() => window.__PLAZA_REVIEW__),
    renderer: await page.evaluate(() => window.__PIXEL_METRICS__.renderer),
  });
}
await page.setViewportSize({ width: 2200, height: 1300 });
await page.goto(
  (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4200/3D-pharse5-/") +
    "production-review.html?overview",
);
await page.waitForFunction(() => window.__SEOUL__?.ready);
await page.waitForTimeout(300);
await page.locator("canvas").screenshot({ path: `${out}/overview.png` });
if (phase === "after") {
  await page.setViewportSize({ width: 1440, height: 1140 });
  await page.goto(
    (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4200/3D-pharse5-/") +
      "production-review.html?qa",
  );
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  await page.evaluate(() => window.__SEOUL_TEST__.place(3824, 1312));
  await page.waitForTimeout(400);
  const occlusion = await page.evaluate(() => window.__PLAZA_REVIEW__);
  if (!(occlusion.occludedPixels > 0))
    throw Error("New museum stele visibility cue missing");
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/new-prop-occlusion.png` });
  observations.push({ id: "new-prop-occlusion", metrics: occlusion });
  await page.evaluate(() => window.__SEOUL_TEST__.place(3312, 860));
  await page.locator("#night").click();
  await page.waitForTimeout(400);
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/evening-native.png` });
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 1,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const mp = await mobile.newPage();
  mp.on("pageerror", (e) => errors.push(e.message));
  mp.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  mp.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await mp.goto(
    (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4200/3D-pharse5-/") +
      "production-review.html?qa&renderer=canvas",
  );
  await mp.waitForFunction(() => window.__SEOUL__?.ready);
  await mp.evaluate(() => window.__SEOUL_TEST__.place(672, 960));
  await mp.waitForTimeout(400);
  await mp.locator("canvas").screenshot({ path: `${out}/mobile-canvas.png` });
  await mp.screenshot({ path: `${out}/mobile-ui.png`, fullPage: true });
  observations.push({
    id: "mobile",
    renderer: await mp.evaluate(() => window.__PIXEL_METRICS__.renderer),
    overflow: await mp.evaluate(
      () => document.documentElement.scrollWidth > 390,
    ),
  });
  await mobile.close();
}
await browser.close();
await fs.writeFile(
  `${out}/capture.json`,
  JSON.stringify(
    {
      phase,
      source:
        "Actual Phaser rendered canvas element; QA still positions, reduced motion, fixed daytime and viewport; no painted screenshot pixels",
      observations,
      errors,
    },
    null,
    2,
  ) + "\n",
);
if (errors.length) throw Error(JSON.stringify(errors));
console.log({ phase, images: phase === "after" ? 11 : 7, errors });
