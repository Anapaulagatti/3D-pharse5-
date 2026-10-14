const urls={house:new URL('../../../exports/v0.6/models/letter-plaza.glb',import.meta.url).href,nari:new URL('../../../exports/v0.6/models/nari-chibi.glb',import.meta.url).href,poster:new URL('../../../exports/v0.6/posters/plaza-day.png',import.meta.url).href}
export const townURL=(id:string)=>urls[id as keyof typeof urls]
