// Fast actual render review before spending time on all clip/motion regressions.
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile} from 'node:fs/promises'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium,expect}=req('@playwright/test')
const out=resolve(root,process.argv[2]||'quality-reports/v0.5/gate-c/boneheat-keyposes');await mkdir(out,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const errors=[],states={}
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())})
 await p.goto('http://127.0.0.1:4186/?candidate=v05');await p.getByLabel('Chế độ',{exact:true}).selectOption('portrait');await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.skinBones),{timeout:60000}).toBe(28)
 const shot=async n=>{await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));await p.screenshot({path:resolve(out,n+'.png'),clip:await p.locator('canvas').boundingBox()});states[n]=await p.evaluate(()=>window.__REFORGE_METRICS__)}
 for(const view of ['front','left','rear','right']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(view);await shot(view)}
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('front')
 for(const clip of ['Happy','Greeting','Thinking','Celebration','JumpAir','Walk','Run']){await p.getByLabel('Animation',{exact:true}).selectOption(clip);await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.clip),{timeout:60000}).toBe(clip);await shot(clip.toLowerCase())}
 await writeFile(resolve(out,'inspection.json'),JSON.stringify({status:'ACTUAL_KEYPOSES_PENDING_HUMAN_REVIEW',errors,states},null,2)+'\n');console.log('Actual key poses captured, inspect before accepting')
}finally{await browser.close()}
