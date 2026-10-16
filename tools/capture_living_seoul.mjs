import { chromium } from "@playwright/test";
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
const out = "docs/living-seoul";
mkdirSync(".cache/living-seoul/video", { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const base =
  process.env.DISTRICT_PREVIEW_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const errors = [],
  warnings = [],
  requests = [],
  steps = [];
async function axis(page, key, field, target, positive = true) {
  await page.locator("canvas").focus();
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      ({ field, target, positive }) => {
        const d = window.__DISTRICT__;
        return d && (positive ? d[field] >= target : d[field] <= target);
      },
      { field, target, positive },
      { timeout: 24000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.waitForTimeout(150);
  steps.push({
    key,
    target,
    actual: await page.evaluate(() => window.__DISTRICT__),
  });
}
let video;
try {
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1200 },
    reducedMotion: "no-preference",
    recordVideo: {
      dir: ".cache/living-seoul/video",
      size: { width: 1440, height: 1200 },
    },
  });
  const page = await ctx.newPage();
  video = page.video();
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
    if (m.type() === "warning") warnings.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  page.on("request", (r) => requests.push(r.url()));
  await page.goto(base + "district-review.html");
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  assert(
    !requests.some((u) => u.includes("/living-seoul/room/")),
    "interior must load lazily",
  );
  await page.locator("canvas").screenshot({ path: `${out}/plaza-native.png` });
  await page.locator("canvas").focus();
  await page.keyboard.down("Shift");
  await axis(page, "ArrowRight", "x", 1280);
  await axis(page, "ArrowUp", "y", 544, false);
  await axis(page, "ArrowRight", "x", 1536);
  await axis(page, "ArrowUp", "y", 475, false);
  await page.keyboard.up("Shift");
  await page.waitForTimeout(700);
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/academy-native.png` });
  await page.locator("#night").click();
  await page.waitForTimeout(200);
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/academy-evening.png` });
  await page.locator("#night").click();
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__DISTRICT__?.area === "room");
  await page.waitForTimeout(600);
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/reading-room-native.png` });
  await axis(page, "ArrowUp", "y", 397, false);
  await page.locator("#interact").click();
  await page
    .locator("#dialog-copy")
    .getByRole("button", { name: "mieum", exact: true })
    .click();
  assert(
    (await page.locator("#dialog-copy").textContent()).includes("Chưa đúng"),
  );
  for (const name of ["giyeok", "nieun", "mieum"]) {
    await page
      .locator("#dialog-copy")
      .getByRole("button", { name, exact: true })
      .click();
    await page.waitForTimeout(400);
    if (name === "giyeok")
      await page.screenshot({
        path: `${out}/learning-activity.png`,
        fullPage: true,
      });
    await page
      .locator("#dialog-copy")
      .getByRole("button", {
        name: name === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  assert(
    (await page.locator("#quest-progress").textContent()).includes("Đã ghép"),
  );
  await page.waitForTimeout(600);
  await page.locator("#close-dialog").click();
  await axis(page, "ArrowDown", "y", 490);
  await page.locator("#interact").click();
  await page.waitForFunction(
    () =>
      window.__DISTRICT__?.area === "outdoor" &&
      window.__DISTRICT__.transitions >= 2,
  );
  const returned = await page.evaluate(() => window.__DISTRICT__);
  assert(Math.abs(returned.x - 1536) < 2 && Math.abs(returned.y - 475) < 2);
  await page.locator("#wave").click();
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "wave");
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${out}/playable-page.png`, fullPage: true });
  await page.reload();
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  assert(
    (await page.locator("#quest-progress").textContent()).includes("Đã ghép"),
  );
  const localSave = await page.evaluate(() =>
    JSON.parse(localStorage.getItem("korean-arena-academy-v1")),
  );
  await ctx.close();
  const overview = await browser.newPage({
    viewport: { width: 2300, height: 1300 },
    reducedMotion: "reduce",
  });
  await overview.goto(base + "district-review.html?overview=1");
  await overview.waitForFunction(() => window.__DISTRICT__?.ready);
  await overview
    .locator("canvas")
    .screenshot({ path: `${out}/district-overview-native.png` });
  await overview.close();
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const mp = await mobile.newPage();
  await mp.addInitScript(() => {
    const get = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      if (
        type === "webgl" ||
        type === "webgl2" ||
        type === "experimental-webgl"
      )
        return null;
      return get.call(this, type, ...args);
    };
  });
  mp.on("pageerror", (e) => errors.push(`mobile:${e.message}`));
  await mp.goto(base + "district-review.html");
  await mp.waitForFunction(() => window.__DISTRICT__?.ready);
  assert(
    (await mp.evaluate(() => window.__PIXEL_METRICS__.renderer)) === "Canvas",
  );
  const before = await mp.evaluate(() => window.__DISTRICT__.x);
  const touch = mp.locator('[data-x="1"]');
  await touch.scrollIntoViewIfNeeded();
  const box = await touch.boundingBox();
  const cdp = await mobile.newCDPSession(mp);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: box.x + box.width / 2, y: box.y + box.height / 2 }],
  });
  await mp.waitForTimeout(700);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await mp.waitForTimeout(250);
  assert((await mp.evaluate(() => window.__DISTRICT__.x)) > before + 10);
  await mp.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "idle");
  const frozen = await mp.evaluate(() => ({
    frame: window.__PLAZA_REVIEW__.frame,
    clock: window.__PLAZA_REVIEW__.environmentClock,
  }));
  await mp.waitForTimeout(400);
  assert.deepEqual(
    await mp.evaluate(() => ({
      frame: window.__PLAZA_REVIEW__.frame,
      clock: window.__PLAZA_REVIEW__.environmentClock,
    })),
    frozen,
  );
  await mp
    .locator("canvas")
    .screenshot({ path: `${out}/mobile-canvas-native.png` });
  await mp.screenshot({ path: `${out}/mobile-page.png`, fullPage: true });
  await mobile.close();
  assert.deepEqual(errors, []);
  writeFileSync(
    `${out}/browser-verification.json`,
    JSON.stringify(
      {
        status: "RUNTIME_VERIFIED_VISUAL_INSPECTION_PENDING",
        base,
        errors,
        warnings,
        steps,
        returned,
        localSave,
        roomLazyLoaded: true,
        mobile: {
          renderer: "Canvas",
          realCDPTouch: true,
          reducedMotionFrozen: true,
          viewport: [390, 844],
          deviceScaleFactor: 2,
          physicalHardware: false,
        },
        videoSource: await video.path(),
        method:
          "Real Phaser / keyboard and buttons / no pose or position injection / unsped video",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    JSON.stringify({
      video: await video.path(),
      errors,
      warnings,
      steps: steps.length,
    }),
  );
} finally {
  await browser.close();
}
