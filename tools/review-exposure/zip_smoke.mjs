import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync, spawn } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
const dir = "docs/review-exposure",
  proof = JSON.parse(
    await fs.readFile(dir + "/PRIVATE_PACKAGE_PROOF.json", "utf8"),
  );
const temp = await fs.mkdtemp(path.join(tmpdir(), "restricted20-launch-"));
execFileSync("python3", [
  "-c",
  "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])",
  proof.file,
  temp,
]);
const server = spawn(
  "python3",
  ["-u", path.join(temp, "KoreanPixelTown-20NPC-PrivateReview/start.py")],
  { stdio: ["ignore", "pipe", "ignore"] },
);
let output = "";
server.stdout.on("data", (b) => (output += b.toString()));
let browser;
try {
  for (let i = 0; i < 100 && !output.includes("one-session password:"); i++)
    await new Promise((r) => setTimeout(r, 50));
  const base = output.match(
      /Open (http:\/\/127\.0\.0\.1:\d+\/3D-pharse5-review\/)/,
    )?.[1],
    password = output.match(/one-session password: (\S+)/)?.[1];
  if (!base || !password)
    throw Error("Standalone startup did not produce local review");
  const r = await fetch(base);
  if (r.status !== 401) throw Error("Private startup exposed anonymously");
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const context = await browser.newContext({
    httpCredentials: { username: "review", password },
    viewport: { width: 960, height: 640 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage(),
    errors = [],
    external = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (
      /^https?:/.test(r.url()) &&
      !r.url().startsWith(new URL(base).origin + "/")
    )
      external.push(r.url());
  });
  await page.goto(base);
  await page.locator("#roster article").nth(19).waitFor();
  if ((await page.locator("#roster article").count()) !== 20)
    throw Error("Extracted portal roster differs");
  await page.goto(base + "play/?qa&renderer=canvas&npcReview=npc-minseo");
  await page.waitForFunction(
    () =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-minseo"),
  );
  const state = await page.evaluate(() => ({
    total: window.__NPC_WORLD__.catalogTotal,
    archive: window.__NPC_WORLD__.historicalArchiveCount,
    active: window.__NPC_WORLD__.active,
    scale: window.__NPC_WORLD__.actors.find((a) => a.id === "npc-minseo")
      .nativeScale,
  }));
  if (
    state.total !== 20 ||
    state.archive !== 0 ||
    state.active > 4 ||
    !state.scale.every((v) => v === 1) ||
    errors.length ||
    external.length
  )
    throw Error("Extracted runtime regression");
  await page.screenshot({ path: dir + "/extracted-game.png" });
  proof.launch =
    "PASS extracted ZIP + actual bundled start.py, authenticated loopback, actual Phaser20 / archive0 / native1x / no external request";
  proof.extractedRuntime = state;
  proof.errors = errors;
  proof.externalRequests = external;
  proof.physicalDevices = "NOT TESTED";
} finally {
  server.kill();
  await browser?.close();
  await fs.rm(temp, { recursive: true, force: true });
}
await fs.writeFile(
  dir + "/PRIVATE_PACKAGE_PROOF.json",
  JSON.stringify(proof, null, 2) + "\n",
);
