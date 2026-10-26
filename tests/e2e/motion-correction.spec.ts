import { test, expect } from "@playwright/test";
for (const id of ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"])
  test(`${id}: actual right walk/run, consecutive phases, stop and turn without engine overrides`, async ({
    page,
  }) => {
    await page.addInitScript((id) => {
      if (!localStorage.getItem("korean-arena-player-preferences-v1"))
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        );
    }, id);
    for (const action of ["walk", "run"]) {
      await page.goto("./?native&renderer=canvas&entry=transition");
      await page.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      );
      await page
        .locator("#stage canvas")
        .click({ position: { x: 640, y: 450 } });
      const start = await page.evaluate(() => window.__GATE3__!.x);
      const tracePromise = page.evaluate(async () => {
        const rows: {
          x: number;
          y: number;
          frame: string;
          players: number;
          nearest: number;
        }[] = [];
        const begun = performance.now();
        await new Promise<void>((resolve) => {
          const sample = () => {
            const s = window.__GATE3__!;
            rows.push({
              x: s.x,
              y: s.y,
              frame: s.frame,
              players: s.playerSprites,
              nearest: s.samplingMode,
            });
            if (performance.now() - begun > 4400) resolve();
            else requestAnimationFrame(sample);
          };
          requestAnimationFrame(sample);
        });
        return rows;
      });
      if (action === "run") await page.keyboard.down("Shift");
      await page.keyboard.down("d");
      const stride = action === "walk" ? 44 : 64;
      await page.waitForFunction(
        ({ start, distance }) => window.__GATE3__!.x > start + distance,
        { start, distance: stride * 4.2 },
      );
      await page.keyboard.up("d");
      await page.keyboard.up("Shift");
      await page.waitForFunction(() =>
        window.__GATE3__!.frame.startsWith("idle-right-"),
      );
      const end = await page.evaluate(() => window.__GATE3__!.x);
      const trace = await tracePromise;
      expect(end - start).toBeGreaterThan(stride * 4);
      expect(trace.every((s) => s.players === 1 && s.nearest === 1)).toBe(true);
      expect(trace.some((s) => s.frame.startsWith("stop-right-"))).toBe(true);
      const gait = trace.filter((s) => s.frame.startsWith(action + "-right-"));
      const phases = gait
        .map((s) => Number(s.frame.split("-").at(-1)))
        .filter((v, i, a) => !i || a[i - 1] !== v);
      const zero = phases.indexOf(0);
      expect(zero).toBeGreaterThanOrEqual(0);
      expect(phases.slice(zero, zero + 24)).toEqual(
        Array.from({ length: 24 }, (_, i) => i % 8),
      );
      for (let i = 1; i < gait.length; i++)
        expect(gait[i].x).toBeGreaterThanOrEqual(gait[i - 1].x);
      await page.keyboard.down("a");
      await page.waitForFunction(() =>
        window.__GATE3__!.frame.startsWith("walk-left-"),
      );
      await page.keyboard.up("a");
      expect(await page.evaluate(() => window.__GATE3__!.x)).toBeLessThan(end);
    }
  });
