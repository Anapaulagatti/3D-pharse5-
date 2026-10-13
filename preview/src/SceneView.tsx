import { Suspense, useCallback, useEffect, useMemo, useRef, useState, type ComponentRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, useAnimations, useGLTF } from '@react-three/drei'
import { Color, Mesh, MeshStandardMaterial, OrthographicCamera, PCFShadowMap, Vector3 } from 'three'
import type { Object3D } from 'three'
import type { Focus, SceneSettings } from './types'
import { assetURL } from './assets'

const targets: Record<Focus, [number, number, number]> = {
  overview: [0, 1.15, 0], dais: [-.4, .9, 1], roof: [-1.5, 1.6, -1.6], garden: [-3, 1.1, 1.15],
}

function useModel(id: string) {
  const gltf = useGLTF(assetURL(id))
  const scene = useMemo(() => {
    const clone = gltf.scene.clone(true)
    const materials = new Map<MeshStandardMaterial, MeshStandardMaterial>()
    clone.traverse(object => {
      if (!(object instanceof Mesh)) return
      object.castShadow = true
      object.receiveShadow = true
      const copy = (m: MeshStandardMaterial) => {
        if (!materials.has(m)) materials.set(m, m.clone())
        return materials.get(m)!
      }
      object.material = Array.isArray(object.material) ? object.material.map(copy) : copy(object.material as MeshStandardMaterial)
    })
    return clone
  }, [gltf.scene])
  useEffect(() => () => {
    const materials = new Set<MeshStandardMaterial>()
    scene.traverse(object => {
      if (object instanceof Mesh) {
        const list = Array.isArray(object.material) ? object.material : [object.material]
        for (const m of list) materials.add(m as MeshStandardMaterial)
      }
    })
    for (const material of materials) material.dispose()
  }, [scene])
  return { ...gltf, scene }
}

function Mascot({ settings, animate, onReady }: { settings: SceneSettings; animate: boolean; onReady: () => void }) {
  const invalidate = useThree(state => state.invalidate)
  const { scene, animations } = useModel('mascot-base')
  const { actions, mixer } = useAnimations(animations, scene)
  const root = useMemo(() => scene.getObjectByName('MascotRoot')!, [scene])
  const frames = useRef(0)
  const reported = useRef(false)
  useEffect(() => {
    mixer.stopAllAction()
    const action = actions[settings.mood]
    if (!action) throw new Error(`Missing mascot clip ${settings.mood}`)
    action.reset().setEffectiveWeight(1).play()
    return () => { mixer.stopAllAction() }
  }, [actions, settings.mood, mixer])
  useEffect(() => {
    const action = actions[settings.mood]
    if (!action) return
    action.paused = !animate
    if (settings.reducedMotion || (settings.paused && action.time === 0)) { action.time = .8; mixer.update(0) }
    invalidate()
  }, [actions, animate, settings.mood, settings.reducedMotion, settings.paused, mixer, invalidate])
  useFrame(({ gl, invalidate }) => {
    frames.current++
    if (frames.current < 2) invalidate()
    if (!reported.current && frames.current >= 2) { reported.current = true; onReady() }
    queueMicrotask(() => { window.__STUDIO_METRICS__ = {
      frames: frames.current, activeClip: settings.mood, clipTime: actions[settings.mood]?.time || 0,
      mascotY: root.position.y, drawCalls: gl.info.render.calls, triangles: gl.info.render.triangles,
      textures: gl.info.memory.textures, geometries: gl.info.memory.geometries, assetsLoaded: true,
      reducedMotion: settings.reducedMotion, paused: settings.paused, focus: settings.focus, quality: settings.quality,
      canvasWidth: gl.domElement.width, canvasHeight: gl.domElement.height,
    } })
  })
  return <group position={settings.scene === 'courtyard' ? [-.4, .48, 1] : [0, .1, 0]} scale={settings.scene === 'courtyard' ? .82 : 1.35} rotation={[0, .25, 0]}>
    <primitive object={scene} />
  </group>
}

