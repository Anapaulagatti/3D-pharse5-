import { Component, Suspense, useState, useEffect, type ReactNode } from 'react'
import Scene from './Scene'
import type { Settings } from './types'
import './style.css'
import { clips, expressions } from './Nari'

class Boundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false }
  static getDerivedStateFromError() { return { failed: true } }
  render() { return this.state.failed ? <p>3D không khả dụng. Bản v0.4 vẫn được bảo toàn trong thư mục showcase-v0.4.</p> : this.props.children }
}
export default function ReforgeApp() {
  const [s,set]=useState<Settings>({view:'architecture',lighting:'day',quality:matchMedia('(max-width:640px)').matches?'low':'medium',reduced:matchMedia('(prefers-reduced-motion:reduce)').matches,paused:false,preset:'hero',door:false,angle:null,clip:'Idle',expression:'Auto'})
  useEffect(()=>{const q=matchMedia('(prefers-reduced-motion:reduce)'),change=()=>set(a=>({...a,reduced:q.matches}));q.addEventListener('change',change);return()=>q.removeEventListener('change',change)},[])
  const update=<K extends keyof Settings>(k:K,v:Settings[K])=>set(a=>({...a,[k]:v}))
  return <div className="reforge"><header><a href="#main">KOREAN ARENA <span>/ STUDIO</span></a><b>v0.5 · JOSEON FANTASY REFORGE</b></header>
    <main id="main"><p className="overline">NARI'S FIRST DELIVERY</p><h1>Một mái nhà.<br/><em>Một hành trình mới.</em></h1><p className="intro">Gate B · kiểm tra kết cấu Hanok. Bản thử riêng; Pages v0.4 được giữ nguyên.</p>
      <section className="workspace"><aside><h2>Khảo sát Hanok</h2>
        <label>Chế độ<select aria-label="Chế độ" value={s.view} onChange={e=>set(a=>({...a,view:e.target.value as Settings['view'],preset:'hero',angle:null}))}><option value="architecture">Kiến trúc Hanok</option><option value="portrait">Cận cảnh Nari</option><option value="animation">Xem chuyển động</option></select></label>
        <label>Góc kiểm tra<select aria-label="Góc kiểm tra" value={s.preset} onChange={e=>set(a=>({...a,preset:e.target.value as Settings['preset'],angle:null}))}>{Object.entries({hero:'Tổng thể',front:'Mặt trước',rear:'Mặt sau',left:'Bên trái',right:'Bên phải',roof:'Toàn mái',connection:'Liên kết mái–cột',interior:'Bên trong'}).map(([v,t])=><option key={v} value={v}>{t}</option>)}</select></label>
        <label>Vòng kiểm tra 360°<input aria-label="Vòng kiểm tra 360°" type="range" min="0" max="360" step="1" value={s.angle??0} onChange={e=>update('angle',Number(e.target.value))}/></label>
        <label>Chất lượng<select aria-label="Chất lượng" value={s.quality} onChange={e=>update('quality',e.target.value as Settings['quality'])}><option value="low">Thấp</option><option value="medium">Vừa</option><option value="high">Cao</option></select></label>
        {s.view!=='architecture'&&<><label>Animation<select aria-label="Animation" value={s.clip} onChange={e=>update('clip',e.target.value)}>{clips.map(c=><option key={c}>{c}</option>)}</select></label><label>Biểu cảm<select aria-label="Biểu cảm" value={s.expression} onChange={e=>update('expression',e.target.value)}>{expressions.map(c=><option key={c}>{c}</option>)}</select></label></>}
        <label><input aria-label="Giảm chuyển động" type="checkbox" checked={s.reduced} onChange={e=>update('reduced',e.target.checked)}/> Giảm chuyển động</label>
        <button onClick={()=>update('paused',!s.paused)}>{s.paused?'Tiếp tục':'Tạm dừng'}</button>
        <button onClick={()=>update('door',!s.door)}>{s.door?'Đóng cửa':'Mở cửa'}</button><p>Kéo để xoay 360°. Cuộn để xem gần. Ngôi nhà có bốn mặt và hệ đỡ mái thật.</p>
      </aside><div className="stage" data-testid="reforge-stage"><Boundary><Suspense fallback={<p>Đang nạp kết cấu…</p>}><Scene settings={s}/></Suspense></Boundary></div></section>
      <footer>Nhân vật A — Nari đã được duyệt. Đây là graybox kiểm tra cấu trúc, chưa phải bản mỹ thuật hoàn chỉnh.</footer>
    </main></div>
}
