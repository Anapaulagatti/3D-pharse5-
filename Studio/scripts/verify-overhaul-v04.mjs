// Actual WebGL images, locomotion/face values, native input and accessibility checks.
import assert from 'node:assert/strict'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile} from 'node:fs/promises'
import {createHash} from 'node:crypto'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json'))
const {chromium,expect}=req('@playwright/test'),url=process.argv[2]||'http://127.0.0.1:4184/'
const out=resolve(root,process.env.STUDIO_V04_REPORT_DIR||'quality-reports/v0.4/render');await mkdir(out,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const errors=[],missing=[],checks=[],states={},metrics={};let current
const watch=p=>{p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})}
const ready=async p=>{await expect(p.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout:60_000});await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));await expect.poll(()=>p.evaluate(()=>window.__STUDIO_METRICS__?.assetsLoaded),{timeout:60_000}).toBe(true)}
const click=async(p,l)=>{await expect(l).toBeVisible();await expect(l).toBeEnabled();await l.evaluate(e=>e.scrollIntoView({block:'center'}));const b=await l.boundingBox();await p.mouse.click(b.x+b.width/2,b.y+b.height/2)}
const shot=async(p,name)=>{await p.locator('canvas').evaluate(e=>e.scrollIntoView({block:'center'}));const b=await p.locator('canvas').boundingBox();return p.screenshot({path:resolve(out,name+'.png'),clip:b})}
const m=p=>p.evaluate(()=>window.__STUDIO_METRICS__),hash=b=>createHash('sha256').update(b).digest('hex')
const toggle=async(p,label,value)=>{const l=p.getByLabel(label);if(await l.isChecked()!==value)await click(p,l);if(value)await expect(l).toBeChecked();else await expect(l).not.toBeChecked()}
const recordCheck=async label=>{checks.push(label);await writeFile(resolve(out,'progress.json'),JSON.stringify({status:'IN_PROGRESS',url,checks,states,metrics,errors,missing},null,2)+'\n')}
try{
 const context=await browser.newContext({viewport:{width:1280,height:1100},reducedMotion:'reduce'})
 const page=await context.newPage();current=page;watch(page);page.setDefaultTimeout(60_000)
 assert.equal((await page.goto(url)).status(),200);await ready(page);await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
 for(const light of ['day','evening','night']){await page.getByLabel('Ánh sáng').selectOption(light);await shot(page,light);metrics[light]=await m(page)}
 await page.getByLabel('Ánh sáng').selectOption('day');await shot(page,'hero');await page.screenshot({path:resolve(out,'desktop.png'),fullPage:true})
 await recordCheck('Actual richer Hanok day/evening/night/hero renders with OS reduced motion respected')
 await click(page,page.getByRole('button',{name:/Linh vật gốm/}));await ready(page)
 const names=['Idle','Walk','Run','Jump','Greeting','Happy','Thinking','Celebration','Disappointed','Curious','ClickReaction','ReturnToIdle']
 const signatures=new Set()
 for(const name of names){await page.getByLabel('Trạng thái linh vật').selectOption(name);await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout:60_000}).toBe(name);const img=await shot(page,'mascot-'+name.toLowerCase());states[name]=await m(page);signatures.add(hash(img))}
 assert.equal(signatures.size,12);assert.equal(new Set(states.Idle.authoredClips).size,12)
 assert.ok(states.Happy.facialParts.FaceOpen);assert.ok(states.Disappointed.facialParts.FaceFrown);assert.ok(states.Thinking.facialParts.FaceThought);assert.ok(states.Curious.facialParts.FaceO)
 assert.notDeepEqual(states.Walk.limbRotations,states.Run.limbRotations);assert.notDeepEqual(states.Walk.facialParts,states.Run.facialParts)
 await recordCheck('Twelve real authored clips have distinct rendered poses; actual happy/sad/thinking/curious mouth and eye geometry differs; Walk and Run limbs/face differ')
 await toggle(page,'Giảm chuyển động',false);await ready(page)
 for(const name of names){await page.getByLabel('Trạng thái linh vật').selectOption(name);await ready(page);await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe(name);const start=await m(page),a=await shot(page,'live-'+name.toLowerCase()+'-a');await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.clipTime)).not.toBe(start.clipTime);await page.waitForTimeout(280);const b=await shot(page,'live-'+name.toLowerCase()+'-b');assert.notEqual(hash(a),hash(b));states[name].live={start,end:await m(page),pixelsChanged:true}}
 await recordCheck('All twelve clips visibly change pixels and native mixer time; walk/run/jump full-body motion captured')
 await page.getByLabel('Trạng thái linh vật').selectOption('Idle');await ready(page)
 const b=await page.locator('canvas').boundingBox(),point=(await m(page)).interactivePoints.mascot
 await page.mouse.click(b.x+point[0],b.y+point[1]);await expect(page.locator('.interaction-notice')).toHaveText('Một cú nhảy nhỏ dành cho bạn.')
 await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe('ClickReaction');await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe('ReturnToIdle');await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe('Idle')
 const greet=page.getByRole('button',{name:'Vẫy chào',exact:true});await greet.focus();await page.keyboard.press('Enter');await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe('Greeting');await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip)).toBe('Idle')
 await recordCheck('Actual mascot click hops; keyboard action waves; native one-shot ReturnToIdle settles both to Idle')
 await click(page,page.getByRole('button',{name:/Sân hanok/}));await ready(page);await page.getByLabel('Ánh sáng').selectOption('night')
 const ambient=await shot(page,'ambient-a'),before=await m(page);await page.waitForTimeout(700);assert.notEqual(hash(ambient),hash(await shot(page,'ambient-b')));const after=await m(page);assert.ok(after.environmentTime>before.environmentTime);assert.notEqual(after.lanternIntensity,before.lanternIntensity)
 for(const type of ['lantern','tree']){await ready(page);const box=await page.locator('canvas').boundingBox(),p=(await m(page)).interactivePoints[type];await page.mouse.click(box.x+p[0],box.y+p[1]);await expect(page.locator('.interaction-notice')).toHaveText(type==='lantern'?'Ánh đèn ấm vừa bừng lên.':'Một làn gió nhẹ qua cành mận.');await shot(page,type+'-response')}
 await recordCheck('Actual ambient canopy/lantern/paper motion and lantern/tree mesh interactions provide visible feedback')
 await click(page,page.getByRole('button',{name:'Tạm dừng',exact:true}));await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive)).toBe(false);await page.waitForTimeout(100);const frozen=await m(page);await page.waitForTimeout(450);const paused=await m(page);assert.equal(paused.clipTime,frozen.clipTime);assert.equal(paused.environmentTime,frozen.environmentTime)
 await click(page,page.getByRole('button',{name:'Tiếp tục',exact:true}));await page.emulateMedia({reducedMotion:'no-preference'});await expect(page.locator('.motion-preference')).toHaveCount(0);await page.emulateMedia({reducedMotion:'reduce'});await expect(page.getByLabel('Giảm chuyển động')).toBeChecked();await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive)).toBe(false);await shot(page,'reduced-motion')
 await recordCheck('Pause freezes mixer/world; native changed OS reduced motion yields a deliberate static expressive pose')
 await page.emulateMedia({reducedMotion:'no-preference'});await ready(page)
 const box=await page.locator('canvas').boundingBox(),cam=(await m(page)).cameraPosition
 await page.mouse.move(box.x+box.width*.45,box.y+box.height*.3);await page.mouse.down();await page.mouse.move(box.x+box.width*.63,box.y+box.height*.36,{steps:12});await page.mouse.up();assert.notDeepEqual((await m(page)).cameraPosition,cam);await shot(page,'orbit')
 await click(page,page.getByRole('button',{name:/Đặt lại góc nhìn/}));await ready(page)
 for(const [name,f] of [['Mái hanok','roof'],['Vườn mận','garden'],['Đài gốm','dais']]){await click(page,page.getByRole('button',{name,exact:true}));await ready(page);await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.focus)).toBe(f);await shot(page,f+'-detail')}
 await click(page,page.getByRole('button',{name:'Tổng quan',exact:true}));await toggle(page,'Góc nhìn điện ảnh',true);const cinema=(await m(page)).cameraPosition;await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.cameraPosition)).not.toEqual(cinema);const ob=await page.locator('canvas').boundingBox();await page.mouse.move(ob.x+ob.width*.6,ob.y+ob.height*.3);await page.mouse.down();await page.mouse.move(ob.x+ob.width*.65,ob.y+ob.height*.32,{steps:7});await page.mouse.up();await expect(page.getByLabel('Góc nhìn điện ảnh')).not.toBeChecked()
 await recordCheck('Real orbit/reset/focus and gentle cinematic movement; cinematic yields to manual orbit')
 await toggle(page,'Giảm chuyển động',true);await ready(page);metrics.medium=await m(page)
 await page.getByLabel('Chất lượng').selectOption('high');await ready(page);await shot(page,'high-quality');metrics.high=await m(page)
 await page.getByLabel('Chất lượng').selectOption('low');await ready(page);metrics.low=await m(page);assert.ok(metrics.low.drawCalls<metrics.medium.drawCalls);assert.ok(metrics.low.triangles<155000);assert.ok(metrics.low.drawCalls<=135)
 await page.getByLabel('Ánh sáng').selectOption('day');await click(page,page.getByRole('button',{name:/Đặt lại góc nhìn/}));await ready(page);await page.setViewportSize({width:390,height:844});await ready(page);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:resolve(out,'mobile.png'),fullPage:true});await shot(page,'mobile-hero')
 await click(page,page.getByRole('button',{name:/Linh vật gốm/}));await ready(page);await page.getByLabel('Trạng thái linh vật').selectOption('Jump');await shot(page,'mobile-mascot');metrics.mobile=await m(page)
 await recordCheck('Low/medium/high quality tested; measured low draw/triangle budget; responsive 390×844 hero/Jump portrait without overflow')
 await toggle(page,'Giảm chuyển động',false);await ready(page);await page.evaluate(()=>{const d=document.createElement('div');d.id='qa-scroll';d.style.height='1600px';document.body.appendChild(d);scrollTo(0,document.body.scrollHeight)});await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive)).toBe(false);await page.evaluate(()=>document.getElementById('qa-scroll').remove());await ready(page);await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive)).toBe(true);await recordCheck('Actual offscreen IntersectionObserver pauses and scrolling back resumes performance')
 await context.close();current=null
 const fc=await browser.newContext({viewport:{width:390,height:844}}),fp=await fc.newPage();watch(fp)
 await fp.addInitScript(()=>{const old=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.startsWith('webgl')?null:old.call(this,t,...a)}});await fp.goto(url);await expect(fp.locator('.stage')).toHaveAttribute('data-engine','fallback');await expect(fp.locator('.poster img')).toBeVisible();await expect(fp.getByLabel('Góc nhìn điện ảnh')).toBeDisabled();await fp.screenshot({path:resolve(out,'fallback.png'),fullPage:true});await click(fp,fp.getByRole('button',{name:/Linh vật gốm/}));await expect(fp.locator('.poster img')).toBeVisible();await fc.close();await recordCheck('Actual missing-WebGL original PNG fallback and usable phone controls, no misleading action buttons')
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 await writeFile(resolve(out,'verification.json'),JSON.stringify({status:'PASS',url,verified_at:new Date().toISOString(),checks,states,metrics,critical_errors:errors,missing_resources:missing,public_deployment:false,limitation:'Cloud SwiftShader functional rendering; physical phone/GPU FPS unmeasured'},null,2)+'\n')
 console.log(checks.length+' actual v0.4 browser checks PASS; 12 authored static/live states; no critical errors/missing resources')
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({status:'FAIL',url,checks,errors,missing,message:String(e),metrics:current?await m(current).catch(()=>null):null},null,2)+'\n');throw e}finally{await browser.close()}
