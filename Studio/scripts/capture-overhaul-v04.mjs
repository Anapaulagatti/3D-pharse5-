// Capture actual composited Chromium frames AFTER readiness; preserve real CDP timestamps.
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,writeFile} from 'node:fs/promises'
import assert from 'node:assert/strict'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json'))
const {chromium,expect}=req('@playwright/test'),dir=resolve(root,'quality-reports/v0.4/capture');await mkdir(dir,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const context=await browser.newContext({viewport:{width:1280,height:720},reducedMotion:'no-preference'})
const page=await context.newPage(),errors=[],frames=[],samples=[],writes=[]
page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())})
const url=process.argv[2]||'http://127.0.0.1:4184/'
const ready=async()=>{await expect(page.locator('.stage')).toHaveAttribute('data-engine','ready',{timeout:60_000});await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.assetsLoaded),{timeout:60_000}).toBe(true)}
const click=async locator=>{await locator.evaluate(e=>e.scrollIntoView({block:'center'}));const b=await locator.boundingBox();await page.mouse.click(b.x+b.width/2,b.y+b.height/2)}
try{
 await page.goto(url);await ready();await page.getByLabel('Chất lượng').selectOption('low')
 await click(page.getByRole('button',{name:/Linh vật gốm/}));await ready();await page.getByLabel('Trạng thái linh vật').selectOption('Idle')
 await page.addStyleTag({content:'.intro,.topbar,.controls,.viewer-header,.viewer-footer,.interaction-bar,.performance-actions,.asset-panel,.notes,.site-footer,.stage-note{display:none!important}.studio-shell{padding:0!important;max-width:none}.workspace{display:block;border:0}.viewer-section{padding:0!important}.stage{height:720px!important;border-radius:0}.stage.mobile-frame{max-width:none;width:100%}'})
 await page.locator('canvas').evaluate(e=>e.scrollIntoView({block:'start'}));await page.waitForTimeout(600)
 // A film caption reads the genuine native select; it does not alter character state/rendering.
 await page.evaluate(()=>{const caption=document.createElement('div');caption.style.cssText='position:fixed;left:24px;bottom:22px;background:#fffefaD9;color:#355e51;padding:9px 15px;border-radius:6px;font:15px sans-serif';caption.id='film-caption';document.body.appendChild(caption);window.__FILM_CAPTION_TIMER__=setInterval(()=>{const select=[...document.querySelectorAll('select')].find(s=>s.options[0]?.value==='Idle');caption.textContent=select?.selectedOptions[0]?.textContent||'Living Hanok'},100)})
 const client=await context.newCDPSession(page)
 client.on('Page.screencastFrame',event=>{
  const index=frames.length,file='frame-'+String(index).padStart(5,'0')+'.jpg'
  frames.push({file,timestamp:event.metadata.timestamp});writes.push(writeFile(resolve(dir,file),Buffer.from(event.data,'base64')))
  client.send('Page.screencastFrameAck',{sessionId:event.sessionId}).catch(e=>errors.push(e.message))
 })
 await client.send('Page.startScreencast',{format:'jpeg',quality:90,maxWidth:1280,maxHeight:720,everyNthFrame:1})
 for(const [clip,ms] of [['Idle',1600],['Walk',3600],['Run',3000],['Jump',2800],['Greeting',2500],['Happy',2200],['Thinking',2400],['Disappointed',2200],['Curious',2300],['Celebration',3500],['ClickReaction',2200],['ReturnToIdle',1600]]){
  await page.getByLabel('Trạng thái linh vật').selectOption(clip);await expect.poll(()=>page.evaluate(()=>window.__STUDIO_METRICS__?.activeClip),{timeout:60_000}).toBe(clip)
  samples.push({clip,firstFrame:frames.length,selected_at:Date.now(),metrics:await page.evaluate(()=>window.__STUDIO_METRICS__)})
  await page.waitForTimeout(ms)
 }
 await client.send('Page.stopScreencast');await Promise.all(writes)
 assert.deepEqual(errors,[]);assert.ok(frames.length>=20,'Insufficient actual compositor frames');assert.ok(frames.every(f=>Number.isFinite(f.timestamp)))
 await writeFile(resolve(dir,'capture.json'),JSON.stringify({status:'CAPTURED',url,frames,samples,errors,method:'Native Chromium CDP compositor JPEG frames captured only after real GLB readiness; timestamps preserved; no animation override, synthetic image or motion interpolation',renderer:'Cloud SwiftShader; physical device FPS unmeasured'},null,2)+'\n')
 console.log(frames.length+' actual composited frames captured, twelve native animation states, no browser errors')
}finally{await context.close();await browser.close()}
