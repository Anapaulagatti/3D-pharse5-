/** Media playback, nested assets, privacy, and denied paths from the exact export. */
import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { randomBytes, createHash } from "node:crypto";
const root = process.env.REVIEW_OUT ?? ".cache/review-portal";
const prefix = process.env.VITE_REVIEW_BASE ?? "/3D-pharse5-review/";
const url = "http://127.0.0.1:4493" + prefix;
const password = randomBytes(24).toString("hex"),
  username = "review-extra";
const server = spawn(
  "python3",
  [
    "tools/review-portal/serve.py",
    "--root",
    root,
    "--port",
    "4493",
    "--base",
    prefix,
  ],
  {
    env: { ...process.env, REVIEW_USER: username, REVIEW_PASSWORD: password },
    stdio: "ignore",
  },
);
const result = {
  status: "RUNNING",
  checks: [],
  errors: [],
  missing: [],
  physicalDevices: "NOT_TESTED",
};
let browser;
const assert = (v, message) => {
  if (!v) throw Error(message);
};
try {
  for (let i = 0; i < 100; i++) {
    try {
      await fetch(url);
      break;
    } catch {
      await new Promise((r) => setTimeout(r, 150));
    }
  }
  const headers = {
    Authorization:
      "Basic " + Buffer.from(username + ":" + password).toString("base64"),
  };
  for (const path of [
    ".env",
    ".git/config",
    "docs/phase3b-a/RIGHTS_MATRIX.json",
    "assets-src/rights/npc-inventory.json",
    "../index.html",
  ]) {
    const r = await fetch(url + path, { headers });
    assert(r.status === 404, "Disallowed file accessible: " + path);
  }
  const manifest = JSON.parse(
    await fs.readFile(root + "/export-manifest.json", "utf8"),
  );
  for (const row of manifest.files) {
    const bytes = await fs.readFile(root + "/" + row.filename);
    assert(
      createHash("sha256").update(bytes).digest("hex") === row.sha256,
      "Export hash mismatch",
    );
    assert(
      !/(?:^|\/)(?:\.env|\.git|source-master|ART_PROVENANCE|npc-inventory|provenance\.json)(?:\/|\.|$)/i.test(
        row.filename,
      ),
      "Disallowed raw audit/source exported",
    );
    if (/\.(js|json|html|css|mjs|md)$/.test(row.filename))
      assert(
        !/gh[pousr]_[a-zA-Z0-9]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----/.test(
          bytes.toString(),
        ),
        "Secret-shaped content found",
      );
  }
  result.checks.push({
    name: "manifest hashes +private files absent +denied paths",
    files: manifest.files.length,
    status: "PASS",
  });
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    httpCredentials: { username, password },
  });
  const p = await context.newPage();
  p.on("pageerror", (e) => result.errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400 && r.status() !== 401)
      result.missing.push({ url: r.url(), status: r.status() });
  });
  await p.goto(url);
  await p.locator(".roster article").nth(25).waitFor();
  // Natural scrolling triggers lazy thumbnails; do not change their loading policy.
  for (
    let y = 0;
    y < (await p.evaluate(() => document.documentElement.scrollHeight));
    y += 600
  ) {
    await p.evaluate((y) => window.scrollTo(0, y), y);
    await p.waitForTimeout(100);
  }
  await p.waitForFunction(() =>
    [...document.querySelectorAll(".roster img")].every(
      (i) => i.complete && i.naturalWidth === 96,
    ),
  );
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.screenshot({
    path: "docs/review-portal/screenshots/desktop.png",
    fullPage: true,
  });
  for (let i = 0; i < 4; i++) {
    await p.locator("#movies article").nth(i).locator("button").click();
    const v = p.locator("#movies article").nth(i).locator("video");
    await v.evaluate(async (element) => {
      await element.play();
    });
    await p.waitForTimeout(300);
    const state = await v.evaluate((element) => ({
      time: element.currentTime,
      duration: element.duration,
      width: element.videoWidth,
      height: element.videoHeight,
      error: element.error?.message,
    }));
    assert(
      state.time > 0 && state.duration > 0 && state.width > 0 && !state.error,
      "Video did not actually play",
    );
    await v.evaluate((element) => element.pause());
    result.checks.push({
      name: "checkpoint video " + i,
      status: "PASS",
      ...state,
    });
  }
  const history = JSON.parse(await fs.readFile(root + "/history.json", "utf8"));
  const path = history.snapshots[0].path;
  const manifestResponse = await fetch(url + path + "export-manifest.json", {
    headers,
  });
  assert(manifestResponse.status === 200, "Snapshot manifest not accessible");
  await p.goto(url + path + "play/?qa&renderer=canvas&npcReview=npc-minseo");
  await p.waitForFunction(
    () =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-minseo"),
  );
  await p.locator("#portal-review-controls summary").click();
  await p.locator("#portal-review-controls a").click();
  await p.waitForURL(url + path);
  result.checks.push({
    name: "nested snapshot actual Phaser +lazy assets +return",
    status: "PASS",
  });
  await p.setViewportSize({ width: 390, height: 844 });
  await p.goto(url);
  await p.locator(".roster article").nth(25).waitFor();
  for (
    let y = 0;
    y < (await p.evaluate(() => document.documentElement.scrollHeight));
    y += 700
  ) {
    await p.evaluate((y) => window.scrollTo(0, y), y);
    await p.waitForTimeout(80);
  }
  await p.waitForFunction(() =>
    [...document.querySelectorAll(".roster img")].every((i) => i.complete),
  );
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.screenshot({
    path: "docs/review-portal/screenshots/mobile-390.png",
    fullPage: true,
  });
  assert(
    !result.errors.length && !result.missing.length,
    "Browser/resource regression",
  );
  result.status = "PASS";
} catch (e) {
  result.status = "FAIL";
  result.failure = e.stack;
  console.error(e);
  process.exitCode = 1;
} finally {
  await fs.writeFile(
    "docs/review-portal/EXTRA_SMOKE.json",
    JSON.stringify(result, null, 2) + "\n",
  );
  await browser?.close();
  server.kill("SIGTERM");
}
