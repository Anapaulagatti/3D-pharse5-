import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const phase = process.env.PIXEL_PHASE ?? "before",
  port = process.env.PIXEL_PORT ?? "4271",
  dir = "docs/gate3a-pixel-audit";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const results = [];
for (const renderer of ["auto", "canvas"]) {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await p.addInitScript(() => {
    window.__pixelContexts = [];
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (...args) {
      const c = original.apply(this, args);
      if (c && !window.__pixelContexts.includes(c))
        window.__pixelContexts.push(c);
      return c;
    };
    window.__pixelDraws = new Map();
    const drawImage = window.CanvasRenderingContext2D.prototype.drawImage;
    window.CanvasRenderingContext2D.prototype.drawImage = function (...args) {
      if (args.length === 9 && args[0]?.src) {
        const key = args[0].src + ":" + args[7] + ":" + args[8];
        window.__pixelDraws.set(key, {
          source: args[0].src,
          sourceRect: args.slice(1, 5),
          destinationRect: args.slice(5),
          smoothing: this.imageSmoothingEnabled,
        });
      }
      return drawImage.apply(this, args);
    };
    window.__pixelFilters = [];
    for (const proto of [
      window.WebGLRenderingContext.prototype,
      window.WebGL2RenderingContext.prototype,
    ]) {
      const original = proto.texParameteri;
      proto.texParameteri = function (target, name, value) {
        window.__pixelFilters.push({ name, value });
        return original.call(this, target, name, value);
      };
    }
  });

  async function shot(name) {
    const renderAudit = await p.evaluate(async () =>
      window.__GATE3_PIXEL_AUDIT__
        ? await window.__GATE3_PIXEL_AUDIT__()
        : null,
    );
    if (renderAudit) {
      await fs.writeFile(
        `${dir}/${phase}-${renderer}-${name}-backing.png`,
        Buffer.from(renderAudit.png.split(",")[1], "base64"),
      );
      delete renderAudit.png;
    }
    const state = await p.evaluate(() => ({
      state: window.__GATE3__,
      rect: document.querySelector("canvas").getBoundingClientRect().toJSON(),
      canvas: [
        document.querySelector("canvas").width,
        document.querySelector("canvas").height,
      ],
      css: getComputedStyle(document.querySelector("canvas")).imageRendering,
      dpr: devicePixelRatio,
      visualScale: window.visualViewport.scale,
      filters: window.__pixelFilters,
      canvasDraws: [...window.__pixelDraws.values()],
      contexts: window.__pixelContexts.map((c) => ({
        kind: c.constructor.name,
        smoothing: c.imageSmoothingEnabled,
        antialias: c.getContextAttributes?.()?.antialias,
      })),
    }));
    await p
      .locator("canvas")
      .screenshot({ path: `${dir}/${phase}-${renderer}-${name}.png` });
    results.push({ name, renderer, ...state, renderAudit });
  }
  const url = `http://127.0.0.1:${port}/gate3-review.html?scene=district&entry=station&renderer=${renderer}`;
  async function open(u) {
    await p.goto(u + (phase === "after" ? "&pixelAudit" : ""));
    await p.waitForFunction(() => window.__GATE3__?.ready);
    await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
    await p.waitForTimeout(400);
  }
  await open(url + "&native");
  await shot("native");
  await open(url.replace("entry=station", "entry=alley"));
  await p.addStyleTag({
    content:
      "header,footer,#camera-tools,#joystick,#touch-actions,#tour-controls {visibility:hidden!important}",
  });
  await shot("stationary");
  await p.keyboard.down("a");
  await p.waitForTimeout(700);
  await shot("moving");
  await p.keyboard.up("a");
  await p.setViewportSize({ width: 1281, height: 1001 });
  await open(url + "&native");
  await shot("odd-display");
  if (renderer === "auto") {
    await p.setViewportSize({ width: 843, height: 391 });
    await open(url);
    await p.locator("#scenic").click();
    await p.mouse.move(420, 195);
    await p.mouse.wheel(0, 100);
    await p.waitForTimeout(300);
    await shot("half-zoom-odd");
    await p.goto(
      `http://127.0.0.1:${port}/gate3-review.html?scene=world&entry=jeju&pixelAudit`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    await p.locator("#scenic").click();
    await p.locator("#start-tour").click();
    await p.waitForTimeout(1700);
    await shot("tour-moving");
    await p.setViewportSize({ width: 1280, height: 1000 });
    await open(
      `http://127.0.0.1:${port}/gate3-review.html?scene=registration&entry=station&native`,
    );
    await shot("station-pivot");
  }
  await p.close();
}
await fs.writeFile(
  `${dir}/${phase}-capture.json`,
  JSON.stringify(results, null, 2),
);
await b.close();
console.log(phase, results.length, "captures");
