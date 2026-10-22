import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
const D = "docs/gate25-station-planters";
async function record(p, name) {
  const dir = ".cache/gate25-station-planters/" + name;
  await fs.mkdir(dir, { recursive: true });
  const c = await p.context().newCDPSession(p),
    frames = [],
    writes = [];
  c.on("Page.screencastFrame", (e) => {
    const n = String(frames.length).padStart(6, "0") + ".jpg";
    frames.push({ name: n, t: e.metadata.timestamp });
    writes.push(fs.writeFile(dir + "/" + n, Buffer.from(e.data, "base64")));
    void c
      .send("Page.screencastFrameAck", { sessionId: e.sessionId })
      .catch(() => {});
  });
  await c.send("Page.startScreencast", {
    format: "jpeg",
    quality: 88,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 4,
  });
  return async () => {
    await c.send("Page.stopScreencast");
    await Promise.all(writes);
    await fs.writeFile(
      dir + "/frames.txt",
      frames
        .map(
          (f, i) =>
            `file '${f.name}'\nduration ${Math.max(0.001, (frames[i + 1]?.t ?? f.t + 0.1) - f.t)}`,
        )
        .join("\n") + "\n",
    );
    execFileSync("ffmpeg", [
      "-y",
      "-hide_banner",
      "-loglevel",
      "error",
      "-f",
      "concat",
      "-safe",
      "0",
      "-i",
      dir + "/frames.txt",
      "-fps_mode",
      "vfr",
      "-c:v",
      "libx264",
      "-threads",
      "2",
      "-preset",
      "fast",
      "-crf",
      "22",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      D + "/" + name + ".mp4",
    ]);
    return {
      source:
        "actual Phaser/CDP normal-entry real input, no QA placement or speed change",
      frames: frames.length,
      seconds: frames.at(-1).t - frames[0].t,
    };
  };
}

const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-gpu-compositing",
      "--disable-background-timer-throttling",
    ],
  }),
  errors = [],
  rows = [];
const watch = (p) => {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
};
try {
  for (const [id, phase] of [
    ["district-refinement", "BEFORE"],
    ["district-planter-repair", "AFTER"],
  ]) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    watch(p);
    await ready(p, id, "&native&overview");
    assert.equal((await state(p)).zoom, 1);
    await capture(p, D + "/" + phase + "_NATIVE_1X.png");
    await p.close();
  }
  const p = await b.newPage({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  watch(p);
  await ready(p, "district-planter-repair");
  assert.equal(
    await p.evaluate(() => typeof window.__GATE2_TEST__),
    "undefined",
  );
  const g = await grid(p),
    routes = [];
  const finish = await record(p, "STATION_GAMEPLAY");
  for (const t of [
    [1552, 780],
    [1998, 780],
    [2548, 790],
    [2824, 817],
    [2824, 697],
    [2780, 710],
    [2780, 805],
    [2868, 805],
    [2868, 710],
    [2824, 697],
  ])
    routes.push(await walk(p, g, t));
  const collisions = [];
  for (const [name, cx] of [
    ["left", 2636],
    ["right", 3004],
  ]) {
    routes.push(await walk(p, g, [cx, 736]));
    const before = await state(p);
    assert(before.behind.includes("station-planter-" + name));
    assert.equal(
      before.occluders.find((o) => o.id === "station-planter-" + name).alpha,
      1,
    );
    await p.screenshot({ path: D + "/BEHIND_" + name.toUpperCase() + ".png" });
    await p.keyboard.down("ArrowDown");
    await p.waitForTimeout(750);
    await p.keyboard.up("ArrowDown");
    const blocked = await state(p);
    assert(blocked.y < 752 && blocked.y > before.y);
    collisions.push({
      name,
      before: [before.x, before.y],
      blocked: [blocked.x, blocked.y],
      pass: true,
      foregroundDepth: before.occluders.find(
        (o) => o.id === "station-planter-" + name,
      ),
    });
    await p.keyboard.down("ArrowUp");
    await p.waitForTimeout(200);
    await p.keyboard.up("ArrowUp");
  }
  routes.push(await walk(p, g, [2824, 697]));
  await p.screenshot({ path: D + "/STATION_WITH_JUNI_GAMEPLAY.png" });
  const video = await finish();
  await p.setViewportSize({ width: 3184, height: 1214 });
  await p.waitForTimeout(350);
  const s = await state(p);
  assert.equal(s.zoom, 1);
  assert(Math.abs(s.x - 2824) < 4);
  await capture(p, D + "/JUNI_GAMEPLAY_CANVAS_1X.png");
  rows.push({
    case: "normal-entry station approach / both edges of tactile route / two planter foot collisions / native foreground depth",
    pass: true,
    routes,
    collisions,
    video,
    finalState: s,
  });
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    D + "/browser-qa.json",
    JSON.stringify(
      {
        rows,
        errors,
        physicalDevices: "NOT TESTED",
        humanVisualQuality: "PENDING",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS native Phaser captures / actual entrance and clearance traversal / both foot collisions / Y-sorted opaque planters",
  );
  await p.close();
} finally {
  await b.close();
}
