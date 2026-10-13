export type SceneKind = 'courtyard' | 'mascot'
export type Quality = 'low' | 'medium' | 'high'
export type Mood = 'Idle' | 'Happy' | 'Thinking' | 'Celebration' | 'Disappointed' | 'Greeting'
export type Lighting = 'day' | 'evening' | 'night'
export type Focus = 'overview' | 'dais' | 'roof' | 'garden'
export interface SceneSettings {
  scene: SceneKind
  quality: Quality
  mood: Mood
  lighting: Lighting
  reducedMotion: boolean
  paused: boolean
  mobile: boolean
  focus: Focus
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
}
declare global { interface Window { __STUDIO_METRICS__?: StudioMetrics } }
