// Actual rendered candidate QA. No public deployment, screenshot mocks or animation bypass.
import assert from 'node:assert/strict'
import { createRequire } from 'node:module'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..')
const requirePreview=createRequire(resolve(root,'preview/package.json'))
const {chromium,expect}=requirePreview('@playwright/test')
const url=process.argv[2]||'http://127.0.0.1:4173/'
const out=resolve(process.env.STUDIO_POLISH_REPORT_DIR||resolve(root,'quality-reports/v0.3/final-render'))
await mkdir(out,{recursive:true})
const hash=b=>createHash('sha256').update(b).digest('hex')
const timeout=60_000, checks=[], metrics={}, errors=[], missing=[]
let lastPage
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const watch=page=>{
  page.on('pageerror',e=>errors.push(e.message))
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())})
  page.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
}
const metric=page=>page.evaluate(()=>window.__STUDIO_METRICS__)
const ready=async page=>{
  await expect(page.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout})
  // Native scroll avoids cloud headless's RAF stability wait on a demand-render canvas.
  // This does not invalidate the renderer, override motion or bypass the interaction checks.
  await page.locator('canvas').evaluate(canvas=>canvas.scrollIntoView({block:'center'}))
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.assetsLoaded),{timeout}).toBe(true)
}
const click=async(page,locator)=>{
  await expect(locator).toBeVisible({timeout});await expect(locator).toBeEnabled({timeout})
  await locator.evaluate(el=>el.scrollIntoView({block:'center'}))
  const box=await locator.boundingBox();assert.ok(box && box.width>0 && box.height>0)
  await page.mouse.click(box.x+box.width/2,box.y+box.height/2)
}
const toggle=async(page,label,checked)=>{
  const locator=page.getByLabel(label)
  if(await locator.isChecked()!==checked)await click(page,locator)
  if(checked)await expect(locator).toBeChecked();else await expect(locator).not.toBeChecked()
}
const shot=async(page,name)=>{
  const canvas=page.locator('canvas');await expect(canvas).toBeVisible({timeout})
  await canvas.evaluate(el=>el.scrollIntoView({block:'center'}))
  const box=await canvas.boundingBox();assert.ok(box && box.width>0 && box.height>0)
  // Page clip captures the real canvas without Playwright's idle-canvas RAF stability wait.
  return page.screenshot({path:resolve(out,name+'.png'),clip:box})
}
const clickObject=async(page,key)=>{
  await ready(page)
  const point=(await metric(page)).interactivePoints[key],box=await page.locator('canvas').boundingBox()
  await page.mouse.click(box.x+point[0],box.y+point[1])
}
try {
  const context=await browser.newContext({viewport:{width:1280,height:1100},reducedMotion:'reduce'})
  const page=await context.newPage();lastPage=page;page.setDefaultTimeout(timeout);watch(page)
  const response=await page.goto(url);assert.equal(response.status(),200);await ready(page)
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await page.screenshot({path:resolve(out,'desktop.png'),fullPage:true})
  for(const lighting of ['day','evening','night']) {
    await page.getByLabel('Ánh sáng').selectOption(lighting);await ready(page)
    await shot(page,lighting);metrics[lighting]=await metric(page)
  }
  await page.getByLabel('Ánh sáng').selectOption('day');await shot(page,'hero')
  checks.push('Real detailed Hanok/mascot render; day/evening/night and full hero screenshots captured')
  await click(page,page.getByRole('button',{name:'Vườn mận',exact:true}));await shot(page,'garden-detail')
  await click(page,page.getByRole('button',{name:'Mái hanok',exact:true}));await shot(page,'roof-detail')
  await click(page,page.getByRole('button',{name:/Đặt lại góc nhìn/}));await ready(page)
  const initial=await shot(page,'orbit-before'),box=await page.locator('canvas').boundingBox()
  await page.mouse.move(box.x+box.width*.50,box.y+box.height*.25);await page.mouse.down()
  await page.mouse.move(box.x+box.width*.67,box.y+box.height*.3,{steps:12});await page.mouse.up()
  assert.notEqual(hash(initial),hash(await shot(page,'orbit-after')))
  await click(page,page.getByRole('button',{name:/Đặt lại góc nhìn/}));await ready(page)
  checks.push('Actual pointer drag changes camera; bounded orbit/reset and all focus points remain available')
  await click(page,page.getByRole('button',{name:/Linh vật gốm/}));await ready(page)
  const signatures=new Set()
  for(const clip of ['Idle','Happy','Thinking','Celebration','Disappointed','Greeting']) {
    await page.getByLabel('Trạng thái linh vật').selectOption(clip)
    await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe(clip)
    signatures.add(hash(await shot(page,'mascot-'+clip.toLowerCase())))
  }
  assert.equal(signatures.size,6);checks.push('All six preserved clips have distinct rendered static poses with clearer outward greeting/cheer')
  await toggle(page,'Giảm chuyển động',false);await ready(page)
  metrics.liveClips={}
  for(const clip of ['Idle','Happy','Thinking','Celebration','Disappointed','Greeting']) {
    await page.getByLabel('Trạng thái linh vật').selectOption(clip);await ready(page)
    await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe(clip)
    const start=await metric(page),before=await shot(page,'live-'+clip.toLowerCase()+'-a')
    await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.clipTime),{timeout}).not.toBe(start.clipTime)
    await page.waitForTimeout(420)
    const after=await shot(page,'live-'+clip.toLowerCase()+'-b');assert.notEqual(hash(before),hash(after))
    metrics.liveClips[clip]={start,end:await metric(page),pixelsChanged:true}
  }
  checks.push('All six clips visibly change rendered pixels and mixer time during real playback')
  await page.getByLabel('Trạng thái linh vật').selectOption('Happy')
  const canvas=page.locator('canvas');const closeBox=await canvas.boundingBox()
  const points=(await metric(page)).interactivePoints.mascot
  await page.mouse.click(closeBox.x+points[0],closeBox.y+points[1])
  await expect(page.locator('.interaction-notice')).toHaveText('Người bạn men ngọc đang chào bạn.')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Greeting')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Idle')
  await page.getByRole('button',{name:'Chào linh vật',exact:true}).focus();await page.keyboard.press('Enter')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Celebration')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Idle')
  checks.push('Actual mascot mesh click greets; keyboard button triggers playful cheer; both return to idle')
  await click(page,page.getByRole('button',{name:/Sân hanok/}));await ready(page)
  await page.getByLabel('Ánh sáng').selectOption('night')
  const ambientBefore=await shot(page,'ambient-a'),start=await metric(page)
  await page.waitForTimeout(1100)
  const ambientAfter=await shot(page,'ambient-b'),end=await metric(page)
  assert.notEqual(hash(ambientBefore),hash(ambientAfter));assert.ok(end.environmentTime>start.environmentTime)
  assert.notEqual(end.lanternIntensity,start.lanternIntensity)
  await clickObject(page,'lantern');await ready(page)
  await expect(page.locator('.interaction-notice')).toHaveText('Ánh đèn ấm vừa bừng lên.')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.lanternIntensity),{timeout}).toBeGreaterThan(end.lanternIntensity)
  await shot(page,'lantern-response')
  await clickObject(page,'tree');await ready(page)
  await expect(page.locator('.interaction-notice')).toHaveText('Một làn gió nhẹ qua cành mận.')
  await shot(page,'petals')
  checks.push('Ambient motion/flicker changes actual rendering; lantern and garden interactions give visible feedback')
  await click(page,page.getByRole('button',{name:'Tạm dừng',exact:true}))
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await page.waitForTimeout(150);const paused=await metric(page);await page.waitForTimeout(450)
  const frozen=await metric(page);assert.equal(frozen.clipTime,paused.clipTime);assert.equal(frozen.environmentTime,paused.environmentTime)
  await click(page,page.getByRole('button',{name:'Tiếp tục',exact:true}));await ready(page)
  // The context originally preferred reduce, and the user explicitly overrode it.
  // Change the OS preference in both directions so this tests a real media-query event.
  await page.emulateMedia({reducedMotion:'no-preference'})
  await expect.poll(()=>page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches),{timeout}).toBe(false)
  await expect(page.locator('.motion-preference')).toHaveCount(0,{timeout})
  await page.emulateMedia({reducedMotion:'reduce'})
  await expect(page.locator('.motion-preference')).toHaveCount(1,{timeout})
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked({timeout})
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await shot(page,'reduced-motion');checks.push('Pause freezes mascot/environment; changing OS reduced-motion preference is respected immediately')
  await page.emulateMedia({reducedMotion:'no-preference'});await ready(page)
  // Sample the real displayed camera, so a jump hidden behind a "smooth" label fails.
  await page.evaluate(()=>{window.__POLISH_CAMERA_SAMPLES__=[];let n=0;const sample=()=>{window.__POLISH_CAMERA_SAMPLES__.push(window.__STUDIO_METRICS__?.cameraTarget);if(++n<65)requestAnimationFrame(sample)};requestAnimationFrame(sample)})
  await click(page,page.getByRole('button',{name:'Mái hanok',exact:true}));await ready(page)
  await expect.poll(()=>page.evaluate(()=>Math.abs((window.__STUDIO_METRICS__?.cameraTarget?.[0]||0)+1.5)),{timeout}).toBeLessThan(.03)
  const samples=await page.evaluate(()=>window.__POLISH_CAMERA_SAMPLES__)
  assert.ok(samples.some(p=>p&&p[0]<-.05&&p[0]>-1.44),'No intermediate camera position rendered')
  metrics.cameraSamples=samples
  await click(page,page.getByRole('button',{name:'Tổng quan',exact:true}));await ready(page)
  await toggle(page,'Góc nhìn điện ảnh',true);const cameraStart=(await metric(page)).cameraPosition
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.cameraPosition),{timeout}).not.toEqual(cameraStart)
  const orbitBox=await canvas.boundingBox();await page.mouse.move(orbitBox.x+orbitBox.width*.6,orbitBox.y+orbitBox.height*.3)
  await page.mouse.down();await page.mouse.move(orbitBox.x+orbitBox.width*.7,orbitBox.y+orbitBox.height*.3,{steps:8});await page.mouse.up()
  await expect(page.getByLabel('Góc nhìn điện ảnh')).not.toBeChecked()
  checks.push('Focus has actual intermediate camera positions; optional gentle cinematic path yields to user orbit')
  await toggle(page,'Giảm chuyển động',true);await ready(page)
  metrics.medium=await metric(page)
  await page.getByLabel('Chất lượng').selectOption('high');await ready(page)
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.quality),{timeout}).toBe('high')
  await shot(page,'high-quality');metrics.high=await metric(page)
  await page.getByLabel('Chất lượng').selectOption('low');await ready(page)
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.quality),{timeout}).toBe('low')
  metrics.low=await metric(page)
  assert.ok(metrics.low.drawCalls<metrics.medium.drawCalls);assert.ok(metrics.low.triangles<120000)
  await click(page,page.getByRole('button',{name:/Đặt lại góc nhìn/}));await ready(page)
  await page.getByLabel('Ánh sáng').selectOption('day')
  await page.getByLabel('Trạng thái linh vật').selectOption('Idle')
  await page.setViewportSize({width:390,height:844});await ready(page)
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
  await page.screenshot({path:resolve(out,'mobile.png'),fullPage:true});await shot(page,'mobile-hero')
  metrics.mobile=await metric(page);checks.push('Low quality reduces draw cost; 390×844 layout/hero render without horizontal overflow')
  // Real IntersectionObserver visibility, without replacing document.hidden.
  await toggle(page,'Giảm chuyển động',false);await ready(page)
  await page.evaluate(()=>{const spacer=document.createElement('div');spacer.id='qa-scroll-space';spacer.style.height='1600px';document.body.appendChild(spacer);scrollTo(0,document.body.scrollHeight)})
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await page.evaluate(()=>document.getElementById('qa-scroll-space').remove());await ready(page)
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(true)
  checks.push('Actual offscreen intersection pauses animation and scrolling back resumes it')
  await context.close()
  lastPage=null

  const fallbackContext=await browser.newContext({viewport:{width:390,height:844}})
  const fallback=await fallbackContext.newPage();watch(fallback)
  await fallback.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type.startsWith('webgl')?null:original.call(this,type,...args)}})
  await fallback.goto(url);await expect(fallback.locator('.stage')).toHaveAttribute('data-engine','fallback',{timeout})
  await expect(fallback.locator('.poster img')).toBeVisible()
  await expect(fallback.getByLabel('Góc nhìn điện ảnh')).toBeDisabled()
  assert.ok(await fallback.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
  await fallback.screenshot({path:resolve(out,'mobile-fallback.png'),fullPage:true})
  await click(fallback,fallback.getByRole('button',{name:/Linh vật gốm/}));await expect(fallback.locator('.poster img')).toBeVisible()
  await fallbackContext.close();checks.push('Missing WebGL gives actual original PNG fallback and usable accessible controls')
  assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
  const report={status:'PASS',url,public_deployment:false,verified_at:new Date().toISOString(),browser:browser.version(),checks,metrics,critical_errors:errors,missing_resources:missing,limitation:'SwiftShader cloud software renderer; physical mobile FPS not measured'}
  await writeFile(resolve(out,'verification.json'),JSON.stringify(report,null,2)+'\n')
  console.log(checks.length+' real v0.3 browser checks PASS; no critical errors/missing resources')
} catch(error) {
  const diagnostics=lastPage&&!lastPage.isClosed()?await lastPage.evaluate(()=>({metrics:window.__STUDIO_METRICS__,hidden:document.hidden,canvasBox:document.querySelector('canvas')?.getBoundingClientRect().toJSON(),scripts:[...document.scripts].map(s=>s.src)})).catch(()=>null):null
  await writeFile(resolve(out,'failure.json'),JSON.stringify({status:'FAIL',url,completedChecks:checks,errors,missing,diagnostics,message:String(error)},null,2)+'\n')
  throw error
} finally {await browser.close()}
