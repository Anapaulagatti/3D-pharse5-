import { existsSync } from "node:fs";
import { test, expect, type Page } from "@playwright/test";
// Use the same default Canvas compositor as the shipped fallback. Forced software-WebGL is
// separately verified by tools/verify_v6_renderers.mjs; old browser cases are unchanged.
test.use({
  launchOptions: {
    executablePath:
      process.env.PIXEL_CHROMIUM_PATH ??
      (existsSync("/usr/bin/chromium") ? "/usr/bin/chromium" : undefined),
    args: ["--no-sandbox"],
  },
});
async function ready(p: Page) {
  await p.goto("v6-world-review.html?qa&renderer=canvas");
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
test("V6 actual relocation preserves north and routes all five districts", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.world)).toEqual([
    4352, 5312,
  ]);
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.animationFrames),
  ).toBe(144);
  await place(page, 2176, 2176);
  await follow(page, [
    [2176, 2608],
    [1856, 2608],
    [1856, 3024],
    [2240, 3024],
    [2240, 3312],
    [2240, 3504],
    [2016, 3504],
    [2016, 3680],
    [2496, 3680],
    [2496, 3912],
  ]);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
  await follow(page, [
    [2496, 4376],
    [2528, 4560],
    [2528, 4640],
    [2240, 4640],
    [2240, 4800],
    [2144, 4800],
    [2144, 4840],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("basalt");
  await page.locator("#close-dialog").click();
  await place(page, 2496, 4208);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(
    () => window.__FULL_WORLD__?.district === "busan-coast",
  );
});
test("V6 Namsan entrance and park physical approaches remain accessible", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 1472, 3536);
  await follow(page, [
    [1120, 3536],
    [1120, 3296],
  ]);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "namsan",
  );
  await place(page, 3024, 3584);
  await follow(page, [
    [3552, 3584],
    [3552, 3424],
    [3520, 3152],
    [3328, 3152],
    [3328, 3104],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("관람차");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [3328, 3152],
    [3968, 3152],
    [3968, 3072],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("회전목마");
});
test("V6 new rail barrier blocks outside its relocated crossing", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2400, 3056);
  await walk(page, "ArrowDown", 1100);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(3092);
  await place(page, 2240, 3056);
  await follow(page, [[2240, 3312]]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThan(3280);
});
test("V6 mobile uses actual analog movement, retained motion preference and portrait pause", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  try {
    const p = await c.newPage();
    await ready(p);
    await place(p, 2240, 3536);
    const d = await c.newCDPSession(p),
      box = (await p.locator("#joystick").boundingBox())!,
      cx = box.x + box.width / 2,
      cy = box.y + box.height / 2;
    await d.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: cx, y: cy, id: 1 }],
    });
    await d.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: cx + box.width * 0.25, y: cy, id: 1 }],
    });
    await p.waitForFunction(() => window.__SEOUL__!.x > 2254);
    expect(
      await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude),
    ).toBeGreaterThan(0);
    await d.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    await settled(p);
    const clock = await p.evaluate(() => window.__SEOUL__!.ambientClock);
    await p.waitForTimeout(200);
    expect(await p.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(clock);
    await p.setViewportSize({ width: 390, height: 844 });
    await expect(p.locator("#rotate-screen")).toBeVisible();
    await p.setViewportSize({ width: 844, height: 390 });
    await expect(p.locator("#rotate-screen")).toBeHidden();
    expect(await p.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
      "Canvas",
    );
    for (const id of ["interact", "run", "talk", "emote"]) {
      const r = (await p.locator("#" + id).boundingBox())!;
      expect(r.width).toBeGreaterThanOrEqual(44);
      expect(r.height).toBeGreaterThanOrEqual(44);
    }
  } finally {
    await c.close();
  }
});
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
