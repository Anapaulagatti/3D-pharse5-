import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2b/bridge-regression",
  plan = JSON.parse(await fs.readFile(`${D}/walk-plan.json`, "utf8")),
  legs = [],
  samples = [],
  errors = [];
const interactions = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const ctx = await b.newContext({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
  hasTouch: true,
  recordVideo: {
    dir: "/tmp/phase2b-bridge-video",
    size: { width: 1280, height: 1000 },
  },
});
await ctx.addInitScript(() =>
  localStorage.setItem(
    "korean-arena-player-preferences-v1",
    JSON.stringify({
      version: 1,
      characterId: new window.URLSearchParams(window.location.search)
        .get("entry")
        ?.startsWith("bridge-b")
        ? "hyunwoo"
        : "nari",
    }),
  ),
);
const recordingRequestedAt = Date.now();
const p = await ctx.newPage();
p.on("pageerror", (e) => errors.push(e.message));
let held = null;
const movingShots = [],
  poseShots = [],
  poseRequests = [];
let posePending = null;
function armPose(prefix, tag) {
  const stem = tag.replace(/-(stop|turn)$/, "");
  if (posePending || poseShots.filter((a) => a.leg === stem).length >= 4)
    return;
  const requestedAt = Date.now();
  posePending = p
    .evaluate((prefix) => window.__GATE3_PIXEL_POSE__(prefix, 4000), prefix)
    .then(async (a) => {
      poseRequests.push({
        prefix,
        leg: stem,
        requestedAt,
        matched: a.matched,
        actualFrame: a.actualFrame,
      });
      if (a.matched) {
        const name = `pose-${String(poseShots.length + 1).padStart(2, "0")}-${tag}-native`;
        await fs.writeFile(
          `${D}/${name}.png`,
          Buffer.from(a.png.split(",")[1], "base64"),
        );
        delete a.png;
        poseShots.push({ name, leg: stem, ...a });
      }
    })
    .catch((e) => errors.push("POSE_OBSERVE: " + e.message))
    .finally(() => {
      posePending = null;
    });
}
const touch = await ctx.newCDPSession(p);
let touching = false;
async function stopTouch() {
  if (touching)
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
  touching = false;
}
async function fineTouch(axis, direction, strength) {
  const box = await p.locator("#joystick").boundingBox();
  if (!box) throw Error("Native joystick unavailable for real fine input");
  const x = box.x + box.width / 2,
    y = box.y + box.height / 2;
  if (!touching) {
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x, y, id: 1 }],
    });
    touching = true;
  }
  const d = box.width * 0.34 * (0.14 + 0.86 * strength) * direction;
  await touch.send("Input.dispatchTouchEvent", {
    type: "touchMove",
    touchPoints: [
      { x: x + (axis === "x" ? d : 0), y: y + (axis === "y" ? d : 0), id: 1 },
    ],
  });
}
function record(s) {
  samples.push({
    t: Date.now(),
    characterId: s.characterId,
    x: s.x,
    y: s.y,
    ready: s.ready,
    chunks: s.chunks,
    session: s.session,
    frame: s.frame,
    behind: s.behind,
    leg: plan.legs[legs.length]?.id,
    input: touching ? "native joystick" : "WASD",
  });
}

