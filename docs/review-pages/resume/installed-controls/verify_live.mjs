// Hosted QA only: opens the actual deployed game. Never builds or edits game files.
import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const base = process.env.LIVE_URL;
const url = new URL(base);
if (url.protocol !== 'https:' || url.hostname !== 'anapaulagatti.github.io' || url.pathname !== '/3D-pharse5-review/') throw Error('Refuse wrong deployment destination');
const config = JSON.parse(await fs.readFile('review-source.json', 'utf8'));
const result = { status: 'RUNNING', url: base, checkedAt: new Date().toISOString(), actors: [], errors: [], missing: [], assetURLs: [], physicalDevices: 'NOT TESTED', hardwareGPU: 'NOT TESTED' };
const check = (value, message) => { if (!value) throw Error(message); };
await fs.mkdir('evidence', { recursive: true });
let browser;
try {
  let manifest;
  for (let attempt = 0; attempt < 12; attempt++) {
    const r = await fetch(new URL('export-manifest.json', base), { cache: 'no-store' });
    if (r.ok) { manifest = await r.json(); break; }
    await new Promise(r => setTimeout(r, 5000));
  }
  check(manifest, 'Live export manifest unavailable after deployment');
  // Small bounded HEAD pool verifies every root and snapshot asset URL without
  // downloading hundreds of MB of duplicated snapshot artwork.
  let next = 0;
  await Promise.all(Array.from({ length: 4 }, async () => {
    while (next < manifest.files.length) {
      const row = manifest.files[next++];
      const target = new URL(row.filename, base);
      check(target.origin === url.origin && target.pathname.startsWith(url.pathname), 'Asset outside review site');
      const r = await fetch(target, { method: 'HEAD' });
      result.assetURLs.push({ path: row.filename, status: r.status });
      check(r.ok, `Broken asset ${row.filename}: ${r.status}`);
    }
  }));
  const catalog = await (await fetch(new URL('catalog.json', base))).json();
  check(catalog.npcs.length === 26 && new Set(catalog.npcs.map(n => n.id)).size === 26, 'Not26unique NPC catalog identities');
  browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 960, height: 640 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on('pageerror', e => result.errors.push(e.message));
  page.on('response', r => { if (r.status() >= 400) result.missing.push({ url: r.url(), status: r.status() }); });
  await page.goto(base); await page.locator('#roster article').nth(25).waitFor();
  await page.screenshot({ path: 'evidence/portal-desktop.png' });
  for (const n of catalog.npcs) {
    await page.goto(new URL('play/?qa&renderer=canvas&npcReview=' + n.id, base).href);
    await page.waitForFunction(id => window.__GATE3__?.ready && window.__NPC_WORLD__?.actors.some(a => a.id === id), n.id);
    const before = await page.evaluate(() => ({ game: window.__GATE3__, npc: window.__NPC_WORLD__ }));
    if (n.archive) check(!before.npc.actors.some(a => a.id === config.archiveHosts[n.id]), 'Archive actor overlaps displaced host');
    check(before.npc.catalogTotal === 26 && before.npc.active <= 4 && before.npc.assets.loaded <= 4 && before.npc.assets.pending <= 2, 'Runtime roster/cache regression');
    await page.evaluate(() => window.__NPC_LIFE_QA__.setTime(1140, 0));
    const a = before.npc.actors.find(a => a.id === n.id), dx = a.position[0] - before.game.x, dy = a.position[1] - before.game.y;
    const key = Math.abs(dx) > Math.abs(dy) ? dx > 0 ? 'd' : 'a' : dy > 0 ? 's' : 'w';
    await page.locator('#stage canvas').click({ position: { x: 320, y: 180 } });
    await page.keyboard.down(key);
    try { await page.waitForFunction(id => window.__NPC_WORLD__?.target === id, n.id, { timeout: 15000 }); } finally { await page.keyboard.up(key); }
    await page.keyboard.press('e'); await page.locator('#npc-dialogue').waitFor({ state: 'visible' });
    await page.locator('#npc-dialogue-return').click();
    const state = await page.evaluate(id => ({ clock: window.__NPC_WORLD__.clock, actor: window.__NPC_WORLD__.actors.find(a => a.id === id), paused: window.__GATE3__.paused }), n.id);
    check(state.actor.nativeScale.every(v => v === 1) && state.actor.sampling === 1 && !state.paused, 'Native rendering/control recovery failed');
    check(state.clock.minute === 1140 && state.clock.rate === 0, 'Daily-life inspector did not control actual clock');
    result.actors.push({ id: n.id, status: 'PASS', frame: state.actor.frame, zone: state.actor.zone });
  }
  await page.screenshot({ path: 'evidence/game-native.png' });
  for (const viewport of [{ width: 390, height: 844 }, { width: 667, height: 375 }]) {
    await page.setViewportSize(viewport); await page.goto(base); await page.locator('#roster article').nth(25).waitFor();
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Mobile portal overflows');
    await page.screenshot({ path: `evidence/mobile-${viewport.width}.png` });
  }
  const mobile = await browser.newContext({ viewport: { width: 667, height: 375 }, hasTouch: true, deviceScaleFactor: 1 });
  const touch = await mobile.newPage(); await touch.goto(new URL('play/?qa&renderer=canvas&npcReview=npc-minseo', base).href);
  await touch.waitForFunction(() => window.__GATE3__?.ready && window.__NPC_WORLD__?.actors.some(a => a.id === 'npc-minseo'));
  await touch.locator('#portal-review-controls summary').tap();
  await touch.locator('#portal-review-controls input').fill('540'); await touch.locator('#portal-review-controls select').selectOption('0');
  await touch.getByRole('button', { name: 'Đặt giờ · REVIEW ONLY', exact: true }).tap();
  await touch.waitForFunction(() => window.__NPC_WORLD__?.clock.minute === 540 && window.__NPC_WORLD__?.clock.rate === 0);
  await touch.locator('#portal-review-controls summary').tap();
  const stick = await touch.locator('#joystick').boundingBox(); check(stick, 'Landscape joystick missing');
  const p0 = await touch.evaluate(() => ({ x:window.__GATE3__.x,y:window.__GATE3__.y,n:window.__NPC_WORLD__.actors.find(a=>a.id==='npc-minseo').position }));
  const dx=p0.n[0]-p0.x,dy=p0.n[1]-p0.y, ox=Math.abs(dx)>Math.abs(dy)?Math.sign(dx)*32:0,oy=Math.abs(dy)>=Math.abs(dx)?Math.sign(dy)*32:0;
  const session=await mobile.newCDPSession(touch),x=stick.x+stick.width/2,y=stick.y+stick.height/2;
  await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});
  await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+ox,y:y+oy}]});
  await touch.waitForTimeout(650);
  await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  const moved=await touch.evaluate(p=>Math.hypot(window.__GATE3__.x-p.x,window.__GATE3__.y-p.y),p0);check(moved>1,'Actual mobile joystick did not move player');
  result.mobileJoystickDistance=moved;
  await touch.locator('#portal-review-controls summary').tap();
  await touch.locator('#portal-review-controls a').tap(); await touch.waitForURL(base);
  await mobile.close();
  check(!result.errors.length && !result.missing.length, 'Live console/resource errors');
  result.status = 'PASS ACTUAL DEPLOYED HTTPS GAME';
} catch (e) { result.status = 'FAIL'; result.failure = e.stack; throw e; }
finally { await fs.writeFile('evidence/LIVE_QA.json', JSON.stringify(result, null, 2)); await browser?.close(); }
