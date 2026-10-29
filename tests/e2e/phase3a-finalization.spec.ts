import { test, expect } from "@playwright/test";

test("fictional cultural archive works in the ordinary development world without QA flags and preserves identity/state", async ({
  page,
}) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
  await page.goto("?renderer=canvas&entry=palace");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__?.catalogTotal === 26,
  );
  const initial = await page.evaluate(() => ({
    world: window.__GATE3__!,
    npcs: window.__NPC_WORLD__!,
  }));
  expect(initial.npcs.approvedNPCCount).toBe(26);
  expect(initial.npcs.historicalArchiveCount).toBe(6);
  expect(initial.npcs.verifiedHistoricalClaimCount).toBe(0);
  await page.locator("#history-art-review").click();
  await expect(page.locator("#history-art-dialog")).toContainText(
    "nhân vật hư cấu",
  );
  const expected = [
    ["seondeok", "한연화", "Han Yeonhwa"],
    ["sejong", "백준서", "Baek Junseo"],
    ["jang", "남경우", "Nam Gyeongu"],
    ["saimdang", "윤화연", "Yun Hwayeon"],
    ["yi", "강무영", "Kang Muyeong"],
    ["yu", "서다은", "Seo Daeun"],
  ];
  for (const [key, ko, vi] of expected) {
    const button = page.locator(`[data-history-id="npc-history-${key}"]`);
    await expect(button).toContainText(ko);
    await expect(button).toContainText(vi);
    await expect(button).toHaveAccessibleName(new RegExp(vi + " · " + ko));
  }
  await page.locator('[data-history-id="npc-history-sejong"]').click();
  await page.waitForFunction(() =>
    window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-history-sejong"),
  );
  expect(
    await page.evaluate(() => [window.__GATE3__!.x, window.__GATE3__!.y]),
  ).toEqual([initial.world.x, initial.world.y]);
  await page.keyboard.down("d");
  try {
    await page.waitForFunction(
      () => window.__NPC_WORLD__?.target === "npc-history-sejong",
      undefined,
      { timeout: 12000 },
    );
  } finally {
    await page.keyboard.up("d");
  }
  const approached = await page.evaluate(() => ({
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
    appearance: window.__GATE3__!.appearance,
    visited: window.__GATE3__!.visited,
  }));
  await page.keyboard.press("e");
  await expect(page.locator("#npc-dialogue-name")).toHaveText(
    "Baek Junseo · 백준서",
  );
  await expect(page.locator("#npc-dialogue-role")).toContainText(
    "nhân vật hư cấu",
  );
  await page.locator("#npc-dialogue-next").click();
  await expect(page.locator("#npc-dialogue-vi")).toContainText(
    "đang được kiểm chứng",
  );
  await expect(page.locator("#npc-dialogue-ko")).toContainText("검증 중");
  await page.locator("#npc-dialogue-return").click();
  await page.waitForFunction(() => !window.__GATE3__!.paused);
  expect(
    await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
      appearance: window.__GATE3__!.appearance,
      visited: window.__GATE3__!.visited,
    })),
  ).toEqual(approached);
  expect(
    await page.evaluate(() => window.__NPC_WORLD__!.active),
  ).toBeLessThanOrEqual(4);
});
