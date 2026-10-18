import { test, expect, type Page } from "@playwright/test";
async function ready(p: Page) {
  await p.goto("full-world-review.html?qa&renderer=canvas");
  await p.waitForFunction(() => window.__FULL_WORLD__?.world[0] === 4352);
}
async function settled(p: Page) {
  const n = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__!.frameCount >= n + 4,
    n,
  );
}
async function place(p: Page, x: number, y: number) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  await settled(p);
}
async function walk(p: Page, key: string, ms: number) {
  await p.locator("canvas").focus();
  await p.keyboard.down(key);
  await p.waitForTimeout(ms);
  await p.keyboard.up(key);
}
async function follow(p: Page, points: number[][]) {
  const dense: number[][] = [];
  let from = await p.evaluate(() => [window.__SEOUL__!.x, window.__SEOUL__!.y]);
  for (const to of points) {
    const n = Math.max(
      1,
      Math.ceil(Math.hypot(to[0] - from[0], to[1] - from[1]) / 16),
    );
    for (let i = 1; i <= n; i++)
      dense.push([
        from[0] + ((to[0] - from[0]) * i) / n,
        from[1] + ((to[1] - from[1]) * i) / n,
      ]);
    from = to;
  }
  const held = new Set<string>();
  await p.locator("canvas").focus();
  await p.keyboard.down("Shift");
  try {
    for (const [x, y] of dense) {
      const began = Date.now();
      for (;;) {
        const s = await p.evaluate(() => window.__SEOUL__!);
        if (Math.abs(s.x - x) < 6 && Math.abs(s.y - y) < 6) break;
        if (Date.now() - began > 24000)
          throw Error(
            `Actual walking stuck near ${x},${y}: ${JSON.stringify(s)}`,
          );
        const keys = new Set<string>();
        if (s.x < x - 4) keys.add("ArrowRight");
        if (s.x > x + 4) keys.add("ArrowLeft");
        if (s.y < y - 4) keys.add("ArrowDown");
        if (s.y > y + 4) keys.add("ArrowUp");
        for (const k of held)
          if (!keys.has(k)) {
            await p.keyboard.up(k);
            held.delete(k);
          }
        for (const k of keys)
          if (!held.has(k)) {
            await p.keyboard.down(k);
            held.add(k);
          }
        await p.waitForTimeout(25);
      }
    }
  } finally {
    for (const k of held) await p.keyboard.up(k);
    await p.keyboard.up("Shift");
  }
  await settled(p);
}
test("full world loads all five destinations,144frame Juni and bounded visible scenery", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await ready(page);
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.animationFrames),
  ).toBe(144);
  for (const [id, x, y] of [
    ["heritage", 2176, 1328],
    ["namsan", 832, 2912],
    ["entertainment", 3712, 2896],
    ["busan-coast", 2048, 2944],
    ["jeju", 2240, 4208],
  ] as const) {
    await place(page, x, y);
    expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(id);
    const n = await page.evaluate(() => window.__FULL_WORLD__!);
    expect(n.activeProps).toBeGreaterThan(4);
    expect(n.activeProps).toBeLessThan(n.totalProps);
    expect(n.totalProps).toBe(296);
  }
  expect(errors).toEqual([]);
});
test("all mainland districts connect through actual walking and Jeju through explicit reciprocal ferry", async ({
  page,
}) => {
  test.setTimeout(180000);
  await ready(page);
  await place(page, 2176, 2016);
  await follow(page, [
    [2176, 2368],
    [1600, 2368],
    [1440, 2464],
    [1280, 2416],
    [1024, 2416],
    [832, 2560],
    [608, 2624],
    [608, 2928],
    [704, 2992],
    [832, 2992],
    [832, 2912],
  ]);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "namsan",
  );
  await follow(page, [
    [832, 2992],
    [704, 2992],
    [608, 2928],
    [608, 2624],
    [832, 2560],
    [1024, 2416],
    [1280, 2416],
    [1440, 2464],
    [1600, 2368],
    [2176, 2368],
    [2944, 2368],
    [2992, 2512],
    [2976, 2784],
    [3136, 2800],
    [3328, 2816],
    [3456, 2848],
    [3712, 2848],
  ]);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "entertainment",
  );
  await follow(page, [
    [3712, 3120],
    [3712, 3296],
    [3328, 3296],
    [3072, 3136],
    [2912, 3136],
    [2848, 3136],
  ]);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "busan-coast",
  );
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
  await follow(page, [
    [1952, 4480],
    [2080, 4256],
    [2240, 4128],
  ]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(4140);
  await follow(page, [
    [2080, 4256],
    [1952, 4480],
    [1760, 4544],
  ]);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(
    () => window.__FULL_WORLD__?.district === "busan-coast",
  );
  expect(
    await page.evaluate(() => window.__FULL_WORLD__!.transitions),
  ).toBeGreaterThanOrEqual(2);
});
test("drag joystick has analog strength, diagonal motion, independent sprint and correct partial release", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    reducedMotion: "no-preference",
  });
  const p = await c.newPage();
  try {
    await ready(p);
    await place(p, 2176, 1328);
    const d = await c.newCDPSession(p),
      box = (await p.locator("#joystick").boundingBox())!,
      run = (await p.locator("#run").boundingBox())!,
      cx = box.x + box.width / 2,
      cy = box.y + box.height / 2,
      r = box.width * 0.34;
    let a = { x: cx, y: cy, id: 1 };
    const b = { x: run.x + run.width / 2, y: run.y + run.height / 2, id: 2 };
    await d.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [a],
    });
    await p.waitForTimeout(200);
    expect(await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude)).toBe(
      0,
    );
    a = { x: cx + r * 0.55, y: cy, id: 1 };
    await d.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [a],
    });
    // CI/software GPU frame throughput varies. Observe real displacement and
    // fractional physics velocity, rather than treating700ms as an FPS guarantee.
    await p.waitForFunction(() => window.__SEOUL__!.x > 2186, undefined, {
      timeout: 4000,
    });
    const slow = await p.evaluate(() => ({
      x: window.__SEOUL__!.x,
      m: window.__FULL_WORLD__!.analogMagnitude,
      velocity: window.__FULL_WORLD__!.velocity,
    }));
    expect(slow.x - 2176).toBeGreaterThan(10);
    expect(slow.x - 2176).toBeLessThan(28);
    expect(slow.m).toBeGreaterThan(0.4);
    expect(slow.m).toBeLessThan(0.6);
    expect(slow.velocity[0]).toBeCloseTo(slow.m * 60, 0);
    expect(Math.abs(slow.velocity[1])).toBeLessThan(0.01);
    await d.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [a, b],
    });
    a = { x: cx + r * 0.7072, y: cy - r * 0.7072, id: 1 };
    await d.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [a, b],
    });
    await p.waitForFunction(() => window.__SEOUL__!.y < 1295, undefined, {
      timeout: 3000,
    });
    expect(await p.evaluate(() => window.__PIXEL_METRICS__!.speed)).toBe(100);
    expect(
      await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude),
    ).toBeGreaterThan(0.98);
    expect(
      await p.evaluate(() => Math.hypot(...window.__FULL_WORLD__!.velocity)),
    ).toBeGreaterThan(95);
    expect(await p.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(1295);
    await d.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [b],
    });
    await p.waitForTimeout(180);
    expect(await p.evaluate(() => window.__PIXEL_METRICS__!.speed)).toBe(60);
    expect(
      await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude),
    ).toBeGreaterThan(0.98);
    await d.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    await p.waitForTimeout(180);
    expect(await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude)).toBe(
      0,
    );
    await p.locator("#emote").tap();
    await p.locator("#wave").tap();
    await p.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "wave");
    await p.locator("#interact").tap();
    await expect(p.locator("#dialog")).toBeVisible();
    await p.locator("#talk").tap();
    await expect(p.locator("#dialog")).toBeHidden();
  } finally {
    await c.close();
  }
});
test("royal gate has real safe closure and retained Academy room lesson returns to global entrance", async ({
  page,
}) => {
  await ready(page);
  await page.locator("#interact").click();
  await page.locator("#close-dialog").click();
  expect(await page.evaluate(() => window.__FULL_WORLD__!.gateOpen)).toBe(true);
  await follow(page, [[2176, 700]]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("ngưỡng cửa");
  await page.locator("#close-dialog").click();
  expect(await page.evaluate(() => window.__FULL_WORLD__!.gateOpen)).toBe(true);
  await place(page, 1568, 1152);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "room");
  await place(page, 385, 392);
  await page.locator("#interact").click();
  await expect(page.locator(".hangul-letter")).toHaveText("ㄱ");
  await page.getByRole("button", { name: "giyeok", exact: true }).click();
  await expect(page.locator("#dialog-copy")).toContainText("giyeok");
  await page.locator("#close-dialog").click();
  await place(page, 384, 490);
  await page.locator("#interact").click();
  await page.waitForFunction(
    () => window.__FULL_WORLD__?.district === "heritage",
  );
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBe(1568);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBe(1152);
});
test("rail blocks outside timber crossing, real bridge passes and sea/oreum retain solid boundaries", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2176, 2936);
  await walk(page, "ArrowUp", 1000);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    2912,
  );
  await place(page, 2048, 2936);
  await follow(page, [[2048, 2820]]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(2848);
  await place(page, 2288, 3160);
  await follow(page, [[2464, 3160]]);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(2450);
  await place(page, 2320, 3096);
  await walk(page, "ArrowRight", 1000);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeLessThanOrEqual(
    2328,
  );
  await place(page, 2240, 3160);
  await walk(page, "ArrowDown", 1500);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(3220);
  await place(page, 2240, 4208);
  await walk(page, "ArrowUp", 2000);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    4100,
  );
});
test("landscape thumb targets fit common viewports, portrait pauses and explicit software GPU uses Canvas", async ({
  browser,
}) => {
  for (const [w, h] of [
    [568, 320],
    [640, 360],
    [844, 390],
    [932, 430],
  ]) {
    const c = await browser.newContext({
      viewport: { width: w, height: h },
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 3,
      reducedMotion: "reduce",
    });
    const p = await c.newPage();
    try {
      await ready(p);
      await expect(p.locator("#rotate-screen")).toBeHidden();
      const ids = ["joystick", "interact", "talk", "run", "emote"];
      const rects = await p.evaluate(
        (ids) =>
          ids.map((id) => {
            const r = document.getElementById(id)!.getBoundingClientRect();
            return { id, x: r.x, y: r.y, w: r.width, h: r.height };
          }),
        ids,
      );
      for (const r of rects) {
        expect(r.x).toBeGreaterThanOrEqual(0);
        expect(r.y).toBeGreaterThan(36);
        expect(r.x + r.w).toBeLessThanOrEqual(w);
        expect(r.y + r.h).toBeLessThanOrEqual(h);
        expect(Math.min(r.w, r.h)).toBeGreaterThanOrEqual(44);
      }
      for (let a = 0; a < rects.length; a++)
        for (let b = a + 1; b < rects.length; b++) {
          const x = rects[a],
            y = rects[b];
          expect(
            x.x + x.w <= y.x ||
              y.x + y.w <= x.x ||
              x.y + x.h <= y.y ||
              y.y + y.h <= x.y,
          ).toBe(true);
        }
      expect(await p.evaluate(() => window.__PIXEL_METRICS__!.reduced)).toBe(
        true,
      );
      await p.setViewportSize({ width: 390, height: 844 });
      await expect(p.locator("#rotate-screen")).toBeVisible();
      await settled(p);
      const before = await p.evaluate(() => [
        window.__SEOUL__!.x,
        window.__SEOUL__!.y,
      ]);
      await p.waitForTimeout(200);
      expect(
        await p.evaluate(() => [window.__SEOUL__!.x, window.__SEOUL__!.y]),
      ).toEqual(before);
      await p.setViewportSize({ width: w, height: h });
      await expect(p.locator("#rotate-screen")).toBeHidden();
    } finally {
      await c.close();
    }
  }
  const p = await browser.newPage();
  try {
    await p.goto("full-world-review.html");
    await p.waitForFunction(() => window.__FULL_WORLD__);
    const fallback = await p.evaluate(() => document.body.dataset.fallback);
    if (fallback === "software-gpu")
      expect(await p.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
        "Canvas",
      );
    expect(await p.evaluate(() => !!window.__SEOUL_TEST__)).toBe(false);
  } finally {
    await p.close();
  }
});
