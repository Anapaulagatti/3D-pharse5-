// Evidence gallery: lay out original browser PNGs unchanged, no synthetic art.
import {createRequire} from 'node:module'
import {resolve} from 'node:path'
import {mkdir,readFile,writeFile} from 'node:fs/promises'
const root=resolve(import.meta.dirname,'../..'),req=createRequire(resolve(root,'preview/package.json')),{chromium}=req('@playwright/test'),out=resolve(root,'quality-reports/v0.5/gate-e/gallery');await mkdir(out,{recursive:true})
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--disable-gpu']})
try{
 for(const [name,files,cols,width] of [['faces',['Neutral','Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating'].map(x=>'face-'+x.toLowerCase()),4,1600],['poses',['Idle','Walk','Run','WalkStart','WalkStop','RunStart','RunStop','JumpStart','JumpAir','JumpLand','TurnLeft','TurnRight','Greeting','Happy','Thinking','Sad','Celebration','Surprised','Curious','InteractionReaction'].map(x=>'pose-'+x.toLowerCase()),5,1800],['views',['front','left','rear','right'],4,1600],['motion',['walk','run','jumpair','greeting','celebration','interactionreaction'].flatMap(x=>['live-'+x+'-a','live-'+x+'-b']),4,1800]]){
  const cards=await Promise.all(files.map(async f=>`<figure><figcaption>${f}</figcaption><img src="data:image/png;base64,${(await readFile(resolve(root,'quality-reports/v0.5/gate-e/final-static-character',f+'.png'))).toString('base64')}"></figure>`)),html=`<!doctype html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box}body{margin:0;background:#f4f0e6;color:#243b36;font:15px sans-serif}main{display:grid;grid-template-columns:repeat(${cols},1fr);gap:8px;padding:8px}figure{margin:0}figcaption{padding:8px;font-weight:bold}img{display:block;width:100%;height:auto}</style></head><body><main>${cards.join('')}</main></body></html>`
  await writeFile(resolve(out,name+'.html'),html);const p=await browser.newPage({viewport:{width,height:1000}});await p.setContent(html);await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await p.screenshot({path:resolve(out,name+'.png'),fullPage:true});await p.close()
 }
}finally{await browser.close()}
