import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
const characterIds = Object.keys(
  JSON.parse(
    readFileSync("assets-src/characters/phase2c/base-bindings.json", "utf8"),
  ),
);
const retiredHairAccessories = new Set([
  "ara-shell-barrette",
  "kr-hair-ornament",
  "kr-fashion-cap",
  "kr-garden-hat",
]);
const seed = async (page: import("@playwright/test").Page, id = "juni") => {
  await page.addInitScript(
    ({ id, retired }) => {
      localStorage.setItem(
        "korean-arena-player-preferences-v1",
        JSON.stringify({ version: 1, characterId: id }),
      );
      localStorage.setItem(
        "korean-arena-appearance-preferences-v2",
        JSON.stringify({
          version: 2,
          selectedCharacterId: id,
          appearances: {
            [id]: {
              schemaVersion: 2,
              characterId: id,
              hairstyleId: null,
              outfitId: null,
              accessoryIds: retired,
            },
          },
          presets: [],
        }),
      );
    },
    { id, retired: [...retiredHairAccessories] },
  );
};
test("all twelve identities ignore deprecated head equipment while native movement and Studio remain available", async ({
  browser,
}) => {
  for (const id of characterIds) {
    const context = await browser.newContext();
    const page = await context.newPage();
    await seed(page, id);
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("?qa&renderer=canvas&entry=transition");
    await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
      timeout: 45000,
    });
    const state = await page.evaluate(() => window.__GATE3__!);
    expect(state.characterId).toBe(id);
    expect(state.appearance.accessoryIds).toEqual([]);
    expect(state.playerSprites).toBe(1);
    await page.keyboard.down("s");
    await page.waitForFunction(() =>
      window.__GATE3__!.frame.startsWith("walk-front"),
    );
    await page.keyboard.down("Shift");
    await page.waitForFunction(() =>
      window.__GATE3__!.frame.startsWith("run-front"),
    );
    await page.keyboard.up("s");
    await page.keyboard.up("Shift");
    await page.waitForFunction(() =>
      window.__GATE3__!.frame.startsWith("idle-front"),
    );
    await page.locator("#settings summary").click();
    await page.locator("#character-open").click();
    await page.locator('[data-category="accessory"]').click();
    for (const id of retiredHairAccessories)
      await expect(page.locator(`[data-cosmetic="${id}"]`)).toHaveCount(0);
    expect(errors).toEqual([]);
    await context.close();
  }
});
test("mobile landscape quest journal supports touch, visible answers and clean control recovery", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 667, height: 375 },
    hasTouch: true,
    isMobile: true,
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  await seed(page);
  await page.goto("?qa&renderer=canvas&npcReview=npc-minseo");
  await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
    timeout: 45000,
  });
  // Explicit quiz-stage fixture, not a claim of completing mobile world objectives.
  await page.evaluate(() =>
    localStorage.setItem(
      "korean-arena-quests-v1",
      JSON.stringify({
        schemaVersion: 1,
        records: {
          "modern-delivery-v1": { status: "challenge", step: 0, attempts: 0 },
        },
        inventory: {},
        coins: 0,
        xp: 0,
        transactions: [],
      }),
    ),
  );
  await page.reload();
  await page.waitForFunction(() => window.__GATE3__?.ready);
  await page.locator("#quest-journal").tap();
  await expect(page.locator("#quest-dialogue")).toBeVisible();
  const card = page.locator('[data-quest="modern-delivery-v1"]');
  await card.locator('[data-answer="0"]').tap();
  await expect(card.locator("[data-question]")).toHaveAttribute(
    "data-question",
    "parcel-2",
  );
  await page.screenshot({
    path: "docs/phase3bc/mobile-landscape-question.png",
  });
  await card.locator('[data-answer="0"]').tap();
  await expect(page.locator("#quest-inventory")).toContainText(
    "Town Coins: 20",
  );
  const box = await page.locator("#quest-dialogue").boundingBox();
  expect(box!.width).toBeLessThanOrEqual(667);
  expect(box!.height).toBeLessThanOrEqual(375);
  await page
    .getByRole("button", { name: "Trở lại thế giới / Từ chối", exact: true })
    .tap();
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  expect((await page.evaluate(() => window.__GATE3__!)).paused).toBe(false);
  await context.close();
});
test("collision-only doorstep corrections do not disable real building barriers", async ({
  page,
}) => {
  await seed(page);
  await page.goto("?qa&renderer=canvas&entry=retail&collisionDebug");
  await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
    timeout: 45000,
  });
  expect(
    await page.evaluate(() => window.__GATE3_TEST__!.walkable(1128, 2597)),
  ).toBe(true);
  expect(
    await page.evaluate(() => window.__GATE3_TEST__!.walkable(1128, 2500)),
  ).toBe(false);
  await page.screenshot({
    path: "docs/phase3bc/collision-runtime-overlay.png",
  });
});
