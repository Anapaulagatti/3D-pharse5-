import { useEffect, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { AnimationMixer, LoopRepeat, Mesh, SkinnedMesh, Vector3 } from 'three'
import { clone } from 'three/addons/utils/SkeletonUtils.js'
import type { Settings } from './types'

export const clips=['Idle','Walk','Run','WalkStart','WalkStop','RunStart','RunStop','JumpStart','JumpAir','JumpLand','TurnLeft','TurnRight','Greeting','Happy','Thinking','Sad','Celebration','Surprised','Curious','InteractionReaction']
export const expressions=['Auto','Neutral','Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating']
export default function Nari({settings:s}:{settings:Settings}){
 const gltf=useGLTF('/v0.5/models/nari-messenger.glb'),{invalidate}=useThree()
 const model=useMemo(()=>clone(gltf.scene),[gltf.scene]),mixer=useMemo(()=>new AnimationMixer(model),[model])
 const actions=useMemo(()=>new Map(gltf.animations.map(c=>[c.name,mixer.clipAction(c)])),[gltf.animations,mixer])
 const faces=useMemo(()=>{const meshes:Mesh[]=[];model.traverse(o=>{if(o instanceof Mesh){o.castShadow=true;o.receiveShadow=true;if(o.morphTargetDictionary)meshes.push(o)}});return meshes},[model])
 useEffect(()=>{const action=actions.get(s.clip);if(!action)throw new Error('Missing actual Nari clip '+s.clip);mixer.stopAllAction();action.reset().setLoop(LoopRepeat,Infinity).play();if(s.reduced||s.paused){action.time=Math.min(action.getClip().duration*.42,.9);action.paused=true}mixer.update(0);invalidate();return()=>{action.stop()}},[actions,s.clip,s.reduced,s.paused,mixer,invalidate])
 useEffect(()=>{invalidate()},[s.expression,invalidate])
 useEffect(()=>()=>{mixer.stopAllAction();mixer.uncacheRoot(model)},[mixer,model])
 useFrame(({gl},delta)=>{
  if(!s.reduced&&!s.paused)mixer.update(Math.min(delta,.15))
  const morphs:Record<string,number>={}
  for(const face of faces){const dict=face.morphTargetDictionary!,values=face.morphTargetInfluences!
   if(s.expression!=='Auto'){for(const [name,i] of Object.entries(dict))if(name!=='Blink')values[i]=name===s.expression?1:0}
   for(const [name,i] of Object.entries(dict))morphs[name]=values[i]
  }
  model.updateMatrixWorld(true);const feet:number[][]=[],v=new Vector3();let bones=0
  model.traverse(o=>{if(o instanceof SkinnedMesh)bones=Math.max(bones,o.skeleton.bones.length);if(/^Foot[._]?L$|^Foot[._]?R$/.test(o.name)){o.getWorldPosition(v);feet.push(v.toArray())}})
  queueMicrotask(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,ready:true,stage:'Gate C real skinned Nari',clip:s.clip,clipTime:actions.get(s.clip)?.time,clips:gltf.animations.map(c=>c.name),morphs,feet,skinBones:bones,motion:!s.reduced&&!s.paused,draws:gl.info.render.calls,triangles:gl.info.render.triangles}})
 })
 return <primitive object={model}/>
}
