import { test, expect, type Page } from "@playwright/test";
async function ready(page: Page) {
  await page.goto("./production-review.html?qa");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
}
async function place(page: Page, x: number, y: number) {
  await page.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  await page.waitForTimeout(100);
}
async function move(
  page: Page,
  key: string,
  axis: "x" | "y",
  target: number,
  positive = false,
) {
  await page.locator("canvas").focus();
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      ({ axis, target, positive }) => {
        const p = window.__SEOUL__!;
        return positive ? p[axis] >= target : p[axis] <= target;
      },
      { axis, target, positive },
      { timeout: 20000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.waitForTimeout(160);
}

test("approved structural masses, open U courtyard, real room and preserved letter lesson", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await ready(page);
  expect((await page.evaluate(() => window.__SEOUL__!)).world).toEqual([
    4096, 1728,
  ]);
  await place(page, 672, 832);
  await move(page, "ArrowUp", "y", 773);
  const y = await page.evaluate(() => window.__SEOUL__!.y);
  expect(y).toBeGreaterThanOrEqual(770);
  expect(y).toBeLessThan(785);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "room");
  await place(page, 385, 392);
  await page.locator("#interact").click();
  await expect(page.locator(".hangul-letter")).toBeVisible();
  for (const answer of ["giyeok", "nieun", "mieum"]) {
    await page
      .locator("#dialog-copy")
      .getByRole("button", { name: answer, exact: true })
      .click();
    await page
      .locator("#dialog-copy")
      .getByRole("button", {
        name: answer === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  await expect(page.locator("#dialog-copy")).toContainText("Hoàn thành");
  await page.locator("#close-dialog").click();
  await place(page, 384, 490);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeCloseTo(672, 0);
  await place(page, 672, 1010);
  await move(page, "ArrowLeft", "x", 580);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeLessThan(620);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(456);
  await place(page, 3008, 1632);
  await move(page, "ArrowDown", "y", 1674, true);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThanOrEqual(
    1677,
  );
  expect(errors).toEqual([]);
});
test("palace leaf collision really opens, safe close refuses player in threshold, inner palace remains closed", async ({
  page,
}) => {
  await ready(page);
  await place(page, 2048, 832);
  await move(page, "ArrowUp", "y", 741);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    739,
  );
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.gateOpen === true);
  await page.locator("#close-dialog").click();
  await move(page, "ArrowUp", "y", 660);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(690);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.gateOpen === true);
  await expect(page.locator("#dialog-copy")).toContainText("ngưỡng cửa");
  await page.locator("#close-dialog").click();
  await move(page, "ArrowUp", "y", 453);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    451,
  );
  await place(page, 2048, 800);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.gateOpen === false);
  await page.locator("#close-dialog").click();
  await move(page, "ArrowUp", "y", 741);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    739,
  );
});
test("mobile Canvas touch, reduced-motion and pause preserve usable world", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("./production-review.html?renderer=canvas");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  expect(await page.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
    "Canvas",
  );
  expect(await page.evaluate(() => !!window.__SEOUL_TEST__)).toBe(false);
  await expect(page.locator("#motion")).toBeChecked();
  const clock = await page.evaluate(() => window.__SEOUL__!.ambientClock);
  await page.waitForTimeout(250);
  expect(await page.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(clock);
  const right = page.locator('[data-x="1"]');
  await right.scrollIntoViewIfNeeded();
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setTouchEmulationEnabled", { enabled: true });
  const box = (await right.boundingBox())!;
  const touch = async () =>
    cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: box.x + box.width / 2, y: box.y + box.height / 2 }],
    });
  const release = async () =>
    cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  await touch();
  const x = await page.evaluate(() => window.__SEOUL__!.x);
  await page.waitForTimeout(500);
  await release();
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(
    x + 15,
  );
  await page.locator("#pause").click();
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.paused);
  // Scene metrics precede Arcade's post-update flush in the first paused frame.
  const pauseFrame = await page.evaluate(
    () => window.__PIXEL_METRICS__!.frameCount,
  );
  await page.waitForFunction(
    (frame) =>
      window.__PIXEL_METRICS__!.paused &&
      window.__PIXEL_METRICS__!.frameCount >= frame + 2,
    pauseFrame,
  );
  const frozen = await page.evaluate(() => window.__SEOUL__!.x);
  await right.scrollIntoViewIfNeeded();
  const b2 = (await right.boundingBox())!;
  box.x = b2.x;
  box.y = b2.y;
  await touch();
  await page.waitForTimeout(250);
  await release();
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBe(frozen);
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(390);
});

test("courtyard additions have small real foot collisions and leave the Academy centre open", async ({
  page,
}) => {
  await ready(page);
  for (const [x, y] of [
    [824, 940],
    [3100, 804],
    [3592, 948],
    [3824, 1352],
  ]) {
    await place(page, x, y + 42);
    await page.locator("canvas").focus();
    await page.keyboard.down("ArrowUp");
    try {
      await page.waitForFunction(
        ({ y }) => window.__SEOUL__!.y < y + 9,
        { y },
        { timeout: 10000 },
      );
      await page.waitForTimeout(350);
      const actual = await page.evaluate(() => window.__SEOUL__!.y);
      expect(actual).toBeGreaterThanOrEqual(y + 3);
      expect(actual).toBeLessThan(y + 9);
    } finally {
      await page.keyboard.up("ArrowUp");
    }
  }
  await place(page, 672, 1216);
  await move(page, "ArrowUp", "y", 852);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(860);
});
