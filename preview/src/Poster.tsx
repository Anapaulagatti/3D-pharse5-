import { useState } from 'react'
import { assets, assetURL } from './assets'

export default function Poster({ mascot = false }: { mascot?: boolean }) {
  const [failed, setFailed] = useState(false)
  const image = assets.find(a => a.id === (mascot ? 'mascot-transparent' : 'arena-desktop'))
  if (image && !failed) return <img src={assetURL(image.id)} alt={mascot ? 'Chân dung linh vật gốm — chế độ 2D' : 'Minh họa tĩnh sân hanok và linh vật men ngọc'} onError={() => setFailed(true)} />
  return (
    <svg viewBox="0 0 700 500" role="img" aria-label="Minh họa tĩnh sân hanok và linh vật men ngọc">
      <defs>
        <linearGradient id="sky" x2="0" y2="1"><stop stopColor="#dce7e2" /><stop offset="1" stopColor="#f5efe1" /></linearGradient>
      </defs>
      <rect width="700" height="500" fill="url(#sky)" />
      <circle cx="540" cy="110" r="42" fill="#f9e5b5" />
      <path d="M80 295 330 165 620 300 370 450Z" fill="#98bbae" />
      <path d="M80 295v25l290 155v-25ZM370 450v25l250-150v-25Z" fill="#668e84" />
      <path d="M185 290v-95h110v95M210 285v-65m60 65v-65" fill="#e9ddc4" stroke="#997b5d" strokeWidth="10" />
      <path d="M150 200 245 140l105 60-25 15H172Z" fill="#293c55" />
      <path d="M180 200h138" stroke="#72beac" strokeWidth="7" />
      <ellipse cx="395" cy="326" rx="67" ry="29" fill="#cfac67" />
      <ellipse cx="395" cy="317" rx="64" ry="26" fill="#f5efe1" />
      <path d="M370 274q-42-46-8-64l22 25 32-8 23-28q23 14 2 46 25 66-39 69-53 0-32-40Z" fill="#72beac" />
      <ellipse cx="398" cy="281" rx="21" ry="23" fill="#f5efe1" />
      <circle cx="383" cy="257" r="4" fill="#15243a" /><circle cx="415" cy="257" r="4" fill="#15243a" />
      <path d="M393 267q6 6 12 0" fill="none" stroke="#15243a" strokeWidth="3" />
      <path d="M500 295v-72m-20 5h40" stroke="#997b5d" strokeWidth="7" />
      <rect x="488" y="229" width="24" height="28" rx="9" fill="#f9d795" />
      <path d="M125 292v-50m-15-5q10-28 23-3 25-13 21 10-21 20-44-7Z" fill="#e57b69" stroke="#997b5d" strokeWidth="3" />
    </svg>
  )
}
