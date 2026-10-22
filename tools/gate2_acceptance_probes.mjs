import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state, grid, walk } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [];
const stats = (a) => {
  const s = [...a].sort((a, b) => a - b);
  return {
    samples: s.length,
    p50: s[Math.floor(s.length * 0.5)],
    p95: s[Math.floor(s.length * 0.95)],
    max: s.at(-1),
  };
};
try {
  const p = await b.newPage({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 1,
  });
  await ready(p, "c");
  await p.locator("#scenic").click();
  await p.mouse.move(420, 180);
  for (let i = 0; i < 4; i++) {
    if (i) await p.mouse.wheel(0, 100);
    await p.waitForTimeout(180);
    const s = await state(p);
    assert(Math.abs(s.zoom - [1, 0.5, 1 / 3, 0.25][i]) < 1e-8);
    const sample = await p.evaluate(async () => {
      const s = window.__GATE2__,
        cam = s.camera,
        c = document.querySelector("canvas"),
        actual = c.getContext("2d"),
        expected = document.createElement("canvas");
      expected.width = c.width;
      expected.height = c.height;
      const ctx = expected.getContext("2d");
      ctx.imageSmoothingEnabled = false;
      const im = new Image();
      im.src = "assets/gate2/c/ground.png";
      await im.decode();
      ctx.drawImage(
        im,
        cam.viewport[0] - cam.worldView[0] * s.zoom,
        cam.viewport[1] - cam.worldView[1] * s.zoom,
        im.width * s.zoom,
        im.height * s.zoom,
      );
      const x = Math.floor(cam.viewport[0] + 20),
        y = Math.floor(cam.viewport[1] + cam.viewport[3] * 0.45);
      const a = actual.getImageData(x, y, 12, 12).data,
        e = ctx.getImageData(x, y, 12, 12).data;
      let mismatch = 0;
      for (let j = 0; j < a.length; j += 4)
        if (a[j] !== e[j] || a[j + 1] !== e[j + 1] || a[j + 2] !== e[j + 2])
          mismatch++;
      return {
        mismatchingPixels: mismatch,
        comparedPixels: 144,
        imageSmoothingEnabled: actual.imageSmoothingEnabled,
        rectangle: [x, y, 12, 12],
      };
    });
    assert.equal(
      sample.mismatchingPixels,
      0,
      JSON.stringify({ zoom: s.zoom, sample }),
    );
    assert.equal(s.samplingMode, 1);
    const view = s.camera.renderedWorldView;
    assert(Math.abs(view[0] * s.zoom - Math.round(view[0] * s.zoom)) < 1e-6);
    assert(Math.abs(view[1] * s.zoom - Math.round(view[1] * s.zoom)) < 1e-6);
    await p.screenshot({
      path: `docs/gate2/acceptance/ZOOM_${Math.round(s.zoom * 100)}.png`,
    });
    rows.push({
      case: "Actual Phaser pixels match independent nearest-source sample; pixel-aligned camera",
      zoom: s.zoom,
      sample,
      camera: s.camera,
    });
  }
  await p.close();
  const station = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await ready(station, "station");
  const g = await grid(station);
  await walk(station, g, [360, 430]);
  await station.keyboard.down("w");
  await station.waitForTimeout(900);
  await station.keyboard.up("w");
  const stopped = await state(station);
  assert(
    stopped.y >= 418.4 && stopped.y <= 421,
    JSON.stringify({
      thresholdStop: stopped.y,
      southContact: 410,
      footClearance: 8,
    }),
  );
  rows.push({
    case: "Station threshold walkable; facade collision stops actual input",
    state: stopped,
  });
  await station.close();
  const fit = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await ready(fit, "jeju-fit");
  const fg = await grid(fit),
    route = await walk(fit, fg, [830, 920]);
  await fit.keyboard.down("a");
  await fit.waitForTimeout(900);
  await fit.keyboard.up("a");
  const landing = await state(fit);
  assert(landing.x >= 807 && landing.x < 830);
  await fit.keyboard.down("d");
  await fit.waitForTimeout(300);
  await fit.keyboard.up("d");
  await walk(fit, fg, [850, 920]);
  rows.push({
    case: "Exact future island landing, continuous pier collar and water stop",
    route,
    landing,
  });
  await fit.close();
  for (const id of ["c", "b", "seam"]) {
    const q = await b.newPage({
      viewport: { width: 844, height: 390 },
      isMobile: true,
      hasTouch: true,
    });
    await ready(q, id);
    await q.waitForTimeout(5000);
    const s = await state(q);
    rows.push({
      case: "Warm short-session browser timing / active textures / heap snapshot",
      scene: id,
      frameTimes: stats(s.frameTimes),
      heap: s.heap,
      textures: s.textures,
      rgba8EquivalentBytes: s.textures.reduce(
        (v, t) => v + t.width * t.height * 4,
        0,
      ),
    });
    await q.close();
  }
  await fs.writeFile(
    "docs/gate2/acceptance/probes.json",
    JSON.stringify(
      {
        rows,
        limits: [
          "Pixel comparison samples12x12 unchanged terrain, not all source pixels",
          "RGBA8 equivalent is not measured total browser/GPU residency",
          "Chrome heap snapshot excludes native image/canvas allocations; no forced GC or physical-device FPS claim",
        ],
      },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS", rows.length, "render/collision/memory probes");
} finally {
  await b.close();
}
