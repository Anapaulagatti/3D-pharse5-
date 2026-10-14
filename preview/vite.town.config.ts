import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react'
import {resolve} from 'node:path'
export default defineConfig({
 plugins:[react()],base:'./',
 // Only the versioned export directory is served outside preview/, never sources/secrets.
 server:{port:4191,strictPort:true,fs:{allow:[import.meta.dirname,resolve(import.meta.dirname,'../exports/v0.6')]}},
 build:{outDir:'.cache/town-dist',emptyOutDir:true,rollupOptions:{input:resolve(import.meta.dirname,'town.html')}},
})
