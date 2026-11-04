from pathlib import Path
from PIL import Image
import json,hashlib,subprocess,shutil
D=Path('docs/phase3bd-final-quality');A=D/'review-assets';A.mkdir(exist_ok=True);(A/'videos').mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'frozen/FARM_QA.json').read_text());assert q['status'].startswith('PASS');h=json.loads((D/'HANOK_AFTER_QA.json').read_text());assert h['status'].startswith('PASS');assert {x['observedCharacter']for x in h['characters']}=={'juni','haneul'}
raws=[(D/'frozen/videos/farm-per-cell.webm','farm-per-cell'),(D/'videos/hanok-before-blocked.webm','hanok-before-blocked'),(D/'videos/hanok-after-juni.webm','hanok-after-juni'),(D/'videos/hanok-after-haneul.webm','hanok-after-haneul'),(D/'mobile/videos/mobile-touch.webm','mobile-touch')];videos=[]
for p,name in raws:
 out=A/'videos'/(name+'.mp4');out.exists() or subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-an','-c:v','libx264','-preset','veryfast','-threads','2','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));assert not any(s['codec_type']=='audio'for s in probe['streams']);videos.append({'file':'videos/'+out.name,'bytes':out.stat().st_size,'sha256':sha(out),'sourceCapture':str(p),'sourceSHA256':sha(p),'seconds':probe['format']['duration'],'kind':'Actual unmodified Phaser input recording; H264lossy review, no resize; nativePNG is pixel evidence','audioStreams':0})
(D/'VIDEO_PROOF.json').write_text(json.dumps(videos,indent=2)+'\n')
# Selected full native frames are copied LOSSLESSLY; originals remain untouched.
full={'farm-before':D/'farm-overview-before-native.png','farm-after':D/'farm-overview-after-native.png','farm-mixed':D/'frozen/farm-09-mature-next-to-young-native.png','hanok-before':D/'hanok-before-native.png','hanok-after-juni':D/'hanok-after-juni-native.png','hanok-after-haneul':D/'hanok-after-haneul-native.png'};native=[]
for name,p in full.items():
 im=Image.open(p).convert('RGBA');out=A/(name+'-native.png');im.save(out,optimize=True,compress_level=9);check=Image.open(out).convert('RGBA');assert check.tobytes()==im.tobytes()
 im.convert('RGB').save(A/(name+'-review.jpg'),quality=85,optimize=True)
 native.append({'file':out.name,'original':str(p),'originalSHA256':sha(p),'publishedSHA256':sha(out),'nativePixelsSHA256':hashlib.sha256(im.tobytes()).hexdigest(),'dimensions':im.size,'operation':'Lossless PNG encode only; no scaling/filtering/color changes; original retained'})
# Original-resolution crops from actual world rendering, never synthetic growth images.
for v in q['captures']:
 p=D/'frozen'/(v['name']+'-native.png');im=Image.open(p).convert('RGBA');a=v['audit'];tile=next(x for x in a['farmSprites']if x['key']=='farm-materials'and x['position']==[394,535]);x,y=map(round,tile['screen']);im.crop((x-10,y-12,x+150,y+102)).save(A/(v['name']+'-crop-1x.png'),optimize=True)
sc=json.loads((D/'scallion/SCALLION_QA.json').read_text());assert sc['status'].startswith('PASS')
for v in sc['stages']:
 p=D/'scallion'/('scallion-'+v['frame']+'-native.png');im=Image.open(p);tile=next(x for x in v['audit']['farmSprites']if x['key']=='farm-materials'and x['position']==[394,535]);x,y=map(round,tile['screen']);im.crop((x-10,y-12,x+150,y+102)).save(A/('scallion-'+v['frame']+'-crop-1x.png'),optimize=True)
# Exact opaque native-pixel readback (all visible source pixels; no artistic PASS inferred).
atlas=Image.open('public/assets/farming/phase3bd-final-quality/crops.png').convert('RGBA');frames=json.load(open('public/assets/farming/phase3bd-final-quality/crops.json'))['frames'];pixels=[]
for v in q['captures']:
 plants=[x for x in v['audit']['farmSprites']if x['key']=='farm-crops'and x['visible']and x['position']==[464,619]]
 if not plants:continue
 p=plants[0];im=Image.open(D/'frozen'/(v['name']+'-native.png')).convert('RGBA');r=frames[p['frame']]['frame'];src=atlas.crop((r['x'],r['y'],r['x']+40,r['y']+44));x,y=round(p['screen'][0]-20),round(p['screen'][1]-40);total=matched=0
 for yy in range(44):
  for xx in range(40):
   rgba=src.getpixel((xx,yy))
   if rgba[3]:total+=1;matched+=im.getpixel((x+xx,y+yy))[:3]==rgba[:3]
 pixels.append({'capture':v['name'],'frame':p['frame'],'opaquePixels':total,'exactMatches':matched,'status':'PASS'if matched==total else'OCCLUSION_OR_MISMATCH_REVIEW'})
