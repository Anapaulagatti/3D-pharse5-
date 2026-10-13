import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import validator from 'gltf-validator'

const [input, output] = process.argv.slice(2)
if (!input) {
  console.error('Usage: npm run validate -- path/to/model.glb [report.json]')
  process.exit(2)
}
const bytes = await readFile(resolve(input))
const report = await validator.validateBytes(new Uint8Array(bytes), {
  uri: input,
  externalResourceFunction: async (uri) => {
    const path = resolve(dirname(resolve(input)), decodeURIComponent(uri))
    return new Uint8Array(await readFile(path))
  },
})
if (output) {
  await mkdir(dirname(resolve(output)), { recursive: true })
  await writeFile(resolve(output), JSON.stringify(report, null, 2) + '\n')
}
console.log(JSON.stringify({
  file: input,
  bytes: bytes.byteLength,
  errors: report.issues.numErrors,
  warnings: report.issues.numWarnings,
  infos: report.issues.numInfos,
}, null, 2))
if (report.issues.numErrors) process.exitCode = 1
