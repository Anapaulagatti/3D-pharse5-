import { test, expect } from "@playwright/test";
const visitors = [
  "modern-daon",
  "modern-miram",
  "modern-geonu",
  "modern-seorin",
  "modern-haru",
  "modern-yeori",
];
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
});
test("all six original cultural visitors use actual NPC movement, dialogue and bounded native textures", async ({
  page,
}) => {
  test.setTimeout(240000);
  for (const short of visitors) {
    const id = "npc-" + short;
    await page.goto(`?qa&renderer=canvas&pixelAudit&npcReview=${id}`);
    await page.waitForFunction(
      (id) =>
        window.__GATE3__?.ready &&
        window.__NPC_WORLD__?.actors.some((a) => a.id === id),
      id,
    );
    const start = await page.evaluate(
      (id) => ({
        w: window.__GATE3__!,
        npc: window.__NPC_WORLD__!.actors.find((a) => a.id === id)!,
        n: window.__NPC_WORLD__!,
      }),
      id,
    );
    expect(start.n.catalogTotal).toBe(26);
    expect(start.n.residentCount).toBe(14);
    expect(start.n.modernVisitorCount).toBe(6);
    expect(start.n.historicalArchiveCount).toBe(6);
    expect(new Set(start.n.records.map((n) => n.id)).size).toBe(26);
    expect(start.npc.nativeScale).toEqual([1, 1]);
    expect(start.npc.sampling).toBe(1);
    await page.waitForFunction(
      ({ id, pos }) => {
        const n = window.__NPC_WORLD__?.actors.find((a) => a.id === id);
        return (
          n && Math.hypot(n.position[0] - pos[0], n.position[1] - pos[1]) > 3
        );
      },
      { id, pos: start.npc.position },
      { timeout: 15000 },
    );
    const approach = await page.evaluate(
      (id) => ({
        p: window.__GATE3__!,
        n: window.__NPC_WORLD__!.actors.find((a) => a.id === id)!,
      }),
      id,
    );
    const dx = approach.n.position[0] - approach.p.x,
      dy = approach.n.position[1] - approach.p.y,
      key =
        Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
    await page.locator("#stage canvas").click({ position: { x: 480, y: 300 } });
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
    const position = await page.evaluate(() => [
      window.__GATE3__!.x,
      window.__GATE3__!.y,
    ]);
    await page.keyboard.press("e");
    await expect(page.locator("#npc-dialogue")).toBeVisible();
    await expect(page.locator("[data-npc-choice]")).toHaveCount(4);
    await page.locator('[data-npc-choice="words"]').click();
    await expect(page.locator("#npc-dialogue-hint")).toContainText("=");
    await page.locator("#npc-dialogue-next").click();
    await expect(page.locator("#npc-dialogue-ko")).toContainText("천천히");
    await page.keyboard.press("Escape");
    await expect(page.locator("#npc-dialogue")).not.toBeVisible();
    await page.waitForFunction(() => !window.__GATE3__!.paused);
    const end = await page.evaluate(() => ({
      p: window.__GATE3__!,
      n: window.__NPC_WORLD__!,
    }));
    expect([end.p.x, end.p.y]).toEqual(position);
    expect(end.p.playerSprites).toBe(1);
    expect(end.p.paused).toBe(false);
    expect(end.n.active).toBeLessThanOrEqual(4);
    expect(end.n.assets.loaded).toBeLessThanOrEqual(4);
    expect(end.n.assets.pending).toBeLessThanOrEqual(2);
    expect(end.n.assets.errors).toEqual([]);
  }
});
test("normal population activates an original visitor and never preloads all20textures", async ({
  page,
}) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-npc-visits-v1",
      JSON.stringify({ version: 1, epochMs: Date.now() - 95000 }),
    ),
  );
  // Existing canonical review entry positions Juni; no NPC selection or actor override.
  await page.goto("?qa&renderer=canvas&entry=modern");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__,
  );
  await page.waitForFunction(() =>
    window.__NPC_WORLD__?.actors.some((a) => a.id === "npc-modern-daon"),
  );
  const state = await page.evaluate(() => window.__NPC_WORLD__!);
  expect(state.catalogTotal).toBe(26);
  expect(state.active).toBeLessThanOrEqual(4);
  expect(state.assets.loaded).toBeLessThanOrEqual(4);
  expect(state.records).toHaveLength(26);
  expect(state.actors.some((a) => a.id === "npc-minseo")).toBe(false);
  // Actual region re-entry/memory coverage is also recorded by the canonical traversal harness.
});
test("new learning vocabulary remains readable and touch-isolated in mobile landscape", async ({
  browser,
}) => {
  test.setTimeout(120000);
  for (const [width, height] of [
    [667, 375],
    [844, 390],
  ]) {
    const c = await browser.newContext({
      viewport: { width, height },
      hasTouch: true,
      isMobile: true,
      deviceScaleFactor: 1,
    });
    await c.addInitScript(() =>
      localStorage.setItem(
        "korean-arena-player-preferences-v1",
        JSON.stringify({ version: 1, characterId: "juni" }),
      ),
    );
    const p = await c.newPage(),
      id = "npc-modern-daon";
    await p.goto(`?qa&renderer=canvas&npcReview=${id}`);
    await p.waitForFunction(
      (id) =>
        window.__GATE3__?.ready &&
        window.__NPC_WORLD__?.actors.some((a) => a.id === id),
      id,
    );
    const s = await p.evaluate(
      (id) => ({
        p: window.__GATE3__!,
        n: window.__NPC_WORLD__!.actors.find((a) => a.id === id)!,
      }),
      id,
    );
    const dx = s.n.position[0] - s.p.x,
      dy = s.n.position[1] - s.p.y,
      key =
        Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
    await p.keyboard.down(key);
    try {
      await p.waitForFunction((id) => window.__NPC_WORLD__?.target === id, id);
    } finally {
      await p.keyboard.up(key);
    }
    await p.locator("#npc-interact").tap();
    await p.locator('[data-npc-choice="words"]').tap();
    await expect(p.locator("#npc-dialogue-hint")).toBeVisible();
    await expect(p.locator("#npc-dialogue-hint")).toContainText(
      "노래 = bài hát",
    );
    const r = (await p.locator("#joystick").boundingBox())!,
      cdp = await c.newCDPSession(p);
    const drag = async () => {
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x: r.x + r.width / 2, y: r.y + r.height / 2 }],
      });
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchMove",
        touchPoints: [{ x: r.x + r.width - 6, y: r.y + r.height / 2 }],
      });
      await p.waitForTimeout(450);
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
    };
    const locked = await p.evaluate(() => [
      window.__GATE3__!.x,
      window.__GATE3__!.y,
    ]);
    await drag();
    expect(
      await p.evaluate(() => [window.__GATE3__!.x, window.__GATE3__!.y]),
    ).toEqual(locked);
    await p.locator("#npc-dialogue-return").scrollIntoViewIfNeeded();
    await p.locator("#npc-dialogue-return").tap();
    await p.waitForFunction(() => !window.__GATE3__!.paused);
    const before = await p.evaluate(() => window.__GATE3__!.x);
    await drag();
    expect(await p.evaluate(() => window.__GATE3__!.x)).toBeGreaterThan(before);
    expect(await p.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
    await c.close();
  }
});
