import { useEffect, useMemo, useRef, type RefObject } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { AnimationMixer, Color, DirectionalLight, DoubleSide, Fog, HemisphereLight, InstancedMesh, MathUtils, Mesh, MeshStandardMaterial, Object3D, PMREMGenerator, PointLight, Vector3 } from 'three'
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js'
import type { Settings } from './types'
import type { Player } from './physics'
import { floorHeight } from './physics'
import { reforgeURL } from './assets'

const looks={day:{bg:'#d9e4de',fog:'#d9e4de',key:'#fff2cf',fill:'#bad5e2',ground:'#a3ab89',keyI:3,fillI:.95,ambient:.32,env:.28,lantern:.45,pos:[-3,9,6]},evening:{bg:'#e8cdb4',fog:'#e8cdb4',key:'#ffd299',fill:'#aabacb',ground:'#8b8972',keyI:2.7,fillI:.85,ambient:.34,env:.23,lantern:1.5,pos:[-5,5,4]},night:{bg:'#263e58',fog:'#3e566d',key:'#b8d2f0',fill:'#8eaeca',ground:'#737f82',keyI:1.15,fillI:.95,ambient:.48,env:.22,lantern:3.3,pos:[-3,7,-4]}}
export function Lighting({settings:s}:{settings:Settings}){
 const {gl,scene,invalidate}=useThree(),key=useRef<DirectionalLight>(null),rim=useRef<DirectionalLight>(null),hemi=useRef<HemisphereLight>(null)
 const bg=useMemo(()=>new Color(looks[s.lighting].bg),[]),fog=useMemo(()=>new Fog(looks[s.lighting].fog,17,40),[]),ambient=useRef({value:looks[s.lighting].ambient})
 const portrait=s.view==='portrait'||s.view==='animation'
 useEffect(()=>{const pmrem=new PMREMGenerator(gl),room=new RoomEnvironment(),texture=pmrem.fromScene(room,.04);scene.environment=texture.texture;room.dispose();pmrem.dispose();return()=>{scene.environment=null;texture.dispose()}},[gl,scene])
 useEffect(()=>{scene.background=bg;scene.fog=portrait?null:fog;invalidate();return()=>{scene.fog=null}},[scene,bg,fog,portrait,invalidate])
 useEffect(()=>{invalidate()},[s.lighting,s.reduced,invalidate])
 useFrame((_,dt)=>{
  const l=looks[s.lighting],a=s.reduced||s.paused?1:1-Math.exp(-Math.min(dt,.15)*3),c=new Color(l.bg)
  bg.lerp(c,a);fog.color.lerp(new Color(l.fog),a)
  if(key.current){key.current.color.lerp(new Color(l.key),a);key.current.intensity=MathUtils.lerp(key.current.intensity,l.keyI,a);key.current.position.lerp(new Vector3(...l.pos),a)}
  if(rim.current)rim.current.intensity=MathUtils.lerp(rim.current.intensity,s.lighting==='night'?.70:.50,a)
  if(hemi.current){hemi.current.color.lerp(new Color(l.fill),a);hemi.current.groundColor.lerp(new Color(l.ground),a);hemi.current.intensity=MathUtils.lerp(hemi.current.intensity,l.fillI,a)}
  ambient.current.value=MathUtils.lerp(ambient.current.value,l.ambient,a);scene.environmentIntensity=MathUtils.lerp(scene.environmentIntensity,l.env,a)
  window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,lighting:s.lighting,lightColor:bg.getHexString()}
  if(s.active&&(Math.abs(bg.r-c.r)+Math.abs(bg.g-c.g)+Math.abs(bg.b-c.b))>.002)invalidate()
 })
 return <><ambientLight intensity={.30}/><hemisphereLight ref={hemi} args={[looks[s.lighting].fill,looks[s.lighting].ground,.95]}/>
  <directionalLight ref={key} position={[-3,9,6]} intensity={3} color="#fff2cf" castShadow={s.quality!=='low'} shadow-mapSize={[s.quality==='high'?2048:1024,s.quality==='high'?2048:1024]} shadow-camera-left={portrait?-2.2:-8} shadow-camera-right={portrait?2.2:8} shadow-camera-top={portrait?2.2:8} shadow-camera-bottom={portrait?-2.2:-8} shadow-normalBias={portrait?.006:.025} shadow-bias={-.00015} onUpdate={light=>light.shadow.camera.updateProjectionMatrix()}/>
  <directionalLight ref={rim} position={[4,5,-5]} color="#dae6ec" intensity={.5}/>
 </>
}

