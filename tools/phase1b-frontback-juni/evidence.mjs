/* global setInterval, clearInterval */
import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
const D='docs/phase1b-frontback-juni',base='http://127.0.0.1:4320/3D-pharse5-/',key='korean-arena-player-preferences-v1';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const rows=[],errors=[];
try {
 for(const id of ['juni','haneul','bomi','minjun']){
  const ctx=await browser.newContext({viewport:{width:1280,height:1000},deviceScaleFactor:1,recordVideo:{dir:'/tmp/p1b-fb-video',size:{width:1280,height:1000}}});
  await ctx.addInitScript(({key,id})=>localStorage.setItem(key,JSON.stringify({version:1,characterId:id})),{key,id});
  const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));
  for(const action of ['walk','run'])for(const [view,button]of [['front','s'],['back','w']]){
   const prefix=`${action}-${view}-`;
   await p.goto(base+`?native&pixelAudit&renderer=canvas&entry=transition&review=${id}-${prefix}`);
   await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,{}, {timeout:45000});
   await p.locator('canvas').first().click({position:{x:640,y:450}});
   await p.evaluate(()=>{window.__FB_TRACE__=[];window.__FB_TIMER__=setInterval(()=>{const a=window.__GATE3__;window.__FB_TRACE__.push({x:a.x,y:a.y,frame:a.frame,characterId:a.characterId});},16);});
   if(action==='run')await p.keyboard.down('Shift');await p.keyboard.down(button);
   const a=await p.evaluate(prefix=>window.__GATE3_PIXEL_POSE__(prefix,4000),prefix);
   await fs.writeFile(`${D}/${id}-${action}-${view}-phaser-native.png`,Buffer.from(a.png.split(',')[1],'base64'));delete a.png;
   await p.waitForTimeout(1450);await p.keyboard.up(button);await p.keyboard.up('Shift');
   const trace=await p.evaluate(()=>{clearInterval(window.__FB_TIMER__);return window.__FB_TRACE__;});
   const seen=[...new Set(trace.map(a=>a.frame).filter(f=>f.startsWith(prefix)))];
   rows.push({id,clip:prefix.slice(0,-1),observedFrames:seen,audit:a,trace});console.log(id,prefix,seen.length);
   if(seen.length!==8)throw Error('Incomplete real gait '+id+prefix+' '+seen.length);
   await p.waitForTimeout(200);
  }
  const video=p.video();await ctx.close();await video.saveAs(`${D}/${id}-actual-phaser.webm`);
 }
 await fs.writeFile(`${D}/gameplay-qa.json`,JSON.stringify({rows,errors,method:'Actual input-driven Phaser Canvas gameplay at 60px/s walk and 100px/s run; native96x112 sprites, zoom1. Video is browser capture, separate native PNGs from POST_RENDER backing canvas. No synthetic pose forcing.',physicalDevices:'NOT TESTED',humanMotionAcceptance:'PENDING'},null,2));
}finally{await browser.close();}
