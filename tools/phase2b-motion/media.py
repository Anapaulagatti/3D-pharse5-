"""Review evidence: source-only previews kept distinct from actual Phaser samples."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,io,math
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';IDS=['sori','jiwon','nari','taeyang','yuna','hyunwoo'];BASE=json.loads((D/'before-manifest.json').read_text())['commit'];clips=[a+'-'+v for a in ['walk','run']for v in ['front','back','right']]
def cell(a,m,key):
 f=m[key]['frame'];return a.crop((f['x'],f['y'],f['x']+96,f['y']+112))
def encode(frames,out,fps):
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{frames[0].width}x{frames[0].height}','-framerate',str(fps),'-i','-','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for frame in frames:p.stdin.write(frame.convert('RGB').tobytes())
 p.stdin.close();assert p.wait()==0
records=[]
for id in IDS:
 stem=f'public/assets/characters/{id}/atlas';m=json.loads((R/(stem+'.json')).read_text())['frames'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',BASE+':'+stem+'.png']))).convert('RGBA');new=Image.open(R/(stem+'.png')).convert('RGBA');guide=json.loads((R/f'assets-src/characters/phase2b-motion/{id}/motion-guide.json').read_text());guide={r['frame']:r for r in guide['poses']}
 for action in ['walk','run']:
  board=Image.new('RGB',(768,792),(28,30,38));dr=ImageDraw.Draw(board)
  for v,view in enumerate(['front','back','right']):
   for row,(label,atlas)in enumerate([('BEFORE source',old),('AFTER source',new)]):
    for i in range(8):
     xy=(i*96,(v*2+row)*132+20);im=cell(atlas,m,f'{action}-{view}-{i}');board.paste(im,xy,im);dr.text((xy[0]+2,xy[1]-17),f'{view}{i} {label}',fill='white')
  board.save(D/f'{id}-{action}-before-after-native.png')
 for clip in clips:
  anim=[]
  for i in range(8):
   panel=Image.new('RGB',(288,244),(28,30,38));dr=ImageDraw.Draw(panel);dr.text((6,4),f'{id} {clip} | SOURCE ONLY',fill='white');dr.text((10,22),'BEFORE',fill='white');dr.text((154,22),'AFTER',fill='white')
   for j,a in enumerate([old,new]):
    im=cell(a,m,f'{clip}-{i}');panel.paste(im,(24+j*144,60),im)
   dr.text((8,204),f'phase {i}/7 - loop x3',fill='white');anim.append(panel)
  anim[0].save(D/f'{id}-{clip}-source-before-after.gif',save_all=True,append_images=anim[1:],duration=92 if clip.startswith('walk')else 80,loop=2,disposal=2)
  # Original-resolution annotations: joint/sole guide overlays are NOT screenshots.
  board=Image.new('RGB',(768,152),(28,30,38));dr=ImageDraw.Draw(board)
  for i in range(8):
   key=f'{clip}-{i}';im=cell(new,m,key);board.paste(im,(i*96,24),im);land=guide[key]['landmarks'];dr.text((i*96+2,2),f'{i} guide',fill='white')
   for p in land:
    color=(90,220,250)if p['side']=='L'else(255,186,90);x,y=p.get('sole',p.get('ankle'));x+=i*96;y+=24;dr.ellipse((x-2,y-2,x+2,y+2),outline=color);dr.text((x-7,y+4),p['side'],fill=color)
  board.save(D/f'{id}-{clip}-foot-guide-native.png')
 # Phase-aligned game images, not a second animation engine or claimed raw video.
 frames=[]
 for clip in clips:
  jdata=json.loads((D/'juni-gameplay.json').read_text());ndata=json.loads((D/f'{id}-gameplay.json').read_text());jr=next(r for r in jdata['rows']if r['clip']==clip);nr=next(r for r in ndata['rows']if r['clip']==clip)
  for sampleNumber,(j,n) in enumerate(zip(jr['samples'],nr['samples'])):
   assert(j['loop'],j['index'])==(n['loop'],n['index']);panel=Image.new('RGB',(384,272),(28,30,38));dr=ImageDraw.Draw(panel)
   for col,who in enumerate(['juni',id]):
    im=Image.open(D/f'{who}-{clip}-loop{j["loop"]}-{j["index"]}-context-native.png');panel.paste(im,(col*192,32));dr.text((col*192+4,16),who,fill='white')
   dr.text((4,2),f'PHASER {clip} cycle {j["loop"]+1}/3 phase {j["index"]}',fill='white');dr.text((4,258),'phase-aligned captures | normal gait timing',fill='white')
   step=60*((44/60/8)if clip.startswith('walk')else(64/100/8))
   frames.extend([panel]*(round((sampleNumber+1)*step)-round(sampleNumber*step)))
 encode(frames,D/f'juni-vs-{id}-synchronized-phaser.mp4',60)
 # Full unretimed browser recording; exact1280x1000, no crop/scale, no speed change.
 out=D/f'{id}-actual-gameplay.mp4';subprocess.run(['ffmpeg','-v','error','-y','-i',str(D/f'{id}-actual-gameplay.webm'),'-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 records.append({'id':id,'comparison':f'juni-vs-{id}-synchronized-phaser.mp4','method':'Actual native context crops from three consecutive captured cycles; Juni and actor aligned by original index0..7, displayed at nominal44/60 or64/100 seconds/cycle. This is phase-aligned evidence, NOT an unretimed simultaneous gameplay recording.','actual':out.name,'raw':'Uncut/unretimed1280x1000 browser gameplay recording, real input and canonical world; review spawn reload between clips. Lossy MP4 for access; lossless native PNG is pixel-fidelity authority.','clips':clips})
 print(id,'native source comparisons,6 animated previews,6 foot guides, synchronous Phaser video, unretimed gameplay',flush=True)
(D/'media-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
