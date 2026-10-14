// Actual served GLB, native controls, real pixels and skin/morph state.
import assert from 'node:assert/strict'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile} from 'node:fs/promises'
import {createHash} from 'node:crypto'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium,expect:base}=req('@playwright/test'),expect=base.configure({timeout:60_000})
const out=resolve(root,process.env.STUDIO_V05_CHARACTER_REPORT_DIR||'quality-reports/v0.5/gate-c/corrected-render');await mkdir(out,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const url=process.argv[2]||'http://127.0.0.1:4186/?candidate=v05',errors=[],missing=[],states={}
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.setDefaultTimeout(60000)
 p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
 assert.equal((await p.goto(url)).status(),200);await p.getByLabel('Chế độ',{exact:true}).selectOption('portrait')
 await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.skinBones)).toBe(28)
 const m=()=>p.evaluate(()=>window.__REFORGE_METRICS__),hash=b=>createHash('sha256').update(b).digest('hex')
 const shot=async n=>{await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));const buffer=await p.screenshot({path:resolve(out,n+'.png'),clip:await p.locator('canvas').boundingBox()});states[n]=await m();return hash(buffer)}
 for(const view of ['front','left','rear','right']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(view);await shot(view)}
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('front')
 const clips=['Idle','Walk','Run','WalkStart','WalkStop','RunStart','RunStop','JumpStart','JumpAir','JumpLand','TurnLeft','TurnRight','Greeting','Happy','Thinking','Sad','Celebration','Surprised','Curious','InteractionReaction']
 assert.deepEqual(new Set((await m()).clips),new Set(clips))
 for(const clip of clips){await p.getByLabel('Animation',{exact:true}).selectOption(clip);await expect.poll(async()=> (await m()).clip).toBe(clip);await shot('pose-'+clip.toLowerCase())}
 await p.getByLabel('Animation',{exact:true}).selectOption('Idle')
 const faceHashes=new Set()
 for(const name of ['Neutral','Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating']){
  await p.getByLabel('Biểu cảm',{exact:true}).selectOption(name)
  if(name!=='Neutral')await expect.poll(async()=> (await m()).morphs[name]).toBe(1)
  faceHashes.add(await shot('face-'+name.toLowerCase()))
 }
 assert.equal(faceHashes.size,10)
 await p.getByLabel('Biểu cảm',{exact:true}).selectOption('Auto');await p.getByLabel('Giảm chuyển động',{exact:true}).uncheck()
 for(const clip of clips){await p.getByLabel('Animation',{exact:true}).selectOption(clip);await expect.poll(async()=> (await m()).clip).toBe(clip);const start=(await m()).clipTime,a=await shot('live-'+clip.toLowerCase()+'-a');await expect.poll(async()=> (await m()).clipTime).not.toBe(start);await p.waitForTimeout(130);const b=await shot('live-'+clip.toLowerCase()+'-b');assert.notEqual(a,b,clip+' actual rendered motion');states['live-'+clip.toLowerCase()+'-b'].pixelsChanged=true}
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 await writeFile(resolve(out,'verification.json'),JSON.stringify({status:'PASS_PENDING_VISUAL_REVIEW',url,verified_at:new Date().toISOString(),authored_clips:clips,static_views:4,expressions:10,actual_live_pairs:20,states,critical_errors:errors,missing_resources:missing,limitation:'Actual skinned GLB/render/animation/morph inspection only. Game controller, clothing/body human review and final mobile/quality/accessibility gates still required; no hardware FPS claim.'},null,2)+'\n')
 console.log('Actual Nari28bones/20clips/10distinct expression images/20moving pairs; no critical errors')
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({status:'FAIL',message:String(e),states,errors,missing},null,2)+'\n');throw e}finally{await browser.close()}
