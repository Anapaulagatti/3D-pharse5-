import { Suspense, useEffect, useRef, useMemo, type ComponentRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { Vector3, OrthographicCamera, PerspectiveCamera, Raycaster, MathUtils } from 'three'
import type { Object3D } from 'three'
import type { Settings, Preset } from './types'
import type { InputState, Player, Collider } from './physics'
import structure from '../../../exports/v0.5/collision-world.json'
import Nari from './Nari'
import { Lighting, House, Contact } from './World'

const positions:Record<Preset,[number[],number[],number]>={
 face:[[0,1.2,4],[0,1.2,0],.9],
 hero:[[10,8,14],[0,1.3,-.55],16.2],front:[[0,3,13],[0,1.8,-1.5],10],rear:[[0,3,-17],[0,1.8,-2.5],10],left:[[-15,3,-2],[0,2.0,-2],10.2],right:[[15,3,-2],[0,2.0,-2],10.2],roof:[[8,12,5],[0,1.6,-1.4],16],connection:[[4.1,3.2,2.4],[2.6,3,-.2],3.7],interior:[[-2.1,1.65,-1.95],[-2.15,1.0,-3.45],2.1],
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
 const goal=useRef<{pos:Vector3;look:Vector3;zoom:number}|null>(null),initialized=useRef(false)
 const offset=useRef(new Vector3(0,2.0,4.0)),target=useRef(new Vector3()),manual=useRef(false),point=useMemo(()=>new Vector3(),[]),dir=useMemo(()=>new Vector3(),[]),ray=useMemo(()=>new Raycaster(),[])
 useEffect(()=>{
  let [pos,look,scale]=positions[s.preset]
  const portrait=s.view==='portrait'||s.view==='animation'
  if(portrait){look=[0,.75,0];scale=2.7;pos=s.preset==='rear'?[0,1.1,-4]:s.preset==='left'?[-4,1.1,0]:s.preset==='right'?[4,1.1,0]:s.preset==='front'?[0,1.1,4]:[2,1.7,4]}
  if(portrait&&s.preset==='face'){look=[0,1.2,0];scale=.85;pos=[0,1.2,4]}
  if(s.angle!==null){const a=s.angle*Math.PI/180;pos=portrait?[4*Math.sin(a),1.2,4*Math.cos(a)]:[14*Math.sin(a),5,-2.5+14*Math.cos(a)];look=portrait?[0,.75,0]:[0,1.7,-2.5];scale=portrait?2.7:11}
  if(s.view==='play'){look=[player.position[0],player.position[1]+.84,player.position[2]];pos=[look[0],look[1]+2,look[2]+4];offset.current.set(0,2,4)}
  const zoom=Math.min(size.width/scale,size.height/(scale*.72))
  goal.current={pos:new Vector3().fromArray(pos),look:new Vector3().fromArray(look),zoom}
  if(!initialized.current||s.reduced||s.paused||s.view==='play'){camera.position.fromArray(pos);target.current.fromArray(look);camera.lookAt(target.current);if(camera instanceof OrthographicCamera)camera.zoom=zoom;goal.current=null}
  initialized.current=true
  if(camera instanceof PerspectiveCamera){camera.zoom=1;camera.fov=45}
  camera.updateProjectionMatrix();controls.current?.target.copy(target.current);controls.current?.update();invalidate()
 },[camera,size,s.preset,s.angle,s.view,s.reset,s.reduced,s.paused,player,invalidate])
 useFrame((_,dt)=>{
  if(goal.current&&s.view!=='play'&&controls.current){const g=goal.current,a=s.reduced||s.paused?1:1-Math.exp(-Math.min(dt,.15)*5);camera.position.lerp(g.pos,a);target.current.lerp(g.look,a);if(camera instanceof OrthographicCamera)camera.zoom=MathUtils.lerp(camera.zoom,g.zoom,a);camera.updateProjectionMatrix();controls.current.target.copy(target.current);controls.current.update();if(camera.position.distanceTo(g.pos)+target.current.distanceTo(g.look)<.003){goal.current=null}else if(s.active)invalidate()}
  if(s.view==='play'&&controls.current){
   point.set(player.position[0],player.position[1]+.84,player.position[2])
   target.current.lerp(point,s.reduced?1:1-Math.exp(-Math.min(dt,.15)*6))
   camera.position.copy(target.current).add(offset.current)
   const house=scene.userData.reforgeHouse as Object3D|undefined
   if(house){dir.copy(offset.current).normalize();ray.set(target.current,dir);ray.far=offset.current.length();const hit=ray.intersectObject(house,true).find(h=>h.distance>.20);if(hit)camera.position.copy(target.current).addScaledVector(dir,Math.max(.5,hit.distance-.16))}
   controls.current.target.copy(target.current);controls.current.update()
  }
  window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,camera:camera.position.toArray(),target:controls.current?.target.toArray(),projection:Array.from(camera.projectionMatrix.toArray()),viewMatrix:Array.from(camera.matrixWorldInverse.toArray())}
 })
 return <OrbitControls ref={controls} makeDefault enablePan={s.view!=='play'} minPolarAngle={.10} maxPolarAngle={Math.PI*.49} minZoom={15} maxZoom={500} minDistance={s.view==='play'?1.2:1} maxDistance={s.view==='play'?8:100} enableDamping={false}
  onStart={()=>{manual.current=true;goal.current=null}} onEnd={()=>{manual.current=false}}
  onChange={()=>{if(manual.current&&s.view==='play'&&controls.current)offset.current.copy(camera.position).sub(controls.current.target)}}
 />
}
export default function Scene({settings:s,input,player,onReact,onDoor,onDoorBlocked,onStory,onReady,onFailure}:{settings:Settings;input:InputState;player:Player;onReact:()=>void;onDoor:()=>void;onDoorBlocked:()=>void;onStory:(kind:string)=>void;onReady:()=>void;onFailure:()=>void}){
 const portrait=s.view==='portrait'||s.view==='animation',world=s.view==='hero'||s.view==='play'
 const colliders=structure.colliders as Collider[]
 return <Canvas key={s.view==='play'?'perspective':'orthographic'} orthographic={s.view!=='play'} shadows={s.quality!=='low'} camera={{position:[11,10,14],near:.05,far:100,zoom:45}} dpr={s.quality==='low'?1:[1,s.quality==='high'?1.75:1.25]} frameloop={s.active&&!s.reduced&&!s.paused?'always':'demand'} gl={{antialias:s.quality!=='low'}} fallback={<p>WebGL không khả dụng.</p>}>
  <ContextGuard onFailure={onFailure}/>
  <Lighting settings={s}/>
  <Suspense fallback={null}>
   {!portrait&&<House settings={s} player={player} onDoor={onDoor} onDoorBlocked={onDoorBlocked} onStory={onStory}/>}
   {(portrait||world)&&<Nari settings={s} input={input} player={player} colliders={colliders} doorOpen={s.door} onReact={onReact}/>}
   {(portrait||world)&&<Contact settings={s} player={player}/>}
   <Ready key={s.view} onReady={onReady}/>
  </Suspense><Camera settings={s} player={player}/>
  {portrait?<mesh position={[0,-.035,0]} receiveShadow><cylinderGeometry args={[.85,.88,.07,48]}/><meshStandardMaterial color="#ddd8c8" roughness={.9}/></mesh>:!world&&<mesh position={[0,.725,1.8]} castShadow><capsuleGeometry args={[.24,.97,6,12]}/><meshStandardMaterial color="#72beac" roughness={.8}/></mesh>}
 </Canvas>
}
