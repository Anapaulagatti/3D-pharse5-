import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const base =
  process.env.GATE1_URL ??
  "http://127.0.0.1:4230/3D-pharse5-/gate1-street.html";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const rows = [],
  errors = [],
  requests = new Set();
async function axis(p, a, t) {
  let v = await p.evaluate((a) => window.__GATE1__[a], a);
  if (Math.abs(t - v) < 5) return;
  const sign = Math.sign(t - v),
    key =
      a === "x"
        ? sign > 0
          ? "ArrowRight"
          : "ArrowLeft"
        : sign > 0
          ? "ArrowDown"
          : "ArrowUp";
  await p.keyboard.down("Shift");
  await p.keyboard.down(key);
  try {
    await p.waitForFunction(
      ({ a, t, sign }) => (window.__GATE1__[a] - t) * sign >= -9,
      { a, t, sign },
      { timeout: Math.max(6000, Math.abs(t - v) * 25), polling: "raf" },
    );
  } finally {
    await p.keyboard.up(key);
    await p.keyboard.up("Shift");
    await p.waitForTimeout(150);
  }
  for (let i = 0; i < 16; i++) {
    v = await p.evaluate((a) => window.__GATE1__[a], a);
    if (Math.abs(t - v) < 5) return;
    const k =
      a === "x"
        ? t > v
          ? "ArrowRight"
          : "ArrowLeft"
        : t > v
          ? "ArrowDown"
          : "ArrowUp";
    await p.keyboard.down(k);
    await p.waitForTimeout(Math.max(20, Math.min(80, Math.abs(t - v) * 9)));
    await p.keyboard.up(k);
    await p.waitForTimeout(140);
  }
  throw Error("Could not reach " + a + "=" + t + " actual=" + v);
}
function watch(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  p.on("request", (r) => {
    const path = new URL(r.url()).pathname;
    requests.add(path);
    if (/\/assets\/v[1-9]|\/assets\/v10-city|\/assets\/world\//.test(path))
      errors.push("Rejected source request " + path);
  });
}
try {
  const page = await browser.newPage({
    viewport: { width: 1280, height: 980 },
    reducedMotion: "reduce",
  });
  watch(page);
  await page.goto(base + "?renderer=canvas");
  await page.waitForFunction(() => window.__GATE1__?.ready);
  if (await page.evaluate(() => !!window.__GATE1_TEST__))
    throw Error("Normal entry exposes placement");
  await page.locator("canvas").focus();
  const frames = new Set();
  for (const [x, label] of [
    [242, "모퉁이 커피"],
    [598, "문장 책방"],
    [888, "배움"],
    [1288, "마루 편의점"],
  ]) {
    await axis(page, "x", x);
    frames.add(await page.evaluate(() => window.__GATE1__.frame));
    await page.keyboard.press("e");
    await page.waitForFunction(() => !document.querySelector("#dialog").hidden);
    const title = await page.locator("#dialog-title").textContent();
    if (!title.includes(label)) throw Error("Wrong entrance " + title);
    await page.locator("#close-dialog").click();
    rows.push({
      case: "real-input entrance",
      label,
      position: await page.evaluate(() => [
        window.__GATE1__.x,
        window.__GATE1__.y,
      ]),
    });
  }
  await axis(page, "x", 992);
  await axis(page, "y", 928);
  await axis(page, "x", 1120);
  await page.keyboard.press("e");
  await page.waitForFunction(() => !document.querySelector("#dialog").hidden);
  if (
    !(await page.locator("#dialog-title").textContent()).includes("Sân gặp gỡ")
  )
    throw Error("Court interaction missing");
  await page.locator("#close-dialog").click();
  rows.push({
    case: "continuous walk through crossing to court",
    state: await page.evaluate(() => window.__GATE1__),
  });
  // Real input against the painted facade, with one disclosed QA start for collision isolation.
  await page.goto(base + "?renderer=canvas&qa");
  await page.waitForFunction(() => window.__GATE1__?.ready);
  await page.evaluate(() => window.__GATE1_TEST__.place(598, 590));
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(1200);
  await page.keyboard.up("ArrowUp");
  const stopped = await page.evaluate(() => window.__GATE1__.y);
  if (stopped < 560) throw Error("Facade collision failed " + stopped);
  rows.push({ case: "facade blocks real upward input", stopped });
  await page.close();
  const context = await browser.newContext({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const mobile = await context.newPage();
  watch(mobile);
  await mobile.goto(base + "?renderer=canvas");
  await mobile.waitForFunction(() => window.__GATE1__?.ready);
  const cdp = await context.newCDPSession(mobile),
    b = await mobile.locator("#joystick").boundingBox(),
    x = b.x + b.width / 2,
    y = b.y + b.height / 2,
    start = await mobile.evaluate(() => window.__GATE1__.x);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [{ x: x + b.width * 0.3, y, id: 1 }],
  });
  await mobile.waitForFunction((s) => window.__GATE1__.x > s + 20, start);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  rows.push({
    case: "landscape emulated mobile joystick",
    moved: await mobile.evaluate((s) => window.__GATE1__.x - s, start),
    renderer: await mobile.evaluate(() => window.__PIXEL_METRICS__.renderer),
  });
  await context.close();
  const web = await browser.newPage({ viewport: { width: 1280, height: 980 } });
  watch(web);
  await web.goto(base + "?renderer=webgl");
  await web.waitForFunction(() => window.__GATE1__?.ready);
  const renderer = await web.evaluate(() => window.__PIXEL_METRICS__.renderer);
  if (!renderer.includes("WebGL")) throw Error("Forced WebGL unavailable");
  rows.push({ case: "forced WebGL", renderer });
  await web.close();
  const result = {
    status: errors.length ? "FAIL" : "PASS",
    source:
      "Actual Phaser; normal-entry continuous keyboard tour + isolated QA collision + emulated mobile actual CDP touch; not artistic approval",
    rows,
    errors,
    requests: [...requests].sort(),
  };
  await fs.writeFile(
    "docs/gate1/gameplay-qa.json",
    JSON.stringify(result, null, 2) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(
    JSON.stringify({ status: result.status, cases: rows.length, errors }),
  );
} finally {
  await browser.close();
}
