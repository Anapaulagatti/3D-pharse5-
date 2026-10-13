import { spawnSync } from 'node:child_process'
import { readFile, writeFile, mkdir, copyFile, stat } from 'node:fs/promises'
import { dirname, resolve, relative, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { NodeIO } from '@gltf-transform/core'
import { ALL_EXTENSIONS } from '@gltf-transform/extensions'
import validator from 'gltf-validator'

const studio = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const root = resolve(studio, '..')
const exportDir = resolve(root, 'exports/v1')
const reports = resolve(root, 'quality-reports')
const force = process.argv.includes('--regenerate')
const onlyPack = process.argv.includes('--pack-only')
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS)
const sha = (b) => createHash('sha256').update(b).digest('hex')
const run = (cmd, args) => {
  const p = spawnSync(cmd, args, { cwd: root, stdio: 'inherit' })
  if (p.error) throw p.error
  if (p.status !== 0) throw new Error(`${cmd} failed with status ${p.status}`)
}
async function exists(path) { try { return (await stat(path)).isFile() } catch { return false } }
async function validate(path, reportPath) {
  const bytes = await readFile(path)
  const report = await validator.validateBytes(new Uint8Array(bytes), { uri: path.slice(root.length + 1) })
  await writeFile(reportPath, JSON.stringify(report, null, 2) + '\n')
  if (report.issues.numErrors) throw new Error(`Validator errors: ${path}`)
  return report
}
function clips(doc) {
  return doc.getRoot().listAnimations().map(animation => {
    const samplers = animation.listSamplers()
    const max = Math.max(0, ...samplers.map(s => Math.max(...s.getInput().getArray())))
    const min = Math.min(0, ...samplers.map(s => Math.min(...s.getInput().getArray())))
    return { name: animation.getName(), duration_seconds: Number((max-min).toFixed(5)), channels: animation.listChannels().length }
  }).sort((a,b) => a.name.localeCompare(b.name))
}
function bounds(doc) {
  const min = [Infinity,Infinity,Infinity], max = [-Infinity,-Infinity,-Infinity]
  for (const node of doc.getRoot().listNodes()) {
    if (!node.getMesh()) continue
    const matrix = node.getWorldMatrix()
    for (const primitive of node.getMesh().listPrimitives()) {
      const a = primitive.getAttribute('POSITION')
      if (!a) continue
      const p = []
      for (let i=0;i<a.getCount();i++) {
        a.getElement(i,p)
        const world = [matrix[0]*p[0]+matrix[4]*p[1]+matrix[8]*p[2]+matrix[12],
          matrix[1]*p[0]+matrix[5]*p[1]+matrix[9]*p[2]+matrix[13],
          matrix[2]*p[0]+matrix[6]*p[1]+matrix[10]*p[2]+matrix[14]]
        for (let k=0;k<3;k++) { min[k]=Math.min(min[k],world[k]); max[k]=Math.max(max[k],world[k]) }
      }
    }
  }
  return { min: min.map(n=>Number(n.toFixed(4))), max: max.map(n=>Number(n.toFixed(4))),
    size: max.map((n,i)=>Number((n-min[i]).toFixed(4))) }
}
function sceneGeometry(doc) {
  // Validator counts serialized mesh resources. Dedup can share identical meshes,
  // so parity must compare geometry at each actual scene node, including instances.
  const nodes = doc.getRoot().listNodes().filter(n=>n.getMesh()).map(n=>({
    name:n.getName(),primitives:n.getMesh().listPrimitives().map(p=>({
      mode:p.getMode(),vertices:p.getAttribute('POSITION').getCount(),
      triangles:(p.getIndices()?.getCount() || p.getAttribute('POSITION').getCount())/3,
    })),
  })).sort((a,b)=>a.name.localeCompare(b.name))
  return { nodes,triangles:nodes.reduce((s,n)=>s+n.primitives.reduce((v,p)=>v+p.triangles,0),0),
    vertices:nodes.reduce((s,n)=>s+n.primitives.reduce((v,p)=>v+p.vertices,0),0),
    draw_calls:nodes.reduce((s,n)=>s+n.primitives.length,0) }
}
function animationData(doc) {
  return doc.getRoot().listAnimations().map(a=>({name:a.getName(),channels:a.listChannels().map(c=>{
    const s=c.getSampler()
    return {node:c.getTargetNode().getName(),path:c.getTargetPath(),interpolation:s.getInterpolation(),
      times:Array.from(s.getInput().getArray()),values:Array.from(s.getOutput().getArray())}
  }).sort((a,b)=>(a.node+a.path).localeCompare(b.node+b.path))})).sort((a,b)=>a.name.localeCompare(b.name))
}
await mkdir(resolve(exportDir,'models'), { recursive:true })
await mkdir(resolve(exportDir,'textures'), { recursive:true })
await mkdir(resolve(exportDir,'posters'), { recursive:true })
await mkdir(reports,{recursive:true})
const assets = []
for (const [id, script, purpose, expected] of [
  ['arena-hero','arena.py','Hanok Rooftop Arena',['LanternSway']],
  ['mascot-base','mascot.py','Ceramic Seed Spirit',['Idle','Happy','Thinking','Celebration','Disappointed','Greeting']],
]) {
  const sourceGLB = resolve(root,`assets/models/${id}.glb`)
  const blend = resolve(root,`assets/source-blend/${id}.blend`)
  if (!onlyPack && (force || !await exists(sourceGLB) || !await exists(blend))) {
    run(process.env.BLENDER_BIN || 'blender', ['--background','--factory-startup','--threads','4','--python',resolve(studio,'modeling',script)])
  }
  if (!await exists(sourceGLB) || !await exists(blend)) throw new Error(`Missing model/source: ${id}`)
  const original = await validate(sourceGLB,resolve(reports,`${id}-original-validation.json`))
  const before = await io.read(sourceGLB)
  const target = resolve(exportDir,`models/${id}.glb`)
  run(resolve(studio,'node_modules/.bin',process.platform === 'win32' ? 'gltf-transform.cmd' : 'gltf-transform'),[
    'optimize',sourceGLB,target,'--compress','false','--texture-compress','false','--simplify','false',
    '--flatten','false','--join','false','--instance','false','--palette','false','--prune-attributes','false','--weld','false','--resample','false',
  ])
  const after = await io.read(target)
  const optimized = await validate(target,resolve(reports,`${id}-validation.json`))
  const clipInfo = clips(after)
  if (JSON.stringify(clips(before)) !== JSON.stringify(clipInfo)) throw new Error(`Animation parity failure: ${id}`)
  if (JSON.stringify(animationData(before)) !== JSON.stringify(animationData(after))) throw new Error(`Animation sample data changed: ${id}`)
  for (const name of expected) if (!clipInfo.some(c=>c.name === name)) throw new Error(`Missing clip ${name} in ${id}`)
  const beforeGeometry=sceneGeometry(before), afterGeometry=sceneGeometry(after)
  if (JSON.stringify(beforeGeometry) !== JSON.stringify(afterGeometry)) throw new Error(`Scene node topology changed: ${id}`)
  if (JSON.stringify(bounds(before)) !== JSON.stringify(bounds(after))) throw new Error(`Scene bounds changed: ${id}`)
  const bytes = await readFile(target)
  const entry = { id,type:'glb',file:`models/${id}.glb`,version:'0.2.0',purpose,origin:'original-procedural',
    license:'project-owned-original',source_url:null,source_file:`../../assets/source-blend/${id}.blend`,
    generator_script:`../../Studio/modeling/${script}`,coordinate_system:'Y-up, meter-equivalent units, ground origin',
    dimensions:bounds(after),file_bytes:bytes.length,original_file_bytes:(await stat(sourceGLB)).size,
    checksum_sha256:sha(bytes),source_checksum_sha256:sha(await readFile(blend)),
    animations:clipInfo.map(c=>c.name),animation_details:clipInfo,
    geometry:{...optimized.info,serializedTriangleCount:optimized.info.totalTriangleCount,
      totalTriangleCount:afterGeometry.triangles,totalVertexCount:afterGeometry.vertices,drawCallCount:afterGeometry.draw_calls},
    textures:after.getRoot().listTextures().map(t=>({name:t.getName(),mime_type:t.getMimeType(),size:t.getSize()})),
    dependencies:[],verified:true,validation:{errors:optimized.issues.numErrors,warnings:optimized.issues.numWarnings},
    optimization:'Conservative glTF Transform optimize; no mesh simplification or required decoders; clip/topology parity checked',
    created_at:new Date().toISOString() }
  assets.push(entry)
}
for (const name of ['hanji-grain','courtyard-stone']) {
  const input=resolve(root,`assets/textures/${name}.png`),output=resolve(exportDir,`textures/${name}.png`)
  await copyFile(input,output)
  const bytes=await readFile(output)
  assets.push({id:name,type:'png',file:`textures/${name}.png`,version:'0.2.0',origin:'original-procedural',
    license:'project-owned-original',source_url:null,source_file:'../../Studio/modeling/common.py',
    dimensions:{width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)},file_bytes:bytes.length,
    checksum_sha256:sha(bytes),color_space:'sRGB',verified:true,animations:[],dependencies:[],created_at:new Date().toISOString()})
}
for (const name of ['arena-desktop','arena-mobile','mascot-transparent']) {
  const input=resolve(root,`assets/posters/${name}.png`)
  if (!await exists(input)) continue
  const output=resolve(exportDir,`posters/${name}.png`)
  await copyFile(input,output)
  const bytes=await readFile(output)
  assets.push({id:name,type:'png',file:`posters/${name}.png`,version:'0.2.0',origin:'original-3d-render',
    license:'project-owned-original',source_url:null,source_file:name==='mascot-transparent'?'../../Studio/modeling/render-mascot.py':'../../preview/tests/studio.spec.ts',
    dimensions:{width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)},file_bytes:bytes.length,checksum_sha256:sha(bytes),
    verified:true,animations:[],dependencies:[],created_at:new Date().toISOString()})
}
const manifest={version:'0.2.0',name:'The Living Hangeul District — golden slice',assets,
  missing_assets:['learning-alley','celebration-scene','six-additional-learning-districts'],
  limitations:['Physical-device GPU/FPS not verified','Scene polish is subject to visual review; not production-app integration'],
  generated_at:new Date().toISOString()}
await writeFile(resolve(exportDir,'asset-manifest.json'),JSON.stringify(manifest,null,2)+'\n')
const quote = (v) => '"'+String(v??'').replaceAll('"','""')+'"'
const header=['id','file','asset_type','version','origin','source_url','license','author','created_at','source_file','file_bytes','sha256','validated','notes']
await writeFile(resolve(root,'ASSET_MANIFEST.csv'),header.join(',')+'\n'+assets.map(a=>[
  a.id,`exports/v1/${a.file}`,a.type,a.version,a.origin,'',a.license,'Original Studio procedural artwork',a.created_at,
  relative(root,resolve(exportDir,a.source_file)).split(sep).join('/'),a.file_bytes,a.checksum_sha256,a.verified,a.optimization||a.color_space||'Actual original render',
].map(quote).join(',')).join('\n')+'\n')
await writeFile(resolve(reports,'asset-pipeline-summary.json'),JSON.stringify({assets:assets.filter(a=>a.type==='glb'),passed:true},null,2)+'\n')
console.log('Asset export pipeline PASS:',assets.map(a=>`${a.id}: ${a.file_bytes} bytes`).join(', '))
