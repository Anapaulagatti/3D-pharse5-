import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [],
  errors = [];
try {
  for (const [id, hairstyleId, accessoryIds] of [
    ["juni", "kr-classic-bob", ["kr-hair-ornament"]],
    ["minjun", "kr-layered-cut", ["kr-fashion-cap"]],
    ["doyun", "kr-side-part", ["kr-garden-hat"]],
    ["sori", "kr-classic-bob", ["kr-hair-ornament"]],
  ]) {
    const c = await b.newContext({
      viewport: { width: 960, height: 640 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
      recordVideo: {
        dir: "/tmp/phase3bb-custom-motion",
        size: { width: 960, height: 640 },
      },
    });
    await c.addInitScript(
      ({ id, hairstyleId, accessoryIds }) => {
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
                hairstyleId,
                outfitId: null,
                accessoryIds,
              },
            },
            presets: [],
          }),
        );
      },
      { id, hairstyleId, accessoryIds },
    );
    const p = await c.newPage();
    p.on("pageerror", (e) => errors.push(e.message));
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?renderer=canvas&entry=transition",
    );
    await p.waitForFunction(
      (id) =>
        window.__GATE3__?.ready &&
        window.__GATE3__.characterId === id &&
        window.__GATE3__.chunks.inflight === 0,
      id,
      { timeout: 60000 },
    );
    const look = await p.evaluate(() => window.__GATE3__.appearance);
    if (
      look.hairstyleId !== hairstyleId ||
      look.accessoryIds[0] !== accessoryIds[0]
    )
      throw Error("Cosmetic silently missing " + JSON.stringify(look));
    const trace = [];
    const cases = [
      ["start-right", ["d"]],
      ["add-up", ["d", "w"]],
      ["reverse-left", ["a"]],
      ["up", ["w"]],
      ["down", ["s"]],
      ["run", ["Shift", "d"]],
      ["run-turn", ["Shift", "w"]],
      ["diagonal-run", ["Shift", "w", "a"]],
    ];
    let held = [];
    for (const [name, keys] of cases) {
      for (const k of held) if (!keys.includes(k)) await p.keyboard.up(k);
      for (const k of keys) if (!held.includes(k)) await p.keyboard.down(k);
      held = keys;
      await p.waitForTimeout(230);
      const s = await p.evaluate(() => window.__GATE3__);
      if (
        s.camera.lookAhead.some((v) => v !== 0) ||
        s.playerSprites !== 1 ||
        s.samplingMode !== 1
      )
        throw Error("Camera/duplicate/sampling regression");
      trace.push({
        scenario: name,
        x: s.x,
        y: s.y,
        frame: s.frame,
        camera: s.camera,
        appearance: s.appearance,
      });
    }
    for (const k of held) await p.keyboard.up(k);
    await p.keyboard.press("Space");
    await p.waitForTimeout(300);
    await p.screenshot({
      path: `docs/phase3bb-hotfix/${id}-custom-gameplay-native.png`,
    });
    const pos = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
    }));
    await p.reload();
    await p.waitForFunction(() => window.__GATE3__?.ready);
    const restored = await p.evaluate(() => window.__GATE3__.appearance);
    if (JSON.stringify(restored) !== JSON.stringify(look))
      throw Error("Appearance persistence changed");
    const v = p.video();
    await c.close();
    await v.saveAs(`docs/phase3bb-hotfix/${id}-custom-gameplay.webm`);
    rows.push({ id, look, trace, restored, positionBeforeReload: pos });
  }
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    "docs/phase3bb-hotfix/MOVEMENT_MATRIX.json",
    JSON.stringify(
      {
        status: "PASS ACTUAL PHASER INPUT/COSMETIC MATRIX",
        rows,
        errors,
        physicalDevices: "NOT TESTED",
        artisticAcceptance: "PENDING",
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
