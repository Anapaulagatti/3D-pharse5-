import exported from '../../exports/v1/asset-manifest.json'

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
export const assets = exported.assets as StudioAsset[]
export const modelAssets = assets.filter(asset => asset.type === 'glb')
export const assetURL = (id: string) => '/' + assets.find(a => a.id === id)!.file
export const formatBytes = (n: number) => n < 1024 * 1024 ? `${(n / 1024).toFixed(0)} KB` : `${(n / 1024 / 1024).toFixed(2)} MB`
