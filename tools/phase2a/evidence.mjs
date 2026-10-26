import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2a",
  FULL = "/tmp/phase2a-native-full",
  BASE = "http://127.0.0.1:4325/3D-pharse5-/";
await fs.mkdir(FULL, { recursive: true });
const catalog = JSON.parse(
  await fs.readFile(
    "assets-src/characters/phase2a/cosmetics/catalog.json",
    "utf8",
  ),
);
const modes = [
  ...["ara", "doyun"].map((id) => ({
    name: id + "-default",
    id,
    appearance: {
      schemaVersion: 2,
      characterId: id,
      hairstyleId: null,
      outfitId: null,
      accessoryIds: [],
    },
  })),
  ...catalog.presets.map((p) => ({
    name: p.id,
    id: p.appearance.characterId,
    appearance: p.appearance,
    preset: p.id,
  })),
];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [],
  switches = [],
  errors = [];
const ready = (p) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
try {
  for (const mode of modes) {
    const c = await b.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
      recordVideo: {
        dir: "/tmp/phase2a-evidence-video",
        size: { width: 1280, height: 1000 },
      },
    });
    await c.addInitScript((id) => {
      if (!localStorage.getItem("korean-arena-player-preferences-v1"))
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        );
    }, mode.id);
    const p = await c.newPage();
    p.on("pageerror", (e) =>
      errors.push({ mode: mode.name, message: e.message }),
    );
    await p.goto(BASE + "?renderer=canvas&entry=transition");
    await ready(p);
    if (!(await p.locator("#character-open").isVisible()))
      await p.locator("#settings summary").click();
    await p.locator("#character-open").click();
    await p.locator("#character-selection").waitFor();
    const before = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
      visited: window.__GATE3__.visited,
    }));
    if (mode.preset)
      await p.locator("#appearance-preset").selectOption(mode.preset);
    else await p.locator(`[data-character="${mode.id}"]`).click();
    await p.locator('[data-action="walk"]').click();
    await p.waitForTimeout(450);
    await p.screenshot({
      path: `${D}/${mode.name}-studio-desktop.jpg`,
      type: "jpeg",
      quality: 85,
    });
    await p.locator("#character-confirm").click();
    await p.locator("#character-selection").waitFor({ state: "hidden" });
    await ready(p);
    await p.waitForFunction(
      (mode) =>
        window.__GATE3__.characterId === mode.id &&
        JSON.stringify(window.__GATE3__.appearance) ===
          JSON.stringify(mode.appearance),
      mode,
    );
    const after = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
      visited: window.__GATE3__.visited,
      appearance: window.__GATE3__.appearance,
      players: window.__GATE3__.playerSprites,
    }));
    if (
      JSON.stringify(before) !==
        JSON.stringify({ x: after.x, y: after.y, visited: after.visited }) ||
      after.players !== 1 ||
      JSON.stringify(after.appearance) !== JSON.stringify(mode.appearance)
    )
      throw Error("Studio transfer changed state " + mode.name);
    switches.push({ mode: mode.name, before, after });
    for (const action of ["idle", "walk", "run", "wave", "celebrate"])
      for (const [view, key] of ["wave", "celebrate"].includes(action)
        ? [["front", action === "wave" ? "Space" : "c"]]
        : [
            ["front", "s"],
            ["back", "w"],
            ["left", "a"],
            ["right", "d"],
          ]) {
        const prefix = `${action}-${view}-`;
        await p.goto(
          BASE +
            `?native&pixelAudit&renderer=canvas&entry=transition&phase2a=${mode.name}-${prefix}`,
        );
        await ready(p);
        await p
          .locator("#stage canvas")
          .click({ position: { x: 640, y: 450 } });
        await p.evaluate(() => {
          window.__P2_TRACE__ = [];
          const sample = () => {
            const a = window.__GATE3__;
            window.__P2_TRACE__.push({
              x: a.x,
              y: a.y,
              frame: a.frame,
              id: a.characterId,
              appearance: a.appearance,
              players: a.playerSprites,
              sampling: a.samplingMode,
              ready: a.ready,
            });
            window.__P2_TIMER__ = requestAnimationFrame(sample);
          };
          window.__P2_TIMER__ = requestAnimationFrame(sample);
        });
        if (action === "idle") {
          await p.keyboard.down(key);
          await p.waitForTimeout(200);
          await p.keyboard.up(key);
          await p.waitForFunction(
            (prefix) => window.__GATE3__.frame.startsWith(prefix),
            prefix,
          );
        } else if (["wave", "celebrate"].includes(action))
          await p.keyboard.press(key);
        else {
          if (action === "run") await p.keyboard.down("Shift");
          await p.keyboard.down(key);
        }
        const audit = await p.evaluate(
          (prefix) => window.__GATE3_PIXEL_POSE__(prefix, 4000),
          prefix,
        );
        if (!audit.matched)
          throw Error("Missing real pose " + mode.name + prefix);
        const file = `${mode.name}-${action}-${view}-phaser-native.png`,
          bytes = Buffer.from(audit.png.split(",")[1], "base64");
        delete audit.png;
        await fs.writeFile(`${FULL}/${file}`, bytes);
        if (action === "walk" && view === "front")
          await fs.writeFile(`${D}/${file}`, bytes);
        await p.waitForFunction(
          ({ prefix, count }) =>
            new Set(
              window.__P2_TRACE__
                .map((r) => r.frame)
                .filter((f) => f.startsWith(prefix)),
            ).size >= count,
          { prefix, count: action === "idle" ? 2 : 8 },
          { timeout: 12000 },
        );
        await p.waitForTimeout(150);
        await p.keyboard.up(key);
        await p.keyboard.up("Shift");
        const trace = await p.evaluate(() => {
          window.cancelAnimationFrame(window.__P2_TIMER__);
          return window.__P2_TRACE__;
        });
        const frames = [
          ...new Set(
            trace.map((r) => r.frame).filter((f) => f.startsWith(prefix)),
          ),
        ];
        if (["walk", "run"].includes(action) && frames.length !== 8)
          throw Error(
            `Incomplete real gait ${mode.name} ${prefix} ${frames.length}`,
          );
        if (
          trace.some(
            (t) =>
              t.id !== mode.id ||
              t.players !== 1 ||
              t.sampling !== 1 ||
              JSON.stringify(t.appearance) !== JSON.stringify(mode.appearance),
          )
        )
          throw Error("Actor/appearance drift " + mode.name);
        rows.push({
          mode: mode.name,
          id: mode.id,
          action,
          view,
          file,
          sourcePath: `${FULL}/${file}`,
          audit,
          observedFrames: frames,
          trace,
        });
        await fs.writeFile(
          `${D}/actual-gameplay-working.json`,
          JSON.stringify({ modes, rows, switches, errors }, null, 2),
        );
        console.log(mode.name, prefix, frames.length);
      }
    const video = p.video();
    await c.close();
    await video.saveAs(`${D}/${mode.name}-actual-gameplay.webm`);
  }
  await fs.writeFile(
    `${D}/actual-gameplay.json`,
    JSON.stringify(
      {
        method:
          "Real production Phaser build, original WASD/Shift/Space/C. Studio item application through actual UI. Native POST_RENDER backing PNGs, zoom1. Each review entry navigates to the declared free path, never teleports or forces frames. Full originals retained under /tmp/phase2a-native-full; native crops and selected full PNGs delivered separately.",
        modes,
        rows,
        switches,
        errors,
        physicalDevices: "NOT TESTED",
        humanPhase2AApproval: "PENDING",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(JSON.stringify(errors));
} finally {
  await b.close();
}
