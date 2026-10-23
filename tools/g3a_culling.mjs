import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
for (let repeat = 0; repeat < 2; repeat++)
  for (const renderer of ["auto", "canvas"])
    for (const unculled of repeat ? [false, true] : [true, false]) {
      const context = await b.newContext({
        viewport: { width: 1280, height: 1000 },
        deviceScaleFactor: 1,
      });
      const p = await context.newPage();
      for (const phase of ["stationary", "tour"]) {
        await p.goto(
          `http://127.0.0.1:4271/gate3-review.html?profile&renderer=${renderer}&${unculled ? "unculled&" : ""}scene=${phase === "stationary" ? "district&entry=station" : "world"}`,
        );
        await p.waitForFunction(() => window.__GATE3__?.ready);
        await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
        await p.evaluate(() => window.__GATE3_PROFILE__.reset());
        if (phase === "tour") {
          await p.locator("#scenic").click();
          await p.locator("#start-tour").click();
        }
        await p.waitForTimeout(phase === "tour" ? 8000 : 4000);
        rows.push({
          repeat,
          renderer,
          unculled,
          phase,
          ...(await p.evaluate(() => ({
            state: window.__GATE3__,
            profile: window.__GATE3_PROFILE__.snapshot(),
          }))),
        });
      }
      await context.close();
      console.log("cull", repeat, renderer, unculled);
    }
await fs.writeFile(
  "docs/gate3a-corrections/culling-ablation.json",
  JSON.stringify(
    {
      conditions:
        "Stage2 render-only ablation on final build;2 repeats, reversed culling order; native assets/zoom/viewport unchanged; no recording or concurrent browser work.",
      rows,
    },
    null,
    2,
  ),
);
await b.close();
