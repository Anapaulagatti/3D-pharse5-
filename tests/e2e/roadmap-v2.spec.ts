import { test, expect, type Page } from "@playwright/test";
async function choose(page: Page) {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
}
async function move(
  page: Page,
  kind: "world" | "room",
  target: readonly [number, number],
) {
  let held: string[] = [];
  try {
    for (let i = 0; i < 450; i++) {
      const s = await page.evaluate(
        (k) => (k === "room" ? window.__INTERIOR__ : window.__GATE3__),
        kind,
      );
      if (!s) throw Error("Absent " + kind);
      const dx = target[0] - s.x,
        dy = target[1] - s.y;
      if (Math.hypot(dx, dy) < 5) return;
      const keys = ["Shift"];
      if (Math.abs(dx) > 2) keys.push(dx > 0 ? "d" : "a");
      if (Math.abs(dy) > 2) keys.push(dy > 0 ? "s" : "w");
      for (const k of held.filter((k) => !keys.includes(k)))
        await page.keyboard.up(k);
      for (const k of keys.filter((k) => !held.includes(k)))
        await page.keyboard.down(k);
      held = keys;
      await page.waitForTimeout(25);
    }
    throw Error("Physical movement blocked " + JSON.stringify(target));
  } finally {
    for (const k of held) await page.keyboard.up(k);
  }
}
for (const [id, x] of [
  ["seed-shop", 717],
  ["bookshop", 1128],
  ["workshop", 1418],
] as const)
  test(`V2 ${id}: same native player, repeated enter/exit, restore world and no orphan`, async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await choose(page);
    await page.goto(
      `?qa&entry=${id === "seed-shop" ? "cafe-roof" : id === "bookshop" ? "retail" : "learning-roof"}&renderer=canvas`,
    );
    await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
      timeout: 45000,
    });
    await move(page, "world", [x, 2618]);
    await page.waitForTimeout(1800);
    const origin = await page.evaluate(() => [
      window.__GATE3__!.x,
      window.__GATE3__!.y,
    ]);
    for (let cycle = 0; cycle < 2; cycle++) {
      await page.locator("#interior-door").click();
      await page.waitForFunction((id) => window.__INTERIOR__?.id === id, id, {
        timeout: 15000,
      });
      await move(page, "room", [320, 320]);
      if (cycle === 0) {
        await page.waitForTimeout(650);
        await page.reload();
        await page.waitForFunction((id) => window.__INTERIOR__?.id === id, id, {
          timeout: 45000,
        });
        expect(await page.evaluate(() => window.__INTERIOR__!.y)).toBeLessThan(
          326,
        );
      }
      const s = await page.evaluate(() => window.__INTERIOR__!);
      expect(s.playerIdentity).toBe("juni");
      expect(s.scale).toBe(1);
      expect(s.sampling).toBe(1);
      expect(s.footOnFloor).toBe(true);
      await move(page, "room", [320, 438]);
      await page.keyboard.press("e");
      await page.waitForFunction(
        () => !window.__INTERIOR__ && window.__GATE3__?.ready,
      );
      expect(
        await page.evaluate(() => [window.__GATE3__!.x, window.__GATE3__!.y]),
      ).toEqual(origin);
      expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(
        1,
      );
    }
    expect(errors).toEqual([]);
  });
test("V2 mobile landscape: native icon HUD, safe focus and room touch action", async ({
  page,
}) => {
  await page.setViewportSize({ width: 667, height: 375 });
  await choose(page);
  await page.goto("?qa&entry=cafe-roof&renderer=canvas");
  await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
    timeout: 45000,
  });
  await expect(page.locator("#quest-inventory img")).toHaveAttribute(
    "src",
    /roadmap-v2\/bag.png$/,
  );
  await page.locator("#interior-door").click();
  await page.waitForFunction(() => window.__INTERIOR__?.id === "seed-shop");
  await expect(page.locator("#interior-action")).toBeVisible();
  const before = await page.evaluate(() => window.__INTERIOR__!.x),
    box = (await page.locator("#joystick").boundingBox())!;
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [
      { id: 1, x: box.x + box.width * 0.82, y: box.y + box.height * 0.5 },
    ],
  });
  await page.waitForTimeout(450);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  expect(await page.evaluate(() => window.__INTERIOR__!.x)).toBeGreaterThan(
    before + 4,
  );

  await page.locator("#interior-action").click();
  await page.waitForFunction(() => !window.__INTERIOR__);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});
