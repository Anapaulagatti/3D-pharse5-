import { useEffect, useMemo, useRef, type ComponentRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { MathUtils, OrthographicCamera, Vector3 } from 'three'
import type { Focus, SceneSettings } from './types'

export const targets: Record<Focus, [number, number, number]> = {
  overview: [.08, .9, 0], dais: [-.4, 1.05, 1], roof: [-1.5, 1.75, -1.6], garden: [-3, 1.22, 1.15],
}
const focusZoom: Record<Focus, number> = { overview: 1, dais: 1.48, roof: 1.20, garden: 1.42 }

export default function PolishedCamera({ settings, animate, onOrbit }: { settings: SceneSettings; animate: boolean; onOrbit: () => void }) {
  const controls = useRef<ComponentRef<typeof OrbitControls>>(null)
  const { camera, size, invalidate } = useThree()
  const desired = useMemo(() => new Vector3(...(settings.scene === 'mascot' ? [0, 1.85, 0] : targets[settings.focus])), [settings.scene, settings.focus])
  const current = useRef(desired.clone()), zoom = useRef(40), cinemaTime = useRef(0)
  const initialTarget = useRef(desired.toArray())
  const manual = useRef(false)
  const cinemaAnchor = useRef(new Vector3()), initialized = useRef(false)
  const axis = useMemo(() => new Vector3(0, 1, 0), [])
  const locations = useMemo(() => ({ mascot: new Vector3(), lantern: new Vector3(), tree: new Vector3() }), [])
  useEffect(() => {
    const ortho = camera as OrthographicCamera
    const fit = settings.scene === 'mascot' ? Math.min(size.width / 3.75, size.height / 4.65)
      : Math.min(size.width / (size.width < 500 ? 14.2 : 12.05), size.height / 9.0)
    zoom.current = fit * (settings.scene === 'courtyard' ? focusZoom[settings.focus] : 1)
    if (!initialized.current || !animate) {
      current.current.copy(desired); controls.current?.target.copy(desired)
      ortho.zoom = zoom.current; ortho.updateProjectionMatrix(); controls.current?.update(); initialized.current = true
    }
    invalidate()
  }, [camera, size, settings.scene, settings.focus, desired, animate, invalidate])
  useEffect(() => { cinemaAnchor.current.copy(camera.position).sub(current.current); cinemaTime.current = 0 }, [camera, settings.cinematic])
  useFrame((_, delta) => {
    const ortho = camera as OrthographicCamera
    if (animate && controls.current) {
      const dt = Math.min(delta, .15)
      current.current.lerp(desired, 1 - Math.exp(-dt * 4))
      if (!manual.current) { ortho.zoom = MathUtils.damp(ortho.zoom, zoom.current, 4, dt); ortho.updateProjectionMatrix() }
      controls.current.target.copy(current.current)
      if (settings.cinematic) {
        cinemaTime.current += dt
        camera.position.copy(cinemaAnchor.current).applyAxisAngle(axis, .16 * Math.sin(cinemaTime.current * .16)).add(current.current)
      }
      controls.current.update()
    }
    const m = window.__STUDIO_METRICS__
    if (m) {
      m.cameraZoom = ortho.zoom; m.cameraTarget = current.current.toArray(); m.cameraPosition = camera.position.toArray()
      if (settings.scene === 'mascot') locations.mascot.set(0, 1.60, 0)
      else locations.mascot.set(-.4, 1.65, 1)
      locations.lantern.set(-2.1, 1, 2.5); locations.tree.set(-3, 1.78, 1.15)
      m.interactivePoints = Object.fromEntries(Object.entries(locations).map(([key, p]) => {
        p.project(camera); return [key, [(p.x + 1) * size.width / 2, (1 - p.y) * size.height / 2]]
      })) as NonNullable<typeof m.interactivePoints>
    }
  })
  return <OrbitControls ref={controls} makeDefault target={initialTarget.current} enablePan={false}
    minZoom={12} maxZoom={220} minPolarAngle={.42} maxPolarAngle={Math.PI / 2.4}
    enableDamping={animate} dampingFactor={.09}
    onStart={() => { manual.current = true; if (settings.cinematic) onOrbit() }}
    onEnd={() => { manual.current = false; zoom.current = (camera as OrthographicCamera).zoom }} />
}
