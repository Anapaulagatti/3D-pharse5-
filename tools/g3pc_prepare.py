from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/palace-cleanup-v1'
m=json.loads((R/'public/assets/gate3/west-hanok-world/manifest.json').read_text());W,H=m['size']
lock={'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'manifest':m,'files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for root in ['assets-src','public'] for p in sorted((R/root).rglob('*')) if p.is_file() and 'palace-cleanup' not in str(p)}}
if not (S/'baseline-lock.json').exists():(S/'baseline-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
else:lock=json.loads((S/'baseline-lock.json').read_text());m=lock['manifest']
polys={'axis':[(1855,1080),(2180,1080),(2180,1740),(2160,1830),(1935,1830),(1935,1740),(1855,1740)],'axis-gateway':[(1790,1460),(2200,1460),(2200,1660),(1790,1660)],'right-access':[(2110,1431),(2650,1431),(2650,1494),(2110,1494)],'facade-left':[(1510,628),(1610,628),(1610,685),(1510,685)],'facade-right':[(2095,635),(2190,635),(2190,750),(2095,750)]}
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
for poly in polys.values():d.polygon(poly,fill=255)
# Existing transverse public lane is protected through the new axis.
d.rectangle((1855,1370,1984,1437),fill=0)
mask.save(S/'edit-scope-mask.png');g=Image.new('RGBA',(W,H))
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
for o in sorted(m['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
g.crop((1400,320,2936,1856)).save(S/'before-authoring-context.png');im=g.crop((1400,320,2936,1856));d=ImageDraw.Draw(im)
for name,poly in polys.items():p=[(x-1400,y-320)for x,y in poly];d.line(p+[p[0]],fill='#ff38b0',width=2);d.text(p[0],name,fill='white',stroke_fill='black',stroke_width=1)
d.line([(648,430),(648,1510)],fill='#33ffff',width=1);im.save(S/'exact-edit-guide.png')
(S/'scope.json').write_text(json.dumps({'origin':[1400,320],'size':[1536,1536],'polygons':polys,'ceremonialAxisX':2048,'doorThresholdY':685,'houseFrontAxisX':2600,'publicBranchY':1460,'protected':'All pixels outside polygons; western approved house/garden, station, bridges, original source and Juni. Roofs/building footprints unchanged.'},indent=2)+'\n')
print(len(lock['files']))
