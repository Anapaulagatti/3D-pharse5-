import { test, expect } from "@playwright/test";

test("three new static concepts render in the existing Phaser town at exact integer scales", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  await page.goto("./character-review.html");
  await page.waitForFunction(() => window.__CHARACTER_REVIEW__?.ready);
  for (const view of ["front", "back", "left", "right"]) {
    await page.locator(`[data-view="${view}"]`).click();
    await page.waitForFunction(
      (v) => window.__CHARACTER_REVIEW__!.view === v,
      view,
    );
    const m = await page.evaluate(() => window.__CHARACTER_REVIEW__!);
    expect(m.candidates.map((c) => c.id)).toEqual(["A", "B", "C"]);
    expect(m.candidates.every((c) => c.frame === view)).toBe(true);
    expect(m.staticDesignProof).toBe(true);
    expect(m.userApproval).toBe("PENDING");
    expect(m.nativeBodyHeight).toBe(80);
    for (const c of m.candidates) {
      expect(c.foot.x).toBeGreaterThan(50);
      expect(c.foot.x).toBeLessThan(m.canvas.width - 50);
      expect(c.foot.y - 80 * m.zoom).toBeGreaterThan(0);
      expect(c.foot.y).toBeLessThan(m.canvas.height);
    }
  }
  for (const zoom of ["1", "2"]) {
    await page.locator("#review-zoom").selectOption(zoom);
    await page.waitForFunction(
      (z) => window.__CHARACTER_REVIEW__!.zoom === +z,
      zoom,
    );
    const canvas = await page
      .locator("canvas")
      .evaluate((c: HTMLCanvasElement) => ({
        cssWidth: c.getBoundingClientRect().width,
        width: c.width,
        cssHeight: c.getBoundingClientRect().height,
        height: c.height,
        sampling: getComputedStyle(c).imageRendering,
      }));
    expect(canvas.sampling).toBe("pixelated");
    expect(canvas.cssWidth).toBe(canvas.width);
    expect(canvas.cssHeight).toBe(canvas.height);
  }
  expect(errors).toEqual([]);
});

test("mobile static concept proof retains separate silhouettes with reduced motion and Canvas fallback", async ({
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
    page.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await page.goto("./character-review.html?renderer=canvas");
    await page.waitForFunction(() => window.__CHARACTER_REVIEW__?.ready);
    const m = await page.evaluate(() => window.__CHARACTER_REVIEW__!);
    expect(m.renderer).toBe("Canvas");
    expect(m.candidates[1].foot.x - m.candidates[0].foot.x).toBeGreaterThan(
      100,
    );
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.locator('[data-view="back"]').tap();
    await page.waitForFunction(() =>
      window.__CHARACTER_REVIEW__!.candidates.every((c) => c.frame === "back"),
    );
    expect(errors).toEqual([]);
  } finally {
    await context.close();
  }
});
