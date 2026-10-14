// Portable fallback frame for zero-UV-area cap tangents, then lossless vertex weld.
import {NodeIO} from '@gltf-transform/core'
import {ALL_EXTENSIONS} from '@gltf-transform/extensions'
import {weld,dedup,prune,quantize} from '@gltf-transform/functions'
import {resolve} from 'node:path'
import {readFile,writeFile,mkdir} from 'node:fs/promises'
import {createHash} from 'node:crypto'
const root=resolve(import.meta.dirname,'../..'),file=resolve(root,'exports/v0.5/models/hanok-reforge.glb'),io=new NodeIO().registerExtensions(ALL_EXTENSIONS),before=await readFile(file),doc=await io.read(file),hash=b=>createHash('sha256').update(b).digest('hex')
let repairs=0
for(const m of doc.getRoot().listMeshes())for(const p of m.listPrimitives()){
 const t=p.getAttribute('TANGENT'),n=p.getAttribute('NORMAL');if(!t)continue
 const v=[],normal=[]
 for(let i=0;i<t.getCount();i++){
  t.getElement(i,v);let length=Math.hypot(v[0],v[1],v[2])
  if(length<.00001){
   n.getElement(i,normal);const a=Math.abs(normal[0])<.8?[1,0,0]:[0,1,0]
   v[0]=normal[1]*a[2]-normal[2]*a[1];v[1]=normal[2]*a[0]-normal[0]*a[2];v[2]=normal[0]*a[1]-normal[1]*a[0];length=Math.hypot(v[0],v[1],v[2]);repairs++
  }
  if(!Number.isFinite(length)||length<.00001)throw Error('Invalid surface normal; cannot construct tangent')
  v[0]/=length;v[1]/=length;v[2]/=length;v[3]=v[3]<0?-1:1;t.setElement(i,v)
 }
}
await doc.transform(weld({tolerance:0}),dedup(),prune({keepLeaves:true,keepAttributes:true,keepExtras:true}),quantize({quantizePosition:14,quantizeNormal:12,quantizeTexcoord:12,quantizeColor:8}),weld({tolerance:0}),dedup(),prune({keepLeaves:true,keepAttributes:true,keepExtras:true}))
await io.write(file,doc);const after=await readFile(file)
await mkdir(resolve(root,'quality-reports/v0.5/gate-d'),{recursive:true});await writeFile(resolve(root,'quality-reports/v0.5/gate-d/portable-tangents.json'),JSON.stringify({method:'For degenerate UV-area cap vertices, construct a unit tangent perpendicular to the exported normal; preserve handedness. Lossless exact-attribute weld/dedup/prune, then KHR_mesh_quantization: position14bit/normal12bit/UV12bit where normalized; tiled UVs remain float32. A second exact weld follows quantization. Submillimetre positions over this courtyard. Native Three support; no Draco/decoder, material or animation removal.',repairs,before:{bytes:before.length,sha256:hash(before)},after:{bytes:after.length,sha256:hash(after)}},null,2)+'\n');console.log('Portable tangent frames:',repairs,'bytes',before.length,'->',after.length)
