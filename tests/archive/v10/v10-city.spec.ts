import { test, expect, type Page } from "@playwright/test";
import fs from "node:fs";
const plan = JSON.parse(
  fs.readFileSync("assets-src/v10-city/plan/city.json", "utf8"),
);
async function boot(p: Page, renderer = "canvas") {
  const errors: string[] = [],
    legacy: string[] = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  p.on("request", (r) => {
    if (/\/assets\/world\/|\/v9-world\//.test(r.url())) legacy.push(r.url());
  });
  await p.goto(`v10-city-review.html?qa&renderer=${renderer}`);
  await p.waitForFunction(
    () =>
      window.__SEOUL__?.ready &&
      window.__WORLD_REVIEW__?.candidate === "v10-graybox",
  );
  return { errors, legacy };
}
async function place(p: Page, x: number, y: number) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  const n = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__!.frameCount > n + 4,
    n,
  );
}
async function axis(p: Page, axis: "x" | "y", target: number) {
  // The approved controller decelerates after keyup. Starting the next axis
  // before it settles introduced ~8px perpendicular drift and flaky corners.
  // Wait for real velocity; no placement, speed or collision overrides.
  const settle = () =>
    p.waitForFunction(() =>
      window.__FULL_WORLD__!.velocity.every((v) => Math.abs(v) < 0.1),
    );
  await settle();
  const position = () => p.evaluate((axis) => window.__SEOUL__![axis], axis);
  const move = async (start: number, stopBefore: number) => {
    const sign = Math.sign(target - start);
    const key =
      axis === "x"
        ? sign > 0
          ? "ArrowRight"
          : "ArrowLeft"
        : sign > 0
          ? "ArrowDown"
          : "ArrowUp";
    await p.keyboard.down(key);
    try {
      await p.waitForFunction(
        ({ axis, target, sign, stopBefore }) =>
          (target - window.__SEOUL__![axis]) * sign <= stopBefore,
        { axis, target, sign, stopBefore },
        { timeout: Math.max(8000, Math.abs(target - start) * 22) },
      );
    } finally {
      await p.keyboard.up(key);
    }
    await settle();
  };
  let current = await position();
  if (Math.abs(current - target) < 4) return;
  if (Math.abs(current - target) > 24) await move(current, 12);
  // Use original walking input for the braking-distance approach, then restore
  // the caller's run key. The waypoint/obstacle/final-distance gates are retained.
  await p.keyboard.up("Shift");
  try {
    for (let attempt = 0; attempt < 5; attempt++) {
      current = await position();
      if (Math.abs(current - target) < 4) break;
      await move(current, 3);
    }
    expect(Math.abs((await position()) - target)).toBeLessThan(4);
  } finally {
    await p.keyboard.down("Shift");
  }
}
// Each route uses one QA start, real running keys and native walk-speed final approaches.
for (const [name, points] of [
  [
    "historic gateway to high street",
    [
      [2176, 2256],
      [2176, 2400],
      [2016, 2400],
      [2016, 2960],
    ],
  ],
  [
    "entire high street and station forecourt",
    [
      [1456, 2960],
      [3776, 2960],
      [3776, 2832],
    ],
  ],
  [
    "urban block circuit",
    [
      [1456, 2960],
      [1456, 3504],
      [2768, 3504],
      [2768, 2400],
      [2016, 2400],
    ],
  ],
  [
    "west scenic loop and tower approach",
    [
      [1216, 2960],
      [1216, 2672],
      [560, 2672],
      [320, 2784],
      [352, 3104],
      [656, 3328],
      [1024, 3248],
      [1216, 2960],
      [896, 3040],
      [736, 3040],
    ],
  ],
  [
    "leisure campus and ride approaches",
    [
      [1280, 3904],
      [1280, 3744],
      [400, 3744],
      [400, 4224],
      [400, 4352],
      [960, 4352],
      [1232, 4176],
      [1232, 4080],
      [952, 4080],
      [616, 4072],
    ],
  ],
  [
    "coastal neighborhood to boarding pier",
    [
      [2768, 3504],
      [3776, 3504],
      [3776, 4224],
      [3968, 4384],
      [3968, 4560],
    ],
  ],
  [
    "Jeju olle and village circuit",
    [
      [3296, 5216],
      [3568, 5216],
      [3552, 5568],
      [3288, 5568],
      [3216, 5664],
      [2752, 5648],
      [2624, 5648],
      [2624, 5456],
      [2464, 5456],
      [2576, 5360],
      [2800, 5384],
    ],
  ],
] as [string, number[][]][]) {
  test(`V10 real input route: ${name}`, async ({ page }) => {
    const observed = await boot(page);
    await place(page, points[0][0], points[0][1]);
    await page.locator("canvas").focus();
    await page.keyboard.down("Shift");
    try {
      for (const [x, y] of points.slice(1)) {
        await axis(page, "x", x);
        await axis(page, "y", y);
      }
    } finally {
      await page.keyboard.up("Shift");
    }
    const last = points.at(-1)!;
    const actual = await page.evaluate(() => [
      window.__SEOUL__!.x,
      window.__SEOUL__!.y,
    ]);
    expect(Math.hypot(actual[0] - last[0], actual[1] - last[1])).toBeLessThan(
      16,
    );
    expect(observed).toEqual({ errors: [], legacy: [] });
  });
}
test("all 23 entrances are walkable and identify their intended venue", async ({
  page,
}) => {
  const observed = await boot(page);
  for (const lot of plan.plots) {
    await place(page, lot.door[0], lot.door[1]);
    await page.locator("#interact").click();
    await expect(page.locator("#dialog-copy")).toContainText(lot.label);
    await page.locator("#close-dialog").click();
  }
  expect(observed).toEqual({ errors: [], legacy: [] });
});
test("two ferry journeys land outside triggers and allow subsequent walking", async ({
  page,
}) => {
  const observed = await boot(page);
  for (const [point, label, target] of [
    [
      plan.travel.mainlandTrigger,
      "Lên phà đến Jeju",
      plan.travel.islandArrival,
    ],
    [
      plan.travel.islandTrigger,
      "Lên phà về bờ biển",
      plan.travel.mainlandArrival,
    ],
  ] as [number[], string, number[]][]) {
    await place(page, point[0], point[1]);
    await page.locator("#interact").click();
    await page.getByRole("button", { name: label }).click();
    await page.waitForFunction(
      ([x, y]) =>
        Math.abs(window.__SEOUL__!.x - x) < 3 &&
        Math.abs(window.__SEOUL__!.y - y) < 3,
      target,
    );
    await page.locator("canvas").focus();
    await page.keyboard.down("ArrowDown");
    try {
      await page.waitForFunction(
        (y) => window.__SEOUL__!.y > y + 12,
        target[1],
      );
    } finally {
      await page.keyboard.up("ArrowDown");
    }
  }
  expect(observed).toEqual({ errors: [], legacy: [] });
});
test("station tracks and building masses block input; marked crossing is clear", async ({
  page,
}) => {
  await boot(page);
  await page.locator("canvas").focus();
  for (const [x, y, limit, key] of [
    [3600, 2496, 2472, "ArrowUp"],
    [2256, 2824, 2752, "ArrowUp"],
  ] as [number, number, number, string][]) {
    await place(page, x, y);
    await page.keyboard.down(key);
    await page.waitForTimeout(1800);
    await page.keyboard.up(key);
    expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThan(
      limit,
    );
  }
  await place(page, 3456, 2504);
  await axis(page, "y", 2376);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(2424);
});
test("forced WebGL renders V10 without fetching rejected assets", async ({
  page,
}) => {
  const observed = await boot(page, "webgl");
  await place(page, 2352, 2960);
  expect(
    await page.evaluate(() => window.__PIXEL_METRICS__!.renderer),
  ).toContain("WebGL");
  expect(observed).toEqual({ errors: [], legacy: [] });
});
