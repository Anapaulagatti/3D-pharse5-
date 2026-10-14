// Validate/version only new exports; every previous source/asset/artifact remains intact.
import {readFile,writeFile,mkdir} from 'node:fs/promises'
import {resolve} from 'node:path'
import {createHash} from 'node:crypto'
import {NodeIO} from '@gltf-transform/core'
import {ALL_EXTENSIONS} from '@gltf-transform/extensions'
import validator from 'gltf-validator'
const root=resolve(import.meta.dirname,'../..'),out=resolve(root,'quality-reports/v0.4');await mkdir(out,{recursive:true})
const hash=b=>createHash('sha256').update(b).digest('hex')
const baseline=JSON.parse(await readFile(resolve(out,'preserved-v03.json')))
for(const [file,a] of Object.entries(baseline.files)){const b=await readFile(resolve(root,file));if(b.length!==a.bytes||hash(b)!==a.sha256)throw Error('Approved file changed: '+file)}
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS),assets=[]
for(const id of ['mascot-living','hanok-living']){
 const file=`models/${id}.glb`,bytes=await readFile(resolve(root,'exports/v0.4',file)),doc=await io.read(resolve(root,'exports/v0.4',file))
 const report=await validator.validateBytes(new Uint8Array(bytes),{uri:file});await writeFile(resolve(out,id+'-validation.json'),JSON.stringify(report,null,2)+'\n')
 if(report.issues.numErrors||report.issues.numWarnings)throw Error(id+' Validator failure')
 let triangles=0,draws=0;for(const n of doc.getRoot().listNodes())for(const p of n.getMesh()?.listPrimitives()||[]){triangles+=(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3;draws++}
 const clips=doc.getRoot().listAnimations().map(a=>({name:a.getName(),channels:a.listChannels().length,duration_seconds:Math.max(...a.listSamplers().map(s=>Math.max(...s.getInput().getArray())))}))
 if(id==='mascot-living'){
  const names=['Idle','Walk','Run','Jump','Greeting','Happy','Thinking','Celebration','Disappointed','Curious','ClickReaction','ReturnToIdle']
  if(names.some(n=>!clips.some(c=>c.name===n))||clips.length!==12)throw Error('Expected 12 real exported clips')
  const nodes=doc.getRoot().listNodes().map(n=>n.getName());for(const n of ['LegLeftPivot','LegRightPivot','FaceFrown','FaceOpen','FaceBrowLeft','FaceHappyEyeLeft'])if(!nodes.includes(n))throw Error('Missing rig/face: '+n)
 }
 if(bytes.length>1_300_000 || triangles>28_000 || draws>(id==='mascot-living'?55:25))throw Error('Versioned asset budget exceeded: '+id+' '+bytes.length+' '+triangles+' '+draws)
 assets.push({id,type:'glb',file,version:'0.4.0',file_bytes:bytes.length,checksum_sha256:hash(bytes),license:'project-owned-original',origin:'original-versioned-studio-art',source_url:null,source_file:`../../assets/v0.4/source-blend/${id}.blend`,source_checksum_sha256:hash(await readFile(resolve(root,`assets/v0.4/source-blend/${id}.blend`))),generator_script:`../../Studio/modeling/${id==='mascot-living'?'mascot-v04':'hanok-v04'}.py`,animations:clips.map(c=>c.name),animation_details:clips,geometry:{totalTriangleCount:triangles,drawCallCount:draws,materialCount:doc.getRoot().listMaterials().length},validation:{errors:0,warnings:0},verified:true,purpose:id==='mascot-living'?'Independently articulated limbs, twelve readable full-body/face performances':'Complementary readable architecture, garden canopy, courtyard storytelling and silhouette depth',created_at:new Date().toISOString()})
 console.log(id,bytes.length+' bytes',triangles+' triangles',draws+' primitives',clips.map(c=>c.name).join(', '))
}
await writeFile(resolve(root,'exports/v0.4/asset-manifest.json'),JSON.stringify({version:'0.4.0',name:'Living Hanok Overhaul',base_manifest:'../v1/asset-manifest.json',detail_manifest:'../v0.3/asset-manifest.json',assets},null,2)+'\n')
await writeFile(resolve(out,'preservation-check.json'),JSON.stringify({status:'PASS',files_checked:Object.keys(baseline.files).length,baseline_commit:baseline.baseline_commit,checked_at:new Date().toISOString()},null,2)+'\n')
