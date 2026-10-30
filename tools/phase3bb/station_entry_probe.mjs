import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
try {
  for (const [name, base] of [
    ["approved20", "http://127.0.0.1:4498/"],
    ["hotfix", "http://127.0.0.1:4320/3D-pharse5-/"],
  ]) {
    const c = await b.newContext({ viewport: { width: 960, height: 640 } });
    await c.addInitScript(() =>
      localStorage.setItem(
        "korean-arena-player-preferences-v1",
        JSON.stringify({ version: 1, characterId: "haneul" }),
      ),
    );
    const p = await c.newPage();
    await p.goto(base + "?entry=station-all&renderer=canvas");
    await p.waitForFunction(
      () => window.__GATE3__?.characterId === "haneul",
      {},
      { timeout: 45000 },
    );
    await p.waitForTimeout(1500);
    rows.push({ name, game: await p.evaluate(() => window.__GATE3__) });
    await c.close();
  }
  await fs.writeFile(
    "docs/phase3bb-hotfix/STATION_ENTRY_PROBE.json",
    JSON.stringify(rows, null, 2),
  );
  console.log(
    rows.map((r) => ({
      name: r.name,
      x: r.game.x,
      y: r.game.y,
      ready: r.game.ready,
      chunks: r.game.chunks.inflight,
    })),
  );
} finally {
  await b.close();
}