function Arena({ settings, animate }: { settings: SceneSettings; animate: boolean }) {
  const invalidate = useThree(state => state.invalidate)
  const { scene, animations } = useModel('arena-hero')
  const { actions, mixer } = useAnimations(animations, scene)
  useEffect(() => {
    const action = actions.LanternSway
    action?.reset().play()
    return () => { mixer.stopAllAction() }
  }, [actions, mixer])
  useEffect(() => {
    if (actions.LanternSway) actions.LanternSway.paused = !animate
    if (!animate) { actions.LanternSway?.reset(); mixer.update(0) }
    invalidate()
  }, [actions, animate, mixer, invalidate])
  useEffect(() => {
    scene.traverse(o => {
      if (!(o instanceof Mesh)) return
      const list = Array.isArray(o.material) ? o.material : [o.material]
      for (const m of list) {
        if (m instanceof MeshStandardMaterial && m.name === 'PaperLight') {
          m.emissiveIntensity = settings.lighting === 'night' ? 2.2 : settings.lighting === 'evening' ? 1.4 : .5
        }
      }
    })
    invalidate()
  }, [scene, settings.lighting, invalidate])
  return <primitive object={scene} />
}

function FocusMarker({ point, label, selected, onPick }: { point: Focus; label: string; selected: boolean; onPick: (point: Focus) => void }) {
  const [hovered, setHovered] = useState(false)
  const pos = targets[point]
  return <group position={[pos[0], point === 'roof' ? 2.9 : pos[1] + .6, pos[2]]}>
    <mesh name={`Poi-${label}`} scale={hovered || selected ? 1.35 : 1} onClick={e => { e.stopPropagation(); onPick(point) }}
      onPointerOver={e => { e.stopPropagation(); setHovered(true) }} onPointerOut={() => setHovered(false)}>
      <sphereGeometry args={[.065, 12, 8]} /><meshStandardMaterial color="#cfac67" emissive="#cfac67" emissiveIntensity={selected ? .8 : .2} />
    </mesh>
  </group>
}

function PaperMotes({ animate, low }: { animate: boolean; low: boolean }) {
  const group = useRef<Object3D>(null)
  const positions = useMemo(() => Array.from({ length: 18 }, (_, i) => [Math.sin(i * 11.1) * 3, .7 + (i % 5) * .5, Math.cos(i * 8.3) * 2.8] as [number, number, number]), [])
  useFrame(({ clock }) => { if (group.current && animate) group.current.rotation.y = Math.sin(clock.elapsedTime * .13) * .1 })
  return low ? null : <group ref={group}>
    {positions.map((p, i) => <mesh key={i} position={p} rotation={[0, i, .6]}>
      <planeGeometry args={[.025, .035]} /><meshBasicMaterial color="#fff1cc" transparent opacity={.65} depthWrite={false} />
    </mesh>)}
  </group>
}

function CameraRig({ settings, animate }: { settings: SceneSettings; animate: boolean }) {
  const controls = useRef<ComponentRef<typeof OrbitControls>>(null)
  const { camera, size, invalidate } = useThree()
  const desired = useMemo(() => new Vector3(...(settings.scene === 'mascot' ? [0, 1.15, 0] as [number, number, number] : targets[settings.focus])), [settings.scene, settings.focus])
  const current = useRef(new Vector3(0, .85, .45))
  useEffect(() => {
    const orthographic = camera as OrthographicCamera
    const fit = settings.scene === 'mascot' ? Math.min(size.width / 3.5, size.height / 3.9) : Math.min(size.width / 12.2, size.height / 9.3)
    orthographic.zoom = fit * (settings.scene === 'courtyard' && settings.focus !== 'overview' ? 1.12 : 1)
    orthographic.updateProjectionMatrix()
    if (!animate) { current.current.copy(desired); controls.current?.target.copy(desired); controls.current?.update() }
    invalidate()
  }, [camera, size.width, size.height, settings.scene, settings.focus, desired, animate, invalidate])
  useFrame((_, delta) => {
    if (animate && controls.current && current.current.distanceTo(desired) > .001) {
      current.current.lerp(desired, 1 - Math.exp(-delta * 4))
      controls.current.target.copy(current.current)
      controls.current.update()
    }
  })
  return <OrbitControls ref={controls} makeDefault target={[0, 1.15, 0]} enablePan={false} minZoom={12} maxZoom={180}
    minPolarAngle={.35} maxPolarAngle={Math.PI / 2.3} enableDamping={animate} dampingFactor={.08} />
}

