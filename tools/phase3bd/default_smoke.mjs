import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
try {
  const context = await browser.newContext({ viewport: { width: 960, height: 640 }, deviceScaleFactor: 1 });
  await context.addInitScript(() => localStorage.setItem('korean-arena-player-preferences-v1', JSON.stringify({ version: 1, characterId: 'juni' })));
  const page = await context.newPage(), errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  await page.goto('http://127.0.0.1:4333/play/');
  await page.waitForFunction(() => window.__GATE3__?.ready && window.__NPC_WORLD__?.catalogTotal === 26, undefined, { timeout: 60000 });
  const start = await page.evaluate(() => [window.__GATE3__.x, window.__GATE3__.y]);
  await page.keyboard.down('d');
  try { await page.waitForFunction(start => window.__GATE3__.x > start[0] + 8, start, { timeout: 8000 }); }
  finally { await page.keyboard.up('d'); }
  const state = await page.evaluate(() => ({ renderer: window.__GATE3__.renderer, zoom: window.__GATE3__.zoom, nearest: window.__GATE3__.samplingMode, playerSprites: window.__GATE3__.playerSprites, position: [window.__GATE3__.x, window.__GATE3__.y], catalogTotal: window.__NPC_WORLD__.catalogTotal }));
  await page.screenshot({ path: 'docs/phase3bd/offline-default-renderer.png' });
  const report = { status: errors.length ? 'FAIL' : 'PASS', url: page.url(), defaultEntryNoQAOrRendererOverride: true, start, state, errors, context: 'Desktop Chromium ANGLE SwiftShader software renderer; no hardware FPS claim', physicalDevices: 'NOT TESTED', hardwareGPU: 'NOT TESTED' };
  await fs.writeFile('docs/phase3bd/DEFAULT_ENTRY_PROOF.json', JSON.stringify(report, null, 2));
  if (errors.length || state.playerSprites !== 1 || state.nearest !== 1) throw Error('Default renderer failure');
  console.log(JSON.stringify(report));
} finally { await browser.close(); }
