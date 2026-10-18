import { test, expect, type Page } from "@playwright/test";
async function ready(p: Page) {
  await p.goto("living-korea-review.html?qa&renderer=canvas");
  await p.waitForFunction(() => window.__SEOUL__?.ready);
}
async function place(p: Page, x: number, y: number) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  const frame = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__!.frameCount >= n + 4,
    frame,
  );
}
async function walk(p: Page, key: string, ms: number) {
  await p.locator("canvas").focus();
  await p.keyboard.down(key);
  await p.waitForTimeout(ms);
  await p.keyboard.up(key);
}
test("repaired palace side returns block at former floating gates, main gate still opens safely", async ({
  page,
}) => {
  await ready(page);
  await place(page, 340, 392);
  await walk(page, "ArrowRight", 1000);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeLessThan(370);
  await place(page, 1964, 392);
  await walk(page, "ArrowLeft", 1000);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(1930);
  await place(page, 1152, 800);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog")).toBeVisible();
  await page.locator("#close-dialog").click();
  expect(await page.evaluate(() => window.__SEOUL__!.gateOpen)).toBe(true);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForFunction(() => window.__SEOUL__!.y < 710);
  await page.keyboard.up("ArrowUp");
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(720);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("ngưỡng cửa");
  expect(await page.evaluate(() => window.__SEOUL__!.gateOpen)).toBe(true);
});
test("academy true entrance and retained lesson survive; museum cross-lane is now physically clear", async ({
  page,
}) => {
  await ready(page);
  await place(page, 544, 1152);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "room");
  await place(page, 385, 392);
  await page.locator("#interact").click();
  await expect(page.locator(".hangul-letter")).toHaveText("ㄱ");
  await page.getByRole("button", { name: "giyeok", exact: true }).click();
  await expect(page.locator("#dialog-copy")).toContainText("giyeok");
  await page.locator("#close-dialog").click();
  await place(page, 384, 490);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
  await place(page, 1800, 1560);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowRight");
  await page.waitForFunction(() => window.__SEOUL__!.x > 1910);
  await page.keyboard.up("ArrowRight");
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(1900);
  await place(page, 1984, 2000);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("역사");
});
test("landscape touch is multi-pointer, rotates/pauses cleanly and preserves user pause", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  try {
    await ready(page);
    await expect(page.locator("#rotate-screen")).toBeHidden();
    expect(
      await page
        .locator("canvas")
        .evaluate((c) => (c as HTMLCanvasElement).width),
    ).toBeLessThanOrEqual(1024);
    expect(await page.evaluate(() => window.__PIXEL_METRICS__!.reduced)).toBe(
      true,
    );
    const client = await context.newCDPSession(page);
    const right = (await page
      .locator('[aria-label="Sang phải"]')
      .boundingBox())!;
    const run = (await page.locator("#run").boundingBox())!;
    await place(page, 1152, 1320);
    const a = {
        x: right.x + right.width / 2,
        y: right.y + right.height / 2,
        id: 1,
      },
      b = { x: run.x + run.width / 2, y: run.y + run.height / 2, id: 2 };
    await client.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [a, b],
    });
    await page.waitForTimeout(700);
    expect(
      await page.evaluate(() => window.__PIXEL_METRICS__!.speed),
    ).toBeGreaterThan(85);
    await client.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [b],
    });
    await page.waitForTimeout(150);
    expect(await page.evaluate(() => window.__PIXEL_METRICS__!.moving)).toBe(
      true,
    );
    await client.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    await page.setViewportSize({ width: 390, height: 844 });
    await expect(page.locator("#rotate-screen")).toBeVisible();
    await page.waitForFunction(() => window.__PIXEL_METRICS__?.paused);
    const pausedFrame = await page.evaluate(
      () => window.__PIXEL_METRICS__!.frameCount,
    );
    await page.waitForFunction(
      (n) => window.__PIXEL_METRICS__!.frameCount >= n + 2,
      pausedFrame,
    );
    const x = await page.evaluate(() => window.__SEOUL__!.x);
    await page.waitForTimeout(150);
    expect(await page.evaluate(() => window.__SEOUL__!.x)).toBe(x);
    await page.setViewportSize({ width: 844, height: 390 });
    await expect(page.locator("#rotate-screen")).toBeHidden();
    await page.waitForFunction(
      () => window.__PIXEL_METRICS__?.paused === false,
    );
    await page.locator("#pause").click();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.setViewportSize({ width: 844, height: 390 });
    expect(await page.locator("#pause").getAttribute("aria-pressed")).toBe(
      "true",
    );
    await page.waitForFunction(() => window.__PIXEL_METRICS__?.paused);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
  } finally {
    await context.close();
  }
});
