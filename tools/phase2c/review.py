"""Build review plates from real native Phaser crops; label source-only sheets explicitly."""
from compose import Composer
from core import *
from PIL import ImageDraw
import html
c=Composer();ids=list(B);bg=(29,39,53);fg=(240,234,218)
def save(im,name,review=False):
 im.save(D/name)
 if review:im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(D/name.replace('-native.png','-review-2x.png'))
board=Image.new('RGB',(768,516),bg);dr=ImageDraw.Draw(board)
for i,id in enumerate(ids):
 x=i%4*192;y=i//4*172;dr.text((x+6,y+5),id.title()+'  default | fashion',fill=fg)
 for j,mode in enumerate([id+'-default','fashion-'+id]):board.paste(Image.open(D/'gameplay'/f'{mode}-walk-front-native-crop.png'),(x+j*96,y+24))
 dr.text((x+6,y+141),'Actual Phaser / 1 native px',fill=fg)
save(board,'twelve-default-fashion-native.png',True)
# Single-item identity cards are source previews, not gameplay screenshots.
board=Image.new('RGB',(864,492),bg);dr=ImageDraw.Draw(board)
for i,item in enumerate(c.catalog['items'][10:]):
 x=i%6*144;y=i//6*164;v=item['variants'][0];im=Image.open(R/'public'/v['preview']).convert('RGBA');board.paste(im,(x+24,y+21),im);dr.text((x+4,y+2),item['id'][3:][:22],fill=fg);dr.text((x+4,y+140),'/'.join(item['compatibility']['characterIds']),fill=fg)
save(board,'eighteen-catalog-source-native.png',True)
# Old version reproducer: original old patches against the current approved gait.
old=Composer();old.catalog=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());old.items={i['id']:i for i in old.catalog['items']}
for item in [i for i in c.catalog['items'][:10]if i['category']=='outfit']:
 id=item['compatibility']['characterIds'][0];im=Image.new('RGB',(768,272),bg);dr=ImageDraw.Draw(im);dr.text((4,3),'SOURCE ONLY: original old outfit patch / current approved base',fill=fg);dr.text((4,139),'RESTORED: pose-bound current outfit / same scale, same phases',fill=fg)
 for n in range(8):
  name=f'walk-front-{n}'
  for row,compiler in enumerate([old,c]):
   q=compiler.render(id,[item['id']],name);im.paste(q,(n*96,row*136+20),q)
 save(im,'foundation-'+item['id']+'-source-before-after-native.png',True)
# Cross-reference approved Juni vs customized all12, phase aligned source only.
for action,view in [('walk','front'),('walk','right'),('run','back')]:
 im=Image.new('RGB',(768,13*132),bg);dr=ImageDraw.Draw(im)
 for row,id in enumerate(['juni-reference']+ids):
  dr.text((4,row*132+2),'SOURCE PHASES: '+id,fill=fg)
  look=next((p['appearance']for p in c.catalog['presets']if p['id']=='fashion-'+id),None)
  selected=[]if look is None else[look['hairstyleId'],look['outfitId'],*look['accessoryIds']]
  for n in range(8):
   q=c.render('juni'if id=='juni-reference'else id,selected,f'{action}-{view}-{n}');im.paste(q,(n*96,row*132+18),q)
 save(im,f'{action}-{view}-approved-reference-source-native.png')
