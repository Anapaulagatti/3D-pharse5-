import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({ viewport: { width: 1280, height: 1000 } });
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
let result;
try {
  await p.goto("http://127.0.0.1:4292/");
  await p.getByText("Play restored station", { exact: true }).click();
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const start = await p.evaluate(() => window.__GATE3__.y);
  await p.keyboard.down("s");
  await p.waitForTimeout(600);
  await p.keyboard.up("s");
  const end = await p.evaluate(() => window.__GATE3__.y);
  if (end <= start) throw Error("Package movement failed");
  const m = await p.evaluate(
    async () =>
      await (
        await fetch("assets/gate3/registration-working-v3/manifest.json")
      ).json(),
  );
  if (m.objects.some((o) => o.id.startsWith("station-platform/")))
    throw Error("Rejected visuals active");
  if (errors.length) throw Error(errors.join("\n"));
  result = {
    status: "PASS",
    packageMovement: { startY: start, endY: end },
    originalCanopyActive: m.objects.some(
      (o) => o.id === "registration/station-platform-canopy",
    ),
    rejectedLayersActive: false,
    errors,
    transferCertified: false,
  };
  await fs.writeFile(
    "docs/g3a-platform-restoration/package-smoke.json",
    JSON.stringify(result, null, 2),
  );
  console.log(result);
} finally {
  await b.close();
}
