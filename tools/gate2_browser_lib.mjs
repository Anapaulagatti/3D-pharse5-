import fs from "node:fs/promises";
export const base = "http://127.0.0.1:4250/3D-pharse5-/";
export async function ready(p, id, suffix = "") {
  await p.goto(base + `gate2-review.html?scene=${id}${suffix}`);
  await p.waitForFunction(() => window.__GATE2__?.ready);
  await p.waitForTimeout(150);
}
export const state = (p) => p.evaluate(() => window.__GATE2__);
export async function grid(p) {
  return p.evaluate(async () => {
    const s = window.__GATE2__;
    const d = await (
      await fetch("assets/gate2/" + s.scene + "/scene.json")
    ).json();
    const im = new Image();
    im.src = "assets/gate2/" + d.mask;
    await im.decode();
    const c = document.createElement("canvas");
    c.width = im.width;
    c.height = im.height;
    const ctx = c.getContext("2d");
    ctx.drawImage(im, 0, 0);
    const pixels = ctx.getImageData(0, 0, c.width, c.height).data;
    const w = Math.ceil(d.size[0] / 8),
      h = Math.ceil(d.size[1] / 8),
      mask = [];
    for (let y = 0; y < h; y++)
      for (let x = 0; x < w; x++)
        mask.push(
          [-3, 0, 3].every((dy) =>
            [-3, 0, 3].every(
              (dx) =>
                pixels[((y * 8 + 4 + dy) * c.width + x * 8 + 4 + dx) * 4] > 127,
            ),
          )
            ? 1
            : 0,
        );
    return { w, h, mask };
  });
}
function path(g, start, target) {
  const cell = ([x, y]) => [Math.round((x - 4) / 8), Math.round((y - 4) / 8)],
    a = cell(start),
    b = cell(target),
    key = ([x, y]) => y * g.w + x,
    ok = (x, y) =>
      x >= 0 && y >= 0 && x < g.w && y < g.h && g.mask[y * g.w + x];
  const startKey = key(a),
    endKey = key(b);
  if (!ok(...a) || !ok(...b))
    throw Error(
      "Grid endpoint blocked " + JSON.stringify({ start, target, a, b }),
    );
  const q = [startKey],
    prev = new Int32Array(g.w * g.h).fill(-1);
  prev[startKey] = startKey;
  for (let head = 0; head < q.length && prev[endKey] < 0; head++) {
    const n = q[head],
      x = n % g.w,
      y = Math.floor(n / g.w);
    for (const [dx, dy] of [
      [1, 0],
      [-1, 0],
      [0, 1],
      [0, -1],
      [1, 1],
      [-1, 1],
      [1, -1],
      [-1, -1],
    ]) {
      const nx = x + dx,
        ny = y + dy,
        k = ny * g.w + nx;
      if (
        ok(nx, ny) &&
        prev[k] < 0 &&
        (!dx || !dy || (ok(nx, y) && ok(x, ny)))
      ) {
        prev[k] = n;
        q.push(k);
      }
    }
  }
  if (prev[endKey] < 0) throw Error("No route");
  const raw = [];
  for (let n = endKey; n !== startKey; n = prev[n])
    raw.push([(n % g.w) * 8 + 4, Math.floor(n / g.w) * 8 + 4]);
  raw.push([a[0] * 8 + 4, a[1] * 8 + 4]);
  raw.reverse();
  const compressed = [];
  for (let i = 1; i < raw.length - 1; i++) {
    const a = raw[i - 1],
      b = raw[i],
      c = raw[i + 1];
    if (b[0] - a[0] !== c[0] - b[0] || b[1] - a[1] !== c[1] - b[1])
      compressed.push(b);
  }
  compressed.push(raw.at(-1));
  return compressed;
}
export async function walk(p, g, target, running = true) {
  let s = await state(p);
  const points = path(g, [s.x, s.y], target),
    trace = [],
    start = Date.now();
  await p.keyboard.down(running ? "Shift" : "Control");
  let keys = new Set();
  try {
    for (const [x, y] of points) {
      const deadline = Date.now() + 10000;
      while (true) {
        s = await state(p);
        trace.push([s.x, s.y]);
        const dx = x - s.x,
          dy = y - s.y;
        if (Math.abs(dx) < 2.5 && Math.abs(dy) < 2.5) break;
        if (Date.now() > deadline)
          throw Error(`Input stuck ${s.scene} ${s.x},${s.y} toward${x},${y}`);
        const wanted = new Set();
        if (Math.abs(dx) >= 2.5)
          wanted.add(dx > 0 ? "ArrowRight" : "ArrowLeft");
        if (Math.abs(dy) >= 2.5) wanted.add(dy > 0 ? "ArrowDown" : "ArrowUp");
        for (const k of keys) if (!wanted.has(k)) await p.keyboard.up(k);
        for (const k of wanted) if (!keys.has(k)) await p.keyboard.down(k);
        keys = wanted;
        await p.waitForTimeout(35);
      }
    }
  } finally {
    for (const k of keys) await p.keyboard.up(k);
    await p.keyboard.up(running ? "Shift" : "Control");
  }
  return {
    milliseconds: Date.now() - start,
    samples: trace.length,
    start: trace[0],
    end: trace.at(-1),
    qaPlacement: false,
  };
}
export async function capture(p, file) {
  const d = await p
    .locator("canvas")
    .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
  await fs.writeFile(file, Buffer.from(d.png.split(",")[1], "base64"));
  return d.size;
}