# Reuse independent composition readback for the actual software WebGL screenshot.
q=json.loads((D/'webgl-evidence.json').read_text());a=q['audit'];st=a['state'];name=a.get('actualFrame',st['frame']);look=st['appearance'];sprite=c.render(st['characterId'],[look['hairstyleId'],look['outfitId'],*look['accessoryIds']],name);sx,sy=a['camera']['scroll'];x=math.floor(st['x']+.5)-48-sx;y=math.floor(st['y']+.5)-100-sy;actual=Image.open(D/q['file']).convert('RGB').crop((x,y,x+96,y+112));p=np.array(sprite);m=int(((p[:,:,3]==255)&np.any(np.array(actual)!=p[:,:,:3],2)).sum());assert m==0,m;actual.save(D/'custom-ara-webgl-native-crop.png');q['nativeOpaqueReadback']={'pixels':int((p[:,:,3]==255).sum()),'mismatch':m,'scale':[1,1],'filter':'nearest','implementation':'Independent Python native sparse composition versus actual WebGL backing pixels'};(D/'webgl-evidence.json').write_text(json.dumps(q,indent=2)+'\n')
lines=['# Cosmetic catalog','', '28 unique items: 10 preserved IDs with derived pose-bound revisions; 18 new designs. 46 character-specific variants. All are free review items; human art approval is pending.','', '| ID | Vietnamese / Korean | Category | Compatible characters | Origin |','|---|---|---|---|---|']
for i in c.catalog['items']:lines.append('| '+i['id']+' | '+i['name']['vi']+' / '+i['name']['ko']+' | '+i['category']+' | '+', '.join(i['compatibility']['characterIds'])+' | '+('New Phase2C design'if i['id'].startswith('kr-')else'Preserved ID; derived native-motion revision')+' |')
lines+=['','[18 source identity previews](eighteen-catalog-source-native.png) · [2× nearest review](eighteen-catalog-source-review-2x.png). These are source compositions; see [actual Phaser clips](REVIEW.html).','','Every variant contains stable character ID, paint/erase textures, per-frame mapping, preview, provenance, base SHA256, content revision, native96×112 registration and48,100 anchor. Per-file provenance describes the source and hidden cells. Sources: [catalog](../../assets-src/characters/phase2c/catalog.json), [native authoring recipes](../../tools/phase2c/designs.py), [compiler](../../tools/phase2c/collection.py).','','New design work: native hair contours and directional silhouettes; wrap collars, goreum ties, skirt/coat panels, campus layers, streetwear, utility pockets and garden apron; head/torso-registered ornaments, bags, glasses and hats. Approved pose anatomy and contact footwear are intentionally retained. No paid API, generated portrait substitution, base re-export or old-body pose replacement.']
(D/'COSMETIC_CATALOG.md').write_text('\n'.join(lines)+'\n')
lines=['# Compatibility matrix','','✓ = authored and registered for all native cells. Blank = unavailable; never inferred universal.','', '| Item | '+' | '.join(ids)+' |','|---|'+'---|'*12]
for i in c.catalog['items']:lines.append('| '+i['id']+' | '+' | '.join('✓'if id in i['compatibility']['characterIds']else'—'for id in ids)+' |')
lines+=['','## Complete curated looks','','| Character | Hair | Outfit | Accessory |','|---|---|---|---|']
for id in ids:
 p=next(p for p in c.catalog['presets']if p['id']=='fashion-'+id)['appearance'];lines.append('| '+id+' | '+p['hairstyleId']+' | '+p['outfitId']+' | '+', '.join(p['accessoryIds'])+' |')
