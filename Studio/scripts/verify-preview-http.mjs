// Inspect the real rendered app at HTTP endpoints, including the deployable HTML.
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const requirePreview = createRequire(resolve(root, 'preview/package.json'))
const { chromium, expect } = requirePreview('@playwright/test')
const manifest = JSON.parse(await readFile(resolve(root, 'exports/v1/asset-manifest.json'), 'utf8'))
const targets = process.argv.slice(2).map(arg => {
  const separator = arg.indexOf('=')
  const label = arg.slice(0, separator)
  const url = arg.slice(separator + 1)
  if (separator < 1 || !/^[a-z0-9-]+$/.test(label) || !/^https?:\/\//.test(url)) throw new Error('Use label=http(s)://address/ arguments')
  return { label, url }
})
assert.ok(targets.length, 'Provide at least one real HTTP endpoint')
const reports = resolve(process.env.STUDIO_HTTP_REPORT_DIR || resolve(root, 'quality-reports/preview-access'))
const targetScope = process.env.STUDIO_HTTP_TARGET_SCOPE === 'public' ? 'public' : 'internal'
await mkdir(reports, { recursive: true })
const hash = buffer => createHash('sha256').update(buffer).digest('hex')
const timeout = 30_000
const captureStyle = '.stage-note, .model-loading-overlay { visibility: hidden !important; }'
const browser = await chromium.launch({
  executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || '/usr/bin/chromium',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
})
const results = []
try {
  for (const { label, url } of targets) {
    const context = await browser.newContext({ viewport: { width: 1280, height: 1000 }, reducedMotion: 'reduce', acceptDownloads: true })
    const page = await context.newPage()
    const pageErrors = [], consoleErrors = [], failedRequests = [], missingResources = [], httpResources = [], checks = []
    page.on('pageerror', error => pageErrors.push(error.message))
    page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()) })
    page.on('requestfailed', request => failedRequests.push(request.url()))
    page.on('response', response => {
      if (response.status() >= 400) missingResources.push({ url: response.url(), status: response.status() })
      if (response.url().startsWith('http')) httpResources.push({ path: new URL(response.url()).pathname, status: response.status() })
    })
    const loadStarted = Date.now()
    const response = await page.goto(url)
    assert.equal(response.status(), 200)
    assert.match(response.headers()['content-type'], /^text\/html/)
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
    const readyMilliseconds = Date.now() - loadStarted
    await expect(page.getByRole('heading', { name: 'Hanok Rooftop', exact: true })).toBeVisible()
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.textures), { timeout }).toBeGreaterThanOrEqual(3)
    assert.equal(await page.evaluate(() => document.doctype?.name), 'html')
    await page.screenshot({ path: resolve(reports, `${label}-desktop.png`), fullPage: true })
    const canvas = page.locator('canvas')
    const initial = await canvas.screenshot({ path: resolve(reports, `${label}-day.png`), style: captureStyle })
    checks.push('HTTP 200 text/html; Hanok Arena and actual mascot rendered with uploaded textures')

    // Exercise the actual canvas pointer controls, rather than checking only buttons.
    const box = await canvas.boundingBox()
    await page.mouse.move(box.x + box.width * .35, box.y + box.height * .45)
    await page.mouse.down()
    await page.mouse.move(box.x + box.width * .65, box.y + box.height * .5, { steps: 12 })
    await page.mouse.up()
    await expect.poll(async () => hash(await canvas.screenshot({ style: captureStyle })), { timeout }).not.toBe(hash(initial))
    await canvas.screenshot({ path: resolve(reports, `${label}-camera-drag.png`), style: captureStyle })
    await page.getByRole('button', { name: /Đặt lại góc nhìn/ }).click()
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
    await page.getByRole('button', { name: 'Mái hanok', exact: true }).click()
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.focus), { timeout }).toBe('roof')
    await page.getByRole('button', { name: 'Tổng quan', exact: true }).click()
    checks.push('Canvas drag visibly changes camera; reset and roof POI work')

    await page.getByLabel('Ánh sáng').selectOption('night')
    await expect.poll(async () => hash(await canvas.screenshot({ style: captureStyle })), { timeout }).not.toBe(hash(initial))
    await canvas.screenshot({ path: resolve(reports, `${label}-night.png`), style: captureStyle })
    await page.getByLabel('Ánh sáng').selectOption('day')
    checks.push('Day/night control changes the actual rendered scene')
    for (const [index, id] of ['arena-hero', 'mascot-base'].entries()) {
      const event = page.waitForEvent('download')
      await page.locator('.asset-cards a').nth(index).click()
      const download = await event
      assert.equal(download.suggestedFilename(), `${id}.glb`)
      assert.equal(await download.failure(), null)
      const bytes = await readFile(await download.path())
      const asset = manifest.assets.find(asset => asset.id === id)
      assert.equal(bytes.length, asset.file_bytes)
      assert.equal(hash(bytes), asset.checksum_sha256)
    }
    checks.push('Both real GLBs and embedded textures available; download bytes match approved exports')

    await page.getByRole('button', { name: /Linh vật gốm/ }).click()
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
    const poses = new Set()
    for (const clip of ['Idle', 'Happy', 'Thinking', 'Celebration', 'Disappointed', 'Greeting']) {
      await page.getByLabel('Trạng thái linh vật').selectOption(clip)
      await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.activeClip), { timeout }).toBe(clip)
      await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime), { timeout }).toBeCloseTo(.8, 3)
      poses.add(hash(await canvas.screenshot({ path: resolve(reports, `${label}-mascot-${clip.toLowerCase()}.png`), style: captureStyle })))
    }
    assert.equal(poses.size, 6)
    await page.getByLabel('Giảm chuyển động').uncheck()
    const animated = await page.evaluate(() => window.__STUDIO_METRICS__.clipTime)
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime), { timeout }).not.toBe(animated)
    await page.getByLabel('Giảm chuyển động').check()
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime), { timeout }).toBeCloseTo(.8, 3)
    await page.waitForTimeout(500)
    assert.ok(Math.abs((await page.evaluate(() => window.__STUDIO_METRICS__.clipTime)) - .8) < .001)
    checks.push('Six distinct real poses; animation advances; reduced motion stops playback at frozen pose')
    await page.setViewportSize({ width: 390, height: 844 })
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready', { timeout })
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true)
    await page.screenshot({ path: resolve(reports, `${label}-mobile.png`), fullPage: true })
    checks.push('390×844 layout renders without horizontal overflow')
    await writeFile(resolve(reports, `${label}-diagnostics.json`), JSON.stringify({ readyMilliseconds, checks, pageErrors, consoleErrors, failedRequests, missingResources, httpResources }, null, 2) + '\n')
    assert.deepEqual(pageErrors, [])
    assert.deepEqual(consoleErrors, [])
    assert.deepEqual(failedRequests, [])
    assert.deepEqual(missingResources, [])
    await context.close()

    const fallbackContext = await browser.newContext({ viewport: { width: 1280, height: 1000 } })
    const fallback = await fallbackContext.newPage()
    await fallback.addInitScript(() => {
      const original = HTMLCanvasElement.prototype.getContext
      HTMLCanvasElement.prototype.getContext = function (type, ...args) {
        return type.startsWith('webgl') ? null : original.call(this, type, ...args)
      }
    })
    await fallback.goto(url)
    await expect(fallback.locator('.stage')).toHaveAttribute('data-engine', 'fallback', { timeout })
    const poster = fallback.getByRole('img', { name: 'Minh họa tĩnh sân hanok và linh vật men ngọc' })
    await expect.poll(() => poster.evaluate(image => image.naturalWidth), { timeout }).toBe(844)
    await fallback.screenshot({ path: resolve(reports, `${label}-fallback.png`), fullPage: true })
    await fallback.getByRole('button', { name: /Linh vật gốm/ }).click()
    const portrait = fallback.getByRole('img', { name: 'Chân dung linh vật gốm — chế độ 2D' })
    await expect.poll(() => portrait.evaluate(image => image.naturalWidth), { timeout }).toBe(800)
    await fallback.setViewportSize({ width: 390, height: 844 })
    await expect(fallback.locator('.stage')).toHaveAttribute('data-engine', 'fallback')
    assert.equal(await fallback.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true)
    await fallback.screenshot({ path: resolve(reports, `${label}-mobile-fallback.png`), fullPage: true })
    await fallbackContext.close()
    checks.push('Missing WebGL shows actual arena/mascot PNG fallback; controls work at desktop and 390x844 without overflow')
    results.push({ label, url, status: 'PASS', readyMilliseconds, checks, httpResources, pageErrors, consoleErrors, failedRequests, missingResources })
    console.log(`${label}: ${checks.length} rendered HTTP checks PASS`)
  }
  await writeFile(resolve(reports, 'http-verification.json'), JSON.stringify({
    status: 'PASS', verified_at: new Date().toISOString(), browser: browser.version(),
    renderer: 'Cloud SwiftShader software GPU; physical-device FPS not verified',
    target_scope: targetScope,
    public_deployment: targetScope === 'public' ? 'Public URL response and rendered behavior verified at the listed endpoint' : 'No public deployment claim; these are internal validation endpoints',
    results,
  }, null, 2) + '\n')
} finally {
  await browser.close()
}
