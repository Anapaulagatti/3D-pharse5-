import { test, expect, type Page } from "@playwright/test";

async function axis(
  page: Page,
  key: string,
  field: "x" | "y",
  target: number,
  positive: boolean,
) {
  await page.locator("canvas").focus();
  await page.keyboard.down(key);
  try {
    // Browser-local key release avoids a Node/CDP polling overshoot at the44px bridge.
    // Only a keyboard event: no position, velocity, collider or assertion mutation.
    await page.evaluate(
      ({ field, target, positive }) =>
        new Promise<void>((resolve, reject) => {
          const start = performance.now();
          const tick = () => {
            const value = window.__PIXEL_METRICS__![field];
            if (positive ? value >= target : value <= target) {
              const key =
                field === "x"
                  ? positive
                    ? "ArrowRight"
                    : "ArrowLeft"
                  : positive
                    ? "ArrowDown"
                    : "ArrowUp";
              const keyCode = {
                ArrowRight: 39,
                ArrowLeft: 37,
                ArrowDown: 40,
                ArrowUp: 38,
              }[key];
              window.dispatchEvent(
                new KeyboardEvent("keyup", {
                  key,
                  code: key,
                  keyCode,
                  bubbles: true,
                }),
              );
              resolve();
            } else if (performance.now() - start > 20000)
              reject(Error(`Actual movement did not reach ${field}=${target}`));
            else requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        }),
      { field, target, positive },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.waitForTimeout(160);
}

test("new layered district retains the controller: water blocks, bridge passes, Juni occludes without canopy fading", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await page.goto("./plaza-review.html");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.waitForFunction(() => window.__PIXEL_METRICS__!.reduced);
  const daylight = await page.locator("canvas").screenshot();
  await page.locator("#night").click();
  await page.waitForTimeout(100);
  const evening = await page.locator("canvas").screenshot();
  expect(evening.equals(daylight)).toBe(false);
  await page.locator("#night").click();
  const initial = await page.evaluate(() => ({
    r: window.__PLAZA_REVIEW__!,
    m: window.__PIXEL_METRICS__!,
  }));
  expect(initial.r.player).toContain("Juni");
  expect(initial.r.staticCharacter).toBe(false);
  expect(initial.m.colliders).toBe(33);
  expect(initial.m.guests).toHaveLength(0);
  expect(initial.m.animationFrames).toBe(144);
  await axis(page, "ArrowUp", "y", 555, false);
  await axis(page, "ArrowRight", "x", 661, true);
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(650);
  await page.keyboard.up("ArrowRight");
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.x),
  ).toBeLessThanOrEqual(664.2);
  await axis(page, "ArrowDown", "y", 605, true);
  await axis(page, "ArrowRight", "x", 780, true);
  await expect
    .poll(() => page.evaluate(() => window.__PLAZA_REVIEW__!.occludedPixels))
    .toBeGreaterThan(100);
  await axis(page, "ArrowDown", "y", 720, true);
  expect(
    await page.evaluate(() => window.__PLAZA_REVIEW__!.occludedPixels),
  ).toBe(0);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog")).toBeVisible();
  await expect
    .poll(() => page.evaluate(() => window.__PIXEL_METRICS__!.interactions))
    .toBeGreaterThan(0);
  expect(errors).toEqual([]);
});

test("mobile Canvas fallback preserves touch movement, reduced-motion and pause freeze the environment", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  try {
    const page = await context.newPage();
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.addInitScript(() => {
      const get = HTMLCanvasElement.prototype.getContext;
      HTMLCanvasElement.prototype.getContext = function (
        this: HTMLCanvasElement,
        kind,
        ...args
      ) {
        if (String(kind).startsWith("webgl")) return null;
        return Reflect.apply(get, this, [kind, ...args]);
      } as typeof get;
    });
    await page.goto("./plaza-review.html");
    await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
    expect(await page.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
      "Canvas",
    );
    const clock = await page.evaluate(
      () => window.__PLAZA_REVIEW__!.environmentClock,
    );
    await page.waitForTimeout(300);
    expect(
      await page.evaluate(() => window.__PLAZA_REVIEW__!.environmentClock),
    ).toBe(clock);
    const before = await page.evaluate(() => window.__PIXEL_METRICS__!.x);
    const button = page.locator('[data-x="1"]');
    await button.scrollIntoViewIfNeeded();
    const box = (await button.boundingBox())!;
    const touch = await context.newCDPSession(page);
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: box.x + box.width / 2, y: box.y + box.height / 2 }],
    });
    await expect
      .poll(() => page.evaluate(() => window.__PIXEL_METRICS__!.x))
      .toBeGreaterThan(before + 15);
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await expect
      .poll(() =>
        page.evaluate(() => window.__PLAZA_REVIEW__!.environmentClock),
      )
      .toBeGreaterThan(clock + 100);
    await page.locator("#pause").click();
    await page.waitForFunction(() => window.__PIXEL_METRICS__!.paused);
    const paused = await page.evaluate(
      () => window.__PLAZA_REVIEW__!.environmentClock,
    );
    await page.waitForTimeout(300);
    expect(
      await page.evaluate(() => window.__PLAZA_REVIEW__!.environmentClock),
    ).toBe(paused);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    expect(errors).toEqual([]);
  } finally {
    await context.close();
  }
});
