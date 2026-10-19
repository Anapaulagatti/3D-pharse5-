import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const base =
    process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/",
  out = (process.env.PIXEL_REVIEW_DIR ?? "docs/v6-restructure") + "/quality";
const results = [],
  errors = [],
  externalRequests = [];
for (const gl of [true, false]) {
  const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: gl
      ? [
          "--no-sandbox",
          "--use-gl=angle",
          "--use-angle=swiftshader",
          "--enable-unsafe-swiftshader",
        ]
      : ["--no-sandbox", "--disable-webgl"],
  });
  try {
    const p = await b.newPage({
      viewport: { width: 1440, height: 1140 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    p.on("request", (r) => {
      if (
        /^https?:/.test(r.url()) &&
        new URL(r.url()).origin !== new URL(base).origin
      )
        externalRequests.push(r.url());
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("console", (m) => {
      if (m.type() === "error") errors.push(m.text());
    });
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(
      base + "v6-world-review.html?qa" + (gl ? "&renderer=webgl" : ""),
    );
    await p.waitForFunction(
      () => window.__V3_WORLD__ && window.__SEOUL__?.ready,
    );
    const renderer = await p.evaluate(() => window.__PIXEL_METRICS__.renderer);
    if (renderer !== (gl ? "WebGL" : "Canvas"))
      throw Error("Wrong actual renderer " + renderer);
    const available = await p.evaluate(() => {
      const c = document.createElement("canvas");
      const q = c.getContext("webgl2") || c.getContext("webgl");
      return !!q;
    });
    if (!gl && available)
      throw Error("Controlled --disable-webgl was ineffective");
    const shots = [];
    for (const [name, x, y] of gl
      ? [
          ["heritage", 2176, 1328],
          ["namsan", 704, 3072],
          ["bora", 3728, 3152],
          ["coast", 2240, 3024],
          ["jeju", 1830, 4704],
        ]
      : [["no-webgl-fallback", 2176, 1328]]) {
      await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
      const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
      await p.waitForFunction(
        (n) => window.__PIXEL_METRICS__.frameCount > n + 4,
        n,
      );
      const bytes = await p.locator("canvas").screenshot();
      await fs.writeFile(
        `${out}/${gl ? "webgl" : "canvas"}-${name}-native.png`,
        bytes,
      );
      shots.push({
        name,
        sha256: createHash("sha256").update(bytes).digest("hex"),
        state: await p.evaluate(() => window.__SEOUL__),
      });
    }
    await p.locator("canvas").focus();
    const y = await p.evaluate(() => window.__SEOUL__.y);
    await p.keyboard.down("ArrowDown");
    await p.waitForFunction((y) => window.__SEOUL__.y > y + 8, y, {
      timeout: 4000,
    });
    await p.keyboard.up("ArrowDown");
    results.push({
      renderer,
      controlledWebGLDisabled: !gl,
      webglContextAvailable: available,
      actualWalking: true,
      shots,
    });
  } finally {
    await b.close();
  }
}
if (errors.length || externalRequests.length)
  throw Error(JSON.stringify({ errors, externalRequests }));
await fs.writeFile(
  out + "/renderer-verification.json",
  JSON.stringify(
    {
      status: "PASS",
      method:
        "Actual native Chromium compositor PNGs in forced ANGLE software WebGL across5districts; separate browser with --disable-webgl proves automatic Canvas and real keyboard movement. Not hardware-GPU or physical-phone certification.",
      results,
      externalRequests,
      errors,
    },
    null,
    2,
  ) + "\n",
);
console.log(
  JSON.stringify({
    status: "PASS",
    results: results.map((r) => ({
      renderer: r.renderer,
      walking: r.actualWalking,
      shots: r.shots.length,
    })),
    errors,
  }),
);
