import { build } from 'vite';
import { checkAssetRights } from '../rights-gate.mjs';
checkAssetRights('private-review');
await build({configFile:false,base:'./',publicDir:false,define:{'import.meta.env.VITE_RELEASE_PROFILE':JSON.stringify('private-review')},plugins:[{name:'private-review-label',transformIndexHtml(html){return html.replace('<head>','<head><meta name="korean-arena-release-profile" content="private-review">')}}],build:{outDir:'/tmp/phase3ba-private-review',emptyOutDir:true,manifest:true,target:'es2022',chunkSizeWarningLimit:1900,rolldownOptions:{input:{game:'index.html'}}}});
