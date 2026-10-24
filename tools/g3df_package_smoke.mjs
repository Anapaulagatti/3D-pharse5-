import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const base = "http://127.0.0.1:4307",
  errors = [],
  rows = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.url().startsWith(base) && r.status() >= 400)
      errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto(base + "/");
  await p.locator("text=OPEN VISUAL GALLERY").waitFor();
  await p.goto(base + "/gate3-review.html");
  await p.waitForURL(/scene=aligned-world/);
  for (const entry of [
    "palace",
    "academy",
    "culture",
    "transition",
    "retail",
    "station",
    "namsan",
    "amusement",
    "market",
    "jeju-culture",
  ]) {
    await p.goto(
      `${base}/gate3-review.html?scene=aligned-world&entry=${entry}&worldOnly&pixelAudit`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    const state = await p.evaluate(() => window.__GATE3__);
    const compat = await p.evaluate(() => document.compatMode);
    if (compat !== "CSS1Compat") throw Error("Non-standard document mode");
    if ((await p.locator("#scene-picker option").count()) !== 1)
      throw Error("Package exposes missing historical scene");
    rows.push({
      entry,
      renderer: state.renderer,
      ready: state.ready,
      zoom: state.zoom,
      errors: state.chunks.errors,
      compat,
    });
    if (entry === "retail") {
      const x = state.x;
      await p.keyboard.down("d");
      await p.waitForTimeout(400);
      await p.keyboard.up("d");
      if ((await p.evaluate(() => window.__GATE3__.x)) <= x)
        throw Error("WASD did not move Juni");
    }
  }
  const ctx = await b.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "no-preference",
    acceptDownloads: true,
  });
  const m = await ctx.newPage();
  m.on("pageerror", (e) => errors.push(e.message));
  await m.goto(
    `${base}/gate3-review.html?scene=aligned-world&entry=transition&worldOnly`,
  );
  await m.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const before = await m.evaluate(() => window.__GATE3__);
  const box = await m.locator("#joystick").boundingBox();
  const cdp = await ctx.newCDPSession(m);
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
  await m.waitForTimeout(600);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  const moved = await m.evaluate(() => window.__GATE3__);
  await m.locator("#scenic").click();
  await m.locator("#start-tour").click();
  await m.waitForTimeout(250);
  await m.locator("#tour-pause").click();
  await m.waitForFunction(() => window.__GATE3__?.camera.tour.paused);
  const paused = await m.evaluate(() => window.__GATE3__.camera.tour.paused);
  await m.locator("#tour-pause").click();
  await m.locator("#tour-next").click();
  await m.waitForFunction(() => window.__GATE3__?.camera.tour.index >= 1);
  await m.locator("#tour-controls").click();
  const collapsed =
    (await m.locator("#tour-controls").getAttribute("aria-expanded")) ===
    "false";
  await m.locator("#tour-controls").click();
  await m.locator("#return-juni").click();
  await m.waitForTimeout(200);
  const returned = await m.evaluate(() => window.__GATE3__);
  await m.emulateMedia({ reducedMotion: "reduce" });
  await m.locator("#scenic").click();
  await m.locator("#start-tour").click();
  await m.waitForFunction(() => window.__GATE3__?.camera.tour.paused);
  const reducedPauseDisabled = await m.locator("#tour-pause").isDisabled();
  await m.locator("#tour-next").click();
  await m.waitForFunction(() => window.__GATE3__?.camera.tour.index >= 1);
  await m.locator("#return-juni").click();
  await m.waitForTimeout(200);
  const reducedReturned = await m.evaluate(() => window.__GATE3__);
  await m.locator("#settings summary").click();
  const dl = m.waitForEvent("download");
  await m.locator("#export-session").click();
  await (await dl).saveAs("docs/gate3-alignment/package-emulated-session.json");
  const mobile = {
    environment:
      "Chromium844x390 DPR3 touch/reduced-motion emulation; NOT physical hardware",
    joystickMoved: moved.x > before.x,
    joystickZoomIsolated: moved.zoom === before.zoom,
    pauseWorked: paused,
    reducedMotionStaticPauseDisabled: reducedPauseDisabled,
    reducedMotionReturnPreserved:
      Math.abs(reducedReturned.x - moved.x) < 0.1 &&
      Math.abs(reducedReturned.y - moved.y) < 0.1,
    controlsCollapseRestore: collapsed,
    tourOriginalPositionPreserved:
      Math.abs(returned.x - moved.x) < 0.1 &&
      Math.abs(returned.y - moved.y) < 0.1,
    exportDownloaded: true,
    physicalAndroidChrome: "NOT TESTED",
    physicalIPhoneSafari: "NOT TESTED",
  };
  await ctx.close();
  await p.goto(base + "/docs/gate3-alignment/VISUAL_REVIEW.html");
  await p.locator("video").evaluate((v) => v.load());
  await p.waitForFunction(
    () => document.querySelector("video").readyState >= 1,
    {},
    { timeout: 30000 },
  );
  const report = {
    method:
      "Extracted ZIP on private localhost; all10 live Phaser entries, standards mode, WASD, emulated touch/tour/export and gallery video metadata",
    rows,
    mobile,
    errors,
    artAcceptance: "PENDING HUMAN",
    physicalDevices: "NOT TESTED",
  };
  await fs.writeFile(
    "docs/gate3-alignment/package-smoke.json",
    JSON.stringify(report, null, 2),
  );
  if (
    errors.length ||
    Object.entries(mobile).some(
      ([k, v]) =>
        [
          "joystickMoved",
          "joystickZoomIsolated",
          "pauseWorked",
          "reducedMotionStaticPauseDisabled",
          "reducedMotionReturnPreserved",
          "controlsCollapseRestore",
          "tourOriginalPositionPreserved",
          "exportDownloaded",
        ].includes(k) && !v,
    )
  )
    throw Error(JSON.stringify(report));
  console.log(
    "ZIP smoke PASS:10 entries, WASD, touch/tour/export; physical devices NOT TESTED",
  );
} finally {
  await b.close();
}
