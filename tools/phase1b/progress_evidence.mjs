import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
const D='docs/phase1b',browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const c=await browser.newContext({viewport:{width:1024,height:768},recordVideo:{dir:'/tmp/phase1b-progress-video',size:{width:1024,height:768}}});const p=await c.newPage();const rows=[],errors=[];p.on('pageerror',e=>errors.push(e.message));
const ready=async()=>p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,{}, {timeout:45000});
const state=async()=>p.evaluate(()=>({id:window.__GATE3__.characterId,x:window.__GATE3__.x,y:window.__GATE3__.y,visited:window.__GATE3__.visited,sprites:window.__GATE3__.playerSprites}));
try{
 await p.goto('http://127.0.0.1:4320/3D-pharse5-/?renderer=canvas&pixelAudit');await p.locator('#character-confirm').click();await ready();
 await p.keyboard.press('e');await p.locator('#dialog').waitFor();await p.locator('#close').click();await p.keyboard.down('d');await p.waitForFunction(x=>window.__GATE3__.x>x+18,2048);await p.keyboard.up('d');await p.waitForTimeout(300);
 for(const id of ['juni','haneul','bomi','minjun']){
  const before=await state();if(!before.visited.length)throw Error('No actual visited marker');
  await p.locator('#settings summary').click();await p.locator('#character-open').click();await p.locator(`[data-character="${id}"]`).click();await p.locator('#character-confirm').click();await p.locator('#character-selection').waitFor({state:'hidden'});await p.waitForFunction(id=>window.__GATE3__.characterId===id,id);await p.locator('#settings summary').click();await p.waitForTimeout(250);
  const after=await state();if(before.x!==after.x||before.y!==after.y||JSON.stringify(before.visited)!==JSON.stringify(after.visited)||after.sprites!==1)throw Error('Switch state loss');
  await p.reload();await ready();const reload=await state();if(JSON.stringify(after)!==JSON.stringify(reload))throw Error('Reload state loss');rows.push({id,before,after,reload,status:'PASS'});
 }
 const video=p.video();await c.close();await video.saveAs(`${D}/progress-switch-refresh.webm`);await fs.writeFile(`${D}/progress-switch-refresh.json`,JSON.stringify({method:'Actual E at approved gate target creates existing visited marker; real walking/UI switches/refresh. No fake progress values, actor moves, test-frame forcing or scene rewrites.',rows,errors},null,2));
}finally{await browser.close();}
