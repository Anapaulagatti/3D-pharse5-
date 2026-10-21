"""Honest engine-image crops/annotations; never used for map authoring."""
from map_pipeline import *
from PIL import Image,ImageDraw,ImageFont
import io,shutil
Q=ROOT/'docs/v9-world';native=Image.open(Q/'quality/final/V9_FULL_WORLD_OVERVIEW.png').convert('RGB');assert native.size==(4352,6144)
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
# Nearest thumbnail is labeled as a reduced preview, never native gameplay proof.
native.resize((1088,1536),Image.Resampling.NEAREST).save(Q/'V9_WEB_OVERVIEW.png')
regions={'CITY_STREETS':[704,2240,2832,3472],'NAMSAN':[2832,2240,4352,3472],'STATION':[704,3376,2640,4256],'ENTERTAINMENT':[2784,3408,4256,4672],'WATERFRONT':[1856,4256,2896,5008],'JEJU':[480,4928,2448,6144]}
for k,box in regions.items():native.crop(box).save(Q/f'V9_{k}.png')
# V8 is read from its verified archive ONLY after V9 production. No planner imports this module.
tag='recovery/before-v9-total-southern-reset-20261021';path='docs/v8-city/FINAL_WORLD_OVERVIEW_NATIVE.png';data=subprocess.check_output(['git','show',tag+':'+path],cwd=ROOT);before=Image.open(io.BytesIO(data)).convert('RGB');assert before.size==(4352,5312)
board=Image.new('RGB',(2176,1656),'#142b37');d=ImageDraw.Draw(board)
d.text((24,18),'V8 · REJECTED',font=font(30),fill='#f7c7ae');d.text((1112,18),'V9 · CANDIDATE FOR USER REVIEW',font=font(30),fill='#c0f1d2')
board.paste(before.resize((1088,1328),Image.Resampling.NEAREST),(0,80));board.paste(native.resize((1088,1536),Image.Resampling.NEAREST),(1088,80))
d=ImageDraw.Draw(board)
for x in [0,1088]:d.line((x,80+560,x+1088,80+560),fill='#f3cf7f',width=2)
d.text((16,1424),'V8 canvas ends at y5312. Dark area is padding, not terrain.',font=font(20),fill='#d4dee0');d.text((16,1620),'Same world-pixel scale 1:4; y2240 fixed north boundary. No map stretching, tracing or perspective warp.',font=font(20),fill='white');board.save(Q/'V8_V9_REAL_DIFFERENCE.png')
write(Q/'quality/comparison-provenance.json',{'method':'Two actual-engine images at identical1:4world-pixel scale, common frame0..6144; shorter V8 padded explicitly, no geometry warp.','before':{'tag':tag,'path':path,'sha256':hashlib.sha256(data).hexdigest(),'size':list(before.size)},'after':{'path':'quality/final/V9_FULL_WORLD_OVERVIEW.png','sha256':sha(Q/'quality/final/V9_FULL_WORLD_OVERVIEW.png'),'size':list(native.size)},'nativeDistrictCrops':regions,'web':'Nearest4:1 preview; inspect native PNG/gameplay crops for pixel sharpness'})
# Annotated actual world: tested route centerlines and property entrances, not an art concept.
nav=Image.new('RGB',(2176,3168),'#142b37');nav.paste(native.resize((2176,3072),Image.Resampling.NEAREST),(0,96));d=ImageDraw.Draw(nav);d.text((24,20),'V9 NAVIGATION · 33 INPUT-VERIFIED ROUTES',font=font(34),fill='white')
plan=json.loads((SOURCE/'plan/city.json').read_text());routes=json.loads((SOURCE/'plan/navigation-routes.json').read_text())
for r in routes:d.line([(round(x/2),round(y/2)+96)for x,y in r['points']],fill='#b9ffff',width=3)
for p in plan['plots']:
 x,y=p['entrance'];d.ellipse((x/2-5,y/2+91,x/2+5,y/2+101),fill='#fff08d')
for region in plan['districts']:
 l,t,r,b=region['bounds'];d.rectangle((l/2,t/2+96,r/2,b/2+96),outline='#eabce5',width=2);d.text((l/2+8,t/2+105),region['id'],font=font(24),fill='#fff5e3')
nav.save(Q/'V9_NAVIGATION.png')
# Only current reviewed evidence enters active docs. Baseline raw V8 remains in its recovery tag.
old=Q/'V8_BEFORE_ENGINE.png'
if old.exists():assert hashlib.sha256(old.read_bytes()).hexdigest()==hashlib.sha256(data).hexdigest();old.unlink()
shutil.copytree(ROOT/'.cache/v9-reset/final-browser/mobile',Q/'quality/mobile',dirs_exist_ok=True)
for source,name in [('.cache/v9-reset/final-browser/e2e-results.json','full-browser-results.json'),('.cache/v9-reset/occlusion/e2e-results.json','occlusion-results.json')]:shutil.copyfile(ROOT/source,Q/'quality'/name)
print('Actual engine crops, nearest web overview, honest V8/V9 comparison and navigation board saved')
