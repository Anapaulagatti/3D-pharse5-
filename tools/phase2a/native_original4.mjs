import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2a",
  base = "http://127.0.0.1:4325/3D-pharse5-/",
  key = "korean-arena-player-preferences-v1";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [],
  errors = [];
try {
  for (const renderer of ["canvas", "webgl"]) {
    const ctx = await browser.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
    });
    await ctx.addInitScript(
      (key) =>
        localStorage.setItem(
          key,
          JSON.stringify({ version: 1, characterId: "juni" }),
        ),
      key,
    );
    const p = await ctx.newPage();
    p.on("pageerror", (e) => errors.push(e.message));
    for (const entry of [
      "palace-front-local",
      "station-all",
      "bridge-a-full",
    ]) {
      await p.goto(
        base + `?native&pixelAudit&renderer=${renderer}&entry=${entry}`,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      const file = `regression-${entry}-${renderer}-native-1x.png`;
      await fs.writeFile(
        `${D}/${file}`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      rows.push({ entry, renderer, file, audit: a });
    }
    await ctx.close();
  }
  for (const id of ["juni", "haneul", "bomi", "minjun"]) {
    const ctx = await browser.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
    });
    await ctx.addInitScript(
      ({ key, id }) =>
        localStorage.setItem(
          key,
          JSON.stringify({ version: 1, characterId: id }),
        ),
      { key, id },
    );
    const p = await ctx.newPage();
    await p.goto(base + "?native&pixelAudit&renderer=canvas&entry=station-all");
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    const file = `${id}-complete-station-frontage-native-1x.png`;
    await fs.writeFile(
      `${D}/${file}`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    rows.push({ id, entry: "station-all", renderer: "canvas", file, audit: a });
    await ctx.close();
  }
  await fs.writeFile(
    `${D}/native-regression.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser POST_RENDER backing PNGs, zoom1, integer camera and nearest textures. Same canonical native entries/camera as accepted Phase1. Character bodies are real single-player renders; source lineup is separately labelled.",
        rows,
        errors,
        physicalDevices: "NOT TESTED",
        webgl:
          "Software-rendered smoke evidence only; no hardware performance claim",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join(";"));
} finally {
  await browser.close();
}
