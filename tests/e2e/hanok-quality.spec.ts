import { test, expect } from "@playwright/test";
for (const id of ["juni", "haneul"])
  test(`western hanok corridor ${id}: real north/south and fixed native camera`, async ({
    page,
  }) => {
    await page.addInitScript(
      (id) =>
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        ),
      id,
    );
    await page.goto(
      "?qa&native&entry=west-house-local&renderer=canvas&pixelAudit",
    );
    await page.waitForFunction(() => window.__GATE3__?.ready, undefined, {
      timeout: 45000,
    });
    const camera = await page.evaluate(() => window.__GATE3__!.camera.center);
    await page.keyboard.down("d");
    try {
      await page.waitForFunction(() => window.__GATE3__!.x > 532);
    } finally {
      await page.keyboard.up("d");
    }
    await page.keyboard.down("w");
    try {
      await page.waitForFunction(() => window.__GATE3__!.y < 1080, undefined, {
        timeout: 10000,
      });
    } finally {
      await page.keyboard.up("w");
    }
    await page.keyboard.down("Shift");
    await page.keyboard.down("s");
    try {
      await page.waitForFunction(() => window.__GATE3__!.y > 1385, undefined, {
        timeout: 10000,
      });
    } finally {
      await page.keyboard.up("s");
      await page.keyboard.up("Shift");
    }
    const end = await page.evaluate(() => window.__GATE3__!);
    expect(end.y).toBeGreaterThan(1385);
    expect(end.camera.center).toEqual(camera);
    expect(end.playerSprites).toBe(1);
    expect(end.samplingMode).toBe(1);
    expect(
      await page.evaluate(() =>
        [
          [534, 1200],
          [600, 1200],
          [640, 1200],
        ].map(([x, y]) => window.__GATE3_TEST__!.walkable(x, y)),
      ),
    ).toEqual([true, false, false]);
  });
