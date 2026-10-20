import { chromium } from "playwright";
import fs from "node:fs/promises";
import crypto from "node:crypto";

const phase = process.argv[2] ?? "before";
if (!["before", "after"].includes(phase))
  throw Error("before or after required");
const out = `${process.env.PIXEL_PATH_CAPTURE_ROOT ?? "docs/v6-path-fix/quality"}/${phase}`;
await fs.mkdir(out, { recursive: true });
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
    "--disable-gpu-compositing",
  ],
});
const errors = [],
  shots = [],
  displays = [];
const hash = (b) => crypto.createHash("sha256").update(b).digest("hex");
async function settled(p) {
  const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount > n + 5,
    n,
  );
}
async function native(p, name) {
  const s = await p
    .locator("#stage canvas")
    .evaluate((c) => ({ data: c.toDataURL(), size: [c.width, c.height] }));
  const webgl = await p.evaluate(
    () => window.__PIXEL_METRICS__.renderer === "WebGL",
  );
  let b;
  if (webgl) {
    // preserveDrawingBuffer is false in the REAL production renderer. Read the
    // composited browser frame, never a cleared post-render WebGL backbuffer.
    // DPR1 here means one screenshot pixel is one native canvas pixel.
    if (await p.evaluate(() => devicePixelRatio !== 1))
      throw Error("Native WebGL compositor capture requires DPR1");
    const style = await p.addStyleTag({
      content:
        "#mini-wrap,.touch-controls,.hint,#rotate-screen{visibility:hidden!important}",
    });
    b = await p.locator("#stage canvas").screenshot();
    await style.evaluate((node) => node.remove());
  } else b = Buffer.from(s.data.split(",")[1], "base64");
  await fs.writeFile(`${out}/${name}-native.png`, b);
  shots.push({
    name,
    size: s.size,
    sha256: hash(b),
    camera: await p.evaluate(() => window.__FULL_WORLD__.camera),
    method: webgl
      ? "Actual browser compositor screenshot at DPR1; HUD hidden for unobstructed native proof"
      : "Native Canvas2D toDataURL",
  });
}
async function open(entry, options, renderer = "canvas", query = "qa") {
  const context = await browser.newContext({
    reducedMotion: "reduce",
    ...options,
  });
  await context.addInitScript(() => {
    window.__DISPLAY_AUDIT__ = [];
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (...args) {
      const ctx = original.apply(this, args);
      if (ctx && !window.__DISPLAY_AUDIT__.some((r) => r.ctx === ctx)) {
        const record = {
          canvas: this,
          ctx,
          type: args[0],
          filters: {},
          draws: {},
        };
        window.__DISPLAY_AUDIT__.push(record);
        if (ctx.drawImage) {
          const draw = ctx.drawImage.bind(ctx);
          ctx.drawImage = function (...items) {
            const source = items[0],
              key = source.currentSrc?.split("/").pop() ?? "[canvas]";
            const counts = (record.draws[key] ??= { nearest: 0, smoothed: 0 });
            counts[ctx.imageSmoothingEnabled ? "smoothed" : "nearest"]++;
            return draw(...items);
          };
        }
        if (ctx.texParameteri) {
          const set = ctx.texParameteri.bind(ctx);
          ctx.texParameteri = function (target, key, value) {
            if (key === 10240 || key === 10241)
              record.filters[value] = (record.filters[value] ?? 0) + 1;
            return set(target, key, value);
          };
        }
      }
      return ctx;
    };
  });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push({ entry, message: e.message }));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push({ entry, message: m.text() });
  });
  page.on("response", (r) => {
    if (r.status() >= 400)
      errors.push({ entry, message: r.url(), status: r.status() });
  });
  await page.goto(`${base}${entry}?${query}&renderer=${renderer}`);
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  return { context, page };
}
async function display(p, name, zoom) {
  const report = await p.evaluate(() => {
    const c = document.querySelector("#stage canvas"),
      rect = c.getBoundingClientRect(),
      css = getComputedStyle(c);
    const record = window.__DISPLAY_AUDIT__.find((r) => r.canvas === c);
    const ctx = record.ctx;
    return {
      dpr: devicePixelRatio,
      viewport: [window.innerWidth, window.innerHeight],
      canvas: [c.width, c.height],
      rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
      css: { imageRendering: css.imageRendering, transform: css.transform },
      renderer: window.__PIXEL_METRICS__.renderer,
      camera: window.__FULL_WORLD__.camera,
      postRenderSmoothing: ctx.imageSmoothingEnabled ?? null,
      textureDraws: record.draws,
      filters: record.filters,
    };
  });
  await p.screenshot({ path: `${out}/${name}-browser.png` });
  await native(p, name);
  displays.push({ name, requestedZoom: zoom, ...report });
}
try {
  for (const renderer of ["canvas", "webgl"]) {
    for (const version of ["v4", "v6"]) {
      const entry =
        version === "v4"
          ? "v4-readability-review.html"
          : "v6-world-review.html";
      const { context, page } = await open(
        entry,
        { viewport: { width: 1440, height: 1140 }, deviceScaleFactor: 1 },
        renderer,
      );
      await page.evaluate(() => window.__SEOUL_TEST__.place(1568, 1292));
      await settled(page);
      await page.locator("#pause").click();
      await settled(page);
      await display(page, `${version}-${renderer}-native-1x`, 1);
      await context.close();
    }
  }
  for (const [name, width, height, dpr, mobile] of [
    ["odd-desktop", 1279, 969, 1, false],
    ["retina-desktop", 1440, 1140, 2, false],
    ["mobile", 844, 390, 3, true],
    ["odd-mobile", 845, 391, 3, true],
  ]) {
    const { context, page } = await open("v6-world-review.html", {
      viewport: { width, height },
      deviceScaleFactor: dpr,
      isMobile: mobile,
      hasTouch: mobile,
    });
    await page.evaluate(() => window.__SEOUL_TEST__.place(1776, 3520));
    await settled(page);
    await page.locator("#pause").click();
    await settled(page);
    await display(page, name, 1);
    if (name === "retina-desktop") {
      await page.locator("#settings-open").click();
      for (const zoom of [0.5, 2]) {
        await page.locator("#zoom").selectOption(String(zoom));
        await settled(page);
        await display(page, `${name}-zoom-${zoom}`, zoom);
      }
    }
    await context.close();
  }
  const { context, page } = await open("v6-world-review.html", {
    viewport: { width: 1440, height: 1140 },
    deviceScaleFactor: 1,
  });
  for (const [name, x, y] of [
    ["museum-join", 2640, 1832],
    ["civic-join", 2176, 2072],
    ["civic-transition", 2176, 2544],
    ["station-joins", 2240, 3024],
    ["modern-forecourt", 2240, 3496],
    ["west-connector", 1472, 3536],
    ["park-circulation", 3712, 3328],
    ["park-hall-passage", 3792, 3456],
    ["waterfront-access", 2752, 3744],
    ["pier-approach", 2496, 3864],
    ["island-dock", 2496, 4320],
    ["island-garden", 2240, 4640],
    ["island-village", 1830, 4800],
    ["island-coast-loop", 2600, 4880],
  ]) {
    await page.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    await settled(page);
    await native(page, name);
  }
  await context.close();
  const full = await open(
    "v6-world-review.html",
    { viewport: { width: 4352, height: 5312 }, deviceScaleFactor: 1 },
    "canvas",
    "overview",
  );
  await settled(full.page);
  await native(full.page, "full-map");
  await full.context.close();
  if (errors.length) throw Error(JSON.stringify(errors));
  const report = {
    phase,
    method:
      "Actual production Phaser renders. Matched V4/V6 camera pose1568,1292, zoom1, renderer, viewport1440x1140, DPR1 and native canvas PNG extraction. Browser screenshots independently retain physical DPR pixels. QA placements are still framing only, not traversal evidence. WebGL uses software SwiftShader; host CPU compositor shim does not disable WebGL. No sharpness filter or screenshot enhancement.",
    shots,
    displays,
    errors,
  };
  await fs.writeFile(
    `${out}/captures.json`,
    JSON.stringify(report, null, 2) + "\n",
  );
  console.log(JSON.stringify({ phase, shots: shots.length, displays, errors }));
} finally {
  await browser.close();
}
