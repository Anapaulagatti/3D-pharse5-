import { test, expect, type Page } from "@playwright/test";
const ids = ["seondeok", "sejong", "jang", "saimdang", "yi", "yu"].map(
  (id) => "npc-history-" + id,
);
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
});
async function enter(page: Page, id: string) {
  await page.goto(
    `?qa&historyArtReview=1&renderer=canvas&pixelAudit&npcReview=${id}`,
  );
  await page.waitForFunction(
    (id) =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === id),
    id,
  );
}
async function approach(page: Page, id: string) {
  const s = await page.evaluate(
    (id) => ({
      p: window.__GATE3__!,
      n: window.__NPC_WORLD__!.actors.find((a) => a.id === id)!,
    }),
    id,
  );
  const dx = s.n.position[0] - s.p.x,
    dy = s.n.position[1] - s.p.y;
  const key =
    Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
  await page.locator("#stage canvas").click({ position: { x: 320, y: 120 } });
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      (id) => window.__NPC_WORLD__?.target === id,
      id,
      { timeout: 12000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
}
test("production stays20 until facts are verified; an unqualified review URL cannot unlock history", async ({
  page,
}) => {
  await page.goto("?qa&renderer=canvas&npcReview=npc-history-seondeok");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
  );
  const s = await page.evaluate(() => window.__NPC_WORLD__!);
  expect(s.catalogTotal).toBe(20);
  expect(s.historicalArchiveCount).toBe(0);
  expect(s.historicalArtCandidateCount).toBe(0);
  expect(s.records.some((n) => n.id.startsWith("npc-history-"))).toBe(false);
  await expect(page.locator("#history-art-review")).toHaveCount(0);
});
test("six authored historical candidates move and interact through the existing engine with an honest source gate", async ({
  page,
}) => {
  test.setTimeout(240000);
  for (const id of ids) {
    await enter(page, id);
    const before = await page.evaluate(
      (id) => window.__NPC_WORLD__!.actors.find((a) => a.id === id)!.position,
      id,
    );
    await page.waitForFunction(
      ({ id, before }) => {
        const actor = window.__NPC_WORLD__?.actors.find((a) => a.id === id);
        return (
          actor &&
          Math.hypot(
            actor.position[0] - before[0],
            actor.position[1] - before[1],
          ) > 3
        );
      },
      { id, before },
      { timeout: 15000 },
    );
    await approach(page, id);
    await page.keyboard.press("e");
    await expect(page.locator("#npc-dialogue")).toBeVisible();
    await expect(page.locator("#npc-dialogue")).toHaveAttribute(
      "data-npc-id",
      id,
    );
    await page.locator("#npc-dialogue-next").click();
    await expect(page.locator("#npc-dialogue-vi")).toContainText(
      "chưa được kiểm chứng",
    );
    await page.locator("#npc-dialogue-next").click();
    await expect(page.locator("#npc-dialogue-hint")).toContainText("=");
    await page.locator("#npc-dialogue-return").click();
    await page.waitForFunction(
      () => !window.__GATE3__!.paused && !window.__NPC_WORLD__!.dialogue,
    );
    const s = await page.evaluate(() => ({
      world: window.__GATE3__!,
      npcs: window.__NPC_WORLD__!,
    }));
    expect(s.npcs.registered).toBe(14);
    expect(s.npcs.catalogTotal).toBe(26);
    expect(s.npcs.modernVisitorCount).toBe(6);
    expect(s.npcs.historicalArchiveCount).toBe(0);
    expect(s.npcs.historicalArtCandidateCount).toBe(6);
    expect(new Set(s.npcs.records.map((n) => n.id)).size).toBe(26);
    expect(s.npcs.active).toBeLessThanOrEqual(4);
    expect(s.npcs.assets.loaded).toBeLessThanOrEqual(4);
    expect(s.npcs.assets.pending).toBeLessThanOrEqual(2);
    expect(s.npcs.assets.errors).toEqual([]);
    expect(s.world.playerSprites).toBe(1);
  }
});
test("same-zone archive selection despawns the old actor and restores residents without duplicate sprites", async ({
  page,
}) => {
  await enter(page, ids[0]);
  for (let i = 0; i < 8; i++) {
    const id = ids[i % 2];
    await page.locator("#history-art-review").click();
    await page.locator(`[data-history-id="${id}"]`).click();
    await page.waitForFunction((id) => {
      const s = window.__NPC_WORLD__;
      return (
        s?.actors.filter((a) => a.id.startsWith("npc-history-")).length === 1 &&
        s.actors.some((a) => a.id === id)
      );
    }, id);
    const s = await page.evaluate(() => window.__NPC_WORLD__!);
    expect(new Set(s.actors.map((a) => a.id)).size).toBe(s.active);
    expect(s.assets.loaded).toBeLessThanOrEqual(4);
  }
  await page.locator("#history-art-review").click();
  await page.locator("#history-art-return").click();
  await page.waitForFunction(
    () =>
      !window.__NPC_WORLD__!.actors.some((a) =>
        a.id.startsWith("npc-history-"),
      ) && window.__NPC_WORLD__!.actors.some((a) => a.id === "npc-seoyeon"),
  );
  await page.waitForFunction(() => !window.__GATE3__!.paused);
  const before = await page.evaluate(() => window.__GATE3__!.x);
  await page.keyboard.down("d");
  try {
    await page.waitForFunction((x) => window.__GATE3__!.x > x + 3, before);
  } finally {
    await page.keyboard.up("d");
  }
});
test("small landscape supports touch dialogue, readable vocabulary, close and resumed original joystick", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 667, height: 375 },
    hasTouch: true,
    isMobile: true,
  });
  await context.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
  const page = await context.newPage();
  await enter(page, ids[0]);
  await approach(page, ids[0]);
  await page.locator("#npc-interact").tap();
  await page.locator("#npc-dialogue-next").tap();
  await page.locator("#npc-dialogue-next").tap();
  await expect(page.locator("#npc-dialogue-hint")).toBeVisible();
  const box = await page.locator("#npc-dialogue-return").boundingBox();
  expect(box?.height).toBeGreaterThanOrEqual(44);
  const r = (await page.locator("#joystick").boundingBox())!,
    cdp = await context.newCDPSession(page);
  const drag = async () => {
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: r.x + r.width / 2, y: r.y + r.height / 2 }],
    });
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: r.x + r.width - 6, y: r.y + r.height / 2 }],
    });
    await page.waitForTimeout(450);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
  };
  const locked = await page.evaluate(() => [
    window.__GATE3__!.x,
    window.__GATE3__!.y,
  ]);
  await drag();
  expect(
    await page.evaluate(() => [window.__GATE3__!.x, window.__GATE3__!.y]),
  ).toEqual(locked);
  await page.locator("#npc-dialogue-return").tap();
  await page.waitForFunction(() => !window.__GATE3__!.paused);
  const x = await page.evaluate(() => window.__GATE3__!.x);
  await drag();
  expect(await page.evaluate(() => window.__GATE3__!.x)).toBeGreaterThan(x);
  await expect(page.locator("#history-art-review")).toBeVisible();
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
  expect(
    await page.evaluate(() => window.__NPC_WORLD__!.active),
  ).toBeLessThanOrEqual(4);
  await context.close();
});