async function up() {
  if (held) await p.keyboard.up(held);
  held = null;
}
async function axis(axis, target) {
  const end = Date.now() + 90000;
  let last = Date.now(),
    prior = null;
  while (Date.now() < end) {
    const s = await p.evaluate(() => window.__GATE3__);
    const d = target - s[axis];
    if (Math.abs(d) <= 4) {
      if (
        held &&
        (plan.legs[legs.length]?.id.includes("bridge") ||
          plan.legs[legs.length]?.id.includes("jeju"))
      )
        armPose("stop-", `${plan.legs[legs.length].id}-stop`);
      await up();
      record(s);
      if (Math.abs(s[axis] - target) <= 0.3) {
        await stopTouch();
        await p.waitForTimeout(70);
        const settled = await p.evaluate(() => window.__GATE3__);
        if (Math.abs(settled[axis] - target) <= 0.3) return;
        continue;
      }
      await fineTouch(axis, d > 0 ? 1 : -1, Math.abs(d) < 1.5 ? 0.05 : 0.1);
      if (prior === null || Math.abs(s[axis] - prior) > 0.1) {
        last = Date.now();
        prior = s[axis];
      }
      if (Date.now() - last > 5500)
        throw Error(
          `Real input stalled ${axis} at${s.x},${s.y},target${target}`,
        );
      await p.waitForTimeout(40);
      await stopTouch();
      await p.waitForTimeout(100);
      continue;
    }
    await stopTouch();
    const key = axis === "x" ? (d > 0 ? "d" : "a") : d > 0 ? "s" : "w";
    if (key !== held) {
      await up();
      if (
        plan.legs[legs.length]?.id.includes("bridge") ||
        plan.legs[legs.length]?.id.includes("jeju")
      )
        armPose("turn-", `${plan.legs[legs.length].id}-turn`);
      await p.keyboard.down(key);
      held = key;
    }
    if (prior === null || Math.abs(s[axis] - prior) > 0.2) {
      last = Date.now();
      prior = s[axis];
    }
    if (Date.now() - last > 4500)
      throw Error(`Stalled ${axis} target${target} at${s.x},${s.y}`);
    if (
      plan.legs[legs.length]?.id === "complete-bridge-to-jeju" &&
      axis === "x" &&
      Math.abs(d) > 15 &&
      movingShots.length < 4 &&
      s.x >= [3180, 3250, 3350, 3450][movingShots.length]
    ) {
      const a = await p.evaluate(() =>
        window
          .__GATE3_PIXEL_AUDIT__()
          .then((a) => ({ ...a, state: window.__GATE3__ })),
      );
      const name = `bridge-moving-${movingShots.length + 1}-native`;
      await fs.writeFile(
        `${D}/${name}.png`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      movingShots.push({ name, ...a });
    }
    samples.push({
      t: Date.now(),
      characterId: s.characterId,
      x: s.x,
      y: s.y,
      ready: s.ready,
      chunks: s.chunks,
      session: s.session,
      frame: s.frame,
      behind: s.behind,
      leg: plan.legs[legs.length]?.id,
    });
    await p.waitForTimeout(20);
  }
  throw Error("Movement timed out");
}
try {
  // Walk at original60px/s, no teleport or collision override.
  for (const leg of plan.legs) {
    if (leg.sceneResetBefore) {
      await up();
      await stopTouch();
      if (posePending) await posePending;
      await p.goto(
        `http://127.0.0.1:4325/3D-pharse5-/?native&renderer=canvas&entry=${leg.entry}&pixelAudit`,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
    }

    if (leg.running) await p.keyboard.down("Shift");
    else await p.keyboard.up("Shift");
    const legStartedAt = Date.now();
    const start = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
    }));
    let failure = null;
    try {
      for (const [x, y] of leg.points) {
        await axis("x", x);
        await axis("y", y);
        if (leg.id.endsWith("walk-out")) {
          await up();
          await stopTouch();
          for (let n = 0; n < 25; n++) {
            record(await p.evaluate(() => window.__GATE3__));
            await p.waitForTimeout(24);
          }
          if (x === 3300 && y === (leg.bridge === "A" ? 3555 : 4020)) {
            // Native controls: face/move both ways, stop; press toward railing,
            // let original collisions stop movement, then return normally.
            for (const [key, ms] of [
              ["a", 180],
              ["d", 360],
              ["a", 180],
              ["w", 500],
            ]) {
              armPose("turn-", `${leg.id}-turn`);
              await p.keyboard.down(key);
              for (let n = 0; n < Math.ceil(ms / 25); n++) {
                record(await p.evaluate(() => window.__GATE3__));
                await p.waitForTimeout(25);
              }
              armPose("stop-", `${leg.id}-stop`);
              await p.keyboard.up(key);
              await p.waitForTimeout(350);
              record(await p.evaluate(() => window.__GATE3__));
              if (key === "a" || key === "d") await axis("x", x);
              else await axis("y", y);
            }
            await axis("y", y);
            await axis("x", x);
          }
        }
      }
    } catch (e) {
      failure = e.message;
      await up();
    }
    await p.keyboard.up("Shift");
    const end = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
    }));
    legs.push({
      id: leg.id,
      scene: leg.scene,
      sceneResetBefore: leg.sceneResetBefore,
      startedAt: legStartedAt,
      endedAt: Date.now(),
      start,
      end,
      status: failure ? "FAIL" : "PASS_REAL_KEYBOARD_AND_JOYSTICK_MOVEMENT",
      failure,
      requested: leg.requestedTarget,
      gridTarget: leg.gridTarget,
    });
    console.log(
      leg.id,
      legs.at(-1).status,
      Math.round(end.x),
      Math.round(end.y),
    );
    const a = await p.evaluate(() =>
      window
        .__GATE3_PIXEL_AUDIT__()
        .then((a) => ({ ...a, state: window.__GATE3__ })),
    );
    await fs.writeFile(
      `${D}/walk-${leg.id}-native.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    await fs.writeFile(
      `${D}/walk-${leg.id}-audit.json`,
      JSON.stringify(a, null, 2),
    );
    if (failure) break;
    await p.waitForTimeout(200);
  }

  await up();
  await stopTouch();
  if (posePending) await posePending;
  const final = await p.evaluate(() => window.__GATE3__);
  const video = p.video();
  await ctx.close();
  const recordingClosedAt = Date.now();
  await video.saveAs(`${D}/world-traversal.webm`);
  await fs.writeFile(
    `${D}/movement-report.json`,
    JSON.stringify(
      {
        method:
          "Real WASD plus native captured joystick for fine corner control; Chromium touch emulation, NOT a physical device. Two independent crossings, each four continuous out/return walk/run legs after its own initial review spawn. Original Shift speed, no overrides. Stop at every outward waypoint including landings and narrow section; real left/right and toward-rail input at midpoint. No in-movement teleport/collision override or movement-speed changes. A* gives intended waypoints; native contact and rendered-body evidence reported separately.",
        legs,
        samples,
        movingShots,
        poseShots,
        poseRequests,
        interactions,
        recordingRequestedAt,
        recordingClosedAt,
        errors,
        final,
        complete:
          legs.length === plan.legs.length && legs.every((x) => !x.failure),
        physicalDeviceEvidence: false,
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
