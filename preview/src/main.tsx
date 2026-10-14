import { StrictMode, lazy, Suspense } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './style.css'

const Reforge = lazy(() => import('./reforge/App'))
const candidate = new URLSearchParams(location.search).get('candidate') === 'v05'

createRoot(document.getElementById('root')!).render(
  <StrictMode><Suspense fallback={<p>Đang mở Studio…</p>}>{candidate ? <Reforge /> : <App />}</Suspense></StrictMode>,
)
