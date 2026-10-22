import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [];
try {
  const p = await b.newPage({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await ready(p, "c");
  const c = await p.context().newCDPSession(p),
    touch = (type, touchPoints) =>
      c.send("Input.dispatchTouchEvent", { type, touchPoints });
  const a = await state(p),
    j = await p.locator("#joystick").boundingBox(),
    point = { x: j.x + j.width / 2 + 30, y: j.y + j.height / 2, id: 1 };
  await touch("touchStart", [point]);
  await p.waitForTimeout(400);
  await touch("touchEnd", []);
  assert((await state(p)).x > a.x + 5);
  await p.tap("#scenic");
  await p.tap("#start-tour");
  await p.waitForTimeout(400);
  await p.tap("#tour-pause");
  const start = await state(p);
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
  assert.equal((await state(p)).x, start.x);
  await p.tap("#tour-pause");
  await p.waitForTimeout(400);
  assert.equal((await state(p)).zoom, 0.5);
  await touch("touchStart", [point]);
  await touch("touchEnd", []);
  await p.waitForTimeout(400);
  assert.equal((await state(p)).camera.mode, "follow");
  rows.push({
    case: "real joystick / paused pinch / Resume50% / joystick cancellation / no tour teleport",
    pass: true,
  });
  await p.locator("#settings summary").click();
  const pending = p.waitForEvent("download");
  await p.locator("#export-session").click();
  const download = await pending;
  const report = JSON.parse(await fs.readFile(await download.path(), "utf8"));
  assert(report.state.session.samples > 0);
  assert(report.physicalDeviceVerification.includes("NOT"));
  await fs.writeFile(
    "docs/gate25-polish/emulated-session-export.json",
    JSON.stringify(report, null, 2) + "\n",
  );
  rows.push({
    case: "retained downloadable report workflow / physical identity not falsely certified",
    pass: true,
  });
  await ready(p, "district-polish");
  for (let i = 0; i < 5; i++) {
    await p.tap("#scenic");
    await p.tap("#overview-mode");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "overview");
    const s = await state(p);
    assert.equal(s.chunks.resident.length, 3);
    assert(
      Math.abs(s.camera.worldView[2] - 3184) < 0.01 &&
        Math.abs(s.camera.worldView[3] - 1214) < 0.01,
    );
    await p.tap("#return-juni");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
  }
  const end = await state(p);
  assert.equal(
    end.chunks.events.filter((x) => x.event === "request").length,
    1,
  );
  rows.push({
    case: "five complete overview / native follow cycles / all chunks preloaded without repeat requests",
    pass: true,
    state: end,
  });
  await p.close();
  await fs.writeFile(
    "docs/gate25-polish/controls-qa.json",
    JSON.stringify({ rows, physicalDevices: "NOT TESTED" }, null, 2) + "\n",
  );
  console.log("PASS", rows.length, "touch/cache/export checks");
} finally {
  await b.close();
}
