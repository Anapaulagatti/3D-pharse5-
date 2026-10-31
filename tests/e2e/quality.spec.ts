import { test, expect, type Page } from "@playwright/test";
import fs from "node:fs/promises";
async function boot(p: Page, renderer = "canvas") {
  const errors: string[] = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (e) => {
    if (e.type() === "error") errors.push(e.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await p.goto(`v9-world-review.html?qa&renderer=${renderer}`);
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  return errors;
}
async function place(p: Page, x: number, y: number) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  const n = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__!.frameCount > n + 5,
    n,
  );
}
async function pixels(p: Page, rect = [0, 0, 128, 128]) {
  return p.locator("canvas").evaluate((c, rect) => {
    const ctx = (c as HTMLCanvasElement).getContext("2d");
    if (!ctx) throw Error("Canvas required");
    return Array.from(
      ctx.getImageData(rect[0], rect[1], rect[2], rect[3]).data,
    );
  }, rect);
}
test("real Canvas draw-time atlas filtering is nearest at native zoom", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const native = CanvasRenderingContext2D.prototype.drawImage;
    const state = { calls: 0, smoothed: 0 };
    Object.assign(window, { __ATLAS_SAMPLING__: state });
    CanvasRenderingContext2D.prototype.drawImage = function (
      ...args: unknown[]
    ) {
      const source = args[0] as HTMLImageElement;
      if (source.width === 4096) {
        state.calls++;
        if (this.imageSmoothingEnabled) state.smoothed++;
      }
      return Reflect.apply(native, this, args);
    };
  });
  const errors = await boot(page);
  await place(page, 2176, 3056);
  const sampling = await page.evaluate(
    () =>
      (
        window as unknown as {
          __ATLAS_SAMPLING__: { calls: number; smoothed: number };
        }
      ).__ATLAS_SAMPLING__,
  );
  expect(sampling.calls).toBeGreaterThan(100);
  expect(sampling.smoothed).toBe(0);
  expect(await page.evaluate(() => window.__PIXEL_METRICS__!.cameraZoom)).toBe(
    1,
  );
  expect(errors).toEqual([]);
});
test("forced WebGL actually renders; source atlas uses nearest min/mag filters", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const results: { width: number; min: number; mag: number }[] = [];
    Object.assign(window, { __GL_ATLASES__: results });
    for (const Klass of [WebGLRenderingContext, WebGL2RenderingContext]) {
      const proto = Klass.prototype;
      const originalBind = proto.bindTexture,
        originalFilter = proto.texParameteri,
        originalUpload = proto.texImage2D;
      let bound: WebGLTexture | null = null;
      const states = new WeakMap<
        WebGLTexture,
        { width: number; min: number; mag: number }
      >();
      proto.bindTexture = function (target, texture) {
        bound = texture;
        if (texture && !states.has(texture))
          states.set(texture, { width: 0, min: 0, mag: 0 });
        return Reflect.apply(originalBind, this, [target, texture]);
      };
      proto.texParameteri = function (target, name, value) {
        if (bound) {
          const s = states.get(bound)!;
          if (name === 10241) s.min = value;
          if (name === 10240) s.mag = value;
        }
        return Reflect.apply(originalFilter, this, [target, name, value]);
      };
      proto.texImage2D = function (...args: unknown[]) {
        const source = args[args.length - 1] as unknown as HTMLImageElement;
        if (bound && source?.width === 4096) {
          const s = states.get(bound)!;
          s.width = 4096;
          results.push(s);
        }
        return Reflect.apply(originalUpload, this, args);
      };
    }
  });
  const errors = await boot(page, "webgl");
  await place(page, 1376, 3960);
  expect(await page.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
    "WebGL",
  );
  const samples = await page.evaluate(
    () =>
      (
        window as unknown as {
          __GL_ATLASES__: { width: number; min: number; mag: number }[];
        }
      ).__GL_ATLASES__,
  );
  expect(samples.length).toBeGreaterThan(0);
  for (const s of samples) {
    expect(s.min).toBe(9728);
    expect(s.mag).toBe(9728);
  }
  expect(errors).toEqual([]);
});
test("OS reduced motion stays honored; original water pixels visibly animate only when enabled", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 1440, height: 1140 },
    reducedMotion: "reduce",
  });
  try {
    const p = await c.newPage();
    const errors = await boot(p);
    await place(p, 2560, 4880);
    const frozen = await pixels(p, [640, 620, 128, 100]);
    const clock = await p.evaluate(() => window.__SEOUL__!.ambientClock);
    await p.waitForTimeout(500);
    expect(await pixels(p, [640, 620, 128, 100])).toEqual(frozen);
    expect(await p.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(clock);
    await p.emulateMedia({ reducedMotion: "no-preference" });
    await p.waitForFunction(() => window.__SEOUL__!.ambientClock > 300);
    const live = await pixels(p, [640, 620, 128, 100]);
    await expect
      .poll(
        async () => {
          const next = await pixels(p, [640, 620, 128, 100]);
          let changed = 0;
          for (let i = 0; i < next.length; i += 4)
            if (
              next[i] !== live[i] ||
              next[i + 1] !== live[i + 1] ||
              next[i + 2] !== live[i + 2]
            )
              changed++;
          return changed;
        },
        { timeout: 3000, intervals: [80, 120, 180] },
      )
      .toBeGreaterThan(128);
    await p.emulateMedia({ reducedMotion: "reduce" });
    await p.waitForTimeout(100);
    const t = await p.evaluate(() => window.__SEOUL__!.ambientClock);
    await p.waitForTimeout(200);
    expect(await p.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(t);
    expect(errors).toEqual([]);
  } finally {
    await c.close();
  }
});
test("new rail collision blocks track access while designated crossing stays open", async ({
  page,
}) => {
  const errors = await boot(page);
  await place(page, 1504, 3488);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForTimeout(1700);
  await page.keyboard.up("ArrowDown");
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(3560);
  await place(page, 1936, 3504);
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction(() => window.__SEOUL__!.y > 3620);
  await page.keyboard.up("ArrowDown");
  expect(errors).toEqual([]);
});
test("new library and cafe foundations block penetration, not street approaches", async ({
  page,
}) => {
  const errors = await boot(page);
  for (const [x, y] of [
    [2544, 2656],
    [2672, 3184],
  ]) {
    await place(page, x, y + 44);
    await page.locator("canvas").focus();
    await page.keyboard.down("ArrowUp");
    await page.waitForTimeout(900);
    await page.keyboard.up("ArrowUp");
    expect(
      await page.evaluate(() => window.__SEOUL__!.y),
    ).toBeGreaterThanOrEqual(y);
  }
  expect(errors).toEqual([]);
});
test("native pixel canvas stays the same size at DPR1 and3", async ({
  browser,
}) => {
  const bodies: number[][] = [];
  for (const dpr of [1, 3]) {
    const c = await browser.newContext({
      viewport: { width: 1440, height: 1140 },
      deviceScaleFactor: dpr,
      reducedMotion: "reduce",
    });
    try {
      const p = await c.newPage();
      await boot(p);
      await place(p, 1376, 3960);
      const size = await p
        .locator("canvas")
        .evaluate((c) => [
          (c as HTMLCanvasElement).width,
          (c as HTMLCanvasElement).height,
        ]);
      expect(size).toEqual([1024, 768]);
      bodies.push(await pixels(p, [464, 344, 96, 112]));
    } finally {
      await c.close();
    }
  }
  expect(bodies[0]).toEqual(bodies[1]);
});
for (const [id, x, y] of [
  ["civic", 2176, 3056],
  ["namsan", 3520, 2960],
  ["station", 1376, 3960],
  ["leisure", 3408, 3912],
  ["coast", 2560, 4760],
  ["jeju", 1536, 5552],
] as const)
  test(`mobile real native review: ${id}`, async ({ browser }) => {
    const c = await browser.newContext({
      viewport: { width: 844, height: 390 },
      deviceScaleFactor: 1,
      isMobile: true,
      hasTouch: true,
      reducedMotion: "reduce",
    });
    try {
      const p = await c.newPage();
      const errors = await boot(p);
      await place(p, x, y);
      expect(await p.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
        "Canvas",
      );
      expect(await p.evaluate(() => window.__PIXEL_METRICS__!.cameraZoom)).toBe(
        1,
      );
      const out = `${process.env.PIXEL_REPORT_DIR ?? ".cache/browser"}/mobile`;
      await fs.mkdir(out, { recursive: true });
      await p.screenshot({ path: `${out}/${id}.png` });
      for (const button of ["run", "interact", "talk", "emote"]) {
        const b = (await p.locator("#" + button).boundingBox())!;
        expect(b.width).toBeGreaterThanOrEqual(44);
        expect(b.height).toBeGreaterThanOrEqual(44);
        expect(b.y + b.height).toBeLessThanOrEqual(390);
      }
      expect(errors).toEqual([]);
    } finally {
      await c.close();
    }
  });
