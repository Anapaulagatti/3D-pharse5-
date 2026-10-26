import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
try {
  const c = await b.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await c.addInitScript(() =>
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "hyunwoo" }),
    ),
  );
  const p = await c.newPage();
  await p.goto(
    "http://127.0.0.1:4325/3D-pharse5-/?native&pixelAudit&renderer=webgl&entry=transition",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  if ((await p.evaluate(() => window.__GATE3__.renderer)) !== "WebGL")
    throw Error("Not WebGL");
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__()),
    file = "hyunwoo-software-webgl-native.png";
  await fs.writeFile(
    "docs/phase2b/" + file,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  const path = "/tmp/phase2b-native-full/" + file;
  await fs.copyFile("docs/phase2b/" + file, path);
  const q = JSON.parse(
    await fs.readFile("docs/phase2b/actual-gameplay.json", "utf8"),
  );
  q.rows = q.rows.filter((r) => r.mode !== "hyunwoo-webgl");
  q.rows.push({
    mode: "hyunwoo-webgl",
    id: "hyunwoo",
    action: "idle",
    view: "front",
    file,
    sourcePath: path,
    audit: a,
    observedFrames: [a.state.frame],
    trace: [],
    method:
      "Actual native WebGL backing capture; desktop SwiftShader software renderer, not hardware performance evidence",
  });
  await fs.writeFile(
    "docs/phase2b/actual-gameplay.json",
    JSON.stringify(q, null, 2),
  );
  console.log("Actual new-character native WebGL capture; SwiftShader only");
  await c.close();
} finally {
  await b.close();
}