export function Particles({settings:s,burst,center,ambient=true}:{settings:Settings;burst:RefObject<number>;center:[number,number,number]|RefObject<[number,number,number]>;ambient?:boolean}){
 const mesh=useRef<InstancedMesh>(null),dummy=useMemo(()=>new Object3D(),[]),t=useRef(0),born=useRef(-20),previous=useRef(0)
 const off=s.reduced||s.effects==='off'||s.view==='architecture',count=s.quality==='low'||s.effects==='reduced'?10:22
 useFrame((_,dt)=>{
  if(!mesh.current)return
  if(burst.current!==previous.current){born.current=t.current;previous.current=burst.current}
  const origin=Array.isArray(center)?center:center.current
  if(s.active&&!s.paused&&!s.reduced)t.current+=Math.min(dt,.15)
  for(let i=0;i<22;i++){
   const k=i*.6180339887,phase=(t.current*.09+k)%1,a=k*6.28
   let x=-4.4+Math.sin(a)*.9+phase*.9,y=.12+(1-phase)*2.3,z=1.1+Math.cos(a)*1.1,scale=.022
   const age=t.current-born.current
   if(age>=0&&age<2.6&&i<10){x=origin[0]+Math.sin(a)*age*.42;y=origin[1]+.3+Math.sin(Math.min(age/2.6,1)*Math.PI)*.6;z=origin[2]+Math.cos(a)*age*.42;scale=.035*(1-age/2.6)}else if(!ambient)scale=0
   if(off||i>=count)scale=0
   dummy.position.set(x,y,z);dummy.rotation.set(a+t.current*.5,a*.6+t.current*.3,a);dummy.scale.setScalar(scale);dummy.updateMatrix();mesh.current.setMatrixAt(i,dummy.matrix)
  }
  mesh.current.instanceMatrix.needsUpdate=true
 })
 return <instancedMesh ref={mesh} args={[undefined,undefined,22]} frustumCulled={false}><planeGeometry args={[1,1]}/><meshStandardMaterial color="#f2c9b9" side={DoubleSide} roughness={.95}/></instancedMesh>
}

