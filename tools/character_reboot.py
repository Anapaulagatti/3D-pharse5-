"""Process host-generated concept stills with real Forge tools. No generation/API calls.

Turnaround cells are static direction drawings, NEVER represented as animation.
The `approve` Forge verb normalizes geometry; it does not grant user approval.
"""
from pathlib import Path
from PIL import Image
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--forge-root', default='/workspace/tooling-cache/agent-sprite-forge')
parser.add_argument('--export-review', action='store_true', help='Export static concept candidates; never replaces game actors')
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]
FORGE = Path(args.forge_root)
SOURCE = ROOT / 'assets-src/character-reboot'
OUT = ROOT / '.cache/reboot/pipeline' / uuid.uuid4().hex[:8]
OUT.mkdir(parents=True)
commands = []

def call(skill, script, *argv, expected=(0,)):
    cmd = [sys.executable, str(FORGE/'skills'/skill/'scripts'/script), *map(str, argv)]
    env = dict(os.environ, FORGE_MAX_PAID_REQUESTS='0')
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
    commands.append(dict(argv=cmd, exit_code=p.returncode, stdout=p.stdout.strip(), stderr=p.stderr.strip()))
    (OUT/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
    if p.returncode not in expected:
        raise RuntimeError((cmd, p.stdout, p.stderr))
    return p

for key in 'ABC':
    concept = SOURCE/key
    bg = 'magenta' if key == 'A' else 'green'
    # Inspect cross-cell ownership before any lossless cell extraction.
    call('generate2dsprite', 'sheet_qc.py', 'spill', '--input', concept/'source-turnaround.png',
         '--rows', 1, '--cols', 3, '--key', bg, '--safe-margin', '0.08',
         '--output-dir', OUT/key/'spill')
    sheet = Image.open(concept/'source-turnaround.png').convert('RGBA')
    assert sheet.width % 3 == 0
    raw = OUT/key/'raw'; raw.mkdir(parents=True)
    registered = OUT/key/'registered'; registered.mkdir()
    shutil.copy2(concept/'master-front/master_rgba.png', registered/'00-front.png')
    # Native, lossless source cell extraction. Forge performs keying and framing.
    for i, direction in enumerate(['back', 'left', 'right']):
        cell = raw/(direction+'.png')
        sheet.crop((i*sheet.width//3, 0, (i+1)*sheet.width//3, sheet.height)).save(cell)
        master = OUT/key/('master-'+direction)
        call('generate2dsprite', 'master_still.py', 'approve', '--spec', concept/'spec.json',
             '--still', cell, '--route', 'host-image_gen', '--facing', direction,
             '--key', bg, '--prompt-file', concept/'turnaround.prompt.txt', '--output-dir', master)
        shutil.copy2(master/'master_rgba.png', registered/f'{i+1:02d}-{direction}.png')
    # First compare the standard pixel finish with a feature-preserving documented
    # area/quantize route. All four static directions share canvas/root/palette.
    call('video2dsprite', 'finish_frames.py', 'pixel', '--frames', registered,
         '--output-dir', OUT/key/'bold', '--target-height', 80,
         '--canvas', '80x104', '--canvas-anchor', '40,96', '--colors', 48,
         '--shade-gap', '0.025', '--contrast', 1, '--saturation', 1,
         '--character', key, '--role', 'hero', '--loop-policy', 'oneshot')
    call('video2dsprite', 'finish_frames.py', 'hd', '--frames', registered,
         '--output-dir', OUT/key/'area', '--target-height', 80,
         '--canvas', '80x104', '--canvas-anchor', '40,96',
         '--character', key, '--role', 'hero', '--loop-policy', 'oneshot')
    call('generate2dsprite', 'palette_tool.py', 'quantize-seq', '--input', OUT/key/'area/frames',
         '--output-dir', OUT/key/'features', '--colors', 40,
         '--orphans', 0, '--no-despeckle', '--loop-policy', 'oneshot')
    if args.export_review:
        call('codeart2d', 'pixel_qa.py', '--input', str(OUT/key/'features/*.png'),
             '--palette', OUT/key/'features/palette.json', '--anchor', '40,96',
             '--scales', '1,3', '--bg', 'light,dark', '--review', OUT/key/'pixel-review.png',
             '--report', OUT/key/'pixel-qa.json')
        call('video2dsprite', 'engine_export.py', 'package', '--clean-dir', OUT/key/'features',
             '--output-dir', OUT/key/'package', '--name', 'direction-stills', '--fps', 1,
             '--loop-policy', 'oneshot', '--source-size', '80,104', '--source-anchor', '40,96',
             '--formats', 'png', '--key', bg, '--pixel-art', '--sampling', 'nearest',
             '--body-height-px', 80, '--art-source', 'host_image')
        # Forge's verify verb requires an encoded transport, not a PNG-only
        # still collection. Record that limitation; do not manufacture a movie
        # of direction swaps and pass it off as approved character animation.
        if key == 'A':
            unsupported = call('video2dsprite', 'engine_export.py', 'verify', '--package', OUT/key/'package', expected=(1,))
            assert 'needs an encoded transport' in unsupported.stderr
        native = concept/'native'; native.mkdir(exist_ok=True)
        for png in (OUT/key/'features').glob('*.png'):
            shutil.copy2(png, native/png.name)
        shutil.copy2(OUT/key/'features/palette.json', native/'palette.json')
        runtime = ROOT/'public/review/characters'/key; runtime.mkdir(parents=True, exist_ok=True)
        for name in ['direction-stills-atlas-00.png','animation.json']:
            shutil.copy2(OUT/key/'package'/name, runtime/name)
        # Read the Forge-exported page and adapt only frame names to Phaser's
        # standard atlas schema. The PNG pixels are never repacked or altered.
        meta = json.loads((OUT/key/'package/animation.json').read_text())
        assert meta['sourceSize'] == [80,104] and meta['frameCount'] == 4
        atlas = Image.open(OUT/key/'package/direction-stills-atlas-00.png').convert('RGBA')
        for i, frame in enumerate(sorted(native.glob('*.png'))):
            assert atlas.crop((i*80,0,(i+1)*80,104)).tobytes() == Image.open(frame).convert('RGBA').tobytes()
        frames = {direction:{'frame':{'x':i*80,'y':0,'w':80,'h':104},
                            'rotated':False,'trimmed':False,
                            'spriteSourceSize':{'x':0,'y':0,'w':80,'h':104},
                            'sourceSize':{'w':80,'h':104}}
                  for i,direction in enumerate(['front','back','left','right'])}
        (runtime/'atlas.json').write_text(json.dumps({'frames':frames,'meta':{
            'image':'direction-stills-atlas-00.png','size':{'w':320,'h':104},'scale':'1',
            'candidate':key,'userApproval':'PENDING','kind':'four STATIC directions; no action animation'}},indent=2)+'\n')

(ROOT/'.cache/reboot/pipeline-latest.json').write_text(json.dumps({'folder':str(OUT)},indent=2)+'\n')
print(json.dumps({'folder':str(OUT),'commands':len(commands),'status':'PENDING_VISUAL_ROUTE_SELECTION'}))
