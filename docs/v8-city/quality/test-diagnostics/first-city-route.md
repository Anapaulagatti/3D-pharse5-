# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: v8-city.spec.ts >> V8 continuous civic boulevard, four urban frontages and safe platform access
- Location: tests/e2e/v8-city.spec.ts:38:1

# Error details

```
Error: Actual walking stuck near 2896.8888888888887,2688: {"ready":true,"area":"outdoor","x":2904,"y":2685.356391175725,"world":[4352,5312],"gateOpen":false,"transitions":0,"activeProps":38,"totalProps":482,"ambientClock":82119.24333333394,"reservedNPCs":[],"view":[2392,2299,1024,652]}
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - link "KOREAN ARENA NHỮNG CON ĐƯỜNG HÀN QUỐC" [ref=e4] [cursor=pointer]:
      - /url: /3D-pharse5-/
      - text: KOREAN ARENA
      - generic [ref=e5]: NHỮNG CON ĐƯỜNG HÀN QUỐC
    - generic [ref=e6]: Blue Letter Coast · Ga & bờ biển
    - button "Tạm dừng" [ref=e7] [cursor=pointer]
    - button "Mở cài đặt" [ref=e8] [cursor=pointer]: ☰
  - main [ref=e9]:
    - generic "Thế giới Korean Arena" [ref=e10]:
      - 'generic "Korean Arena — toàn thế giới: WASD hoặc joystick để đi, giữ chạy, E khám phá; cung điện, rừng tháp, lễ hội, ga ven biển và vườn Jeju." [active] [ref=e11]'
    - button "Mở bản đồ hành trình" [ref=e12] [cursor=pointer]:
      - img "Bản đồ di sản, Namsan, Bora Bloom, bờ biển và Windstone" [ref=e13]
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
  79  | test("V8 continuous waterfront, ferry-only travel and Jeju scenic circuit", async ({
  80  |   page,
  81  | }) => {
  82  |   test.setTimeout(300000);
  83  |   await ready(page);
  84  |   await place(page, 2112, 3648);
  85  |   await follow(page, route("harbor-approach"));
  86  |   await follow(page, route("mainland-boarding"));
  87  |   await page.locator("#interact").click();
  88  |   await page.locator("#travel-go").click();
  89  |   await page.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
  90  |   await follow(page, route("jeju-arrival"));
  91  |   await follow(page, route("jeju-scenic-loop"));
  92  |   await follow(page, route("jeju-arrival", true));
  93  |   await follow(page, route("island-boarding", true));
  94  |   await page.locator("#interact").click();
  95  |   await page.locator("#travel-go").click();
  96  |   await page.waitForFunction(
  97  |     () => window.__FULL_WORLD__?.district === "busan-coast",
  98  |   );
  99  | });
  100 | test("V8 mobile uses actual analog movement, retained motion preference and portrait pause", async ({
  101 |   browser,
  102 | }) => {
  103 |   const c = await browser.newContext({
  104 |     viewport: { width: 844, height: 390 },
  105 |     deviceScaleFactor: 3,
  106 |     isMobile: true,
  107 |     hasTouch: true,
  108 |     reducedMotion: "reduce",
  109 |   });
  110 |   try {
  111 |     const p = await c.newPage();
  112 |     await ready(p);
  113 |     await place(p, 2112, 3008);
  114 |     const d = await c.newCDPSession(p),
  115 |       box = (await p.locator("#joystick").boundingBox())!,
  116 |       cx = box.x + box.width / 2,
  117 |       cy = box.y + box.height / 2;
  118 |     await d.send("Input.dispatchTouchEvent", {
  119 |       type: "touchStart",
  120 |       touchPoints: [{ x: cx, y: cy, id: 1 }],
  121 |     });
  122 |     await d.send("Input.dispatchTouchEvent", {
  123 |       type: "touchMove",
  124 |       touchPoints: [{ x: cx + box.width * 0.25, y: cy, id: 1 }],
  125 |     });
  126 |     await p.waitForFunction(() => window.__SEOUL__!.x > 2126);
  127 |     expect(
  128 |       await p.evaluate(() => window.__FULL_WORLD__!.analogMagnitude),
  129 |     ).toBeGreaterThan(0);
  130 |     await d.send("Input.dispatchTouchEvent", {
  131 |       type: "touchEnd",
  132 |       touchPoints: [],
  133 |     });
  134 |     await settled(p);
  135 |     const clock = await p.evaluate(() => window.__SEOUL__!.ambientClock);
  136 |     await p.waitForTimeout(200);
  137 |     expect(await p.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(clock);
  138 |     await p.setViewportSize({ width: 390, height: 844 });
  139 |     await expect(p.locator("#rotate-screen")).toBeVisible();
  140 |     await p.setViewportSize({ width: 844, height: 390 });
  141 |     await expect(p.locator("#rotate-screen")).toBeHidden();
  142 |     expect(await p.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
  143 |       "Canvas",
  144 |     );
  145 |     for (const id of ["interact", "run", "talk", "emote"]) {
  146 |       const r = (await p.locator("#" + id).boundingBox())!;
  147 |       expect(r.width).toBeGreaterThanOrEqual(44);
  148 |       expect(r.height).toBeGreaterThanOrEqual(44);
  149 |     }
  150 |   } finally {
  151 |     await c.close();
  152 |   }
  153 | });
  154 | async function follow(p: Page, points: number[][]) {
  155 |   const dense: number[][] = [];
  156 |   let from = await p.evaluate(() => [window.__SEOUL__!.x, window.__SEOUL__!.y]);
  157 |   for (const to of points) {
  158 |     const n = Math.max(
  159 |       1,
  160 |       Math.ceil(Math.hypot(to[0] - from[0], to[1] - from[1]) / 16),
  161 |     );
  162 |     for (let i = 1; i <= n; i++)
  163 |       dense.push([
  164 |         from[0] + ((to[0] - from[0]) * i) / n,
  165 |         from[1] + ((to[1] - from[1]) * i) / n,
  166 |       ]);
  167 |     from = to;
  168 |   }
  169 |   const held = new Set<string>();
  170 |   await p.locator("canvas").focus();
  171 |   await p.keyboard.down("Shift");
  172 |   try {
  173 |     for (const [x, y] of dense) {
  174 |       const began = Date.now();
  175 |       for (;;) {
  176 |         const s = await p.evaluate(() => window.__SEOUL__!);
  177 |         if (Math.abs(s.x - x) < 6 && Math.abs(s.y - y) < 6) break;
  178 |         if (Date.now() - began > 24000)
> 179 |           throw Error(
      |                 ^ Error: Actual walking stuck near 2896.8888888888887,2688: {"ready":true,"area":"outdoor","x":2904,"y":2685.356391175725,"world":[4352,5312],"gateOpen":false,"transitions":0,"activeProps":38,"totalProps":482,"ambientClock":82119.24333333394,"reservedNPCs":[],"view":[2392,2299,1024,652]}
  180 |             `Actual walking stuck near ${x},${y}: ${JSON.stringify(s)}`,
  181 |           );
  182 |         const keys = new Set<string>();
  183 |         if (s.x < x - 4) keys.add("ArrowRight");
  184 |         if (s.x > x + 4) keys.add("ArrowLeft");
  185 |         if (s.y < y - 4) keys.add("ArrowDown");
  186 |         if (s.y > y + 4) keys.add("ArrowUp");
  187 |         for (const k of held)
  188 |           if (!keys.has(k)) {
  189 |             await p.keyboard.up(k);
  190 |             held.delete(k);
  191 |           }
  192 |         for (const k of keys)
  193 |           if (!held.has(k)) {
  194 |             await p.keyboard.down(k);
  195 |             held.add(k);
  196 |           }
  197 |         await p.waitForTimeout(25);
  198 |       }
  199 |     }
  200 |   } finally {
  201 |     for (const k of held) await p.keyboard.up(k);
  202 |     await p.keyboard.up("Shift");
  203 |   }
  204 |   await settled(p);
  205 | }
  206 | 
```