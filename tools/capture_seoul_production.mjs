import { chromium } from "playwright";
import fs from "node:fs/promises";
const out = "docs/seoul-production/quality";
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const context = await browser.newContext({
  viewport: { width: 1440, height: 1140 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const observations = [];
await page.goto(base + "production-review.html?qa");
await page.waitForFunction(() => window.__SEOUL__?.ready);
async function shot(id, x, y) {
  if (x !== undefined)
    await page.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
  await page.locator("canvas").scrollIntoViewIfNeeded();
  await page.waitForTimeout(240);
  await page.locator("canvas").screenshot({ path: `${out}/${id}.png` });
  observations.push({
    id,
    world: await page.evaluate(() => window.__SEOUL__),
    animation: await page.evaluate(() => window.__PLAZA_REVIEW__),
  });
}
await shot("opening-native");
await shot("gate-native", 2048, 832);
await shot("academy-native", 672, 960);
await shot("workshop-native", 3312, 860);
await shot("museum-native", 3552, 1360);
await shot("palace-boundary-native", 1200, 650);
await shot("occlusion-native", 1120, 886);
if (!(await page.evaluate(() => window.__PLAZA_REVIEW__.occludedPixels > 0)))
  throw Error("Occlusion cue not observed");
await shot("courtyard-reading-door", 672, 832);
await page.locator("#interact").click();
await page.waitForFunction(() => window.__SEOUL__?.area === "room");
await shot("reading-room-native");
await page.evaluate(() => window.__SEOUL_TEST__.place(385, 392));
await page.waitForTimeout(80);
await page.locator("#interact").click();
await page.locator(".hangul-letter").waitFor();
await page.screenshot({ path: `${out}/letter-lesson-ui.png` });
await page.locator("#close-dialog").click();
await page.evaluate(() => window.__SEOUL_TEST__.place(384, 490));
await page.waitForTimeout(80);
await page.locator("#interact").click();
await page.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
await page.evaluate(() => window.__SEOUL_TEST__.place(2048, 832));
await page.waitForTimeout(100);
await page.locator("#interact").click();
await page.waitForFunction(() => window.__SEOUL__?.gateOpen);
await page.locator("#close-dialog").click();
await shot("gate-open-native");
await page.locator("#night").click();
await shot("evening-native");
await page.locator("#night").click();
await page.setViewportSize({ width: 2200, height: 1300 });
await page.goto(base + "production-review.html?overview");
await page.waitForFunction(() => window.__SEOUL__?.ready);
await page.locator("canvas").scrollIntoViewIfNeeded();
await page.waitForTimeout(200);
await page.locator("canvas").screenshot({ path: `${out}/phaser-overview.png` });
observations.push({
  id: "overview",
  world: await page.evaluate(() => window.__SEOUL__),
});
await context.close();
const mobile = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 1,
  isMobile: true,
  hasTouch: true,
  reducedMotion: "reduce",
});
const mp = await mobile.newPage();
mp.on("pageerror", (e) => errors.push("mobile " + e.message));
await mp.goto(base + "production-review.html?qa&renderer=canvas");
await mp.waitForFunction(() => window.__SEOUL__?.ready);
await mp.evaluate(() => window.__SEOUL_TEST__.place(672, 960));
await mp.waitForTimeout(180);
await mp.locator("canvas").screenshot({ path: `${out}/mobile-canvas.png` });
await mp.screenshot({ path: `${out}/mobile-ui.png`, fullPage: true });
observations.push({
  id: "mobile",
  world: await mp.evaluate(() => window.__SEOUL__),
  renderer: await mp.evaluate(() => window.__PIXEL_METRICS__.renderer),
  overflow: await mp.evaluate(() => document.documentElement.scrollWidth > 390),
});
await mobile.close();
await browser.close();
await fs.writeFile(
  `${out}/rendered-evidence.json`,
  JSON.stringify(
    {
      source:
        "Actual Chromium Phaser production build; 1x native except labelled overview",
      capturePositions:
        "QA preset placement for stills only; real-input uninterrupted video recorded separately",
      errors,
      observations,
      limits: [
        "Emulated mobile, no physical phone/FPS certification",
        "Overview fits area only for review; default gameplay integer zoom with follow",
        "No new NPCs/south district/art approval claimed",
      ],
    },
    null,
    2,
  ) + "\n",
);
if (errors.length) throw Error(JSON.stringify(errors));
console.log(
  JSON.stringify({
    status: "PASS",
    actualScreenshots: 15,
    observations: observations.length,
    errors,
  }),
);
