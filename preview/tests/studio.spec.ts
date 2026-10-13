import { test, expect } from '@playwright/test'
import { mkdirSync } from 'node:fs'
import { resolve } from 'node:path'

const reports = resolve(process.env.STUDIO_REPORT_DIR || resolve(process.cwd(), '../quality-reports'))
mkdirSync(reports, { recursive: true })

test('3D renders and scene, quality, light and motion controls work', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto('/')
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await expect(page.locator('canvas')).toBeVisible()
  await page.getByLabel('Giảm chuyển động').check()
  await expect(page.getByLabel('Giảm chuyển động')).toBeChecked()
  await page.screenshot({ path: resolve(reports, 'preview-desktop.png'), fullPage: true })
  await page.getByRole('button', { name: /Linh vật gốm/ }).click()
  await expect(page.getByRole('heading', { name: 'Ceramic Spirit' })).toBeVisible()
  await page.getByLabel('Chất lượng').selectOption('low')
  await page.getByLabel('Ánh sáng').selectOption('evening')
  await page.getByLabel('Trạng thái linh vật').selectOption('celebrate')
  await expect(page.getByLabel('Chất lượng')).toHaveValue('low')
  await expect(page.getByLabel('Ánh sáng')).toHaveValue('evening')
  await expect(page.getByLabel('Trạng thái linh vật')).toHaveValue('celebrate')
  await page.getByRole('button', { name: 'Tạm dừng' }).click()
  await expect(page.getByRole('button', { name: 'Tiếp tục' })).toHaveAttribute('aria-pressed', 'true')
  await page.getByRole('button', { name: /Đặt lại góc nhìn/ }).click()
  await expect(page.locator('.stage')).toHaveAttribute('data-engine', 'ready')
  await expect(page.locator('canvas')).toBeVisible()
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
