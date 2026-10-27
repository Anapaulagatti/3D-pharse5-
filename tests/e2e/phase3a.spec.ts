import { axisTo, walkPath } from "../../tools/phase3a/walk.mjs";
import { test, expect, type Page } from "@playwright/test";
import fs from "node:fs";
const defs = JSON.parse(
  fs.readFileSync("assets-src/npcs/phase3a/registry.json", "utf8"),
).npcs as { id: string; homeZone: string; reviewSpawn: [number, number] }[];
async function ready(p: Page, id: string) {
  await p.waitForFunction(
    (id) =>
      window.__GATE3__?.ready &&
      window.__NPC_WORLD__?.actors.some((a) => a.id === id),
    id,
    { timeout: 60000 },
  );
}
async function boot(p: Page, id: string) {
  await p.addInitScript(() => {
    if (!sessionStorage.getItem("npc-seed")) {
      localStorage.setItem(
        "korean-arena-player-preferences-v1",
        JSON.stringify({ version: 1, characterId: "juni" }),
      );
      localStorage.setItem("npc-learning-sentinel", "KEEP");
      sessionStorage.setItem("npc-seed", "1");
    }
  });
  await p.goto(`./?qa&renderer=canvas&pixelAudit&npcReview=${id}`);
  await ready(p, id);
}
async function approach(p: Page, id: string) {
  const s = await p.evaluate(
    (id) => ({
      npc: window.__NPC_WORLD__!.actors.find((a) => a.id === id)!,
      player: window.__GATE3__!,
    }),
    id,
  );
  const dx = s.npc.position[0] - s.player.x,
    dy = s.npc.position[1] - s.player.y,
    key =
      Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "d" : "a") : dy > 0 ? "s" : "w";
  await p.locator("#stage canvas").click({ position: { x: 300, y: 250 } });
  await p.keyboard.down(key);
  try {
    await p.waitForFunction((id) => window.__NPC_WORLD__?.target === id, id, {
      timeout: 12000,
    });
  } finally {
    await p.keyboard.up(key);
  }
}
test("all14 contextual residents are approachable with real controls and close/resume safely in the canonical world", async ({
  page,
}) => {
  test.setTimeout(240000);
  expect(defs).toHaveLength(14);
  for (const d of defs) {
    await boot(page, d.id);
    await approach(page, d.id);
    const before = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
      appearance: window.__GATE3__!.appearance,
      visited: window.__GATE3__!.visited,
    }));
    await page.keyboard.press("e");
    await expect(page.locator("#npc-dialogue")).toHaveAttribute(
      "data-npc-id",
      d.id,
    );
    await expect(page.locator("#npc-dialogue")).toBeVisible();
    await expect(page.locator("#npc-dialogue-ko")).toContainText(/[가-힣]/);
    await expect(page.locator("#npc-dialogue-vi")).not.toBeEmpty();
    await page.keyboard.down("d");
    await page.waitForTimeout(100);
    await page.keyboard.up("d");
    const during = await page.evaluate(() => ({
      x: window.__GATE3__!.x,
      y: window.__GATE3__!.y,
      appearance: window.__GATE3__!.appearance,
      visited: window.__GATE3__!.visited,
    }));
    expect(during).toEqual(before);
    await page.locator('[data-npc-choice="place"]').click();
    await page.locator("#npc-dialogue-next").click();
    await page.keyboard.press("Escape");
    await expect(page.locator("#npc-dialogue")).not.toBeVisible();
    await page.waitForFunction(
      () => !window.__GATE3__!.paused && !window.__NPC_WORLD__!.dialogue,
    );
    const state = await page.evaluate(
      (id) => ({
        world: window.__GATE3__,
        npc: window.__NPC_WORLD__?.actors.find((n) => n.id === id),
        population: window.__NPC_WORLD__,
      }),
      d.id,
    );
    expect(state.world!.scene).toBe("palace-cleanup-world");
    expect(state.world!.playerSprites).toBe(1);
    expect(state.npc!.state).not.toBe("TALK");
    expect(state.population!.active).toBeLessThanOrEqual(4);
    expect(state.population!.assets.loaded).toBeLessThanOrEqual(4);
    expect(
      await page.evaluate(() => localStorage.getItem("npc-learning-sentinel")),
    ).toBe("KEEP");
  }
});
test("keyboard choices/Enter, close and corrupt NPC-only storage preserve player appearance and progress", async ({
  page,
}) => {
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-npc-world-v1",
      JSON.stringify({
        version: 1,
        records: { "npc-seoyeon": { position: "xx" } },
      }),
    ),
  );
  await boot(page, "npc-seoyeon");
  await approach(page, "npc-seoyeon");
  await page.keyboard.press("e");
  await page.keyboard.press("Enter");
  await expect(page.locator("#npc-dialogue")).toHaveAttribute(
    "data-node-id",
    "npc-seoyeon-place",
  );
  await page.keyboard.press("Enter");
  await expect(page.locator("#npc-dialogue")).toHaveAttribute(
    "data-node-id",
    "npc-seoyeon-care",
  );
  await page.keyboard.press("Enter");
  await expect(page.locator("#npc-dialogue")).not.toBeVisible();
  await page.reload();
  await ready(page, "npc-seoyeon");
  expect(await page.evaluate(() => window.__GATE3__!.characterId)).toBe("juni");
  expect(
    await page.evaluate(() => localStorage.getItem("npc-learning-sentinel")),
  ).toBe("KEEP");
});
for (const [width, height] of [
  [667, 375],
  [844, 390],
])
  test(`touch${width}x${height}: reachable Korean/Vietnamese dialogue,isolated controls and resumed joystick`, async ({
    browser,
  }) => {
    const c = await browser.newContext({
        viewport: { width, height },
        hasTouch: true,
        isMobile: true,
      }),
      p = await c.newPage();
    try {
      await boot(p, "npc-harin");
      await approach(p, "npc-harin");
      await p.locator("#npc-interact").tap();
      await expect(p.locator("#npc-dialogue")).toBeVisible();
      const geometry = await p.locator("#npc-dialogue").evaluate((d) => {
        const r = d.getBoundingClientRect();
        return {
          w: r.width,
          h: r.height,
          x: r.x,
          y: r.y,
          buttons: [...d.querySelectorAll("button")]
            .filter((b) => !b.hidden)
            .map((b) => {
              const q = b.getBoundingClientRect();
              return {
                w: q.width,
                h: q.height,
                inside:
                  q.x >= 0 &&
                  q.y >= 0 &&
                  q.right <= innerWidth &&
                  q.bottom <= innerHeight,
              };
            }),
        };
      });
      expect(geometry.x).toBeGreaterThanOrEqual(0);
      expect(geometry.y).toBeGreaterThanOrEqual(0);
      expect(geometry.w).toBeLessThanOrEqual(width);
      for (const b of geometry.buttons) {
        expect(b.w).toBeGreaterThanOrEqual(44);
        expect(b.h).toBeGreaterThanOrEqual(44);
        expect(b.inside).toBe(true);
      }
      await p.locator('[data-npc-choice="care"]').tap();
      await p.locator("#npc-dialogue-return").tap();
      await p.waitForFunction(() => !window.__GATE3__!.paused);
      const before = await p.evaluate(() => window.__GATE3__!.x),
        r = (await p.locator("#joystick").boundingBox())!,
        cdp = await c.newCDPSession(p);
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
      expect(await p.evaluate(() => window.__GATE3__!.x)).toBeGreaterThan(
        before,
      );
      expect(await p.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
    } finally {
      await c.close();
    }
  });
test("NPC resource failure does not replace or freeze the approved player", async ({
  page,
}) => {
  await page.route("**/assets/npcs/phase3a/npc-seoyeon/atlas.png", (r) =>
    r.fulfill({ status: 404, body: "missing NPC art" }),
  );
  await page.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
  await page.goto("./?qa&renderer=canvas&npcReview=npc-seoyeon");
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__NPC_WORLD__?.assets.errors.length,
  );
  const before = await page.evaluate(() => window.__GATE3__!.y);
  await page.keyboard.down("s");
  await page.waitForTimeout(350);
  await page.keyboard.up("s");
  expect(await page.evaluate(() => window.__GATE3__!.y)).toBeGreaterThan(
    before,
  );
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
  expect(await page.locator("#npc-dialogue").isVisible()).toBe(false);
});

