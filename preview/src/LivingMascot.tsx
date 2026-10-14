import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useAnimations } from '@react-three/drei'
import { AnimationClip, Euler, Group, LoopOnce, LoopRepeat, MathUtils, Quaternion, Vector3, VectorKeyframeTrack } from 'three'
import type { AnimationAction } from 'three'
import type { Interaction, Mood, SceneSettings } from './types'
import { useStudioModel } from './useStudioModel'

// Clone and accent the exported samples; original GLB/source/clip bytes stay intact.
function expressiveClip(source: AnimationClip) {
  const clip = source.clone()
  const q = new Quaternion(), e = new Euler()
  for (const track of clip.tracks) {
    if (track.name.includes('MascotRoot.position')) {
      for (let i = 1; i < track.values.length; i += 3) track.values[i] *= 1.55
    } else if (track.name.endsWith('.scale') && track.name.includes('MascotRoot')) {
      for (let i = 0; i < track.values.length; i++) track.values[i] = 1 + (track.values[i] - 1) * 1.65
    } else if (track.name.endsWith('.quaternion') && /Arm|HeadPivot/.test(track.name)) {
      for (let i = 0; i < track.values.length; i += 4) {
        q.fromArray(track.values, i); e.setFromQuaternion(q)
        const arm = track.name.includes('Arm')
        const gain = arm ? source.name === 'Greeting' || source.name === 'Celebration' ? 2.1 : 1.55 : 1.25
        // Original greeting/cheer rotated the mittens into the torso. Open the silhouette.
        const outward = arm && ['Greeting', 'Celebration', 'Happy'].includes(source.name) ? -1 : 1
        e.set(e.x * gain, e.y * gain, e.z * gain * outward); q.setFromEuler(e).toArray(track.values, i)
      }
    }
  }
  if (source.name === 'Thinking') {
    const times = Array.from(clip.tracks[0].times)
    const values = times.flatMap(t => {
      const weight = Math.sin(Math.PI * t / clip.duration) ** 2
      // Bring the mitten in front of the ceramic body, just beneath the chin.
      return [.375 - .05 * weight, .77 + .26 * weight, .36 * weight]
    })
    clip.tracks.push(new VectorKeyframeTrack('ArmRightPivot.position', times, values))
  }
  return clip
}

