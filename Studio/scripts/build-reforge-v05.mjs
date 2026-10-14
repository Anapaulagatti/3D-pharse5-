// Build only the reviewed Reforge app. Does not import/regenerate legacy scenes.
import {createHash} from 'node:crypto'
import {mkdir,readFile,writeFile} from 'node:fs/promises'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {pathToFileURL} from 'node:url'
const root=resolve(import.meta.dirname,'../..'),preview=resolve(root,'preview'),req=createRequire(resolve(preview,'package.json')),hash=b=>createHash('sha256').update(b).digest('hex')
if(!process.argv.includes('--candidate'))throw Error('Use --candidate after actual v0.5 source and art verification')
const {build}=await import(pathToFileURL(req.resolve('vite')).href),{default:react}=await import(pathToFileURL(req.resolve('@vitejs/plugin-react')).href)
const manifest=JSON.parse(await readFile(resolve(root,'exports/v0.5/asset-manifest.json'))),old=JSON.parse(await readFile(resolve(root,'exports/v1/asset-manifest.json'))),embedded={},records=[]
for(const [key,id,dir] of [['house','hanok-reforge','exports/v0.5'],['nari','nari-messenger-art','exports/v0.5'],['poster','hanok-day','exports/v0.5'],['legacy','mascot-base','exports/v1']]){
 const asset=[...manifest.assets,...old.assets].find(a=>a.id===id);if(!asset)throw Error('Missing verified asset '+id)
 const file=resolve(root,dir,asset.file);if(!file.startsWith(resolve(root,dir)+'/'))throw Error('Invalid asset path')
 const b=await readFile(file);if(b.length!==asset.file_bytes||hash(b)!==asset.checksum_sha256)throw Error('Unverified bytes '+id)
 embedded[key]={mime:asset.type==='glb'?'model/gltf-binary':'image/png',base64:b.toString('base64')};records.push({key,id,file_bytes:b.length,checksum_sha256:hash(b),license:asset.license})
}
let replaced=false
const result=await build({root:preview,configFile:false,publicDir:false,define:{'process.env.NODE_ENV':JSON.stringify('production')},plugins:[react(),{name:'reforge-embedded-assets',enforce:'pre',transform(code,id){
 if(id!==resolve(preview,'src/reforge/assets.ts'))return null
 const target=code.split('\n').find(line=>line.startsWith('export const reforgeURL ='))
 if(!target)throw Error('Update standalone asset adapter for changed source')
 replaced=true
 return code.replace(target,`const embedded:Record<string,{mime:string;base64:string}>=${JSON.stringify(embedded)}
 const urls=new Map<string,string>()
 export const reforgeURL=(id:string)=>{if(!urls.has(id)){const a=embedded[id];if(!a)throw new Error('Missing embedded asset '+id);urls.set(id,URL.createObjectURL(new Blob([Uint8Array.from(atob(a.base64),c=>c.charCodeAt(0))],{type:a.mime})))}return urls.get(id)!}`)
}}],build:{write:false,copyPublicDir:false,cssCodeSplit:false,minify:'oxc',sourcemap:false,license:true,lib:{entry:resolve(preview,'src/reforge/standalone.tsx'),name:'JoseonFantasyReforge',formats:['iife']},rolldownOptions:{output:{codeSplitting:false}}}})
if(!replaced)throw Error('Embedding adapter did not run')
const output=(Array.isArray(result)?result:[result]).flatMap(r=>r.output),chunks=output.filter(x=>x.type==='chunk')
if(chunks.length!==1||chunks[0].imports.length||chunks[0].dynamicImports.some(x=>x!==chunks[0].fileName))throw Error('Expected one fully self-contained IIFE')
const css=output.filter(x=>x.type==='asset'&&x.fileName.endsWith('.css')).map(x=>String(x.source)).join('\n'),license=output.find(x=>x.type==='asset'&&x.fileName.endsWith('license.md'));if(!css||!license)throw Error('Missing styles/licenses')
const safe=s=>s.replace(/<\/script/gi,'<\\/script')
const html=`<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#15243a"><link rel="icon" href="data:,"><title>Korean Arena 3D Studio v0.5 — Joseon Fantasy Reforge</title><meta name="description" content="Khám phá sân Hanok cùng Nari — nhân vật 3D thật, chuyển động, biểu cảm và điều khiển tương tác."><style>${css.replace(/<\/style/gi,'<\\/style')}</style></head><body><div id="root"></div><noscript>Bật JavaScript để khám phá Hanok.</noscript><script>${safe(chunks[0].code)}</script><script type="text/plain" id="studio-dependency-licenses">${safe(String(license.source))}</script></body></html>\n`
const dir=resolve(root,'showcase-v0.5');await mkdir(dir,{recursive:true});await writeFile(resolve(dir,'index.html'),html);await writeFile(resolve(dir,'.nojekyll'),'')
const info={format:'single-file-self-contained-html',app_source:'preview/src/reforge/standalone.tsx',asset_version:'0.5.0',release_status:'candidate; user authorizes publication after verified Gates D/E',file:'showcase-v0.5/index.html',file_bytes:Buffer.byteLength(html),checksum_sha256:hash(html),embedded_assets:records,generated_at:new Date().toISOString()}
await writeFile(resolve(dir,'build-info.json'),JSON.stringify(info,null,2)+'\n');console.log('Built exact v0.5 standalone',info.file_bytes,'bytes',info.checksum_sha256)