test("approved Juni walk/run/emotes use distinct real atlas frames and recover", async ({
  page,
}) => {
  await boot(page);
  await place(page, 2176, 2448);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "walk");
  const a = await page.evaluate(() => window.__PLAZA_REVIEW__!.frame);
  await page.keyboard.down("Shift");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "run");
  const b = await page.evaluate(() => window.__PLAZA_REVIEW__!.frame);
  expect(a).not.toBe(b);
  await page.keyboard.up("Shift");
  await page.keyboard.up("ArrowDown");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "idle");
  await page.locator("#emote").click();
  await page.locator("#celebrate").click();
  await page.waitForFunction(
    () => window.__PLAZA_REVIEW__?.action === "celebrate",
  );
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "idle");
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.animationFrames),
  ).toBe(144);
});

test("automatic Canvas fallback remains rendered and playable without WebGL", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const native = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (...args: unknown[]) {
      if (String(args[0]).includes("webgl")) return null;
      return Reflect.apply(native, this, args);
    };
  });
  await page.goto("v9-world-review.html?qa");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  expect(await page.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
    "Canvas",
  );
  await place(page, 2176, 2448);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction(() => window.__SEOUL__!.y > 2472);
  await page.keyboard.up("ArrowDown");
  const data = await pixels(page);
  expect(new Set(data).size).toBeGreaterThan(40);
});

