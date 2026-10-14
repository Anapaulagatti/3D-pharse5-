// Separate review artifact. Existing public v0.5 inputs are never touched.
import {createHash} from 'node:crypto'
import {mkdir,readFile,writeFile} from 'node:fs/promises'
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {pathToFileURL} from 'node:url'
const root=resolve(import.meta.dirname,'../..'),preview=resolve(root,'preview'),req=createRequire(resolve(preview,'package.json')),hash=b=>createHash('sha256').update(b).digest('hex')
const protectedFiles=JSON.parse(await readFile(resolve(root,'quality-reports/v0.6/preserved-v05.json')))
for(const [name,record] of Object.entries(protectedFiles.files))if(hash(await readFile(resolve(root,name)))!==record.sha256)throw Error('Protected baseline changed: '+name)
const manifest=JSON.parse(await readFile(resolve(root,'exports/v0.6/asset-manifest.json'))),embedded={},records=[]
for(const [key,id] of [['house','letter-plaza'],['nari','nari-chibi']]){
 const asset=manifest.assets.find(a=>a.id===id),b=await readFile(resolve(root,asset.file));if(b.length!==asset.bytes||hash(b)!==asset.sha256||asset.validation.errors||asset.validation.warnings)throw Error('Unverified '+id)
 embedded[key]={mime:'model/gltf-binary',base64:b.toString('base64')};records.push({key,file:asset.file,bytes:b.length,sha256:hash(b),license:asset.license})
}
const poster=await readFile(resolve(root,'exports/v0.6/posters/plaza-day.png'));if(poster.toString('hex',0,8)!=='89504e470d0a1a0a')throw Error('Missing real PNG poster');embedded.poster={mime:'image/png',base64:poster.toString('base64')};records.push({key:'poster',file:'exports/v0.6/posters/plaza-day.png',bytes:poster.length,sha256:hash(poster),license:'project-owned-original-actual-render'})
const {build}=await import(pathToFileURL(req.resolve('vite')).href),{default:react}=await import(pathToFileURL(req.resolve('@vitejs/plugin-react')).href);let replaced=false
const result=await build({root:preview,configFile:false,publicDir:false,define:{'process.env.NODE_ENV':JSON.stringify('production')},plugins:[react(),{name:'town-embedded-assets',enforce:'pre',transform(code,id){
 if(id!==resolve(preview,'src/town/assets.ts'))return null;replaced=true
 return `const embedded:Record<string,{mime:string;base64:string}>=${JSON.stringify(embedded)}
 const urls=new Map<string,string>()
 export const townURL=(id:string)=>{if(!urls.has(id)){const a=embedded[id];if(!a)throw Error('Missing verified embedded asset '+id);urls.set(id,URL.createObjectURL(new Blob([Uint8Array.from(atob(a.base64),c=>c.charCodeAt(0))],{type:a.mime})))}return urls.get(id)!}`
}}],build:{write:false,copyPublicDir:false,cssCodeSplit:false,minify:'oxc',sourcemap:false,license:true,lib:{entry:resolve(preview,'src/town/main.tsx'),name:'PlayfulHangeulTown',formats:['iife']},rolldownOptions:{output:{codeSplitting:false}}}})
if(!replaced)throw Error('Asset adapter did not run');const output=(Array.isArray(result)?result:[result]).flatMap(r=>r.output),chunks=output.filter(x=>x.type==='chunk');if(chunks.length!==1||chunks[0].imports.length||chunks[0].dynamicImports.some(x=>x!==chunks[0].fileName))throw Error('Expected one self-contained IIFE')
const css=output.filter(x=>x.type==='asset'&&x.fileName.endsWith('.css')).map(x=>String(x.source)).join('\n'),license=output.find(x=>x.type==='asset'&&x.fileName.endsWith('license.md'));if(!css||!license)throw Error('Missing styles/license notices')
const safe=s=>s.replace(/<\/script/gi,'<\\/script'),html=`<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#fff7e9"><link rel="icon" href="data:,"><title>Korean Arena v0.6 — Playful Hangeul Town Prototype</title><style>${css.replace(/<\/style/gi,'<\\/style')}</style></head><body><div id="root"></div><noscript>Bật JavaScript để gặp Nari.</noscript><script>${safe(chunks[0].code)}</script><script type="text/plain" id="studio-dependency-licenses">${safe(String(license.source))}</script></body></html>\n`
for(const pattern of [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,/gh[pousr]_[A-Za-z0-9]{36}/,/AKIA[A-Z0-9]{16}/])if(pattern.test(html))throw Error('Credential pattern found')
const dir=resolve(root,'showcase-v0.6');await mkdir(dir,{recursive:true});await writeFile(resolve(dir,'index.html'),html);await writeFile(resolve(dir,'.nojekyll'),'')
const info={format:'single-file-self-contained-html',version:'0.6-prototype',public_release:'NOT_AUTHORIZED_REVIEW_CANDIDATE_ONLY',entry:'preview/src/town/main.tsx',file:'showcase-v0.6/index.html',bytes:Buffer.byteLength(html),sha256:hash(html),embedded_assets:records,protected_baseline_files_verified:Object.keys(protectedFiles.files).length,built_at:new Date().toISOString()}
await writeFile(resolve(dir,'build-info.json'),JSON.stringify(info,null,2)+'\n');console.log('Town candidate built',info.bytes,'bytes',info.sha256)
