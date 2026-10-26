import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const base = "http://127.0.0.1:4340/",
  rows = [],
  errors = [],
  missing = [];
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const ready = (p) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 60000 },
  );
const state = (p) =>
  p.evaluate(() => {
    const s = window.__GATE3__;
    return {
      id: s.characterId,
      x: s.x,
      y: s.y,
      visited: s.visited,
      players: s.playerSprites,
      appearance: s.appearance,
      cache: s.characterAssets,
    };
  });
async function open(p) {
  if (await p.locator("#character-selection").isVisible()) return;
  if (!(await p.locator("#character-open").isVisible()))
    await p.locator("#settings summary").click({ noWaitAfter: true });
  await p.locator("#character-open").click({ noWaitAfter: true });
  await p.locator("#character-selection").waitFor();
}
try {
  const c = await browser.newContext({
      viewport: { width: 1280, height: 1000 },
    }),
    p = await c.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) missing.push([r.url(), r.status()]);
  });
  await p.goto(base + "?renderer=canvas&pixelAudit");
  await p.locator("#character-selection").waitFor();
  await p.waitForFunction(() => window.__GATE3__);
  for (const id of ["juni", "haneul", "bomi", "minjun", "ara", "doyun"]) {
    await open(p);
    const before = await state(p);
    await p.locator(`[data-character="${id}"]`).click({ noWaitAfter: true });
    await p.locator('[data-action="walk"]').click({ noWaitAfter: true });
    await p.locator("#character-confirm").click({ noWaitAfter: true });
    await p.locator("#character-selection").waitFor({ state: "hidden" });
    await ready(p);
    const after = await state(p);
    if (
      after.id !== id ||
      after.players !== 1 ||
      after.x !== before.x ||
      after.y !== before.y
    )
      throw Error("Package identity/state " + id);
    rows.push({ id, before, after });
  }
  for (const preset of [
    "review-ara-harbor",
    "review-ara-sunlit",
    "review-doyun-field",
    "review-doyun-varsity",
  ]) {
    await open(p);
    const before = await state(p);
    await p.locator("#appearance-preset").selectOption(preset);
    await p.locator("#character-confirm").click({ noWaitAfter: true });
    await p.locator("#character-selection").waitFor({ state: "hidden" });
    await ready(p);
    const after = await state(p);
    if (
      after.players !== 1 ||
      after.x !== before.x ||
      after.y !== before.y ||
      !after.appearance?.outfitId
    )
      throw Error("Package preset " + preset);
    rows.push({ preset, before, after });
  }
  if (await p.locator("#settings[open]").count())
    await p.locator("#settings summary").click({ noWaitAfter: true });
  const start = await state(p);
  await p.keyboard.down("d");
  await p.waitForFunction((x) => window.__GATE3__.x > x + 8, start.x);
  await p.keyboard.up("d");
  await p.waitForTimeout(250);
  await p.keyboard.press("e");
  await p.locator("#dialog").waitFor();
  await p.locator("#close").click({ noWaitAfter: true });
  const beforeReload = await state(p);
  await p.reload();
  await ready(p);
  const afterReload = await state(p);
  for (const k of ["id", "x", "y", "visited", "appearance"])
    if (JSON.stringify(beforeReload[k]) !== JSON.stringify(afterReload[k]))
      throw Error("Reload " + k);
  if (!afterReload.visited.length) throw Error("Missing real world progress");
  await c.close();
  const m = await browser.newContext({
      viewport: { width: 844, height: 390 },
      deviceScaleFactor: 3,
      isMobile: true,
      hasTouch: true,
    }),
    q = await m.newPage();
  q.on("pageerror", (e) => errors.push(e.message));
  q.on("response", (r) => {
    if (r.status() >= 400) missing.push([r.url(), r.status()]);
  });
  await q.goto(base);
  await q.locator("#character-selection").waitFor();
  await q.locator("#appearance-preset").selectOption("review-ara-harbor");
  await q.locator('[data-action="run"]').tap();
  await q.screenshot({
    path: "docs/phase2a/package-mobile-landscape.jpg",
    type: "jpeg",
    quality: 80,
  });
  await q.locator("#character-confirm").tap();
  await ready(q);
  const mobileStart = await state(q),
    touch = await m.newCDPSession(q),
    box = await q.locator("#joystick").boundingBox(),
    x = box.x + box.width / 2,
    y = box.y + box.height / 2;
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [{ x: x + box.width * 0.3, y, id: 1 }],
  });
  await q.waitForFunction((x) => window.__GATE3__.x > x + 8, mobileStart.x);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  const mobile = await state(q);
  if (mobile.players !== 1 || mobile.id !== "ara")
    throw Error("Package mobile");
  await m.close();
  await fs.writeFile(
    "docs/phase2a/package-smoke.json",
    JSON.stringify(
      {
        source:
          "Actual extracted ZIP, local server; not Vite/dev or mocked renderer",
        rows,
        reload: { before: beforeReload, after: afterReload },
        mobile,
        errors,
        missing,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  if (errors.length || missing.length)
    throw Error(JSON.stringify({ errors, missing }));
  console.log(
    "Extracted ZIP PASS:6 identities,4 cosmetic looks, movement, real visited/reload, landscape touch;0 missing requests/page errors",
  );
} finally {
  await browser.close();
}
