import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2a",
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
const ctx = await browser.newContext({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
  recordVideo: {
    dir: "/tmp/ara-pilot-video",
    size: { width: 1280, height: 1000 },
  },
});
await ctx.addInitScript(() =>
  localStorage.setItem(
    "korean-arena-player-preferences-v1",
    JSON.stringify({ version: 1, characterId: "ara" }),
  ),
);
const p = await ctx.newPage(),
  rows = [];
try {
  for (const action of ["walk", "run"])
    for (const [view, key] of [
      ["front", "s"],
      ["back", "w"],
      ["left", "a"],
      ["right", "d"],
    ]) {
      const prefix = `${action}-${view}-`;
      await p.goto(
        "http://127.0.0.1:4320/3D-pharse5-/?native&pixelAudit&renderer=canvas&entry=transition&pilot=" +
          prefix,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      await p
        .locator("canvas")
        .first()
        .click({ position: { x: 640, y: 450 } });
      if (action === "run") await p.keyboard.down("Shift");
      await p.keyboard.down(key);
      const a = await p.evaluate(
        (prefix) => window.__GATE3_PIXEL_POSE__(prefix, 4000),
        prefix,
      );
      if (!a.matched || a.state.characterId !== "ara")
        throw Error("Ara missing actual gait");
      await fs.writeFile(
        `${D}/ara-pilot-${action}-${view}-native.png`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      await p.waitForTimeout(850);
      await p.keyboard.up(key);
      await p.keyboard.up("Shift");
      rows.push({ clip: prefix, audit: a });
      console.log(prefix, "PASS");
    }
  await fs.writeFile(
    `${D}/ara-pilot-gameplay.json`,
    JSON.stringify(
      {
        rows,
        source:
          "Actual input-driven native Phaser pilot inspected before Doyun authoring",
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  const v = p.video();
  await ctx.close();
  await v.saveAs(`${D}/ara-pilot-actual.webm`);
} finally {
  await browser.close();
}
