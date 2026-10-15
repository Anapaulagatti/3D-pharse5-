"""Lossless frame-name adapter for the actual Forge Aseprite export."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageChops

R = Path(__file__).resolve().parents[1]
S = R/'assets-src/juni-animation'
E = R/'.cache/juni-animation/final/engine'
D = R/'public/review/juni-animation'
D.mkdir(parents=True, exist_ok=True)
runtime = json.loads((S/'runtime.json').read_text())
export = json.loads((E/'aseprite/juni.json').read_text())
image = Image.open(E/'aseprite/juni.png').convert('RGBA')
frames = {}
for i, source in enumerate(runtime['nativeFrames']):
    f = export['frames'][i]
    assert f['filename'] == str(i) and not f['trimmed'] and not f['rotated']
    b = f['frame']
    pixels = image.crop((b['x'], b['y'], b['x']+b['w'], b['y']+b['h']))
    native = Image.open(S/source['file']).convert('RGBA')
    assert not ImageChops.difference(pixels, native).getbbox(alpha_only=False), source['name']
    frames[source['name']] = {k:v for k,v in f.items() if k!='filename'}
assert len(frames) == runtime['frameCount'] == 144
shutil.copyfile(E/'aseprite/juni.png', D/'juni.png')
shutil.copyfile(E/'aseprite/juni.json', D/'juni-aseprite.json')
(D/'juni.json').write_text(json.dumps({'frames':frames, 'meta':dict(export['meta'], image='juni.png')}, indent=2)+'\n')
shutil.copyfile(E/'engine-export.json', S/'engine-export.json')
report = {'status':'PASS','method':'Actual Forge export PNG retained byte-for-byte; Aseprite numeric keys renamed only. Every exported96x112 frame compared against canonical native source, zero differing pixels.',
          'frames':len(frames),'sourcePNG_sha256':hashlib.sha256((D/'juni.png').read_bytes()).hexdigest(),
          'cell':runtime['cell'],'anchor':runtime['anchor'],'phaser_import':'Verified separately in actual browser, not inferred from this structural check.'}
(S/'runtime-export.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
