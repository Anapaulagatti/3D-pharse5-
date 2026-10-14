// Reuses the v0.5 lighting/door/mixer/visibility contracts with lightweight palette art.
import {useEffect,useMemo,useRef} from 'react'
import {useFrame,useThree} from '@react-three/fiber'
import {useGLTF} from '@react-three/drei'
import {AnimationMixer,Color,DirectionalLight,HemisphereLight,MathUtils,Mesh,MeshStandardMaterial,Object3D} from 'three'
import {townURL} from './assets'
import type {Settings} from './types'
import type {Player} from './physics'
import {floorHeight} from './physics'
import world from '../../../exports/v0.6/collision-world.json'
const looks={day:{bg:'#c7e6ec',key:'#fff1d1',fill:'#c2dbea',ground:'#c1c7a6',intensity:2.7,hemi:1.3,glow:.5},evening:{bg:'#f5d6b8',key:'#ffd294',fill:'#b9cde9',ground:'#b1b098',intensity:2.4,hemi:1.2,glow:1.4},night:{bg:'#405c7f',key:'#c5dcff',fill:'#b4d1f1',ground:'#9faea8',intensity:1.4,hemi:1.3,glow:2.8}}
export function Lighting({settings:s}:{settings:Settings}){
 const {scene,invalidate}=useThree(),key=useRef<DirectionalLight>(null),hemi=useRef<HemisphereLight>(null),bg=useMemo(()=>new Color(looks[s.lighting].bg),[])
 useEffect(()=>{scene.background=bg;return()=>{scene.background=null}},[scene,bg])
 useEffect(()=>{invalidate()},[s.lighting,invalidate])
 useFrame((_,dt)=>{const l=looks[s.lighting],a=s.reduced||s.paused?1:1-Math.exp(-Math.min(dt,.15)*4),target=new Color(l.bg);bg.lerp(target,a);if(key.current){key.current.color.lerp(new Color(l.key),a);key.current.intensity=MathUtils.lerp(key.current.intensity,l.intensity,a)}if(hemi.current){hemi.current.color.lerp(new Color(l.fill),a);hemi.current.groundColor.lerp(new Color(l.ground),a);hemi.current.intensity=l.hemi}window.__TOWN_METRICS__={...window.__TOWN_METRICS__,lighting:s.lighting,lightColor:bg.getHexString()};if(s.active&&(Math.abs(bg.r-target.r)+Math.abs(bg.g-target.g)+Math.abs(bg.b-target.b))>.002)invalidate()})
 return <><ambientLight intensity={.40}/><hemisphereLight ref={hemi} args={[looks[s.lighting].fill,looks[s.lighting].ground,1.3]}/><directionalLight ref={key} position={[-3,7,5]} intensity={2.7} castShadow={s.quality!=='low'} shadow-mapSize={s.quality==='high'?[1536,1536]:[1024,1024]} shadow-camera-left={-7} shadow-camera-right={7} shadow-camera-top={7} shadow-camera-bottom={-7} shadow-normalBias={.025} shadow-bias={-.0001}/><directionalLight position={[4,4,-4]} color="#deedff" intensity={.7}/></>
}
export function House({settings:s,player,onDoor,onDoorBlocked,onStory}:{settings:Settings;player:Player;onDoor:()=>void;onDoorBlocked:()=>void;onStory:(kind:string)=>void}){
 const gltf=useGLTF(townURL('house')),{scene,invalidate}=useThree(),model=useMemo(()=>gltf.scene.clone(true),[gltf.scene]),mixer=useMemo(()=>new AnimationMixer(model),[model]),time=useRef(0),opening=useRef(s.door?1:0),flash=useRef(-10),trigger=useRef(0),notice=useRef(false)
 const materials=useMemo(()=>{const found=new Set<MeshStandardMaterial>();model.traverse(o=>{if(o instanceof Mesh){const mats=Array.isArray(o.material)?o.material:[o.material];o.material=mats.map(m=>{const c=m.clone() as MeshStandardMaterial;found.add(c);return c});if(mats.length===1)o.material=(o.material as MeshStandardMaterial[])[0];o.castShadow=!o.name.includes('stone')&&!o.name.includes('paver')&&!o.name.includes('glow');o.receiveShadow=true}});return found},[model])
 const doors=useMemo(()=>['DoorLeft','DoorRight'].map(n=>{const o=model.getObjectByName(n)!;return {o,x:o.position.x}}),[model])
 useEffect(()=>{const actions=gltf.animations.map(c=>mixer.clipAction(c).play());scene.userData.townHouse=model;return()=>{actions.forEach(a=>a.stop());mixer.uncacheRoot(model);delete scene.userData.townHouse}},[gltf.animations,mixer,model,scene])
 useEffect(()=>()=>{materials.forEach(m=>m.dispose())},[materials])
 useEffect(()=>{for(let i=0;i<3;i++){const tree=model.getObjectByName('TreeWind'+i);tree?.children.forEach((o,j)=>o.visible=s.quality!=='low'||j!==2)}invalidate()},[model,s.quality,invalidate])
 useEffect(()=>{notice.current=false;invalidate()},[s.door,s.lighting,invalidate])
 useEffect(()=>{if(s.reduced)mixer.setTime(.4);invalidate()},[s.reduced,mixer,invalidate])
 useFrame((_,dt)=>{const motion=s.active&&!s.paused&&!s.reduced;if(motion){time.current+=Math.min(dt,.15);mixer.update(Math.min(dt,.15))}const occupied=s.view==='play'&&Math.abs(player.position[0]+1.2)<.68&&Math.abs(player.position[2]+1.13)<.42,desired=s.door||occupied&&opening.current>.5?1:0;if(occupied&&!s.door&&opening.current>.5&&!notice.current){notice.current=true;onDoorBlocked()}if(!s.paused)opening.current=s.reduced?desired:MathUtils.damp(opening.current,desired,7,Math.min(dt,.15));doors.forEach(({o,x},i)=>o.position.x=x+(i?1:-1)*world.door.travel*opening.current);const glow=looks[s.lighting].glow*(s.reduced?1:1+.09*Math.sin(time.current*5.3))*(time.current-flash.current<1.3?2:1);for(const m of materials)if(m.name.includes('glow'))m.emissiveIntensity=glow;window.__TOWN_METRICS__={...window.__TOWN_METRICS__,door:opening.current,environmentTime:time.current,environmentClips:gltf.animations.map(a=>a.name),lanternGlow:glow,worldInteraction:trigger.current,effects:s.effects};if(s.active&&!s.paused&&Math.abs(opening.current-desired)>.002)invalidate()})
 return <primitive object={model} onClick={(e:{object:Object3D;stopPropagation:()=>void})=>{let o:Object3D|null=e.object;while(o&&o!==model){if(o.name.startsWith('InteractiveLantern')){e.stopPropagation();flash.current=time.current;trigger.current++;onStory('lantern');invalidate();break}if(/^DoorLeft|^DoorRight/.test(o.name)){e.stopPropagation();onDoor();break}o=o.parent}}}/>
}
export function Contact({settings:s,player}:{settings:Settings;player:Player}){
 const shadow=useRef<Mesh>(null)
 useFrame(()=>{const p=s.view==='portrait'||s.view==='animation'?[0,0,0]:player.position;if(shadow.current){shadow.current.position.set(p[0],floorHeight(p[0],p[2])+.009,p[2]);shadow.current.scale.setScalar(Math.max(.5,1-(p[1]-floorHeight(p[0],p[2]))*.6))}})
 return <mesh ref={shadow} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[.19,24]}/><meshBasicMaterial color="#6a806c" transparent opacity={.17} depthWrite={false}/></mesh>
}
