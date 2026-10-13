export type SceneKind = 'courtyard' | 'mascot'
export type Quality = 'low' | 'medium' | 'high'
export type Mood = 'Idle' | 'Happy' | 'Thinking' | 'Celebration' | 'Disappointed' | 'Greeting'
export type Lighting = 'day' | 'evening' | 'night'
export type Focus = 'overview' | 'dais' | 'roof' | 'garden'
export type Interaction = 'mascot' | 'lantern' | 'tree'
export interface SceneSettings {
  scene: SceneKind
  quality: Quality
  mood: Mood
  lighting: Lighting
  reducedMotion: boolean
  paused: boolean
  mobile: boolean
  focus: Focus
  cinematic: boolean
  interaction: { type: Interaction | null; id: number }
}

export interface StudioMetrics {
  frames: number
  activeClip: Mood
  clipTime: number
  mascotY: number
  drawCalls: number
  triangles: number
  textures: number
  geometries: number
  assetsLoaded: boolean
  reducedMotion: boolean
  paused: boolean
  focus: Focus
  quality: Quality
  canvasWidth: number
  canvasHeight: number
  environmentTime?: number
  lanternIntensity?: number
  cameraZoom?: number
  cameraTarget?: number[]
  cameraPosition?: number[]
  interactivePoints?: Record<Interaction, [number, number]>
  facialBlink?: number
  motionActive?: boolean
  cinematic?: boolean
}
declare global { interface Window { __STUDIO_METRICS__?: StudioMetrics } }
