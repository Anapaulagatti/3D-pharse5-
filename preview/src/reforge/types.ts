export type View = 'hero' | 'architecture' | 'play' | 'portrait' | 'animation'
export type Light = 'day' | 'evening' | 'night'
export type Quality = 'low' | 'medium' | 'high'
export type Preset = 'hero' | 'front' | 'rear' | 'left' | 'right' | 'roof' | 'connection' | 'interior'
export interface Settings { view: View; lighting: Light; quality: Quality; reduced: boolean; paused: boolean; preset: Preset; door: boolean; angle: number | null; clip: string; expression: string }
export interface ReforgeMetrics { ready?: boolean; draws?: number; triangles?: number; camera?: number[]; target?: number[]; door?: number; stage?: string; clip?: string; clipTime?: number; clips?: string[]; morphs?: Record<string,number>; feet?: number[][]; skinBones?: number; motion?: boolean }
declare global { interface Window { __REFORGE_METRICS__?: ReforgeMetrics } }
