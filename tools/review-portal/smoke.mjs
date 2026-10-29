import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { randomBytes } from "node:crypto";
const root = process.env.REVIEW_OUT ?? ".cache/review-portal";
const prefix = process.env.VITE_REVIEW_BASE ?? "/3D-pharse5-review/";
const origin = "http://127.0.0.1:4492",
  base = origin + prefix;
const password = randomBytes(24).toString("hex"),
  username = "review-smoke";
const server = spawn(
  "python3",
  [
    "tools/review-portal/serve.py",
    "--root",
    root,
    "--port",
    "4492",
    "--base",
    prefix,
  ],
  {
    env: { ...process.env, REVIEW_USER: username, REVIEW_PASSWORD: password },
    stdio: ["ignore", "pipe", "pipe"],
  },
);
let stderr = "";
server.stderr.on("data", (b) => {
  stderr += b;
});
const evidence = {
  status: "RUNNING",
  base: prefix,
  anonymous: {},
  rows: [],
  errors: [],
  missing: [],
  external: [],
  physicalDevices: "NOT_TESTED",
};
const dest = "docs/review-portal";
const save = () =>
  fs.writeFile(
    dest + "/PORTAL_SMOKE.json",
    JSON.stringify(evidence, null, 2) + "\n",
  );
let browser;
const assert = (value, message) => {
  if (!value) throw Error(message);
};
try {
  for (let i = 0; i < 100; i++) {
    try {
      await fetch(base);
      break;
    } catch {
      await new Promise((r) => setTimeout(r, 150));
    }
  }
  for (const file of [
    "",
    "play/",
    "catalog.json",
    "play/assets/main-BVEfAx5q.js",
    "export-manifest.json",
    "phases/3b-a/47107da9/play/",
  ]) {
    const response = await fetch(base + file);
    evidence.anonymous[file] = response.status;
    assert(response.status === 401, "Anonymous resource exposed: " + file);
  }
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 1,
    httpCredentials: { username, password },
  });
  const page = await context.newPage();
  page.on("pageerror", (e) => evidence.errors.push(e.message));
  page.on("response", (r) => {
    if (r.status() >= 400 && r.status() !== 401)
      evidence.missing.push({ url: r.url(), status: r.status() });
  });
  page.on("request", (r) => {
    if (r.url().startsWith("http") && !r.url().startsWith(origin + "/"))
      evidence.external.push(r.url());
  });
  await page.goto(base);
  await page.locator(".roster article").nth(25).waitFor();
  assert((await page.locator("video").count()) === 0, "Videos loaded eagerly");
  assert(
    (await page.locator("#version").textContent()).includes("47107da9"),
    "Wrong checked game SHA",
  );
  await fs.mkdir(dest + "/screenshots", { recursive: true });
  await page.screenshot({
    path: dest + "/screenshots/desktop.png",
    fullPage: true,
  });
  await page.locator("#search").fill("Junseo");
  assert(
    (await page.locator("#roster article").count()) === 1,
    "Fictional identity filter broken",
  );
  await page.locator("#search").fill("");
  await page
    .locator("#steps")
    .fill(
      "1. Mở phố thương mại\nMong đợi: NPC đọc được\nThực tế: review smoke",
    );
  await page.locator("#copy").click();
  assert(
    (await page.locator("#report").inputValue()).includes("47107da9"),
    "Bug report lost SHA",
  );
  const snapshot = "phases/3b-a/47107da9/";
  await page.goto(base + snapshot);
  await page.locator(".roster article").nth(25).waitFor();
  assert(
    (await page.locator("#snapshot-label").textContent()).startsWith(
      "SNAPSHOT",
    ),
    "Snapshot not distinguished",
  );
  evidence.rows.push({
    check: "portal +26 gallery +lazy media +search +feedback +snapshot",
    status: "PASS",
  });
  await save();
  // Seed original game records. QA links must not mutate those records.
  await page.evaluate(() => {
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "doyun" }),
    );
    localStorage.setItem(
      "korean-arena-npc-life-v1",
      JSON.stringify({
        version: 1,
        day: 7,
        minute: 345,
        seed: 123,
        scheduleCheckpoint: {},
      }),
    );
    window.sessionStorage.setItem(
      "korean-arena-world-session-v1",
      "preservation-sentinel",
    );
  });
  const preserved = await page.evaluate(() => [
    localStorage.getItem("korean-arena-player-preferences-v1"),
    localStorage.getItem("korean-arena-npc-life-v1"),
    window.sessionStorage.getItem("korean-arena-world-session-v1"),
  ]);
  const catalog = JSON.parse(await fs.readFile(root + "/catalog.json", "utf8"));
  for (const n of catalog.npcs) {
    await page.goto(
      base + "play/?qa&renderer=canvas&pixelAudit&npcReview=" + n.id,
    );
    await page.waitForFunction(
      (id) =>
        window.__GATE3__?.ready &&
        window.__NPC_WORLD__?.actors.some((a) => a.id === id),
      n.id,
      { timeout: 60000 },
    );
    const state = await page.evaluate(() => ({
      world: window.__GATE3__,
      npc: window.__NPC_WORLD__,
    }));
    assert(
      state.npc.catalogTotal === 26 &&
        state.npc.active <= 4 &&
        state.npc.assets.loaded <= 4 &&
        state.npc.assets.pending <= 2,
      "Caps/catalog failure",
    );
    assert(state.world.characterId === "juni", "QA preferences not isolated");
    await page.locator("#portal-review-controls summary").click();
    await page.locator("#portal-review-controls input").fill("1140");
    await page.locator("#portal-review-controls select").selectOption("0");
    await page
      .getByRole("button", { name: "Đặt giờ · REVIEW ONLY", exact: true })
      .click();
    await page.waitForFunction(
      () =>
        window.__NPC_WORLD__?.clock.minute === 1140 &&
        window.__NPC_WORLD__?.clock.rate === 0,
    );
    await page.locator("#portal-review-controls summary").click();
    const dx =
        state.npc.actors.find((a) => a.id === n.id).position[0] - state.world.x,
      dy =
        state.npc.actors.find((a) => a.id === n.id).position[1] - state.world.y;
    const key =
      Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
    await page.locator("#stage canvas").click({ position: { x: 320, y: 180 } });
    await page.keyboard.down(key);
    try {
      await page.waitForFunction(
        (id) => window.__NPC_WORLD__?.target === id,
        n.id,
        { timeout: 15000 },
      );
    } finally {
      await page.keyboard.up(key);
    }
    await page.keyboard.press("e");
    await page.locator("#npc-dialogue").waitFor({ state: "visible" });
    await page.locator("#npc-dialogue-return").click();
    const audit = await page.evaluate((id) => window.__NPC_CAPTURE__(id), n.id);
    assert(audit.matched, "No native Phaser draw");
    await fs.mkdir(".cache/review-native", { recursive: true });
    await fs.writeFile(
      `.cache/review-native/${n.id}.png`,
      Buffer.from(audit.png.split(",")[1], "base64"),
    );
    delete audit.png;
    delete audit.npc;
    delete audit.player;
    const after = await page.evaluate(() => window.__NPC_WORLD__);
    assert(!after.assets.errors.length, "Texture load failed");
    if (n.archive) {
      const metadata = JSON.parse(
        await fs.readFile(
          "assets-src/npcs/phase3a-final-six/metadata.json",
          "utf8",
        ),
      );
      const host = metadata.find((h) => h.id === n.id).hostResidentId;
      assert(
        !after.actors.some((a) => a.id === host),
        "Archive host overlapped",
      );
    }
    if (["npc-minseo", "npc-history-sejong"].includes(n.id))
      await page.screenshot({ path: dest + "/screenshots/" + n.id + ".png" });
    evidence.rows.push({
      check: n.id,
      status: "PASS",
      native: audit,
      approachDialogueReturn: true,
      actors: after.active,
      textures: after.assets.loaded,
    });
    await save();
  }
  await page.goto(base);
  const restored = await page.evaluate(() => [
    localStorage.getItem("korean-arena-player-preferences-v1"),
    localStorage.getItem("korean-arena-npc-life-v1"),
    window.sessionStorage.getItem("korean-arena-world-session-v1"),
  ]);
  assert(
    JSON.stringify(preserved) === JSON.stringify(restored),
    "QA modified normal player records",
  );
  await page.goto(base + "play/?renderer=canvas");
  await page.waitForFunction(() => window.__GATE3__?.ready);
  assert(
    (await page.evaluate(() => window.__GATE3__.characterId)) === "doyun",
    "Normal game lost original avatar",
  );
  await page.locator("#portal-review-controls summary").click();
  await page.locator("#portal-review-controls a").click();
  await page.waitForURL(base);
  evidence.rows.push({
    check: "normal storage +QA isolation +return",
    status: "PASS",
  });
  for (const viewport of [
    { width: 390, height: 844 },
    { width: 667, height: 375 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto(base);
    await page.locator(".roster article").nth(25).waitFor();
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      "Portal horizontal overflow",
    );
    await page.screenshot({
      path: dest + `/screenshots/mobile-${viewport.width}.png`,
      fullPage: true,
    });
  }
  const mobile = await browser.newContext({
    viewport: { width: 667, height: 375 },
    hasTouch: true,
    deviceScaleFactor: 1,
    httpCredentials: { username, password },
  });
  const touch = await mobile.newPage();
  await touch.goto(base + "play/?qa&renderer=canvas&npcReview=npc-minseo");
  await touch.waitForFunction(
    () =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-minseo"),
  );
  await touch.locator("#portal-review-controls summary").tap();
  await touch.locator("#portal-review-controls select").selectOption("0");
  await touch
    .getByRole("button", { name: "Đặt giờ · REVIEW ONLY", exact: true })
    .tap();
  await touch.locator("#portal-review-controls summary").tap();
  await touch.screenshot({ path: dest + "/screenshots/mobile-game.png" });
  await touch.locator("#portal-review-controls summary").tap();
  await touch.locator("#portal-review-controls a").tap();
  await touch.waitForURL(base);
  await mobile.close();
  evidence.rows.push({
    check: "portrait/landscape portal +actual mobile touch controls/return",
    status: "PASS",
  });
  assert(
    !evidence.errors.length &&
      !evidence.missing.length &&
      !evidence.external.length,
    "Browser/resource/external regression",
  );
  evidence.status = "PASS";
} catch (e) {
  evidence.status = "FAIL";
  evidence.failure = e.stack;
  console.error(e);
  process.exitCode = 1;
} finally {
  await save();
  await browser?.close();
  server.kill("SIGTERM");
  if (stderr) console.error(stderr);
}
