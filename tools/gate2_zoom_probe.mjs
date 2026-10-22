import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [];
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
  await fs.writeFile(
    "docs/gate2/acceptance/zoom-probes.json",
    JSON.stringify({ rows }, null, 2) + "\n",
  );
  const previous = JSON.parse(
    await fs.readFile("docs/gate2/acceptance/probes.json", "utf8"),
  );
  previous.rows = [
    ...rows,
    ...previous.rows.filter((r) => !r.case.startsWith("Actual Phaser pixels")),
  ];
  await fs.writeFile(
    "docs/gate2/acceptance/probes.json",
    JSON.stringify(previous, null, 2) + "\n",
  );
  console.log(
    "PASS distinct nearest sampling at",
    rows.map((r) => r.zoom),
  );
} finally {
  await b.close();
}