(D/'PIXEL_READBACK.json').write_text(json.dumps(pixels,indent=2)+'\n');(D/'NATIVE_EVIDENCE.json').write_text(json.dumps(native,indent=2)+'\n')
summary={'gameplay':q['status'],'actualCharacterSelection':q.get('actualCharacterSelection'),'normalSpawn':q.get('start'),'fixtures':q['fixtures'],'captures':[{'name':x['name'],'selectedCell':x['save']['economy']['plots']['NW-FARM-04'],'neighbor':x['save']['economy']['plots']['NW-FARM-04-C4'],'inventory':x['save']['inventory'],'coins':x['save']['coins']}for x in q['captures']],'shop':{'coins':q['shop']['coins'],'inventory':q['shop']['inventory']},'independence':q['independence'],'persistence':q['persistence'],'hanok':h['status'],'characters':[{'id':v['id'],'observedCharacter':v['observedCharacter'],'crossings':v['crossings'],'semantics':v['semantics'],'status':v['status']}for v in h['characters']],'pixelReadback':pixels,'physicalDevices':'NOT TESTED','artisticAcceptance':'PENDING HUMAN REVIEW'};(A/'QA_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
for n in ['RUNTIME_PIXEL_DIFF.json','HANOK_COLLISION_DIAGNOSIS.json','PROTECTED_AUDIT.json','FORGE_RETAINED_WARNINGS.json','TOOLS_ACTUALLY_USED.json']:
 shutil.copy2(D/n,A/n)
html='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase3B-D · Farm art và Tây Hanok</title><style>body{background:#172c2b;color:#f8edd1;font:17px system-ui;margin:20px}a{color:#aee9ce}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}img{max-width:100%;height:auto}img.pixel{image-rendering:pixelated;width:480px}video{width:min(100%,1000px)}article{background:#203a31;padding:12px;border:1px solid #6c7856}</style><h1>Farm native và hành lang Tây Hanok</h1><p>Candidate để nghiệm thu. 6 luống/36 ô độc lập; 26 NPC,12 nhân vật,24 cosmetics giữ nguyên. Chưa có phê duyệt mỹ thuật cuối.</p><p><a href="../play/">Chơi candidate</a> · <a href="../play/?qa&entry=west-house-local&native&collisionDebug">Kiểm tra Tây Hanok</a> · <a href="QA_SUMMARY.json">Bằng chứng trạng thái</a> · <a href="QA.md">QA/WARN/NOT TESTED</a></p><h2>Trước/sau — ảnh native riêng, preview dưới1MB</h2><div class="grid">'''
for name in full:html+=f'<article><h3>{name}</h3><a href="{name}-native.png"><img src="{name}-review.jpg"></a><p><a href="{name}-native.png">Native1:1PNG</a></p></article>'
html+='</div><h2>Chuỗi ô trồng — crop1:1 từ Phaser, hiển thị3× nearest</h2><div class="grid">'
for v in q['captures']:html+=f'<article><h3>{v["name"]}</h3><a href="{v["name"]}-crop-1x.png"><img class="pixel" src="{v["name"]}-crop-1x.png"></a></article>'
html+='</div><h2>Hành lá —90giây thật</h2><div class="grid">'
for v in sc['stages']:html+=f'<article><h3>{v["frame"]}</h3><img class="pixel" src="scallion-{v["frame"]}-crop-1x.png"></article>'
html+='</div><h2>Video gameplay thật, không có âm thanh</h2>'
for v in videos:html+=f'<h3>{v["file"]}</h3><video controls muted preload="metadata" src="{v["file"]}"></video>'
html+='''<p>PNG native là bằng chứng pixel; videoH264 chỉ để xem chuyển động. Android/iPhone/GPU vật lý: NOT TESTED. Forge native QC giữ nguyên FAIL tiny seed/sprout và WARN safe margin; không gọi technicalPASS là phê duyệt art.</p></html>''';(A/'index.html').write_text(html)
print('Review assets bytes',sum(p.stat().st_size for p in A.rglob('*')if p.is_file()),'nativePixels',pixels)
