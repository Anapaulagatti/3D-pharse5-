import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import assert from "node:assert/strict";

const out = process.env.REVIEW_DIR ?? "docs/juni-animation";
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
  samples = [],
  segments = [];
function observe(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) missing.push(`${r.status()} ${r.url()}`);
  });
}
const metrics = (p) =>
  p.evaluate(() => ({
    review: window.__PLAZA_REVIEW__,
    game: window.__PIXEL_METRICS__,
  }));
async function sample(p, name) {
  await p.locator("canvas").screenshot({ path: `${out}/${name}.png` });
  samples.push({ name, ...(await metrics(p)) });
}
async function still(p, name) {
  await p.locator("#pause").click();
  await p.waitForFunction(() => window.__PIXEL_METRICS__.paused);
  await sample(p, name);
  await p.locator("#pause").click();
  await p.waitForFunction(() => !window.__PIXEL_METRICS__.paused);
}
try {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1200 },
    reducedMotion: "no-preference",
    recordVideo: {
      dir: ".cache/juni-animation/video",
      size: { width: 1440, height: 1200 },
    },
  });
  const page = await context.newPage();
  observe(page);
  await page.goto(new URL("plaza-review.html", base).href);
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  await page.locator("#motion").check();
  await page.waitForFunction(() => window.__PIXEL_METRICS__.reduced);
  await still(page, "native-after-map");
  await page.locator("#night").click();
  await still(page, "evening-after-map");
  await page.locator("#night").click();
  await page.locator("#motion").uncheck();
  await page.locator("#zoom").selectOption("2");
  await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 2);
  await still(page, "native-gameplay-detail");
  const started = Date.now();
  await page.evaluate(() => {
    const log = [];
    window.__JUNI_CAPTURE__ = log;
    function sample() {
      const r = window.__PLAZA_REVIEW__,
        m = window.__PIXEL_METRICS__;
      if (r && m)
        log.push({
          t: performance.now(),
          frame: r.frame,
          action: r.action,
          direction: r.direction,
          phase: r.phase,
          x: m.x,
          y: m.y,
          fps: m.fps,
        });
      requestAnimationFrame(sample);
    }
    requestAnimationFrame(sample);
  });
  // Real keyboard traversal on the unobstructed gathering rectangle. NO actor
  // teleport, pose injection, CSS bounce, speed change or recording time warp.
  await page.waitForTimeout(3300);
  for (const running of [false, true]) {
    if (running) await page.keyboard.down("Shift");
    for (const [key, direction] of [
      ["ArrowRight", "right"],
      ["ArrowUp", "back"],
      ["ArrowLeft", "left"],
      ["ArrowDown", "front"],
    ]) {
      await page.locator("canvas").focus();
      const start = Date.now();
      await page.keyboard.down(key);
      try {
        await page.waitForFunction(
          ({ running, direction }) =>
            window.__PLAZA_REVIEW__.action === (running ? "run" : "walk") &&
            window.__PLAZA_REVIEW__.direction === direction,
          { running, direction },
        );
        // Full cadence cycle after entry while still keeping travel inside the
        // real open plaza; 0.8s walk,0.65s run at original60/100world speed.
        await page.waitForTimeout(running ? 750 : 900);
      } finally {
        await page.keyboard.up(key);
      }
      await page.waitForFunction(
        () => window.__PLAZA_REVIEW__.action === "idle",
      );
      segments.push({
        kind: running ? "run" : "walk",
        direction,
        start_ms: start - started,
        end_ms: Date.now() - started,
        ...(await metrics(page)),
      });
    }
    if (running) await page.keyboard.up("Shift");
  }
  // A continuous corner demonstrates turning without the stop/idle gap.
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(220);
  await page.keyboard.up("ArrowRight");
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(320);
  await page.keyboard.up("ArrowUp");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__.action === "idle");
  for (const [id, action] of [
    ["wave", "wave"],
    ["celebrate", "celebrate"],
    ["pose", "social"],
  ]) {
    const start = Date.now();
    await page.locator(`#${id}`).click();
    await page.waitForFunction(
      (action) => window.__PLAZA_REVIEW__.action === action,
      action,
    );
    await page.waitForFunction(() => window.__PLAZA_REVIEW__.action === "idle");
    segments.push({
      kind: action,
      start_ms: start - started,
      end_ms: Date.now() - started,
    });
  }
  await page.waitForTimeout(1700);
  await still(page, "gameplay-after-traversal");
  await page.screenshot({ path: `${out}/review-page.png`, fullPage: true });
  const frameLog = await page.evaluate(() => window.__JUNI_CAPTURE__);
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
  assert.equal((await metrics(mp)).game.renderer, "Canvas");
  const before = await metrics(mp);
  await sample(mp, "mobile-canvas");
  const button = mp.locator('[data-x="1"]');
  await button.scrollIntoViewIfNeeded();
  const rect = await button.boundingBox();
  const touch = await mobile.newCDPSession(mp);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 }],
  });
  await mp.waitForFunction(
    (x) => window.__PIXEL_METRICS__.x > x + 24,
    before.game.x,
  );
  const moving = await metrics(mp);
  assert.match(moving.review.frame, /^(walk|start)-right-/);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await mp.waitForFunction(() => window.__PLAZA_REVIEW__.action === "idle");
  const after = await metrics(mp);
  assert.equal(after.review.environmentClock, before.review.environmentClock);
  assert(
    await mp.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
  );
  await mp.screenshot({ path: `${out}/mobile-page.png`, fullPage: true });
  await mobile.close();
  const original = await browser.newPage();
  observe(original);
  await original.goto(base);
  await original.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  const old = await original.evaluate(() => window.__PIXEL_METRICS__);
  assert.equal(old.guests.length, 4);
  assert.equal(old.avatarVersion, "chibi-motion-v2");
  const report = {
    status: "CAPTURED_REQUIRES_VISUAL_INSPECTION",
    method:
      "Actual Phaser native/enlarged screenshots and real-time recorded keyboard gameplay. Source-generated articulated poses, no actor position/pose injection, mirror/bounce substitute, camera-only motion or video speed-up.",
    samples,
    segments,
    frameLog,
    videoSource: videoPath,
    mobile: { before, moving, after },
    preservedGame: {
      guests: old.guests.length,
      avatarVersion: old.avatarVersion,
    },
    errors,
    missing,
    limits: [
      "Software-rendered Chromium and emulated mobile, not physical-device performance.",
      "Side idle and small gesture near-duplicate detector warnings remain documented; no automatic art approval.",
    ],
  };
  writeFileSync(
    `${out}/browser-verification.json`,
    JSON.stringify(report, null, 2) + "\n",
  );
  assert.deepEqual(errors, []);
  assert.deepEqual(missing, []);
  console.log(
    JSON.stringify({ videoPath, screens: samples.length, errors, missing }),
  );
} finally {
  await browser.close();
}
