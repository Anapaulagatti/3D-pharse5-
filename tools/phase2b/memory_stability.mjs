import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const ids=['juni','haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo'];
const base=process.env.P2B_BASE??'http://127.0.0.1:4325/3D-pharse5-/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-precise-memory-info']});
const ready=p=>p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,{}, {timeout:45000});
try{
 const c=await browser.newContext({viewport:{width:1280,height:1000}});
 await c.addInitScript(()=>{if(!sessionStorage.getItem('p2b-seed')){localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:'juni'}));sessionStorage.setItem('p2b-seed','1');}});
 const p=await c.newPage(),requests=[],errors=[],samples=[];p.on('request',r=>{if(/(?:characters\/[^/]+\/atlas|juni\/juni)\.png/.test(r.url()))requests.push(r.url());});p.on('pageerror',e=>errors.push(e.message));
 const client=await c.newCDPSession(p);
 async function observe(stage){await client.send('HeapProfiler.collectGarbage');const s=await p.evaluate(()=>{const s=window.__GATE3__;return {id:s.characterId,x:s.x,y:s.y,visited:s.visited,players:s.playerSprites,cache:s.characterAssets,heap:performance.memory?.usedJSHeapSize??null};});samples.push({stage,...s,atlasRequests:[...new Set(requests)]});if(s.players!==1||s.cache.textures.length>3||s.cache.composition.baseImages>2||s.cache.composition.compositeImages>2)throw Error('Unbounded owner counts '+stage);return s;}
 await p.goto(base+'?renderer=canvas');await ready(p);await observe('initial-load');if(new Set(requests).size!==1)throw Error('Initial atlas preload');
 await p.keyboard.press('e');await p.locator('#dialog').waitFor();await p.locator('#close').click({noWaitAfter:true});
 await p.locator('#settings summary').click({noWaitAfter:true});await p.locator('#character-open').click({noWaitAfter:true});
 for(const id of ids){await p.locator(`[data-character="${id}"]`).click({noWaitAfter:true});await p.waitForFunction(id=>document.querySelector('#character-name').textContent.includes(id.charAt(0).toUpperCase()+id.slice(1)),id);await p.waitForTimeout(120);}
 const baseline=await observe('twelve-gallery-browse');const originalPos=[baseline.x,baseline.y,baseline.visited];
 for(let i=0;i<60;i++){
  const id=ids[i%ids.length];await p.locator(`[data-character="${id}"]`).click({noWaitAfter:true});await p.locator('#appearance-save').click({noWaitAfter:true});await p.waitForFunction(id=>window.__GATE3__?.ready&&window.__GATE3__.characterId===id,id);await p.waitForFunction(()=>document.querySelector('#character-feedback').textContent.includes('Đã lưu'));
  const s=await observe('switch-'+(i+1));if(JSON.stringify([s.x,s.y,s.visited])!==JSON.stringify(originalPos))throw Error('Switch state loss');
 }
 // Existing approved looks and user preset data stay available independently.
 await p.locator('#appearance-preset').selectOption('review-ara-harbor');await p.locator('#appearance-preset-name').fill('Biển giữ nguyên');await p.locator('#appearance-save').click({noWaitAfter:true});await p.waitForFunction(()=>window.__GATE3__.characterId==='ara'&&window.__GATE3__.appearance.hairstyleId==='ara-braided-bun'&&document.querySelector('#character-feedback').textContent.includes('Đã lưu'));
 await p.locator('[data-character="hyunwoo"]').click({noWaitAfter:true});await p.locator('#character-confirm').click({noWaitAfter:true});await p.locator('#character-selection').waitFor({state:'hidden'});await ready(p);
 const beforeMove=await observe('gameplay-after-switching');await p.keyboard.down('d');await p.waitForFunction(x=>window.__GATE3__.x>x+8,beforeMove.x);await p.keyboard.up('d');await p.waitForTimeout(250);const before=await observe('before-reload');
 const saved=await p.evaluate(()=>JSON.parse(localStorage.getItem('korean-arena-appearance-preferences-v2')));await p.reload();await ready(p);const restored=await observe('after-reload');if(JSON.stringify([before.id,before.x,before.y,before.visited])!==JSON.stringify([restored.id,restored.x,restored.y,restored.visited]))throw Error('Reload state loss');
 const savedAfter=await p.evaluate(()=>JSON.parse(localStorage.getItem('korean-arena-appearance-preferences-v2')));if(JSON.stringify(saved)!==JSON.stringify(savedAfter))throw Error('Preset data altered on reload');
 await p.locator('#settings summary').click({noWaitAfter:true});await p.locator('#character-open').click({noWaitAfter:true});await observe('studio-reopened');
 const warm=samples.find(s=>s.stage==='switch-36'),last=samples.find(s=>s.stage==='switch-60');
 await fs.writeFile('docs/phase2b/memory-stability.json',JSON.stringify({method:'Actual Studio UI,60 committed identity changes (five complete12-character rotations), gallery-only browsing, gameplay, reload and Studio reopen. Explicit GC before samples. All source controls/scene unchanged.',samples,retainedHeapDelta36To60:last.heap-warm.heap,oldPresetBeforeReload:saved,oldPresetAfterReload:savedAfter,errors,physicalDevices:'NOT TESTED',hardwarePerformance:'NOT TESTED',note:'Heap and dimension-based texture estimates are observations; not measured total VRAM or hardware leak certification.'},null,2));if(errors.length)throw Error(JSON.stringify(errors));console.log('60switches/12identities PASS; one actor, bounded caches, preset and world-state retention; warm heap delta',last.heap-warm.heap);
}finally{await browser.close();}