test("Juni cue matches source-alpha reference behind new civic tree and clears on exit", async ({
  browser,
}) => {
  const images: string[] = [];
  for (const mode of ["cached", "reference"]) {
    const c = await browser.newContext({
      viewport: { width: 1440, height: 1140 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    try {
      const p = await c.newPage();
      await p.goto(
        "v9-world-review.html?qa&renderer=canvas" +
          (mode === "reference" ? "&occlusion=reference" : ""),
      );
      await p.waitForFunction(() => window.__SEOUL__?.ready);
      await place(p, 2176, 2840);
      await p.waitForFunction(
        () => window.__PLAZA_REVIEW__!.occludedPixels > 0,
      );
      images.push(
        await p
          .locator("canvas")
          .evaluate((c) => (c as HTMLCanvasElement).toDataURL()),
      );
      if (mode === "cached") {
        await p.locator("canvas").focus();
        await p.keyboard.down("ArrowLeft");
        await p.waitForFunction(() => window.__SEOUL__!.x < 2032);
        await p.keyboard.up("ArrowLeft");
        await p.waitForFunction(
          () => window.__PLAZA_REVIEW__!.occludedPixels === 0,
        );
      }
    } finally {
      await c.close();
    }
  }
  expect(images[0]).toBe(images[1]);
});
