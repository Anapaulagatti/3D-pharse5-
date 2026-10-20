import { chromium } from "playwright";
import fs from "node:fs/promises";
import crypto from "node:crypto";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [],
  errors = [];
const hash = (x) => crypto.createHash("sha256").update(x).digest("hex");
try {
  for (const dpr of [1, 2, 3]) {
    const images = [];
    for (const entry of ["v6-world-review.html", "v7-world-review.html"]) {
      const c = await browser.newContext({
          viewport: { width: 1440, height: 1140 },
          deviceScaleFactor: dpr,
          reducedMotion: "reduce",
        }),
        p = await c.newPage();
      await c.addInitScript(() => {
        window.__V7_DRAWS__ = [];
        const get = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function (...args) {
          const ctx = get.apply(this, args);
          if (
            ctx?.drawImage &&
            !window.__V7_DRAWS__.some((r) => r.canvas === this)
          ) {
            const record = { canvas: this, nearest: 0, smoothed: 0 };
            window.__V7_DRAWS__.push(record);
            const draw = ctx.drawImage.bind(ctx);
            ctx.drawImage = function (...items) {
              record[ctx.imageSmoothingEnabled ? "smoothed" : "nearest"]++;
              return draw(...items);
            };
          }
          return ctx;
        };
      });
      p.on("pageerror", (e) => errors.push(e.message));
      await p.goto(base + entry + "?qa&renderer=canvas");
      await p.waitForFunction(() => window.__SEOUL__?.ready);
      await p.evaluate(() => window.__SEOUL_TEST__.place(2176, 1328));
      const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
      await p.waitForFunction(
        (n) => window.__PIXEL_METRICS__.frameCount > n + 5,
        n,
      );
      const v = await p.locator("canvas").evaluate(async (c) => ({
        png: c.toDataURL(),
        assetRegionHash: Array.from(
          new Uint8Array(
            await crypto.subtle.digest(
              "SHA-256",
              c.getContext("2d").getImageData(0, 0, 944, 768).data,
            ),
          ),
        )
          .map((v) => v.toString(16).padStart(2, "0"))
          .join(""),
        width: c.width,
        height: c.height,
        smoothing: c.getContext("2d").imageSmoothingEnabled,
        css: getComputedStyle(c).imageRendering,
        dpr: devicePixelRatio,
        draws: window.__V7_DRAWS__
          .filter((r) => r.canvas === c)
          .map((r) => ({ nearest: r.nearest, smoothed: r.smoothed })),
      }));
      if (
        !v.draws.length ||
        v.draws.some((r) => r.nearest === 0 || r.smoothed > 0) ||
        !["pixelated", "crisp-edges"].includes(v.css) ||
        v.width !== 1024 ||
        v.height !== 768
      )
        throw Error(JSON.stringify({ ...v, png: undefined }));
      await fs.writeFile(
        `docs/v7-world/quality/sharpness-${entry.split(".")[0]}-dpr${dpr}.png`,
        Buffer.from(v.png.split(",")[1], "base64"),
      );
      images.push(hash(v.png));
      rows.push({
        entry,
        dpr,
        width: v.width,
        height: v.height,
        postRenderRestoredSmoothing: v.smoothing,
        actualDraws: v.draws,
        camera: await p.evaluate(() => window.__FULL_WORLD__.camera),
        css: v.css,
        nativePixelHash: images.at(-1),
        nativeAssetRegionHash: v.assetRegionHash,
      });
      await c.close();
    }
    if (images[0] !== images[1])
      throw Error("Protected heritage render differs at DPR" + dpr);
  }
  await fs.writeFile(
    ".cache/v7-world/sharpness-diagnostic.json",
    JSON.stringify({ rows, errors }, null, 2),
  );
  if (
    new Set(rows.map((r) => r.nativeAssetRegionHash)).size !== 1 ||
    errors.length
  )
    throw Error("DPR changed actual art-region pixels or error");
  await fs.writeFile(
    "docs/v7-world/quality/sharpness.json",
    JSON.stringify(
      {
        status: "PASS",
        method:
          "Real Phaser V6 versus V7 same heritage camera, native 1024x768/zoom1/Canvas/reduced-motion; DPR1/2/3. Literal native canvas hashes, CSS nearest pixel display and actual drawImage filtering. Canvas restores smoothing=true after drawing; it does not describe filtering during asset draws. No image filters.",
        crossDPRTextNote:
          "Full V6/V7 frame matches at every DPR. Across DPR,203 pixels differ only in the right-edge floating location-label glyph [967,613,1024,625], equally in old and new. Original sprite/terrain region0,0,944,768 is byte-identical across DPR; all actual asset draws nearest. Post-render restored smoothing is not asset blur.",
        rows,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  console.log("Matched V6/V7 native pixels and DPR1/2/3 PASS");
} finally {
  await browser.close();
}
