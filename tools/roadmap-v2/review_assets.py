from pathlib import Path
from PIL import Image
import json,hashlib,html,shutil,subprocess
R=Path.cwd();D=R/'docs/roadmap-v2';O=D/'review-assets';O.mkdir(exist_ok=True);q=json.loads((D/'farm/FARM_QA.json').read_text());assert q['status'].startswith('PASS')
entries=[]
def add(name,path,crop=None):
 im=Image.open(path).convert('RGBA');im=im.crop(crop)if crop else im
 browser='-dpr'in name
 p=O/(name+('-browser.png'if browser else'-native.png'));im.save(p,optimize=True);preview=O/(name+'-review.jpg');im.convert('RGB').save(preview,quality=82,optimize=True)
 entries.append({'name':name,'native':p.name,'preview':preview.name,'dimensions':list(im.size),'nativeScale':None if browser else 1,'kind':'BROWSER_DPR_LAYOUT'if browser else'PHASER_NATIVE_READBACK','source':str(path.relative_to(R)),'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest()})
add('baseline-farm',R/'docs/phase3bd-final-quality/review-assets/farm-after-native.png')
for name in ['farm-00-empty','farm-01-prepared','farm-02-seeded','farm-07-harvested','three-00-sown','three-01-sprout','three-02-young','three-03-growing','three-04-mature','three-05-harvested','three-06-unlocked']:
 p=D/'farm'/(name+'-native.png');add(name,p)
 # Original-resolution local bed crop, derived from the ACTUAL camera scroll, never scaled artwork.
 cap=next(c for c in q['captures']if c['name']==name);sx,sy=cap['audit']['camera']['scroll'];im=Image.open(p)
 box=(int(388-sx),int(530-sy),int(540-sx),int(635-sy))
 if min(box[:2])>=0 and box[2]<=im.width and box[3]<=im.height:add(name+'-bed-crop-1x',p,box)
for name in ['story-00-accepted','story-01-room-shop','story-02-sign-restored','story-03-complete','story-04-reloaded']:add(name,D/(name+'-native.png'))
for name in ['hud-960-dpr1','hud-667-dpr2','hud-844-dpr3','interior-960-dpr1','interior-667-dpr2','interior-844-dpr3']:add(name,D/(name+'.png'))
for name in ['farm-six-and-exit','western-hanok-mouth','station-plaza','bridge-A','bridge-B']:add('route-'+name,D/('route-'+name+'-native.png'))
shutil.copy2(R/'public/assets/roadmap-v2/crops.png',O/'crop-atlas-native.png');shutil.copy2(R/'assets-src/roadmap-v2/crops-review-3x.png',O/'crop-atlas-3x.png')
(O/'IMAGE_PROOF.json').write_text(json.dumps({'status':'Actual Phaser native PNGs/crops; JPEGs review copies only','entries':entries,'approvedSourceArtworkAltered':False},indent=2)+'\n')
# 1x files retain exact native coordinates; DPR browser screenshots explicitly identified by names.
page='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V2 · Farm / Interior / Quest review</title><style>body{margin:18px;background:#1c332c;color:#f4e4ba;font:16px/1.5 system-ui}a{color:#a9e1c3}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}article{padding:10px;background:#294337;border:1px solid #9b895e}img{max-width:100%;height:auto}video{width:min(100%,960px)}.pixel{image-rendering:pixelated}</style><h1>V2 local playable candidate</h1><p><a href="../play/">Chơi bình thường</a> · <a href="../play/?qa&entry=farm">Review farm riêng</a> · <a href="../play/?qa&entry=retail">Review cửa phòng</a> · <a href="../">26 NPC / Daily Life / QA Portal</a></p><p>Không phải multiplayer hay bản thương mại. New art và tiếng Hàn chờ người duyệt. Các PNG farm/story/route là readback Phaser native1:1; ảnh DPR2/3 là browser-layout evidence, không thay thế native PNG. Video có nén, không dùng để chứng minh pixel-exact.</p><h2>Atlas crop native ·12loài/62frames</h2><a href="crop-atlas-native.png"><img class="pixel" src="crop-atlas-3x.png"></a><h2>Gameplay thật · không audio, không tăng tốc</h2>'''
for file in ['farm-world-loop.mp4','interiors-sign-courier.mp4']:page+=f'<h3>{html.escape(file)}</h3><video controls muted playsinline preload="metadata" src="videos/{file}"></video>'
page+='<h2>Native / trước-sau / mobile / tuyến đi</h2><div class="grid">'
for e in entries:page+=f'<article><h3>{html.escape(e["name"])}</h3><a href="{e["native"]}"><img src="{e["preview"]}" loading="lazy"></a><p>{e["dimensions"][0]}×{e["dimensions"][1]} · {e["kind"]} · <a href="{e["native"]}">PNG</a></p></article>'
page+='</div><p><a href="QA.md">QA đầy đủ</a> · <a href="IMAGE_PROOF.json">Nguồn ảnh</a> · <a href="VIDEO_PROOF.json">Nguồn video</a></p></html>'
(O/'index.html').write_text(page)
proof=[]
for name,raw in [('farm-world-loop.mp4',D/'farm/videos/farm-per-cell.webm'),('interiors-sign-courier.mp4',D/'videos/story.webm')]:
 p=O/'videos'/name;meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True));assert not[s for s in meta['streams']if s['codec_type']=='audio'];duration=float(meta['format']['duration']);assert duration>=(180 if 'farm' in name else 1);assert p.stat().st_size<100*1024*1024,'GitHub individual file limit'
 proof.append({'file':'videos/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'durationSeconds':duration,'audioStreams':0,'processing':'H264 encode only; original timing/dimensions, no scale/frame interpolation; native PNGs authoritative for texels'})
(O/'VIDEO_PROOF.json').write_text(json.dumps({'status':'PASS real recorded Phaser; no audio','videos':proof},indent=2)+'\n');print(len(entries),'image entries;2real silent videos')
