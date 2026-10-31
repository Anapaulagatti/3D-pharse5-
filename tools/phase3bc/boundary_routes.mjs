import {chromium} from '@playwright/test';import fs from 'node:fs/promises';import {execFileSync} from 'node:child_process';
const D='docs/phase3bc',base='http://127.0.0.1:4322/3D-pharse5-/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-gpu-compositing']});
const report={status:'RUNNING',routes:[],errors:[],physicalDevices:'NOT TESTED'};
const cases=[
 ['palace','palace-route',[[2048,990],[2320,1110],[2580,1110]]],
 ['retail','retail',[[1128,2610],[1128,2597],[1418,2610],[1418,2597]]],
 ['station','station',[[2598,2610],[2888,2660],[2970,2680],[2970,2530]]],
 ['bridge-a','bridge-a-mainland',[[3010,3460],[3530,3640],[3730,3335]]],
 ['bridge-b','bridge-b-mainland',[[3030,3920],[3570,4060],[3680,4430]]],
 ['farm','farm',[[470,669],[690,669],[915,669],[915,481]]],
 ['coast','ferry',[[2900,3480],[2814,3670],[2048,3790]]],
 ['namsan','namsan',[[1460,3260],[940,2910]]],
 ['amusement','amusement',[[2440,3260],[2820,3260]]],
];
const only=process.argv.slice(2);
if(only.length){const previous=JSON.parse(await fs.readFile(`${D}/TRAVERSAL_QA.json`));report.routes=previous.routes.filter(r=>!only.includes(r.id));}
for(const [name,entry,targets] of cases){if(only.length&&!only.includes(name))continue;let context,page;const row={id:name,status:'RUNNING',legs:[]};try{
 context=await browser.newContext({viewport:{width:960,height:640},deviceScaleFactor:1,recordVideo:{dir:`${D}/videos`,size:{width:960,height:640}}});
 await context.addInitScript(()=>localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:'juni'})));
 page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await page.goto(base+`?qa&renderer=canvas&entry=${entry}`);await page.waitForFunction(()=>window.__GATE3__?.ready,undefined,{timeout:60000});
 for(const target of targets){
  const start=await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]);
  const plan=JSON.parse(execFileSync('python3',['tools/phase3bc/path.py',...start.map(String),...target.map(String),'4'],{encoding:'utf8'}));
  for(const waypoint of plan.points){let limit=0,stale=0,last=Infinity;while(limit++<220){
   const pos=await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]);const dx=waypoint[0]-pos[0],dy=waypoint[1]-pos[1],dist=Math.hypot(dx,dy);if(dist<2.8)break;
   stale=Math.abs(last-dist)<.05?stale+1:0;last=dist;if(stale>12)throw Error('Blocked '+JSON.stringify({pos,waypoint}));
   const keys=[];if(Math.abs(dx)>1.5)keys.push(dx>0?'d':'a');if(Math.abs(dy)>1.5)keys.push(dy>0?'s':'w');
   for(const k of ['Shift',...keys])await page.keyboard.down(k);await page.waitForTimeout(Math.min(90,Math.max(18,dist*7)));for(const k of [...keys,'Shift'])await page.keyboard.up(k);
  }if(limit>=220)throw Error('Traversal limit');}
  row.legs.push({start,target,end:await page.evaluate(()=>[window.__GATE3__.x,window.__GATE3__.y]),length:plan.length});
 }
 await page.screenshot({path:`${D}/route-${name}-native.png`});
 row.status='PASS REAL KEYBOARD TRAVERSAL';
 const video=page.video();await context.close();await video.saveAs(`${D}/videos/route-${name}.webm`);await fs.unlink(await video.path()).catch(()=>{});
}catch(e){row.status='FAIL';row.failure=String(e);if(page)await page.screenshot({path:`${D}/route-${name}-failure.png`}).catch(()=>{});await context?.close().catch(()=>{});}
 report.routes.push(row);await fs.writeFile(`${D}/TRAVERSAL_QA.json`,JSON.stringify(report,null,2));console.log(name,row.status);
}
report.status=report.routes.some(r=>r.status==='FAIL')||report.errors.length?'FAIL':'PASS';await fs.writeFile(`${D}/TRAVERSAL_QA.json`,JSON.stringify(report,null,2));await browser.close();
