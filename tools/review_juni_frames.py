"""Run actual creator QA/preview scripts on padded, unscaled native frames."""
from pathlib import Path
import json
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/juni-animation'; D=R/'docs/juni-animation'
T=Path(os.environ.get('CHARACTER_CREATOR_ROOT','/workspace/tooling-cache/character-animation-creator-skill'))/'scripts'
C=R/'.cache/juni-animation/creator-qa';C.mkdir(exist_ok=True)
commands=[]
def run(*args):
    p=subprocess.run([str(a)for a in args],cwd=R,text=True,capture_output=True)
    commands.append({'command':[str(a)for a in args],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    (D/'creator-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    return p

for action in ['walk','run','idle','transition','wave','celebrate','social','turn']:
    dirs=['south','north','west','east'] if action in ['walk','run','idle','transition'] else ['south']
    n=6 if action in ['idle','transition'] else 8
    sheet=Image.new('RGBA',(n*112,len(dirs)*112))
    for y,direction in enumerate(dirs):
        for i in range(n):
            sheet.alpha_composite(Image.open(S/'native'/f'{action}-{direction}-{i:02}.png'),(i*112+8,y*112))
    path=C/f'{action}.png';sheet.save(path)
    run(sys.executable,T/'validate_sheet.py','--input',path,'--rows',len(dirs),'--columns',n,
        '--cell',112,'--row-names',','.join(dirs),'--fail-on-warnings',
        '--json-out',D/f'{action}-geometry.json','--contact-sheet',C/f'{action}-contact.png')
    if action in ['walk','run']:
        run(sys.executable,T/'audit_sprite_motion.py','--input',path,'--rows',len(dirs),'--columns',n,
            '--cell',112,'--row-names',','.join(dirs),'--fail-on-warnings','--json-out',D/f'{action}-motion.json')
    if action in ['walk','run','idle']:
        run(sys.executable,T/'export_animation_previews.py','--atlas',path,'--rows',len(dirs),
            '--columns',n,'--cell',112,'--row-names',','.join(dirs),'--scale',2,
            '--duration',92 if action=='walk' else 80 if action=='run' else 180,
            '--prefix',action,'--out-dir',D/'previews')

# Every pose at its exact native resolution on a labelled light/dark contact
# board. The board is review material, never a replacement runtime texture.
manifest=json.loads((S/'run-manifest.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
board=Image.new('RGB',(1130,100+len(manifest['strips'])*132),'#eee8da');draw=ImageDraw.Draw(board)
draw.text((20,14),'JUNI / GENERATED ACTION FRAMES — NATIVE 1x',font=font,fill='#263f3a')
draw.text((20,43),'Original reference-imagegen poses; fixed96x112 cell, shared root48,100; no mirrors or procedural limbs.',font=small,fill='#52615b')
draw.text((20,65),'Idle timing/gesture holds are authored separately; this contact sheet does not claim runtime timing or artistic approval.',font=small,fill='#52615b')
for row,record in enumerate(manifest['strips']):
    y=100+row*132;action=record['action'];direction=record['direction']
    draw.text((10,y+24),f'{action} / {direction}',font=small,fill='#263f3a')
    for i in range(record['frames']):
        x=210+i*112;draw.rectangle((x,y,x+103,y+113),fill='#303540'if row%2 else'#d9d1bf')
        im=Image.open(S/'native'/f'{action}-{direction}-{i:02}.png').convert('RGBA')
        board.paste(im,(x+4,y),im);draw.text((x+44,y+116),str(i),font=small,fill='#52615b')
board.save(D/'sprite-contact-sheet.png')
print(json.dumps({'geometry_reports':8,'motion_reports':2,'command_failures':[x['command'] for x in commands if x['exit']],'board':str(D/'sprite-contact-sheet.png')}))
