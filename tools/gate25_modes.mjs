import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state } from "./gate2_browser_lib.mjs";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [],
  errors = [];
const D = "docs/gate25";
try {
  const p = await browser.newPage({
    viewport: { width: 844, height: 390 },
    hasTouch: true,
    isMobile: true,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  await ready(p, "c");
  const cdp = await p.context().newCDPSession(p),
    touch = (type, pts) =>
      cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts });
  const origin = await state(p);
  const joy = await p.locator("#joystick").boundingBox(),
    j = { x: joy.x + joy.width / 2 + 30, y: joy.y + joy.height / 2, id: 1 };
  await touch("touchStart", [j]);
  await p.waitForTimeout(350);
  await touch("touchEnd", []);
  assert((await state(p)).x > origin.x + 5);
  await p.tap("#scenic");
  await p.tap("#start-tour");
  await p.waitForTimeout(500);
  await p.tap("#tour-pause");
  await touch("touchStart", [
    { x: 280, y: 170, id: 1 },
    { x: 580, y: 170, id: 2 },
  ]);
  for (let i = 1; i <= 8; i++) {
    await touch("touchMove", [
      { x: 280 + i * 10, y: 170, id: 1 },
      { x: 580 - i * 10, y: 170, id: 2 },
    ]);
    await p.waitForTimeout(25);
  }
  await touch("touchEnd", []);
  await p.waitForTimeout(100);
  assert.equal((await state(p)).zoom, 0.25);
  await p.tap("#tour-pause");
  await p.waitForTimeout(450);
  assert.equal((await state(p)).zoom, 0.5);
  await p.tap("#return-juni");
  await p.waitForTimeout(450);
  assert.equal((await state(p)).zoom, 1);
  rows.push({
    case: "real touch joystick / paused-tour pinch / resumed50% / native return",
    pass: true,
  });
  await p.tap("#scenic");
  await p.tap("#start-tour");
  await p.waitForTimeout(250);
  await touch("touchStart", [j]);
  await touch("touchEnd", []);
  await p.waitForTimeout(450);
  assert.equal((await state(p)).camera.mode, "follow");
  rows.push({
    case: "joystick movement intent cancels auto tour without moving Juni",
    pass: true,
  });
  // Extended emulated session: record actual visible cadence across repeated camera mode switching.
  await ready(p, "district");
  const start = await state(p);
  for (let i = 0; i < 12; i++) {
    await p.tap("#scenic");
    await p.tap("#overview-mode");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "overview");
    const s = await state(p);
    assert.equal(s.chunks.resident.length, 3);
    await p.tap("#return-juni");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
    await p.waitForTimeout(500);
  }
  await p.waitForTimeout(8000);
  const end = await state(p);
  assert.equal(
    end.chunks.events.filter((e) => e.event === "request").length,
    1,
  );
  assert(Math.abs(start.x - end.x) < 0.01 && Math.abs(start.y - end.y) < 0.01);
  rows.push({
    case: "12 repeated camera cycles / one-time cached load / no teleport or reload",
    pass: true,
    state: end,
  });
  const download = p.waitForEvent("download");
  await p.locator("#settings summary").click();
  await p.locator("#export-session").click();
  const dl = await download;
  const path = await dl.path();
  const report = JSON.parse(await fs.readFile(path, "utf8"));
  assert(report.state.session.samples > 500);
  await fs.writeFile(
    D + "/emulated-session-export.json",
    JSON.stringify(report, null, 2) + "\n",
  );
  rows.push({
    case: "real downloadable diagnostics / client type explicitly unverified",
    pass: true,
  });
  await p.close();
  for (const [width, height, dpr] of [
    [740, 360, 1],
    [932, 430, 2],
    [960, 432, 1],
  ]) {
    const q = await browser.newPage({
      viewport: { width, height },
      deviceScaleFactor: dpr,
      hasTouch: true,
      isMobile: true,
    });
    await ready(q, "c");
    await q.tap("#scenic");
    await q.tap("#start-tour");
    await q.waitForTimeout(450);
    const boxes = await q
      .locator("#tour-pause,#tour-next,#return-juni")
      .evaluateAll((es) =>
        es.map((e) => {
          const r = e.getBoundingClientRect();
          return [r.left, r.top, r.right, r.bottom];
        }),
      );
    assert(
      boxes.every(
        (r) => r[0] >= 0 && r[1] >= 0 && r[2] <= width && r[3] <= height,
      ),
    );
    await q.screenshot({ path: D + `/TOUR_${width}x${height}.png` });
    rows.push({
      case: "landscape tour controls " + width + "x" + height + " DPR" + dpr,
      pass: true,
      boxes,
    });
    await q.close();
  }
  // QA placement is explicitly confined to this depth diagnostic, not movement/videos.
  const o = await browser.newPage();
  await ready(o, "district", "&qa");
  await o.evaluate(() => window.__GATE2_TEST__.place(1415, 780));
  await o.waitForTimeout(120);
  const behind = await state(o);
  assert(behind.behind.length > 0);
  await o.evaluate(() => window.__GATE2_TEST__.place(1415, 830));
  await o.waitForTimeout(120);
  const front = await state(o);
  assert(!front.behind.includes("district-gate1-5"));
  rows.push({
    case: "foreground Y-sort/softening / explicit diagnostic placement",
    pass: true,
    behind: behind.behind,
    front: front.behind,
  });
  await o.close();
  assert.equal(errors.length, 0);
  await fs.writeFile(
    D + "/modes-qa.json",
    JSON.stringify({ rows, errors, physicalDevices: "NOT TESTED" }, null, 2) +
      "\n",
  );
  console.log("PASS", rows.length, "mode/cache/touch/ratio/depth diagnostics");
} catch (e) {
  await fs.writeFile(
    D + "/modes-failure.json",
    JSON.stringify({ rows, errors, error: String(e) }, null, 2),
  );
  throw e;
} finally {
  await browser.close();
}
