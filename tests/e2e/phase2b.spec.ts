import { test, expect } from "@playwright/test";
const ready = (p: import("@playwright/test").Page) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__!.chunks.inflight === 0,
  );
test("twelve-entry mobile landscape gallery reaches the final identity, restores it on reopen and survives orientation changes", async ({
  page,
}) => {
  await page.setViewportSize({ width: 844, height: 390 });
  await page.goto("./?renderer=canvas");
  await expect(page.locator("[data-character]")).toHaveCount(12);
  for (const id of ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"]) {
    await page.locator(`[data-character="${id}"]`).click();
    await expect(page.locator(`[data-character="${id}"]`)).toHaveAttribute(
      "aria-pressed",
      "true",
    );
  }
  await expect(page.locator("#future-roster")).toBeHidden();
  await expect(page.locator("[data-cosmetic]")).toHaveCount(0);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.setViewportSize({ width: 667, height: 375 });
  await page.waitForTimeout(250);
  const fit = await page.evaluate(() => {
    const d = document.querySelector("#character-selection")!,
      c = document.querySelector("#character-preview")!,
      a = document.querySelector("#character-art")!;
    const r = c.getBoundingClientRect(),
      b = a.getBoundingClientRect();
    return {
      overflow: d.scrollWidth > d.clientWidth,
      preview: {
        width: r.width,
        height: r.height,
        inside:
          r.x >= b.x &&
          r.y >= b.y &&
          r.right <= b.right &&
          r.bottom <= b.bottom,
      },
      buttons: [
        "#character-confirm",
        "#appearance-save",
        "#appearance-reset",
      ].map((s) => {
        const r = document.querySelector(s)!.getBoundingClientRect();
        return { w: r.width, h: r.height };
      }),
    };
  });
  expect(fit.overflow).toBe(false);
  expect(fit.preview).toEqual({ width: 96, height: 112, inside: true });
  for (const b of fit.buttons) {
    expect(b.w).toBeGreaterThanOrEqual(44);
    expect(b.h).toBeGreaterThanOrEqual(44);
  }
  await page.locator("#character-confirm").click();
  await ready(page);
  expect(await page.evaluate(() => window.__GATE3__!.characterId)).toBe(
    "hyunwoo",
  );
  await page.locator("#settings summary").click();
  await page.locator("#character-open").click();
  await expect(page.locator('[data-character="hyunwoo"]')).toBeInViewport();
});
test("new identities resolve incompatible stored cosmetics without deleting an approved look, preset or real visited marker", async ({
  page,
}) => {
  await page.addInitScript(() => {
    if (sessionStorage.getItem("p2b-seed")) return;
    sessionStorage.setItem("p2b-seed", "1");
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "yuna" }),
    );
    localStorage.setItem(
      "korean-arena-appearance-preferences-v2",
      JSON.stringify({
        version: 2,
        selectedCharacterId: "yuna",
        appearances: {
          ara: {
            schemaVersion: 2,
            characterId: "ara",
            hairstyleId: "ara-braided-bun",
            outfitId: "ara-coastal-parka",
            accessoryIds: ["ara-shell-barrette"],
          },
          yuna: {
            schemaVersion: 2,
            characterId: "yuna",
            hairstyleId: "ara-braided-bun",
            outfitId: "ara-coastal-parka",
            accessoryIds: ["ara-shell-barrette"],
          },
        },
        presets: [],
      }),
    );
  });
  await page.goto("./?renderer=canvas");
  await ready(page);
  expect(await page.evaluate(() => window.__GATE3__!.appearance)).toEqual({
    schemaVersion: 2,
    characterId: "yuna",
    hairstyleId: null,
    outfitId: null,
    accessoryIds: [],
  });
  await page.keyboard.press("e");
  await expect(page.locator("#dialog")).toBeVisible();
  await page.locator("#close").click();
  const before = await page.evaluate(() => ({
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
    visited: window.__GATE3__!.visited,
  }));
  expect(before.visited.length).toBeGreaterThan(0);
  await page.locator("#settings summary").click();
  await page.locator("#character-open").click();
  await page.locator('[data-character="hyunwoo"]').click();
  await page.locator("#appearance-preset-name").fill("Hành trình mới");
  await page.locator("#character-confirm").click();
  await ready(page);
  await page.reload();
  await ready(page);
  const after = await page.evaluate(() => ({
    id: window.__GATE3__!.characterId,
    x: window.__GATE3__!.x,
    y: window.__GATE3__!.y,
    visited: window.__GATE3__!.visited,
    store: JSON.parse(
      localStorage.getItem("korean-arena-appearance-preferences-v2")!,
    ),
  }));
  expect(after.id).toBe("hyunwoo");
  expect({ x: after.x, y: after.y, visited: after.visited }).toEqual(before);
  expect(after.store.appearances.ara.hairstyleId).toBe("ara-braided-bun");
  expect(JSON.stringify(after.store.presets)).toContain("Hành trình mới");
});
