import { Component, Suspense, lazy, useCallback, useState, type ReactNode } from 'react'
import Poster from './Poster'
import type { SceneSettings } from './types'
import { modelAssets, formatBytes, assetURL } from './assets'

const SceneView = lazy(() => import('./SceneView'))
class SceneBoundary extends Component<{ children: ReactNode; fallback: ReactNode; onFailure: () => void }, { failed: boolean }> {
  state = { failed: false }
  static getDerivedStateFromError() { return { failed: true } }
  componentDidCatch() { this.props.onFailure() }
  render() { return this.state.failed ? this.props.fallback : this.props.children }
}

function canRender3D() {
  try { return !!document.createElement('canvas').getContext('webgl2') } catch { return false }
}

export default function App() {
  const [settings, setSettings] = useState<SceneSettings>({
    scene: 'courtyard', quality: 'medium', mood: 'Idle', lighting: 'day',
    reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    paused: false, mobile: window.matchMedia('(max-width: 640px)').matches, focus: 'overview',
  })
  const [webgl] = useState(canRender3D)
  const [engine, setEngine] = useState<'loading' | 'ready' | 'fallback'>(webgl ? 'loading' : 'fallback')
  const [reset, setReset] = useState(0)
  const ready = useCallback(() => setEngine('ready'), [])
  const failed = useCallback(() => setEngine('fallback'), [])
  const update = <K extends keyof SceneSettings>(key: K, value: SceneSettings[K]) => setSettings(s => ({ ...s, [key]: value }))
  const resetCamera = () => { update('focus', 'overview'); setReset(r => r + 1); if (engine !== 'fallback') setEngine('loading') }
  const switchScene = (scene: SceneSettings['scene']) => { if (settings.scene === scene) return; update('scene', scene); if (engine !== 'fallback') setEngine('loading') }
  const poster = <div className="poster"><Poster mascot={settings.scene === 'mascot'} /><p>Ảnh tĩnh · 3D tạm thời không khả dụng</p></div>
  return <div className="studio-shell">
    <header className="topbar">
      <a className="wordmark" href="#main"><span className="logo-mark" aria-hidden="true">◈</span> DISTRICT <span className="wordmark-light">/ 3D STUDIO</span></a>
      <span className="demo-pill"><span /> DEMO ĐỘC LẬP</span>
    </header>
    <main id="main">
      <section className="intro">
        <p className="eyebrow">THE LIVING HANGEUL DISTRICT <span>한글 마을</span></p>
        <h1>Một góc phố.<br /><em>Một thế giới nhỏ.</em></h1>
        <p className="intro-copy">Mái hanok, ánh đèn ấm và một người bạn men ngọc. Không gian thử nghiệm cho một hành trình học tập sống động.</p>
      </section>
      <div className="workspace">
        <aside className="controls" aria-label="Điều khiển demo 3D">
          <div className="section-label"><span>01</span> KHÔNG GIAN</div>
          <div className="scene-options">
            <button className={settings.scene === 'courtyard' ? 'scene-option active' : 'scene-option'} aria-pressed={settings.scene === 'courtyard'} onClick={() => switchScene('courtyard')}>
              <span className="scene-symbol" aria-hidden="true">⌂</span><span><strong>Sân hanok</strong><small>Mái cong & vườn mận</small></span><span className="option-arrow" aria-hidden="true">+</span>
            </button>
            <button className={settings.scene === 'mascot' ? 'scene-option active' : 'scene-option'} aria-pressed={settings.scene === 'mascot'} onClick={() => switchScene('mascot')}>
              <span className="scene-symbol" aria-hidden="true">♧</span><span><strong>Linh vật gốm</strong><small>Ceramic Seed Spirit</small></span><span className="option-arrow" aria-hidden="true">+</span>
            </button>
          </div>
          <div className="section-label"><span>02</span> THIẾT LẬP</div>
          <label className="field">Chất lượng<select value={settings.quality} onChange={e => update('quality', e.target.value as SceneSettings['quality'])}><option value="low">Thấp</option><option value="medium">Vừa</option><option value="high">Cao</option></select></label>
          <label className="field">Ánh sáng<select value={settings.lighting} onChange={e => update('lighting', e.target.value as SceneSettings['lighting'])}><option value="day">Nắng dịu</option><option value="evening">Chiều ấm</option><option value="night">Đêm đèn</option></select></label>
          <label className="field">Trạng thái linh vật<select value={settings.mood} onChange={e => update('mood', e.target.value as SceneSettings['mood'])}><option value="Idle">Bình yên</option><option value="Happy">Vui vẻ</option><option value="Thinking">Suy nghĩ</option><option value="Celebration">Ăn mừng</option><option value="Disappointed">Buồn nhẹ</option><option value="Greeting">Chào bạn</option></select></label>
          <label className="toggle"><input type="checkbox" checked={settings.reducedMotion} onChange={e => update('reducedMotion', e.target.checked)} /><span>Giảm chuyển động</span></label>
          <label className="toggle"><input type="checkbox" checked={settings.mobile} onChange={e => { update('mobile', e.target.checked); resetCamera() }} /><span>Khung điện thoại</span></label>
          <div className="palette" aria-label="Bảng màu hanji và men ngọc"><span style={{ background: '#15243a' }} /><span style={{ background: '#f5efe1' }} /><span style={{ background: '#72beac' }} /><span style={{ background: '#e57b69' }} /><span style={{ background: '#cfac67' }} /></div>
          <p className="palette-caption">Hanji · Celadon · Gentle magic</p>
          <div className="focus-controls"><div className="section-label"><span>03</span> KHÁM PHÁ</div>
            {([['overview', 'Tổng quan'], ['dais', 'Đài gốm'], ['roof', 'Mái hanok'], ['garden', 'Vườn mận']] as const).map(([value, label]) =>
              <button key={value} disabled={settings.scene !== 'courtyard'} aria-pressed={settings.focus === value} onClick={() => update('focus', value)}>{label}</button>)}
          </div>
        </aside>
        <section className="viewer-section" aria-label="Khung xem 3D">
          <div className="viewer-header"><div><span className="eyebrow">{settings.scene === 'courtyard' ? 'SCENE 01' : 'SCENE 02'}</span><h2>{settings.scene === 'courtyard' ? 'Hanok Rooftop' : 'Ceramic Spirit'}</h2></div><span className="viewer-tag">LIVING DISTRICT · v0.2</span></div>
          <div className={`stage ${settings.mobile ? 'mobile-frame' : ''}`} data-engine={engine} data-clip={settings.mood}>
            {engine === 'fallback' ? poster : <SceneBoundary fallback={poster} onFailure={failed}>
              <Suspense fallback={<div className="loading" role="status">Đang dựng không gian…</div>}>
                <SceneView key={`${settings.scene}:${reset}`} settings={settings} onReady={ready} onFailure={failed} onFocus={focus => update('focus', focus)} />
              </Suspense>
            </SceneBoundary>}
            {engine === 'loading' && <div className="model-loading-overlay" role="status">Đang tải mô hình 3D…</div>}
            <span className="stage-note" role="status">{engine === 'ready' ? '3D đang hoạt động' : engine === 'fallback' ? 'Chế độ 2D' : 'Đang tải 3D'}</span>
          </div>
          <div className="viewer-footer"><span>Kéo để xoay · Chọn điểm sáng để khám phá</span><div><button onClick={() => update('paused', !settings.paused)} aria-pressed={settings.paused}>{settings.paused ? 'Tiếp tục' : 'Tạm dừng'}</button><button onClick={resetCamera}>Đặt lại góc nhìn <span aria-hidden="true">↺</span></button></div></div>
        </section>
      </div>
      <section className="asset-panel" aria-label="Thông tin asset"><div className="section-label">BỘ SƯU TẬP · ASSET 3D NGUYÊN BẢN</div><div className="asset-cards">
        {modelAssets.map(asset => <article key={asset.id}><div><h3>{asset.id === 'arena-hero' ? 'Hanok Rooftop Arena' : 'Ceramic Seed Spirit'}</h3><span>v{asset.version} · {formatBytes(asset.file_bytes)}</span></div><p>{asset.geometry?.totalTriangleCount.toLocaleString('vi-VN')} tam giác · {asset.animations?.length} clip · Nguyên bản</p><a href={assetURL(asset.id)} download={asset.file.split('/').pop()}>Tải model GLB <span aria-hidden="true">↓</span></a></article>)}
      </div></section>
      <section className="notes" aria-label="Thông tin bản demo"><div><span className="section-label">CHẤT LIỆU</span><p>Giấy hanji. Gốm men ngọc.<br />Ánh sáng nhẹ, hình khối rõ ràng.</p></div><div><span className="section-label">CERAMIC SEED SPIRIT</span><p>Sáu chuyển động, một người bạn nhỏ.<br />Model và animation từ Blender.</p></div><div><span className="section-label">KHÔNG GIAN ĐỘC LẬP</span><p>Dữ liệu demo, không cần tài khoản.<br />Chưa tích hợp vào ứng dụng Korean Arena.</p></div></section>
    </main>
    <footer className="site-footer"><span>3D-pharse5- / Studio</span><span>Mỗi góc nhỏ, một khởi đầu.</span></footer>
  </div>
}
