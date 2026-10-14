// Real-time browser recording of the existing candidate. No accelerated animation or mock frames.
import { createRequire } from 'node:module'
import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..')
process.env.PLAYWRIGHT_BROWSERS_PATH ||= resolve(root,'Studio/.cache/playwright')
const req=createRequire(resolve(root,'preview/package.json'))
const {chromium,expect}=req('@playwright/test')
const dir=resolve(root,'quality-reports/v0.3/capture');await mkdir(dir,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const url=process.argv[2]||'http://127.0.0.1:4173/'
const records=[]
try {
  for(const scene of ['courtyard','mascot']) {
    const context=await browser.newContext({viewport:{width:1280,height:720},reducedMotion:'no-preference',recordVideo:{dir,size:{width:1280,height:720}}})
    const started=Date.now(),page=await context.newPage(),errors=[]
    page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(60_000)
    await page.goto(url);await expect(page.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout:60_000})
    await page.getByLabel('Chất lượng').selectOption(scene==='courtyard'?'medium':'low')
    if(scene==='mascot') {
      const button=page.getByRole('button',{name:/Linh vật gốm/});await button.evaluate(el=>el.scrollIntoView({block:'center'}))
      const box=await button.boundingBox();await page.mouse.click(box.x+box.width/2,box.y+box.height/2)
      await expect(page.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout:60_000})
    }
    await page.getByLabel('Ánh sáng').selectOption('day')
    await page.addStyleTag({content:'.intro,.topbar,.controls,.viewer-header,.viewer-footer,.interaction-bar,.asset-panel,.notes,.site-footer{display:none!important}.studio-shell{padding:0!important;max-width:none}.workspace{display:block;border:0}.viewer-section{padding:0!important}.stage{height:720px!important;border-radius:0}.stage-note{display:none}'})
    await page.locator('canvas').evaluate(el=>el.scrollIntoView({block:'start'}))
    await page.waitForTimeout(1200)
    const trimStart=(Date.now()-started)/1000,samples=[]
    const clickObject=async name=>{
      const m=await page.evaluate(()=>window.__STUDIO_METRICS__),box=await page.locator('canvas').boundingBox()
      const point=m.interactivePoints[name]
      await page.mouse.click(box.x+point[0],box.y+point[1])
      samples.push({time:Date.now(),object:name,metrics:await page.evaluate(()=>window.__STUDIO_METRICS__)})
    }
    await page.waitForTimeout(3200)
    if(scene==='courtyard') {
      // Choreograph the same native lighting control while its UI is hidden for filming.
      for(const lighting of ['evening','night']) {
        await page.getByLabel('Ánh sáng').evaluate((select,value)=>{select.value=value;select.dispatchEvent(new Event('change',{bubbles:true}))},lighting)
        await page.waitForTimeout(2000)
      }
    }
    await clickObject('mascot');await page.waitForTimeout(4000)
    if(scene==='courtyard') {await clickObject('lantern');await page.waitForTimeout(2500);await clickObject('tree');await page.waitForTimeout(4500)}
    else {await clickObject('mascot');await page.waitForTimeout(4300);await clickObject('mascot');await page.waitForTimeout(4000)}
    const canvas=page.locator('canvas'),box=await canvas.boundingBox()
    await page.screenshot({path:resolve(dir,scene+'-frame.png'),clip:box})
    const final=await page.evaluate(()=>window.__STUDIO_METRICS__)
    const video=page.video();await context.close()
    records.push({scene,path:await video.path(),trimStart,final,samples,errors})
    console.log(scene+' actual video captured; '+errors.length+' page errors')
  }
  await writeFile(resolve(dir,'capture.json'),JSON.stringify({url,records,animation_speed:'Original real-time browser playback; not retimed',renderer:'Cloud software GPU; not a physical-device FPS benchmark'},null,2)+'\n')
} finally {await browser.close()}
