import { spawnSync } from 'node:child_process'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { mkdirSync } from 'node:fs'

const studio = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const smoke = resolve(studio, '.cache/smoke')
mkdirSync(smoke, { recursive: true })
function run(executable, args, cwd = studio) {
  const result = spawnSync(executable, args, { cwd, stdio: 'inherit' })
  if (result.error) throw result.error
  if (result.status !== 0) process.exit(result.status || 1)
}
const bin = (name) => resolve(studio, 'node_modules/.bin', name + (process.platform === 'win32' ? '.cmd' : ''))
run(process.env.BLENDER_BIN || 'blender', ['--background', '--factory-startup', '--python', resolve(studio, 'scripts/create-smoke-fixture.py')])
run(process.execPath, ['scripts/validate-glb.mjs', '.cache/smoke/toolchain-fixture.glb', '.cache/smoke/validation.json'])
run(bin('gltf-transform'), ['inspect', '.cache/smoke/toolchain-fixture.glb'])
// Conservative optimization: preserve geometry and node names, add no decoder requirements.
run(bin('gltf-transform'), ['optimize', '.cache/smoke/toolchain-fixture.glb', '.cache/smoke/toolchain-fixture.optimized.glb',
  '--compress', 'false', '--texture-compress', 'false', '--simplify', 'false',
  '--flatten', 'false', '--join', 'false', '--instance', 'false', '--palette', 'false'])
run(process.execPath, ['scripts/validate-glb.mjs', '.cache/smoke/toolchain-fixture.optimized.glb', '.cache/smoke/validation-optimized.json'])
run(bin('gltfjsx'), ['toolchain-fixture.optimized.glb', '--types', '--output', 'ToolchainFixture.tsx'], smoke)
console.log('Blender → GLB → Khronos Validator → glTF Transform → gltfjsx: PASS')