export default function SceneView({ settings, onReady, onFailure, onFocus }: {
  settings: SceneSettings; onReady: () => void; onFailure: () => void; onFocus: (focus: Focus) => void
}) {
  const container = useRef<HTMLDivElement>(null)
  const canvas = useRef<HTMLCanvasElement | null>(null)
  const [visible, setVisible] = useState(true)
  const [tabVisible, setTabVisible] = useState(!document.hidden)
  useEffect(() => {
    const observer = new IntersectionObserver(entries => setVisible(entries[0].isIntersecting))
    if (container.current) observer.observe(container.current)
    const changed = () => setTabVisible(!document.hidden)
    document.addEventListener('visibilitychange', changed)
    return () => { observer.disconnect(); document.removeEventListener('visibilitychange', changed) }
  }, [])
  const lost = useCallback((event: Event) => { event.preventDefault(); onFailure() }, [onFailure])
  useEffect(() => () => canvas.current?.removeEventListener('webglcontextlost', lost), [lost])
  const animate = visible && tabVisible && !settings.reducedMotion && !settings.paused
  const night = settings.lighting === 'night'
  const evening = settings.lighting === 'evening'
  const bg = night ? '#182e43' : evening ? '#d2c5b3' : '#e7e9df'
  return <div className="canvas-container" ref={container}>
    <Canvas orthographic shadows={settings.quality !== 'low' ? { type: PCFShadowMap } : false}
      camera={{ position: [10, 8.7, 12], zoom: 42, near: .1, far: 100 }}
      dpr={settings.quality === 'low' ? 1 : [1, settings.quality === 'high' ? 2 : 1.5]}
      frameloop={animate ? 'always' : 'demand'} gl={{ antialias: settings.quality !== 'low', alpha: false }}
      onCreated={({ gl }) => {
        canvas.current = gl.domElement
        gl.domElement.addEventListener('webglcontextlost', lost)
        gl.setClearColor(new Color(bg))
      }}
      fallback={<p>WebGL không khả dụng. Chuyển sang ảnh tĩnh.</p>}
    >
      <color attach="background" args={[bg]} />
      <ambientLight intensity={night ? .65 : 1.15} color={night ? '#afc7e0' : '#fff2d9'} />
      <hemisphereLight args={[night ? '#94b9d9' : '#e3efff', night ? '#293c55' : '#b8af92', night ? .75 : 1.4]} />
      <directionalLight position={[3, 8, 5]} intensity={night ? .8 : evening ? 2.3 : 2.5} color={night ? '#afc7e0' : '#ffdeb0'} castShadow
        shadow-mapSize={[settings.quality === 'high' ? 2048 : 1024, settings.quality === 'high' ? 2048 : 1024]}
        shadow-camera-left={-8} shadow-camera-right={8} shadow-camera-top={8} shadow-camera-bottom={-8} shadow-normalBias={.045} />
      <directionalLight position={[-4, 3, -3]} intensity={night ? .4 : .7} color="#a8c7eb" />
      {night && settings.quality !== 'low' && settings.scene === 'courtyard' && <>
        <pointLight position={[-2.1, .95, 2.5]} color="#ffd59b" intensity={4} distance={3.5} decay={2} />
        <pointLight position={[.9, 1.1, -.75]} color="#ffd59b" intensity={5} distance={4} decay={2} />
      </>}
      <Suspense fallback={null}>
        {settings.scene === 'courtyard' ? <Arena settings={settings} animate={animate} /> : <mesh position={[0, .035, 0]} receiveShadow>
          <cylinderGeometry args={[1.15, 1.2, .09, 64]} /><meshStandardMaterial color="#f5efe1" roughness={.6} />
        </mesh>}
        <Mascot settings={settings} animate={animate} onReady={onReady} />
      </Suspense>
      {settings.scene === 'courtyard' && <>
        <FocusMarker point="dais" label="Đài gốm" selected={settings.focus === 'dais'} onPick={onFocus} />
        <FocusMarker point="roof" label="Mái hanok" selected={settings.focus === 'roof'} onPick={onFocus} />
        <FocusMarker point="garden" label="Vườn mận" selected={settings.focus === 'garden'} onPick={onFocus} />
        <PaperMotes animate={animate} low={settings.quality === 'low'} />
      </>}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.72, 0]} receiveShadow>
        <planeGeometry args={[200, 200]} /><meshStandardMaterial color={bg} roughness={1} />
      </mesh>
      <CameraRig settings={settings} animate={animate} />
    </Canvas>
  </div>
}
