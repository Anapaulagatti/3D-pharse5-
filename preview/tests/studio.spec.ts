import { test, expect } from '@playwright/test'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { resolve } from 'node:path'

const reports = resolve(process.env.STUDIO_REPORT_DIR || resolve(process.cwd(), '../quality-reports'))
mkdirSync(reports, { recursive: true })
const posters = resolve(process.env.STUDIO_POSTER_DIR || (process.env.STUDIO_REPORT_DIR ? resolve(reports, 'posters') : resolve(process.cwd(), '../assets/posters')))
mkdirSync(posters, { recursive: true })
const captureStyle = '.stage-note, .model-loading-overlay { visibility: hidden !important; }'

test('3D renders and scene, quality, light and motion controls work', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  const modelResponse = page.waitForResponse(r => r.url().endsWith('/models/arena-hero.glb') && r.status() === 200)
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await expect(page.locator('canvas')).toBeVisible()
  const response = await modelResponse
  const manifest = JSON.parse(readFileSync(resolve(process.cwd(), '../exports/v1/asset-manifest.json'), 'utf8'))
  const body = await response.body()
  expect(createHash('sha256').update(body).digest('hex')).toBe(manifest.assets.find((a: { id: string }) => a.id === 'arena-hero').checksum_sha256)
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.assetsLoaded)).toBe(true)
  await page.getByLabel('Giảm chuyển động').check()
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await page.screenshot({ path: resolve(reports, 'preview-desktop.png'), fullPage: true })
  await page.locator('canvas').screenshot({ path: resolve(posters, 'arena-desktop.png'), style: captureStyle })
  writeFileSync(resolve(reports, 'renderer-desktop.json'), JSON.stringify(await page.evaluate(() => window.__STUDIO_METRICS__), null, 2) + '\n')
  await page.getByRole('button', { name: 'Mái hanok', exact: true }).click()
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.focus)).toBe('roof')
  await page.getByRole('button', { name: 'Vườn mận', exact: true }).click()
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.focus)).toBe('garden')
  await page.getByRole('button', { name: /Linh vật gốm/ }).click()
  await expect(page.getByRole('heading', { name: 'Ceramic Spirit' })).toBeVisible()
  await page.getByLabel('Chất lượng').selectOption('low')
  await page.getByLabel('Ánh sáng').selectOption('evening')
  await page.getByLabel('Trạng thái linh vật').selectOption('Celebration')
  await expect(page.getByLabel('Chất lượng')).toHaveValue('low')
  await expect(page.getByLabel('Ánh sáng')).toHaveValue('evening')
  await expect(page.getByLabel('Trạng thái linh vật')).toHaveValue('Celebration')
  await page.getByRole('button', { name: 'Tạm dừng' }).click()
  await expect(page.getByRole('button', { name: 'Tiếp tục' })).toHaveAttribute('aria-pressed', 'true')
  await page.getByRole('button', { name: /Đặt lại góc nhìn/ }).click()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await expect(page.locator('canvas')).toBeVisible()
  for (let i = 0; i < 2; i++) {
    await page.getByRole('button', { name: /Sân hanok/ }).click()
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
    await page.getByRole('button', { name: /Linh vật gốm/ }).click()
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  }
  expect(errors).toEqual([])
})

test('phone viewport renders 3D without horizontal overflow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await page.getByLabel('Khung điện thoại').check()
  await page.getByLabel('Giảm chuyển động').check()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await expect(page.locator('canvas')).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  await page.screenshot({ path: resolve(reports, 'preview-mobile.png'), fullPage: true })
  await page.locator('canvas').screenshot({ path: resolve(posters, 'arena-mobile.png'), style: captureStyle })
})

test('WebGL unavailable shows accessible static illustration and keeps controls usable', async ({ page }) => {
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext
    HTMLCanvasElement.prototype.getContext = function (type: string, ...args: unknown[]) {
      if (type.startsWith('webgl') || type === 'experimental-webgl') return null
      return original.apply(this, [type, ...args] as Parameters<typeof original>)
    } as typeof original
  })
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'fallback')
  await expect(page.getByRole('img', { name: 'Minh họa tĩnh sân hanok và linh vật men ngọc' })).toBeVisible()
  await page.getByRole('button', { name: /Linh vật gốm/ }).click()
  await expect(page.getByRole('heading', { name: 'Ceramic Spirit' })).toBeVisible()
  await expect(page.locator('canvas')).toHaveCount(0)
  await page.screenshot({ path: resolve(reports, 'preview-fallback.png'), fullPage: true })
})

