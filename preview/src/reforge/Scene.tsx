import { Suspense, useEffect, useRef, useMemo, type ComponentRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { Color, Mesh, Vector3, OrthographicCamera, PerspectiveCamera, Raycaster, MathUtils } from 'three'
import type { Object3D } from 'three'
import type { Settings, Preset } from './types'
import type { InputState, Player, Collider } from './physics'
import structure from '../../../exports/v0.5/hanok-graybox-structure.json'
import Nari from './Nari'

const positions:Record<Preset,[number[],number[],number]>={
 face:[[0,1.2,4],[0,1.2,0],.9],
 hero:[[11,10,14],[0,1.1,-.7],15],front:[[0,3,13],[0,1.8,-1.5],10],rear:[[0,3,-17],[0,1.8,-2.5],10],left:[[-15,3,-2],[0,1.8,-2],9],right:[[15,3,-2],[0,1.8,-2],9],roof:[[8,12,5],[0,1.2,-1.4],14],connection:[[4.1,3.2,2.4],[2.6,3,-.2],3.7],interior:[[-1.4,1.85,-1.95],[-2.2,1.1,-3.6],2.75],
}
function Ready({onReady}:{onReady:()=>void}){
 const reported=useRef(false),frames=useRef(0),{invalidate}=useThree()
 useFrame(()=>{frames.current++;if(frames.current<2)invalidate();else if(!reported.current){reported.current=true;onReady()}})
 return null
}
function ContextGuard({onFailure}:{onFailure:()=>void}){
 const {gl}=useThree()
 useEffect(()=>{const lost=(e:Event)=>{e.preventDefault();onFailure()};gl.domElement.addEventListener('webglcontextlost',lost);return()=>gl.domElement.removeEventListener('webglcontextlost',lost)},[gl,onFailure])
 return null
}
function Camera({settings:s,player}:{settings:Settings;player:Player}){
 const controls=useRef<ComponentRef<typeof OrbitControls>>(null),{camera,size,invalidate,scene}=useThree()
 const offset=useRef(new Vector3(0,2.0,4.0)),target=useRef(new Vector3()),manual=useRef(false),point=useMemo(()=>new Vector3(),[]),dir=useMemo(()=>new Vector3(),[]),ray=useMemo(()=>new Raycaster(),[])
 useEffect(()=>{
  let [pos,look,scale]=positions[s.preset]
  const portrait=s.view==='portrait'||s.view==='animation'
  if(portrait){look=[0,.75,0];scale=2.7;pos=s.preset==='rear'?[0,1.1,-4]:s.preset==='left'?[-4,1.1,0]:s.preset==='right'?[4,1.1,0]:s.preset==='front'?[0,1.1,4]:[2,1.7,4]}
  if(portrait&&s.preset==='face'){look=[0,1.2,0];scale=.85;pos=[0,1.2,4]}
  if(s.angle!==null){const a=s.angle*Math.PI/180;pos=portrait?[4*Math.sin(a),1.2,4*Math.cos(a)]:[14*Math.sin(a),5,-2.5+14*Math.cos(a)];look=portrait?[0,.75,0]:[0,1.7,-2.5];scale=portrait?2.7:11}
  if(s.view==='play'){look=[player.position[0],player.position[1]+.84,player.position[2]];pos=[look[0],look[1]+2,look[2]+4];offset.current.set(0,2,4)}
  camera.position.fromArray(pos);target.current.fromArray(look);camera.lookAt(target.current)
  if(camera instanceof OrthographicCamera)camera.zoom=Math.min(size.width/scale,size.height/(scale*.72))
  if(camera instanceof PerspectiveCamera){camera.zoom=1;camera.fov=45}
  camera.updateProjectionMatrix();controls.current?.target.copy(target.current);controls.current?.update();invalidate()
 },[camera,size,s.preset,s.angle,s.view,s.reset,player,invalidate])
 useFrame((_,dt)=>{
  if(s.view==='play'&&controls.current){
   point.set(player.position[0],player.position[1]+.84,player.position[2])
   target.current.lerp(point,s.reduced?1:1-Math.exp(-Math.min(dt,.15)*6))
   camera.position.copy(target.current).add(offset.current)
   const house=scene.userData.reforgeHouse as Object3D|undefined
   if(house){dir.copy(offset.current).normalize();ray.set(target.current,dir);ray.far=offset.current.length();const hit=ray.intersectObject(house,true).find(h=>h.distance>.20);if(hit)camera.position.copy(target.current).addScaledVector(dir,Math.max(.5,hit.distance-.16))}
   controls.current.target.copy(target.current);controls.current.update()
  }
  window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,camera:camera.position.toArray(),target:controls.current?.target.toArray()}
 })
 return <OrbitControls ref={controls} makeDefault enablePan={s.view!=='play'} minPolarAngle={.10} maxPolarAngle={Math.PI*.49} minZoom={15} maxZoom={500} minDistance={s.view==='play'?1.2:1} maxDistance={s.view==='play'?8:100} enableDamping={false}
  onStart={()=>{manual.current=true}} onEnd={()=>{manual.current=false}}
  onChange={()=>{if(manual.current&&s.view==='play'&&controls.current)offset.current.copy(camera.position).sub(controls.current.target)}}
 />
}
function House({settings:s,player,onDoor,onDoorBlocked}:{settings:Settings;player:Player;onDoor:()=>void;onDoorBlocked:()=>void}){
 const {scene:model}=useGLTF('/v0.5/models/hanok-graybox.glb'),{invalidate,scene}=useThree(),opening=useRef(s.door?1:0),blockedNotice=useRef(false)
 useEffect(()=>{model.traverse(o=>{if(o instanceof Mesh){o.castShadow=true;o.receiveShadow=true}});scene.userData.reforgeHouse=model;window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,ready:true,stage:'Gate B graybox'};invalidate();return()=>{delete scene.userData.reforgeHouse}},[model,scene,invalidate])
 useEffect(()=>{blockedNotice.current=false;if(s.paused)opening.current=s.door?1:0;invalidate()},[s.door,invalidate])
 useFrame((_,dt)=>{
  const occupied=s.view==='play'&&Math.abs(player.position[0])<.84&&Math.abs(player.position[2]+.6)<.52
  const desired=s.door||occupied&&opening.current>.5?1:0
  if(!s.door&&occupied&&opening.current>.5&&!blockedNotice.current){blockedNotice.current=true;onDoorBlocked()}
  if(!s.paused)opening.current=s.reduced?desired:MathUtils.damp(opening.current,desired,6,Math.min(dt,.15))
  for(const [name,sign] of [['DoorLeft',-1],['DoorRight',1]] as const){const o=model.getObjectByName(name);if(o)o.position.x=sign*.56*opening.current}
  if(!s.paused&&Math.abs(opening.current-desired)>.002)invalidate()
  queueMicrotask(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,door:opening.current}})
 })
 return <primitive object={model} onClick={(e:{object:Object3D;stopPropagation:()=>void})=>{let o:Object3D|null=e.object;while(o&&o!==model){if(/^DoorLeft|^DoorRight/.test(o.name)){e.stopPropagation();onDoor();break}o=o.parent}}}/>
}
export default function Scene({settings:s,input,player,onReact,onDoor,onDoorBlocked,onReady,onFailure}:{settings:Settings;input:InputState;player:Player;onReact:()=>void;onDoor:()=>void;onDoorBlocked:()=>void;onReady:()=>void;onFailure:()=>void}){
 const portrait=s.view==='portrait'||s.view==='animation',world=s.view==='hero'||s.view==='play'
 const colliders=structure.colliders as Collider[]
 return <Canvas key={s.view==='play'?'perspective':'orthographic'} orthographic={s.view!=='play'} shadows={s.quality!=='low'} camera={{position:[11,10,14],near:.05,far:100,zoom:45}} dpr={s.quality==='low'?1:[1,s.quality==='high'?1.75:1.25]} frameloop={s.active&&!s.reduced&&!s.paused?'always':'demand'} gl={{antialias:s.quality!=='low'}} fallback={<p>WebGL không khả dụng.</p>}>
  <ContextGuard onFailure={onFailure}/>
  <color attach="background" args={[new Color('#dddeda')]}/><ambientLight intensity={.40}/><hemisphereLight args={['#d9e9f2','#8b856b',.8]}/>
  <directionalLight position={[3,9,6]} intensity={2.2} castShadow shadow-mapSize={[s.quality==='high'?2048:1024,s.quality==='high'?2048:1024]} shadow-camera-left={portrait?-2.2:-8} shadow-camera-right={portrait?2.2:8} shadow-camera-top={portrait?2.2:8} shadow-camera-bottom={portrait?-2.2:-8} shadow-normalBias={portrait?.006:.035} shadow-bias={portrait?-.00005:-.0002} onUpdate={light=>light.shadow.camera.updateProjectionMatrix()}/>
  <directionalLight position={[-4,5,-5]} intensity={.7}/>
  <Suspense fallback={null}>
   {!portrait&&<House settings={s} player={player} onDoor={onDoor} onDoorBlocked={onDoorBlocked}/>}
   {(portrait||world)&&<Nari settings={s} input={input} player={player} colliders={colliders} doorOpen={s.door} onReact={onReact}/>}
   <Ready key={s.view} onReady={onReady}/>
  </Suspense><Camera settings={s} player={player}/>
  {portrait?<mesh position={[0,-.035,0]} receiveShadow><cylinderGeometry args={[.85,.88,.07,48]}/><meshStandardMaterial color="#ddd8c8" roughness={.9}/></mesh>:!world&&<mesh position={[0,.725,1.8]} castShadow><capsuleGeometry args={[.24,.97,6,12]}/><meshStandardMaterial color="#72beac" roughness={.8}/></mesh>}
 </Canvas>
}