test("continuous mainland-to-Jeju exploration uses the repaired bridge with original movement and collision", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    hasTouch: true,
  });
  const page = await context.newPage();
  try {
    test.setTimeout(360000);
    const plan = JSON.parse(
      fs.readFileSync("docs/phase3a/cross-zone-route.json", "utf8"),
    );
    await boot(page, "npc-soobin");
    let bridge = false;
    await walkPath(page, plan.waypoints, async () => {
      const s = await page.evaluate(() => window.__GATE3__!);
      if (s.x > 3180 && s.x < 3500 && s.y > 3400 && s.y < 3700) bridge = true;
      expect(s.scene).toBe("palace-cleanup-world");
      expect(s.playerSprites).toBe(1);
    });
    const state = await page.evaluate(() => ({
      p: window.__GATE3__!,
      n: window.__NPC_WORLD__!,
    }));
    expect(bridge).toBe(true);
    expect(state.p.x).toBeGreaterThan(3500);
    expect(state.p.y).toBeGreaterThan(4300);
    expect(state.n.assets.loaded).toBeLessThanOrEqual(4);
  } finally {
    await context.close();
  }
});
test("real zone exit/reentry freezes inactive residents and restores them without duplicate/orphan sprites", async ({
  page,
}) => {
  test.setTimeout(180000);
  await boot(page, "npc-seoyeon");
  await axisTo(page, "x", 2048);
  const snapshots = [];
  for (let i = 0; i < 3; i++) {
    await axisTo(page, "y", 1470);
    await page.waitForFunction(() => window.__NPC_WORLD__!.active === 0);
    const before = await page.evaluate(() => window.__NPC_WORLD__!.records);
    await page.waitForTimeout(300);
    expect(await page.evaluate(() => window.__NPC_WORLD__!.records)).toEqual(
      before,
    );
    await axisTo(page, "y", 1310);
    await page.waitForFunction(() => window.__NPC_WORLD__!.active >= 2);
    const s = await page.evaluate(() => window.__NPC_WORLD__!);
    expect(new Set(s.actors.map((a) => a.id)).size).toBe(s.active);
    expect(s.active).toBeLessThanOrEqual(4);
    expect(s.assets.loaded).toBeLessThanOrEqual(4);
    snapshots.push(s);
  }
  expect(snapshots.at(-1)!.despawns).toBeGreaterThanOrEqual(6);
  expect(await page.evaluate(() => window.__GATE3__!.playerSprites)).toBe(1);
});