test('respects operating system reduced motion preference', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/')
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
})

test('switches to static illustration after WebGL context loss', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await page.locator('canvas').evaluate(canvas => {
    canvas.dispatchEvent(new Event('webglcontextlost', { cancelable: true }))
  })
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'fallback')
  await expect(page.getByRole('img', { name: 'Minh họa tĩnh sân hanok và linh vật men ngọc' })).toBeVisible()
})

test('six exported clips produce distinct static poses and live animation advances', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await page.getByRole('button', { name: /Linh vật gốm/ }).click()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  const signatures = new Set<string>()
  for (const clip of ['Idle', 'Happy', 'Thinking', 'Celebration', 'Disappointed', 'Greeting']) {
    await page.getByLabel('Trạng thái linh vật').selectOption(clip)
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.activeClip)).toBe(clip)
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.clipTime)).toBeCloseTo(.8, 3)
    const image = await page.locator('canvas').screenshot({ path: resolve(reports, `mascot-${clip.toLowerCase()}.png`), style: captureStyle })
    signatures.add(createHash('sha256').update(image).digest('hex'))
  }
  expect(signatures.size).toBe(6)
  await page.getByLabel('Giảm chuyển động').uncheck()
  const time = await page.evaluate(() => window.__STUDIO_METRICS__!.clipTime)
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__!.clipTime)).not.toBe(time)
  await page.getByRole('button', { name: 'Tạm dừng' }).click()
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__!.paused)).toBe(true)
  const paused = await page.evaluate(() => window.__STUDIO_METRICS__!.clipTime)
  await page.waitForTimeout(250)
  expect(await page.evaluate(() => window.__STUDIO_METRICS__!.clipTime)).toBe(paused)
})

test('night lighting renders the arena and low quality lowers render cost', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  const medium = await page.evaluate(() => window.__STUDIO_METRICS__!.drawCalls)
  await page.getByLabel('Ánh sáng').selectOption('night')
  await page.locator('canvas').screenshot({ path: resolve(reports, 'arena-night.png'), style: captureStyle })
  await page.getByLabel('Chất lượng').selectOption('low')
  await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__!.quality)).toBe('low')
  const low = await page.evaluate(() => window.__STUDIO_METRICS__!)
  expect(low.drawCalls).toBeLessThan(medium)
  expect(low.triangles).toBeLessThan(120_000)
  writeFileSync(resolve(reports, 'renderer-low.json'), JSON.stringify({ mediumDrawCalls: medium, low }, null, 2) + '\n')
})

test('failed model request displays fallback without blocking controls', async ({ page }) => {
  await page.route('**/models/mascot-base.glb', route => route.fulfill({ status: 404, body: 'Missing asset' }))
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'fallback')
  await expect(page.getByRole('img', { name: 'Minh họa tĩnh sân hanok và linh vật men ngọc' })).toBeVisible()
  await page.getByLabel('Chất lượng').selectOption('low')
  await expect(page.getByLabel('Chất lượng')).toHaveValue('low')
})

test('original and optimized mascot render identically in a deterministic static pose', async ({ browser }) => {
  const captures: Buffer[] = []
  for (const original of [true, false]) {
    const context = await browser.newContext({ viewport: { width: 1100, height: 1000 }, reducedMotion: 'reduce' })
    const page = await context.newPage()
    if (original) await page.route('**/models/mascot-base.glb', route => route.fulfill({ path: resolve(process.cwd(), '../assets/models/mascot-base.glb'), contentType: 'model/gltf-binary' }))
    await page.goto('/')
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
    await page.getByRole('button', { name: /Linh vật gốm/ }).click()
    await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
    await page.getByLabel('Chất lượng').selectOption('low')
    await page.getByLabel('Trạng thái linh vật').selectOption('Celebration')
    await expect.poll(() => page.evaluate(() => window.__STUDIO_METRICS__?.activeClip)).toBe('Celebration')
    captures.push(await page.locator('canvas').screenshot({ path: resolve(reports, original ? 'mascot-original.png' : 'mascot-optimized.png'), style: captureStyle }))
    await context.close()
  }
  expect(createHash('sha256').update(captures[0]).digest('hex')).toBe(createHash('sha256').update(captures[1]).digest('hex'))
})
