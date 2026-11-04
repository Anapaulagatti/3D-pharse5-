import { test, expect } from "@playwright/test";
const seed = async (page: import("@playwright/test").Page, extras?: unknown) =>
  page.addInitScript((v) => {
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    );
    if (v && !sessionStorage.getItem("phase3bd-fixture")) {
      sessionStorage.setItem("phase3bd-fixture", "1");
      localStorage.setItem("korean-arena-quests-v1", JSON.stringify(v));
    }
  }, extras);
test("only canonical world survives legacy query/direct URL/reload; no rejected asset requests", async ({
  page,
}) => {
  await seed(page);
  const old: string[] = [];
  page.on("request", (r) => {
    if (/\/assets\/(v10-city|v9-world)\//.test(r.url())) old.push(r.url());
  });
  for (const path of [
    "?scene=production&qa&renderer=canvas",
    "?scene=recovery-world&qa&renderer=canvas",
    "v10-city-review.html?qa&renderer=canvas",
    "?qa&renderer=canvas",
  ]) {
    const response = await page.goto(path);
    if (response?.status() === 404) continue;
    await page.waitForFunction(
      () =>
        window.__GATE3__?.ready && window.__NPC_WORLD__?.catalogTotal === 26,
      undefined,
      { timeout: 45000 },
    );
    expect(await page.evaluate(() => window.__GATE3__!.scene)).toBe(
      "palace-cleanup-world",
    );
    await page.reload();
    await page.waitForFunction(() => window.__GATE3__?.ready);
    expect(await page.evaluate(() => window.__GATE3__!.scene)).toBe(
      "palace-cleanup-world",
    );
  }
  expect(old).toEqual([]);
});
for (const [entry, x, y] of [
  ["palace-west", 1837, 1090],
  ["jeju-arrival", 3500, 3633],
  ["jeju-landing", 3188, 3999],
] as const)
  test(`versioned QA approach ${entry} starts on real walkable floor and moves without world relocation`, async ({
    page,
  }) => {
    await seed(page);
    await page.goto(`?qa&renderer=canvas&entry=${entry}&collisionDebug`);
    await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
      timeout: 45000,
    });
    const start = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
    }));
    expect(start.x).toBe(x);
    expect(start.y).toBe(y);
    await page.keyboard.down("d");
    await page.keyboard.down("Shift");
    await page.waitForTimeout(250);
    await page.keyboard.up("d");
    await page.keyboard.up("Shift");
    const end = await page.evaluate(() => window.__GATE3__!);
    expect(end.x - start.x).toBeGreaterThan(5);
    expect(end.playerSprites).toBe(1);
    expect(end.zoom).toBe(1);
    expect(end.samplingMode).toBe(1);
    await page.screenshot({ path: `docs/phase3bd/marker-${entry}-native.png` });
  });
test("shop double-click, invalid quantity and reload use one atomic receipt; old quests and learning remain available", async ({
  page,
}) => {
  // Explicit wallet fixture, not a claim of earned/account-synced coins.
  await seed(page, {
    schemaVersion: 1,
    records: {},
    inventory: {},
    coins: 4,
    xp: 0,
    transactions: [],
  });
  await page.goto("?qa&renderer=canvas&npcReview=npc-minseo");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__?.target !== undefined,
  );
  await page.keyboard.down("w");
  try {
    await page.waitForFunction(
      () => window.__NPC_WORLD__?.target === "npc-minseo",
    );
  } finally {
    await page.keyboard.up("w");
  }
  await page.keyboard.press("e");
  await page.locator('[data-npc-shop="npc-minseo"]').click();
  await page.locator('[data-trade="buy"][data-item="seed-radish"]').dblclick();
  await page.waitForTimeout(100);
  const s = await page.evaluate(() => window.__NPC_WORLD__!.quests);
  expect(s.coins).toBe(0);
  expect(s.inventory["seed-radish"]).toBe(1);
  expect(s.economy.stock["seed-radish"]).toBe(49);
  expect(s.transactions).toHaveLength(1);
  await page.waitForTimeout(350);
  await page.locator("#shop-quantity").fill("-1");
  await page.locator('[data-trade="buy"][data-item="seed-scallion"]').click();
  expect(await page.evaluate(() => window.__NPC_WORLD__!.quests)).toEqual(s);
  await page.locator("#quest-close").click();
  await page.reload();
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
  );
  expect(await page.evaluate(() => window.__NPC_WORLD__!.quests)).toEqual(s);
});
test("mobile landscape reaches an actual farm row by joystick and plants/waters without overlay leakage", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 667, height: 375 },
    hasTouch: true,
    isMobile: true,
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  // Explicit seed fixture to isolate mobile input; desktop full quest film proves earned acquisition.
  await seed(page, {
    schemaVersion: 1,
    records: {},
    inventory: { "seed-radish": 1 },
    coins: 0,
    xp: 0,
    transactions: [],
  });
  await page.goto("?qa&renderer=canvas&entry=farm");
  await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
    timeout: 45000,
  });
  const touch = await context.newCDPSession(page),
    box = await page.locator("#joystick").boundingBox();
  const x = box!.x + box!.width / 2,
    y = box!.y + box!.height / 2;
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [
      { x: x - box!.width * 0.08, y: y - box!.height * 0.4, id: 1 },
    ],
  });
  await page.waitForFunction(
    () => Math.hypot(window.__GATE3__!.x - 470, window.__GATE3__!.y - 669) < 24,
    undefined,
    { timeout: 8000 },
  );
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await page.locator("#quest-world-action").tap();
  await page.waitForFunction(
    () =>
      window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage ===
      "tilled",
  );
  await page.waitForTimeout(550);
  await page.locator("#quest-world-action").tap();
  await page.waitForFunction(
    () =>
      window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage ===
      "planted",
  );
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  await page.waitForTimeout(550);
  await page.locator("#quest-world-action").tap();
  await page.waitForFunction(
    () =>
      window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage ===
      "watered",
  );
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  await page.screenshot({
    path: "docs/phase3bd-in-world/mobile-farm-touch.png",
  });
  await page.waitForFunction(() => window.__GATE3__?.paused === false);
  const afterClose = await page.evaluate(() => window.__GATE3__!.x);
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [{ x: x + box!.width * 0.3, y, id: 1 }],
  });
  await page.waitForFunction(
    (start) => window.__GATE3__!.x > start + 3,
    afterClose,
    { timeout: 8000 },
  );
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await context.close();
});
