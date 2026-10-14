import assert from 'node:assert/strict'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile,readFile} from 'node:fs/promises'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json'))
const {chromium,expect:base}=req('@playwright/test'),expect=base.configure({timeout:60_000})
const out=resolve(root,'quality-reports/v0.5/gate-b/render');await mkdir(out,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const url=process.argv[2]||'http://127.0.0.1:4186/?candidate=v05',errors=[],missing=[],views={}
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.setDefaultTimeout(60_000)
 p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
 assert.equal((await p.goto(url)).status(),200)
 await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.ready)).toBe(true)
 const shot=async name=>{await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.draws||0)).toBeGreaterThan(0);const b=await p.locator('canvas').boundingBox();await p.screenshot({path:resolve(out,name+'.png'),clip:b});views[name]=await p.evaluate(()=>window.__REFORGE_METRICS__)}
 for(const preset of ['hero','front','rear','left','right','roof','connection']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(preset);await p.waitForTimeout(150);await shot(preset)}
 const door=p.getByRole('button',{name:'Mở cửa',exact:true});await door.evaluate(e=>e.click());await expect.poll(()=>p.evaluate(()=>window.__REFORGE_METRICS__?.door)).toBe(1)
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('interior');await shot('interior')
 for(let i=0;i<24;i++){
  await p.getByLabel('Vòng kiểm tra 360°',{exact:true}).fill(String(i*15));await p.waitForTimeout(90);await shot('orbit-'+String(i).padStart(2,'0'))
 }
 await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('hero');await p.setViewportSize({width:390,height:844});await p.getByLabel('Chất lượng',{exact:true}).selectOption('low');await shot('mobile')
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true)
 const structure=JSON.parse(await readFile(resolve(root,'exports/v0.5/hanok-graybox-structure.json'),'utf8')),modules=new Map(structure.modules.map(m=>[m.name,m]))
 const gaps=structure.support_connections.map(c=>{const a=modules.get(c.supported),b=modules.get(c.support);assert.ok(a&&b);return {connection:c,gap:Math.hypot(...a.min.map((v,i)=>Math.max(v-b.max[i],b.min[i]-a.max[i],0)))}})
 assert.equal(gaps.filter(g=>g.gap>g.connection.tolerance_m).length,0)
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 await writeFile(resolve(out,'verification.json'),JSON.stringify({status:'PASS_PENDING_VISUAL_REVIEW',url,checked_at:new Date().toISOString(),views,support_pairs:gaps.length,support_bounds_failures:[],critical_errors:errors,missing_resources:missing,limitations:'Actual browser renders and broad-phase support bounds, not engineering proof. Human visual inspection required. 360 sequence is manually stepped camera views, not real-time gameplay or measured FPS.'},null,2)+'\n')
 console.log('Gate B: 8 views +24 actual orbit views +mobile;209 support pairs; no critical errors/missing resources')
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({status:'FAIL',message:String(e),views,errors,missing},null,2)+'\n');throw e}finally{await browser.close()}
