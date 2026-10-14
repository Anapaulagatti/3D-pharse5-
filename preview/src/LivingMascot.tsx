import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useAnimations } from '@react-three/drei'
import { Group, LoopOnce, LoopRepeat, MathUtils, Mesh, Vector3 } from 'three'
import type { AnimationAction } from 'three'
import type { Interaction, Mood, SceneSettings } from './types'
import { useStudioModel } from './useStudioModel'

// Twelve authored Blender clips drive body AND face. Camera awareness/blinks are secondary.
export default function LivingMascot({ settings, animate, onReady, onInteract }: {
  settings: SceneSettings; animate: boolean; onReady: () => void; onInteract: (type: Interaction) => void
}) {
  const invalidate = useThree(s => s.invalidate)
  const { scene, animations } = useStudioModel('mascot-living')
  const { actions, mixer } = useAnimations(animations, scene)
  const [mood, setMood] = useState<Mood>(settings.mood), [gestureId, setGestureId] = useState(0)
  const outer = useRef<Group>(null), follow = useRef<Group>(null)
  const previous = useRef<AnimationAction | null>(null), temporary = useRef(0)
  const intro = useRef(false), age = useRef(0), elapsed = useRef(0), frames = useRef(0), reported = useRef(false)
  const world = useMemo(() => new Vector3(), [])
  const root = useMemo(() => scene.getObjectByName('MascotRoot')!, [scene])
  const head = useMemo(() => scene.getObjectByName('HeadPivot')!, [scene])
  const eyePivots = useMemo(() => ['FaceEyeLeftPivot', 'FaceEyeRightPivot'].map(n => scene.getObjectByName(n)!), [scene])
  const faceParts = useMemo(() => {
    const parts: Mesh[] = []
    scene.traverse(o => { if (o instanceof Mesh && /Face|EyeLeft|EyeRight|EyeCatchlight/.test(o.name)) parts.push(o) })
    return parts
  }, [scene])
  const gesture = useCallback((next: Mood) => { temporary.current = next === 'ReturnToIdle' ? 2 : 1; age.current = 0; setMood(next); setGestureId(n => n + 1); invalidate() }, [invalidate])
  useEffect(() => { temporary.current = 0; age.current = 0; setMood(settings.mood); setGestureId(n => n + 1) }, [settings.mood])
  useEffect(() => { if (animate && !intro.current && settings.mood === 'Idle') { intro.current = true; gesture('Greeting') } }, [animate, settings.mood, gesture])
  useEffect(() => { if (settings.interaction.type === 'mascot' && settings.interaction.id) { intro.current = true; gesture('ClickReaction') } }, [settings.interaction, gesture])
  useEffect(() => { if (settings.action.id && settings.action.mood) { intro.current = true; gesture(settings.action.mood) } }, [settings.action, gesture])
  useEffect(() => {
    const action = actions[mood]
    if (!action) throw new Error('Missing authored v0.4 mascot clip: ' + mood)
    const old = previous.current
    action.reset().setEffectiveWeight(1).setEffectiveTimeScale(1).setLoop(temporary.current ? LoopOnce : LoopRepeat, temporary.current ? 1 : Infinity)
    action.clampWhenFinished = !!temporary.current
    if (old && old !== action && animate) { action.play(); action.crossFadeFrom(old, .20, false) }
    else { if (old && old !== action) old.stop(); action.play() }
    previous.current = action
    action.paused = !animate
    if (settings.reducedMotion) action.time = Math.min(action.getClip().duration * .4, .85)
    mixer.update(0); invalidate()
  }, [actions, mood, gestureId, mixer, invalidate])
  useEffect(() => {
    const finished = (event: { action: AnimationAction }) => {
      if (!temporary.current || event.action !== previous.current) return
      if (temporary.current === 1) { temporary.current = 2; setMood('ReturnToIdle') }
      else { temporary.current = 0; age.current = 0; setMood('Idle') }
    }
    mixer.addEventListener('finished', finished)
    return () => mixer.removeEventListener('finished', finished)
  }, [mixer])
  useEffect(() => {
    mixer.timeScale = animate ? 1 : 0
    const action = actions[mood]
    if (action) {
      action.paused = !animate
      if (settings.reducedMotion) action.time = Math.min(action.getClip().duration * .4, .85)
    }
    mixer.update(0); invalidate()
  }, [actions, mood, animate, settings.reducedMotion, mixer, invalidate])
  useEffect(() => () => { mixer.stopAllAction() }, [mixer])
  useFrame(({ gl, camera }, delta) => {
    frames.current++
    let blink = 1
    if (animate) {
      const dt = Math.min(delta, .15); elapsed.current += dt
      if (!temporary.current && mood === 'Idle') { age.current += dt; if (age.current > 12) gesture('Curious') }
      const t = elapsed.current, phase = t % 4.8
      blink = phase > 4.58 ? 1 - .95 * Math.sin((phase - 4.58) / .22 * Math.PI) : 1
      if (outer.current && follow.current) {
        outer.current.getWorldPosition(world)
        const yaw = Math.atan2(camera.position.x - world.x, camera.position.z - world.z)
        follow.current.rotation.y = MathUtils.damp(follow.current.rotation.y, yaw, 1.5, dt)
      }
    }
    for (const pivot of eyePivots) {
      pivot.scale.y = blink
      pivot.rotation.y = animate ? .055 * Math.sin(elapsed.current * .55) : 0
    }
    // Exported hidden face shapes use tiny positive scales; skip their draws on the browser.
    for (const part of faceParts) part.visible = Math.max(part.scale.x, part.scale.y, part.scale.z) > .04
    if (frames.current < 2) invalidate()
    if (!reported.current && frames.current >= 2) { reported.current = true; onReady() }
    const facial = Object.fromEntries(faceParts.filter(o => o.visible).map(o => [o.name, o.scale.toArray()]))
    const leftFoot = scene.getObjectByName('LegLeftPivot')!, rightFoot = scene.getObjectByName('LegRightPivot')!
    queueMicrotask(() => { window.__STUDIO_METRICS__ = {
      ...window.__STUDIO_METRICS__, frames: frames.current, activeClip: mood, clipTime: actions[mood]?.time || 0,
      mascotY: root.position.y, drawCalls: gl.info.render.calls, triangles: gl.info.render.triangles,
      textures: gl.info.memory.textures, geometries: gl.info.memory.geometries, assetsLoaded: true,
      reducedMotion: settings.reducedMotion, paused: settings.paused, focus: settings.focus, quality: settings.quality,
      canvasWidth: gl.domElement.width, canvasHeight: gl.domElement.height, motionActive: animate,
      cinematic: settings.cinematic, facialBlink: blink, facialExpression: mood, facialParts: facial,
      limbRotations: [leftFoot.quaternion.toArray(), rightFoot.quaternion.toArray()], rootPosition: root.position.toArray(),
      headTilt: head.quaternion.toArray(), authoredClips: animations.map(a => a.name),
    } })
  })
  return <group ref={outer} position={settings.scene === 'courtyard' ? [-.4, .48, 1] : [0, .1, 0]} scale={settings.scene === 'courtyard' ? 1.18 : 1.35}>
    <group ref={follow} rotation={[0, .30, 0]} onClick={e => { e.stopPropagation(); onInteract('mascot') }}
      onPointerOver={() => { document.body.style.cursor = 'pointer' }} onPointerOut={() => { document.body.style.cursor = '' }}>
      <primitive object={scene} />
    </group>
  </group>
}
