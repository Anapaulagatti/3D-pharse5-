import { useEffect, useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useAnimations } from '@react-three/drei'
import { Color, DoubleSide, Fog, InstancedMesh, MathUtils, Mesh, MeshStandardMaterial, Object3D, PMREMGenerator } from 'three'
import type { DirectionalLight, HemisphereLight, AmbientLight, PointLight } from 'three'
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js'
import { useStudioModel } from './useStudioModel'
import type { Interaction, SceneSettings } from './types'

const presets = {
  day: { bg: new Color('#e7e9df'), key: new Color('#ffedcf'), fill: new Color('#abc9df'), ambient: .40, hemi: .72, sun: 2.25, rim: .85, warmth: .32, reflection: .13 },
  evening: { bg: new Color('#c7a9a3'), key: new Color('#ffd09a'), fill: new Color('#b3bfdc'), ambient: .34, hemi: .62, sun: 2.35, rim: .95, warmth: 3.8, reflection: .10 },
  night: { bg: new Color('#30465c'), key: new Color('#bdcfe4'), fill: new Color('#86a9ce'), ambient: .36, hemi: .65, sun: .75, rim: 1.15, warmth: 7.0, reflection: .065 },
}

export function Atmosphere({ settings, animate }: { settings: SceneSettings; animate: boolean }) {
  const { scene, gl, invalidate } = useThree()
  const ambient = useRef<AmbientLight>(null), hemi = useRef<HemisphereLight>(null)
  const sun = useRef<DirectionalLight>(null), rim = useRef<DirectionalLight>(null)
  const warmA = useRef<PointLight>(null), warmB = useRef<PointLight>(null), hero = useRef<PointLight>(null)
  const ground = useRef<MeshStandardMaterial>(null)
  const bg = useMemo(() => presets.day.bg.clone(), [])
  const time = useRef(0)
  useEffect(() => {
    const room = new RoomEnvironment(), pmrem = new PMREMGenerator(gl)
    const env = pmrem.fromScene(room, .06)
    scene.environment = env.texture
    scene.environmentIntensity = .18
    scene.background = bg
    scene.fog = new Fog(bg, 24, 55)
    invalidate()
    return () => { scene.environment = null; scene.fog = null; env.dispose(); room.dispose(); pmrem.dispose() }
  }, [scene, gl, bg, invalidate])
  useEffect(() => { invalidate() }, [settings.lighting, animate, invalidate])
  useFrame((_, delta) => {
    if (animate) time.current += Math.min(delta, .15)
    const p = presets[settings.lighting], a = animate ? 1 - Math.exp(-delta * 3.6) : 1
    scene.environmentIntensity = MathUtils.lerp(scene.environmentIntensity, p.reflection, a)
    bg.lerp(p.bg, a)
    if (scene.fog instanceof Fog) scene.fog.color.copy(bg)
    ground.current?.color.copy(bg)
    if (ambient.current) ambient.current.intensity = MathUtils.lerp(ambient.current.intensity, p.ambient, a)
    if (hemi.current) hemi.current.intensity = MathUtils.lerp(hemi.current.intensity, p.hemi, a)
    if (sun.current) {
      const direction = settings.lighting === 'evening' ? [-4,4,5] : settings.lighting === 'night' ? [-3,7,1] : [2,8,5]
      sun.current.position.set(...sun.current.position.toArray().map((v,i) => MathUtils.lerp(v,direction[i],a)) as [number,number,number]); sun.current.intensity = MathUtils.lerp(sun.current.intensity, p.sun, a); sun.current.color.lerp(p.key, a) }
    if (rim.current) { rim.current.intensity = MathUtils.lerp(rim.current.intensity, p.rim, a); rim.current.color.lerp(p.fill, a) }
    const response = settings.interaction.type === 'lantern' ? 1.22 : 1
    const warmth = p.warmth * response * (animate ? 1 + .045 * Math.sin(time.current * 3.5) : 1)
    for (const light of [warmA.current, warmB.current, hero.current]) if (light) light.intensity = MathUtils.lerp(light.intensity, warmth, a)
  })
  return <>
    <ambientLight ref={ambient} intensity={1.05} color="#f2e4cd" />
    <hemisphereLight ref={hemi} args={['#c5daec', '#738577', 1.25]} />
    <directionalLight ref={sun} position={[2, 8, 5]} intensity={2.15} color="#ffedcf" castShadow={settings.quality !== 'low'}
      shadow-mapSize={[settings.quality === 'high' ? 2048 : 1024, settings.quality === 'high' ? 2048 : 1024]}
      shadow-camera-left={-7} shadow-camera-right={7} shadow-camera-top={7} shadow-camera-bottom={-7}
      shadow-normalBias={.04} shadow-bias={-.0002} shadow-radius={3} />
    <directionalLight ref={rim} position={[-4, 5, -4]} intensity={.8} color="#abc9df" />
    {settings.quality !== 'low' && <>
      <pointLight ref={warmA} position={[-2.1, 1.1, 2.5]} color="#ffd59b" intensity={.35} distance={4} decay={2} />
      <pointLight ref={warmB} position={[.9, 1.25, -.75]} color="#ffd59b" intensity={.35} distance={4.4} decay={2} />
    </>}
    <pointLight ref={hero} position={settings.scene === 'courtyard' ? [-.1, 2, 2.4] : [0, 2.3, 2]} color="#ffe4bd" intensity={.35} distance={4.4} decay={2} />
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, settings.scene === 'courtyard' ? -.72 : -.035, 0]} receiveShadow>
      <planeGeometry args={[200, 200]} /><meshStandardMaterial ref={ground} color="#e7e9df" roughness={1} />
    </mesh>
  </>
}

