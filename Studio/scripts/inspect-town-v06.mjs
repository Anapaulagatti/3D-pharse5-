import {NodeIO} from '@gltf-transform/core'
import {ALL_EXTENSIONS} from '@gltf-transform/extensions'
import {readFile,writeFile} from 'node:fs/promises'
import {createHash} from 'node:crypto'
import {resolve} from 'node:path'
import validator from 'gltf-validator'
const root=resolve(import.meta.dirname,'../..'),io=new NodeIO().registerExtensions(ALL_EXTENSIONS),hash=b=>createHash('sha256').update(b).digest('hex'),assets=[]
for(const name of ['nari-chibi','letter-plaza']){
 const file=`exports/v0.6/models/${name}.glb`,source=`assets/v0.6/source-blend/${name}.blend`,bytes=await readFile(resolve(root,file)),doc=await io.readBinary(bytes),r=doc.getRoot(),validation=await validator.validateBytes(bytes,{uri:file});if(validation.issues.numErrors||validation.issues.numWarnings)throw Error('GLB validation must pass0/0')
 let triangles=0,primitives=0;for(const node of r.listNodes())for(const p of node.getMesh()?.listPrimitives()||[]){primitives++;triangles+=(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3}
 const animations=r.listAnimations().map(a=>({name:a.getName(),channels:a.listChannels().length,duration:Math.max(...a.listSamplers().map(s=>s.getInput().getMax([])[0]))}))
 assets.push({id:name,file,bytes:bytes.length,sha256:hash(bytes),source,source_sha256:hash(await readFile(resolve(root,source))),triangles,primitives,materials:r.listMaterials().length,textures:r.listTextures().length,skins:r.listSkins().map(s=>s.listJoints().length),morphs:[...new Set(r.listMeshes().flatMap(m=>m.getExtras().targetNames||[]))],animations,validation:{errors:0,warnings:0},license:'project-owned-original',provenance:'Approved B+T1, original Blender procedural authored geometry and adapted original controller/IK authoring; no external game assets.'})
}
const report={version:'0.6-prototype',status:'DATA_VERIFIED_RENDER_ACCEPTANCE_SEPARATE',assets,combined_glb_bytes:assets.reduce((s,a)=>s+a.bytes,0),combined_triangles:assets.reduce((s,a)=>s+a.triangles,0),optimization:'Geometry deliberately budgeted in Blender: continuous body decimation, shared static palette/material batches, low-segment curves/crowns, no PBR texture/decoder. glTF Transform used for structural/accessor/clip inspection. No lossy post-export simplification needed for this prototype.',public_release:'NOT_AUTHORIZED'}
await writeFile(resolve(root,'exports/v0.6/asset-manifest.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({assets:assets.map(a=>({id:a.id,bytes:a.bytes,triangles:a.triangles,primitives:a.primitives})),combined_bytes:report.combined_glb_bytes}))
