import { chromium } from "playwright";
import fs from "node:fs/promises";
import { spawn, execFileSync } from "node:child_process";
import crypto from "node:crypto";
const dir = process.env.PIXEL_REVIEW_DIR ?? "docs/modern-streets",
  m = JSON.parse(await fs.readFile(dir + "/package.json", "utf8"));
const extracted =
  process.cwd() +
  "/.cache/portable-http/" +
  m.zip_sha256 +
  "/Korean-Arena-Modern-Streets-Review";
execFileSync("python3", [
  "-c",
  "import sys,zipfile,pathlib,json,hashlib;p=pathlib.Path(sys.argv[2]);z=zipfile.ZipFile(sys.argv[1]);assert z.testzip()is None;assert all(not pathlib.Path(n).is_absolute()and '..'not in pathlib.Path(n).parts for n in z.namelist());z.extractall(p.parent);j=json.load(open(sys.argv[3]));assert all(hashlib.sha256((p/'3D-pharse5-'/r['path']).read_bytes()).hexdigest()==r['sha256']for r in j['files'])",
  m.zip,
  extracted,
  dir + "/package.json",
]);
const server = spawn(
    "python3",
    [extracted + "/start.py", "--port", "4202", "--no-browser"],
    { stdio: "ignore" },
  ),
  root = "http://127.0.0.1:4202/3D-pharse5-/",
  source =
    process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
let b;
const errors = [],
  results = [];
const hash = (x) => crypto.createHash("sha256").update(x).digest("hex");
async function settle(p) {
  const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount > n + 4,
    n,
  );
}
async function place(p, x, y) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
  await settle(p);
}
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(root + "modern-streets-review.html")).ok) break;
    } catch {
      /* owned launcher */
    }
    if (i === 99) throw Error("Launcher not ready");
    await new Promise((r) => setTimeout(r, 100));
  }
  b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  for (const mobile of [false, true]) {
    const images = [];
    for (const origin of [source, root]) {
      const c = await b.newContext({
          viewport: mobile
            ? { width: 844, height: 390 }
            : { width: 1440, height: 1140 },
          deviceScaleFactor: 1,
          isMobile: mobile,
          hasTouch: mobile,
          reducedMotion: "reduce",
        }),
        p = await c.newPage();
      p.on("pageerror", (e) => errors.push(e.message));
      p.on("console", (m) => {
        if (m.type() === "error") errors.push(m.text());
      });
      p.on("response", (r) => {
        if (r.status() >= 400) errors.push(r.url());
      });
      await p.goto(origin + "modern-streets-review.html?qa&renderer=canvas");
      await p.waitForFunction(() => window.__FULL_WORLD__?.world[0] === 4352);
      const captures = [];
      for (const [x, y] of [
        [2176, 1328],
        [832, 2912],
        [3712, 2896],
        [2048, 2944],
        [2240, 4208],
      ]) {
        await place(p, x, y);
        captures.push(
          hash(await p.locator("canvas").evaluate((c) => c.toDataURL())),
        );
      }
      if (mobile) {
        await p.setViewportSize({ width: 390, height: 844 });
        await p.locator("#rotate-screen").waitFor({ state: "visible" });
        await p.waitForTimeout(200);
        captures.push(hash(await p.locator("#rotate-screen").screenshot()));
        await p.setViewportSize({ width: 844, height: 390 });
        await p.locator("#rotate-screen").waitFor({ state: "hidden" });
      }
      if (origin === root && !mobile) {
        await place(p, 2848, 3136);
        await p.locator("#interact").click();
        await p.locator("#travel-go").click();
        await p.waitForFunction(
          () => window.__FULL_WORLD__?.district === "jeju",
        );
        await place(p, 2144, 4608);
        await p.locator("#interact").click();
        await p.locator('button[data-discovery="false"]').first().click();
        if (
          !(await p.locator("#discovery-feedback").textContent()).includes(
            "Chưa đúng",
          )
        )
          throw Error("Discovery retry missing");
        await p.locator('button[data-discovery="true"]').click();
        await p.waitForFunction(() => window.__V3_WORLD__?.discoveryFound);
        await p.locator("#close-dialog").click();
        await place(p, 1760, 4544);
        await p.locator("#interact").click();
        await p.locator("#travel-go").click();
        await p.waitForFunction(
          () => window.__FULL_WORLD__?.district === "busan-coast",
        );
        await place(p, 1568, 1120);
        await p.locator("#interact").click();
        await p.waitForFunction(() => window.__SEOUL__?.area === "room");
        await place(p, 385, 392);
        await p.locator("#interact").click();
        await p.locator(".hangul-letter").waitFor();
        await p.locator("#close-dialog").click();
        await place(p, 384, 490);
        await p.locator("#interact").click();
        await p.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
      }
      images.push(captures);
      await c.close();
    }
    if (JSON.stringify(images[0]) !== JSON.stringify(images[1]))
      throw Error(
        "Source/ZIP pixels differ " + JSON.stringify({ mobile, images }),
      );
    results.push({
      device: mobile ? "emulated landscape mobile Canvas" : "desktop Canvas",
      fiveDistrictNativePixelHashes: images[0].slice(0, 5),
      portraitHash: images[0][5] ?? null,
      equal: true,
    });
  }
  const p = await b.newPage();
  await p.goto(root + "production-review.html?renderer=canvas");
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  const prior = await p.evaluate(() => window.__SEOUL__.world);
  if (prior[0] !== 4096 || prior[1] !== 1728) throw Error("Prior town missing");
  await p.goto(root);
  await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  const old = await p.evaluate(() => window.__PIXEL_METRICS__);
  if (old.guests.length !== 4) throw Error("Original guests missing");
  if (errors.length) throw Error(JSON.stringify(errors));
  m.status = "VERIFIED_EXACT_ZIP_OVER_HTTP";
  m.httpVerification = {
    launcherExecuted: true,
    port: 4202,
    results,
    reciprocalPublicFerry: true,
    retainedAcademyLessonAndReturn: true,
    originalBasaltDiscoveryRetryAndCompletion: true,
    originalGuests: 4,
    priorProductionWorld: prior,
    errors,
  };
  await fs.writeFile(dir + "/package.json", JSON.stringify(m, null, 2) + "\n");
  console.log(
    JSON.stringify({
      status: m.status,
      zipSha256: m.zip_sha256,
      files: m.files.length,
      results,
      errors,
    }),
  );
} finally {
  if (b) await b.close();
  server.kill("SIGINT");
}
