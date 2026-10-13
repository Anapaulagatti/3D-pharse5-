import { Suspense, useCallback, useEffect, useRef, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { PCFSoftShadowMap } from 'three'
import type { Focus, Interaction, SceneSettings } from './types'
import LivingMascot from './LivingMascot'
import { Atmosphere, LivingArena, PaperAndPetals } from './LivingWorld'
import PolishedCamera, { targets } from './PolishedCamera'

function FocusMarker({ point, label, selected, onPick }: { point: Focus; label: string; selected: boolean; onPick: (point: Focus) => void }) {
  const [hovered, setHovered] = useState(false)
  const pos = targets[point]
  return <group position={[pos[0], point === 'roof' ? 2.9 : pos[1] + .55, pos[2]]}>
    <mesh name={'Poi-' + label} scale={hovered || selected ? 1.35 : 1}
      onClick={e => { e.stopPropagation(); onPick(point) }}
      onPointerOver={e => { e.stopPropagation(); setHovered(true) }} onPointerOut={() => setHovered(false)}>
      <sphereGeometry args={[.055, 10, 6]} /><meshStandardMaterial color="#cfac67" emissive="#cfac67" emissiveIntensity={selected ? .7 : .15} />
    </mesh>
  </group>
}

export default function SceneView({ settings, onReady, onFailure, onFocus, onInteract, onOrbit }: {
  settings: SceneSettings; onReady: () => void; onFailure: () => void; onFocus: (focus: Focus) => void
  onInteract: (type: Interaction) => void; onOrbit: () => void
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
    return () => { observer.disconnect(); document.removeEventListener('visibilitychange', changed); document.body.style.cursor = '' }
  }, [])
  const lost = useCallback((event: Event) => { event.preventDefault(); onFailure() }, [onFailure])
  useEffect(() => () => canvas.current?.removeEventListener('webglcontextlost', lost), [lost])
  const animate = visible && tabVisible && !settings.reducedMotion && !settings.paused
  return <div className="canvas-container" ref={container}>
    <Canvas orthographic shadows={settings.quality !== 'low' ? { type: PCFSoftShadowMap } : false}
      camera={{ position: settings.scene === 'courtyard' ? [9, 7.7, 11] : [3.1, 2.6, 6], zoom: 42, near: .1, far: 100 }}
      dpr={settings.quality === 'low' ? 1 : [1, settings.quality === 'high' ? 1.75 : 1.25]}
      frameloop={animate ? 'always' : 'demand'} gl={{ antialias: settings.quality !== 'low', alpha: false }}
      onCreated={({ gl }) => { canvas.current = gl.domElement; gl.domElement.addEventListener('webglcontextlost', lost) }}
      fallback={<p>WebGL không khả dụng. Chuyển sang ảnh tĩnh.</p>}>
      <Atmosphere settings={settings} animate={animate} />
      <Suspense fallback={null}>
        {settings.scene === 'courtyard' ? <LivingArena settings={settings} animate={animate} onInteract={onInteract} /> : <mesh position={[0, .035, 0]} receiveShadow>
          <cylinderGeometry args={[1.15, 1.2, .09, 48]} /><meshStandardMaterial color="#f5efe1" roughness={.58} />
        </mesh>}
        <LivingMascot settings={settings} animate={animate} onReady={onReady} onInteract={onInteract} />
      </Suspense>
      {settings.scene === 'courtyard' && <>
        <FocusMarker point="dais" label="Đài gốm" selected={settings.focus === 'dais'} onPick={onFocus} />
        <FocusMarker point="roof" label="Mái hanok" selected={settings.focus === 'roof'} onPick={onFocus} />
        <FocusMarker point="garden" label="Vườn mận" selected={settings.focus === 'garden'} onPick={onFocus} />
        <PaperAndPetals settings={settings} animate={animate} />
      </>}
      <PolishedCamera settings={settings} animate={animate} onOrbit={onOrbit} />
    </Canvas>
  </div>
}
