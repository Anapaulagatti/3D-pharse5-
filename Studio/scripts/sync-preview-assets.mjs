import { copyFile, mkdir, readFile } from 'node:fs/promises'
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
console.log('Synced',manifest.assets.length,'verified export assets to preview/public/')
