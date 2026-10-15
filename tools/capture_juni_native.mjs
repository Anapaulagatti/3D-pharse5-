import { chromium } from "@playwright/test";
import { readFileSync, writeFileSync } from "node:fs";
import assert from "node:assert/strict";
const out = "docs/juni-animation";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const evidence = [];
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1200 },
    reducedMotion: "no-preference",
  });
  await page.goto("http://127.0.0.1:4201/3D-pharse5-/plaza-review.html");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  for (const [name, key, run, frame] of [
    ["native-walk-right", "ArrowRight", false, "walk-right-2"],
    ["native-run-back", "ArrowUp", true, "run-back-3"],
  ]) {
    await page.locator("canvas").focus();
    if (run) await page.keyboard.down("Shift");
    await page.keyboard.down(key);
    try {
      await page.waitForFunction(
        (frame) => window.__PLAZA_REVIEW__.frame === frame,
        frame,
      );
      await page.locator("#pause").click();
      await page.waitForFunction(() => window.__PIXEL_METRICS__.paused);
    } finally {
      await page.keyboard.up(key);
      if (run) await page.keyboard.up("Shift");
    }
    const m = await page.evaluate(() => ({
      review: window.__PLAZA_REVIEW__,
      game: window.__PIXEL_METRICS__,
    }));
    assert(m.review.frame.startsWith(run ? "run-back-" : "walk-right-"));
    await page.locator("canvas").screenshot({ path: `${out}/${name}.png` });
    evidence.push({ name, ...m });
    await page.locator("#pause").click();
    await page.waitForFunction(() => window.__PLAZA_REVIEW__.action === "idle");
  }
  for (const [name, id, frame] of [
    ["native-wave", "wave", "wave-front-3"],
    ["native-celebrate", "celebrate", "celebrate-front-4"],
  ]) {
    await page.locator(`#${id}`).click();
    await page.waitForFunction(
      (frame) => window.__PLAZA_REVIEW__.frame === frame,
      frame,
    );
    await page.locator("#pause").click();
    await page.waitForFunction(() => window.__PIXEL_METRICS__.paused);
    const m = await page.evaluate(() => ({
      review: window.__PLAZA_REVIEW__,
      game: window.__PIXEL_METRICS__,
    }));
    await page.locator("canvas").screenshot({ path: `${out}/${name}.png` });
    evidence.push({ name, ...m });
    await page.locator("#pause").click();
    await page.waitForFunction(() => window.__PLAZA_REVIEW__.action === "idle");
  }
  const report = JSON.parse(
    readFileSync(`${out}/browser-verification.json`, "utf8"),
  );
  report.nativePoses = evidence;
  report.nativePoseMethod =
    "Real keyboard/button input at camera1x, then existing Pause UI freezes the current actual frame; no pose/position injection.";
  writeFileSync(
    `${out}/browser-verification.json`,
    JSON.stringify(report, null, 2) + "\n",
  );
  console.log(
    JSON.stringify(
      evidence.map((x) => ({ name: x.name, frame: x.review.frame })),
    ),
  );
} finally {
  await browser.close();
}
