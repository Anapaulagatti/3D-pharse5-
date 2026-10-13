// Package the existing React/R3F app and verified exports into one offline HTML file.
// Reuses preview's pinned Vite/plugin-react; never generates models or installs packages.
import { createHash } from 'node:crypto'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const preview = resolve(root, 'preview')
const requirePreview = createRequire(resolve(preview, 'package.json'))
const { build } = await import(pathToFileURL(requirePreview.resolve('vite')).href)
const { default: react } = await import(pathToFileURL(requirePreview.resolve('@vitejs/plugin-react')).href)
const exportDir = resolve(root, 'exports/v1')
const manifest = JSON.parse(await readFile(resolve(exportDir, 'asset-manifest.json'), 'utf8'))
const embedded = {}
for (const asset of manifest.assets) {
  const path = resolve(exportDir, asset.file)
  if (!path.startsWith(exportDir + '/')) throw new Error(`Invalid asset path: ${asset.id}`)
  const bytes = await readFile(path)
  if (bytes.length !== asset.file_bytes || createHash('sha256').update(bytes).digest('hex') !== asset.checksum_sha256) {
    throw new Error(`Unverified asset: ${asset.id}; repack changed assets before bundling`)
  }
  embedded[asset.id] = { mime: asset.type === 'glb' ? 'model/gltf-binary' : 'image/png', base64: bytes.toString('base64') }
}

// Blob URLs work with GLTFLoader, embedded images and model downloads under file://.
// Only this build replaces assetURL; the served preview keeps normal HTTP asset paths.
const assetModule = resolve(preview, 'src/assets.ts')
let replaced = false
const result = await build({
  root: preview,
  configFile: false,
  publicDir: false,
  define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  plugins: [react(), {
    name: 'studio-embedded-assets',
    enforce: 'pre',
    transform(code, id) {
      if (id !== assetModule) return null
      const target = "export const assetURL = (id: string) => '/' + assets.find(a => a.id === id)!.file"
      if (!code.includes(target)) throw new Error('assets.ts changed: update the offline asset adapter')
      replaced = true
      return code.replace(target, `
const embedded: Record<string, { mime: string; base64: string }> = ${JSON.stringify(embedded)}
const urls = new Map<string, string>()
export const assetURL = (id: string) => {
  if (!urls.has(id)) {
    const asset = embedded[id]
    if (!asset) throw new Error('Unknown embedded asset: ' + id)
    const bytes = Uint8Array.from(atob(asset.base64), char => char.charCodeAt(0))
    urls.set(id, URL.createObjectURL(new Blob([bytes], { type: asset.mime })))
  }
  return urls.get(id)!
}`)
    },
  }],
  build: {
    write: false,
    copyPublicDir: false,
    cssCodeSplit: false,
    minify: 'oxc',
    sourcemap: false,
    license: true,
    lib: { entry: resolve(preview, 'src/main.tsx'), name: 'StudioShowcase', formats: ['iife'] },
    rolldownOptions: { output: { codeSplitting: false } },
  },
})
if (!replaced) throw new Error('Offline asset adapter was not applied')
const output = (Array.isArray(result) ? result : [result]).flatMap(r => r.output)
const chunks = output.filter(file => file.type === 'chunk')
// Rolldown records an inlined lazy import as a reference to the same IIFE chunk.
// Reject external chunks; direct-file offline QA additionally verifies no requests.
if (chunks.length !== 1 || chunks[0].imports.length || chunks[0].dynamicImports.some(file => file !== chunks[0].fileName)) {
  throw new Error('Showcase must contain exactly one self-contained JavaScript bundle: ' + JSON.stringify(chunks.map(({ fileName, imports, dynamicImports }) => ({ fileName, imports, dynamicImports }))))
}
const css = output.filter(file => file.type === 'asset' && file.fileName.endsWith('.css')).map(file => String(file.source)).join('\n')
const license = output.find(file => file.type === 'asset' && file.fileName.endsWith('license.md'))
if (!css || !license) throw new Error('Missing bundled styles or dependency license notices')
const safeScript = text => text.replace(/<\/script/gi, '<\\/script')
const html = `<!doctype html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#15243a" />
  <meta name="description" content="Showcase 3D Hanok và Ceramic Seed Spirit — bản offline tự chứa, model và animation thật từ Blender." />
  <title>Living Hangeul District · 3D Studio</title>
  <style>${css.replace(/<\/style/gi, '<\\/style')}</style>
</head>
<body>
  <div id="root"></div>
  <noscript>Bật JavaScript để xem showcase 3D.</noscript>
  <script>${safeScript(chunks[0].code)}</script>
  <script type="text/plain" id="studio-dependency-licenses">${safeScript(String(license.source))}</script>
</body>
</html>
`
const dir = resolve(root, 'showcase')
await mkdir(dir, { recursive: true })
await writeFile(resolve(dir, 'index.html'), html)
const info = {
  format: 'single-file-offline-html',
  app_source: 'preview/src/main.tsx',
  asset_manifest: 'exports/v1/asset-manifest.json',
  asset_version: manifest.version,
  file: 'showcase/index.html',
  file_bytes: Buffer.byteLength(html),
  checksum_sha256: createHash('sha256').update(html).digest('hex'),
  embedded_assets: manifest.assets.map(({ id, file_bytes, checksum_sha256 }) => ({ id, file_bytes, checksum_sha256 })),
  generated_at: new Date().toISOString(),
}
await writeFile(resolve(dir, 'build-info.json'), JSON.stringify(info, null, 2) + '\n')
console.log(`Saved ${info.file}: ${(info.file_bytes / 1024 / 1024).toFixed(2)} MiB; ${info.embedded_assets.length} verified assets; no server/CDN required`)
