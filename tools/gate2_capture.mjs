import { chromium } from "@playwright/test";
import { ready, capture } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
try {
  for (const id of process.argv[2]
    ? [process.argv[2]]
    : ["a", "b", "c", "transition", "station"]) {
    const sizes = {
      a: [1536, 1024],
      b: [1536, 1024],
      c: [1024, 1536],
      transition: [1536, 1024],
      station: [720, 720],
    };
    const [width, height] = sizes[id];
    const p = await b.newPage({
      viewport: { width: Math.max(1280, width + 40), height: height + 200 },
      deviceScaleFactor: 1,
    });
    await ready(p, id, "&native&overview");
    console.log(
      id,
      await capture(p, `docs/gate2/${id.toUpperCase()}_NATIVE_1X.png`),
    );
    await p.close();
  }
} finally {
  await b.close();
}
