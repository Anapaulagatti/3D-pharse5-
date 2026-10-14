import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ReforgeApp from './App'
import '../style.css'
createRoot(document.getElementById('root')!).render(<StrictMode><ReforgeApp/></StrictMode>)
