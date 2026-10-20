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
  await p.goto("v7-world-review.html?qa&renderer=canvas");
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
import { readFileSync } from "node:fs";
const routes = JSON.parse(
  readFileSync("assets-src/v7-world/routes.json", "utf8"),
) as { id: string; points: number[][] }[];
function route(id: string, reverse = false) {
  const points = routes
    .find((r) => r.id === id)!
    .points.filter((_, i, a) => i % 4 === 0 || i === a.length - 1);
  return reverse ? [...points].reverse() : points;
}
test("V7 historical transition, station facade and physical rail crossing", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 2176, 1984);
  await follow(page, route("historic-threshold"));
  await follow(page, route("west-station-arrival"));
  await follow(page, [
    [2240, 2928],
    [2240, 2888],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("Nhà ga");
  await page.locator("#close-dialog").click();
  await follow(page, [[2240, 2928], ...route("rail-and-platform-stair")]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThan(3350);
  await place(page, 2400, 3024);
  await walk(page, "ArrowDown", 1000);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(3045);
});
test("V7 Namsan real entrance, full scenic loop and central terrace stairs", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 1456, 3712);
  await follow(page, route("namsan-arrival"));
  await follow(page, route("namsan-tower-loop"));
  await follow(page, route("lookout-stairs"));
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "namsan",
  );
});
test("V7 amusement gateway, full loop and independent attraction courts", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 3152, 3712);
  await follow(page, route("amusement-entry"));
  await follow(page, [[3352, 3456], [3352, 3200], ...route("amusement-loop")]);
  await follow(page, [[3352, 3200], [3472, 3128], ...route("wheel-arrival")]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("관람차");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [3464, 3128],
    [3920, 3128],
    ...route("carousel-arrival"),
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("회전목마");
});
test("V7 coastal bridge, visible ferry boarding, island trails and reciprocal arrival", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 2744, 3712);
  await follow(page, route("coastal-channel-bridge"));
  await follow(page, route("coastal-channel-bridge", true));
  await follow(page, [[2240, 3712], ...route("mainland-boarding")]);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
  await follow(page, route("jeju-arrival"));
  await follow(page, route("jeju-garden-link"));
  await follow(page, route("jeju-learning-arrival"));
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("basalt");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [2160, 4800],
    ...route("jeju-garden-link", true),
    ...route("jeju-arrival", true),
    [2704, 4240],
  ]);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(
    () => window.__FULL_WORLD__?.district === "busan-coast",
  );
});
test("V7 mobile uses actual analog movement, retained motion preference and portrait pause", async ({
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
    await place(p, 2240, 2928);
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
