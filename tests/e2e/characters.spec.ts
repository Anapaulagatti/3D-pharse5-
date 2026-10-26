import { test, expect, type Page } from "@playwright/test";
const key = "korean-arena-player-preferences-v1";
async function ready(page: Page) {
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
}
async function chooseJuni(page: Page) {
  await page.locator('[data-character="juni"]').click();
  await page.locator("#character-confirm").click();
  await expect(page.locator("#character-selection")).not.toBeVisible();
  await ready(page);
}
test("production starts in frozen world with six-character selection", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("");
  await expect(page.locator("#character-selection")).toBeVisible();
  await expect(page.locator("[data-character]")).toHaveCount(6);
  for (const id of ["haneul", "bomi", "minjun", "ara", "doyun"]) {
    await page.locator(`[data-character="${id}"]`).click();
    await expect(page.locator("#character-confirm")).toBeEnabled();
    await expect(page.locator("#character-art-status")).toContainText(
      "Người bạn nguyên bản",
    );
  }
  await chooseJuni(page);
  expect(await page.evaluate(() => window.__GATE3__)).toMatchObject({
    characterId: "juni",
    scene: "palace-cleanup-world",
    playerSprites: 1,
  });
  expect(
    await page.evaluate((key) => JSON.parse(localStorage.getItem(key)!), key),
  ).toEqual({ version: 1, characterId: "juni" });
  expect(errors).toEqual([]);
});
test("saved Juni restores and settings round-trip preserves location, emotes, progress and body ownership", async ({
  page,
}) => {
  await page.addInitScript(
    ({ key }) => {
      localStorage.setItem(
        key,
        JSON.stringify({ version: 1, characterId: "juni" }),
      );
      localStorage.setItem("phase1-progress-sentinel", "KEEP");
    },
    { key },
  );
  await page.goto("");
  await ready(page);
  await expect(page.locator("#character-selection")).not.toBeVisible();
  const initial = await page.evaluate(() => ({
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
  }));
  await page.keyboard.down("s");
  await page.waitForFunction((y) => window.__GATE3__!.y > y + 12, initial.y);
  await page.keyboard.up("s");
  for (let i = 0; i < 3; i++) {
    await page.locator("#settings summary").click();
    await page.locator("#character-open").click();
    await expect(page.locator("#character-selection")).toBeVisible();
    const frozen = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
    }));
    await page.keyboard.down("d");
    await page.waitForTimeout(150);
    await page.keyboard.up("d");
    expect(
      await page.evaluate(() => ({
        x: window.__GATE3__!.x,
        y: window.__GATE3__!.y,
      })),
    ).toEqual(frozen);
    await chooseJuni(page);
    expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
    await page.locator("#settings summary").click();
  }
  await page.keyboard.press("c");
  await page.waitForFunction(() =>
    window.__GATE3__!.frame.startsWith("celebrate-front"),
  );
  await page.waitForFunction(() => window.__GATE3__!.frame.startsWith("idle-"));
  expect(
    await page.evaluate(() => localStorage.getItem("phase1-progress-sentinel")),
  ).toBe("KEEP");
  await page.reload();
  await ready(page);
  await expect(page.locator("#character-selection")).not.toBeVisible();
});
test("corrupt, unknown and unavailable storage recover to Juni without crashing", async ({
  browser,
}) => {
  for (const value of [
    "{",
    '{"version":1,"characterId":"removed"}',
    '{"version":1,"characterId":"unfinished"}',
    null,
  ]) {
    const ctx = await browser.newContext();
    await ctx.addInitScript(
      ({ key, value }) => {
        if (value === null)
          Object.defineProperty(window, "localStorage", {
            get() {
              throw new DOMException("Denied", "SecurityError");
            },
          });
        else localStorage.setItem(key, value);
      },
      { key, value },
    );
    const p = await ctx.newPage();
    await p.goto("");
    await expect(p.locator("#character-selection")).toBeVisible();
    await chooseJuni(p);
    expect(await p.evaluate(() => window.__GATE3__!.characterId)).toBe("juni");
    await ctx.close();
  }
});
test("mobile landscape preview fits; modal isolates joystick and original touch movement returns", async ({
  browser,
}) => {
  const ctx = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const p = await ctx.newPage();
  await p.goto("");
  await expect(p.locator("#character-selection")).toBeVisible();
  await p.locator('[data-action="walk"]').tap();
  const layout = await p.evaluate(() => {
    const d = document.querySelector("#character-selection")!,
      c = document.querySelector("#character-preview")!.getBoundingClientRect(),
      r = d.getBoundingClientRect();
    return {
      overflow: d.scrollWidth > d.clientWidth + 1,
      contained:
        c.left >= r.left &&
        c.right <= r.right &&
        c.top >= r.top &&
        c.bottom <= r.bottom,
    };
  });
  expect(layout).toEqual({ overflow: false, contained: true });
  await chooseJuni(p);
  const state = await p.evaluate(() => window.__GATE3__!);
  const s = await ctx.newCDPSession(p),
    b = (await p.locator("#joystick").boundingBox())!,
    x = b.x + b.width / 2,
    y = b.y + b.height / 2;
  await s.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  await s.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [{ x: x + b.width * 0.3, y, id: 1 }],
  });
  await p.waitForFunction((x) => window.__GATE3__!.x > x + 8, state.x);
  await s.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  expect(await p.evaluate(() => window.__GATE3__!.camera.pointers)).toBe(0);
  await ctx.close();
});
test("Canvas native Juni and Scenic Tour survive the production bootstrap", async ({
  page,
}) => {
  await page.addInitScript(
    (key) =>
      localStorage.setItem(
        key,
        JSON.stringify({ version: 1, characterId: "juni" }),
      ),
    key,
  );
  await page.goto("?renderer=canvas&entry=jeju-culture");
  await ready(page);
  expect(await page.evaluate(() => window.__GATE3__!.renderer)).toBe("Canvas");
  const before = await page.evaluate(() => ({
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
  }));
  await page.locator("#scenic").click();
  await page.locator("#start-tour").click();
  await page.waitForFunction(() => window.__GATE3__!.camera.mode === "tour");
  await page.locator("#tour-pause").click();
  await page.locator("#return-juni").click();
  await page.waitForFunction(() => window.__GATE3__!.camera.mode === "follow");
  expect(
    await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
    })),
  ).toEqual(before);
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});

