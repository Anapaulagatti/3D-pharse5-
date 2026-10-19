import { existsSync } from "node:fs";
import { test, expect, type Page } from "@playwright/test";

test.use({
  launchOptions: {
    executablePath:
      process.env.PIXEL_CHROMIUM_PATH ??
      (existsSync("/usr/bin/chromium") ? "/usr/bin/chromium" : undefined),
    args: ["--no-sandbox"],
  },
});

async function start(page: Page, x: number, y: number) {
  await page.goto("v6-world-review.html?qa&renderer=canvas");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  await page.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  await page.waitForTimeout(120);
}

// Journey destinations are independent of the authored path JSON. These tests
// exercise the unchanged actual player body with real held keyboard input.
async function follow(page: Page, points: number[][]) {
  const dense: number[][] = [];
  let from = await page.evaluate(() => [
    window.__SEOUL__!.x,
    window.__SEOUL__!.y,
  ]);
  for (const to of points) {
    const count = Math.max(
      1,
      Math.ceil(Math.hypot(to[0] - from[0], to[1] - from[1]) / 16),
    );
    for (let i = 1; i <= count; i++)
      dense.push([
        from[0] + ((to[0] - from[0]) * i) / count,
        from[1] + ((to[1] - from[1]) * i) / count,
      ]);
    from = to;
  }
  await page.locator("canvas").focus();
  const held = new Set<string>();
  await page.keyboard.down("Shift");
  try {
    for (const [x, y] of dense) {
      const start = Date.now();
      for (;;) {
        const s = await page.evaluate(() => window.__SEOUL__!);
        if (Math.abs(s.x - x) < 6 && Math.abs(s.y - y) < 6) break;
        if (Date.now() - start > 24000)
          throw Error(
            `Actual traversal blocked toward${x},${y}: ${JSON.stringify(s)}`,
          );
        const keys = new Set<string>();
        if (s.x < x - 4) keys.add("ArrowRight");
        if (s.x > x + 4) keys.add("ArrowLeft");
        if (s.y < y - 4) keys.add("ArrowDown");
        if (s.y > y + 4) keys.add("ArrowUp");
        for (const k of held)
          if (!keys.has(k)) {
            await page.keyboard.up(k);
            held.delete(k);
          }
        for (const k of keys)
          if (!held.has(k)) {
            await page.keyboard.down(k);
            held.add(k);
          }
        await page.waitForTimeout(25);
      }
    }
  } finally {
    for (const k of held) await page.keyboard.up(k);
    await page.keyboard.up("Shift");
  }
}

test("V6 repaired attraction circuit reaches both rides and hall without crossing their masses", async ({
  page,
}) => {
  test.setTimeout(240000);
  await start(page, 3552, 3584);
  await follow(page, [
    [3552, 3424],
    [3552, 3296],
    [3264, 3296],
    [3264, 3152],
    [3328, 3152],
    [3328, 3104],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("관람차");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [3328, 3152],
    [3968, 3152],
    [3968, 3072],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("회전목마");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [3968, 3152],
    [4192, 3152],
    [4192, 3296],
    [3792, 3296],
    [3792, 3584],
    [4016, 3584],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("발견");
});

test("V6 repaired island scenic circuit returns to the village and dock approach", async ({
  page,
}) => {
  test.setTimeout(240000);
  await start(page, 2528, 4560);
  await follow(page, [
    [2528, 4640],
    [2736, 4640],
    [2736, 4896],
    [2464, 4896],
    [2400, 5072],
    [2240, 5088],
    [2048, 5032],
    [1760, 5032],
    [1760, 4896],
    [1830, 4896],
    [1830, 4800],
  ]);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("초가");
  await page.locator("#close-dialog").click();
  await follow(page, [
    [2048, 4800],
    [2048, 4560],
    [2240, 4560],
    [2528, 4560],
    [2528, 4416],
    [2496, 4320],
    [2496, 4280],
  ]);
  expect(await page.evaluate(() => window.__FULL_WORLD__!.district)).toBe(
    "jeju",
  );
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(4288);
});
