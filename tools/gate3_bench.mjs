import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const reports = [];
for (const renderer of ["auto", "canvas"]) {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await p.goto(
    "http://127.0.0.1:4261/gate3-review.html?scene=district&entry=station&renderer=" +
      renderer,
  );
  await p.waitForFunction(() => window.__GATE3__?.ready);
  await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  await p.waitForTimeout(6000);
  reports.push(
    await p.evaluate(() => {
      const c = document.querySelector("canvas"),
        g = c.getContext("webgl2") || c.getContext("webgl"),
        ext = g?.getExtension("WEBGL_debug_renderer_info");
      return {
        state: window.__GATE3__,
        driver: ext ? g.getParameter(ext.UNMASKED_RENDERER_WEBGL) : null,
        measurement:
          "Isolated stationary six-second desktop browser sample, no recording; still no physical-device certification",
      };
    }),
  );
  await p.close();
}
await fs.writeFile(
  "docs/gate3a/renderer-bench.json",
  JSON.stringify(reports, null, 2),
);
await b.close();
console.log(
  reports.map((r) => ({
    renderer: r.state.renderer,
    driver: r.driver,
    session: r.state.session,
  })),
);
