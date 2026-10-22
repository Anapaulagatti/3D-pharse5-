import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ready, state } from "./gate2_browser_lib.mjs";
const D = "docs/gate25-reconstruction";
async function record(p, name) {
  const dir = ".cache/gate25-reconstruction/" + name;
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
    maxWidth: 1280,
    maxHeight: 900,
    everyNthFrame: 3,
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
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const p = await b.newPage({ viewport: { width: 1280, height: 900 } }),
  errors = [];
p.on("pageerror", (e) => errors.push(e.message));
try {
  await ready(p, "district-reconstruction");
  assert.equal(
    await p.evaluate(() => typeof window.__GATE2_TEST__),
    "undefined",
  );
  const origin = await state(p);
  await p.click("#scenic");
  const box = await p.locator("canvas").boundingBox();
  const sx = box.x + box.width / 2,
    sy = box.y + box.height / 2;
  async function drag(dx, dy) {
    await p.mouse.move(sx - dx / 2, sy - dy / 2);
    await p.mouse.down();
    for (let n = 1; n <= 35; n++) {
      await p.mouse.move(
        sx - dx / 2 + (dx * n) / 35,
        sy - dy / 2 + (dy * n) / 35,
      );
      await p.waitForTimeout(25);
    }
    await p.mouse.up();
    await p.waitForTimeout(300);
  }
  await drag(580, 350);
  await drag(580, 350);
  const finish = await record(p, "NATIVE_CAMERA_PAN"),
    samples = [];
  for (const [band, dir] of [
    ["UPPER", -1],
    ["LOWER", 1],
  ]) {
    if (band === "LOWER") await drag(0, -550);
    for (let i = 0; i < 5; i++) {
      const s = await state(p);
      samples.push({ band, view: s.camera.worldView, zoom: s.zoom });
      assert.equal(s.zoom, 1);
      assert.equal(s.x, origin.x);
      assert.equal(s.y, origin.y);
      if (i === 1 || i === 3)
        await p.screenshot({ path: D + `/PAN_${band}_${i}.png` });
      if (i < 4) await drag(dir * 550, 0);
    }
  }
  const video = await finish();
  assert.equal(errors.length, 0);
  await fs.writeFile(
    D + "/camera-pan.json",
    JSON.stringify(
      {
        video,
        samples,
        errors,
        actualMouseDrag: true,
        noQAPlacement: true,
        JuniRetained: true,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS actual native mouse camera pan, upper/lower bands / Juni retained",
  );
} finally {
  await b.close();
}
