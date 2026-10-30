import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase3bb-hotfix/native";
await fs.mkdir(D, { recursive: true });
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
try {
  for (const [id, h, acc] of [
    ["juni", "kr-classic-bob", "kr-hair-ornament"],
    ["minjun", "kr-layered-cut", "kr-fashion-cap"],
    ["doyun", "kr-side-part", "kr-garden-hat"],
  ]) {
    const c = await b.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
    });
    await c.addInitScript(
      ({ id, h, acc }) => {
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        );
        localStorage.setItem(
          "korean-arena-appearance-preferences-v2",
          JSON.stringify({
            version: 2,
            selectedCharacterId: id,
            appearances: {
              [id]: {
                schemaVersion: 2,
                characterId: id,
                hairstyleId: h,
                outfitId: null,
                accessoryIds: [acc],
              },
            },
            presets: [],
          }),
        );
      },
      { id, h, acc },
    );
    const p = await c.newPage();
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?native&pixelAudit&renderer=canvas&entry=transition",
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 60000 },
    );
    for (const [action, view, key] of [
      ["walk", "front", "s"],
      ["walk", "back", "w"],
      ["walk", "left", "a"],
      ["walk", "right", "d"],
      ["run", "front", "s"],
      ["run", "back", "w"],
      ["run", "left", "a"],
      ["run", "right", "d"],
      ["wave", "front", "Space"],
      ["celebrate", "front", "c"],
    ]) {
      if (action === "wave" || action === "celebrate")
        await p.keyboard.press(key);
      else {
        if (action === "run") await p.keyboard.down("Shift");
        await p.keyboard.down(key);
      }
      const prefix = `${action}-${view}-`;
      const audit = await p.evaluate(
        (prefix) => window.__GATE3_PIXEL_POSE__(prefix, 6000),
        prefix,
      );
      if (!audit.matched) throw Error(id + " missing " + prefix);
      const file = `${id}-${action}-${view}.png`;
      await fs.writeFile(
        D + "/" + file,
        Buffer.from(audit.png.split(",")[1], "base64"),
      );
      delete audit.png;
      rows.push({ id, action, view, file, audit });
      await p.keyboard.up(key);
      await p.keyboard.up("Shift");
      await p.waitForFunction(
        () => window.__GATE3__.frame.startsWith("idle-"),
        {},
        { timeout: 6000 },
      );
    }
    await c.close();
  }
  await fs.writeFile(D + "/CAPTURES.json", JSON.stringify(rows, null, 2));
  console.log("30 genuine native POST_RENDER captures");
} finally {
  await b.close();
}
