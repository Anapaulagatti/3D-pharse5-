import { Component, Suspense, useState, useEffect, useMemo, useRef, useCallback, type ReactNode } from 'react'
import Scene from './Scene'
import type { Settings } from './types'
import { createInput, createPlayer } from './physics'
import { clips, expressions } from './Nari'
import './style.css'

class Boundary extends Component<{children:ReactNode;onFailure:()=>void},{failed:boolean}>{
 state={failed:false}
 static getDerivedStateFromError(){return {failed:true}}
 componentDidCatch(){this.props.onFailure()}
 render(){return this.state.failed?<p>Đang chuyển sang ảnh dự phòng…</p>:this.props.children}
}
const canRender=()=>{try{return !!document.createElement('canvas').getContext('webgl2')}catch{return false}}
export default function ReforgeApp(){
 const input=useMemo(createInput,[]),player=useMemo(createPlayer,[]),stage=useRef<HTMLDivElement>(null)
 const [s,set]=useState<Settings>({view:'architecture',lighting:'day',quality:matchMedia('(max-width:640px)').matches?'low':'medium',reduced:matchMedia('(prefers-reduced-motion:reduce)').matches,paused:false,preset:'hero',door:false,angle:null,clip:'Idle',expression:'Auto',active:true,gesture:{name:'',id:0},reset:0})
 const [engine,setEngine]=useState<'loading'|'ready'|'fallback'>(()=>canRender()?'loading':'fallback')
 const [notice,setNotice]=useState('Một lá thư đang chờ được đưa đến ngôi nhà học.'),[visible,setVisible]=useState(true),[tab,setTab]=useState(!document.hidden),[mobileRun,setMobileRun]=useState(false)
 const update=<K extends keyof Settings>(k:K,v:Settings[K])=>set(a=>({...a,[k]:v}))
 const clear=useCallback(()=>{input.keys.clear();input.jump=false;input.wake?.()},[input])
 useEffect(()=>{const q=matchMedia('(prefers-reduced-motion:reduce)'),change=()=>set(a=>({...a,reduced:q.matches}));q.addEventListener('change',change);return()=>q.removeEventListener('change',change)},[])
 useEffect(()=>{const observer=new IntersectionObserver(e=>setVisible(e[0].isIntersecting));if(stage.current)observer.observe(stage.current);const visibility=()=>{setTab(!document.hidden);if(document.hidden)clear()};document.addEventListener('visibilitychange',visibility);window.addEventListener('blur',clear);return()=>{observer.disconnect();document.removeEventListener('visibilitychange',visibility);window.removeEventListener('blur',clear);document.body.style.cursor=''}},[clear])
 useEffect(()=>{clear()},[s.view,s.paused,clear])
 const door=useCallback(()=>{
  if(s.view==='play'&&Math.hypot(player.position[0],player.position[2]+.6)>2.1){setNotice('Đến gần cửa Hanok để tương tác.');return}
  set(a=>({...a,door:!a.door}));setNotice(s.door?'Cánh cửa khép lại nhẹ nhàng.':'Cửa mở — mời bạn bước vào.')
 },[s.view,s.door,player])
 const doorBlocked=useCallback(()=>{set(a=>({...a,door:true}));setNotice('Cửa đợi Nari đi qua rồi mới đóng.')},[])
 useEffect(()=>{
  const down=(e:KeyboardEvent)=>{
   if(s.view!=='play'||s.paused||engine!=='ready'||!stage.current?.contains(document.activeElement)||e.ctrlKey||e.metaKey||e.altKey)return
   if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','ShiftLeft','ShiftRight','Space','KeyE'].includes(e.code)){
    e.preventDefault();input.keys.add(e.code);if(e.code==='Space'&&!e.repeat)input.jump=true;if(e.code==='KeyE'&&!e.repeat)door();input.wake?.()
   }
  }
  const up=(e:KeyboardEvent)=>{input.keys.delete(e.code);input.wake?.()}
  window.addEventListener('keydown',down);window.addEventListener('keyup',up);return()=>{window.removeEventListener('keydown',down);window.removeEventListener('keyup',up)}
 },[s.view,s.paused,engine,input,door])
 const gesture=useCallback((name:string)=>{set(a=>({...a,gesture:{name,id:a.gesture.id+1}}));setNotice(name==='Greeting'?'Nari gửi bạn một lời chào.':name==='Celebration'?'Một niềm vui nhỏ trong sân Hanok.':'Nari vừa chú ý đến bạn.')},[])
 const react=useCallback(()=>gesture('InteractionReaction'),[gesture])
 const ready=useCallback(()=>setEngine('ready'),[]),failure=useCallback(()=>{clear();setEngine('fallback')},[clear])
 const changeView=(value:Settings['view'])=>{if(engine!=='fallback')setEngine('loading');set(a=>({...a,view:value,preset:'hero',angle:null}));clear()}
 const reset=()=>{Object.assign(player,createPlayer());set(a=>({...a,reset:a.reset+1,preset:'hero',angle:null,door:false,gesture:{name:'',id:0}}));clear();setNotice('Nari đã trở về đầu sân.')}
 const disabled=engine==='fallback'
 return <div className="reforge"><header><a href="#main">KOREAN ARENA <span>/ STUDIO</span></a><b>v0.5 · JOSEON FANTASY REFORGE</b></header>
  <main id="main"><p className="overline">NARI'S FIRST DELIVERY</p><h1>Một mái nhà.<br/><em>Một hành trình mới.</em></h1><p className="intro">Theo chân Nari qua sân đèn lồng, ghé ngôi nhà học và khám phá một góc Joseon tưởng tượng.</p>
   <section className="workspace"><aside><h2>Chọn góc khám phá</h2>
    <label>Chế độ<select aria-label="Chế độ" value={s.view} onChange={e=>changeView(e.target.value as Settings['view'])}><option value="hero">Toàn cảnh sân</option><option value="play">Chơi thử cùng Nari</option><option value="portrait">Cận cảnh Nari</option><option value="architecture">Kiến trúc Hanok</option><option value="animation">Xem chuyển động</option></select></label>
    {s.view!=='play'&&<><label>Góc kiểm tra<select aria-label="Góc kiểm tra" value={s.preset} disabled={disabled} onChange={e=>set(a=>({...a,preset:e.target.value as Settings['preset'],angle:null}))}>{Object.entries({hero:'Tổng thể',front:'Mặt trước',rear:'Mặt sau',left:'Bên trái',right:'Bên phải',roof:'Toàn mái',connection:'Liên kết mái–cột',interior:'Bên trong'}).map(([v,t])=><option key={v} value={v}>{t}</option>)}{(s.view==='portrait'||s.view==='animation')&&<option value="face">Khuôn mặt</option>}</select></label>
    <label>Vòng kiểm tra 360°<input aria-label="Vòng kiểm tra 360°" type="range" min="0" max="360" step="1" value={s.angle??0} disabled={disabled} onChange={e=>update('angle',Number(e.target.value))}/></label></>}
    <label>Ánh sáng<select aria-label="Ánh sáng" value={s.lighting} onChange={e=>update('lighting',e.target.value as Settings['lighting'])}><option value="day">Ngày trong trẻo</option><option value="evening">Chiều vàng</option><option value="night">Đêm đèn lồng</option></select></label>
    <label>Chất lượng<select aria-label="Chất lượng" value={s.quality} onChange={e=>update('quality',e.target.value as Settings['quality'])}><option value="low">Thấp</option><option value="medium">Vừa</option><option value="high">Cao</option></select></label>
    {(s.view==='portrait'||s.view==='animation')&&<><label>Animation<select aria-label="Animation" value={s.clip} disabled={disabled} onChange={e=>update('clip',e.target.value)}>{clips.map(c=><option key={c}>{c}</option>)}</select></label><label>Biểu cảm<select aria-label="Biểu cảm" value={s.expression} disabled={disabled} onChange={e=>update('expression',e.target.value)}>{expressions.map(c=><option key={c}>{c}</option>)}</select></label></>}
    <label><input aria-label="Giảm chuyển động" type="checkbox" checked={s.reduced} onChange={e=>update('reduced',e.target.checked)}/> Giảm chuyển động</label>
    {s.reduced&&<p>Chuyển động trang trí đã tắt. Nari vẫn di chuyển khi bạn điều khiển.</p>}
    <div className="buttons"><button disabled={disabled} onClick={()=>update('paused',!s.paused)}>{s.paused?'Tiếp tục':'Tạm dừng'}</button><button disabled={disabled} onClick={reset}>Trở lại sân</button></div>
    <p>Kéo để xoay, cuộn để xem gần. Mỗi mặt Hanok đều có thể được khám phá.</p>
   </aside><div className="presentation">
    <div className="stage" ref={stage} data-testid="reforge-stage" data-engine={engine} tabIndex={0} role="group" aria-label="Sân chơi Nari" aria-describedby="play-help" onPointerDown={()=>{if(s.view==='play')stage.current?.focus({preventScroll:true})}} onBlur={clear}>
     {disabled?<div className="reforge-poster"><img src="/posters/arena-desktop.png" alt="Ảnh dự phòng Hanok từ bản v0.4 được bảo toàn"/><p>Ảnh tĩnh · thiết bị chưa hỗ trợ WebGL.</p></div>:<Boundary onFailure={failure}><Suspense fallback={<p>Đang nạp sân Hanok…</p>}><Scene settings={{...s,active:visible&&tab}} input={input} player={player} onReact={react} onDoor={door} onDoorBlocked={doorBlocked} onReady={ready} onFailure={failure}/></Suspense></Boundary>}
     {engine==='loading'&&<p className="reforge-loading">Đang nạp không gian…</p>}
    </div>
    <p id="play-help" className="play-help">{s.view==='play'?'Chạm vào sân rồi dùng WASD / phím mũi tên · Shift chạy · Space nhảy · E mở cửa.':'Chạm Nari để nhận lời chào. Đổi góc nhìn để khám phá mái nhà và căn phòng nhỏ.'}</p>
    <div className="quick-actions"><button disabled={disabled} onClick={()=>gesture('Greeting')}>Vẫy chào</button><button disabled={disabled} onClick={()=>gesture('Thinking')}>Suy nghĩ</button><button disabled={disabled} onClick={()=>gesture('Celebration')}>Ăn mừng</button>{s.view!=='portrait'&&s.view!=='animation'&&<button disabled={disabled} onClick={door}>{s.door?'Đóng cửa':'Mở cửa'}</button>}</div>
    {s.view==='play'&&<div className="touch-controls" aria-label="Điều khiển cảm ứng">
     <div className="dpad">{[['ArrowUp','Đi lên','↑'],['ArrowLeft','Sang trái','←'],['ArrowDown','Đi xuống','↓'],['ArrowRight','Sang phải','→']].map(([key,label,icon])=><button key={key} aria-label={label} disabled={disabled||s.paused} onPointerDown={e=>{e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);input.keys.add(key);input.wake?.()}} onPointerUp={()=>{input.keys.delete(key);input.wake?.()}} onPointerCancel={clear} onLostPointerCapture={()=>input.keys.delete(key)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();input.keys.add(key);input.wake?.()}}} onKeyUp={()=>{input.keys.delete(key);input.wake?.()}}>{icon}</button>)}</div>
     <button aria-pressed={mobileRun} disabled={disabled||s.paused} onClick={()=>{input.mobileRun=!mobileRun;setMobileRun(!mobileRun);input.wake?.()}}>Chạy</button><button disabled={disabled||s.paused} onClick={()=>{input.jump=true;input.wake?.();stage.current?.focus({preventScroll:true})}}>Nhảy</button>
    </div>}
    <p className="reforge-notice" role="status">{notice}</p>
   </div></section><footer>Bản thử riêng v0.5 · Nari là nhân vật hư cấu theo concept A đã duyệt. Pages v0.4 vẫn được giữ nguyên.</footer>
  </main></div>
}
