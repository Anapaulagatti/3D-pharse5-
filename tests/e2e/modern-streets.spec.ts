import { test, expect, type Page } from "@playwright/test";
async function ready(p: Page) {
  await p.goto("modern-streets-review.html?qa&renderer=canvas");
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
test("street candidate preserves native heritage and Jeju pixels and all five destinations", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 1440, height: 1140 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const p = await c.newPage();
  const errors: string[] = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  const captures: string[][] = [];
  try {
    for (const entry of [
      "v3-world-review.html",
      "modern-streets-review.html",
    ]) {
      await p.goto(entry + "?qa&renderer=canvas");
      await p.waitForFunction(() => window.__SEOUL__?.ready);
      const rows: string[] = [];
      for (const [x, y] of [
        [1568, 1292],
        [1830, 4384],
        [2560, 2752],
      ]) {
        await place(p, x, y);
        rows.push(
          await p
            .locator("canvas")
            .evaluate((c) => (c as HTMLCanvasElement).toDataURL()),
        );
      }
      captures.push(rows);
    }
    expect(captures[0][0]).toBe(captures[1][0]);
    expect(captures[0][1]).toBe(captures[1][1]);
    expect(captures[0][2]).not.toBe(captures[1][2]);
    for (const [district, x, y] of [
      ["heritage", 2176, 1328],
      ["namsan", 832, 2912],
      ["entertainment", 3712, 2848],
      ["busan-coast", 2048, 2944],
      ["jeju", 2240, 4144],
    ] as const) {
      await place(p, x, y);
      expect(await p.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
        district,
      );
      expect(await p.evaluate(() => window.__FULL_WORLD__!.totalProps)).toBe(
        406,
      );
    }
    expect(await p.evaluate(() => window.__V3_WORLD__!.candidate)).toBe(
      "modern-streets",
    );
    expect(
      await p.evaluate(() => window.__PIXEL_METRICS__!.animationFrames),
    ).toBe(144);
    expect(errors).toEqual([]);
  } finally {
    await c.close();
  }
});
test("cardinal threshold, actual retail zebra and station crossing remain physically walkable", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2176, 2320);
  await follow(page, [
    [2176, 2384],
    [2048, 2384],
    [2048, 2784],
    [2560, 2784],
    [2560, 2752],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("도시");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [2464, 2752],
    [2464, 2840],
    [2048, 2840],
    [2048, 3040],
  ]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThan(3028);
  await place(page, 2288, 2816);
  await walk(page, "ArrowDown", 1200);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(2858);
  await place(page, 2304, 3040);
  await follow(page, [
    [2304, 3160],
    [2464, 3160],
    [2528, 3160],
    [2528, 3136],
    [2848, 3136],
  ]);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
});
test("park arrival spine, shop and discovery approaches connect by actual cardinal walking", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2912, 3136);
  await follow(page, [
    [3232, 3136],
    [3232, 3296],
    [3712, 3296],
    [3712, 2464],
  ]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(2472);
  await follow(page, [
    [3712, 2848],
    [3920, 2848],
    [3920, 3096],
    [4144, 3096],
    [4144, 3136],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("발견");
});
test("modern street mobile uses actual analog movement, retained motion preference and portrait pause", async ({
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
    await place(p, 2560, 2784);
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
    await p.waitForFunction(() => window.__SEOUL__!.x > 2574);
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
