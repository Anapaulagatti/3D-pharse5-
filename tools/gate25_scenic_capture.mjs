import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await ready(p, "c");
  const initial = await state(p);
  await p.tap("#scenic");
  const c = await p.context().newCDPSession(p);
  await c.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [
      { x: 280, y: 170, id: 1 },
      { x: 580, y: 170, id: 2 },
    ],
  });
  for (let i = 1; i <= 8; i++) {
    await c.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [
        { x: 280 + i * 8, y: 170, id: 1 },
        { x: 580 - i * 8, y: 170, id: 2 },
      ],
    });
    await p.waitForTimeout(25);
  }
  await c.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await p.waitForTimeout(200);
  const end = await state(p);
  assert.equal(end.camera.mode, "scenic");
  assert.equal(end.zoom, 0.5);
  assert.equal(initial.x, end.x);
  await p.screenshot({ path: "docs/gate25/SCENIC.png" });
  await fs.writeFile(
    "docs/gate25/scenic-capture.json",
    JSON.stringify(
      { initial, end, realTouchPinch: true, qaPlacement: false },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS manual Scenic50% capture");
} finally {
  await b.close();
}
