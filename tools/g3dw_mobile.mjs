import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const ctx = await b.newContext({
  viewport: { width: 844, height: 390 },
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true,
  reducedMotion: "reduce",
  acceptDownloads: true,
});
const p = await ctx.newPage();
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
try {
  await p.goto(
    "http://127.0.0.1:4297/gate3-review.html?scene=recovery-world&entry=transition",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const before = await p.evaluate(() => window.__GATE3__);
  const box = await p.locator("#joystick").boundingBox();
  const cdp = await ctx.newCDPSession(p);
  const x = box.x + box.width / 2,
    y = box.y + box.height / 2;
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y }],
  });
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [{ x: x + 28, y }],
  });
  await p.waitForTimeout(700);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  const after = await p.evaluate(() => window.__GATE3__);
  await p.screenshot({
    path: "docs/gate3-recovery-world/mobile-landscape-review.png",
  });
  await p.locator("#scenic").click();
  if (!(await p.locator("#start-tour").isVisible()))
    await p.locator("#tour-controls").click();
  await p.locator("#start-tour").click();
  await p.waitForTimeout(700);
  const tour = await p.evaluate(() => window.__GATE3__);
  await p.screenshot({
    path: "docs/gate3-recovery-world/mobile-tour-review.png",
  });
  await p.locator("#return-juni").click();
  await p.waitForTimeout(200);
  const returned = await p.evaluate(() => window.__GATE3__);
  await p.locator("#settings summary").click();
  const dl = p.waitForEvent("download");
  await p.locator("#export-session").click();
  await (
    await dl
  ).saveAs("docs/gate3-recovery-world/emulated-mobile-session.json");
  const report = {
    environment:
      "Chromium touch emulation844x390 DPR3 reducedMotion=reduce; NOT a physical phone",
    joystick: {
      before: [before.x, before.y],
      after: [after.x, after.y],
      moved: after.x > before.x,
      zoomUnchanged: before.zoom === after.zoom,
      cameraMode: after.camera.mode,
    },
    tour: {
      mode: tour.camera.mode,
      zoom: tour.zoom,
      state: tour.camera.tour,
      returnPosition: [returned.x, returned.y],
      originalJuniPositionPreserved:
        Math.abs(returned.x - after.x) < 0.1 &&
        Math.abs(returned.y - after.y) < 0.1,
    },
    exportDownloaded: true,
    errors,
    physicalAndroidChrome: "NOT TESTED",
    physicalIPhoneSafari: "NOT TESTED",
  };
  await fs.writeFile(
    "docs/gate3-recovery-world/mobile-report.json",
    JSON.stringify(report, null, 2),
  );
  console.log(
    "Mobile emulation",
    report.joystick,
    report.tour.originalJuniPositionPreserved,
  );
  if (errors.length) throw Error(errors.join("\n"));
} finally {
  await ctx.close();
  await b.close();
}
