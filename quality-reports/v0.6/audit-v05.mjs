// Read-only baseline. This does not build or mutate any v0.5 asset or release input.
import assert from 'node:assert/strict'
import {createRequire} from 'node:module'
import {readFile,writeFile,mkdir} from 'node:fs/promises'
import {createHash} from 'node:crypto'
import {resolve} from 'node:path'
const root=resolve(import.meta.dirname,'../..'),out=resolve(root,'quality-reports/v0.6/baseline')
await mkdir(out,{recursive:true})
const studio=createRequire(resolve(root,'Studio/package.json')),preview=createRequire(resolve(root,'preview/package.json'))
const {NodeIO}=studio('@gltf-transform/core'),{ALL_EXTENSIONS}=studio('@gltf-transform/extensions'),validator=studio('gltf-validator')
const assets=[]
for(const name of ['hanok-reforge','nari-messenger-art']){
 const file=`exports/v0.5/models/${name}.glb`,bytes=await readFile(resolve(root,file)),doc=await new NodeIO().registerExtensions(ALL_EXTENSIONS).readBinary(bytes),r=doc.getRoot()
 const validation=await validator.validateBytes(bytes,{uri:file})
 assert.equal(validation.issues.numErrors,0);assert.equal(validation.issues.numWarnings,0)
 let triangles=0,primitives=0
 for(const node of r.listNodes())for(const p of node.getMesh()?.listPrimitives()||[]){primitives++;triangles+=(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3}
 assets.push({file,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),triangles,primitives,materials:r.listMaterials().length,textures:r.listTextures().length,skins:r.listSkins().map(s=>s.listJoints().length),clips:r.listAnimations().map(a=>a.getName()),morphs:[...new Set(r.listMeshes().flatMap(m=>m.getExtras().targetNames||[]))],validation:{errors:0,warnings:0}})
 await writeFile(resolve(out,name+'-validator.json'),JSON.stringify(validation,null,2)+'\n')
}
await writeFile(resolve(out,'assets.json'),JSON.stringify({status:'PASS_READ_ONLY_GLTF_TRANSFORM_AND_VALIDATOR',assets,combined_bytes:assets.reduce((n,a)=>n+a.bytes,0),combined_triangles:assets.reduce((n,a)=>n+a.triangles,0)},null,2)+'\n')
const {chromium,expect:base}=preview('@playwright/test'),expect=base.configure({timeout:90000})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
const url='https://anapaulagatti.github.io/3D-pharse5-/?baseline=v06',errors=[],missing=[],states={}
try{
 const p=await browser.newPage({viewport:{width:1280,height:1100},reducedMotion:'reduce'});p.setDefaultTimeout(90000)
 p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()})})
 const response=await p.context().request.get(url),bytes=await response.body(),sha256=createHash('sha256').update(bytes).digest('hex')
 assert.equal(response.status(),200);assert.equal(sha256,'082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f')
 assert.equal((await p.goto(url)).status(),200)
 const stage=p.getByTestId('reforge-stage'),metrics=()=>p.evaluate(()=>window.__REFORGE_METRICS__)
 await expect(stage).toHaveAttribute('data-engine','ready')
 const shot=async name=>{await stage.evaluate(e=>e.scrollIntoView({block:'center'}));await p.screenshot({path:resolve(out,name+'.png'),clip:await stage.boundingBox()});states[name]=await metrics()}
 for(const q of ['low','medium','high']){
  await p.getByLabel('Chất lượng',{exact:true}).selectOption(q)
  await expect.poll(async()=> (await metrics()).draws).toBe(q==='low'?57:133)
  await shot('hero-'+q);console.log(q,states['hero-'+q].draws,states['hero-'+q].triangles)
 }
 await p.getByLabel('Chất lượng',{exact:true}).selectOption('low');await expect.poll(async()=> (await metrics()).draws).toBe(57)
 await p.getByLabel('Ánh sáng',{exact:true}).selectOption('night');await expect.poll(async()=> (await metrics()).lighting).toBe('night');await shot('hero-night')
 await p.getByLabel('Ánh sáng',{exact:true}).selectOption('day');await p.getByLabel('Chế độ',{exact:true}).selectOption('portrait');await expect(stage).toHaveAttribute('data-engine','ready');await shot('nari-v05')
 const renderer=await p.locator('canvas').evaluate(c=>{const gl=c.getContext('webgl2'),ext=gl.getExtension('WEBGL_debug_renderer_info');return {renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),version:gl.getParameter(gl.VERSION),buffer:[gl.drawingBufferWidth,gl.drawingBufferHeight]}})
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[])
 await writeFile(resolve(out,'browser.json'),JSON.stringify({status:'PASS_AWAITING_IMAGE_INSPECTION',url,checked_at:new Date().toISOString(),http:{status:200,bytes:bytes.length,sha256},viewport:{width:1280,height:1100},renderer,states,errors,missing,physical_device_fps:'NOT_MEASURED',limitation:'Read-only current public v0.5 baseline, static reduced-motion review. Draws/triangles include current relevant render passes; not v0.6 implementation or gameplay acceptance.'},null,2)+'\n')
}catch(e){await writeFile(resolve(out,'failure.json'),JSON.stringify({message:String(e),states,errors,missing},null,2)+'\n');throw e}finally{await browser.close()}
