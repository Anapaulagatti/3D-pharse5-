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
  await p.goto("v8-city-review.html?qa&renderer=canvas");
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
  readFileSync("assets-src/v8-city/routes.json", "utf8"),
) as { id: string; points: number[][] }[];
function route(id: string, reverse = false) {
  const r = routes.find((r) => r.id === id)!;
  // Preserve authored corners on sparse urban polylines; sample only dense curves.
  const points =
    r.points.length > 20
      ? r.points.filter((_, i, a) => i % 4 === 0 || i === a.length - 1)
      : r.points;
  return reverse ? [...points].reverse() : points;
}
test("V8 continuous civic boulevard, four urban frontages and safe platform access", async ({
  page,
}) => {
  test.setTimeout(240000);
  await ready(page);
  await place(page, 2176, 2240);
  await follow(page, route("cultural-gateway"));
  await follow(page, route("civic-boulevard"));
  await follow(page, [[2112, 3008], ...route("metropolitan-avenue")]);
  await follow(page, [[3200, 3008], [3200, 2864], ...route("platform-access")]);
  await follow(page, route("platform-access", true));
  await follow(page, [[2704, 2864], ...route("station-door")]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("Nhà ga");
});
test("V8 Namsan entrance, winding loop and independent amusement campus", async ({
  page,
}) => {
  test.setTimeout(300000);
  await ready(page);
  await place(page, 1392, 3008);
  await follow(page, route("namsan-gate"));
  await follow(page, route("namsan-loop"));
  await follow(page, route("namsan-gate", true));
  await follow(page, [
    [1392, 3008],
    [2112, 3008],
    [3200, 3008],
    [3200, 3520],
    ...route("amusement-urban-access"),
  ]);
  await follow(page, [
    [3744, 3360],
    [3344, 3376],
    [3344, 2944],
    ...route("amusement-loop"),
  ]);
  await follow(page, [[3552, 2912], ...route("wheel-court-access")]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("관람차");
});
test("V8 continuous waterfront, ferry-only travel and Jeju scenic circuit", async ({
  page,
}) => {
  test.setTimeout(300000);
  await ready(page);
  await place(page, 2112, 3648);
  await follow(page, route("harbor-approach"));
  await follow(page, route("mainland-boarding"));
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
  await follow(page, route("jeju-arrival"));
  await follow(page, route("jeju-scenic-loop"));
  await follow(page, route("jeju-arrival", true));
  await follow(page, route("island-boarding", true));
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(
    () => window.__FULL_WORLD__?.district === "busan-coast",
  );
});
test("V8 mobile uses actual analog movement, retained motion preference and portrait pause", async ({
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
    await place(p, 2112, 3008);
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
    await p.waitForFunction(() => window.__SEOUL__!.x > 2126);
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
