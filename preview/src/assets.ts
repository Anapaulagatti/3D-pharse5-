import exported from '../../exports/v1/asset-manifest.json'
import polish from '../../exports/v0.3/asset-manifest.json'

export interface StudioAsset {
  id: string
  type: string
  file: string
  version: string
  file_bytes: number
  checksum_sha256: string
  license: string
  animations?: string[]
  animation_details?: { name: string; duration_seconds: number; channels: number }[]
  geometry?: { totalTriangleCount: number; drawCallCount: number; materialCount: number }
}
export const assets = [...exported.assets, ...polish.assets.map(a => ({ ...a, file: 'v0.3/' + a.file }))] as StudioAsset[]
export const modelAssets = assets.filter(asset => asset.type === 'glb' && asset.id !== 'hanok-polish')
export const assetURL = (id: string) => '/' + assets.find(a => a.id === id)!.file
export const formatBytes = (n: number) => n < 1024 * 1024 ? `${(n / 1024).toFixed(0)} KiB` : `${(n / 1024 / 1024).toFixed(2)} MiB`
