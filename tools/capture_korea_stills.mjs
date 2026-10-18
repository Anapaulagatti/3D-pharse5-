import { chromium } from "playwright";
import fs from "node:fs/promises";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const out = "docs/living-korea/quality";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [],
  shots = [];
async function page(c, entry = "living-korea-review.html?qa&renderer=canvas") {
  const p = await c.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await p.goto(base + entry);
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  return p;
}
async function place(p, x, y) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
  const f = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount >= n + 4,
    f,
  );
}
async function canvas(p, name) {
  const data = await p.locator("canvas").evaluate((c) => c.toDataURL());
  await fs.writeFile(
    `${out}/${name}.png`,
    Buffer.from(data.split(",")[1], "base64"),
  );
  shots.push({
    name,
    canvas: await p.locator("canvas").evaluate((c) => [c.width, c.height]),
    view: await p.evaluate(() => window.__SEOUL__.view),
  });
}
async function goPark(p) {
  await place(p, 1152, 2016);
  await p.locator("#interact").click();
  await p.locator("#travel-go").click();
  await p.waitForFunction(() => window.__KOREA__?.district === "namsan");
}
try {
  const c = await b.newContext({
    viewport: { width: 1440, height: 1140 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  for (const [entry, prefix] of [
    ["refinement-review.html?qa&renderer=canvas", "before"],
    ["living-korea-review.html?qa&renderer=canvas", "after"],
  ]) {
    const p = await page(c, entry);
    for (const [id, x, y] of [
      ["palace-west", 352, 496],
      ["palace-east", 1952, 496],
      ["inner-gate", 1152, 384],
      ["academy-north", 544, 1152],
      ["academy-west", 128, 1280],
      ["academy-east", 992, 1280],
      ["workshop-west", 1440, 1264],
      ["workshop-east", 2176, 1344],
      ["crowded-frontage", 2256, 1584],
    ]) {
      await place(p, x, y);
      await canvas(p, `${prefix}-${id}-native`);
    }
    if (prefix === "after") {
      await place(p, 1984, 2000);
      await canvas(p, "museum-new-frontage-native");
      await place(p, 1152, 2016);
      await canvas(p, "traditional-modern-transition-native");
      await goPark(p);
      for (const [id, x, y] of [
        ["namsan-arrival", 704, 1056],
        ["namsan-tower", 832, 672],
        ["namsan-overlook", 1120, 784],
        ["namsan-forest", 384, 816],
      ]) {
        await place(p, x, y);
        await canvas(p, `${id}-native`);
      }
      await p.locator("#settings-open").click();
      await p.locator("#night").click();
      await p.locator("#settings-close").click();
      await place(p, 832, 672);
      await canvas(p, "namsan-evening-native");
    }
    await p.close();
  }
  await c.close();
  const ov = await b.newContext({
    viewport: { width: 1440, height: 1280 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const op = await page(
    ov,
    "living-korea-review.html?qa&renderer=canvas&overview",
  );
  await op.evaluate(() => {
    const main = document.querySelector("main");
    main.style.width = "1152px";
    main.style.height = "1120px";
  });
  await op.waitForTimeout(400);
  await canvas(op, "north-overview-half-scale");
  await goPark(op);
  await op.evaluate(() => {
    const main = document.querySelector("main");
    main.style.width = "704px";
    main.style.height = "640px";
  });
  await op.waitForTimeout(400);
  await canvas(op, "namsan-overview-half-scale");
  await ov.close();
  for (const [width, height, id] of [
    [844, 390, "mobile-landscape"],
    [640, 360, "mobile-16x9"],
    [568, 320, "mobile-small"],
    [932, 430, "mobile-wide"],
  ]) {
    const mc = await b.newContext({
      viewport: { width, height },
      deviceScaleFactor: 1,
      isMobile: true,
      hasTouch: true,
      reducedMotion: "reduce",
    });
    const p = await page(mc);
    await goPark(p);
    await place(p, 832, 672);
    if (width === 568) {
      await p.locator("#settings-open").tap();
      await p.selectOption("#control-size", "68");
      await p.locator("#settings-close").tap();
    }
    await p.screenshot({ path: `${out}/${id}-interface.png` });
    await canvas(p, `${id}-native`);
    if (width === 844) {
      await p.locator("#settings-open").tap();
      await p.selectOption("#zoom", "0.5");
      await p.locator("#settings-close").tap();
      await p.waitForTimeout(250);
      await p.screenshot({ path: `${out}/mobile-panorama-interface.png` });
      await p.setViewportSize({ width: 390, height: 844 });
      await p.locator("#rotate-screen").waitFor();
      await p.screenshot({ path: `${out}/portrait-rotate-interface.png` });
    }
    await mc.close();
  }
  const rc = await b.newContext({
    viewport: { width: 640, height: 360 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const rp = await page(rc);
  await place(rp, 544, 1152);
  await rp.locator("#interact").tap();
  await rp.waitForFunction(() => window.__SEOUL__?.area === "room");
  await place(rp, 385, 392);
  await rp.locator("#interact").tap();
  await rp.locator(".hangul-letter").waitFor();
  await rp.screenshot({ path: `${out}/mobile-hangul-dialogue.png` });
  await rc.close();
  if (errors.length) throw Error(JSON.stringify(errors));
  await fs.writeFile(
    `${out}/stills.json`,
    JSON.stringify(
      {
        method:
          "Actual production Phaser canvas PNGs; QA placement for matched still-camera poses, never claimed as movement. Native1x landmark shots; two overview renders0.5x; whole-browser mobile HUD and portrait captures are emulated, not physical phones.",
        shots,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  console.log({ shots: shots.length, errors });
} finally {
  await b.close();
}
