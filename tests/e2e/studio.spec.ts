import { test, expect, type Page } from "@playwright/test";
const V1 = "korean-arena-player-preferences-v1",
  V2 = "korean-arena-appearance-preferences-v2";
const ready = (p: Page) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__!.chunks.inflight === 0,
  );
async function boot(
  p: Page,
  id = "juni",
  extra: Record<string, string> = {},
  entry = "",
) {
  await p.addInitScript(
    ({ id, extra, V1 }) => {
      if (!sessionStorage.getItem("phase2a-test-seed")) {
        localStorage.setItem(
          V1,
          JSON.stringify({ version: 1, characterId: id }),
        );
        for (const [k, v] of Object.entries(extra)) localStorage.setItem(k, v);
        sessionStorage.setItem("phase2a-test-seed", "1");
      }
    },
    { id, extra, V1 },
  );
  await p.goto(
    `./?renderer=canvas&pixelAudit${entry ? "&entry=" + entry : ""}`,
  );
  await ready(p);
}
async function open(p: Page) {
  if (await p.locator("#character-selection").isVisible()) return;
  if (!(await p.locator("#character-open").isVisible()))
    await p.locator("#settings summary").click();
  await p.locator("#character-open").click();
  await expect(p.locator("#character-selection")).toBeVisible();
}
const state = (p: Page) =>
  p.evaluate(() => ({
    id: window.__GATE3__!.characterId,
    appearance: window.__GATE3__!.appearance,
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
    visited: window.__GATE3__!.visited,
    players: window.__GATE3__!.playerSprites,
    key: window.__GATE3__!.characterAssets.activeKey,
    sampling: window.__GATE3__!.samplingMode,
  }));
