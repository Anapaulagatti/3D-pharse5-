import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
const D='docs/phase1b-frontback-juni',rows=[],browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
try{
 for(const id of ['juni','haneul','bomi','minjun']){
  const ctx=await browser.newContext({viewport:{width:1280,height:1000},deviceScaleFactor:1,recordVideo:{dir:'/tmp/fb-comparison-video',size:{width:1280,height:1000}}});
  await ctx.addInitScript(id=>localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:id})),id);
  const p=await ctx.newPage(),start=Date.now();
  for(const action of ['walk','run'])for(const [view,key]of [['front','s'],['back','w']]){
   const clip=`${action}-${view}`;
   await p.goto(`http://127.0.0.1:4330/?native&renderer=canvas&entry=transition&comparison=${id}-${clip}`);
   await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,{}, {timeout:45000});
   await p.locator('canvas').first().click({position:{x:640,y:450}});
   if(action==='run')await p.keyboard.down('Shift');await p.keyboard.down(key);
   await p.waitForFunction(clip=>window.__GATE3__.frame.startsWith(clip+'-'),clip);
   const from=(Date.now()-start)/1000;
   await p.waitForTimeout(1400);
   const state=await p.evaluate(()=>({x:window.__GATE3__.x,y:window.__GATE3__.y,frame:window.__GATE3__.frame,id:window.__GATE3__.characterId}));
   await p.keyboard.up(key);await p.keyboard.up('Shift');
   rows.push({id,clip,from,duration:1.2,state});console.log(id,clip,from);
  }
  const v=p.video();await ctx.close();await v.saveAs(`${D}/${id}-comparison-original.webm`);
 }
 await fs.writeFile(`${D}/comparison-recordings.json`,JSON.stringify({rows,method:'Actual WASD/Shift gameplay in original engine at unchanged speed. Real-time1.2s excerpts grouped by action/direction for four-column comparison. Starts observed through normal locomotion; no pose forcing, speed changes or synthetic frames. These videos compare the same clip, not guaranteed identical phase at every video frame.',physicalDevices:'NOT TESTED'},null,2));
}finally{await browser.close();}
