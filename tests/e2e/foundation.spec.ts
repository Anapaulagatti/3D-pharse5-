import { test, expect, type Page } from "@playwright/test";
async function ready(p: Page, qa = true) {
  await p.goto("v10-city-review.html" + (qa ? "?qa&renderer=canvas" : ""));
  await p.waitForFunction(
    () =>
      window.__WORLD_REVIEW__?.candidate === "v10-final-art-review" &&
      window.__SEOUL__?.ready,
  );
}
async function place(p: Page, x: number, y: number) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  const n = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__!.frameCount >= n + 4,
    n,
  );
}
test("preserved north normal entry: actual Juni walk and gesture recover", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await ready(page, false);
  expect(await page.evaluate(() => !!window.__SEOUL_TEST__)).toBe(false);
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.animationFrames),
  ).toBe(144);
  const y = await page.evaluate(() => window.__SEOUL__!.y);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction((y) => window.__SEOUL__!.y > y + 16, y);
  await page.keyboard.up("ArrowDown");
  await page.keyboard.press("Space");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "wave");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.action === "idle");
  expect(errors).toEqual([]);
});
test("approved Academy lesson and return remain functional after cleanup", async ({
  page,
}) => {
  await ready(page);
  await place(page, 1568, 1120);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "room");
  await place(page, 385, 392);
  await page.locator("#interact").click();
  await expect(page.locator(".hangul-letter")).toBeVisible();
  await page.locator("#close-dialog").click();
  await place(page, 384, 490);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
});
test("palace intent toggles retained gate and prevents closing on Juni", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2176, 800);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__FULL_WORLD__?.gateOpen);
  await page.locator("#close-dialog").click();
  await place(page, 2176, 688);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("ngưỡng cửa");
  expect(await page.evaluate(() => window.__FULL_WORLD__!.gateOpen)).toBe(true);
});
test("mobile analog movement, reduced motion and portrait pause survive cleanup", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    reducedMotion: "reduce",
  });
  try {
    const p = await c.newPage();
    await ready(p);
    await place(p, 2176, 1328);
    const s = await c.newCDPSession(p),
      b = (await p.locator("#joystick").boundingBox())!,
      cx = b.x + b.width / 2,
      cy = b.y + b.height / 2;
    await s.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: cx, y: cy, id: 1 }],
    });
    await s.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: cx + b.width * 0.25, y: cy, id: 1 }],
    });
    await p.waitForFunction(() => window.__SEOUL__!.x > 2190);
    await s.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    const t = await p.evaluate(() => window.__SEOUL__!.ambientClock);
    await p.waitForTimeout(180);
    expect(await p.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(t);
    await p.setViewportSize({ width: 390, height: 844 });
    await expect(p.locator("#rotate-screen")).toBeVisible();
    await p.setViewportSize({ width: 844, height: 390 });
    await expect(p.locator("#rotate-screen")).toBeHidden();
    for (const id of ["interact", "run", "talk", "emote"]) {
      const box = (await p.locator("#" + id).boundingBox())!;
      expect(box.width).toBeGreaterThanOrEqual(44);
      expect(box.height).toBeGreaterThanOrEqual(44);
    }
  } finally {
    await c.close();
  }
});
