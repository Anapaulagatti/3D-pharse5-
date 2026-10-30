// Read-only browser checks against exact deployed bytes; no game/source writes.
export async function verifyMotion(browser,base) {
 const rows=[],errors=[],specs=[['juni','kr-classic-bob','kr-hair-ornament'],['minjun','kr-layered-cut','kr-fashion-cap'],['doyun','kr-side-part','kr-garden-hat']];
 const seed=async(c,id,h,acc)=>c.addInitScript(({id,h,acc})=>{localStorage.setItem('korean-arena-player-preferences-v1',JSON.stringify({version:1,characterId:id}));localStorage.setItem('korean-arena-appearance-preferences-v2',JSON.stringify({version:2,selectedCharacterId:id,appearances:{[id]:{schemaVersion:2,characterId:id,hairstyleId:h,outfitId:null,accessoryIds:[acc]}},presets:[]}))},{id,h,acc});
 for(const[id,h,acc]of specs){
  const c=await browser.newContext({viewport:{width:1280,height:1000},deviceScaleFactor:1});
  try{await seed(c,id,h,acc);const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(new URL('play/?native&pixelAudit&renderer=canvas&entry=transition',base).href);await p.waitForFunction(id=>window.__GATE3__?.ready&&window.__GATE3__.characterId===id&&window.__GATE3__.chunks.inflight===0,id,{timeout:60000});
   for(const[view,key]of [['front','s'],['back','w'],['left','a'],['right','d']]){
    for(const action of ['walk','idle','run']){
     if(action==='idle'){await p.keyboard.up(key);await p.waitForFunction(v=>window.__GATE3__.frame.startsWith('idle-'+v+'-'),view,{timeout:6000});}
     else{if(action==='run')await p.keyboard.down('Shift');await p.keyboard.down(key);await p.waitForFunction(prefix=>window.__GATE3__.frame.startsWith(prefix),action+'-'+view+'-',{timeout:6000});}
     const a=await p.evaluate(prefix=>window.__GATE3_PIXEL_POSE__(prefix,6000),action+'-'+view+'-');if(!a.matched||a.state.appearance.hairstyleId!==h||a.state.appearance.accessoryIds[0]!==acc||a.state.playerSprites!==1||a.state.samplingMode!==1||a.camera.zoom!==1||!a.camera.scroll.every(Number.isInteger))throw Error('Native cosmetic pose/registration mismatch '+id+'/'+action+'/'+view);
     rows.push({id,action,view,actualFrame:a.actualFrame,appearance:a.state.appearance,nearest:true,integerCamera:true,playerSprites:1});
     if(action==='run'){await p.keyboard.up(key);await p.keyboard.up('Shift');await p.waitForFunction(()=>window.__GATE3__.frame.startsWith('idle-'),{}, {timeout:6000});}
    }
   }
  }finally{await c.close();}
 }
 const c=await browser.newContext({viewport:{width:960,height:640},deviceScaleFactor:1,reducedMotion:'reduce'});let trace=[];
 try{await seed(c,...specs[0]);const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(new URL('play/?renderer=canvas&entry=transition',base).href);await p.waitForFunction(()=>window.__GATE3__?.ready&&window.__GATE3__.chunks.inflight===0,{}, {timeout:60000});await p.waitForTimeout(300);await p.evaluate(()=>{window.__releaseMotionTrace=[];window.__releaseMotionCapture=true;const f=()=>{const s=window.__GATE3__;if(s)window.__releaseMotionTrace.push({t:performance.now(),x:s.x,y:s.y,frame:s.frame,look:s.camera.lookAhead,view:s.camera.worldView,zoom:s.zoom,players:s.playerSprites,sampling:s.samplingMode});if(window.__releaseMotionCapture)requestAnimationFrame(f)};requestAnimationFrame(f)});
  let held=[];const scenarios=[['d'],['d','w'],[],['w'],['Shift','w'],['Shift','w','a'],['Shift','s','d'],[],['a'],['d'],['w','s'],[]];
  for(const keys of scenarios){for(const k of held)if(!keys.includes(k))await p.keyboard.up(k);for(const k of keys)if(!held.includes(k))await p.keyboard.down(k);held=keys;await p.waitForTimeout(230);}
  trace=await p.evaluate(()=>{window.__releaseMotionCapture=false;return window.__releaseMotionTrace});
 }finally{await c.close();}
 let maximumTravel=0,maximumCameraStep=0,checkedPairs=0;
 for(const r of trace)if(r.players!==1||r.sampling!==1||r.zoom!==1||r.look.some(v=>v!==0))throw Error('Movement texture/camera ownership regression');
 for(let i=1;i<trace.length;i++){const a=trace[i-1],b=trace[i];if(b.t-a.t>=80)continue;const travel=Math.hypot(b.x-a.x,b.y-a.y),camera=Math.hypot(b.view[0]-a.view[0],b.view[1]-a.view[1]);maximumTravel=Math.max(maximumTravel,travel);maximumCameraStep=Math.max(maximumCameraStep,camera);checkedPairs++;if(travel>5.01||camera>6.5)throw Error('One-frame position/camera pop '+JSON.stringify({a,b,travel,camera}));}
 if(rows.length!==36||checkedPairs<20||errors.length)throw Error('Incomplete live cosmetic/movement evidence '+JSON.stringify({rows:rows.length,checkedPairs,errors}));
 return{status:'PASS ACTUAL BROWSER POSE/INPUT CHECKS',nativePoses:rows,movement:{scenarios:12,samples:trace.length,checkedPairs,maximumTravel,maximumCameraStep,reducedMotion:true,inputLead:0,oneFramePopReproduced:false},errors,physicalDevices:'NOT TESTED',scope:'Observed browser scenarios; original96x112 frame/anchor assets remain bound by exact manifest. Not hardware frame-pacing certification.'};
}
