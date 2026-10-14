export type View = 'hero' | 'architecture' | 'play' | 'portrait' | 'animation'
export type Light = 'day' | 'evening' | 'night'
export type Quality = 'low' | 'medium' | 'high'
export type Preset = 'hero' | 'front' | 'rear' | 'left' | 'right' | 'roof' | 'connection' | 'interior' | 'face'
export interface Settings { effects: 'off' | 'reduced' | 'full'; view: View; lighting: Light; quality: Quality; reduced: boolean; paused: boolean; preset: Preset; door: boolean; angle: number | null; clip: string; expression: string; active: boolean; gesture: {name:string;id:number}; reset: number }
export interface ReforgeMetrics { projection?: number[]; viewMatrix?: number[]; lighting?: string; lightColor?: string; environmentTime?: number; environmentClips?: string[]; lanternGlow?: number; worldInteraction?: number; effects?: string; ready?: boolean; draws?: number; triangles?: number; camera?: number[]; target?: number[]; door?: number; stage?: string; clip?: string; clipTime?: number; clips?: string[]; morphs?: Record<string,number>; feet?: number[][]; skinBones?: number; motion?: boolean; player?: number[]; yaw?: number; speed?: number; grounded?: boolean; verticalVelocity?: number; blocked?: number; distance?: number; physicsSteps?: number; reduced?: boolean; events?: {clip:string;at:number;position:number[]}[] }
declare global { interface Window { __REFORGE_METRICS__?: ReforgeMetrics } }
