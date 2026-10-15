"""Process retained imagegen strips; NEVER generates art or calls a provider.

The creator skill's assembler is exercised as a diagnostic, but its per-frame
bbox fitting is unsuitable for Juni's rectangular cells. This adapter keys with
Forge, uses the creator skill component ownership without dropping detached pieces, keeps one scale per strip,
and registers the torso horizontally while retaining the shared vertical plane.
No character geometry, pose, mirrored limb, or in-between is drawn by code.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets-src/juni-animation'
FORGE = Path(os.environ.get('SPRITE_FORGE_ROOT', '/workspace/tooling-cache/agent-sprite-forge'))
CREATOR = Path(os.environ.get('CHARACTER_CREATOR_ROOT', '/workspace/tooling-cache/character-animation-creator-skill'))
V = FORGE / 'skills/video2dsprite/scripts'
G = FORGE / 'skills/generate2dsprite/scripts'
LOG_PATH = SRC / 'processing-commands.json'
LOG = json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def run(*args, allow_failure=False):
    command = [str(a) for a in args]
    p = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                       env=dict(os.environ, FORGE_MAX_PAID_REQUESTS='0'))
    LOG.append({'command': command, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
    write(SRC / 'processing-commands.json', LOG)
    if p.returncode and not allow_failure:
        raise RuntimeError(f'{command}: {p.stderr[-1500:]} {p.stdout[-1500:]}')
    return p


def owned_poses(image, count):
    """Use the actual creator component segmenter without its bbox rescaling.

    All components including tiny detached earrings/curls are retained and owned
    by the nearest primary body. Empty vertical cuts would intersect wide shoes.
    """
    spec = importlib.util.spec_from_file_location('creator_assembler', CREATOR/'scripts/assemble_action_sheet.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    components = module.components(image, 16)
    seeds = sorted(sorted(components, key=lambda c: c['area'], reverse=True)[:count], key=lambda c: c['center_x'])
    if len(seeds) != count or min(c['area'] for c in seeds) < max(c['area'] for c in seeds) * .18:
        raise ValueError(f'Expected {count} full isolated bodies; component ownership is ambiguous')
    groups = [[seed] for seed in seeds]
    for comp in components:
        if any(comp is seed for seed in seeds):
            continue
        nearest = min(range(count), key=lambda i: abs(seeds[i]['center_x']-comp['center_x']))
        groups[nearest].append(comp)
    src = np.array(image).reshape(-1, 4)
    result = []
    for group in groups:
        pixels = np.zeros_like(src)
        for component in group:
            pixels[component['pixels']] = src[component['pixels']]
        result.append(Image.fromarray(pixels.reshape(image.height, image.width, 4)))
    return result


def process_one(record):
    name = f"{record['action']}-{record['direction']}"
    source = SRC / 'source' / f'{name}.png'
    if not source.exists():
        raise FileNotFoundError(source)
    cache = ROOT / '.cache/juni-animation' / f'{name}-{sha(source)[:12]}-v4'
    cache.mkdir(parents=True, exist_ok=True)
    raw = cache / 'raw'
    raw.mkdir(exist_ok=True)
    shutil.copyfile(source, raw / 'raw_0000.png')
    clean = cache / 'clean'
    if not clean.exists():
        run(sys.executable, V / 'video2dsprite.py', 'clean', '--raw-dir', raw,
            '--output-dir', clean, '--key', '#00ff00', '--key-mode', 'always',
            '--matte', 'soft', '--despill-mode', 'edge', '--pockets', 'remove', '--workers', '1')
    image = Image.open(clean / 'clean_0000.png').convert('RGBA')
    owned = owned_poses(image, record['frames'])
    poses = []
    for crop in owned:
        box = crop.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
        if not box:
            raise ValueError('Empty pose')
        top = box[1] + round((box[3] - box[1]) * .53)
        bottom = box[1] + round((box[3] - box[1]) * .68)
        pixels = np.array(crop)[top:bottom].astype(float)
        navy = (pixels[:,:,0]<110) & (pixels[:,:,2]>pixels[:,:,0]+5) & (pixels[:,:,2]>pixels[:,:,1]+2)
        weights = (pixels[:,:,3]*navy).sum(axis=0)
        if weights.sum()<200: raise ValueError('Cannot identify approved navy waistband/hip mass')
        center = float((weights * np.arange(image.width)).sum() / weights.sum())
        poses.append({'bbox': list(box), 'torso_x': center})
    reg = cache / 'registered'
    reg.mkdir(exist_ok=True)
    width = max(512, max(p['bbox'][2]-p['bbox'][0] for p in poses) + 160)
    for i, (pose, owned_image) in enumerate(zip(poses, owned)):
        canvas = Image.new('RGBA', (width, image.height))
        left, _, right, _ = pose['bbox']
        canvas.alpha_composite(owned_image.crop((left, 0, right, image.height)),
                               (round(width/2 - (pose['torso_x']-left)), 0))
        canvas.save(reg / f'frame_{i:04}.png')
    write(cache / 'registration.json', {'source_sha256': sha(source), 'source_size': image.size,
         'method': 'Actual creator component ownership with all detached parts retained; navy upper-hip mass x registration, no arm-dependent centroid; original common y plane; one clip scale, no frame bbox fitting or mirroring.',
         'poses': poses})
    finish = cache / 'finish'
    if not finish.exists():
        run(sys.executable, V / 'finish_frames.py', 'hd', '--frames', reg,
            '--output-dir', finish, '--target-height', '80', '--canvas', '96x112',
            '--canvas-anchor', '48,100', '--character', 'juni-approved', '--role', 'hero',
            '--clip', name, '--loop-policy', 'cycle' if record['action'] in ['idle','walk','run'] else 'oneshot')
    # Forge's default rest-frame stance can be one advanced foot. Correct that
    # source-root offset with ONE integer x translation of the entire clip;
    # never pin individual moving feet, rescale a frame, or erase flight/bob.
    frames = sorted((finish/'frames').glob('*.png'))
    first = np.array(Image.open(frames[0]).convert('RGBA')).astype(float)
    band=first[58:74];navy=(band[:,:,0]<110)&(band[:,:,2]>band[:,:,0]+5)&(band[:,:,2]>band[:,:,1]+2)
    w=(band[:,:,3]*navy).sum(axis=0); assert w.sum()>0
    shift=round(48-float((w*np.arange(96)).sum()/w.sum()))
    registered=cache/'native-root';registered.mkdir(exist_ok=True)
    for f in frames:
        im=Image.open(f).convert('RGBA');canvas=Image.new('RGBA',(96,112));canvas.alpha_composite(im,(shift,0))
        assert sum(im.getchannel('A').get_flattened_data())==sum(canvas.getchannel('A').get_flattened_data()),'Clipped root registration'
        canvas.save(registered/f.name)
    write(cache/'root-correction.json',{'translation_px':[shift,0],'scope':'one fixed whole-clip integer translation, no scale/y/frame-dependent change','source':'Forge finished frames; original finish.json/frames retained','root':[48,100]})
    return name, registered, cache


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', help='diagnostic subset, comma separated action-direction IDs')
    parser.add_argument('--finish', action='store_true', help='Build shared palette, native source, Forge clips and engine export after all sources exist')
    args = parser.parse_args()
    manifest = json.loads((SRC / 'run-manifest.json').read_text())
    wanted = set(args.only.split(',')) if args.only else None
    finished = []
    for record in manifest['strips']:
        name = f"{record['action']}-{record['direction']}"
        if wanted and name not in wanted:
            continue
        finished.append(process_one(record))
        print('Processed', name, flush=True)
    write(SRC / 'registration.json', {name: json.loads((cache/'registration.json').read_text()) for name, _, cache in finished})
    if not args.finish:
        return
    if wanted:
        raise ValueError('--finish requires the whole set')
    cache = ROOT / '.cache/juni-animation/final'
    cache.mkdir(exist_ok=True)
    inputs = cache / 'inputs'
    inputs.mkdir(exist_ok=True)
    for name, folder, _ in finished:
        for i, f in enumerate(sorted(folder.glob('*.png'))):
            shutil.copyfile(f, inputs / f'{name}-{i:02}.png')
    palette = cache / 'palette'
    if not palette.exists():
        run(sys.executable, G/'palette_tool.py', 'build', '--input', inputs,
            '--base', ROOT/'assets-src/character-reboot/B/native/palette.json',
            '--colors', '64', '--output-dir', palette)
    applied = cache / 'applied'
    if not applied.exists():
        run(sys.executable, G/'palette_tool.py', 'apply', '--input', inputs,
            '--palette', palette/'palette.json', '--output-dir', applied,
            '--alpha-threshold', '128', '--orphans', '0')
    shutil.copyfile(palette/'palette.json', SRC/'palette.json')
    native = SRC / 'native'
    native.mkdir(exist_ok=True)
    for f in sorted(applied.glob('*.png')):
        shutil.copyfile(f, native/f.name)
    print('Native frames', len(list(native.glob('*.png'))))
    frames, clips, durations = [], {}, {}
    views = {'south': 'front', 'north': 'back', 'west': 'left', 'east': 'right'}
    times = {'idle': [1600,260,80,100,160,800], 'start':[50,50,60], 'stop':[65,65,90],
             'wave':[100,90,90,110,110,110,100,150],
             'celebrate':[100,80,80,100,120,80,100,160],
             'social':[180,170,180,150,150,200,150,180]}
    ticks_by_action = {a:[round(v*60/1000) for v in values] for a,values in times.items()}
    for a,ticks in ticks_by_action.items():
        boundaries = [round(sum(ticks[:i])*1000/60) for i in range(len(ticks)+1)]
        times[a] = [b-a for a,b in zip(boundaries,boundaries[1:])]
    for record in manifest['strips']:
        action, direction, n = record['action'], record['direction'], record['frames']
        names = []
        for i in range(n):
            if action == 'turn': name = f'turn-{i}'
            elif action == 'transition': name = f"{'start' if i<3 else 'stop'}-{views[direction]}-{i%3}"
            else: name = f'{action}-{views[direction]}-{i}'
            frames.append({'name':name, 'file':f'native/{action}-{direction}-{i:02}.png'})
            names.append(name)
        if action == 'transition':
            for label, ids in [('start',names[:3]),('stop',names[3:])]:
                clips[f'{label}-{views[direction]}'] = {'frames':ids,'ticks':ticks_by_action[label],'loop_policy':'oneshot','role':'player'}
        else:
            label = action if action=='turn' else f'{action}-{views[direction]}'
            clip = {'frames': names, 'loop_policy':'cycle' if action in ['idle','walk','run'] else 'oneshot', 'role':'player'}
            if action in ['walk','run']:
                clip.update(ticks=[6,5,6,5,6,5,6,5] if action=='walk' else [5,5,5,4,5,5,5,4],
                            stride_world_units=44 if action=='walk' else 64, speed_ref=60 if action=='walk' else 100,
                            events=[{'at':0,'name':'step_l'},{'at':4,'name':'step_r'}])
            elif action=='turn': clip['ticks'] = 3
            else: clip['ticks'] = ticks_by_action[action]
            clips[label] = clip
    spec={'schema':'generate2dsprite.animation_clips.v2','frames':frames,'clips':clips,
          'anchor_px':[48,100],'art_source':'host_image','placeholder':False,'pixel_art':True,
          'sampling':'nearest','body_height_px':80,'palette_ref':'palette.json',
          'states':{'idle':'idle-front','moving':'walk-front','running':'run-front'}}
    write(SRC/'clips-input.json',spec)
    built=cache/'clips'
    if not built.exists():
        run(sys.executable,G/'build_animation_clips.py','--manifest',SRC/'clips-input.json',
            '--output-dir',built,'--preview-scale','2','--preview-background','checker')
    engine=cache/'engine'
    if not engine.exists():
        run(sys.executable,G/'export_engine.py','--clips',built/'animation-clips.json',
            '--target','aseprite-json','--name','juni','--output-dir',engine,'--sampling','nearest')
    write(SRC/'runtime.json',{'frameCount':len(frames),'bodyHeight':80,'cell':[96,112],'anchor':[48,100],
          'strides':{'walk':44,'run':64},'durations':times,'sourceClips':list(clips),
          'nativeFrames':frames,'identity':'Approved Juni, unchanged design; original imagegen action strips, not code animation or mirroring.'})
    shutil.copyfile(built/'animation-clips.json',SRC/'animation-clips.json')
    run(sys.executable, ROOT/'tools/export_juni_animation.py')
    print('Built/exported',len(frames),'frames,',len(clips),'clips; engine files', [p.name for p in engine.iterdir()])


if __name__ == '__main__':
    main()
