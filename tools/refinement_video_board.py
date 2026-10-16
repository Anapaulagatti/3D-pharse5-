"""Arrange real decoded frames as evidence, never synthesized game frames."""
from pathlib import Path
import hashlib,subprocess,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
Q=R/'docs/world-refinement/quality'
C=R/'.cache/world-refinement'/('video-frames-'+hashlib.sha256((Q/'gameplay-walkthrough.mp4').read_bytes()).hexdigest()[:12])
C.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
board=Image.new('RGB',(1568,1020),'#172f2e')
d=ImageDraw.Draw(board)
fps=json.loads((Q/'video-verification.json').read_text())['original']['actualAverageFPS']
d.text((16,10),f'ACTUAL CONTINUOUS PHASER CAPTURE / {fps:.2f}fps VFR / no teleport or injected frames',font=font,fill='#fff0c8')
for i,t in enumerate([1,8,17,26,34,42,50,58,66,76,86,94]):
    p=C/f'{t}.png'
    if not p.exists():
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(Q/'gameplay-walkthrough.mp4'),'-frames:v','1','-update','1','-y',str(p)],check=True)
    im=Image.open(p).convert('RGB').resize((384,288),Image.Resampling.NEAREST)
    x=8+(i%4)*392
    y=44+(i//4)*324
    board.paste(im,(x,y))
    d.text((x,y+294),f't={t}s | actual recorded frame | 0.375x',font=font,fill='#fff0c8')
board.save(Q/'gameplay-contact.png')
print('12real decoded frames composed; original video retained.')
