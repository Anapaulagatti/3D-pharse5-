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

test("Namsan travel is reciprocal, true stairs pass, retaining face blocks, exact north pixels return", async ({
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
  await page.emulateMedia({ reducedMotion: "reduce" });
  await ready(page);
  await place(page, 1152, 2016);
  const before = await page
    .locator("canvas")
    .evaluate((c) => (c as HTMLCanvasElement).toDataURL());
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("hư cấu");
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__KOREA__?.district === "namsan");
  expect(await page.evaluate(() => window.__SEOUL__!.world)).toEqual([
    1408, 1280,
  ]);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBe(1056);
  await expect(page.locator("#mini-map")).toHaveAttribute(
    "src",
    /park\/minimap\.png/,
  );
  await place(page, 1032, 848);
  await walk(page, "ArrowUp", 1100);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThan(808);
  await place(page, 1120, 872);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForFunction(() => window.__SEOUL__!.y < 780);
  await page.keyboard.up("ArrowUp");
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(784);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("전망");
  await page.locator("#scenic-view").click();
  await page.waitForFunction(
    () => window.__PIXEL_METRICS__?.cameraZoom === 0.5,
  );
  await page.locator("#settings-open").click();
  await page.selectOption("#zoom", "1");
  await page.locator("#settings-close").click();
  await place(page, 704, 1088);
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__KOREA__?.district === "heritage");
  await place(page, 1152, 2016);
  const after = await page
    .locator("canvas")
    .evaluate((c) => (c as HTMLCanvasElement).toDataURL());
  expect(after).toBe(before);
  expect(await page.evaluate(() => window.__KOREA__!.travelTransitions)).toBe(
    2,
  );
  expect(errors).toEqual([]);
});

test("landscape layouts keep touch, safe-area controls and Hangul dialogue usable; unsupported lock has fallback", async ({
  browser,
}) => {
  for (const [width, height] of [
    [568, 320],
    [640, 360],
    [844, 390],
    [932, 430],
  ]) {
    const c = await browser.newContext({
      viewport: { width, height },
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 3,
      reducedMotion: "reduce",
    });
    const p = await c.newPage();
    try {
      await ready(p);
      await p.evaluate(() => {
        for (const [k, v] of [
          ["--safe-left", "24px"],
          ["--safe-right", "24px"],
          ["--safe-bottom", "12px"],
        ])
          document.documentElement.style.setProperty(k, v);
      });
      for (const sel of [".dpad", ".actions", "#mini-wrap"]) {
        const r = (await p.locator(sel).boundingBox())!;
        expect(r.x).toBeGreaterThanOrEqual(24);
        expect(r.x + r.width).toBeLessThanOrEqual(width - 24);
        expect(r.y + r.height).toBeLessThanOrEqual(height - 12);
      }
      expect(
        await p.evaluate(() => document.documentElement.scrollWidth),
      ).toBeLessThanOrEqual(width);
      expect(
        await p
          .locator("canvas")
          .evaluate((c) => (c as HTMLCanvasElement).width),
      ).toBeLessThanOrEqual(1024);
      await place(p, 544, 1152);
      await p.locator("#interact").tap();
      await p.waitForFunction(() => window.__SEOUL__?.area === "room");
      await place(p, 385, 392);
      await p.locator("#interact").tap();
      await expect(p.locator(".hangul-letter")).toHaveText("ㄱ");
      const d = (await p.locator("#dialog").boundingBox())!;
      expect(d.y).toBeGreaterThanOrEqual(42);
      expect(d.y + d.height).toBeLessThanOrEqual(height - 12);
      await p.getByRole("button", { name: "giyeok", exact: true }).tap();
      await p.locator("#close-dialog").tap();
      await p.locator("#settings-open").tap();
      await p.selectOption("#control-size", "68");
      expect(
        await p
          .locator(".dpad button")
          .first()
          .evaluate((b) => b.getBoundingClientRect().width),
      ).toBe(68);
      if (width === 640) {
        // This simulates an unsupported API route; it is NOT real iOS/Android certification.
        await p.evaluate(() =>
          Object.defineProperty(screen.orientation, "lock", {
            configurable: true,
            value: () =>
              Promise.reject(
                new DOMException("unsupported", "NotSupportedError"),
              ),
          }),
        );
        await p.locator("#fullscreen").tap();
        await expect(p.locator("#orientation-status")).toContainText(
          "không khóa được",
        );
        await p.evaluate(async () => {
          if (document.fullscreenElement) await document.exitFullscreen();
        });
      }
      await p.locator("#settings-close").tap();
    } finally {
      await c.close();
    }
  }
});
