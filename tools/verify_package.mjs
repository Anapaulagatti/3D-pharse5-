import { chromium } from "playwright";
import fs from "node:fs/promises";
import { spawn, execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";
const zip = "docs/v9-world/playable-review.zip";
const zipHash = createHash("sha256")
    .update(await fs.readFile(zip))
    .digest("hex"),
  dest = process.cwd() + "/.cache/v9-package/" + zipHash;
execFileSync("python3", [
  "-c",
  "import zipfile,sys,pathlib;z=zipfile.ZipFile(sys.argv[1]);assert all('..'not in pathlib.PurePosixPath(n).parts for n in z.namelist());z.extractall(sys.argv[2])",
  zip,
  dest,
]);
const root = dest + "/Korean-Arena-V9-World-Review",
  manifest = JSON.parse(
    await fs.readFile(root + "/REVIEW_MANIFEST.json", "utf8"),
  );
for (const r of manifest.files) {
  const bytes = await fs.readFile(root + "/" + r.file);
  assert.equal(createHash("sha256").update(bytes).digest("hex"), r.sha256);
}
const server = spawn(
  "python3",
  [root + "/start.py", "--port", "4278", "--no-browser"],
  { stdio: "ignore" },
);
let browser;
const errors = [],
  rows = [];
const output = "docs/v9-world/quality/package";
await fs.mkdir(output, { recursive: true });
try {
  for (let i = 0; i < 100; i++) {
    try {
      if (
        (await fetch("http://127.0.0.1:4278/3D-pharse5-/v9-world-review.html"))
          .ok
      )
        break;
    } catch {
      /* task-owned server is starting */
    }
    if (i === 99) throw Error("ZIP HTTP launcher unavailable");
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
  });
  async function boot(base, options = {}) {
    const c = await browser.newContext({
        viewport: { width: 1440, height: 1140 },
        deviceScaleFactor: 1,
        reducedMotion: "reduce",
        ...options,
      }),
      p = await c.newPage();
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("console", (e) => {
      if (e.type() === "error") errors.push(e.text());
    });
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(base + "v9-world-review.html?qa&renderer=canvas");
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    return { c, p };
  }
  async function place(p, x, y) {
    await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
    await p.waitForFunction(
      (n) => window.__PIXEL_METRICS__.frameCount > n + 5,
      n,
    );
  }
  for (const [id, x, y] of [
    ["civic", 2176, 3056],
    ["namsan", 3520, 2960],
    ["station", 1376, 3960],
    ["leisure", 3408, 3912],
    ["coast", 2560, 4760],
    ["jeju", 1536, 5552],
  ]) {
    const results = [];
    for (const [kind, base] of [
      ["source", "http://127.0.0.1:4201/3D-pharse5-/"],
      ["zip", "http://127.0.0.1:4278/3D-pharse5-/"],
    ]) {
      const { c, p } = await boot(base);
      try {
        await place(p, x, y);
        const data = await p
          .locator("canvas")
          .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
        const bytes = Buffer.from(data.png.split(",")[1], "base64");
        results.push({
          kind,
          hash: createHash("sha256").update(bytes).digest("hex"),
          size: data.size,
        });
        if (kind === "zip") await fs.writeFile(`${output}/${id}.png`, bytes);
      } finally {
        await c.close();
      }
    }
    assert.equal(
      results[0].hash,
      results[1].hash,
      id + " source/ZIP native canvas differs",
    );
    rows.push({ id, results });
  }
  const { c, p } = await boot("http://127.0.0.1:4278/3D-pharse5-/", {
    viewport: { width: 844, height: 390 },
    hasTouch: true,
    isMobile: true,
  });
  try {
    await place(p, 2560, 4880);
    await p.locator("#interact").click();
    await p.locator("#travel-go").click();
    await p.waitForFunction(() => window.__SEOUL__.y > 5000);
    const arrival = await p.evaluate(() => [
      window.__SEOUL__.x,
      window.__SEOUL__.y,
    ]);
    assert.deepEqual(arrival, [1984, 5504]);
    const d = await c.newCDPSession(p),
      b = await p.locator("#joystick").boundingBox(),
      cx = b.x + b.width / 2,
      cy = b.y + b.height / 2;
    await d.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: cx, y: cy, id: 1 }],
    });
    await d.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: cx - b.width * 0.28, y: cy, id: 1 }],
    });
    await p.waitForFunction(() => window.__SEOUL__.x < 1968);
    await d.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    await place(p, 1536, 5976);
    await p.locator("#interact").click();
    await p.locator('[data-discovery="false"]').first().click();
    assert.match(
      await p.locator("#discovery-feedback").innerText(),
      /Chưa đúng/,
    );
    await p.locator('[data-discovery="true"]').click();
    assert.equal(
      await p.evaluate(() => window.__WORLD_REVIEW__.discoveryFound),
      true,
    );
    await p.locator("#close-dialog").click();
    await place(p, 2064, 5408);
    await p.locator("#interact").click();
    await p.locator("#travel-go").click();
    await p.waitForFunction(() => window.__SEOUL__.y < 5000);
    assert.deepEqual(
      await p.evaluate(() => [window.__SEOUL__.x, window.__SEOUL__.y]),
      [2560, 4760],
    );
    await place(p, 1568, 1120);
    await p.locator("#interact").click();
    await p.waitForFunction(() => window.__SEOUL__.area === "room");
    await place(p, 385, 392);
    await p.locator("#interact").click();
    await p.locator(".hangul-letter").waitFor({ state: "visible" });
    await p.locator("#close-dialog").click();
    await place(p, 384, 490);
    await p.locator("#interact").click();
    await p.waitForFunction(() => window.__SEOUL__.area === "outdoor");
    await p.setViewportSize({ width: 390, height: 844 });
    await p.locator("#rotate-screen").waitFor({ state: "visible" });
    assert.equal(await p.evaluate(() => window.__PIXEL_METRICS__.paused), true);
    await p.setViewportSize({ width: 844, height: 390 });
    await p.locator("#rotate-screen").waitFor({ state: "hidden" });
    await p.goto(
      "http://127.0.0.1:4278/3D-pharse5-/v9-world-review.html?renderer=canvas",
    );
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    assert.equal(await p.evaluate(() => !!window.__SEOUL_TEST__), false);
    const before = await p.evaluate(() => window.__SEOUL__.y);
    await p.locator("canvas").focus();
    await p.keyboard.down("ArrowDown");
    await p.waitForFunction(
      (before) => window.__SEOUL__.y > before + 16,
      before,
    );
    await p.keyboard.up("ArrowDown");
    rows.push({
      id: "zip-mobile-live-systems",
      normalEntryWalk: true,
      analogAfterFerry: true,
      reciprocalFerry: true,
      academyLessonReturn: true,
      basaltWrongAndCorrect: true,
      portraitPause: true,
    });
  } finally {
    await c.close();
  }
  assert.deepEqual(errors, []);
  const proof = {
    status: "PASS",
    zipSha256: zipHash,
    sourceCheckpoint: manifest.sourceCheckpoint,
    allDistributionFileHashesVerified: manifest.files.length,
    method:
      "Extract actual ZIP, run its own Python HTTP server and compare actual native Phaser renders with source; no raw HTML/source-only acceptance.",
    rows,
    errors,
  };
  await fs.writeFile(
    output + "/http-verification.json",
    JSON.stringify(proof, null, 2),
  );
  const metadata = JSON.parse(
    await fs.readFile("docs/v9-world/package.json", "utf8"),
  );
  metadata.httpVerified = true;
  metadata.proof = "quality/package/http-verification.json";
  await fs.writeFile(
    "docs/v9-world/package.json",
    JSON.stringify(metadata, null, 2) + "\n",
  );
  console.log(
    "Actual ZIP HTTP/native parity/mobile/ferry/Academy/discovery PASS",
  );
} finally {
  if (browser) await browser.close();
  server.kill("SIGINT");
}
