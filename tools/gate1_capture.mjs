import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const out = "docs/gate1",
  rows = [],
  errors = [],
  requests = new Set();
try {
  for (const [name, url, x, y, overview] of [
    [
      "GATE1_STREET_NATIVE",
      "gate1-street.html?qa&renderer=canvas&overview",
      992,
      590,
      true,
    ],
    [
      "GATE1_NORTH_REFERENCE",
      "v10-city-review.html?qa&renderer=canvas",
      2176,
      1328,
      false,
    ],
  ]) {
    const p = await browser.newPage({
      viewport: {
        width: overview ? 1600 : 1440,
        height: overview ? 1140 : 1140,
      },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
      serviceWorkers: "block",
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("request", (r) => requests.add(new URL(r.url()).pathname));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto("http://127.0.0.1:4230/3D-pharse5-/" + url);
    await p.waitForFunction(
      (o) => (o ? window.__GATE1__?.ready : window.__SEOUL__?.ready),
      overview,
    );
    await p.evaluate(
      ([x, y, o]) =>
        o
          ? window.__GATE1_TEST__.place(x, y)
          : window.__SEOUL_TEST__.place(x, y),
      [x, y, overview],
    );
    const frame = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
    await p.waitForFunction(
      (n) => window.__PIXEL_METRICS__.frameCount > n + 4,
      frame,
    );
    const data = await p
      .locator("canvas")
      .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
    const buf = Buffer.from(data.png.split(",")[1], "base64");
    await fs.writeFile(`${out}/${name}.png`, buf);
    rows.push({
      name,
      url,
      size: data.size,
      position: [x, y],
      sha256: createHash("sha256").update(buf).digest("hex"),
      source:
        "Actual Phaser Canvas at DPR1/zoom1; QA camera composition only, not traversal proof",
    });
    await p.close();
  }
  await fs.writeFile(
    out + "/capture-provenance.json",
    JSON.stringify({ rows, errors, requests: [...requests].sort() }, null, 2) +
      "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(JSON.stringify({ captures: rows.length, errors }));
} finally {
  await browser.close();
}
