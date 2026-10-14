import { copyFile, mkdir, readFile, cp } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..')
const exportDir=resolve(root,'exports/v1')
const publicDir=resolve(root,'preview/public')
const manifest=JSON.parse(await readFile(resolve(exportDir,'asset-manifest.json'),'utf8'))
for (const asset of manifest.assets) {
  const destination=resolve(publicDir,asset.file)
  if (!destination.startsWith(publicDir+'/')) throw new Error('Asset path must stay inside public/')
  await mkdir(dirname(destination),{recursive:true})
  await copyFile(resolve(exportDir,asset.file),destination)
}
await mkdir(resolve(publicDir,'assets'),{recursive:true})
await copyFile(resolve(exportDir,'asset-manifest.json'),resolve(publicDir,'assets/asset-manifest.json'))
const polishDir=resolve(root,'exports/v0.3')
const polish=JSON.parse(await readFile(resolve(polishDir,'asset-manifest.json'),'utf8'))
for(const asset of polish.assets) {
  const destination=resolve(publicDir,'v0.3',asset.file)
  if(!destination.startsWith(publicDir+'/v0.3/'))throw new Error('Invalid polish asset path')
  await mkdir(dirname(destination),{recursive:true})
  await copyFile(resolve(polishDir,asset.file),destination)
}
console.log('Synced',manifest.assets.length,'preserved base assets and',polish.assets.length,'v0.3 detail asset to preview/public/')

const livingDir=resolve(root,'exports/v0.4')
const living=JSON.parse(await readFile(resolve(livingDir,'asset-manifest.json'),'utf8'))
for(const asset of living.assets){
  const destination=resolve(publicDir,'v0.4',asset.file)
  if(!destination.startsWith(publicDir+'/v0.4/'))throw new Error('Invalid v0.4 asset path')
  await mkdir(dirname(destination),{recursive:true});await copyFile(resolve(livingDir,asset.file),destination)
}
console.log('Synced',living.assets.length,'versioned v0.4 assets')

const reforgeDir=resolve(root,'exports/v0.5')
if(existsSync(reforgeDir)){
  await cp(reforgeDir,resolve(publicDir,'v0.5'),{recursive:true})
  console.log('Synced separate v0.5 candidate exports; no Blender/private source copied')
}
