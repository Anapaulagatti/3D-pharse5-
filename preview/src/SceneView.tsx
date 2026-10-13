import { useCallback, useEffect, useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { Group } from 'three'
import type { SceneSettings } from './types'

const colors = { jade: '#72beac', cream: '#f5efe1', ink: '#293c55', brass: '#cfac67', coral: '#e57b69', wood: '#91745b' }

function Block({ position, size, color, rotation = [0, 0, 0] }: {
  position: [number, number, number]
  size: [number, number, number]
  color: string
  rotation?: [number, number, number]
}) {
  return <mesh position={position} rotation={rotation} castShadow receiveShadow>
    <boxGeometry args={size} /><meshStandardMaterial color={color} roughness={0.78} />
  </mesh>
}

function Pavilion({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) {
  return <group position={position} scale={scale}>
    <Block position={[0, 0.14, 0]} size={[2.6, 0.25, 1.8]} color={colors.cream} />
    {[-0.9, 0.9].flatMap(x => [-0.55, 0.55].map(z =>
      <Block key={`${x}:${z}`} position={[x, 0.83, z]} size={[0.12, 1.25, 0.12]} color={colors.wood} />))}
    <Block position={[0, 0.65, -0.63]} size={[1.8, 0.86, 0.1]} color="#ded2b7" />
    {[-0.65, -0.3, 0.05, 0.4, 0.75].map(x =>
      <Block key={x} position={[x, 0.66, -0.55]} size={[0.035, 0.8, 0.02]} color={colors.wood} />)}
    <Block position={[0, 1.45, 0]} size={[2.8, 0.12, 2]} color={colors.wood} />
    {[-1, 1].map(side => <group key={side}>
      <Block position={[0, 1.67, side * 0.46]} size={[2.7, 0.1, 1.25]} color={colors.ink} rotation={[side * 0.38, 0, 0]} />
      {Array.from({ length: 12 }, (_, i) =>
        <Block key={i} position={[-1.26 + i * 0.23, 1.75, side * 0.46]} size={[0.09, 0.065, 1.25]} color="#40556b" rotation={[side * 0.38, 0, 0]} />)}
      <Block position={[0, 1.49, side * 1.05]} size={[2.98, 0.095, 0.17]} color={colors.jade} />
    </group>)}
    <Block position={[0, 1.95, 0]} size={[2.9, 0.1, 0.14]} color={colors.ink} />
  </group>
}

function Mascot({ mood, animate, position = [0, 0.4, 0] }: {
  mood: SceneSettings['mood']; animate: boolean; position?: [number, number, number]
}) {
  const group = useRef<Group>(null)
  useFrame(({ clock }) => {
    if (group.current && animate) {
      group.current.position.y = position[1] + Math.sin(clock.elapsedTime * (mood === 'celebrate' ? 3 : 1.5)) * 0.06
      group.current.rotation.z = Math.sin(clock.elapsedTime * 1.2) * (mood === 'celebrate' ? 0.1 : 0.025)
    }
  })
  useEffect(() => {
    if (group.current) { group.current.position.y = position[1]; group.current.rotation.z = 0 }
  }, [animate, position])
  return <group ref={group} position={position} rotation={[0, 0.4, 0]}>
    <mesh position={[0, 0.52, 0]} scale={[0.48, 0.58, 0.42]} castShadow>
      <sphereGeometry args={[1, 32, 24]} /><meshStandardMaterial color={colors.jade} roughness={0.3} metalness={0.08} />
    </mesh>
    <mesh position={[0, 0.35, 0.33]} scale={[0.25, 0.28, 0.1]}>
      <sphereGeometry args={[1, 24, 16]} /><meshStandardMaterial color={colors.cream} roughness={0.65} />
    </mesh>
    {[-1, 1].map(side => <group key={side}>
      <mesh position={[side * 0.27, side === 1 ? 1.08 : 1.02, 0]} rotation={[0, 0, side * -0.3]} scale={[0.14, side === 1 ? 0.3 : 0.23, 0.13]} castShadow>
        <dodecahedronGeometry args={[1, 0]} /><meshStandardMaterial color={side === 1 ? colors.cream : colors.jade} roughness={0.48} />
      </mesh>
      <mesh position={[side * 0.15, 0.65, 0.385]} scale={[1, mood === 'celebrate' ? 0.3 : 1, 1]}>
        <sphereGeometry args={[0.036, 12, 8]} /><meshStandardMaterial color="#15243a" />
      </mesh>
      <mesh position={[side * 0.24, 0.55, 0.36]} scale={[1, 0.45, 0.4]}>
        <sphereGeometry args={[0.064, 12, 8]} /><meshStandardMaterial color={colors.coral} />
      </mesh>
      <mesh position={[side * 0.39, 0.4 + (mood === 'ready' ? 0.11 : 0), 0]} scale={[0.14, 0.2, 0.15]} rotation={[0, 0, side * (mood === 'celebrate' ? -0.8 : 0.3)]} castShadow>
        <sphereGeometry args={[1, 16, 12]} /><meshStandardMaterial color={colors.jade} roughness={0.3} />
      </mesh>
    </group>)}
    <mesh position={[0, 0.55, 0.417]} rotation={[0, 0, Math.PI]}>
      <torusGeometry args={[0.055, 0.012, 6, 16, Math.PI]} /><meshStandardMaterial color="#15243a" />
    </mesh>
  </group>
}

function Lantern({ position, evening }: { position: [number, number, number]; evening: boolean }) {
  return <group position={position}>
    <Block position={[0, 0.62, 0]} size={[0.055, 1.25, 0.055]} color={colors.wood} />
    <Block position={[0.12, 1.23, 0]} size={[0.34, 0.05, 0.07]} color={colors.wood} />
    <mesh position={[0.22, 0.98, 0]}>
      <capsuleGeometry args={[0.12, 0.16, 4, 12]} />
      <meshStandardMaterial color="#ffe3a2" emissive="#ffc975" emissiveIntensity={evening ? 1.2 : 0.2} roughness={0.65} />
    </mesh>
    <Block position={[0.22, 1.18, 0]} size={[0.22, 0.045, 0.22]} color={colors.brass} />
  </group>
}

function Courtyard({ settings, animate }: { settings: SceneSettings; animate: boolean }) {
  return <group>
    <Block position={[0, -0.18, 0]} size={[5.8, 0.36, 4.7]} color="#91afa1" />
    <Block position={[0, 0.025, 0]} size={[5.65, 0.065, 4.55]} color="#d2d4c0" />
    {[-1.8, -1.2, -0.6, 0, 0.6, 1.2, 1.8].map(z =>
      <Block key={z} position={[0.65, 0.075, z]} size={[0.9, 0.065, 0.44]} color={colors.cream} />)}
    <Pavilion position={[-1.4, 0.07, -1.1]} scale={0.85} />
    <Pavilion position={[1.85, 0.07, -1.15]} scale={0.5} />
    <mesh position={[0.1, 0.17, 0.7]} receiveShadow castShadow>
      <cylinderGeometry args={[1.05, 1.1, 0.2, 48]} /><meshStandardMaterial color={colors.brass} roughness={0.55} />
    </mesh>
    <mesh position={[0.1, 0.28, 0.7]} receiveShadow>
      <cylinderGeometry args={[0.98, 0.98, 0.035, 48]} /><meshStandardMaterial color={colors.cream} />
    </mesh>
    <Mascot position={[0.1, 0.31, 0.7]} mood={settings.mood} animate={animate} />
    {[[-2.3, 0.07, 1.5], [2.2, 0.07, 1.45], [0.2, 0.07, -1.7]].map((p, i) =>
      <Lantern key={i} position={p as [number, number, number]} evening={settings.lighting === 'evening'} />)}
    <group position={[-2.05, 0.06, 0.55]}>
      <Block position={[0, 0.45, 0]} size={[0.1, 0.9, 0.1]} color={colors.wood} rotation={[0, 0, 0.15]} />
      {[[0, 1, 0], [-0.25, 0.85, 0.1], [0.22, 1.1, 0.05], [0.1, 0.9, -0.25]].map((p, i) =>
        <mesh key={i} position={p as [number, number, number]} castShadow>
          <icosahedronGeometry args={[0.3, 0]} /><meshStandardMaterial color={i % 2 ? '#ecc6b8' : colors.coral} roughness={1} />
        </mesh>)}
    </group>
  </group>
}

export default function SceneView({ settings, onReady, onFailure }: {
  settings: SceneSettings; onReady: () => void; onFailure: () => void
}) {
  const container = useRef<HTMLDivElement>(null)
  const canvas = useRef<HTMLCanvasElement | null>(null)
  const [visible, setVisible] = useState(true)
  useEffect(() => {
    const observer = new IntersectionObserver(entries => setVisible(entries[0].isIntersecting))
    if (container.current) observer.observe(container.current)
    return () => observer.disconnect()
  }, [])
  const lost = useCallback((event: Event) => { event.preventDefault(); onFailure() }, [onFailure])
  useEffect(() => () => canvas.current?.removeEventListener('webglcontextlost', lost), [lost])
  const animate = visible && !settings.reducedMotion && !settings.paused
  const evening = settings.lighting === 'evening'
  return <div className="canvas-container" ref={container}>
    <Canvas
      orthographic
      shadows={settings.quality !== 'low'}
      camera={{ position: [7, 6, 8], zoom: settings.mobile ? 37 : 62, near: 0.1, far: 60 }}
      dpr={settings.quality === 'low' ? 1 : [1, settings.quality === 'high' ? 2 : 1.5]}
      frameloop={animate ? 'always' : 'demand'}
      gl={{ antialias: settings.quality !== 'low', alpha: false }}
      onCreated={({ gl }) => {
        canvas.current = gl.domElement
        gl.domElement.addEventListener('webglcontextlost', lost)
        onReady()
      }}
      fallback={<p>WebGL không khả dụng. Chuyển sang minh họa tĩnh.</p>}
    >
      <color attach="background" args={[evening ? '#b6c4ce' : '#e7ece3']} />
      <ambientLight intensity={evening ? 0.8 : 1.4} color={evening ? '#afc7e0' : '#fff6e0'} />
      <directionalLight position={[3, 7, 4]} intensity={evening ? 2 : 2.8} color={evening ? '#ffdab0' : '#fff1d0'} castShadow shadow-mapSize={[1024, 1024]} shadow-camera-left={-7} shadow-camera-right={7} shadow-camera-top={7} shadow-camera-bottom={-7} shadow-normalBias={0.05} />
      <directionalLight position={[-4, 3, -2]} intensity={1.1} color="#afc7e0" />
      {settings.scene === 'courtyard' ? <Courtyard settings={settings} animate={animate} /> : <group scale={1.7}>
        <mesh position={[0, -0.03, 0]} receiveShadow><cylinderGeometry args={[1, 1.05, 0.14, 48]} /><meshStandardMaterial color={colors.cream} /></mesh>
        <Mascot mood={settings.mood} animate={animate} position={[0, 0.05, 0]} />
      </group>}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.39, 0]} receiveShadow>
        <planeGeometry args={[200, 200]} /><meshStandardMaterial color={evening ? '#b6c4ce' : '#e7ece3'} roughness={1} />
      </mesh>
      <OrbitControls makeDefault target={[0, 0.7, 0]} enablePan={false} minZoom={25} maxZoom={100} minPolarAngle={0.35} maxPolarAngle={Math.PI / 2.2} enableDamping={animate} />
    </Canvas>
  </div>
}
