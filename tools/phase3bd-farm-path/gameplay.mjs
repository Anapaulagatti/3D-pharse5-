import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
import {createWalk} from './walk_driver.mjs';
const D='docs/phase3bd-farm-path',base=process.env.HOTFIX_URL??'http://127.0.0.1:4451/3D-pharse5-/';
await fs.mkdir(D+'/videos',{recursive:true});
const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const c=await b.newContext({viewport:{width:960,height:640},deviceScaleFactor:1,recordVideo:{dir:D+'/videos',size:{width:960,height:640}}});
await c.addInitScript(()=>localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:'juni'})));
const p=await c.newPage(),r={status:'RUNNING',errors:[],routes:[],stages:[],fixtures:'Juni selection only; earned seed through Cheolsu; no clock/item/quest injection',physicalDevices:'NOT TESTED'};
p.on('pageerror',e=>r.errors.push(e.message));p.on('response',x=>{if(x.status()>=400)r.errors.push(x.status()+' '+x.url())});
const move=createWalk(p,r.routes),state=()=>p.evaluate(()=>window.__NPC_WORLD__.quests);
async function capture(name,expected){await p.waitForTimeout(50);const a=await p.evaluate(()=>window.__GATE3_PIXEL_AUDIT__());await fs.writeFile(D+'/'+name+'-native.png',Buffer.from(a.png.split(',')[1],'base64'));await p.screenshot({path:D+'/'+name+'.png'});delete a.png;const plants=a.farmSprites.filter(x=>x.key==='farm-crops'&&x.position[0]>=394&&x.position[0]<534&&x.position[1]>535&&x.position[1]<623);if(plants.length!==18)throw Error('Missing real plot sprites');if(expected&&!plants.every(x=>x.visible&&x.frame==='radish-'+expected))throw Error('Wrong actual stage '+name);if(!plants.every(x=>x.scale[0]===1&&x.scale[1]===1&&x.scaleMode===1))throw Error('Pixel sampling changed');if(['00-empty','07-harvested'].includes(name)&&plants.some(x=>x.visible))throw Error('Old crop did not disappear');r.stages.push({name,expected,plot:(await state()).economy.plots['NW-FARM-04'],audit:a});}
async function npc(id,area){if(area)await move(area,25);const pos=await p.evaluate(id=>window.__NPC_WORLD__.actors.find(a=>a.id===id)?.position,id);if(!pos)throw Error('NPC missing '+id);await move(pos,24);await p.keyboard.press('e');await p.locator(`#npc-dialogue[data-npc-id="${id}"]`).waitFor();}
try{
 await p.goto(base+'?qa&entry=farm&renderer=canvas&pixelAudit');await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__NPC_WORLD__,undefined,{timeout:60000});
 await npc('npc-cheolsu',[500,810]);await p.locator('[data-npc-quest="npc-cheolsu"]').click();await p.getByRole('button',{name:'Nhận lời · 좋아요'}).click();await p.locator('#quest-close').click();await p.waitForFunction(()=>!window.__GATE3__.paused);
 await move([470,669],10);await capture('00-empty');
 await p.keyboard.press('e');await p.waitForFunction(()=>window.__NPC_WORLD__.quests.economy.plots['NW-FARM-04'].stage==='planted');await capture('01-sown','sown');
 await p.waitForTimeout(550);await p.keyboard.press('e');await p.waitForFunction(()=>window.__NPC_WORLD__.quests.economy.plots['NW-FARM-04'].stage==='watered');await capture('02-watered','sown');
 const watered=(await state()).economy.plots['NW-FARM-04'].wateredAt;
 for(const [name,t,frame] of [['03-sprout',.2,'sprout'],['04-young',.42,'young'],['05-growing',.72,'growing'],['06-ready',1.01,'ready']]){
  await p.waitForFunction(({watered,t})=>Date.now()-watered>=window.__NPC_WORLD__.quests.economy.plots['NW-FARM-04'].growMs*t,{watered,t});await capture(name,frame);
 }
 if(await p.locator('#quest-dialogue').isVisible())throw Error('Farming modal');
 await p.keyboard.press('e');await p.waitForFunction(()=>window.__NPC_WORLD__.quests.economy.plots['NW-FARM-04'].stage==='empty');await capture('07-harvested');
 await npc('npc-cheolsu',[500,810]);await p.locator('[data-npc-quest="npc-cheolsu"]').click();await p.locator('[data-answer="1"]').click();await p.waitForFunction(()=>window.__NPC_WORLD__.quests.records['farm-first-seed-v1'].status==='completed');await p.locator('#quest-close').click();await p.waitForFunction(()=>!window.__GATE3__.paused);r.reward=await state();
 const prior=await state();await p.reload();await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__NPC_WORLD__);if(JSON.stringify(prior)!==JSON.stringify(await state()))throw Error('Reload persistence');r.persistence='PASS';
 await move([470,2400],7);await move([458,2400],2);await move([458,2460],2);await move([470,2500],5);await move([650,2660],15);await move([1010,2620],15);
 r.input=[];for(const keys of [['w','d'],['s','a'],['w'],['s'],['d'],['a']]){const a=await p.evaluate(()=>window.__GATE3__);for(const k of ['Shift',...keys])await p.keyboard.down(k);await p.waitForTimeout(140);for(const k of ['Shift',...keys])await p.keyboard.up(k);const z=await p.evaluate(()=>window.__GATE3__);if(Math.hypot(z.x-a.x,z.y-a.y)>25)throw Error('Input speed spike');r.input.push({keys,from:[a.x,a.y],to:[z.x,z.y],frame:z.frame});}
 r.status=r.errors.length?'FAIL':'PASS ACTUAL FARM LIFECYCLE / QUEST / PATHS';
}catch(e){r.status='FAIL';r.failure=e.stack;await p.screenshot({path:D+'/failure.png'}).catch(()=>{});process.exitCode=1;}
finally{const v=p.video();await c.close();await v.saveAs(D+'/videos/farm-lifecycle-paths.webm');await fs.unlink(await v.path()).catch(()=>{});await b.close();await fs.writeFile(D+'/GAMEPLAY_QA.json',JSON.stringify(r,null,2));}
console.log(JSON.stringify({status:r.status,error:r.failure,stages:r.stages.map(s=>s.name),routes:r.routes.length}));
