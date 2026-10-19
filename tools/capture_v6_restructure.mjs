import { chromium } from "playwright";
import fs from "node:fs/promises";
import crypto from "node:crypto";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const out = "docs/v6-restructure/quality";
await fs.mkdir(out, { recursive: true });
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [],
  shots = [];
function monitor(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
}
async function stable(p) {
  const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount > n + 4,
    n,
  );
}
async function snap(p, name) {
  const s = await p
    .locator("canvas")
    .evaluate((c) => ({ data: c.toDataURL(), size: [c.width, c.height] }));
  const data = Buffer.from(s.data.split(",")[1], "base64");
  await fs.writeFile(`${out}/${name}.png`, data);
  shots.push({
    name,
    native: s.size,
    sha256: crypto.createHash("sha256").update(data).digest("hex"),
    state: await p.evaluate(() => window.__SEOUL__),
  });
}
const poses = [
  ["transition", 2176, 2560],
  ["station", 2240, 3024],
  ["retail", 2240, 3536],
  ["promenade", 2496, 3744],
  ["bloom-spine", 3728, 3152],
  ["bloom-entry", 3552, 3576],
  ["namsan", 704, 3072],
  ["heritage", 1568, 1292],
  ["jeju", 1830, 4704],
];

try {
  for (const [version, entry] of [
    ["before", "v4-readability-review.html"],
    ["after", "v6-world-review.html"],
  ]) {
    const c = await b.newContext({
      viewport: { width: 1440, height: 1140 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const p = await c.newPage();
    monitor(p);
    await p.goto(base + entry + "?qa&renderer=canvas");
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    for (const [name, x, y] of poses) {
      await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
      await stable(p);
      await snap(p, version + "-" + name + "-native");
    }
    await c.close();
    const oc = await b.newContext({
      viewport: { width: 4352, height: version === "after" ? 5312 : 4800 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const op = await oc.newPage();
    monitor(op);
    await op.goto(base + entry + "?overview&renderer=canvas");
    await op.waitForFunction(() => window.__SEOUL__?.ready);
    await stable(op);
    await snap(op, version + "-full-map-native");
    await oc.close();
  }
  for (const [name, width, height] of [
    ["mobile", 844, 390],
    ["small-mobile", 568, 320],
    ["wide-mobile", 932, 430],
  ]) {
    const c = await b.newContext({
      viewport: { width, height },
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const p = await c.newPage();
    monitor(p);
    await p.goto(base + "v6-world-review.html?qa&renderer=canvas");
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    await p.evaluate(() => window.__SEOUL_TEST__.place(2240, 3536));
    await stable(p);
    await snap(p, name + "-native");
    await p.screenshot({ path: out + "/" + name + "-interface.png" });
    if (name === "mobile") {
      await p.setViewportSize({ width: 390, height: 844 });
      await p.locator("#rotate-screen").waitFor({ state: "visible" });
      await p.screenshot({ path: out + "/portrait-interface.png" });
    }
    await c.close();
  }
  const nb = await fs.readFile(`${out}/before-heritage-native.png`);
  const na = await fs.readFile(`${out}/after-heritage-native.png`);
  if (!nb.equals(na)) throw Error("Northern native pixels changed");
  if (errors.length) throw Error(JSON.stringify(errors));
  await fs.writeFile(
    out + "/stills.json",
    JSON.stringify(
      {
        method:
          "Actual Phaser native Canvas and mobile browser captures. Identical before/after entry resolution/camera/root poses; still QA placement only, not gameplay motion. Full world is one4352x5312engine frame (V4 before4352x4800). Northern native capture bytes equal; Jeju intentionally moved+320Y. No rendered pixels repainted or resized. Physical phone unmeasured.",
        shots,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    JSON.stringify({
      nativeShots: shots.length,
      protectedNorthernNativeAreaEqual: true,
      errors,
    }),
  );
} finally {
  await b.close();
}
