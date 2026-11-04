from pathlib import Path
for name in ['studio','phase2b','characters']:
 p=Path(f'tests/e2e/{name}.spec.ts');s=p.read_text().replace('await expect(page.locator("#dialog")).toBeVisible();\n  await page.locator("#close").click();','await expect(page.locator("#dialog")).not.toBeVisible();\n  expect(await page.evaluate(() => window.__GATE3__!.paused)).toBe(false);').replace('await expect(page.locator("#dialog")).toBeVisible();\n    await page.locator("#close").click();','await expect(page.locator("#dialog")).not.toBeVisible();\n    expect(await page.evaluate(() => window.__GATE3__!.paused)).toBe(false);');p.write_text(s)
p=Path('tests/e2e/characters.spec.ts');s=p.read_text();start=s.index('test("corrupt, unknown and unavailable storage');end=s.index('test("mobile landscape preview fits',start);seg=s[start:end];a=seg.index('    const ctx =');z=seg.rindex('    await ctx.close();')+len('    await ctx.close();');body=seg[a:z];s=s[:start]+'''// Independent fixtures retain identical assertions and the existing120s timeout each.
for (const [label, value] of [
  ["corrupt", "{"],
  ["removed", '{"version":1,"characterId":"removed"}'],
  ["unfinished", '{"version":1,"characterId":"unfinished"}'],
  ["denied", null],
] as const)
  test(`storage ${label} recovers to Juni without crashing`, async ({browser}) => {
'''+body+'\n  });\n'+s[end:];p.write_text(s)
p=Path('tests/e2e/phase3bd.spec.ts');s=p.read_text().replace('[data-npc-quest="npc-minseo"]','[data-npc-shop="npc-minseo"]');s=s.replace('await page\n    .getByRole("button", { name: "Trở lại thế giới / Từ chối", exact: true })\n    .click();','await page.locator("#quest-close").click();');start=s.index('  await page.locator(\'[data-farm-action="till"]\')');end=s.index('  await page.waitForFunction(() => window.__GATE3__?.paused === false);',start);s=s[:start]+'''  await page.waitForFunction(() => window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage === "planted");
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  await page.waitForTimeout(550);
  await page.locator("#quest-world-action").tap();
  await page.waitForFunction(() => window.__NPC_WORLD__!.quests.economy.plots["NW-FARM-04"].stage === "watered");
  await expect(page.locator("#quest-dialogue")).not.toBeVisible();
  await page.screenshot({ path: "docs/phase3bd-in-world/mobile-farm-touch.png" });
'''+s[end:];p.write_text(s)
p=Path('tests/e2e/phase3bc.spec.ts');s=p.read_text().replace('mobile landscape quest journal supports touch, visible answers and clean control recovery','mobile journal is read-only; a nearby recipient alone opens the learning challenge').replace('?qa&renderer=canvas&npcReview=npc-minseo','?qa&renderer=canvas&npcReview=npc-jiho');start=s.index('  const card = page.locator(\'[data-quest="modern-delivery-v1"]\');');end=s.index('  const box = await page.locator("#quest-dialogue").boundingBox();',start);s=s[:start]+'''  await expect(page.locator("[data-answer]")).toHaveCount(0);
  await expect(page.locator("[data-trade]")).toHaveCount(0);
  await page.locator("#quest-close").tap();
  await page.keyboard.down("w");
  try { await page.waitForFunction(() => window.__NPC_WORLD__?.target === "npc-jiho"); }
  finally { await page.keyboard.up("w"); }
  await page.locator("#npc-interact").tap();
  await page.locator('[data-npc-quest="npc-jiho"]').tap();
  const card = page.locator('[data-quest="modern-delivery-v1"]');
  await card.locator('[data-answer="0"]').tap();
  await expect(card.locator("[data-question]")).toHaveAttribute("data-question", "parcel-2");
  await page.screenshot({path: "docs/phase3bd-in-world/mobile-question.png"});
  await card.locator('[data-answer="0"]').tap();
  expect(await page.evaluate(() => window.__NPC_WORLD__!.quests.coins)).toBe(20);
'''+s[end:];s=s.replace('await page\n    .getByRole("button", { name: "Trở lại thế giới / Từ chối", exact: true })\n    .tap();','await page.locator("#quest-close").tap();');p.write_text(s)
