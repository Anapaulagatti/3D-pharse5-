import { test, expect } from "@playwright/test";
const names = [
  ["seondeok", "한연화", "Han Yeonhwa"],
  ["sejong", "백준서", "Baek Junseo"],
  ["jang", "남경우", "Nam Gyeongu"],
  ["saimdang", "윤화연", "Yun Hwayeon"],
  ["yi", "강무영", "Kang Muyeong"],
  ["yu", "서다은", "Seo Daeun"],
];
const oldNames =
  /선덕여왕|세종대왕|장영실|신사임당|이순신|유관순|Seondeok|Sejong|Jang Yeong-sil|Shin Saimdang|Yi Sun-sin|Yu Gwan-sun/;

test("all six fictional identities remain attached to existing actors and all public dialogue nodes exclude historical personal identities", async ({
  page,
}) => {
  test.setTimeout(180000);
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
  for (const [suffix, ko, vi] of names) {
    const id = "npc-history-" + suffix;
    await page.goto("?qa&renderer=canvas&npcReview=" + id);
    await page.waitForFunction(
      (id) =>
        window.__GATE3__?.ready &&
        window.__NPC_WORLD__?.actors.some((a) => a.id === id),
      id,
    );
    await page.locator("#history-art-review").click();
    await expect(
      page.locator(`[data-history-id="${id}"]`),
    ).toHaveAccessibleName(new RegExp(vi + " · " + ko));
    expect(await page.locator("#history-art-dialog").innerText()).not.toMatch(
      oldNames,
    );
    await page.locator("#history-art-close").click();
    const delta = await page.evaluate((id) => {
      const n = window.__NPC_WORLD__!.actors.find((a) => a.id === id)!;
      return [
        n.position[0] - window.__GATE3__!.x,
        n.position[1] - window.__GATE3__!.y,
      ];
    }, id);
    const [dx, dy] = delta;
    const key =
      Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
    await page.locator("#stage canvas").click({ position: { x: 320, y: 180 } });
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
    await expect(page.locator("#npc-interact")).toContainText(vi);
    await page.keyboard.press("e");
    await expect(page.locator("#npc-dialogue-name")).toHaveText(
      `${vi} · ${ko}`,
    );
    for (let node = 0; node < 6; node++) {
      const dialog = page.locator("#npc-dialogue");
      expect(await dialog.innerText()).not.toMatch(oldNames);
      expect(await dialog.locator("#npc-dialogue-role").innerText()).toContain(
        "nhân vật hư cấu",
      );
      if (node === 0)
        await expect(page.locator("#npc-dialogue-vi")).toContainText(vi);
      if (node === 1)
        await expect(page.locator("#npc-dialogue-ko")).toContainText(
          "실제 역사 인물이 아닙니다",
        );
      if (node < 5) await page.locator("#npc-dialogue-next").click();
    }
    await page.locator("#npc-dialogue-return").click();
    await page.waitForFunction(() => !window.__GATE3__!.paused);
    expect(await page.evaluate(() => window.__NPC_WORLD__!.catalogTotal)).toBe(
      26,
    );
    expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
  }
});
