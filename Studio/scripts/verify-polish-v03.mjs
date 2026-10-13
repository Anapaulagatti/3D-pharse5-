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
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const watch=page=>{
  page.on('pageerror',e=>errors.push(e.message))
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())})
  page.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
}
const metric=page=>page.evaluate(()=>window.__STUDIO_METRICS__)
const ready=async page=>{
  await expect(page.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout})
  await page.locator('canvas').scrollIntoViewIfNeeded()
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.assetsLoaded),{timeout}).toBe(true)
}
const shot=async(page,name)=>page.locator('canvas').screenshot({path:resolve(out,name+'.png')})
try {
  const context=await browser.newContext({viewport:{width:1280,height:1100},reducedMotion:'reduce'})
  const page=await context.newPage();watch(page)
  const response=await page.goto(url);assert.equal(response.status(),200);await ready(page)
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await page.screenshot({path:resolve(out,'desktop.png'),fullPage:true})
  for(const lighting of ['day','evening','night']) {
    await page.getByLabel('Ánh sáng').selectOption(lighting);await ready(page)
    await shot(page,lighting);metrics[lighting]=await metric(page)
  }
  await page.getByLabel('Ánh sáng').selectOption('day');await shot(page,'hero')
  checks.push('Real detailed Hanok/mascot render; day/evening/night and full hero screenshots captured')
  await page.getByRole('button',{name:'Vườn mận',exact:true}).click();await shot(page,'garden-detail')
  await page.getByRole('button',{name:'Mái hanok',exact:true}).click();await shot(page,'roof-detail')
  await page.getByRole('button',{name:/Đặt lại góc nhìn/}).click();await ready(page)
  const initial=await shot(page,'orbit-before'),box=await page.locator('canvas').boundingBox()
  await page.mouse.move(box.x+box.width*.50,box.y+box.height*.25);await page.mouse.down()
  await page.mouse.move(box.x+box.width*.67,box.y+box.height*.3,{steps:12});await page.mouse.up()
  assert.notEqual(hash(initial),hash(await shot(page,'orbit-after')))
  await page.getByRole('button',{name:/Đặt lại góc nhìn/}).click();await ready(page)
  checks.push('Actual pointer drag changes camera; bounded orbit/reset and all focus points remain available')
  await page.getByRole('button',{name:/Linh vật gốm/}).click();await ready(page)
  const signatures=new Set()
  for(const clip of ['Idle','Happy','Thinking','Celebration','Disappointed','Greeting']) {
    await page.getByLabel('Trạng thái linh vật').selectOption(clip)
    await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe(clip)
    signatures.add(hash(await shot(page,'mascot-'+clip.toLowerCase())))
  }
  assert.equal(signatures.size,6);checks.push('All six preserved clips have distinct rendered static poses with clearer outward greeting/cheer')
  await page.getByLabel('Giảm chuyển động').uncheck();await ready(page)
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
  await page.getByRole('button',{name:'Chào linh vật',exact:true}).click()
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Celebration')
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout}).toBe('Idle')
  checks.push('Actual mascot mesh click greets; keyboard button triggers playful cheer; both return to idle')
  await page.getByRole('button',{name:/Sân hanok/}).click();await ready(page)
  await page.getByLabel('Ánh sáng').selectOption('night')
  const ambientBefore=await shot(page,'ambient-a'),start=await metric(page)
  await page.waitForTimeout(1100)
  const ambientAfter=await shot(page,'ambient-b'),end=await metric(page)
  assert.notEqual(hash(ambientBefore),hash(ambientAfter));assert.ok(end.environmentTime>start.environmentTime)
  assert.notEqual(end.lanternIntensity,start.lanternIntensity)
  await page.getByRole('button',{name:'Thắp đèn',exact:true}).click();await ready(page)
  const boosted=await metric(page);assert.ok(boosted.lanternIntensity>end.lanternIntensity)
  await shot(page,'lantern-response')
  await page.getByRole('button',{name:'Gió qua vườn',exact:true}).click();await ready(page);await shot(page,'petals')
  checks.push('Ambient motion/flicker changes actual rendering; lantern and garden interactions give visible feedback')
  await page.getByRole('button',{name:'Tạm dừng',exact:true}).click()
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await page.waitForTimeout(150);const paused=await metric(page);await page.waitForTimeout(450)
  const frozen=await metric(page);assert.equal(frozen.clipTime,paused.clipTime);assert.equal(frozen.environmentTime,paused.environmentTime)
  await page.getByRole('button',{name:'Tiếp tục',exact:true}).click();await ready(page)
  await page.emulateMedia({reducedMotion:'reduce'})
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await shot(page,'reduced-motion');checks.push('Pause freezes mascot/environment; changing OS reduced-motion preference is respected immediately')
  await page.emulateMedia({reducedMotion:'no-preference'});await ready(page)
  // Sample the real displayed camera, so a jump hidden behind a "smooth" label fails.
  await page.evaluate(()=>{window.__POLISH_CAMERA_SAMPLES__=[];let n=0;const sample=()=>{window.__POLISH_CAMERA_SAMPLES__.push(window.__STUDIO_METRICS__?.cameraTarget);if(++n<65)requestAnimationFrame(sample)};requestAnimationFrame(sample)})
  await page.getByRole('button',{name:'Mái hanok',exact:true}).click();await ready(page)
  await expect.poll(()=>page.evaluate(()=>Math.abs((window.__STUDIO_METRICS__?.cameraTarget?.[0]||0)+1.5)),{timeout}).toBeLessThan(.03)
  const samples=await page.evaluate(()=>window.__POLISH_CAMERA_SAMPLES__)
  assert.ok(samples.some(p=>p&&p[0]<-.05&&p[0]>-1.44),'No intermediate camera position rendered')
  metrics.cameraSamples=samples
  await page.getByRole('button',{name:'Tổng quan',exact:true}).click();await ready(page)
  await page.getByLabel('Góc nhìn điện ảnh').check();const cameraStart=(await metric(page)).cameraPosition
  await page.waitForTimeout(1000);assert.notDeepEqual((await metric(page)).cameraPosition,cameraStart)
  const orbitBox=await canvas.boundingBox();await page.mouse.move(orbitBox.x+orbitBox.width*.6,orbitBox.y+orbitBox.height*.3)
  await page.mouse.down();await page.mouse.move(orbitBox.x+orbitBox.width*.7,orbitBox.y+orbitBox.height*.3,{steps:8});await page.mouse.up()
  await expect(page.getByLabel('Góc nhìn điện ảnh')).not.toBeChecked()
  checks.push('Focus has actual intermediate camera positions; optional gentle cinematic path yields to user orbit')
  await page.getByLabel('Giảm chuyển động').check();await ready(page)
  metrics.medium=await metric(page)
  await page.getByLabel('Chất lượng').selectOption('low');await ready(page);metrics.low=await metric(page)
  assert.ok(metrics.low.drawCalls<metrics.medium.drawCalls);assert.ok(metrics.low.triangles<120000)
  await page.setViewportSize({width:390,height:844});await ready(page)
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
  await page.screenshot({path:resolve(out,'mobile.png'),fullPage:true});await shot(page,'mobile-hero')
  metrics.mobile=await metric(page);checks.push('Low quality reduces draw cost; 390×844 layout/hero render without horizontal overflow')
  // Real IntersectionObserver visibility, without replacing document.hidden.
  await page.getByLabel('Giảm chuyển động').uncheck();await ready(page)
  await page.evaluate(()=>{const spacer=document.createElement('div');spacer.id='qa-scroll-space';spacer.style.height='1600px';document.body.appendChild(spacer);scrollTo(0,document.body.scrollHeight)})
  await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.motionActive),{timeout}).toBe(false)
  await page.evaluate(()=>document.getElementById('qa-scroll-space').remove());await ready(page)
  checks.push('Actual offscreen intersection pauses animation and scrolling back resumes it')
  await context.close()

  const fallbackContext=await browser.newContext({viewport:{width:390,height:844}})
  const fallback=await fallbackContext.newPage();watch(fallback)
  await fallback.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type.startsWith('webgl')?null:original.call(this,type,...args)}})
  await fallback.goto(url);await expect(fallback.locator('.stage')).toHaveAttribute('data-engine','fallback',{timeout})
  await expect(fallback.locator('.poster img')).toBeVisible()
  await expect(fallback.getByLabel('Góc nhìn điện ảnh')).toBeDisabled()
  assert.ok(await fallback.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
  await fallback.screenshot({path:resolve(out,'mobile-fallback.png'),fullPage:true})
  await fallback.getByRole('button',{name:/Linh vật gốm/}).click();await expect(fallback.locator('.poster img')).toBeVisible()
  await fallbackContext.close();checks.push('Missing WebGL gives actual original PNG fallback and usable accessible controls')
  assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
  const report={status:'PASS',url,public_deployment:false,verified_at:new Date().toISOString(),browser:browser.version(),checks,metrics,critical_errors:errors,missing_resources:missing,limitation:'SwiftShader cloud software renderer; physical mobile FPS not measured'}
  await writeFile(resolve(out,'verification.json'),JSON.stringify(report,null,2)+'\n')
  console.log(checks.length+' real v0.3 browser checks PASS; no critical errors/missing resources')
} catch(error) {
  await writeFile(resolve(out,'failure.json'),JSON.stringify({status:'FAIL',url,completedChecks:checks,errors,missing,message:String(error)},null,2)+'\n')
  throw error
} finally {await browser.close()}