export function LivingArena({ settings, animate, onInteract }: {
  settings: SceneSettings; animate: boolean; onInteract: (type: Interaction) => void
}) {
  const { scene, animations } = useStudioModel('arena-hero')
  const { scene: detail, animations: detailClips } = useStudioModel('hanok-polish')
  const { scene: narrative, animations: canopyClips } = useStudioModel('hanok-living')
  const { actions, mixer } = useAnimations(animations, scene)
  const { actions: wind, mixer: windMixer } = useAnimations(detailClips, detail)
  const { actions: canopy, mixer: canopyMixer } = useAnimations(canopyClips, narrative)
  const invalidate = useThree(s => s.invalidate)
  const time = useRef(0), boost = useRef(0)
  const paper = useMemo(() => {
    const found = new Set<MeshStandardMaterial>()
    scene.traverse(o => { if (o instanceof Mesh) for (const m of Array.isArray(o.material) ? o.material : [o.material]) if (m.name === 'PaperLight') found.add(m as MeshStandardMaterial) })
    return [...found]
  }, [scene])
  useEffect(() => {
    actions.LanternSway?.reset().setEffectiveTimeScale(.85).play()
    wind.GardenBreeze?.reset().setEffectiveTimeScale(.72).play()
    canopy.CanopyWind?.reset().setEffectiveTimeScale(.75).play()
    return () => { mixer.stopAllAction(); windMixer.stopAllAction(); canopyMixer.stopAllAction() }
  }, [actions, wind, canopy, mixer, windMixer, canopyMixer])
  useEffect(() => {
    mixer.timeScale = windMixer.timeScale = canopyMixer.timeScale = animate ? 1 : 0
    if (actions.LanternSway) actions.LanternSway.paused = !animate
    if (wind.GardenBreeze) wind.GardenBreeze.paused = !animate
    if (canopy.CanopyWind) canopy.CanopyWind.paused = !animate
    invalidate()
  }, [actions, wind, canopy, mixer, windMixer, canopyMixer, animate, invalidate])
  useEffect(() => { if (settings.interaction.type === 'lantern') boost.current = 1.25; invalidate() }, [settings.interaction, invalidate])
  useEffect(() => { invalidate() }, [settings.lighting, invalidate])
  useFrame((_, delta) => {
    if (animate) { time.current += Math.min(delta, .15); boost.current = Math.max(0, boost.current - Math.min(delta, .15) * .32) }
    const base = settings.lighting === 'night' ? 2.7 : settings.lighting === 'evening' ? 1.6 : .65
    const intensity = base * (animate ? 1 + .10 * Math.sin(time.current * 3.2) + .035 * Math.sin(time.current * 7.1) : 1) + boost.current
    for (const m of paper) m.emissiveIntensity = MathUtils.lerp(m.emissiveIntensity, intensity, animate ? 1 - Math.exp(-delta * 5) : 1)
    const metrics = window.__STUDIO_METRICS__
    if (metrics) { metrics.environmentTime = time.current; metrics.lanternIntensity = paper[0]?.emissiveIntensity }
  })
  return <group>
    <primitive object={scene} onClick={(e: { object: Object3D; stopPropagation: () => void }) => {
      // Multi-material GLB primitives have generic mesh names beneath the named lantern node.
      let object: Object3D | null = e.object
      while (object && object !== scene) {
        if (/^Lantern(?:Mesh|Swing)/.test(object.name)) { e.stopPropagation(); onInteract('lantern'); return }
        object = object.parent
      }
    }} />
    <primitive object={detail} /><primitive object={narrative} />
    <mesh name="PlumInteraction" visible={false} position={[-3, 1.78, 1.15]} onClick={e => { e.stopPropagation(); onInteract('tree') }}
      onPointerOver={() => { document.body.style.cursor = 'pointer' }} onPointerOut={() => { document.body.style.cursor = '' }}>
      <sphereGeometry args={[.76, 8, 6]} /><meshBasicMaterial transparent opacity={0} depthWrite={false} colorWrite={false} />
    </mesh>
  </group>
}

