import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  }),
  rows = [];
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  for (const name of ["north", "south", "namsan"]) {
    await p.goto(
      `http://127.0.0.1:4295/gate3-review.html?scene=recovery-pilots&entry=${name}-occlusion&native&pixelAudit`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.waitForTimeout(200);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    await fs.writeFile(
      `docs/gate3-recovery/${name}-occlusion-native.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    const s = await p.evaluate(() => window.__GATE3__);
    const walkable = await p.evaluate(() =>
      window.__GATE3_TEST__.walkable(window.__GATE3__.x, window.__GATE3__.y),
    );
    rows.push({
      pilot: name,
      state: s,
      walkableAtReviewSpawn: walkable,
      audit: a,
      method:
        "One static review spawn behind foreground, no movement or route certification; North/tower soften to expose clean ground; protected retail retains original opaque alpha1 policy, not a player-visibility PASS.",
    });
    console.log("occlusion", name, s.behind, walkable);
  }
  await fs.writeFile(
    "docs/gate3-recovery/occlusion-evidence.json",
    JSON.stringify(
      {
        rows,
        sourceOwnership:
          "Native clean plates and explicit underpaint masks; approved foregrounds reused unchanged",
        status:
          "Selected static depth cases only; not full-region certification",
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
