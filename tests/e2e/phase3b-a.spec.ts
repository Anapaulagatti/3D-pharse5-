import { test, expect } from "@playwright/test";
const seed = async (page: import("@playwright/test").Page) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
};
test("daily intent interrupts/resumes dialogue and refresh preserves time and bounded native ownership", async ({
  page,
}) => {
  await seed(page);
  await page.goto("?qa&renderer=canvas&npcReview=npc-minseo");
  await page.waitForFunction(
    () =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-minseo"),
  );
  await page.evaluate(() => window.__NPC_LIFE_QA__!.setTime(540, 1));
  await page.waitForTimeout(100);
  await expect(page.locator("#npc-life-time")).toContainText("09:00");
  const [dx, dy] = await page.evaluate(() => {
    const n = window.__NPC_WORLD__!.actors.find((a) => a.id === "npc-minseo")!;
    return [
      n.position[0] - window.__GATE3__!.x,
      n.position[1] - window.__GATE3__!.y,
    ];
  });
  const key =
    Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
  await page.locator("#stage canvas").click({ position: { x: 320, y: 180 } });
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      () => window.__NPC_WORLD__?.target === "npc-minseo",
      undefined,
      { timeout: 12000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.keyboard.press("e");
  await expect(page.locator("#npc-dialogue")).toBeVisible();
  const before = await page.evaluate(
    () =>
      window.__NPC_WORLD__!.actors.find((a) => a.id === "npc-minseo")!.position,
  );
  await page.evaluate(() => window.__NPC_LIFE_QA__!.setTime(720, 1));
  await page.waitForTimeout(300);
  expect(
    await page.evaluate(
      () =>
        window.__NPC_WORLD__!.actors.find((a) => a.id === "npc-minseo")!
          .position,
    ),
  ).toEqual(before);
  await page.locator("#npc-dialogue-return").click();
  await page.waitForTimeout(700);
  expect(
    await page.evaluate(
      () =>
        window.__NPC_WORLD__!.actors.find((a) => a.id === "npc-minseo")!
          .activity?.id,
    ),
  ).toContain("midday-break");
  await page.reload();
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
  );
  const s = await page.evaluate(() => window.__NPC_WORLD__!);
  expect(s.clock.minute).toBeGreaterThanOrEqual(720);
  expect(s.clock.minute).toBeLessThan(725);
  expect(s.active).toBeLessThanOrEqual(4);
  expect(s.assets.loaded).toBeLessThanOrEqual(4);
  expect(s.assets.pending).toBeLessThanOrEqual(2);
});
test("archive intentions are local story time, not modern daily work", async ({
  page,
}) => {
  await seed(page);
  await page.goto("?qa&renderer=canvas&npcReview=npc-history-sejong");
  await page.waitForFunction(
    () =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-history-sejong"),
  );
  await page.evaluate(() => window.__NPC_LIFE_QA__!.setTime(60, 60));
  await page.waitForTimeout(200);
  const s = await page.evaluate(() => window.__NPC_WORLD__!);
  expect(
    s.actors.find((a) => a.id === "npc-history-sejong")!.activity?.context,
  ).toBe("archive-story");
  expect(s.actors.some((a) => a.id === "npc-seoyeon")).toBe(false);
  await expect(page.locator("#npc-life-time")).toContainText("giờ riêng");
});
test("browser freeze clamps resume and ordinary query cannot enable developer clock", async ({
  page,
}) => {
  await seed(page);
  await page.goto("?renderer=canvas&entry=modern&npcLifeRate=60");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
  );
  expect(await page.evaluate(() => window.__NPC_LIFE_QA__)).toBeUndefined();
  await expect(page.locator("#settings summary")).toHaveCount(1);
  await page.locator("#settings summary").click();
  await page.locator("#npc-rights-toggle").click();
  await expect(page.locator("#npc-rights-records p")).toHaveCount(26);
  await page.locator("#settings summary").click();

  await expect(page.locator("#npc-life-controls")).toHaveCount(0);
  const before = await page.evaluate(() => window.__NPC_WORLD__!.clock.minute),
    cdp = await page.context().newCDPSession(page);
  await cdp.send("Page.setWebLifecycleState", { state: "frozen" });
  await page.waitForTimeout(1200);
  await cdp.send("Page.setWebLifecycleState", { state: "active" });
  await page.waitForTimeout(300);
  const after = await page.evaluate(() => window.__NPC_WORLD__!);
  expect(after.clock.minute - before).toBeLessThan(2);
  expect(after.active).toBeLessThanOrEqual(4);
  expect(after.assets.loaded).toBeLessThanOrEqual(4);
  await cdp.detach();
});