export default function LivingMascot({ settings, animate, onReady, onInteract }: {
  settings: SceneSettings; animate: boolean; onReady: () => void; onInteract: (type: Interaction) => void
}) {
  const invalidate = useThree(s => s.invalidate)
  const { scene, animations } = useStudioModel('mascot-base')
  const clips = useMemo(() => animations.map(expressiveClip), [animations])
  const { actions, mixer } = useAnimations(clips, scene)
  const [mood, setMood] = useState<Mood>(settings.mood)
  const [gestureId, setGestureId] = useState(0)
  const outer = useRef<Group>(null)
  const follow = useRef<Group>(null)
  const previous = useRef<AnimationAction | null>(null)
  const intro = useRef(false)
  const temporary = useRef(0)
  const elapsed = useRef(0)
  const idleAge = useRef(0)
  const frames = useRef(0)
  const reported = useRef(false)
  const world = useMemo(() => new Vector3(), [])
  const root = useMemo(() => scene.getObjectByName('MascotRoot')!, [scene])
  const eyes = useMemo(() => ['EyeLeft', 'EyeRight'].map(n => scene.getObjectByName(n)!), [scene])
  const catchlights = useMemo(() => ['EyeCatchlight', 'EyeCatchlight001'].map(n => scene.getObjectByName(n)).filter(Boolean), [scene])
  const head = useMemo(() => scene.getObjectByName('HeadPivot')!, [scene])
  const mouth = useMemo(() => scene.getObjectByName('Smile')!, [scene])
  const leaf = useMemo(() => scene.getObjectByName('CeramicLeafPivot')!, [scene])
  const gesture = useCallback((next: Mood) => { temporary.current = 1; idleAge.current = 0; setMood(next); setGestureId(n => n + 1); invalidate() }, [invalidate])

  useEffect(() => { temporary.current = 0; idleAge.current = 0; setMood(settings.mood) }, [settings.mood])
  useEffect(() => {
    if (animate && !intro.current && settings.mood === 'Idle') { intro.current = true; gesture('Greeting') }
  }, [animate, settings.mood, gesture])
  useEffect(() => {
    if (settings.interaction.type === 'mascot' && settings.interaction.id) {
      intro.current = true
      gesture(settings.interaction.id % 2 ? 'Greeting' : 'Celebration')
    }
  }, [settings.interaction, gesture])
  useEffect(() => {
    const action = actions[mood]
    if (!action) throw new Error('Missing original mascot clip: ' + mood)
    if (previous.current && previous.current !== action) {
      if (animate) previous.current.fadeOut(.24); else previous.current.stop()
    }
    action.reset().setEffectiveWeight(1).setEffectiveTimeScale(.8)
      .setLoop(temporary.current ? LoopOnce : LoopRepeat, temporary.current ? 1 : Infinity)
      .fadeIn(animate ? .24 : 0).play()
    action.clampWhenFinished = !!temporary.current
    previous.current = action
    if (!animate) { action.paused = true; action.time = .8; mixer.update(0) }
    invalidate()
  }, [actions, mood, gestureId, mixer, invalidate])
  useEffect(() => {
    const finished = (event: { action: AnimationAction }) => {
      if (temporary.current && event.action === previous.current) { temporary.current = 0; idleAge.current = 0; setMood('Idle') }
    }
    mixer.addEventListener('finished', finished)
    return () => mixer.removeEventListener('finished', finished)
  }, [mixer])
  useEffect(() => {
    mixer.timeScale = animate ? 1 : 0
    if (actions[mood]) {
      actions[mood]!.paused = !animate
      if (settings.reducedMotion || (settings.paused && actions[mood]!.time === 0)) actions[mood]!.time = .8
    }
    mixer.update(0); invalidate()
  }, [actions, mood, animate, settings.reducedMotion, settings.paused, mixer, invalidate])
  useEffect(() => () => { mixer.stopAllAction() }, [mixer])

  useFrame(({ gl, camera }, delta) => {
    frames.current++
    const smiling = mood === 'Happy' || mood === 'Celebration'
    mouth.scale.y = mood === 'Disappointed' ? -1 : smiling ? 1.4 : 1
    mouth.position.y = mood === 'Disappointed' ? .27 : smiling ? -.052 : 0
    if (!animate) {
      for (const eye of eyes) {
        if (mood === 'Disappointed') eye.scale.y = .72
        else if (!smiling) eye.scale.y = 1
      }
      for (const light of catchlights) if (light) light.visible = true
    }
    if (animate) {
      const dt = Math.min(delta, .15)
      elapsed.current += dt
      if (!temporary.current && mood === 'Idle') {
        idleAge.current += dt
        if (idleAge.current > 11) gesture('Thinking')
      }
      if (outer.current && follow.current) {
        outer.current.getWorldPosition(world)
        const yaw = Math.atan2(camera.position.x - world.x, camera.position.z - world.z)
        follow.current.rotation.y = MathUtils.damp(follow.current.rotation.y, yaw, 2.3, dt)
      }
      const t = elapsed.current
      const blinkPhase = t % 4.6
      const blink = blinkPhase > 4.35 ? 1 - .9 * Math.sin((blinkPhase - 4.35) / .25 * Math.PI) : 1
      for (const eye of eyes) eye.scale.y = (mood === 'Happy' || mood === 'Celebration' ? .58 : mood === 'Disappointed' ? .68 : 1) * blink
      for (const light of catchlights) if (light) light.visible = blink > .45
      if (follow.current) {
        follow.current.position.y = mood === 'Idle' ? .027 * Math.sin(t * 1.7) : 0
        follow.current.rotation.z = mood === 'Idle' ? .025 * Math.sin(t * 1.1) : 0
      }
      leaf.rotation.z = .055 * Math.sin(t * 2.2 + .4)
      if (mood === 'Thinking') head.rotation.z += .015 * Math.sin(t * 1.4)
    }
    if (frames.current < 2) invalidate()
    if (!reported.current && frames.current >= 2) { reported.current = true; onReady() }
    queueMicrotask(() => { window.__STUDIO_METRICS__ = {
      ...window.__STUDIO_METRICS__, frames: frames.current, activeClip: mood, clipTime: actions[mood]?.time || 0,
      mascotY: root.position.y + (follow.current?.position.y || 0), drawCalls: gl.info.render.calls,
      triangles: gl.info.render.triangles, textures: gl.info.memory.textures, geometries: gl.info.memory.geometries,
      assetsLoaded: true, reducedMotion: settings.reducedMotion, paused: settings.paused, focus: settings.focus,
      quality: settings.quality, canvasWidth: gl.domElement.width, canvasHeight: gl.domElement.height,
      motionActive: animate, cinematic: settings.cinematic, facialBlink: eyes[0].scale.y,
    } })
  })
  return <group ref={outer} position={settings.scene === 'courtyard' ? [-.4, .48, 1] : [0, .1, 0]} scale={settings.scene === 'courtyard' ? .97 : 1.35}>
    <group ref={follow} rotation={[0, .30, 0]} onClick={e => { e.stopPropagation(); onInteract('mascot') }}
      onPointerOver={() => { document.body.style.cursor = 'pointer' }} onPointerOut={() => { document.body.style.cursor = '' }}>
      <primitive object={scene} />
    </group>
  </group>
}
