/** Refresh visual evidence without repeating unchanged behavioral test cases. */
import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const out = "docs/world-gate1",
  base = "http://127.0.0.1:4240/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const captures = [],
  errors = [];
async function page(width = 1366, height = 1050, extra = {}) {
  const p = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 1,
    ...extra,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  return p;
}
async function ready(p, suffix = "?qa") {
  await p.goto(base + "world-gate1.html" + suffix);
  await p.waitForFunction(() => window.__WORLD_PLAN__?.ready);
}
async function snap(p, name, x, y) {
  if (x !== undefined)
    await p.evaluate(
      ([x, y]) => window.__WORLD_PLAN_TEST__.place(x, y),
      [x, y],
    );
  await p.waitForTimeout(120);
  const d = await p
    .locator("canvas")
    .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
  const bytes = Buffer.from(d.png.split(",")[1], "base64");
  await fs.writeFile(`${out}/${name}.png`, bytes);
  captures.push({
    name,
    size: d.size,
    sha256: createHash("sha256").update(bytes).digest("hex"),
    url: p.url(),
    position: x === undefined ? null : [x, y],
    source:
      "Actual Phaser Canvas DPR1; native zoom1 except explicitly scaled browser overview",
  });
}
try {
  const p = await page();
  await ready(p);
  for (const [name, x, y] of [
    ["NORTH_NATIVE_1X", 2048, 1100],
    ["TRANSITION_NATIVE_1X", 2048, 1900],
    ["SOUTH_NATIVE_1X", 1350, 2690],
    ["COAST_NATIVE_1X", 2900, 3480],
    ["ISLAND_NATIVE_1X", 3680, 4180],
    ["NAMSAN_SW_NATIVE_1X", 1460, 3260],
    ["AMUSEMENT_SE_NATIVE_1X", 2440, 3260],
    ["FERRY_PIERS_NATIVE_1X", 3240, 4100],
    ["JEJU_OREUM_NATIVE_1X", 3910, 3530],
    ["JEJU_BASALT_NATIVE_1X", 3550, 3780],
    ["JEJU_ORCHARD_NATIVE_1X", 3650, 4050],
    ["JEJU_CULTURE_NATIVE_1X", 3490, 4460],
    ["STATION_NATIVE_1X", 2970, 2530],
  ])
    await snap(p, name, x, y);
  await ready(p, "?qa&scale");
  await snap(p, "BUILDING_SCALE_NATIVE_1X", 700, 2690);
  await p.close();
  for (const [name, w, h, x, y, extra] of [
    [
      "MOBILE_LANDSCAPE",
      844,
      390,
      2048,
      1900,
      { isMobile: true, hasTouch: true },
    ],
    ["JEJU_SPATIAL_NATIVE_1X", 1024, 1656, 3550, 3780, {}],
    ["STATION_SPATIAL_NATIVE_1X", 2048, 1250, 3300, 2530, {}],
  ]) {
    const p = await page(w, h, extra);
    await ready(p);
    await snap(p, name, x, y);
    await p.close();
  }
  const o = await page(1300, 1480);
  await ready(o, "?overview");
  await snap(o, "MASTERPLAN_ZONING");
  await o.screenshot({ path: out + "/MASTERPLAN_REVIEW.png" });
  await o.close();
  const n = await page(1280, 900);
  await ready(n, "?overview&native");
  await snap(n, "GRAYBOX_NATIVE_4096x4608");
  await n.close();
  const b = await page(1800, 1800);
  await b.goto(base + "docs/world-gate1/masterplan-board.html");
  await b.evaluate(() =>
    Promise.all([...document.images].map((i) => i.decode())),
  );
  await b.screenshot({ path: out + "/MASTERPLAN_BOARD.png", fullPage: true });
  await b.close();
  if (errors.length) throw Error(JSON.stringify(errors));
  const receipt = {
    captures,
    errors,
    reason:
      "Final station/Jeju labeling refresh only; no movement or collision changes since the 17 behavioral cases.",
  };
  await fs.writeFile(
    out + "/capture-refresh.json",
    JSON.stringify(receipt, null, 2) + "\n",
  );
  const qa = JSON.parse(await fs.readFile(out + "/browser-qa.json", "utf8"));
  qa.captures = captures;
  qa.captureRefresh = receipt.reason;
  await fs.writeFile(
    out + "/browser-qa.json",
    JSON.stringify(qa, null, 2) + "\n",
  );
  console.log(JSON.stringify({ captures: captures.length, errors }));
} finally {
  await browser.close();
}
