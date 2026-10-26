import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--enable-precise-memory-info"],
});
try {
  const c = await browser.newContext({
    viewport: { width: 1280, height: 1000 },
  });
  await c.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "juni" }),
    ),
  );
  const p = await c.newPage();
  await p.goto("http://127.0.0.1:4325/3D-pharse5-/?renderer=canvas");
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  await p.locator("#settings summary").click();
  await p.locator("#character-open").click({ noWaitAfter: true });
  const client = await c.newCDPSession(p),
    samples = [];
  for (let i = 0; i < 48; i++) {
    if (i % 6 === 5)
      await p
        .locator(
          `[data-character="${["juni", "haneul", "bomi", "minjun"][Math.floor(i / 6) % 4]}"]`,
        )
        .click();
    else
      await p
        .locator("#appearance-preset")
        .selectOption(
          [
            "review-ara-harbor",
            "review-ara-sunlit",
            "review-doyun-field",
            "review-doyun-varsity",
          ][i % 4],
        );
    await p.locator("#appearance-save").click();
    await p.waitForFunction(() => {
      const q = JSON.parse(
          localStorage.getItem("korean-arena-appearance-preferences-v2"),
        ),
        s = window.__GATE3__;
      return (
        s?.ready &&
        q &&
        s.characterId === q.selectedCharacterId &&
        JSON.stringify(s.appearance) ===
          JSON.stringify(q.appearances[s.characterId])
      );
    });
    if (i === 23 || i === 47) {
      await client.send("HeapProfiler.collectGarbage");
      await p.waitForTimeout(100);
      samples.push(
        await p.evaluate(
          (i) => ({
            switches: i + 1,
            actor: window.__GATE3__.characterId,
            cache: window.__GATE3__.characterAssets,
            players: window.__GATE3__.playerSprites,
            heap: performance.memory ? performance.memory.usedJSHeapSize : null,
          }),
          i,
        ),
      );
    }
  }
  const growth = samples[1].heap - samples[0].heap;
  await fs.writeFile(
    "docs/phase2a/memory-stability.json",
    JSON.stringify(
      {
        method:
          "Two repeated24-switch schedules, same final identity and bounded cache counts (cached look identities can differ), GC before retained-heap samples. Desktop Chromium Canvas while Studio/world paused; counts are actual texture ownership, not device certification.",
        samples,
        retainedHeapChangeAfterWarmup: growth,
        interpretation:
          "Resource counts must remain bounded; heap samples include the whole browser app and are observational. Physical/hardware leak certification remains NOT TESTED.",
      },
      null,
      2,
    ),
  );
  if (
    samples.some(
      (s) =>
        s.players !== 1 ||
        s.cache.textures.length > 3 ||
        s.cache.composition.compositeImages > 2 ||
        s.cache.composition.baseImages > 2,
    )
  )
    throw Error("Ownership growth");
  console.log("48 switches; retained heap change after warmup", growth);
  await c.close();
} finally {
  await browser.close();
}
