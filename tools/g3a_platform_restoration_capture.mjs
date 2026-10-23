import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
const D='docs/g3a-platform-restoration', rows=[],errors=[];
const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1280,height:1000},deviceScaleFactor:1});
p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
async function load(entry){await p.goto(`http://127.0.0.1:4291/gate3-review.html?scene=registration-working-v3&entry=${entry}&native&pixelAudit`);await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0)}
async function shot(name){const a=await p.evaluate(()=>window.__GATE3_PIXEL_AUDIT__());await fs.writeFile(`${D}/${name}.png`,Buffer.from(a.png.split(',')[1],'base64'));delete a.png;rows.push({name,audit:a,state:await p.evaluate(()=>window.__GATE3__)})}
try{
 await load('station');await shot('restored-station-juni-native');
 await p.keyboard.down('s');await p.waitForFunction(()=>window.__GATE3__.y>=2855,{},{timeout:12000});await p.keyboard.up('s');await shot('restored-station-native');
 await load('platform');await shot('platform-before-blocked-movement-native');
 const start=await p.evaluate(()=>({x:window.__GATE3__.x,y:window.__GATE3__.y}));
 await p.keyboard.down('a');const samples=[];for(let i=0;i<30;i++){await p.waitForTimeout(100);samples.push(await p.evaluate(()=>({x:window.__GATE3__.x,y:window.__GATE3__.y})));}await p.keyboard.up('a');await shot('platform-blocked-movement-native');
 await fs.writeFile(`${D}/movement-test.json`,JSON.stringify({start,samples,end:samples.at(-1),input:'A held 3 seconds from existing platform entry; real keyboard; no teleport or mask override',result:samples.at(-1).x>2957?'BLOCKED':'REQUIRES_REVIEW',transferPass:false},null,2));
 await fs.writeFile(`${D}/native-captures.json`,JSON.stringify({rows,errors,method:'Actual Phaser POST_RENDER native 1280x900 output, DPR1; original renderer unchanged'},null,2));
 if(errors.length)throw Error(errors.join('\n'));console.log('Native captures complete; transfer not certified');
}finally{await b.close()}
