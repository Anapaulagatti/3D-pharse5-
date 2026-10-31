import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const D='docs/phase3bc', base=process.env.QUEST_REVIEW_URL ?? 'http://127.0.0.1:4322/3D-pharse5-/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const results={status:'RUNNING',quests:[],routes:[],errors:[],physicalDevices:'NOT TESTED',hardwareGPU:'NOT TESTED'};
let context,page;
async function move(target,radius=10) {
 const start=await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]);
 const route=JSON.parse(execFileSync('python3',['tools/phase3bc/path.py',...start.map(String),...target.map(String),String(radius)],{encoding:'utf8'}));
 for(const waypoint of route.points){
  let count=0,stale=0,last=1e9;
  while(count++<200){
   const p=await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]);
   const dx=waypoint[0]-p[0],dy=waypoint[1]-p[1],dist=Math.hypot(dx,dy);
   if(dist<2.5)break;
   if(Math.abs(last-dist)<.05)stale++;else stale=0;last=dist;
   if(stale>15)throw Error('Blocked '+JSON.stringify({p,waypoint}));
   const keys=[];if(Math.abs(dx)>1.5)keys.push(dx>0?'d':'a');if(Math.abs(dy)>1.5)keys.push(dy>0?'s':'w');
   for(const k of ['Shift',...keys])await page.keyboard.down(k);
   await page.waitForTimeout(Math.min(90,Math.max(18,dist*7)));
   for(const k of [...keys,'Shift'])await page.keyboard.up(k);
  }
  if(count>=200)throw Error('Movement timeout');
 }
 const end=await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]);
 results.routes.push({start,target,end,plannedLength:route.length,realKeyboard:true});
}
async function begin(npc,name){
 context=await browser.newContext({viewport:{width:960,height:640},deviceScaleFactor:1,recordVideo:{dir:`${D}/videos`,size:{width:960,height:640}}});
 await context.addInitScript(()=>localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:'juni'})));
 page=await context.newPage();page.on('pageerror',e=>results.errors.push(e.message));
 await page.goto(base+`?qa&renderer=canvas&npcReview=${npc}`);
 await page.waitForFunction(()=>window.__GATE3__?.ready&&window.__NPC_WORLD__?.active>0,undefined,{timeout:60000});
 await page.evaluate(()=>window.__NPC_LIFE_QA__.setTime(540,1));
 await page.waitForTimeout(300);
 await talk(npc);await page.locator(`[data-npc-quest="${npc}"]`).click();
 await page.locator(`[data-quest="${name}"] button`).first().click();
 await page.getByRole('button',{name:'Trở lại thế giới / Từ chối',exact:true}).click();
}
async function talk(npc){
 const actor=await page.evaluate(id=>window.__NPC_WORLD__.actors.find(n=>n.id===id)?.position,npc);
 if(!actor)throw Error('NPC not active '+npc);
 await move(actor,45);
 await page.waitForTimeout(200);await page.keyboard.press('e');
 await page.locator('#npc-dialogue').waitFor({state:'visible',timeout:8000});
 const id=await page.locator('#npc-dialogue').getAttribute('data-npc-id');if(id!==npc)throw Error('Wrong target '+id);
}
async function finish(npc,id){
 await talk(npc);await page.locator(`[data-npc-quest="${npc}"]`).click();
 const card=page.locator(`[data-quest="${id}"]`);
 await card.locator('button').first().click();
 const old=await card.locator('[data-question]').getAttribute('data-question');
 // First item in each authored pool has answer1, so answer0 must fail.
 await card.locator('[data-answer="0"]').click();
 const next=await card.locator('[data-question]').getAttribute('data-question');
 if(old===next)throw Error('Question repeated');
 const noReward=await page.evaluate(()=>window.__NPC_WORLD__.quests.coins);if(noReward!==0)throw Error('Wrong answer paid');
 await card.locator('[data-answer="0"]').click();
 await page.waitForTimeout(150);
 await page.screenshot({path:`${D}/${id}-reward.png`});
 const s=await page.evaluate(()=>window.__NPC_WORLD__.quests);
 if(s.records[id].status!=='completed'||s.transactions.length!==1)throw Error('Quest not completed');
 await page.getByRole('button',{name:'Trở lại thế giới / Từ chối',exact:true}).click();
 await page.reload();await page.waitForFunction(()=>window.__GATE3__?.ready&&window.__NPC_WORLD__,undefined,{timeout:60000});
 const after=await page.evaluate(()=>window.__NPC_WORLD__.quests);
 if(JSON.stringify(s)!==JSON.stringify(after))throw Error('Reload changed rewards');
 await page.screenshot({path:`${D}/${id}-world-native.png`});
 const video=page.video();await context.close();await video.saveAs(`${D}/videos/${id}.webm`);await fs.unlink(await video.path()).catch(()=>{});
 results.quests.push({id,status:'PASS',wrongQuestion:old,nextQuestion:next,reloadStable:true,coins:after.coins,transactions:after.transactions});
 await fs.writeFile(`${D}/RUNTIME_QA.json`,JSON.stringify(results,null,2));
}
try{
 await begin('npc-minseo','modern-delivery-v1');
 // Reach recipient naturally in the SAME scene; no reload/teleport.
 await move([1010,2620],40);await page.waitForFunction(()=>window.__NPC_WORLD__.actors.some(a=>a.id==='npc-jiho'),undefined,{timeout:15000});
 await finish('npc-jiho','modern-delivery-v1');
 await begin('npc-harin','jeju-orchard-v1');
 for(const p of [[3900,4070],[3930,4080],[3960,4080]]){await move(p,12);await page.locator('#quest-world-action').waitFor({state:'visible'});await page.keyboard.press('e');await page.waitForTimeout(100);}
 await move([3740,4070],30);await finish('npc-harin','jeju-orchard-v1');
 await begin('npc-cheolsu','farm-first-seed-v1');
 await move([470,669],12);
 for(let i=0;i<3;i++){await page.locator('#quest-world-action').waitFor({state:'visible'});await page.keyboard.press('e');await page.waitForTimeout(180);}
 await move([500,810],25);await finish('npc-cheolsu','farm-first-seed-v1');
 results.status=results.errors.length?'FAIL':'PASS ACTUAL PHASER THREE QUESTS';
}catch(e){results.status='FAIL';results.failure=String(e);if(page)await page.screenshot({path:`${D}/runtime-failure.png`}).catch(()=>{});await context?.close().catch(()=>{});process.exitCode=1;}
await browser.close();await fs.writeFile(`${D}/RUNTIME_QA.json`,JSON.stringify(results,null,2));console.log(JSON.stringify(results));
