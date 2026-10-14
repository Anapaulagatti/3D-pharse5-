// Actual browser renders of the approved prototype; images are not synthesized.
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile,copyFile} from 'node:fs/promises'
import assert from 'node:assert/strict'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium,expect:base}=req('@playwright/test'),expect=base.configure({timeout:90000})
const url=process.argv[2]||'http://127.0.0.1:4190/town.html',out=resolve(root,process.env.TOWN_REVIEW_DIR||'quality-reports/v0.6/prototype/first-render'),states={},errors=[],missing=[]
await mkdir(out,{recursive:true});const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.setDefaultTimeout(90000);p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
 await p.goto(url);const stage=p.getByTestId('town-stage'),m=()=>p.evaluate(()=>window.__TOWN_METRICS__)
 await expect(stage).toHaveAttribute('data-engine','ready');await expect.poll(async()=> (await m()).skinBones).toBe(28)
 const shot=async n=>{await stage.evaluate(e=>e.scrollIntoView({block:'center'}));await p.screenshot({path:resolve(out,n+'.png'),clip:await stage.boundingBox()});states[n]=await m();await writeFile(resolve(out,'states.json'),JSON.stringify({status:'IN_PROGRESS',states,errors,missing},null,2)+'\n')}
 await shot('hero-day');await p.locator('.studio-settings summary').click()
 for(const q of ['low','medium','high']){await p.getByLabel('Chất lượng',{exact:true}).selectOption(q);await shot('quality-'+q)}
 await p.getByLabel('Chất lượng',{exact:true}).selectOption('medium');await p.getByLabel('Ánh sáng',{exact:true}).selectOption('evening');await shot('hero-evening');await p.getByLabel('Ánh sáng',{exact:true}).selectOption('night');await shot('hero-night');await p.getByLabel('Ánh sáng',{exact:true}).selectOption('day')
 await p.getByLabel('Chế độ',{exact:true}).selectOption('architecture');await expect(stage).toHaveAttribute('data-engine','ready')
 for(const v of ['front','rear','left','right','roof','connection','interior']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(v);await shot('house-'+v)}
 await p.getByLabel('Chế độ',{exact:true}).selectOption('portrait');await expect(stage).toHaveAttribute('data-engine','ready')
 for(const v of ['front','left','rear','right']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(v);await shot('nari-'+v)}
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('face')
 for(const v of ['Neutral','Happy','Surprised','Celebrating','Thinking','Sad']){await p.getByLabel('Biểu cảm',{exact:true}).selectOption(v);await expect.poll(async()=> v==='Neutral'?Object.entries((await m()).morphs).filter(([n])=>n!=='Blink').every(([,n])=>n===0):(await m()).morphs[v]===1).toBe(true);await shot('face-'+v)}
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('front');await p.getByLabel('Biểu cảm',{exact:true}).selectOption('Auto')
 for(const v of ['Idle','Walk','Run','JumpStart','JumpAir','JumpLand','Greeting','Happy','Surprised','Celebration','Thinking']){await p.getByLabel('Animation',{exact:true}).selectOption(v);await expect.poll(async()=> (await m()).clip).toBe(v);await shot('pose-'+v)}
 await p.getByLabel('Chất lượng',{exact:true}).selectOption('low');await p.getByLabel('Giảm chuyển động',{exact:true}).uncheck();await p.getByLabel('Animation',{exact:true}).selectOption('Walk');await expect.poll(async()=> (await m()).motion).toBe(true);await shot('walk-a');let before=(await m()).clipTime;await expect.poll(async()=> (await m()).clipTime).not.toBe(before);await shot('walk-b')
 await p.getByLabel('Animation',{exact:true}).selectOption('Run');await shot('run-a');before=(await m()).clipTime;await expect.poll(async()=> (await m()).clipTime).not.toBe(before);await shot('run-b')
 await p.getByLabel('Giảm chuyển động',{exact:true}).check();await p.getByLabel('Chế độ',{exact:true}).selectOption('hero');await expect(stage).toHaveAttribute('data-engine','ready');await p.setViewportSize({width:390,height:844});await shot('mobile-hero');assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 await writeFile(resolve(out,'verification.json'),JSON.stringify({status:'PASS_AUTOMATED_PENDING_VISUAL_INSPECTION',url,states,errors,missing,limitation:'Actual cloud SwiftShader view/pose/mixer/layout evidence, not physical-device FPS. Native gameplay/accessibility is verified separately.'},null,2)+'\n');console.log('Actual prototype static/moving views saved:',Object.keys(states).length)
 if(process.env.TOWN_SAVE_POSTER==='1'){await mkdir(resolve(root,'exports/v0.6/posters'),{recursive:true});await copyFile(resolve(out,'hero-day.png'),resolve(root,'exports/v0.6/posters/plaza-day.png'))}
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({message:String(e),states,errors,missing},null,2)+'\n');throw e}finally{await browser.close()}
