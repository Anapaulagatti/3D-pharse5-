// Verify the actual portable artifact with network disabled, no server.
// Report a managed-browser file:// block separately from functional offline checks.
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const requirePreview = createRequire(resolve(root, 'preview/package.json'))
const { chromium, expect } = requirePreview('@playwright/test')
const info = JSON.parse(await readFile(resolve(root, 'showcase/build-info.json'), 'utf8'))
const html = await readFile(resolve(root, info.file))
assert.equal(html.length, info.file_bytes)
assert.equal(createHash('sha256').update(html).digest('hex'), info.checksum_sha256)
const fileURL = pathToFileURL(resolve(root, info.file)).href
const reports = resolve(root, 'quality-reports')
await mkdir(reports, { recursive: true })
const browser = await chromium.launch({
  executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || '/usr/bin/chromium',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
})
const checks = []
const externalRequests = []
const pageErrors = []
let directFile = 'verified'
const timeout = 30_000
async function open(viewport, noWebGL = false) {
  const context = await browser.newContext({ viewport, reducedMotion: 'reduce', offline: true, acceptDownloads: true })
  let page = await context.newPage()
  const watch = page => {
    page.on('pageerror', error => pageErrors.push(error.message))
    page.on('request', request => {
      if (/^https?:/.test(request.url()) || (request.url().startsWith('file:') && request.url() !== fileURL)) {
        externalRequests.push(request.url())
      }
    })
  }
  watch(page)
  const disableWebGL = () => {
    const original = HTMLCanvasElement.prototype.getContext
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      return type.startsWith('webgl') || type === 'experimental-webgl' ? null : original.call(this, type, ...args)
    }
  }
  if (noWebGL) await page.addInitScript(disableWebGL)
  if (directFile === 'blocked-by-cloud-browser-policy') {
    if (noWebGL) await page.evaluate(disableWebGL)
    await page.setContent(html.toString('utf8'), { waitUntil: 'load' })
  } else {
    try {
      await page.goto(fileURL)
    } catch (error) {
      if (!String(error).includes('net::ERR_BLOCKED_BY_ADMINISTRATOR')) throw error
      directFile = 'blocked-by-cloud-browser-policy'
      // Render the same bytes in an allowed, isolated about:blank page. Never
      // modify/bypass browser policies; this does not count as a file:// pass.
      await page.close()
      page = await context.newPage()
      watch(page)
      if (noWebGL) await page.evaluate(disableWebGL)
      await page.setContent(html.toString('utf8'), { waitUntil: 'load' })
    }
  }
  return { context, page }
}
try {
  const desktop = await open({ width: 1280, height: 1000 })
  const { page } = desktop
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.assetsLoaded), { timeout }).toBe(true)
  await page.screenshot({ path: resolve(reports, 'showcase-desktop.png'), fullPage: true })
  checks.push('Desktop: portable HTML loads real 3D and inline styles with network offline')
  for (const [index, id] of ['arena-hero', 'mascot-base'].entries()) {
    const event = page.waitForEvent('download')
    await page.locator('.asset-cards a').nth(index).click()
    const download = await event
    assert.equal(download.suggestedFilename(), `${id}.glb`)
    assert.equal(await download.failure(), null)
    const bytes = await readFile(await download.path())
    const asset = info.embedded_assets.find(asset => asset.id === id)
    assert.equal(bytes.length, asset.file_bytes)
    assert.equal(createHash('sha256').update(bytes).digest('hex'), asset.checksum_sha256)
  }
  checks.push('Both offline GLB downloads match verified export bytes and filenames')
  await page.getByRole('button', { name: 'Mái hanok', exact: true }).click()
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.focus), { timeout }).toBe('roof')
  await page.getByLabel('Ánh sáng').selectOption('night')
  await page.getByLabel('Chất lượng').selectOption('low')
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.quality), { timeout }).toBe('low')
  await page.getByRole('button', { name: /Linh vật gốm/ }).click()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
  for (const clip of ['Idle', 'Happy', 'Thinking', 'Celebration', 'Disappointed', 'Greeting']) {
    await page.getByLabel('Trạng thái linh vật').selectOption(clip)
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.activeClip), { timeout }).toBe(clip)
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime), { timeout }).toBeCloseTo(.8, 3)
  }
  await page.screenshot({ path: resolve(reports, 'showcase-mascot.png'), fullPage: true })
  await page.getByLabel('Giảm chuyển động').uncheck()
  const time = await page.evaluate(() => window.__STUDIO_METRICS__.clipTime)
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime), { timeout }).not.toBe(time)
  await page.getByRole('button', { name: 'Tạm dừng' }).click()
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.paused), { timeout }).toBe(true)
  const paused = await page.evaluate(() => window.__STUDIO_METRICS__.clipTime)
  await page.waitForTimeout(500)
  assert.equal(await page.evaluate(() => window.__STUDIO_METRICS__.clipTime), paused)
  checks.push('POI, lighting, quality, six real clips, live playback and pause work offline')
  await desktop.context.close()

  const phone = await open({ width: 390, height: 844 })
  await expect(phone.page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
  assert.equal(await phone.page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true)
  await phone.page.screenshot({ path: resolve(reports, 'showcase-mobile.png'), fullPage: true })
  checks.push('390×844 viewport: real 3D, no horizontal overflow')
  await phone.context.close()

  const fallback = await open({ width: 1280, height: 1000 }, true)
  await expect(fallback.page.locator('.stage')).toHaveAttribute('data-engine', 'fallback', { timeout })
  const poster = fallback.page.getByRole('img', { name: 'Minh họa tĩnh sân hanok và linh vật men ngọc' })
  await expect.poll(() => poster.evaluate(image => image.naturalWidth), { timeout }).toBe(844)
  await fallback.page.screenshot({ path: resolve(reports, 'showcase-fallback.png'), fullPage: true })
  await fallback.page.getByRole('button', { name: /Linh vật gốm/ }).click()
  const portrait = fallback.page.getByRole('img', { name: 'Chân dung linh vật gốm — chế độ 2D' })
  await expect.poll(() => portrait.evaluate(image => image.naturalWidth), { timeout }).toBe(800)
  checks.push('No WebGL: both actual embedded PNG fallbacks load offline')
  await fallback.context.close()
  assert.deepEqual(externalRequests, [])
  assert.deepEqual(pageErrors, [])
  checks.push('Zero external network/file requests and zero JavaScript errors')
  await writeFile(resolve(reports, 'showcase-offline.json'), JSON.stringify({
    status: 'PASS', verified_at: new Date().toISOString(), browser: browser.version(),
    renderer: 'Cloud SwiftShader software GPU; physical-device FPS not measured',
    file: info.file, checksum_sha256: info.checksum_sha256,
    direct_file: directFile,
    mode: directFile === 'verified' ? 'file:// with network offline; no web server' : 'Same HTML bytes in about:blank with network offline; file:// blocked by cloud browser policy',
    checks, externalRequests, pageErrors,
  }, null, 2) + '\n')
  console.log(`PASS: ${checks.length} portable-showcase checks; offline rendering and downloads verified; file:// ${directFile}`)
} finally {
  await browser.close()
}
