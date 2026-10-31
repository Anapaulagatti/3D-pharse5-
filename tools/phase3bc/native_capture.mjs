import {chromium}from'@playwright/test';import fs from'node:fs/promises';
const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});const rows=[];
for(const entry of ['retail','station','bridge-a-mainland','bridge-b-mainland','farm']){
 const c=await b.newContext({viewport:{width:960,height:640},deviceScaleFactor:1});await c.addInitScript(()=>localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:'juni'})));const p=await c.newPage();await p.goto(`http://127.0.0.1:4323/play/?qa&renderer=canvas&pixelAudit&entry=${entry}`);await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,undefined,{timeout:60000});const evidence=await p.evaluate(()=>window.__GATE3_PIXEL_AUDIT__());
 if(evidence.state.zoom!==1||evidence.state.samplingMode!==1||!evidence.camera.scroll.every(Number.isInteger)||evidence.state.playerSprites!==1)throw Error('Pixel regression '+entry);
 await fs.writeFile(`docs/phase3bc/native-${entry}.png`,Buffer.from(evidence.png.split(',')[1],'base64'));
 delete evidence.png;rows.push({entry,camera:evidence.camera,state:{renderer:evidence.state.renderer,zoom:evidence.state.zoom,sampling:evidence.state.samplingMode,playerSprites:evidence.state.playerSprites,appearance:evidence.state.appearance},layers:evidence.layers.map(l=>({position:l.position,origin:l.origin,scale:l.scale,scaleMode:l.scaleMode}))});await c.close();
}
await fs.writeFile('docs/phase3bc/NATIVE_RENDERING.json',JSON.stringify({status:'PASS',method:'Actual POST_RENDER canvas PNG, native backing pixels, zoom1, nearest sampler, integer camera. No screenshot resizing or postprocess.',captures:rows},null,2));await b.close();
