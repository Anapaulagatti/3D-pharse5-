// Validate exact original art and preserve approved earlier assets. No regeneration.
import assert from 'node:assert/strict'
import {readFile,writeFile,mkdir} from 'node:fs/promises'
import {resolve} from 'node:path'
import {createHash} from 'node:crypto'
import {NodeIO} from '@gltf-transform/core'
import {ALL_EXTENSIONS} from '@gltf-transform/extensions'
import validator from 'gltf-validator'
const root=resolve(import.meta.dirname,'../..'),dir=resolve(root,'quality-reports/v0.5/gate-e');await mkdir(dir,{recursive:true})
const hash=b=>createHash('sha256').update(b).digest('hex'),baseline=JSON.parse(await readFile(resolve(root,'quality-reports/v0.5/preserved-v04.json')))
// Only two deployment inputs may change AFTER the v0.5 candidate passes and release
// is authorized; this pre-release pack still requires all75 baseline hashes intact.
for(const [file,a] of Object.entries(baseline.files)){const b=await readFile(resolve(root,file));assert.equal(hash(b),a.sha256,file+' preserved')}
const old=JSON.parse(await readFile(resolve(root,'exports/v0.5/asset-manifest.json'))),assets=old.assets.filter(a=>!['hanok-reforge','nari-messenger-art'].includes(a.id)),io=new NodeIO().registerExtensions(ALL_EXTENSIONS)
for(const id of ['hanok-reforge','nari-messenger-art']){
 const file='models/'+id+'.glb',bytes=await readFile(resolve(root,'exports/v0.5',file)),doc=await io.read(resolve(root,'exports/v0.5',file)),r=doc.getRoot(),report=await validator.validateBytes(new Uint8Array(bytes),{uri:file});await writeFile(resolve(dir,id+'-validation.json'),JSON.stringify(report,null,2)+'\n');assert.equal(report.issues.numErrors,0);assert.equal(report.issues.numWarnings,0)
 const ps=r.listMeshes().flatMap(m=>m.listPrimitives()),triangles=ps.reduce((n,p)=>n+(p.getIndices()?.getCount()||0)/3,0),clips=r.listAnimations().map(a=>({name:a.getName(),duration_seconds:Math.max(...a.listSamplers().map(s=>Math.max(...s.getInput().getArray()))),channels:a.listChannels().length}))
 for(const t of r.listTextures()){assert.ok(t.getImage()?.length);assert.ok(t.getMimeType()==='image/png');const z=t.getSize();assert.ok(z[0]<=256&&z[1]<=256)}
 for(const p of ps)if(p.getMaterial()?.getBaseColorTexture()||p.getMaterial()?.getNormalTexture()){assert.ok(p.getAttribute('TEXCOORD_0'));if(p.getMaterial()?.getNormalTexture())assert.ok(p.getAttribute('TANGENT'))}
 if(id==='nari-messenger-art'){
  assert.equal(r.listSkins().length,1);assert.equal(r.listSkins()[0].listJoints().length,28);assert.equal(clips.length,20);assert.ok(triangles<=24000);assert.ok(bytes.length<3.5*1024**2)
  for(const p of ps){assert.ok(p.getAttribute('JOINTS_0'));const weights=p.getAttribute('WEIGHTS_0');assert.ok(weights);const arr=weights.getArray();for(let i=0;i<arr.length;i+=4)assert.ok(Math.abs(arr[i]+arr[i+1]+arr[i+2]+arr[i+3]-1)<.00002)}
  assert.ok(ps.some(p=>p.listTargets().length===10))
 }else{assert.deepEqual(new Set(clips.map(c=>c.name)),new Set(['GardenWind','LanternBreeze','BannerWind']));assert.ok(triangles<80000);assert.ok(bytes.length<6*1024**2)}
 const source=`../../assets/v0.5/source-blend/${id}.blend`
 assets.push({id,type:'glb',file,version:'0.5.0',file_bytes:bytes.length,checksum_sha256:hash(bytes),source_file:source,source_checksum_sha256:hash(await readFile(resolve(root,'exports/v0.5',source))),generator_script:`../../Studio/modeling/${id.startsWith('nari')?'nari-v05.py -- --art':'hanok-v05.py'}`,license:'project-owned-original',source_url:null,geometry:{triangles,primitives:ps.length,materials:r.listMaterials().length,textures:r.listTextures().length},animations:clips.map(c=>c.name),animation_details:clips,validation:{errors:0,warnings:0},status:'verified-data; see rendered acceptance reports'})
 console.log(id,bytes.length,'bytes',triangles,'triangles',ps.length,'primitives',clips.length,'clips')
}
await writeFile(resolve(root,'exports/v0.5/asset-manifest.json'),JSON.stringify({version:'0.5.0',name:'Joseon Fantasy Reforge',assets},null,2)+'\n')
const structure=JSON.parse(await readFile(resolve(root,'exports/v0.5/hanok-reforge-structure.json')));await writeFile(resolve(root,'exports/v0.5/collision-world.json'),JSON.stringify({colliders:structure.colliders,bounds_contract:structure.bounds_contract})+'\n')
await writeFile(resolve(dir,'preservation-check.json'),JSON.stringify({status:'PASS',files_checked:Object.keys(baseline.files).length,baseline:baseline.baseline_commit,checked_at:new Date().toISOString()},null,2)+'\n')
