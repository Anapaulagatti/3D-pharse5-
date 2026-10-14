import { useEffect, useMemo, useRef, useCallback } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { AnimationMixer, LoopRepeat, LoopOnce, Mesh, SkinnedMesh, Vector3, Group, MathUtils } from 'three'
import type { AnimationAction } from 'three'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import { stepPlayer, type InputState, type Player, type Collider } from './physics'
import type { Settings } from './types'
import { TerrainFeet } from './footPlacement'
import { reforgeURL } from './assets'

export const clips=['Idle','Walk','Run','WalkStart','WalkStop','RunStart','RunStop','JumpStart','JumpAir','JumpLand','TurnLeft','TurnRight','Greeting','Happy','Thinking','Sad','Celebration','Surprised','Curious','InteractionReaction']
export const expressions=['Auto','Neutral','Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating']
export default function Nari({settings:s,input,player,colliders,doorOpen,onReact}:{settings:Settings;input:InputState;player:Player;colliders:Collider[];doorOpen:boolean;onReact:()=>void}){
 const gltf=useGLTF(reforgeURL('nari')),{invalidate}=useThree()
 const model=useMemo(()=>clone(gltf.scene),[gltf.scene]),mixer=useMemo(()=>new AnimationMixer(model),[model])
 const terrainFeet=useMemo(()=>new TerrainFeet(model),[model])
 const actions=useMemo(()=>new Map(gltf.animations.map(c=>[c.name,mixer.clipAction(c)])),[gltf.animations,mixer])
 const faces=useMemo(()=>{const meshes:Mesh[]=[];model.traverse(o=>{if(o instanceof Mesh){o.castShadow=!o.morphTargetDictionary;o.receiveShadow=!o.morphTargetDictionary&&!o.name.includes('NariSkinSurface');if(o.morphTargetDictionary)meshes.push(o)}});return meshes},[model])
 const outer=useRef<Group>(null),action=useRef<AnimationAction|null>(null),clip=useRef(''),once=useRef(false),finished=useRef(false)
 const manual=useRef(''),accumulator=useRef(0),idle=useRef(0),introduced=useRef(false),previousSpeed=useRef(0),lastRun=useRef(false)
 const events=useRef<{clip:string;at:number;position:number[]}[]>([])
 const vectors=useMemo(()=>({forward:new Vector3(),point:new Vector3()}),[])
 const world=s.view==='play'||s.view==='hero',play=s.view==='play'
 const switchClip=useCallback((name:string,oneShot=false,fade=.16)=>{
  if(clip.current===name&&!finished.current)return
  const next=actions.get(name);if(!next)throw new Error('Missing authored Nari clip '+name)
  const old=action.current;next.reset().setEffectiveWeight(1).setEffectiveTimeScale(1).setLoop(oneShot?LoopOnce:LoopRepeat,oneShot?1:Infinity);next.clampWhenFinished=oneShot;next.paused=false;next.play()
  if(old&&old!==next&&fade>0)next.crossFadeFrom(old,fade,false);else if(old&&old!==next)old.stop()
  action.current=next;clip.current=name;once.current=oneShot;finished.current=false;invalidate()
  events.current.push({clip:name,at:performance.now(),position:[...player.position]});if(events.current.length>48)events.current.shift()
 },[actions,invalidate,player])
 useEffect(()=>{
  const onFinish=(e:{action:AnimationAction})=>{if(e.action===action.current){finished.current=true;once.current=false;manual.current='';invalidate()}}
  mixer.addEventListener('finished',onFinish);return()=>mixer.removeEventListener('finished',onFinish)
 },[mixer,invalidate])
 useEffect(()=>{
  mixer.stopAllAction();clip.current='';finished.current=true;manual.current='';accumulator.current=0;previousSpeed.current=0
  switchClip(world?'Idle':s.clip,false,0)
  if(s.reduced||s.paused){action.current!.time=Math.min(action.current!.getClip().duration*.42,.9);action.current!.paused=true}
  mixer.update(0);invalidate()
 },[s.clip,s.view,s.reset,world,mixer,switchClip,invalidate])
 useEffect(()=>{if(action.current){action.current.paused=s.reduced||s.paused;if(s.reduced&&!s.paused)action.current.time=Math.min(action.current.getClip().duration*.42,.9)}mixer.update(0);invalidate()},[s.reduced,s.paused,mixer,invalidate])
 useEffect(()=>{
  if(!s.gesture.id)return
  manual.current=s.gesture.name;finished.current=true;switchClip(s.gesture.name,true,s.reduced?0:.16)
  if(s.reduced||s.paused){action.current!.time=action.current!.getClip().duration*.42;action.current!.paused=true;mixer.update(0)}
  invalidate()
  const timer=setTimeout(()=>{if(manual.current===s.gesture.name&&(s.reduced||s.paused)){manual.current='';finished.current=true;switchClip(world?'Idle':s.clip,false,0);action.current!.time=.4;action.current!.paused=true;mixer.update(0);invalidate()}},2500)
  return()=>clearTimeout(timer)
 },[s.gesture.id,s.gesture.name,mixer,switchClip,invalidate])
 useEffect(()=>{input.wake=invalidate;return()=>{input.wake=undefined}},[input,invalidate])
 useEffect(()=>{invalidate()},[s.expression,invalidate])
 useEffect(()=>()=>{mixer.stopAllAction();mixer.uncacheRoot(model)},[mixer,model])
 useFrame(({gl,camera},delta)=>{
  const active=s.active&&!s.paused,ambient=active&&!s.reduced
  let simulated=0,movingInput=false,run=false
  if(play&&active){
   const keys=input.keys,ax=Number(keys.has('KeyD')||keys.has('ArrowRight'))-Number(keys.has('KeyA')||keys.has('ArrowLeft')),az=Number(keys.has('KeyW')||keys.has('ArrowUp'))-Number(keys.has('KeyS')||keys.has('ArrowDown'))
   movingInput=ax!==0||az!==0;run=keys.has('ShiftLeft')||keys.has('ShiftRight')||input.mobileRun
   camera.getWorldDirection(vectors.forward);const len=Math.hypot(vectors.forward.x,vectors.forward.z)||1,fx=vectors.forward.x/len,fz=vectors.forward.z/len,wx=-fz*ax+fx*az,wz=fx*ax+fz*az,length=Math.hypot(wx,wz)||1
   accumulator.current=Math.min(accumulator.current+delta,.25)
   while(accumulator.current>=1/60){stepPlayer(player,[wx/length,wz/length],run,input.jump,1/60,colliders,doorOpen&&(window.__REFORGE_METRICS__?.door??0)>.95);input.jump=false;accumulator.current-=1/60;simulated+=1/60}
   if(movingInput)manual.current=''
   let desired='Idle',single=false
   if(player.crouch>0){desired='JumpStart';single=true}
   else if(!player.grounded)desired='JumpAir'
   else if(player.landing>0){desired='JumpLand';single=true}
   else if(manual.current){desired=manual.current;single=true}
   else if(player.speed>.03){
    if(once.current&&!finished.current&&['WalkStart','RunStart','TurnLeft','TurnRight'].includes(clip.current)){desired=clip.current;single=true}
    else if(previousSpeed.current<=.03||lastRun.current!==run){desired=run?'RunStart':'WalkStart';single=true}
    else desired=run?'Run':'Walk'
   }else if(previousSpeed.current>.03){desired=lastRun.current?'RunStop':'WalkStop';single=true}
   else if(once.current&&!finished.current&&['WalkStop','RunStop'].includes(clip.current)){desired=clip.current;single=true}
   switchClip(desired,single,s.reduced?0:.14)
   previousSpeed.current=player.speed;lastRun.current=run
   if(action.current&&['Walk','Run'].includes(clip.current))action.current.timeScale=player.speed/(clip.current==='Run'?2.4375:.8148)
  }else if(world&&ambient){
   if(!introduced.current){introduced.current=true;player.yaw=Math.atan2(camera.position.x-player.position[0],camera.position.z-player.position[2]);manual.current='Greeting';finished.current=true;switchClip('Greeting',true)}
   else if(!manual.current&&(!once.current||finished.current)){
    idle.current+=Math.min(delta,.15)
    if(idle.current>14){idle.current=0;manual.current='Curious';finished.current=true;switchClip('Curious',true)}
    else switchClip('Idle')
   }
   if(outer.current&&clip.current==='Idle'){const yaw=Math.atan2(camera.position.x-player.position[0],camera.position.z-player.position[2]);player.yaw=MathUtils.damp(player.yaw,yaw,1.8,Math.min(delta,.15))}
  }
  if(!world&&finished.current&&manual.current==='')switchClip(s.clip,false,s.reduced?0:.16)
  const commanded=play&&(movingInput||player.speed>.01||!player.grounded||player.crouch>0||player.landing>0)
  const animate=active&&(ambient||commanded)
  if(action.current)action.current.paused=!animate
  mixer.update(animate?(play?simulated:Math.min(delta,.15)):0)
  const morphs:Record<string,number>={}
  for(const face of faces){const dict=face.morphTargetDictionary!,values=face.morphTargetInfluences!
   if(s.expression!=='Auto'){for(const [name,i] of Object.entries(dict))if(name!=='Blink')values[i]=name===s.expression?1:0}
   for(const [name,i] of Object.entries(dict))morphs[name]=values[i]
  }
  if(outer.current){if(world)outer.current.position.set(...player.position);else outer.current.position.set(0,0,0);outer.current.rotation.y=world?player.yaw:0;outer.current.updateMatrixWorld(true)}
  if(play&&outer.current)terrainFeet.apply(outer.current,player,clip.current,(action.current?.time||0)/(action.current?.getClip().duration||1))
  model.updateMatrixWorld(true);const feet:number[][]=[];let bones=0
  model.traverse(o=>{if(o instanceof SkinnedMesh)bones=Math.max(bones,o.skeleton.bones.length);if(/^Foot[._]?L$|^Foot[._]?R$/.test(o.name)){o.getWorldPosition(vectors.point);feet.push(vectors.point.toArray())}})
  player.clip=clip.current;player.clipTime=action.current?.time||0
  if(commanded&&s.reduced&&active)invalidate()
  queueMicrotask(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,ready:true,stage:'Gate C real skinned Nari',clip:clip.current,clipTime:action.current?.time,clips:gltf.animations.map(c=>c.name),morphs,feet,skinBones:bones,motion:animate,draws:gl.info.render.calls,triangles:gl.info.render.triangles,player:[...player.position],yaw:player.yaw,speed:player.speed,grounded:player.grounded,verticalVelocity:player.vertical,blocked:player.blocked,distance:player.distance,physicsSteps:player.steps,reduced:s.reduced,events:events.current.map(e=>({...e}))}})
 })
 return <group ref={outer} onClick={e=>{e.stopPropagation();onReact()}} onPointerOver={()=>{document.body.style.cursor='pointer'}} onPointerOut={()=>{document.body.style.cursor=''}}><primitive object={model}/></group>
}
