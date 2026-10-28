import { test, expect } from "@playwright/test";

test("approved history archive works in the ordinary development world without QA flags and preserves identity/state", async ({
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
    "không phải chân dung hay lời nói được xác thực",
  );
  const expected = [
    ["seondeok", "선덕여왕", "Nữ vương Seondeok"],
    ["sejong", "세종대왕", "Vua Sejong"],
    ["jang", "장영실", "Jang Yeong-sil"],
    ["saimdang", "신사임당", "Shin Saimdang"],
    ["yi", "이순신", "Đô đốc Yi Sun-sin"],
    ["yu", "유관순", "Yu Gwan-sun"],
  ];
  for (const [key, ko, vi] of expected) {
    const button = page.locator(`[data-history-id="npc-history-${key}"]`);
    await expect(button).toContainText(ko);
    await expect(button).toContainText(vi);
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
    "Vua Sejong · 세종대왕",
  );
  await expect(page.locator("#npc-dialogue-role")).toContainText(
    "Tái hiện giáo dục",
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
