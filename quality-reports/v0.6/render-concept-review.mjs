import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,readFile,writeFile} from 'node:fs/promises'
import assert from 'node:assert/strict'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium,expect}=req('@playwright/test')
const browser=await chromium.launch({executablePath:'/usr/bin/chromium'}),errors=[],requests=[]
try{
 const p=await browser.newPage({viewport:{width:1440,height:1000}})
 p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('request',r=>{if(!r.url().startsWith('data:'))requests.push(r.url())})
 // Static report only: image embedding and DOM/PDF review do not require WebGL.
 await p.setContent(await readFile(resolve(root,'quality-reports/v0.6/concept-review.html'),'utf8'),{waitUntil:'load'})
 const images=await p.locator('img').evaluateAll(a=>a.map(i=>({alt:i.alt,width:i.naturalWidth,height:i.naturalHeight})))
 assert.equal(images.length,5);assert.ok(images.every(i=>i.width>0&&i.height>0))
 await p.screenshot({path:resolve(root,'quality-reports/v0.6/review-desktop.png'),fullPage:true})
 await mkdir(resolve(root,'downloads/v0.6'),{recursive:true})
 await p.pdf({path:resolve(root,'downloads/v0.6/playful-hangeul-town-concepts.pdf'),printBackground:true,preferCSSPageSize:true})
 await p.setViewportSize({width:390,height:844});await p.screenshot({path:resolve(root,'quality-reports/v0.6/review-mobile.png'),fullPage:true})
 assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))
 assert.deepEqual(errors,[]);assert.deepEqual(requests,[])
 await writeFile(resolve(root,'quality-reports/v0.6/report-render.json'),JSON.stringify({status:'PASS_REVIEW_DOCUMENT_LAYOUT_PENDING_IMAGE_INSPECTION',document:'concept-review.html',images,checks:['5 actual embedded PNGs decoded','Desktop document screenshot and landscape PDF created','390px document has no horizontal overflow','Zero JavaScript/console errors and zero external requests'],errors,requests,limitation:'Concept review document only; not a v0.6 WebGL scene, prototype, animation, performance or gameplay check.'},null,2)+'\n');console.log('Review document render PASS; 5 embedded images, desktop/mobile/PDF, no external resources.')
}finally{await browser.close()}
