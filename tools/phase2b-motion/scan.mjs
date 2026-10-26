import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
try {
  const c = await b.newContext({ viewport: { width: 1280, height: 1000 } });
  await c.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "sori" }),
    ),
  );
  const p = await c.newPage();
  for (const entry of [
    "transition",
    "station-all",
    "retail",
    "amusement",
    "palace-front-local",
    "culture",
    "jeju-culture",
  ]) {
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?native&renderer=canvas&entry=" +
        entry,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    rows.push(
      await p.evaluate((entry) => {
        const s = window.__GATE3__,
          v = {
            entry,
            x: s.x,
            y: s.y,
            id: s.characterId,
            scene: s.scene,
            room: {},
          };
        for (const [d, dx, dy] of [
          ["front", 0, 1],
          ["back", 0, -1],
          ["right", 1, 0],
        ]) {
          let n = 0;
          while (
            n < 300 &&
            window.__GATE3_TEST__.walkable(s.x + dx * n, s.y + dy * n)
          )
            n++;
          v.room[d] = n;
        }
        return v;
      }, entry),
    );
  }
  await fs.writeFile(
    "docs/phase2b-motion/path-scan.json",
    JSON.stringify(rows, null, 2),
  );
  console.log(rows);
} finally {
  await b.close();
}
