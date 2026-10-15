import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import assert from "node:assert/strict";
const out = process.env.REVIEW_DIR ?? "docs/gwanghwamun";
const base =
  process.env.REVIEW_BASE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const errors = [],
  missing = [],
  samples = [];
function observe(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) missing.push(`${r.status()} ${r.url()}`);
  });
}
async function sample(p, name) {
  await p.waitForTimeout(160);
  await p.locator("canvas").screenshot({ path: `${out}/${name}.png` });
  samples.push({
    name,
    metrics: await p.evaluate(() => ({
      review: window.__PLAZA_REVIEW__,
      game: window.__PIXEL_METRICS__,
    })),
  });
}
async function axis(p, key, field, target, positive) {
  await p.locator("canvas").focus();
  await p.keyboard.down(key);
  try {
    await p.waitForFunction(
      ({ field, target, positive }) => {
        const v = window.__PIXEL_METRICS__[field];
        return positive ? v >= target : v <= target;
      },
      { field, target, positive },
      { timeout: 20000 },
    );
  } catch (error) {
    writeFileSync(
      `${out}/capture-failure.json`,
      JSON.stringify(
        {
          key,
          field,
          target,
          metrics: await p.evaluate(() => window.__PIXEL_METRICS__),
        },
        null,
        2,
      ),
    );
    await p
      .locator("canvas")
      .screenshot({ path: `${out}/capture-failure.png` });
    throw error;
  } finally {
    await p.keyboard.up(key);
  }
  await p.waitForTimeout(170);
}
try {
  const context = await browser.newContext({
    viewport: { width: 1550, height: 1300 },
    reducedMotion: "reduce",
    recordVideo: {
      dir: ".cache/gwanghwamun/video",
      size: { width: 1240, height: 1040 },
    },
  });
  const page = await context.newPage();
  observe(page);
  await page.goto(new URL("plaza-review.html", base).href);
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  await sample(page, "phaser-native-day");
  await page.screenshot({ path: `${out}/review-page.png`, fullPage: true });
  await page.locator("#night").click();
  await sample(page, "phaser-evening");
  await page.locator("#night").click();
  await page.locator("#motion").uncheck();
  const before = await page.evaluate(
    () => window.__PLAZA_REVIEW__.environmentClock,
  );
  await page.waitForTimeout(600);
  assert(
    (await page.evaluate(() => window.__PLAZA_REVIEW__.environmentClock)) >
      before + 100,
  );
  await axis(page, "ArrowUp", "y", 555, false);
  await axis(page, "ArrowRight", "x", 661, true);
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(750);
  await page.keyboard.up("ArrowRight");
  assert((await page.evaluate(() => window.__PIXEL_METRICS__.x)) <= 664.2);
  await sample(page, "water-collision");
  await axis(page, "ArrowDown", "y", 596, true);
  await axis(page, "ArrowRight", "x", 780, true);
  assert(
    (await page.evaluate(() => window.__PLAZA_REVIEW__.occludedPixels)) > 100,
  );
  await sample(page, "behind-tree");
  await axis(page, "ArrowDown", "y", 720, true);
  assert.equal(
    await page.evaluate(() => window.__PLAZA_REVIEW__.occludedPixels),
    0,
  );
  await sample(page, "front-tree");
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__PIXEL_METRICS__.interactions > 0);
  await page.locator("#close-dialog").click();
  // Return via real unobstructed input; no teleports or injected game-state positions.
  await axis(page, "ArrowUp", "y", 608, false);
  await axis(page, "ArrowLeft", "x", 600, false);
  await axis(page, "ArrowUp", "y", 380, false);
  await page.locator("#motion").check();
  await sample(page, "phaser-scale");
  await page.locator("#zoom").selectOption("2");
  await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 2);
  await sample(page, "phaser-detail");
  const video = page.video();
  await context.close();
  const videoPath = await video.path();
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const mp = await mobile.newPage();
  observe(mp);
  await mp.addInitScript(() => {
    const get = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (kind, ...args) {
      return String(kind).startsWith("webgl")
        ? null
        : Reflect.apply(get, this, [kind, ...args]);
    };
  });
  await mp.goto(new URL("plaza-review.html", base).href);
  await mp.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  assert.equal(
    await mp.evaluate(() => window.__PIXEL_METRICS__.renderer),
    "Canvas",
  );
  const clock = await mp.evaluate(
    () => window.__PLAZA_REVIEW__.environmentClock,
  );
  await mp.waitForTimeout(300);
  assert.equal(
    await mp.evaluate(() => window.__PLAZA_REVIEW__.environmentClock),
    clock,
  );
  await sample(mp, "mobile-canvas");
  await mp.screenshot({ path: `${out}/mobile-page.png`, fullPage: true });
  const oldX = await mp.evaluate(() => window.__PIXEL_METRICS__.x),
    b = mp.locator('[data-x="1"]');
  await b.scrollIntoViewIfNeeded();
  const rect = await b.boundingBox();
  const touch = await mobile.newCDPSession(mp);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 }],
  });
  await mp.waitForFunction((x) => window.__PIXEL_METRICS__.x > x + 20, oldX);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  assert(
    await mp.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
  );
  await mobile.close();
  const original = await browser.newPage();
  observe(original);
  await original.goto(base);
  await original.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  const preserved = await original.evaluate(() => window.__PIXEL_METRICS__);
  assert.equal(preserved.guests.length, 4);
  assert.equal(preserved.avatarVersion, "chibi-motion-v2");
  const report = {
    status: "CAPTURED_REQUIRES_VISUAL_INSPECTION",
    method:
      "Actual Phaser render of separate generated terrain and12 props. Real keyboard/touch movement; Juni4 static directions, NOT walk animation. Environment motion is lightweight runtime animation of generated texture/leaf sprites. No position injection or screenshot overlays.",
    samples,
    videoSource: videoPath,
    preservedGame: {
      avatarVersion: preserved.avatarVersion,
      guests: preserved.guests.length,
    },
    errors,
    missing,
    limits: [
      "Headless software-rendered desktop and emulated mobile; physical-phone performance unmeasured.",
      "Raw source concepts are not engine screenshots.",
      "Juni action clips and new NPCs deferred for visual approval.",
    ],
  };
  writeFileSync(
    `${out}/browser-verification.json`,
    JSON.stringify(report, null, 2) + "\n",
  );
  assert.deepEqual(errors, []);
  assert.deepEqual(missing, []);
  console.log(
    JSON.stringify({
      out,
      videoPath,
      screens: samples.length,
      errors,
      missing,
    }),
  );
} finally {
  await browser.close();
}
