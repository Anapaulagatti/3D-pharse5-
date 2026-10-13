// Package/validate only the new additive layer. Approved v0.2 files are read-only.
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { NodeIO } from '@gltf-transform/core'
import { ALL_EXTENSIONS } from '@gltf-transform/extensions'
import validator from 'gltf-validator'

const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..')
const reportDir=resolve(root,'quality-reports/v0.3')
await mkdir(reportDir,{recursive:true})
const sha=b=>createHash('sha256').update(b).digest('hex')
const preserve=JSON.parse(await readFile(resolve(reportDir,'preserved-v02.json'),'utf8'))
for(const [file,expected] of Object.entries(preserve.files)) {
  const bytes=await readFile(resolve(root,file))
  if(bytes.length!==expected.bytes || sha(bytes)!==expected.sha256) throw new Error('Approved v0.2 changed: '+file)
}
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS)
const path=resolve(root,'exports/v0.3/models/hanok-polish.glb')
const bytes=await readFile(path)
const doc=await io.read(path)
const report=await validator.validateBytes(new Uint8Array(bytes),{uri:'models/hanok-polish.glb'})
await writeFile(resolve(reportDir,'hanok-polish-validation.json'),JSON.stringify(report,null,2)+'\n')
if(report.issues.numErrors || report.issues.numWarnings)throw new Error('New GLB validation failed')
let triangles=0, draws=0
for(const node of doc.getRoot().listNodes())for(const p of node.getMesh()?.listPrimitives()||[]) {
  triangles+=(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3
  draws++
}
const clips=doc.getRoot().listAnimations().map(a=>({name:a.getName(),channels:a.listChannels().length,
  duration_seconds:Math.max(...a.listSamplers().map(s=>Math.max(...s.getInput().getArray())))}))
if(!clips.some(a=>a.name==='GardenBreeze'))throw new Error('Missing wind animation')
const asset={id:'hanok-polish',type:'glb',file:'models/hanok-polish.glb',version:'0.3.0',
  purpose:'Additive handcrafted Hanok architecture, courtyard, plum foliage and distant silhouettes',
  origin:'original-procedural',license:'project-owned-original',source_url:null,
  source_file:'../../assets/v0.3/source-blend/hanok-polish.blend',generator_script:'../../Studio/modeling/polish-v03.py',
  source_checksum_sha256:sha(await readFile(resolve(root,'assets/v0.3/source-blend/hanok-polish.blend'))),
  file_bytes:bytes.length,checksum_sha256:sha(bytes),animations:clips.map(a=>a.name),animation_details:clips,
  geometry:{totalTriangleCount:triangles,drawCallCount:draws,materialCount:doc.getRoot().listMaterials().length},
  textures:[],dependencies:[],verified:true,validation:{errors:0,warnings:0},
  coordinate_system:'Y-up, world origin matches the preserved arena-hero GLB',created_at:new Date().toISOString()}
if(bytes.length>750_000 || triangles>18_000 || draws>24)throw new Error('Detail-layer budget exceeded: '+JSON.stringify(asset.geometry))
await writeFile(resolve(root,'exports/v0.3/asset-manifest.json'),JSON.stringify({version:'0.3.0',name:'Living Hanok — additive polish layer',base_manifest:'../v1/asset-manifest.json',assets:[asset]},null,2)+'\n')
await writeFile(resolve(reportDir,'preservation-check.json'),JSON.stringify({status:'PASS',files_checked:Object.keys(preserve.files).length,baseline_commit:preserve.baseline_commit,checked_at:new Date().toISOString()},null,2)+'\n')
console.log('v0.3 asset PASS:',asset.file_bytes,'bytes;',triangles,'triangles;',draws,'draw primitives; original files unchanged')
