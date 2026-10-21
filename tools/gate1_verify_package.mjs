import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
import { execFileSync, spawn } from "node:child_process";
const archive = "docs/gate1/GATE1_PLAYABLE.zip";
const sha256 = createHash("sha256")
  .update(await fs.readFile(archive))
  .digest("hex");
const extracted = `${process.cwd()}/.cache/gate1-package-check/${sha256}`;
execFileSync("python3", [
  "-c",
  "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])",
  archive,
  extracted,
]);
const root = extracted + "/Korean-Arena-Gate1";
const server = spawn(
  "python3",
  [root + "/start.py", "--port", "0", "--no-browser"],
  { stdio: ["ignore", "pipe", "ignore"] },
);
let browser;
try {
  const url = await new Promise((resolve, reject) => {
    let output = "";
    const timer = setTimeout(
      () => reject(Error("Package HTTP startup timeout")),
      10000,
    );
    server.stdout.on("data", (data) => {
      output += data;
      const match = output.match(/http:\/\/127\.0\.0\.1:\d+\/\S+/);
      if (match) {
        clearTimeout(timer);
        resolve(match[0]);
      }
    });
    server.on("error", reject);
  });
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
  });
  const errors = [],
    rows = [];
  for (const mobile of [false, true]) {
    const context = await browser.newContext({
      viewport: mobile
        ? { width: 844, height: 390 }
        : { width: 1440, height: 1140 },
      isMobile: mobile,
      hasTouch: mobile,
      reducedMotion: "reduce",
      serviceWorkers: "block",
    });
    const page = await context.newPage();
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    page.on("request", (r) => {
      if (/\/assets\/world\/|\/v[1-9](?:0)?-(?:world|city)\//.test(r.url()))
        errors.push("Legacy request " + r.url());
    });
    const response = await page.goto(String(url));
    await page.waitForFunction(() => window.__GATE1__?.ready);
    if (await page.evaluate(() => !!window.__GATE1_TEST__))
      throw Error("Normal entry exposes QA hook");
    const start = await page.evaluate(() => window.__GATE1__.x);
    if (mobile) {
      const cdp = await context.newCDPSession(page),
        b = await page.locator("#joystick").boundingBox(),
        x = b.x + b.width / 2,
        y = b.y + b.height / 2;
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x, y, id: 1 }],
      });
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchMove",
        touchPoints: [{ x: x + b.width * 0.3, y, id: 1 }],
      });
      await page.waitForFunction((x) => window.__GATE1__.x > x + 14, start);
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
    } else {
      await page.locator("canvas").focus();
      await page.keyboard.down("ArrowRight");
      await page.waitForFunction((x) => window.__GATE1__.x > x + 14, start);
      await page.keyboard.up("ArrowRight");
    }
    rows.push({
      mobile,
      http: response.status(),
      moved: await page.evaluate((x) => window.__GATE1__.x - x, start),
      frame: await page.evaluate(() => window.__PLAZA_REVIEW__.frame),
      url: page.url(),
    });
    await context.close();
  }
  const manifest = JSON.parse(
    await fs.readFile(root + "/build-manifest.json", "utf8"),
  );
  for (const [path, want] of Object.entries(manifest)) {
    const a = await fs.readFile(root + "/site/3D-pharse5-/" + path),
      b = await fs.readFile("dist-gate1/" + path);
    if (createHash("sha256").update(a).digest("hex") !== want || !a.equals(b))
      throw Error("Package mismatch " + path);
  }
  const proof = {
    status: errors.length ? "FAIL" : "PASS",
    source:
      "Actual extracted ZIP via Python HTTP launcher; normal-entry desktop keyboard and emulated-mobile CDP touch",
    zipSha256: sha256,
    rows,
    errors,
    exactBuildFiles: Object.keys(manifest).length,
  };
  await fs.writeFile(
    "docs/gate1/package-verification.json",
    JSON.stringify(proof, null, 2) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(JSON.stringify(proof));
} finally {
  if (browser) await browser.close();
  server.kill("SIGTERM");
}
