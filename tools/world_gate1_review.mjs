import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
const out = "docs/world-gate1",
  base = process.env.WORLD_GATE1_URL ?? "http://127.0.0.1:4240/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const errors = [],
  requests = new Set(),
  rows = [],
  captures = [];
async function page(options = {}) {
  const p = await browser.newPage({
    viewport: { width: 1366, height: 1050 },
    deviceScaleFactor: 1,
    ...options,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  p.on("request", (r) => requests.add(new URL(r.url()).pathname));
  return p;
}
async function ready(p, suffix = "") {
  await p.goto(base + "world-gate1.html" + suffix);
  await p.waitForFunction(() => window.__WORLD_PLAN__?.ready);
  await p.waitForTimeout(150);
}
async function capture(p, name) {
  const data = await p
    .locator("canvas")
    .evaluate((c) => ({ url: c.toDataURL(), size: [c.width, c.height] }));
  const bytes = Buffer.from(data.url.split(",")[1], "base64");
  await fs.writeFile(`${out}/${name}.png`, bytes);
  captures.push({
    name,
    size: data.size,
    sha256: createHash("sha256").update(bytes).digest("hex"),
    url: p.url(),
    source: "Actual Phaser Canvas; no image compositing",
  });
}
async function place(p, x, y) {
  await p.evaluate(([x, y]) => window.__WORLD_PLAN_TEST__.place(x, y), [x, y]);
  await p.waitForTimeout(100);
}
async function state(p) {
  return p.evaluate(() => window.__WORLD_PLAN__);
}
try {
  const p = await page();
  await ready(p);
  assert.equal(
    await p.evaluate(() => typeof window.__WORLD_PLAN_TEST__),
    "undefined",
  );
  const start = await state(p);
  await p.keyboard.down("ArrowDown");
  await p.waitForTimeout(1000);
  await p.keyboard.up("ArrowDown");
  const moved = await state(p);
  assert(moved.y > start.y + 35 && moved.y < start.y + 80);
  assert.equal(moved.zoom, 1);
  rows.push({
    case: "Normal entry: original-scale Juni, keyboard at normal speed, zoom1, no teleport hook",
    pass: true,
    deltaY: moved.y - start.y,
  });
  const sampling = await p.locator("canvas").evaluate((c) => ({
    dpr: devicePixelRatio,
    samplingMode: window.__WORLD_PLAN__.samplingMode,
    css: getComputedStyle(c).imageRendering,
  }));
  assert.equal(sampling.dpr, 1);
  assert.equal(sampling.samplingMode, 1);
  assert.equal(sampling.css, "pixelated");
  rows.push({
    case: "Actual Canvas DPR1, Juni texture NEAREST scaleMode=1 and CSS pixelated",
    pass: true,
    ...sampling,
  });
  const routeAudit = await p.evaluate(() => window.__WORLD_PATH_AUDIT__);
  await fs.writeFile(
    `${out}/rendered-route-audit.json`,
    JSON.stringify(routeAudit, null, 2) + "\n",
  );
  assert(
    routeAudit.every((r) => r.blocked.length === 0),
    JSON.stringify(routeAudit.filter((r) => r.blocked.length)),
  );
  rows.push({
    case: "All 19 rendered route centerlines incl actual Phaser splines clear with 16px foot clearance",
    pass: true,
  });
  await ready(p, "?qa");
  await place(p, 700, 2690);
  await p.keyboard.press("e");
  await p.waitForTimeout(100);
  assert((await state(p)).visited.includes("cafe"));
  rows.push({
    case: "Real E at planned cafe entrance opens destination card",
    pass: true,
  });
  await p.locator("#card").click();
  await place(p, 700, 2635);
  await p.keyboard.down("ArrowUp");
  await p.waitForTimeout(1500);
  await p.keyboard.up("ArrowUp");
  const stopped = await state(p);
  assert(stopped.y >= 2606 && stopped.y < 2635);
  rows.push({
    case: "Real keyboard cannot enter cafe solid",
    pass: true,
    stopY: stopped.y,
  });
  await place(p, 2048, 2050);
  await p.keyboard.down("Shift");
  await p.keyboard.down("ArrowDown");
  await p.waitForFunction(() => window.__WORLD_PLAN__.y > 2250, null, {
    timeout: 6000,
  });
  await p.keyboard.up("ArrowDown");
  await p.keyboard.up("Shift");
  rows.push({
    case: "Continuous real-keyboard passage heritage threshold to modern avenue",
    pass: true,
  });
  await place(p, 3090, 3480);
  await p.keyboard.down("Shift");
  await p.keyboard.down("ArrowRight");
  await p.waitForFunction(() => window.__WORLD_PLAN__.x > 3370, null, {
    timeout: 7000,
  });
  await p.keyboard.up("ArrowRight");
  await p.keyboard.up("Shift");
  rows.push({
    case: "Real keyboard crosses physical mainland–island bridge without teleport",
    pass: true,
  });
  await place(p, 2900, 3880);
  await p.keyboard.down("ArrowDown");
  await p.waitForTimeout(2100);
  await p.keyboard.up("ArrowDown");
  assert((await state(p)).y <= 3964);
  rows.push({
    case: "Shore collision stops Juni before water",
    pass: true,
    stopY: (await state(p)).y,
  });
  for (const [id, x, key, target, axis] of [
    ["Namsan southwest", 2048, "ArrowLeft", 1460, "x"],
    ["Amusement southeast", 2048, "ArrowRight", 2440, "x"],
    ["Mainland boarding pier", 2560, "ArrowDown", 4070, "y"],
    ["Jeju dock arrival", 3240, "ArrowRight", 3350, "x"],
  ]) {
    const y =
      id === "Mainland boarding pier"
        ? 3900
        : id === "Jeju dock arrival"
          ? 4100
          : 3260;
    await place(p, x, y);
    await p.keyboard.down("Shift");
    await p.keyboard.down(key);
    await p.waitForFunction(
      ({ axis, target, left }) =>
        left
          ? window.__WORLD_PLAN__[axis] <= target + 5
          : window.__WORLD_PLAN__[axis] >= target - 5,
      { axis, target, left: key === "ArrowLeft" },
      { timeout: 10000 },
    );
    await p.keyboard.up(key);
    await p.keyboard.up("Shift");
    rows.push({
      case: `Real continuous keyboard route: ${id}`,
      pass: true,
      end: await state(p),
    });
  }
  for (const [name, x, y] of [
    ["NORTH_NATIVE_1X", 2048, 1100],
    ["TRANSITION_NATIVE_1X", 2048, 1900],
    ["SOUTH_NATIVE_1X", 1350, 2690],
    ["COAST_NATIVE_1X", 2900, 3480],
    ["ISLAND_NATIVE_1X", 3640, 4220],
    ["NAMSAN_SW_NATIVE_1X", 1460, 3260],
    ["AMUSEMENT_SE_NATIVE_1X", 2440, 3260],
    ["FERRY_PIERS_NATIVE_1X", 3240, 4100],
  ]) {
    await place(p, x, y);
    await capture(p, name);
  }
  await ready(p, "?qa&scale");
  await place(p, 700, 2690);
  await capture(p, "BUILDING_SCALE_NATIVE_1X");
  await p.close();
  const m = await page({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await ready(m);
  assert.equal((await state(m)).zoom, 1);
  const before = await state(m);
  const box = await m.locator("#joystick").boundingBox();
  const cdp = await m.context().newCDPSession(m);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: box.x + box.width / 2 + 32, y: box.y + box.height / 2 }],
  });
  await m.waitForTimeout(1100);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  assert((await state(m)).x > before.x + 35);
  await capture(m, "MOBILE_LANDSCAPE");
  rows.push({
    case: "844×390 mobile landscape: real CDP touch joystick moves Juni at zoom1",
    pass: true,
  });
  await m.close();
  const overview = await page({ viewport: { width: 1300, height: 1480 } });
  await ready(overview, "?overview");
  await capture(overview, "MASTERPLAN_ZONING");
  await overview.screenshot({ path: `${out}/MASTERPLAN_REVIEW.png` });
  await overview.close();
  const n = await page({ viewport: { width: 1280, height: 900 } });
  await ready(n, "?overview&native");
  await capture(n, "GRAYBOX_NATIVE_4096x4608");
  assert.equal((await state(n)).zoom, 1);
  await n.close();
  const board = await page({ viewport: { width: 1800, height: 1600 } });
  await board.goto(base + "docs/world-gate1/masterplan-board.html");
  await board.evaluate(() =>
    Promise.all([...document.images].map((i) => i.decode())),
  );
  await board.screenshot({
    path: `${out}/MASTERPLAN_BOARD.png`,
    fullPage: true,
  });
  await board.close();
  const b = await page({ viewport: { width: 1800, height: 2200 } });
  await b.goto(base + "docs/world-gate1/style-bible.html");
  await b.evaluate(() =>
    Promise.all([...document.images].map((i) => i.decode())),
  );
  await b.screenshot({ path: `${out}/STYLE_BIBLE.png`, fullPage: true });
  await b.close();
  assert(
    ![...requests].some((r) => /assets\/(v[0-9]|world|gate1)/.test(r)),
    JSON.stringify([...requests]),
  );
  assert.equal(errors.length, 0, JSON.stringify(errors));
  rows.push({
    case: "New preview requests Juni only; no legacy southern artwork/map requests; no page/HTTP errors",
    pass: true,
  });
  await fs.writeFile(
    `${out}/browser-qa.json`,
    JSON.stringify(
      {
        rows,
        errors,
        requests: [...requests].sort(),
        captures,
        limits: [
          "Desktop Chromium software Canvas; mobile landscape emulated, no physical phone.",
          "QA placement sets test/capture start only; movement cases use actual keyboard/touch.",
          "No final art, occlusion art, interiors, operational ferry or NPC systems are claimed.",
        ],
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    JSON.stringify({ passed: rows.length, captures: captures.length, errors }),
  );
} finally {
  await browser.close();
}
