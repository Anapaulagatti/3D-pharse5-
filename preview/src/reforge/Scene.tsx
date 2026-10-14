import { Suspense, useEffect, useRef, type ComponentRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { Color, Mesh, Vector3 } from 'three'
import type { Settings, Preset } from './types'
import Nari from './Nari'

const positions:Record<Preset, [number[],number[],number]>={
 hero:[[11,10,14],[0,1.1,-.7],15],front:[[0,3,13],[0,1.8,-1.5],10],rear:[[0,3,-17],[0,1.8,-2.5],10],left:[[-15,3,-2],[0,1.8,-2],9],right:[[15,3,-2],[0,1.8,-2],9],roof:[[8,12,5],[0,1.2,-1.4],14],connection:[[4.1,3.2,2.4],[2.6,3,-.2],3.7],interior:[[-1.4,1.85,-1.95],[-2.2,1.1,-3.6],2.75],
}
function Camera({settings:s}:{settings:Settings}) {
 const controls=useRef<ComponentRef<typeof OrbitControls>>(null),{camera,size,invalidate}=useThree()
 useEffect(()=>{let [pos,target,scale]=positions[s.preset];const portrait=s.view==='portrait'||s.view==='animation';if(portrait){target=[0,.78,0];scale=2.4;pos=s.preset==='rear'?[0,1.1,-4]:s.preset==='left'?[-4,1.1,0]:s.preset==='right'?[4,1.1,0]:s.preset==='front'?[0,1.1,4]:[2,1.7,4]}if(s.angle!==null){const a=s.angle*Math.PI/180;pos=portrait?[4*Math.sin(a),1.2,4*Math.cos(a)]:[14*Math.sin(a),5,-2.5+14*Math.cos(a)];target=portrait?[0,.78,0]:[0,1.7,-2.5];scale=portrait?2.4:11}camera.position.fromArray(pos);camera.lookAt(new Vector3().fromArray(target));if('zoom' in camera)camera.zoom=Math.min(size.width/scale,size.height/(scale*.72));camera.updateProjectionMatrix();controls.current?.target.fromArray(target);controls.current?.update();invalidate()},[camera,size,s.preset,s.angle,s.view,invalidate])
 useFrame(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,camera:camera.position.toArray(),target:controls.current?.target.toArray()}})
 return <OrbitControls ref={controls} makeDefault enablePan minPolarAngle={.10} maxPolarAngle={Math.PI*.49} minZoom={15} maxZoom={500} enableDamping={false}/>
}
function House({settings:s}:{settings:Settings}) {
 const {scene}=useGLTF('/v0.5/models/hanok-graybox.glb'),{invalidate}=useThree()
 useEffect(()=>{scene.traverse(o=>{if(o instanceof Mesh){o.castShadow=true;o.receiveShadow=true}});window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,ready:true,stage:'Gate B graybox'};invalidate()},[scene,invalidate])
 useEffect(()=>{for(const [name,side] of [['DoorLeft',-1],['DoorRight',1]] as const){const o=scene.getObjectByName(name);if(o)o.position.x=s.door?side*.56:0}window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,door:s.door?1:0};invalidate()},[scene,s.door,invalidate])
 useFrame(({gl})=>{queueMicrotask(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,draws:gl.info.render.calls,triangles:gl.info.render.triangles}})})
 return <primitive object={scene}/>
}
export default function Scene({settings:s}:{settings:Settings}) {
 const portrait=s.view==='portrait'||s.view==='animation'
 return <Canvas orthographic shadows={s.quality!=='low'} camera={{position:[11,10,14],near:.05,far:100,zoom:45}} dpr={s.quality==='low'?1:[1,s.quality==='high'?1.75:1.25]} frameloop={!s.reduced&&!s.paused?'always':'demand'} gl={{antialias:s.quality!=='low'}}>
  <color attach="background" args={[new Color('#dddeda')]}/><ambientLight intensity={.40}/><hemisphereLight args={['#d9e9f2','#8b856b',.8]}/><directionalLight position={[3,9,6]} intensity={2.2} castShadow shadow-mapSize={[1024,1024]} shadow-camera-left={-10} shadow-camera-right={10} shadow-camera-top={10} shadow-camera-bottom={-10} shadow-normalBias={.03}/><directionalLight position={[-4,5,-5]} intensity={.7}/>
  <Suspense fallback={null}>{portrait?<Nari settings={s}/>:<House settings={s}/>}</Suspense><Camera settings={s}/>
  {portrait?<><mesh position={[0,-.035,0]} receiveShadow><cylinderGeometry args={[.85,.88,.07,48]}/><meshStandardMaterial color="#ddd8c8" roughness={.9}/></mesh></>:<mesh position={[0,.725,1.8]} castShadow><capsuleGeometry args={[.24,.97,6,12]}/><meshStandardMaterial color="#72beac" roughness={.8}/></mesh>}
 </Canvas>
}
