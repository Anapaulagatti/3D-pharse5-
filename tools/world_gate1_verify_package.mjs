import { chromium } from "@playwright/test";
import { spawn, execFileSync } from "node:child_process";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";
const path = ".cache/world-gate1-extracted";
await fs.rm(path, { recursive: true, force: true });
await fs.mkdir(path, { recursive: true });
execFileSync("python3", [
  "-m",
  "zipfile",
  "-e",
  "docs/world-gate1/WORLD_GATE1_PLAYABLE.zip",
  path,
]);
const folder = path + "/Korean-Arena-World-Gate1";
const manifest = JSON.parse(await fs.readFile(folder + "/files.json", "utf8"));
for (const f of manifest) {
  const b = await fs.readFile(folder + "/" + f.path);
  assert.equal(createHash("sha256").update(b).digest("hex"), f.sha256);
}
const server = spawn("python3", [folder + "/start.py"], {
  stdio: ["ignore", "pipe", "ignore"],
});
const url = await new Promise((resolve, reject) => {
  const t = setTimeout(() => reject(Error("Server startup timeout")), 10000);
  server.stdout.once("data", (b) => {
    clearTimeout(t);
    resolve(String(b).trim());
  });
});
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [];
try {
  const p = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto(url);
  await p.waitForFunction(() => window.__WORLD_PLAN__?.ready);
  assert.equal(
    await p.evaluate(() => typeof window.__WORLD_PLAN_TEST__),
    "undefined",
  );
  const x = await p.evaluate(() => window.__WORLD_PLAN__.x);
  await p.keyboard.down("ArrowRight");
  await p.waitForTimeout(800);
  await p.keyboard.up("ArrowRight");
  assert(await p.evaluate((x) => window.__WORLD_PLAN__.x > x + 25, x));
  await p.getByRole("link", { name: "Quy chuẩn hình ảnh" }).click();
  await p.evaluate(() =>
    Promise.all([...document.images].map((i) => i.decode())),
  );
  await p.close();
  const m = await browser.newPage({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await m.goto(url);
  await m.waitForFunction(() => window.__WORLD_PLAN__?.ready);
  const start = await m.evaluate(() => window.__WORLD_PLAN__.x),
    b = await m.locator("#joystick").boundingBox(),
    cdp = await m.context().newCDPSession(m);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: b.x + b.width / 2 + 32, y: b.y + b.height / 2 }],
  });
  await m.waitForTimeout(900);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  assert(await m.evaluate((x) => window.__WORLD_PLAN__.x > x + 25, start));
  await m.close();
  assert.equal(errors.length, 0, JSON.stringify(errors));
  const result = {
    status: "PASS",
    filesVerified: manifest.length,
    checks: [
      "Actual ZIP extracted and all manifest files SHA256 matched",
      "Own packaged Python HTTP launcher",
      "Desktop real keyboard, normal entry has no QA hook",
      "Style-bible reference PNGs decode over HTTP",
      "Mobile landscape real CDP touch",
    ],
    errors,
  };
  await fs.writeFile(
    "docs/world-gate1/package-verification.json",
    JSON.stringify(result, null, 2) + "\n",
  );
  console.log(JSON.stringify(result));
} finally {
  await browser.close();
  server.kill();
}