async function item(p: Page, category: string, id: string) {
  await p.locator(`[data-category="${category}"]`).click();
  await p.locator(`[data-cosmetic="${id}"]`).click();
  await expect(p.locator(`[data-cosmetic="${id}"]`)).toHaveAttribute(
    "aria-pressed",
    "true",
  );
}
async function apply(p: Page, enter = false) {
  await p.locator(enter ? "#character-confirm" : "#appearance-save").click();
  if (enter) await expect(p.locator("#character-selection")).not.toBeVisible();
  else await expect(p.locator("#character-feedback")).toContainText("Đã lưu");
  await ready(p);
}
const araLook = {
  schemaVersion: 2,
  characterId: "ara",
  hairstyleId: "ara-braided-bun",
  outfitId: "ara-sunlit-linen",
  accessoryIds: ["ara-shell-barrette"],
};
test("Studio previews and applies each category, resets, and persists a named local look without changing world progress", async ({
  page,
}) => {
  await boot(page, "juni", { "lesson-progress-sentinel": "KEEP" });
  await page.keyboard.press("e");
  await expect(page.locator("#dialog")).toBeVisible();
  await page.locator("#close").click();
  const before = await state(page);
  expect(before.visited.length).toBeGreaterThan(0);
  await open(page);
  await expect(page.locator("[data-character]")).toHaveCount(6);
  await page.locator('[data-character="ara"]').click();
  await item(page, "hairstyle", "ara-braided-bun");
  await item(page, "outfit", "ara-sunlit-linen");
  await item(page, "accessory", "ara-shell-barrette");
  await page.locator('[data-action="run"]').click();
  await page.locator("#character-preview-direction").selectOption("back");
  await page.locator("#appearance-preset-name").fill("Buổi dạo biển");
  await apply(page);
  const chosen = await state(page);
  expect(chosen.appearance).toEqual(araLook);
  expect(chosen.key).toContain("studio-ara:");
  expect(chosen.players).toBe(1);
  expect(chosen.sampling).toBe(1);
  expect([chosen.x, chosen.y, chosen.visited]).toEqual([
    before.x,
    before.y,
    before.visited,
  ]);
  const stored = await page.evaluate(
    ({ V1, V2 }) => ({
      v1: JSON.parse(localStorage.getItem(V1)!),
      v2: JSON.parse(localStorage.getItem(V2)!),
      progress: localStorage.getItem("lesson-progress-sentinel"),
    }),
    { V1, V2 },
  );
  expect(stored.v1).toEqual({ version: 1, characterId: "ara" });
  expect(stored.v2.version).toBe(2);
  expect(
    stored.v2.presets.some((p: { name: string }) => p.name === "Buổi dạo biển"),
  ).toBe(true);
  expect(stored.progress).toBe("KEEP");
  await apply(page, true);
  await page.reload();
  await ready(page);
  const restored = await state(page);
  expect(restored.appearance).toEqual(araLook);
  expect([restored.x, restored.y, restored.visited]).toEqual([
    before.x,
    before.y,
    before.visited,
  ]);
  await open(page);
  await page.locator("#appearance-reset").click();
  await apply(page, true);
  const reset = await state(page);
  expect(reset.key).toBe("character-ara");
  expect(reset.appearance).toMatchObject({
    hairstyleId: null,
    outfitId: null,
    accessoryIds: [],
  });
});
test("legacy v1 selection migrates additively without rewriting data just to read it", async ({
  page,
}) => {
  await boot(page, "haneul", { "lesson-progress-sentinel": "KEEP" });
  expect((await state(page)).id).toBe("haneul");
  expect(await page.evaluate((V2) => localStorage.getItem(V2), V2)).toBeNull();
  await open(page);
  await expect(page.locator('[data-character="haneul"]')).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await apply(page, true);
  const after = await page.evaluate(
    ({ V1, V2 }) => ({
      legacy: JSON.parse(localStorage.getItem(V1)!),
      next: JSON.parse(localStorage.getItem(V2)!),
      sentinel: localStorage.getItem("lesson-progress-sentinel"),
    }),
    { V1, V2 },
  );
  expect(after.legacy).toEqual({ version: 1, characterId: "haneul" });
  expect(after.next.appearances.haneul).toMatchObject({
    hairstyleId: null,
    outfitId: null,
    accessoryIds: [],
  });
  expect(after.sentinel).toBe("KEEP");
});
test("switching between cosmetic-compatible and locked original identities restores each own set and keeps one sprite", async ({
  page,
}) => {
  await boot(page, "juni");
  const before = await state(page);
  await open(page);
  for (const [preset, id, accessory] of [
    ["review-ara-harbor", "ara", "ara-shell-barrette"],
    ["review-doyun-varsity", "doyun", "doyun-linen-kerchief"],
  ]) {
    await page.locator("#appearance-preset").selectOption(preset);
    await apply(page);
    const next = await state(page);
    expect(next.id).toBe(id);
    expect(next.appearance.accessoryIds).toEqual([accessory]);
    expect(next.players).toBe(1);
    expect([next.x, next.y, next.visited]).toEqual([
      before.x,
      before.y,
      before.visited,
    ]);
  }
  await page.locator('[data-character="bomi"]').click();
  await apply(page);
  expect((await state(page)).key).toBe("character-bomi");
  await page.locator('[data-character="ara"]').click();
  await apply(page);
  expect((await state(page)).appearance).toMatchObject({
    hairstyleId: "ara-braided-bun",
    outfitId: "ara-coastal-parka",
    accessoryIds: ["ara-shell-barrette"],
  });
  await apply(page, true);
});
test("corrupt and incompatible appearance references preserve the valid v1 identity and original defaults", async ({
  page,
}) => {
  const bad = {
    version: 2,
    selectedCharacterId: "minjun",
    appearances: {
      minjun: {
        ...araLook,
        characterId: "minjun",
        accessoryIds: ["unknown", "ara-shell-barrette"],
      },
    },
    presets: [null, {}],
  };
  await boot(page, "minjun", {
    [V2]: JSON.stringify(bad),
    "lesson-progress-sentinel": "KEEP",
  });
  const s = await state(page);
  expect(s.id).toBe("minjun");
  expect(s.key).toBe("character-minjun");
  expect(s.appearance).toMatchObject({
    hairstyleId: null,
    outfitId: null,
    accessoryIds: [],
  });
  expect(s.players).toBe(1);
  expect(
    await page.evaluate(() => localStorage.getItem("lesson-progress-sentinel")),
  ).toBe("KEEP");
});
test("missing cosmetic artwork falls back to the original character without blank or duplicate players", async ({
  page,
}) => {
  await page.route("**/cosmetics/ara-braided-bun/paint.png", (route) =>
    route.fulfill({ status: 404, body: "Missing review texture" }),
  );
  await boot(page, "ara");
  const before = await state(page);
  await open(page);
  await item(page, "hairstyle", "ara-braided-bun");
  await expect(page.locator("#character-feedback")).toContainText("khôi phục");
  await apply(page, true);
  const after = await state(page);
  expect(after.key).toBe("character-ara");
  expect(after.players).toBe(1);
  expect(after.appearance.hairstyleId).toBeNull();
  expect([after.x, after.y]).toEqual([before.x, before.y]);
});
test("repeated six-character and cosmetic switches keep texture/preview caches bounded and world state fixed", async ({
  page,
}) => {
  test.setTimeout(180000);
  await boot(page);
  await open(page);
  const before = await state(page);
  const checkpoints = [];
  for (let i = 0; i < 20; i++) {
    if (i % 5 === 4)
      await page
        .locator(
          `[data-character="${["juni", "haneul", "bomi", "minjun"][Math.floor(i / 5)]}"]`,
        )
        .click();
    else
      await page
        .locator("#appearance-preset")
        .selectOption(
          [
            "review-ara-harbor",
            "review-ara-sunlit",
            "review-doyun-field",
            "review-doyun-varsity",
          ][i % 4],
        );
    await apply(page);
    const q = await page.evaluate(() => window.__GATE3__!);
    expect(q.playerSprites).toBe(1);
    expect(q.characterAssets.textures.length).toBeLessThanOrEqual(3);
    expect(q.characterAssets.composition.baseImages).toBeLessThanOrEqual(2);
    expect(q.characterAssets.composition.compositeImages).toBeLessThanOrEqual(
      2,
    );
    expect(new Set(q.characterAssets.textures.map((t) => t.key)).size).toBe(
      q.characterAssets.textures.length,
    );
    expect([q.x, q.y, q.visited]).toEqual([before.x, before.y, before.visited]);
    checkpoints.push(q.characterAssets);
  }
  await test.info().attach("texture-cache-observations", {
    body: JSON.stringify(checkpoints, null, 2),
    contentType: "application/json",
  });
});
test("mobile landscape Studio has native-sized visible preview, reachable actions and isolated touch; joystick resumes", async ({
  browser,
}) => {
  const c = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
  });
  const p = await c.newPage();
  try {
    await boot(p, "juni");
    await open(p);
    const before = await state(p);
    await p.locator('[data-character="ara"]').tap();
    await p.locator('[data-category="outfit"]').tap();
    await p.locator('[data-cosmetic="ara-coastal-parka"]').tap();
    const geometry = await p.evaluate(() => {
      const box = (selector: string) => {
        const r = document.querySelector(selector)!.getBoundingClientRect();
        return {
          x: r.x,
          y: r.y,
          width: r.width,
          height: r.height,
          bottom: r.bottom,
          right: r.right,
        };
      };
      return {
        preview: box("#character-preview"),
        direction: box("#character-preview-direction"),
        confirm: box("#character-confirm"),
        save: box("#appearance-save"),
        reset: box("#appearance-reset"),
        screen: [innerWidth, innerHeight],
      };
    });
    await p.setViewportSize({ width: 390, height: 844 });
    await p.setViewportSize({ width: 844, height: 390 });
    await expect(p.locator("#character-preview")).toHaveAttribute(
      "width",
      "96",
    );
    expect(geometry.preview.width).toBe(96);
    expect(geometry.preview.height).toBe(112);
    for (const b of [
      geometry.preview,
      geometry.direction,
      geometry.confirm,
      geometry.save,
      geometry.reset,
    ]) {
      expect(b.x).toBeGreaterThanOrEqual(0);
      expect(b.y).toBeGreaterThanOrEqual(0);
      expect(b.right).toBeLessThanOrEqual(844);
      expect(b.bottom).toBeLessThanOrEqual(390);
    }
    for (const b of [
      geometry.direction,
      geometry.confirm,
      geometry.save,
      geometry.reset,
    ])
      expect(b.height).toBeGreaterThanOrEqual(44);
    expect((await state(p)).x).toBe(before.x);
    expect((await state(p)).y).toBe(before.y);
    await p.locator("#character-confirm").tap();
    await expect(p.locator("#character-selection")).not.toBeVisible();
    await ready(p);
    const initial = await state(p);
    expect(initial.appearance.outfitId).toBe("ara-coastal-parka");
    const touch = await c.newCDPSession(p),
      box = await p.locator("#joystick").boundingBox(),
      x = box!.x + box!.width / 2,
      y = box!.y + box!.height / 2;
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x, y, id: 1 }],
    });
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: x + box!.width * 0.3, y, id: 1 }],
    });
    await p.waitForFunction((x) => window.__GATE3__!.x > x + 6, initial.x);
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    expect((await state(p)).players).toBe(1);
    expect(await p.evaluate(() => window.__GATE3__!.camera.pointers)).toBe(0);
  } finally {
    await c.close();
  }
});
