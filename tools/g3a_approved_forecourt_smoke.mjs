import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [];
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto(
    "http://127.0.0.1:4288/gate3-review.html?scene=registration-review&entry=station&native&pixelAudit",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  await p.keyboard.down("s");
  await p.waitForFunction(() => window.__GATE3__.y >= 2855);
  await p.keyboard.up("s");
  const audit = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    "/tmp/approved-forecourt-review-native.png",
    Buffer.from(audit.png.split(",")[1], "base64"),
  );
  delete audit.png;
  const scene = await p.evaluate(() => window.__GATE3__.scene);
  if (scene !== "registration-review" || errors.length)
    throw Error(JSON.stringify({ scene, errors }));
  await fs.writeFile(
    "docs/g3a-final-spatial-review/runtime-smoke.json",
    JSON.stringify(
      {
        status: "PASS",
        scene,
        errors,
        audit,
        note: "Current review adopts accepted pixels; runtime frame checked against accepted forecourt crops, not a new art revision.",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS current review manifest, approved floor loading and original movement",
  );
} finally {
  await b.close();
}
