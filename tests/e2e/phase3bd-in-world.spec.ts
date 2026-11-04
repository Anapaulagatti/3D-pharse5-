import { test, expect } from "@playwright/test";
test("inventory/journal cannot perform remote actions; plot pointer respects native rectangle and range", async ({
  page,
}) => {
  await page.addInitScript(() => {
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    );
    localStorage.setItem(
      "korean-arena-quests-v1",
      JSON.stringify({
        schemaVersion: 1,
        records: {},
        inventory: { "seed-radish": 2 },
        coins: 0,
        xp: 0,
        transactions: [],
      }),
    );
  });
  await page.goto("?qa&renderer=canvas&entry=farm");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
    undefined,
    { timeout: 45000 },
  );
  const before = await page.evaluate(() => window.__NPC_WORLD__!.quests);
  for (const id of ["quest-inventory", "quest-journal"]) {
    await page.locator("#" + id).click();
    await expect(page.locator("#quest-dialogue")).toBeVisible();
    await expect(
      page.locator("[data-answer],[data-trade],[data-farm-action]"),
    ).toHaveCount(0);
    await page.locator("#quest-close").click();
  }
  expect(await page.evaluate(() => window.__NPC_WORLD__!.quests)).toEqual(
    before,
  );
  const far = await page.evaluate(() => ({
    x: 470 - window.__GATE3__!.camera.renderedWorldView[0],
    y: 610 - window.__GATE3__!.camera.renderedWorldView[1],
  }));
  await page.locator("canvas").first().click({ position: far });
  expect(await page.evaluate(() => window.__NPC_WORLD__!.quests)).toEqual(
    before,
  );
  await page.keyboard.down("a");
  try {
    await page.waitForFunction(() => window.__GATE3__!.x < 480);
  } finally {
    await page.keyboard.up("a");
  }
  await page.keyboard.down("w");
  try {
    await page.waitForFunction(() => window.__GATE3__!.y < 680);
  } finally {
    await page.keyboard.up("w");
  }
  const near = await page.evaluate(() => ({
    x: 470 - window.__GATE3__!.camera.renderedWorldView[0],
    y: 610 - window.__GATE3__!.camera.renderedWorldView[1],
  }));
  await page.locator("canvas").first().click({ position: near });
  await page.waitForFunction(
    () =>
      window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage ===
      "tilled",
  );
  expect(
    (await page.evaluate(() => window.__NPC_WORLD__!.quests)).inventory[
      "seed-radish"
    ],
  ).toBe(2);
  await page.waitForTimeout(550);
  await page.locator("canvas").first().click({ position: near });
  await page.waitForFunction(
    () =>
      window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage ===
      "planted",
  );
  expect(
    (await page.evaluate(() => window.__NPC_WORLD__!.quests)).inventory[
      "seed-radish"
    ],
  ).toBe(1);
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});
test("ordinary visitor window retains a nearby physical shopkeeper and parcel giver", async ({
  page,
}) => {
  await page.addInitScript(() => {
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    );
    localStorage.setItem(
      "korean-arena-npc-life-v1",
      JSON.stringify({ version: 1, day: 0, minute: 540, seed: 20261029 }),
    );
  });
  await page.goto("?renderer=canvas&entry=retail");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
    undefined,
    { timeout: 45000 },
  );
  await page.keyboard.down("s");
  try {
    await page.waitForFunction(() => window.__GATE3__!.y > 2640);
  } finally {
    await page.keyboard.up("s");
  }
  await page.keyboard.down("a");
  await page.keyboard.down("Shift");
  try {
    await page.waitForFunction(() => window.__GATE3__!.x < 680);
  } finally {
    await page.keyboard.up("a");
    await page.keyboard.up("Shift");
  }
  await page.waitForFunction(() =>
    window.__NPC_WORLD__!.actors.some((a) => a.id === "npc-minseo"),
  );
  expect(
    await page.evaluate(() => window.__NPC_WORLD__!.active),
  ).toBeLessThanOrEqual(4);
  expect(
    await page.evaluate(() =>
      window.__NPC_WORLD__!.actors.some((a) => a.id === "npc-modern-daon"),
    ),
  ).toBe(false);
  await page.keyboard.press("e");
  await page.locator('[data-npc-shop="npc-minseo"]').click();
  await expect(page.locator("#town-shop")).toBeVisible();
  await expect(
    page.locator('[data-trade="buy"][data-item="seed-radish"]'),
  ).toBeVisible();
  await page.locator("#quest-close").click();
  await expect
    .poll(() => page.evaluate(() => window.__GATE3__!.paused))
    .toBe(false);
});
