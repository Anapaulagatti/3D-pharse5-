/** Stable viewport recording: no screenshot/fullPage viewport changes during video. */
import { chromium } from "@playwright/test";
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
mkdirSync(".cache/living-seoul/clean-video", { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const errors = [],
  timeline = [];
try {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1200 },
    reducedMotion: "no-preference",
    recordVideo: {
      dir: ".cache/living-seoul/clean-video",
      size: { width: 1440, height: 1200 },
    },
  });
  const page = await context.newPage();
  const video = page.video();
  const begin = Date.now();
  const sample = async (label) =>
    timeline.push({
      label,
      elapsedMs: Date.now() - begin,
      district: await page.evaluate(() => window.__DISTRICT__),
      actor: await page.evaluate(() => window.__PLAZA_REVIEW__),
    });
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await page.goto("http://127.0.0.1:4201/3D-pharse5-/district-review.html");
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  await sample("plaza / approved Juni");
  await page.waitForTimeout(700);
  await page.locator("canvas").focus();
  await page.keyboard.down("Shift");
  for (const [key, field, target, positive, label] of [
    ["ArrowRight", "x", 1280, true, "crossed bridge and book alley"],
    ["ArrowUp", "y", 544, false, "academy approach"],
    ["ArrowRight", "x", 1536, true, "academy court"],
    ["ArrowUp", "y", 475, false, "academy doorstep"],
  ]) {
    await page.keyboard.down(key);
    try {
      await page.waitForFunction(
        ({ field, target, positive }) =>
          positive
            ? window.__DISTRICT__[field] >= target
            : window.__DISTRICT__[field] <= target,
        { field, target, positive },
        { timeout: 23000 },
      );
    } finally {
      await page.keyboard.up(key);
    }
    await page.waitForTimeout(160);
    await sample(label);
  }
  await page.keyboard.up("Shift");
  await page.locator("#wave").click();
  await page.waitForTimeout(1300);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__DISTRICT__?.area === "room");
  await sample("reading room entered");
  await page.waitForTimeout(700);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  try {
    await page.waitForFunction(() => window.__DISTRICT__.y <= 397);
  } finally {
    await page.keyboard.up("ArrowUp");
  }
  await page.waitForTimeout(180);
  await page.locator("#interact").click();
  await sample("letter matching opened");
  for (const name of ["giyeok", "nieun", "mieum"]) {
    await page
      .locator("#dialog-copy")
      .getByRole("button", { name, exact: true })
      .click();
    await page.waitForTimeout(650);
    await page
      .locator("#dialog-copy")
      .getByRole("button", {
        name: name === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  await sample("three letter names completed");
  await page.waitForTimeout(600);
  await page.locator("#close-dialog").click();
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  try {
    await page.waitForFunction(() => window.__DISTRICT__.y >= 490);
  } finally {
    await page.keyboard.up("ArrowDown");
  }
  await page.waitForTimeout(180);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__DISTRICT__?.area === "outdoor");
  await sample("returned to academy court");
  await page.waitForTimeout(900);
  assert.deepEqual(errors, []);
  await context.close();
  writeFileSync(
    "docs/living-seoul/recording.json",
    JSON.stringify(
      {
        status: "RECORDED_REAL_PHASER",
        source: await video.path(),
        viewport: [1440, 1200],
        errors,
        timeline,
        method:
          "Fixed viewport, actual keyboard/buttons, no screenshots during video, no pose/position injection, no time remapping.",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(await video.path());
} finally {
  await browser.close();
}
