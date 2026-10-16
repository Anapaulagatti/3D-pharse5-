import { chromium } from "playwright";
import fs from "node:fs/promises";
import { spawn, execFileSync } from "node:child_process";
import crypto from "node:crypto";
const reviewDir = process.env.PIXEL_REVIEW_DIR ?? "docs/world-refinement";
const manifest = JSON.parse(
  await fs.readFile(`${reviewDir}/package.json`, "utf8"),
);
// Extract the tracked exact ZIP into THIS checkout; never depend on a previous workspace.
const extractedRoot =
  process.cwd() +
  "/.cache/portable-http/" +
  manifest.zip_sha256 +
  "/Korean-Arena-Seoul-Refinement-Review";
execFileSync("python3", [
  "-c",
  "import sys,zipfile,pathlib,json,hashlib; p=pathlib.Path(sys.argv[2]); z=zipfile.ZipFile(sys.argv[1]); assert z.testzip() is None; assert all(not pathlib.Path(n).is_absolute() and '..' not in pathlib.Path(n).parts for n in z.namelist()); z.extractall(p.parent); j=json.load(open(sys.argv[3])); assert all(hashlib.sha256((p/'3D-pharse5-'/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in j['files'])",
  manifest.zip,
  extractedRoot,
  `${reviewDir}/package.json`,
]);
const server = spawn(
  "python3",
  [extractedRoot + "/start.py", "--port", "4202", "--no-browser"],
  { stdio: ["ignore", "pipe", "pipe"] },
);
let log = "";
server.stdout.on("data", (d) => (log += d));
server.stderr.on("data", (d) => (log += d));
const root = "http://127.0.0.1:4202/3D-pharse5-/";
let browser;
const errors = [],
  results = [];
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(root + "refinement-review.html")).ok) break;
    } catch {
      /* Wait only for this owned local launcher. */
    }
    if (i === 99) throw Error("Actual extracted launcher not ready: " + log);
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  for (const mobile of [false, true]) {
    const contexts = [];
    const hashes = [];
    for (const origin of [
      process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/",
      root,
    ]) {
      const context = await browser.newContext({
        viewport: mobile
          ? { width: 390, height: 844 }
          : { width: 1440, height: 1140 },
        deviceScaleFactor: 1,
        isMobile: mobile,
        hasTouch: mobile,
        reducedMotion: "reduce",
      });
      contexts.push(context);
      const p = await context.newPage();
      p.on("pageerror", (e) => errors.push(e.message));
      p.on("console", (m) => {
        if (m.type() === "error") errors.push(m.text());
      });
      p.on("response", (r) => {
        if (r.status() >= 400) errors.push(r.url());
      });
      await p.goto(origin + "refinement-review.html?qa&renderer=canvas");
      await p.waitForFunction(() => window.__SEOUL__?.ready);
      await p.evaluate(() => window.__SEOUL_TEST__.place(544, 1280));
      await p.waitForTimeout(350);
      const image = await p.locator("canvas").evaluate((c) => c.toDataURL());
      hashes.push(crypto.createHash("sha256").update(image).digest("hex"));
      if (origin === root && !mobile) {
        await p.evaluate(() => window.__SEOUL_TEST__.place(544, 1152));
        await p.waitForTimeout(120);
        await p.locator("#interact").click();
        await p.waitForFunction(() => window.__SEOUL__?.area === "room");
        await p.evaluate(() => window.__SEOUL_TEST__.place(385, 392));
        await p.waitForTimeout(100);
        await p.locator("#interact").click();
        await p.locator(".hangul-letter").waitFor();
        await p.locator("#close-dialog").click();
        await p.evaluate(() => window.__SEOUL_TEST__.place(384, 490));
        await p.waitForTimeout(100);
        await p.locator("#interact").click();
        await p.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
      }
    }
    if (hashes[0] !== hashes[1])
      throw Error(
        "Exact extracted ZIP Canvas differs from inspected source " +
          JSON.stringify({ mobile, hashes }),
      );
    results.push({
      device: mobile ? "emulated mobile Canvas" : "desktop Canvas",
      sourceAndExactZipPixelHash: hashes[0],
      equal: true,
    });
    for (const c of contexts) await c.close();
  }
  const prior = await browser.newPage();
  await prior.goto(root + "production-review.html?renderer=canvas");
  await prior.waitForFunction(() => window.__SEOUL__?.ready);
  const preserved = await prior.evaluate(() => window.__SEOUL__.world);
  if (preserved[0] !== 4096 || preserved[1] !== 1728)
    throw Error("Prior town missing");
  await prior.close();
  const p = await browser.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  await p.goto(root);
  await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  const old = await p.evaluate(() => window.__PIXEL_METRICS__);
  if (old.guests.length !== 4) throw Error("Preserved original guests missing");
  await p.close();
  if (errors.length) throw Error(JSON.stringify(errors));
  manifest.status = "VERIFIED_EXACT_ZIP_OVER_HTTP";
  manifest.httpVerification = {
    launcherExecuted: true,
    port: 4202,
    results,
    roomLessonAndReturn: true,
    originalGameGuests: old.guests.length,
    originalProductionWorld: preserved,
    errors,
  };
  await fs.writeFile(
    `${reviewDir}/package.json`,
    JSON.stringify(manifest, null, 2) + "\n",
  );
  console.log(
    JSON.stringify({
      status: manifest.status,
      zipSha256: manifest.zip_sha256,
      zipBytes: manifest.zip_bytes,
      files: manifest.files.length,
      results,
      errors,
    }),
  );
} finally {
  if (browser) await browser.close();
  server.kill("SIGINT");
}
