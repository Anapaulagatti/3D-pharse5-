import { test, expect, type Page } from "@playwright/test";
import fs from "node:fs";
const routes = JSON.parse(
  fs.readFileSync("assets-src/v9-world/plan/navigation-routes.json", "utf8"),
) as { id: string; points: number[][]; length: number }[];
async function boot(page: Page) {
  await page.goto("v9-world-review.html?qa&renderer=canvas");
  await page.waitForFunction(
    () =>
      window.__SEOUL__?.ready &&
      window.__WORLD_REVIEW__?.candidate === "v9-world",
  );
}
for (const r of routes)
  test(`actual input route: ${r.id}`, async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 1100, height: 820 },
      hasTouch: true,
      reducedMotion: "reduce",
    });
    try {
      const page = await context.newPage();
      const errors: string[] = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await boot(page);
      await page.evaluate(
        ([x, y]) => window.__SEOUL_TEST__!.place(x, y),
        r.points[0],
      );
      const stick = (await page.locator("#joystick").boundingBox())!,
        run = (await page.locator("#run").boundingBox())!;
      const cx = stick.x + stick.width / 2,
        cy = stick.y + stick.height / 2,
        rr = stick.width * 0.4;
      const cdp = await context.newCDPSession(page);
      const runner = {
        x: run.x + run.width / 2,
        y: run.y + run.height / 2,
        id: 2,
      };
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x: cx, y: cy, id: 1 }, runner],
      });
      // Sparse polyline CORNERS are never discarded; only dense cubic samples are thinned.
      const points =
        r.points.length > 50
          ? r.points.filter((_, i) => i % 5 === 0 || i === r.points.length - 1)
          : r.points;
      let lastMove = Date.now(),
        previous = r.points[0];
      for (const [tx, ty] of points.slice(1)) {
        for (;;) {
          const p = await page.evaluate(() => ({
            x: window.__SEOUL__!.x,
            y: window.__SEOUL__!.y,
          }));
          const dx = tx - p.x,
            dy = ty - p.y,
            d = Math.hypot(dx, dy);
          if (d < 8) break;
          if (Math.hypot(p.x - previous[0], p.y - previous[1]) > 5) {
            previous = [p.x, p.y];
            lastMove = Date.now();
          }
          expect(
            Date.now() - lastMove,
            `${r.id} stuck at ${p.x},${p.y} toward ${tx},${ty}`,
          ).toBeLessThan(5000);
          await cdp.send("Input.dispatchTouchEvent", {
            type: "touchMove",
            touchPoints: [
              { x: cx + (dx / d) * rr, y: cy + (dy / d) * rr, id: 1 },
              runner,
            ],
          });
          await page.waitForTimeout(Math.min(160, Math.max(30, d * 6)));
        }
      }
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
      expect(errors).toEqual([]);
    } finally {
      await context.close();
    }
  });
test("new ferry boarding works in both directions through existing public UI", async ({
  page,
}) => {
  await boot(page);
  await page.evaluate(() => window.__SEOUL_TEST__!.place(2560, 4880));
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__SEOUL__!.y > 5000);
  await page.evaluate(() => window.__SEOUL_TEST__!.place(2064, 5408));
  await page.locator("#interact").click();
  await page.locator("#travel-go").click();
  await page.waitForFunction(() => window.__SEOUL__!.y < 5000);
  expect(await page.evaluate(() => window.__SEOUL__!.transitions)).toBe(2);
});
