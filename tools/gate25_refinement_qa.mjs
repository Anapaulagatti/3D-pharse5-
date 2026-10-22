import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
const D = "docs/gate25-refinement";
async function record(p, name) {
  const dir = ".cache/gate25-refinement/" + name;
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
function watch(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
}
try {
  for (const [id, phase] of [
    ["district-reconstruction", "BEFORE"],
    ["district-refinement", "AFTER"],
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
  await ready(p, "district-refinement");
  assert.equal(
    await p.evaluate(() => typeof window.__GATE2_TEST__),
    "undefined",
  );
  const g = await grid(p),
    routes = [];
  const finish = await record(p, "DISTRICT_TRAVERSAL");
  for (const target of [
    [1552, 780],
    [1998, 780],
    [2548, 790],
    [2824, 697],
    [2548, 790],
    [1998, 780],
    [1552, 780],
  ]) {
    routes.push(await walk(p, g, target));
    await p.screenshot({ path: D + `/PLAYER_${target[0]}.png` });
  }
  rows.push({
    case: "both joins both directions / station approach / actual normal entry keyboard",
    pass: true,
    routes,
    video: await finish(),
  });
  const stop = await record(p, "PEDESTRIAN_PASSAGES"),
    lanes = [];
  for (const [name, targets] of [
    [
      "WEST",
      [
        [1524, 780],
        [1524, 500],
        [1524, 300],
        [1524, 180],
        [1524, 400],
        [1524, 600],
        [1524, 780],
      ],
    ],
    [
      "EAST",
      [
        [1998, 780],
        [2508, 780],
        [2508, 500],
        [2508, 300],
        [2508, 180],
        [2508, 400],
        [2508, 600],
        [2508, 780],
      ],
    ],
  ]) {
    const steps = [];
    for (const t of targets) {
      steps.push(await walk(p, g, t, t[1] === 780));
      if (t[1] !== 780)
        await p.screenshot({ path: D + `/${name}_PASSAGE_${t[1]}.png` });
    }
    lanes.push({ name, steps });
  }
  const end = await state(p);
  assert.equal(end.chunks.resident.length, 3);
  assert.equal(end.samplingMode, 1);
  rows.push({
    case: "new pedestrian alley and station connector / actual return trips",
    pass: true,
    lanes,
    video: await stop(),
    state: end,
  });
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    D + "/browser-qa.json",
    JSON.stringify(
      {
        rows,
        errors,
        physicalDevice: "NOT TESTED",
        humanArtApproval: "PENDING",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS actual native capture / both joins / both new passage return trips / original nearest sampling",
  );
  await p.close();
} finally {
  await b.close();
}
