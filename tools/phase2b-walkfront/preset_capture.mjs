import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2b-motion/walk-front",
  O = "/tmp/phase2b-walkfront-presets";
await fs.mkdir(O, { recursive: true });
const catalog = JSON.parse(
  await fs.readFile(
    "assets-src/characters/phase2a/cosmetics/catalog.json",
    "utf8",
  ),
);
const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  }),
  rows = [];
try {
  for (const preset of catalog.presets) {
    const id = preset.appearance.characterId,
      c = await b.newContext({
        viewport: { width: 1280, height: 1000 },
        deviceScaleFactor: 1,
      });
    await c.addInitScript(
      (id) =>
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        ),
      id,
    );
    const p = await c.newPage();
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?renderer=canvas&pixelAudit&entry=transition",
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.locator("#settings summary").click();
    await p.locator("#character-open").click();
    await p.locator("#appearance-preset").selectOption(preset.id);
    await p.locator("#character-confirm").click();
    await p.waitForFunction(
      (outfit) =>
        window.__GATE3__.appearance.outfitId === outfit &&
        window.__GATE3__.ready,
      preset.appearance.outfitId,
    );
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?native&renderer=canvas&pixelAudit&entry=transition",
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.locator("#stage canvas").click({ position: { x: 640, y: 450 } });
    await p.keyboard.down("s");
    await p.evaluate(() => window.__GATE3_PIXEL_POSE__("walk-front-7", 6000));
    const samples = await p.evaluate(async () => {
      const zero = await window.__GATE3_PIXEL_POSE__("walk-front-0", 6000);
      const rest = await Promise.all(
        Array.from({ length: 7 }, (_, i) =>
          window.__GATE3_PIXEL_POSE__(`walk-front-${i + 1}`, 6000),
        ),
      );
      return [zero, ...rest];
    });
    await p.keyboard.up("s");
    for (let i = 0; i < samples.length; i++) {
      const a = samples[i];
      if (!a.matched || a.actualFrame !== `walk-front-${i}`)
        throw Error("Preset capture phase");
      const sourcePath = `${O}/${preset.id}-${i}.png`;
      await fs.writeFile(
        sourcePath,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      rows.push({ preset: preset.id, index: i, sourcePath, audit: a });
    }
    await c.close();
    console.log(preset.id, "actual8 walk-front phases");
  }
  await fs.writeFile(
    `${D}/preset-gameplay.json`,
    JSON.stringify(rows, null, 2),
  );
} finally {
  await b.close();
}