for (const id of ["haneul", "bomi", "minjun", "ara", "doyun"]) {
  test(`native pack ${id} plays, switches and restores without position/state loss`, async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("?entry=station-all&pixelAudit");
    await page.locator(`[data-character="${id}"]`).click();
    await page.locator('[data-action="walk"]').click();
    await page.locator("#character-confirm").click();
    await ready(page);
    await page.waitForFunction(
      (id) => window.__GATE3__!.characterId === id,
      id,
    );
    expect(await page.evaluate(() => window.__GATE3__!.characterId)).toBe(id);
    await page.keyboard.down("w");
    await page.waitForFunction(() => window.__GATE3__!.y < 2720);
    await page.keyboard.up("w");
    await page.waitForTimeout(250);
    await page.keyboard.press("e");
    await expect(page.locator("#dialog")).toBeVisible();
    await page.locator("#close").click();
    const before = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
      visited: window.__GATE3__!.visited,
    }));
    for (const key of ["a", "d", "w", "s"]) {
      await page.keyboard.down(key);
      await page.waitForTimeout(700);
      await page.keyboard.up(key);
      await page.waitForTimeout(220);
    }
    for (const emote of ["Space", "c"]) {
      await page.keyboard.press(emote);
      await page.waitForFunction(
        (prefix) => window.__GATE3__!.frame.startsWith(prefix),
        emote === "c" ? "celebrate-front" : "wave-front",
      );
      await page.waitForFunction(() =>
        window.__GATE3__!.frame.startsWith("idle-"),
      );
    }
    const atSwitch = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
      visited: window.__GATE3__!.visited,
    }));
    await page.locator("#settings summary").click();
    await page.locator("#character-open").click();
    await chooseJuni(page);
    expect(
      await page.evaluate(() => ({
        x: window.__GATE3__!.x,
        y: window.__GATE3__!.y,
        visited: window.__GATE3__!.visited,
      })),
    ).toEqual(atSwitch);
    await page.locator("#character-open").click();
    await page.locator(`[data-character="${id}"]`).click();
    await page.locator("#character-confirm").click();
    await expect(page.locator("#character-selection")).not.toBeVisible();
    expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
    await page.reload();
    await ready(page);
    await page.waitForFunction(
      (id) => window.__GATE3__!.characterId === id,
      id,
    );
    expect(await page.evaluate(() => window.__GATE3__!.characterId)).toBe(id);
    expect(
      await page.evaluate(() => ({
        x: window.__GATE3__!.x,
        y: window.__GATE3__!.y,
        visited: window.__GATE3__!.visited,
      })),
    ).toEqual(atSwitch);
    expect(before.visited.length).toBeGreaterThan(0);
    expect(errors).toEqual([]);
  });
}
