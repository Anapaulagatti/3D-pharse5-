// Read-only check for setup/recovery: never regenerate approved art or rewrite manifests.
import { readFile } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { NodeIO } from '@gltf-transform/core'
import { ALL_EXTENSIONS } from '@gltf-transform/extensions'
import validator from 'gltf-validator'

const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..')
const manifest=JSON.parse(await readFile(resolve(root,'exports/v1/asset-manifest.json'),'utf8'))
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS)
for(const asset of manifest.assets){
  const path=resolve(root,'exports/v1',asset.file)
  if(!path.startsWith(resolve(root,'exports/v1')+'/')) throw new Error('Export path escapes directory')
  const bytes=await readFile(path)
  if(bytes.length!==asset.file_bytes || createHash('sha256').update(bytes).digest('hex')!==asset.checksum_sha256){
    throw new Error(`Checksum/size mismatch: ${asset.id}`)
  }
  if(asset.type==='glb'){
    const report=await validator.validateBytes(new Uint8Array(bytes),{uri:asset.file})
    if(report.issues.numErrors) throw new Error(`Invalid GLB: ${asset.id}`)
    const doc=await io.read(path)
    const clips=doc.getRoot().listAnimations().map(a=>a.getName()).sort()
    if(JSON.stringify(clips)!==JSON.stringify([...asset.animations].sort())) throw new Error(`Clip mismatch: ${asset.id}`)
    const blend=await readFile(resolve(root,'exports/v1',asset.source_file))
    if(blend.subarray(0,7).toString()!=='BLENDER') throw new Error(`Invalid editable Blender source: ${asset.id}`)
    if(createHash('sha256').update(blend).digest('hex')!==asset.source_checksum_sha256) throw new Error(`Source changed without repacking manifest: ${asset.id}`)
    console.log(asset.id, bytes.length,'bytes; clips:',clips.join(', '),'; validator:',report.issues.numErrors,'errors,',report.issues.numWarnings,'warnings')
  }else if(asset.type==='png'){
    if(bytes.subarray(0,8).toString('hex')!=='89504e470d0a1a0a') throw new Error(`Invalid PNG: ${asset.id}`)
    if(bytes.readUInt32BE(16)!==asset.dimensions.width || bytes.readUInt32BE(20)!==asset.dimensions.height) throw new Error(`Image size mismatch: ${asset.id}`)
  }
}
console.log(`Read-only asset verification PASS: ${manifest.assets.length} actual exports`)
