import { test, expect, type Page } from "@playwright/test";
const ready = (p: Page) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
async function boot(p: Page, id = "juni", extra: Record<string, string> = {}) {
  await p.addInitScript(
    ({ id, extra }) => {
      if (!sessionStorage.getItem("c2-seed")) {
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        );
        for (const [k, v] of Object.entries(extra)) localStorage.setItem(k, v);
        sessionStorage.setItem("c2-seed", "1");
      }
    },
    { id, extra },
  );
  await p.goto("./?renderer=canvas&entry=transition");
  await ready(p);
}
async function open(p: Page) {
  if (await p.locator("#character-selection").isVisible()) return;
  if (!(await p.locator("#character-open").isVisible()))
    await p.locator("#settings summary").click();
  await p.locator("#character-open").click();
  await p.locator("#character-selection").waitFor();
}
const preview = (p: Page) =>
  p.waitForFunction(
    () =>
      document.querySelector<HTMLCanvasElement>("#character-preview")?.dataset
        .previewState === "ready",
  );
async function apply(p: Page) {
  await p.locator("#character-confirm").click();
  await p.locator("#character-selection").waitFor({ state: "hidden" });
  await ready(p);
}
test("every actor has a working curated hair/outfit/accessory preview, applies it and can reset to approved defaults", async ({
  page,
}) => {
  test.setTimeout(180000);
  await boot(page);
  for (const id of [
    "juni",
    "haneul",
    "bomi",
    "minjun",
    "ara",
    "doyun",
    "sori",
    "jiwon",
    "nari",
    "taeyang",
    "yuna",
    "hyunwoo",
  ]) {
    await open(page);
    const before = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
    }));
    await page.locator("#appearance-preset").selectOption("fashion-" + id);
    await preview(page);
    expect(await page.locator("#appearance-preset-name").inputValue()).toBe("");
    const look = await page
      .locator("#character-preview")
      .getAttribute("data-appearance");
    expect(JSON.parse(look!).characterId).toBe(id);
    await apply(page);
    await page.waitForFunction(
      (look) => JSON.stringify(window.__GATE3__!.appearance) === look,
      look,
    );
    expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
    expect(
      await page.evaluate(() => ({
        x: window.__GATE3__!.x,
        y: window.__GATE3__!.y,
      })),
    ).toEqual(before);
    await open(page);
    await page.locator("#appearance-reset").click();
    await preview(page);
    await apply(page);
    await page.waitForFunction(
      () =>
        window.__GATE3__!.appearance.outfitId === null &&
        window.__GATE3__!.appearance.hairstyleId === null &&
        window.__GATE3__!.appearance.accessoryIds.length === 0,
    );
  }
  expect(
    await page.evaluate(
      () =>
        JSON.parse(
          localStorage.getItem("korean-arena-appearance-preferences-v2")!,
        ).presets,
    ),
  ).toHaveLength(0);
});
test("personal presets rename/delete, cancel a draft, and survive reload without losing other characters or world state", async ({
  page,
}) => {
  await boot(page, "sori", { "lesson-progress-sentinel": "KEEP" });
  await open(page);
  await page.locator("#appearance-preset").selectOption("fashion-sori");
  await preview(page);
  await page.locator("#appearance-preset-name").fill("Seoul dạo phố");
  await page.locator("#appearance-save").click();
  await page.waitForFunction(
    () =>
      JSON.parse(
        localStorage.getItem("korean-arena-appearance-preferences-v2")!,
      ).presets.length === 1,
  );
  const id = await page.evaluate(
    () =>
      JSON.parse(
        localStorage.getItem("korean-arena-appearance-preferences-v2")!,
      ).presets[0].id,
  );
  await page.locator("#appearance-preset").selectOption(id);
  await page.locator("#appearance-preset-name").fill("Ngày ở Jeju");
  await page.locator("#preset-rename").click();
  await page.locator("#appearance-preset").selectOption(id);
  await expect(page.locator("#appearance-preset-name")).toHaveValue(
    "Ngày ở Jeju",
  );
  const old = await page.evaluate(() => window.__GATE3__!.appearance);
  await page.locator("#appearance-preset").selectOption("fashion-haneul");
  await preview(page);
  await page.locator("#character-close").click();
  await ready(page);
  expect(await page.evaluate(() => window.__GATE3__!.appearance)).toEqual(old);
  await page.reload();
  await ready(page);
  expect(await page.evaluate(() => window.__GATE3__!.appearance)).toEqual(old);
  expect(
    await page.evaluate(() => localStorage.getItem("lesson-progress-sentinel")),
  ).toBe("KEEP");
  await open(page);
  await page.locator("#appearance-preset").selectOption(id);
  await page.locator("#preset-delete").click();
  await page.waitForFunction(
    () =>
      JSON.parse(
        localStorage.getItem("korean-arena-appearance-preferences-v2")!,
      ).presets.length === 0,
  );
  expect(await page.evaluate(() => window.__GATE3__!.appearance)).toEqual(old);
});
test("latest rapid preview wins and equipping a hat removes an incompatible quiff without touching original pixels", async ({
  page,
}) => {
  await boot(page, "doyun");
  await open(page);
  await page.locator('[data-category="hairstyle"]').click();
  await page.locator('[data-cosmetic="doyun-curly-crop"]').click();
  await preview(page);
  await page.locator('[data-category="accessory"]').click();
  await page.locator('[data-cosmetic="kr-garden-hat"]').click();
  await preview(page);
  let look = JSON.parse(
    (await page.locator("#character-preview").getAttribute("data-appearance"))!,
  );
  expect(look.hairstyleId).toBeNull();
  expect(look.accessoryIds).toContain("kr-garden-hat");
  for (let i = 0; i < 12; i++)
    await page
      .locator("#appearance-preset")
      .selectOption(i % 2 ? "fashion-sori" : "fashion-juni");
  await preview(page);
  look = JSON.parse(
    (await page.locator("#character-preview").getAttribute("data-appearance"))!,
  );
  expect(look.characterId).toBe("sori");
  expect(
    await page
      .locator("#character-preview")
      .getAttribute("data-preview-character"),
  ).toBe("sori");
  await apply(page);
  await page.waitForFunction(() => window.__GATE3__!.characterId === "sori");
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});
test("mismatched native-pose registration safely restores approved defaults", async ({
  page,
}) => {
  await page.route(
    "**/cosmetics/phase2c/kr-classic-bob/juni/mapping.json",
    async (route) => {
      const response = await route.fetch();
      const data = await response.json();
      data.baseAtlasSHA256 = "0".repeat(64);
      await route.fulfill({ response, json: data });
    },
  );
  await boot(page);
  await open(page);
  await page.locator('[data-category="hairstyle"]').click();
  await page.locator('[data-cosmetic="kr-classic-bob"]').click();
  await preview(page);
  await expect(page.locator('[data-cosmetic="default"]')).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await apply(page);
  expect(
    await page.evaluate(() => window.__GATE3__!.appearance.hairstyleId),
  ).toBeNull();
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});
for (const [width, height] of [
  [667, 375],
  [844, 390],
])
  test(`mobile${width}x${height}: native preview, reachable wardrobe/preset controls, all actions and world joystick`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height });
    await boot(page, "ara");
    await open(page);
    await page.locator("#appearance-preset").selectOption("fashion-ara");
    await preview(page);
    for (const action of ["walk", "run", "wave", "celebrate"]) {
      await page.locator("#character-action-mobile").selectOption(action);
      await page.waitForFunction(
        (action) =>
          document
            .querySelector<HTMLCanvasElement>("#character-preview")
            ?.dataset.frame?.startsWith(action + "-front"),
        action,
      );
    }
    const size = await page.locator("#character-preview").boundingBox();
    expect(size?.width).toBe(96);
    expect(size?.height).toBe(112);
    for (const s of [
      "#character-confirm",
      "#appearance-save",
      "#appearance-reset",
      "#preset-rename",
      "#preset-delete",
    ]) {
      await expect(page.locator(s)).toBeInViewport();
      const r = await page.locator(s).boundingBox();
      expect(r!.width).toBeGreaterThanOrEqual(44);
      expect(r!.height).toBeGreaterThanOrEqual(44);
    }
    await apply(page);
    expect(await page.evaluate(() => window.__GATE3__!.camera.pointers)).toBe(
      0,
    );
    const x = await page.evaluate(() => window.__GATE3__!.x);
    await page.keyboard.down("d");
    await page.waitForFunction((x) => window.__GATE3__!.x > x + 8, x);
    await page.keyboard.up("d");
    expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
  });
test("LAN/offline review without SubtleCrypto still binds and applies a genuine native cosmetic", async ({
  page,
}) => {
  await page.addInitScript(() =>
    Object.defineProperty(window.crypto, "subtle", { value: undefined }),
  );
  await boot(page);
  await open(page);
  await page.locator("#appearance-preset").selectOption("fashion-juni");
  await preview(page);
  await apply(page);
  await page.waitForFunction(
    () => window.__GATE3__!.appearance.outfitId === "kr-daily-hanbok",
  );
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});