lines+=['','Garden hat excludes Doyun’s original swept-quiff and curly-crop cosmetics: those head fits are not claimed. The most recent selection removes the incompatible item in the draft. Face/hand visibility and hat/hair ownership are baked into registered frames. Glasses are intentionally hidden from the back; valid hidden cells use explicit null, never missing mapping entries.','','192 compatible appearance combinations /21,760 offline native frames exhaustively checked. Every claimed variant is observed in an actual combined gameplay look; the original10 are also independently captured as single-item looks. Human interaction/garment quality still requires review.']
(D/'COMPATIBILITY_MATRIX.md').write_text('\n'.join(lines)+'\n')
# Self-contained HTML review, local links portable inside the ZIP.
style='body{margin:24px auto;padding:0 16px;max-width:1100px;background:#172333;color:#efe8d6;font:16px system-ui}a{color:#8be4d5}img{max-width:100%;height:auto;image-rendering:pixelated}video{width:100%;max-height:660px}section{padding:16px 0;border-top:1px solid #657}summary{cursor:pointer;padding:12px}figure{margin:12px 0}figcaption{font-size:14px;color:#cec8b7}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}'
parts=[f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Korean Arena · Phase2C review</title><style>{style}</style><h1>Korean Arena · Fashion Studio</h1><p>TECHNICAL PASS — ARTISTIC APPROVAL PENDING. Phase2B approved and immutable; Phase3 locked. Physical Android/iPhone and hardware performance NOT TESTED.</p><p><a href="../../index.html">Play locally</a> · <a href="README.md">Scope</a> · <a href="QA.md">QA</a> · <a href="COMPATIBILITY_MATRIX.md">Compatibility</a> · <a href="DEVICE_REVIEW.html">Device test/export</a></p><h2>All12 · actual native Phaser</h2><p>Default vs complete fashion look,1 pixel per source pixel. Open PNG directly for1:1; the browser may fit this page to the viewport.</p><a href="twelve-default-fashion-native.png"><img src="twelve-default-fashion-native.png" alt="12 actual Phaser default versus fashion comparisons"></a><p><a href="twelve-default-fashion-review-2x.png">2× nearest review</a> · <a href="gameplay/native-pixel-qa.json">192 native readbacks</a></p><h2>18 new designs · source identity cards</h2><img src="eighteen-catalog-source-native.png" alt="18 new cosmetic source previews"><p>Source previews are labeled separately from gameplay. Each design has2 verified compatible characters.</p><h2>Studio / mobile landscape</h2><div class="grid">']
for n in ['studio-1280x900','studio-667x375','studio-844x390','preset-management-desktop','studio-hairstyle','studio-outfit','studio-accessory','studio-full-gallery']:parts.append(f'<figure><a href="{n}.jpg"><img loading="lazy" src="{n}.jpg" alt="{n}"></a><figcaption>{n}</figcaption></figure>')
parts+=['</div><h2>Actual gameplay · all12 complete customized looks</h2><p>Real canonical Phaser, keyboard input, all idle/walk/run directions and gestures. Videos are unretimed compression copies; PNG is the pixel-quality authority. Expand each character for video.</p>']
for id in ids:
 parts.append(f'<section><h3>{id.title()}</h3><p><a href="gameplay/fashion-{id}-walk-front-phaser-native.png">Full unresampled native Phaser screenshot</a></p><a href="gameplay/fashion-{id}-actual-native-sheet.png"><img loading="lazy" src="gameplay/fashion-{id}-actual-native-sheet.png" alt="{id} actual14clip native sheet"></a><details><summary>Actual full locomotion video</summary><video controls preload="none" src="gameplay/fashion-{id}-actual-gameplay.mp4"></video></details><details><summary>Default front/right comparison video</summary><video controls preload="none" src="gameplay/{id}-default-actual-gameplay.mp4"></video></details></section>')
parts+=['<h2>Foundation: original10 corrected before expansion</h2><p><a href="foundation-gate.json">Foundation gate</a> · <a href="foundation/native-pixel-qa.json">196 actual native readbacks</a>. Old source textures remain immutable. These sheets reproduce old patch ownership versus the new pose-bound revision at identical phase/scale; they are SOURCE ONLY.</p>']
for i in [i for i in c.catalog['items'][:10]if i['category']=='outfit']:parts.append(f'<figure><a href="foundation-{i["id"]}-source-before-after-native.png"><img loading="lazy" src="foundation-{i["id"]}-source-before-after-native.png" alt="Source before after {i["id"]}"></a></figure>')
parts+=['<h2>Preset and extended session video</h2><video controls preload="none" src="studio-session-actual.mp4"></video><p>60 actual switches +100 preview/apply operations, preset save/rename, cancel, return and reload. See <a href="long-session.json">complete session data</a>.</p><h2>Remaining review</h2><p>Human artistic acceptance, physical Android Chrome/iPhone Safari and hardware GPU/thermal/memory certification remain pending. All12 default assets, world, collision and controls remain protected. No Phase3, merge or deployment.</p>']
(D/'REVIEW.html').write_text('\n'.join(parts)+'\n');print('Review plates, catalog, compatibility and gallery built; actual software WebGL native readback mismatch0')
