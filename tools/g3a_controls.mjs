import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  viewport: { width: 844, height: 390 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
  acceptDownloads: true,
});
const page = await context.newPage();
await page.goto("http://127.0.0.1:4271/gate3-review.html");
await page.waitForFunction(() => window.__GATE3__?.ready);
await page.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
const before = await page.evaluate(() => window.__GATE3__);
const box = await page.locator("#joystick").boundingBox();
const cdp = await context.newCDPSession(page);
const x = box.x + box.width / 2,
  y = box.y + box.height / 2;
await cdp.send("Input.dispatchTouchEvent", {
  type: "touchStart",
  touchPoints: [{ x, y, id: 1 }],
});
await cdp.send("Input.dispatchTouchEvent", {
  type: "touchMove",
  touchPoints: [{ x: x + 30, y, id: 1 }],
});
await page.waitForTimeout(650);
await cdp.send("Input.dispatchTouchEvent", {
  type: "touchEnd",
  touchPoints: [],
});
const moved = await page.evaluate(() => window.__GATE3__);
if (moved.x <= before.x || moved.camera.mode !== "follow")
  throw Error("Joystick movement/isolation failed");
await page.locator("#scenic").click();
await page.locator("#start-tour").click();
await page.waitForTimeout(400);
const reducedPauseDisabled = await page.locator("#tour-pause").isDisabled();
if (!reducedPauseDisabled)
  throw Error("Reduced-motion tour should use manual stops");
await page.locator("#tour-next").click();
await page.locator("#tour-controls").click();
const collapsed = await page.evaluate(
  () => window.__GATE3__.camera.tour.controlsCollapsed,
);
if (!collapsed) throw Error("Manual tour collapse failed");
await page.locator("#tour-controls").click();
await page.locator("#return-juni").click();
await page.waitForTimeout(500);
const returned = await page.evaluate(() => window.__GATE3__);
if (returned.x !== moved.x || returned.y !== moved.y)
  throw Error("Tour changed Juni position");
await page.emulateMedia({ reducedMotion: "no-preference" });
await page.locator("#scenic").click();
await page.locator("#start-tour").click();
await page.locator("#tour-pause").click();
await page.locator("#tour-next").click();
await page.locator("#return-juni").click();
await page.locator("#settings summary").click();
const [download] = await Promise.all([
  page.waitForEvent("download"),
  page.locator("#export-session").click(),
]);
await download.saveAs("docs/gate3a-corrections/emulated-export-example.json");
await fs.writeFile(
  "docs/gate3a-corrections/controls-report.json",
  JSON.stringify(
    {
      scope: "Chromium mobile emulation / physical devices NOT TESTED",
      before,
      moved,
      returned,
      joystickIsolated: true,
      reducedMotion: true,
      reducedPauseDisabled,
      pauseSkipReturn: true,
      collapsedControlRestore: collapsed,
      exportFilename: download.suggestedFilename(),
    },
    null,
    2,
  ),
);
await browser.close();
console.log(
  "Touch movement, reduced-motion tour controls and report export verified",
);
