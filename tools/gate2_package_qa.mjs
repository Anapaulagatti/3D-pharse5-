import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const results = [],
  errors = [];
const servers = [];
try {
  for (const [pkg, ids] of [
    ["A", ["a", "transition"]],
    ["B", ["b", "station", "transition"]],
    ["C", ["c"]],
  ]) {
    const port = 4265 + ["A", "B", "C"].indexOf(pkg);
    servers.push(
      spawn(
        "python3",
        [".cache/gate2/extracted/" + pkg + "/start.py", String(port)],
        { stdio: "ignore" },
      ),
    );
    await new Promise((r) => setTimeout(r, 500));
    for (const id of ids) {
      const p = await b.newPage({ viewport: { width: 1280, height: 980 } });
      p.on("pageerror", (e) => errors.push(e.message));
      p.on("response", (r) => {
        if (r.status() >= 400) errors.push(r.url());
      });
      await p.goto(
        `http://127.0.0.1:${port}/3D-pharse5-/gate2-review.html?scene=${id}`,
      );
      await p.waitForFunction(() => window.__GATE2__?.ready);
      assert.equal(
        await p.evaluate(() => typeof window.__GATE2_TEST__),
        "undefined",
      );
      const before = await p.evaluate(() => window.__GATE2__.x);
      await p.keyboard.down("d");
      await p.waitForTimeout(350);
      await p.keyboard.up("d");
      assert((await p.evaluate(() => window.__GATE2__.x)) > before + 10);
      results.push({
        package: pkg,
        scene: id,
        actualExtractedZip: true,
        keyboard: true,
        noQaHook: true,
      });
      await p.close();
    }
  }
  assert.equal(errors.length, 0);
  await fs.writeFile(
    "docs/gate2/package-qa.json",
    JSON.stringify({ results, errors }, null, 2) + "\n",
  );
  console.log(results.length, "packaged scene entries PASS");
} finally {
  await b.close();
  for (const s of servers) s.kill();
}