export function House({settings:s,player,onDoor,onDoorBlocked,onStory}:{settings:Settings;player:Player;onDoor:()=>void;onDoorBlocked:()=>void;onStory:(kind:string)=>void}){
 const gltf=useGLTF(reforgeURL('house')),{scene,invalidate}=useThree(),model=useMemo(()=>gltf.scene.clone(true),[gltf.scene])
 const mixer=useMemo(()=>new AnimationMixer(model),[model]),opening=useRef(s.door?1:0),blockedNotice=useRef(false),time=useRef(0),[petals,flash]=[useRef(0),useRef(-20)],trigger=useRef(0),lamp=useRef<PointLight>(null),lamp2=useRef<PointLight>(null)
 const glows=useMemo(()=>{const result:MeshStandardMaterial[]=[];model.traverse(o=>{if(o instanceof Mesh){o.castShadow=true;o.receiveShadow=true;const mats=Array.isArray(o.material)?o.material:[o.material];o.material=mats.map(m=>{if(m instanceof MeshStandardMaterial&&m.name.includes('LanternHanjiGlow')){const c=m.clone();result.push(c);return c}return m});if(!Array.isArray((o as Mesh).material)||mats.length===1)o.material=(o.material as MeshStandardMaterial[])[0]}});return result},[model])
 const ripples=useMemo(()=>{const result:{o:Object3D;scale:Vector3}[]=[];model.traverse(o=>{if(o.name.startsWith('BasinRipple'))result.push({o,scale:o.scale.clone()})});return result},[model])
 const doors=useMemo(()=>['DoorLeft','DoorRight'].map(name=>{const o=model.getObjectByName(name)!;return {o,x:o.position.x}}),[model])
 useEffect(()=>{const actions=gltf.animations.map(a=>mixer.clipAction(a).play());return()=>{actions.forEach(a=>a.stop());mixer.uncacheRoot(model)}},[gltf.animations,mixer,model])
 useEffect(()=>{scene.userData.reforgeHouse=model;invalidate();return()=>{delete scene.userData.reforgeHouse}},[model,scene,invalidate])
 useEffect(()=>{model.traverse(o=>{if(o.name.startsWith('PlumDetail'))o.visible=s.quality!=='low';if(o.name==='DistantTownBackdrop')o.visible=s.view!=='architecture'});invalidate()},[model,s.quality,s.view,invalidate])
 useEffect(()=>{blockedNotice.current=false;invalidate()},[s.door,invalidate])
 useEffect(()=>{if(s.reduced){mixer.setTime(.4);invalidate()}},[s.reduced,mixer,invalidate])
 useFrame((_,dt)=>{
  const motion=s.active&&!s.paused&&!s.reduced
  if(motion){const d=Math.min(dt,.15);time.current+=d;mixer.update(d)}
  const occupied=s.view==='play'&&Math.abs(player.position[0])<.84&&Math.abs(player.position[2]+.6)<.52,desired=s.door||occupied&&opening.current>.5?1:0
  if(!s.door&&occupied&&opening.current>.5&&!blockedNotice.current){blockedNotice.current=true;onDoorBlocked()}
  if(!s.paused)opening.current=s.reduced?desired:MathUtils.damp(opening.current,desired,6,Math.min(dt,.15))
  doors.forEach(({o,x},i)=>{o.position.x=x+(i?1:-1)*.56*opening.current})
  const flicker=1+(!s.reduced?.075*Math.sin(time.current*5.1)+.045*Math.sin(time.current*9.3):0),boost=time.current-flash.current<1.2?1.9:1
  for(const material of glows)material.emissiveIntensity=looks[s.lighting].lantern*flicker*boost
  if(lamp.current)lamp.current.intensity=s.lighting==='night'?9*flicker*boost:s.lighting==='evening'?3:0
  if(lamp2.current)lamp2.current.intensity=s.lighting==='night'?7*flicker:s.lighting==='evening'?2:0
  ripples.forEach(({o,scale},i)=>o.scale.copy(scale).multiplyScalar(s.reduced?1:1+.07*Math.sin(time.current*1.3-i*.7)))
  if(s.active&&!s.paused&&Math.abs(opening.current-desired)>.002)invalidate()
  queueMicrotask(()=>{window.__REFORGE_METRICS__={...window.__REFORGE_METRICS__,door:opening.current,environmentTime:time.current,environmentClips:gltf.animations.map(a=>a.name),lanternGlow:glows[0]?.emissiveIntensity,worldInteraction:trigger.current,effects:s.effects}})
 })
 return <><primitive object={model} onClick={(e:{object:Object3D;stopPropagation:()=>void})=>{let o:Object3D|null=e.object;while(o&&o!==model){if(/^DoorLeft|^DoorRight/.test(o.name)){e.stopPropagation();onDoor();break}if(/^InteractiveLantern|^LanternSwing/.test(o.name)){e.stopPropagation();flash.current=time.current;trigger.current++;onStory('lantern');invalidate();break}if(/^PlumCore|^PlumDetail|^PlumWind/.test(o.name)){e.stopPropagation();petals.current++;trigger.current++;onStory('plum');invalidate();break}o=o.parent}}}/>
  <pointLight ref={lamp} position={[.25,1.35,3.45]} color="#ffd699" distance={5} decay={2}/><pointLight ref={lamp2} position={[4.10,1.50,-.15]} color="#ffd699" distance={4.8} decay={2}/>
  <Particles settings={s} burst={petals} center={[-4.4,1,1.1]}/>
 </>
}

export function Contact({settings:s,player}:{settings:Settings;player:Player}){
 const shadow=useRef<Mesh>(null),burst=useRef(0),wasGrounded=useRef(true),wasClip=useRef(''),position=useRef<[number,number,number]>([0,0,2.4])
 useFrame(()=>{
  const portrait=s.view==='portrait'||s.view==='animation',p=portrait?[0,0,0]:player.position
  const ground=portrait?0:floorHeight(p[0],p[2])
  if(shadow.current){shadow.current.position.set(p[0],ground+.008,p[2]);shadow.current.scale.setScalar(Math.max(.5,1-(p[1]-ground)*.4))}
  if(s.active&&!s.paused&&((player.grounded&&!wasGrounded.current)||(player.clip==='Celebration'&&wasClip.current!=='Celebration'))){position.current=[p[0],ground+.05,p[2]];burst.current++}
  wasGrounded.current=player.grounded;wasClip.current=player.clip
 })
 return <><mesh ref={shadow} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[.21,24]}/><meshBasicMaterial color="#596354" transparent opacity={s.quality==='low'?.20:.10} depthWrite={false}/></mesh>
  <Particles settings={s} burst={burst} center={position} ambient={false}/>
 </>
}
