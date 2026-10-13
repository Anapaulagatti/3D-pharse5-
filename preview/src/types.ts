export type SceneKind = 'courtyard' | 'mascot'
export type Quality = 'low' | 'medium' | 'high'
export type Mood = 'idle' | 'ready' | 'celebrate'
export type Lighting = 'day' | 'evening'
export interface SceneSettings {
  scene: SceneKind
  quality: Quality
  mood: Mood
  lighting: Lighting
  reducedMotion: boolean
  paused: boolean
  mobile: boolean
}
