import assert from 'node:assert/strict'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile,readFile} from 'node:fs/promises'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium,expect:base}=req('@playwright/test'),expect=base.configure({timeout:60000})
const out=resolve(root,process.env.STUDIO_V05_WORLD_REPORT_DIR||'quality-reports/v0.5/gate-d/render');await mkdir(out,{recursive:true})
const url=process.argv[2]||'http://127.0.0.1:4186/?candidate=v05',errors=[],missing=[],states={}
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.setDefaultTimeout(60000)
 p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
 assert.equal((await p.goto(url)).status(),200);await expect(p.getByTestId('reforge-stage')).toHaveAttribute('data-engine','ready')
 const m=()=>p.evaluate(()=>window.__REFORGE_METRICS__),shot=async n=>{await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));await p.waitForTimeout(180);await p.screenshot({path:resolve(out,n+'.png'),clip:await p.locator('canvas').boundingBox()});states[n]=await m()}
 for(const l of ['day','evening','night']){await p.getByLabel('Ánh sáng',{exact:true}).selectOption(l);await expect.poll(async()=> (await m()).lighting).toBe(l);await shot('hero-'+l)}
 await p.getByLabel('Ánh sáng',{exact:true}).selectOption('day')
 await p.getByLabel('Chế độ',{exact:true}).selectOption('architecture')
 for(const v of ['front','rear','left','right','roof','connection','interior']){await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption(v);await shot('architecture-'+v)}
 await p.getByLabel('Chế độ',{exact:true}).selectOption('portrait');await p.getByLabel('Góc kiểm tra',{exact:true}).selectOption('face');await shot('face-medium')
 await p.getByLabel('Chất lượng',{exact:true}).selectOption('low');await shot('face-low')
 await p.getByLabel('Chế độ',{exact:true}).selectOption('hero');await p.setViewportSize({width:390,height:844});await shot('mobile-hero');assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 const j=JSON.parse(await readFile(resolve(root,'exports/v0.5/hanok-reforge-structure.json'),'utf8')),mods=new Map(j.modules.map(m=>[m.name,m]));const gaps=j.support_connections.map(c=>{const a=mods.get(c.supported),b=mods.get(c.support);return {connection:c,gap:Math.hypot(...a.min.map((v,i)=>Math.max(v-b.max[i],b.min[i]-a.max[i],0)))}}).filter(g=>g.gap>g.connection.tolerance_m);assert.deepEqual(gaps,[])
 await writeFile(resolve(out,'verification.json'),JSON.stringify({status:'PASS_PENDING_VISUAL_REVIEW',url,states,support_pairs:j.support_connections.length,gaps,errors,missing,limitation:'Actual browser frames; human visual review required. No physical-device FPS claim.'},null,2)+'\n');console.log('World frames/lighting/facades/face/mobile captured; support pairs:',j.support_connections.length)
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({message:String(e),states,errors,missing},null,2));throw e}finally{await browser.close()}
