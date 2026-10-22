import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
const server = spawn(
  "python3",
  [".cache/gate25-reconstruction/extracted/start.py", "--port", "4278"],
  { stdio: "ignore" },
);
await new Promise((r) => setTimeout(r, 600));
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [],
  errors = [];
try {
  for (const id of [
    "a",
    "b",
    "c",
    "transition",
    "station",
    "original",
    "seam",
    "jeju-fit",
    "district",
    "jeju25",
    "district-polish",
    "district-reconstruction",
  ]) {
    const p = await b.newPage({
      viewport: { width: 844, height: 390 },
      isMobile: true,
      hasTouch: true,
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(
      "http://127.0.0.1:4278/3D-pharse5-/gate2-review.html?scene=" + id,
    );
    await p.waitForFunction(() => window.__GATE2__?.camera);
    assert.equal(
      await p.evaluate(() => typeof window.__GATE2_TEST__),
      "undefined",
    );
    const start = await p.evaluate(() => window.__GATE2__);
    await p.keyboard.down("d");
    await p.waitForTimeout(250);
    await p.keyboard.up("d");
    const moved = await p.evaluate(() => window.__GATE2__);
    assert(moved.x > start.x + 5, id);
    await p.tap("#scenic");
    await p.waitForTimeout(100);
    assert.equal(
      await p.evaluate(() => window.__GATE2__.camera.mode),
      "scenic",
    );
    await p.tap("#overview-mode");
    await p.waitForFunction(() => window.__GATE2__.camera.mode === "overview");
    assert.equal(
      await p.evaluate(() => window.__GATE2__.camera.mode),
      "overview",
    );
    await p.tap("#return-juni");
    await p.waitForTimeout(400);
    assert.equal(
      await p.evaluate(() => window.__GATE2__.camera.mode),
      "follow",
    );
    if (id === "c") {
      await p.tap("#scenic");
      await p.tap("#start-tour");
      await p.waitForFunction(() => window.__GATE2__.camera.mode === "tour");
      await p.waitForTimeout(350);
      await p.tap("#tour-pause");
      await p.tap("#tour-next");
      await p.waitForFunction(() => window.__GATE2__.camera.tour.index === 1);
      await p.tap("#return-juni");
      await p.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
    }
    rows.push({
      scene: id,
      pass: true,
      extractedZIP: true,
      noQaHook: true,
      actualInputAndCameraModes: true,
    });
    await p.close();
  }
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    "docs/gate25-reconstruction/package-qa.json",
    JSON.stringify({ rows, errors }, null, 2) + "\n",
  );
  console.log("PASS", rows.length, "extracted packaged scene entries");
} finally {
  await b.close();
  server.kill();
}
