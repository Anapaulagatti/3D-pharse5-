import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { gzipSync } from "node:zlib";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
for (const renderer of ["auto", "canvas"]) {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await p.goto(
    `http://127.0.0.1:4271/gate3-review.html?profile&scene=district&entry=alley&renderer=${renderer}`,
  );
  await p.waitForFunction(() => window.__GATE3__?.ready);
  await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  const cdp = await p.context().newCDPSession(p);
  const events = [];
  cdp.on("Tracing.dataCollected", (e) => events.push(...e.value));
  await cdp.send("Tracing.start", {
    categories: "devtools.timeline,v8,disabled-by-default-v8.gc",
    transferMode: "ReportEvents",
  });
  await p.waitForTimeout(2000);
  await p.keyboard.down("Shift");
  await p.keyboard.down("d");
  await p.waitForTimeout(6000);
  await p.keyboard.up("d");
  await p.keyboard.up("Shift");
  const end = new Promise((resolve) =>
    cdp.once("Tracing.tracingComplete", resolve),
  );
  await cdp.send("Tracing.end");
  await end;
  const driver = await p.evaluate(() => {
    const c = document.querySelector("canvas"),
      gl = c.getContext("webgl2") || c.getContext("webgl"),
      e = gl?.getExtension("WEBGL_debug_renderer_info");
    return {
      driver: e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : null,
      timerQuery: !!gl?.getExtension("EXT_disjoint_timer_query_webgl2"),
    };
  });
  const names = {};
  for (const e of events) {
    if (
      e.dur > 0 &&
      /GC|MajorGC|MinorGC|UpdateLayoutTree|Layout|Raster|Paint|RunTask|FunctionCall|Decode|Upload|Composite/.test(
        e.name,
      )
    ) {
      const r = (names[e.name] ??= { count: 0, totalMs: 0, maxMs: 0 });
      r.count++;
      r.totalMs += e.dur / 1000;
      r.maxMs = Math.max(r.maxMs, e.dur / 1000);
    }
  }
  await fs.writeFile(
    `docs/gate3a-corrections/trace-${renderer}.json.gz`,
    gzipSync(JSON.stringify({ traceEvents: events })),
  );
  rows.push({
    renderer,
    ...driver,
    traceEvents: events.length,
    events: names,
    notes:
      "Nested event durations overlap; do not sum categories into elapsed time. Trace adds overhead and is separate from controlled benchmark. GPU query unavailable is NOT TESTED, not zero GPU time.",
  });
  await p.close();
}
await fs.writeFile(
  "docs/gate3a-corrections/trace-summary.json",
  JSON.stringify(rows, null, 2),
);
await b.close();
