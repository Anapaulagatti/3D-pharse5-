import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/g3a-forecourt-restoration",
  b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
const errors = [],
  cases = [];
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto("http://127.0.0.1:4287/");
  const links = await p.locator("a").evaluateAll((as) => as.map((a) => a.href));
  for (const u of links) {
    const r = await p.request.get(u);
    if (!r.ok()) throw Error(u);
  }
  for (const [scene, phase, renderer] of [
    ["registration-refined", "before", "auto"],
    ["registration-forecourt", "after", "auto"],
    ["registration-forecourt", "after", "canvas"],
  ]) {
    await p.goto(
      `http://127.0.0.1:4287/gate3-review.html?scene=${scene}&entry=station&native&pixelAudit&renderer=${renderer}`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.keyboard.down("s");
    await p.waitForFunction(() => window.__GATE3__.y >= 2855);
    await p.keyboard.up("s");
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    await fs.writeFile(
      `/tmp/package-${phase}-${renderer}.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    cases.push({
      scene,
      phase,
      renderer,
      actualRenderer: await p.evaluate(() => window.__GATE3__.renderer),
      audit: a,
    });
  }
  await p.goto("http://127.0.0.1:4287/gate3-review.html?native");
  await p.waitForFunction(() => window.__GATE3__?.ready);
  if ((await p.evaluate(() => window.__GATE3__.scene)) !== "world")
    throw Error("Default changed");
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    `${D}/package-smoke.json`,
    JSON.stringify(
      {
        status: "PASS",
        links: links.length,
        cases,
        errors,
        defaultWorld: "unchanged",
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS extracted ZIP, before/after WebGL, after Canvas, default world and index links",
  );
} finally {
  await b.close();
}