export function PaperAndPetals({ settings, animate }: { settings: SceneSettings; animate: boolean }) {
  const paper = useRef<InstancedMesh>(null), motes = useRef<InstancedMesh>(null), petals = useRef<InstancedMesh>(null)
  const dummy = useMemo(() => new Object3D(), [])
  const time = useRef(0), petalAge = useRef(9)
  const invalidate = useThree(s => s.invalidate)
  useEffect(() => { if (settings.interaction.type === 'tree') petalAge.current = 0; invalidate() }, [settings.interaction, invalidate])
  useFrame((_, delta) => {
    if (animate) { const dt = Math.min(delta, .15); time.current += dt; petalAge.current += dt }
    const t = time.current
    for (let i = 0; i < 7; i++) {
      if (paper.current) {
        dummy.position.set(Math.sin(i * 2.9) * 3.3 + .16 * Math.sin(t * .55 + i), .9 + (i % 3) * .65 + .13 * Math.sin(t * .7 + i), Math.cos(i * 3.1) * 2.6)
        dummy.rotation.set(.6 + .25 * Math.sin(t + i), t * .15 + i, .4 + .2 * Math.sin(t * .8 + i))
        dummy.scale.setScalar(.065 + (i % 2) * .018); dummy.updateMatrix(); paper.current.setMatrixAt(i, dummy.matrix)
      }
      if (motes.current) {
        dummy.position.set(-.4 + Math.sin(i * 2.3 + t * .15) * 1.9, .6 + (i % 4) * .4 + .15 * Math.sin(t * .9 + i), 1 + Math.cos(i * 2.3 + t * .15) * 1.1)
        dummy.rotation.set(0, 0, 0); dummy.scale.setScalar(.017 + .005 * Math.sin(t + i)); dummy.updateMatrix(); motes.current.setMatrixAt(i, dummy.matrix)
      }
    }
    if (paper.current) paper.current.instanceMatrix.needsUpdate = true
    if (motes.current) motes.current.instanceMatrix.needsUpdate = true
    if (petals.current) {
      for (let i = 0; i < 9; i++) {
        const age = animate ? petalAge.current : .35, show = settings.interaction.type === 'tree' && age < 4.2
        dummy.position.set(-3 + .42 * Math.sin(i * 2.1) + age * .20, Math.max(.25, 1.9 - age * .36 + (i % 3) * .13), 1.15 + .32 * Math.cos(i * 1.8) + age * .13)
        dummy.rotation.set(age * 1.4 + i, i * .7, age * .8)
        dummy.scale.setScalar(show ? .065 : 0); dummy.updateMatrix(); petals.current.setMatrixAt(i, dummy.matrix)
      }
      petals.current.instanceMatrix.needsUpdate = true
    }
  })
  return <>
    {settings.quality !== 'low' && <>
      <instancedMesh ref={paper} args={[undefined, undefined, 7]} frustumCulled={false}>
        <planeGeometry args={[1, .68]} /><meshStandardMaterial color="#f5efe1" side={DoubleSide} roughness={.9} transparent opacity={.78} depthWrite={false} />
      </instancedMesh>
      <instancedMesh ref={motes} args={[undefined, undefined, 7]} frustumCulled={false}>
        <sphereGeometry args={[1, 6, 4]} /><meshBasicMaterial color="#fbe7b2" />
      </instancedMesh>
    </>}
    <instancedMesh ref={petals} args={[undefined, undefined, 9]} frustumCulled={false}>
      <circleGeometry args={[1, 5]} /><meshStandardMaterial color="#e57b69" side={DoubleSide} roughness={.9} />
    </instancedMesh>
  </>
}
