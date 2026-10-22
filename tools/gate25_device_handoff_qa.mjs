import { chromium } from "@playwright/test";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
const D = "docs/gate25-device-review",
  server = spawn(
    "python3",
    [".cache/gate25-device-review/extracted/start.py", "--port", "4286"],
    { stdio: "ignore" },
  );
const browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
  }),
  rows = [],
  errors = [];
try {
  for (let n = 0; n < 30; n++) {
    try {
      if ((await fetch("http://127.0.0.1:4286/")).ok) break;
    } catch {
      // Retry while the local test server starts.
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  for (const id of ["district-refinement", "c"]) {
    const p = await browser.newPage({
      viewport: { width: 844, height: 390 },
      isMobile: true,
      hasTouch: true,
      acceptDownloads: true,
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(
      "http://127.0.0.1:4286/3D-pharse5-/gate2-review.html?scene=" + id,
    );
    await p.waitForFunction(() => window.__GATE2__?.ready);
    assert.equal(
      await p.evaluate(() => typeof window.__GATE2_TEST__),
      "undefined",
    );
    if (id === "district-refinement") {
      const origin = await p.evaluate(() => window.__GATE2__),
        box = await p.locator("#joystick").boundingBox();
      assert(box);
      const cx = box.x + box.width / 2,
        cy = box.y + box.height / 2,
        c = await p.context().newCDPSession(p);
      await c.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x: cx, y: cy, id: 1 }],
      });
      await c.send("Input.dispatchTouchEvent", {
        type: "touchMove",
        touchPoints: [{ x: cx + 30, y: cy, id: 1 }],
      });
      await p.waitForTimeout(500);
      await c.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
      await p.waitForTimeout(100);
      const moved = await p.evaluate(() => window.__GATE2__);
      assert(moved.x > origin.x + 3);
      const x = moved.x;
      await p.waitForTimeout(150);
      assert(Math.abs((await p.evaluate(() => window.__GATE2__)).x - x) < 1);
    }
    await p.tap("#scenic");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "scenic");
    await p.tap("#overview-mode");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "overview");
    await p.tap("#return-juni");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
    if (id === "c") {
      await p.tap("#scenic");
      await p.tap("#start-tour");
      await p.waitForFunction(() => window.__GATE2__.camera.mode === "tour");
      await p.tap("#tour-pause");
      await p.tap("#tour-next");
      await p.waitForFunction(() => window.__GATE2__.camera.tour.index === 1);
      await p.tap("#return-juni");
      await p.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
    }
    await p.tap("#settings > summary");
    const dl = p.waitForEvent("download");
    await p.tap("#export-session");
    const download = await dl;
    const location = ".cache/gate25-device-review/" + id + "-export.json";
    await download.saveAs(location);
    const report = JSON.parse(await fs.readFile(location, "utf8"));
    assert.equal(report.state.scene, id);
    assert(
      report.physicalDeviceVerification.includes("NOT AUTOMATICALLY VERIFIED"),
    );
    assert(report.userAgent);
    assert.deepEqual(report.viewport, [844, 390]);
    assert(report.state.session);
    assert(report.state.camera);
    rows.push({
      scene: id,
      pass: true,
      normalEntry: true,
      exportDownload: download.suggestedFilename(),
      exportTopLevelFields: Object.keys(report),
      physicalDeviceVerification: report.physicalDeviceVerification,
      physicalDevice: false,
      desktopChromiumTouchEmulation: true,
    });
    await p.close();
  }
  for (const name of ["ANDROID", "IPHONE"]) {
    const t = JSON.parse(
      await fs.readFile(D + "/DEVICE_REPORT_" + name + ".json", "utf8"),
    );
    assert.equal(t.physicalDeviceStatus, "NOT TESTED");
    assert.equal(t.physicalDeviceConfirmed, false);
    assert(Object.values(t.checks).every((c) => c.status === "NOT TESTED"));
  }
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    D + "/handoff-qa.json",
    JSON.stringify(
      {
        purpose: "PACKAGING_AND_EXPORT_SMOKE_ONLY",
        rows,
        errors,
        reportTemplatesStartUntested: true,
        physicalAndroidChrome: "NOT TESTED",
        physicalIPhoneSafari: "NOT TESTED",
        artisticDistrictPrototype: "HUMAN_APPROVED",
        gate3: "LOCKED",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS frozen extracted ZIP / actual emulated touch / existing camera/tour / report downloads / blank device templates. Physical devices NOT TESTED.",
  );
} finally {
  await browser.close();
  server.kill();
}
