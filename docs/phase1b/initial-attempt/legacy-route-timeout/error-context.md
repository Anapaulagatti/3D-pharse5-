# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: v10-city.spec.ts >> V10 real input route: leisure campus and ride approaches
- Location: tests/e2e/v10-city.spec.ts:142:3

# Error details

```
TimeoutError: page.waitForFunction: Timeout 10375.454222221924ms exceeded.
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - link "KOREAN ARENA V10 · GRAYBOX CHỜ DUYỆT" [ref=e4] [cursor=pointer]:
      - /url: /3D-pharse5-/
      - text: KOREAN ARENA
      - generic [ref=e5]: V10 · GRAYBOX CHỜ DUYỆT
    - generic [ref=e6]: Bora Bloom · Văn hóa và giải trí
    - button "Tạm dừng" [ref=e7] [cursor=pointer]
    - button "Mở cài đặt" [ref=e8] [cursor=pointer]: ☰
  - main [ref=e9]:
    - generic "Thế giới Korean Arena" [ref=e10]:
      - 'generic "Korean Arena — toàn thế giới: WASD hoặc joystick để đi, giữ chạy, E khám phá; cung điện, rừng tháp, lễ hội, ga ven biển và vườn Jeju." [active] [ref=e11]'
    - button "Mở bản đồ hành trình" [ref=e12] [cursor=pointer]:
      - img "Bản đồ di sản, Namsan, Bora Bloom, bờ biển và Jeju" [ref=e13]
    - generic: WASD / ↑↓←→ · Shift chạy · E khám phá
    - generic "Điều khiển cảm ứng":
      - group "Cần di chuyển" [ref=e15]:
        - generic: "N"
      - generic:
        - button "Khám phá" [ref=e16] [cursor=pointer]
        - button "Trò chuyện hoặc xác nhận" [ref=e17] [cursor=pointer]: Nói chuyện
        - button "Giữ để chạy" [ref=e18] [cursor=pointer]: Chạy
        - button "Biểu cảm" [ref=e19] [cursor=pointer]
```

# Test source

```ts
  1   | import { test, expect, type Page } from "@playwright/test";
  2   | import fs from "node:fs";
  3   | const plan = JSON.parse(
  4   |   fs.readFileSync("assets-src/v10-city/plan/city.json", "utf8"),
  5   | );
  6   | async function boot(p: Page, renderer = "canvas") {
  7   |   const errors: string[] = [],
  8   |     legacy: string[] = [];
  9   |   p.on("pageerror", (e) => errors.push(e.message));
  10  |   p.on("response", (r) => {
  11  |     if (r.status() >= 400) errors.push(r.url());
  12  |   });
  13  |   p.on("request", (r) => {
  14  |     if (/\/assets\/world\/|\/v9-world\//.test(r.url())) legacy.push(r.url());
  15  |   });
  16  |   await p.goto(`v10-city-review.html?qa&renderer=${renderer}`);
  17  |   await p.waitForFunction(
  18  |     () =>
  19  |       window.__SEOUL__?.ready &&
  20  |       window.__WORLD_REVIEW__?.candidate === "v10-graybox",
  21  |   );
  22  |   return { errors, legacy };
  23  | }
  24  | async function place(p: Page, x: number, y: number) {
  25  |   await p.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  26  |   const n = await p.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  27  |   await p.waitForFunction(
  28  |     (n) => window.__PIXEL_METRICS__!.frameCount > n + 4,
  29  |     n,
  30  |   );
  31  | }
  32  | async function axis(p: Page, axis: "x" | "y", target: number) {
  33  |   const start = await p.evaluate((axis) => window.__SEOUL__![axis], axis);
  34  |   if (Math.abs(start - target) < 4) return;
  35  |   const sign = Math.sign(target - start),
  36  |     key =
  37  |       axis === "x"
  38  |         ? sign > 0
  39  |           ? "ArrowRight"
  40  |           : "ArrowLeft"
  41  |         : sign > 0
  42  |           ? "ArrowDown"
  43  |           : "ArrowUp";
  44  |   await p.keyboard.down(key);
  45  |   try {
> 46  |     await p.waitForFunction(
      |             ^ TimeoutError: page.waitForFunction: Timeout 10375.454222221924ms exceeded.
  47  |       ({ axis, target, sign }) =>
  48  |         (window.__SEOUL__![axis] - target) * sign >= -2,
  49  |       { axis, target, sign },
  50  |       { timeout: Math.max(8000, Math.abs(target - start) * 22) },
  51  |     );
  52  |   } finally {
  53  |     await p.keyboard.up(key);
  54  |   }
  55  | }
  56  | // Each route uses one QA start, then real keyboard movement at unchanged run speed.
  57  | for (const [name, points] of [
  58  |   [
  59  |     "historic gateway to high street",
  60  |     [
  61  |       [2176, 2256],
  62  |       [2176, 2400],
  63  |       [2016, 2400],
  64  |       [2016, 2960],
  65  |     ],
  66  |   ],
  67  |   [
  68  |     "entire high street and station forecourt",
  69  |     [
  70  |       [1456, 2960],
  71  |       [3776, 2960],
  72  |       [3776, 2832],
  73  |     ],
  74  |   ],
  75  |   [
  76  |     "urban block circuit",
  77  |     [
  78  |       [1456, 2960],
  79  |       [1456, 3504],
  80  |       [2768, 3504],
  81  |       [2768, 2400],
  82  |       [2016, 2400],
  83  |     ],
  84  |   ],
  85  |   [
  86  |     "west scenic loop and tower approach",
  87  |     [
  88  |       [1216, 2960],
  89  |       [1216, 2672],
  90  |       [560, 2672],
  91  |       [320, 2784],
  92  |       [352, 3104],
  93  |       [656, 3328],
  94  |       [1024, 3248],
  95  |       [1216, 2960],
  96  |       [896, 3040],
  97  |       [736, 3040],
  98  |     ],
  99  |   ],
  100 |   [
  101 |     "leisure campus and ride approaches",
  102 |     [
  103 |       [1280, 3904],
  104 |       [1280, 3744],
  105 |       [400, 3744],
  106 |       [400, 4224],
  107 |       [400, 4352],
  108 |       [960, 4352],
  109 |       [1232, 4176],
  110 |       [1232, 4080],
  111 |       [952, 4080],
  112 |       [616, 4072],
  113 |     ],
  114 |   ],
  115 |   [
  116 |     "coastal neighborhood to boarding pier",
  117 |     [
  118 |       [2768, 3504],
  119 |       [3776, 3504],
  120 |       [3776, 4224],
  121 |       [3968, 4384],
  122 |       [3968, 4560],
  123 |     ],
  124 |   ],
  125 |   [
  126 |     "Jeju olle and village circuit",
  127 |     [
  128 |       [3296, 5216],
  129 |       [3568, 5216],
  130 |       [3552, 5568],
  131 |       [3288, 5568],
  132 |       [3216, 5664],
  133 |       [2752, 5648],
  134 |       [2624, 5648],
  135 |       [2624, 5456],
  136 |       [2464, 5456],
  137 |       [2576, 5360],
  138 |       [2800, 5384],
  139 |     ],
  140 |   ],
  141 | ] as [string, number[][]][]) {
  142 |   test(`V10 real input route: ${name}`, async ({ page }) => {
  143 |     const observed = await boot(page);
  144 |     await place(page, points[0][0], points[0][1]);
  145 |     await page.locator("canvas").focus();
  146 |     await page.keyboard.down("Shift");
```