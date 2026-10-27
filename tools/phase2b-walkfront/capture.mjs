import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const ids = process.argv.slice(2);
if (!ids.length) throw Error("Choose inspected motion candidates");
const D = "docs/phase2b-motion/walk-front",
  FULL = "/tmp/phase2b-walkfront-native";
await fs.mkdir(FULL, { recursive: true });
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const all = [];
const ready = (p) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
try {
  for (const id of ids) {
    const c = await b.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
      recordVideo: {
        dir: "/tmp/phase2b-walkfront-video",
        size: { width: 1280, height: 1000 },
      },
    });
    await c.addInitScript((id) => {
      if (!localStorage.getItem("korean-arena-player-preferences-v1"))
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        );
    }, id);
    const p = await c.newPage(),
      rows = [],
      errors = [];
    p.on("pageerror", (e) => errors.push(e.message));
    await p.goto(
      "http://127.0.0.1:4320/3D-pharse5-/?renderer=canvas&entry=transition",
    );
    await ready(p);
    await p.locator("#settings summary").click({ noWaitAfter: true });
    await p.locator("#character-open").click({ noWaitAfter: true });
    await p.locator(`[data-character="${id}"]`).click({ noWaitAfter: true });
    await p.locator('[data-action="walk"]').click({ noWaitAfter: true });
    await p.screenshot({
      path: `${D}/${id}-studio-browser.jpg`,
      type: "jpeg",
      quality: 80,
    });
    await p.locator("#character-confirm").click({ noWaitAfter: true });
    await p.locator("#character-selection").waitFor({ state: "hidden" });
    await ready(p);
    for (const action of ["walk"])
      for (const [view, key] of [["front", "s"]]) {
        const clip = action + "-" + view;
        await p.goto(
          `http://127.0.0.1:4320/3D-pharse5-/?native&renderer=canvas&pixelAudit&entry=transition&motion=${id}-${clip}`,
        );
        await ready(p);
        await p
          .locator("#stage canvas")
          .click({ position: { x: 640, y: 450 } });
        const start = await p.evaluate(() => ({
          x: window.__GATE3__.x,
          y: window.__GATE3__.y,
          id: window.__GATE3__.characterId,
          visited: window.__GATE3__.visited,
        }));
        if (start.id !== id) throw Error("Wrong identity");
        await p.evaluate(() => {
          window.__MOTION_TRACE__ = [];
          const read = () => {
            const s = window.__GATE3__;
            window.__MOTION_TRACE__.push({
              t: performance.now(),
              x: s.x,
              y: s.y,
              frame: s.frame,
              players: s.playerSprites,
              sampling: s.samplingMode,
            });
            window.__MOTION_TRACE_ID__ = requestAnimationFrame(read);
          };
          window.__MOTION_TRACE_ID__ = requestAnimationFrame(read);
        });
        if (action === "run") await p.keyboard.down("Shift");
        await p.keyboard.down(key);
        const warm = await p.evaluate(
          (prefix) => window.__GATE3_PIXEL_POSE__(prefix + "7", 6000),
          clip + "-",
        );
        if (!warm.matched) throw Error("No actual gait " + id + clip);
        const samples = [];
        const cycles = await p.evaluate(async (prefix) => {
          const cycles = [];
          for (let loop = 0; loop < 3; loop++) {
            const zero = await window.__GATE3_PIXEL_POSE__(prefix + "0", 6000);
            const rest = await Promise.all(
              Array.from({ length: 7 }, (_, i) =>
                window.__GATE3_PIXEL_POSE__(prefix + (i + 1), 6000),
              ),
            );
            cycles.push([zero, ...rest]);
          }
          return cycles;
        }, clip + "-");
        for (let loop = 0; loop < 3; loop++)
          for (let i = 0; i < 8; i++) {
            const a = cycles[loop][i];
            if (
              !a.matched ||
              a.state.characterId !== id ||
              a.actualFrame !== clip + "-" + i
            )
              throw Error("Missing actual native phase " + id + clip + i);
            const file = `${id}-${clip}-loop${loop}-${i}.png`;
            await fs.writeFile(
              FULL + "/" + file,
              Buffer.from(a.png.split(",")[1], "base64"),
            );
            delete a.png;
            samples.push({
              loop,
              index: i,
              file,
              sourcePath: FULL + "/" + file,
              audit: a,
            });
          }
        // Observe actual stop and a right-to-left turn without any forced frame/state.
        let stop = null,
          turn = null;
        if (view === "right")
          await p.evaluate(() => {
            window.__MOTION_STOP__ = window.__GATE3_PIXEL_POSE__(
              "stop-right-",
              4000,
            );
          });
        await p.keyboard.up(key);
        await p.keyboard.up("Shift");
        if (view === "right") {
          stop = await p.evaluate(() => window.__MOTION_STOP__);
          if (!stop.matched) throw Error("Right stop not observed");
          await fs.writeFile(
            `${D}/${id}-${action}-right-stop-native.png`,
            Buffer.from(stop.png.split(",")[1], "base64"),
          );
          delete stop.png;
        }
        await p.waitForFunction(
          (view) => window.__GATE3__.frame.startsWith("idle-" + view),
          view,
        );
        const end = await p.evaluate(() => ({
          x: window.__GATE3__.x,
          y: window.__GATE3__.y,
          frame: window.__GATE3__.frame,
          players: window.__GATE3__.playerSprites,
        }));
        if (view === "right") {
          await p.evaluate(
            (prefix) => {
              window.__MOTION_TURN__ = window.__GATE3_PIXEL_POSE__(
                prefix,
                3000,
              );
            },
            id === "juni" ? "turn-" : "idle-front-",
          );
          await p.keyboard.down("a");
          turn = await p.evaluate(() => window.__MOTION_TURN__);
          await p.waitForTimeout(350);
          await p.keyboard.up("a");
          if (!turn.matched) throw Error("Real turn not observed");
          await fs.writeFile(
            `${D}/${id}-${action}-right-turn-native.png`,
            Buffer.from(turn.png.split(",")[1], "base64"),
          );
          delete turn.png;
        }
        const trace = await p.evaluate(() => {
          window.cancelAnimationFrame(window.__MOTION_TRACE_ID__);
          return window.__MOTION_TRACE__;
        });
        const stride = action === "walk" ? 44 : 64;
        for (let loop = 0; loop < 3; loop++) {
          const ss = samples.filter((s) => s.loop === loop);
          const distances = ss.map((s) =>
            Math.hypot(s.audit.state.x - start.x, s.audit.state.y - start.y),
          );
          if (distances.some((v, i) => i && v <= distances[i - 1]))
            throw Error(
              "Phase samples not consecutive actual movement " + id + clip,
            );
          if (distances[7] - distances[0] > stride * 1.2)
            throw Error("Skipped gait cycle " + id + clip);
        }
        for (let loop = 1; loop < 3; loop++) {
          const x = samples.find((s) => s.loop === loop && s.index === 0).audit
              .state,
            y = samples.find((s) => s.loop === loop - 1 && s.index === 0).audit
              .state;
          // Index0 is a sample anywhere inside its 1/8-stride interval,
          // not its exact boundary. Two index0 samples can differ by up to
          // one frame interval; a skipped loop is nearly two whole strides.
          const delta = Math.hypot(x.x - y.x, x.y - y.y);
          if (Math.abs(delta - stride) > stride / 8 + 0.01) {
            await fs.writeFile(
              `${D}/${id}-${clip}-capture-failure.json`,
              JSON.stringify({ stride, delta, samples, trace }, null, 2),
            );
            throw Error(
              "Non-consecutive loops " + id + clip + " delta=" + delta,
            );
          }
        }
        if (view === "right" && end.x <= start.x + stride * 3)
          throw Error("Missing positive X traversal");
        if (trace.some((s) => s.players !== 1 || s.sampling !== 1))
          throw Error("Actor/filter drift");
        const row = {
          id,
          clip,
          action,
          view,
          start,
          end,
          samples,
          trace,
          stop,
          turn,
          method:
            "Three consecutive complete cycles sampled on actual Phaser POST_RENDER from real input at unchanged60/100speed. Declared review spawn before each clip; no in-movement teleport or forced pose.",
        };
        rows.push(row);
        await fs.writeFile(
          `${D}/${id}-gameplay-working.json`,
          JSON.stringify({ id, rows, errors }, null, 2),
        );
        console.log(
          id,
          clip,
          "3 consecutive8-pose loops",
          Math.round(end.x - start.x),
          Math.round(end.y - start.y),
        );
      }
    const video = p.video();
    await c.close();
    await video.saveAs(`${D}/${id}-actual-gameplay.webm`);
    if (errors.length) throw Error(errors.join("\n"));
    const q = {
      id,
      rows,
      errors,
      source:
        "Actual canonical Phaser, input-controlled, unretimed raw recording. Native pixel PNGs preserved separately.",
      physicalDevices: "NOT TESTED",
      humanMotionApproval: "PENDING",
    };
    await fs.writeFile(`${D}/${id}-gameplay.json`, JSON.stringify(q, null, 2));
    all.push(q);
  }
} finally {
  await b.close();
}
