"""Offline source/atlas/pose integrity checks; does not generate or approve art."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/juni-animation'
D=R/'public/assets/juni'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=read(S/'run-manifest.json');runtime=read(S/'runtime.json');atlas=read(D/'juni.json')
assert len(m['strips'])==20 and m['generation']['actual_host_calls']>=20
assert m['generation']['procedural'] is False and m['generation']['paid_provider_routes'] is False
for row in m['strips']:
    assert sha(S/row['source_path'])==row['source_sha256']
    assert row['method']=='imagegen' and row['status']=='generated'
    assert (S/row['prompt_path']).is_file()
assert runtime['frameCount']==len(atlas['frames'])==144
assert runtime['cell']==[96,112] and runtime['anchor']==[48,100]
image=Image.open(D/'juni.png').convert('RGBA');colors=set();checks=[]
for frame in runtime['nativeFrames']:
    native=Image.open(S/frame['file']).convert('RGBA');assert native.size==(96,112)
    box=native.getbbox();assert box and min(box[:2])>=2 and box[2]<=94 and box[3]<=110,frame['name']
    assert set(native.getchannel('A').get_flattened_data())<={0,255},frame['name']
    colors.update(c[:3] for c in native.get_flattened_data() if c[3])
    b=atlas['frames'][frame['name']]['frame'];pixels=image.crop((b['x'],b['y'],b['x']+b['w'],b['y']+b['h']))
    assert not ImageChops.difference(native,pixels).getbbox(alpha_only=False),frame['name']
assert len(colors)<=64
for action in ['walk','run']:
    for direction in ['south','north','west','east']:
        paths=[S/'native'/f'{action}-{direction}-{i:02}.png' for i in range(8)]
        assert len({sha(p) for p in paths})==8,(action,direction)
        # Aligning/translation of one rigid source cannot satisfy changing local
        # limb silhouettes. Compare the registered lower-body pixel regions too.
        diffs=[]
        for a,b in zip(paths,paths[1:]+paths[:1]):
            d=ImageChops.difference(Image.open(a),Image.open(b)).convert('RGB').crop((0,64,96,108))
            changed=sum(1 for p in d.get_flattened_data() if max(p)>0);diffs.append(changed)
        assert min(diffs)>8,(action,direction,diffs)
        checks.append({'action':action,'direction':direction,'unique':8,'lower_body_changed_pixels':diffs})
report={'status':'PASS','source_strips':20,'host_image_calls':m['generation']['actual_host_calls'],'runtime_frames':144,'cell':[96,112],'anchor':[48,100],
        'palette_colors':len(colors),'binary_alpha':True,'source_atlas_equal':True,'gaits':checks,
        'notProven':['Visual appeal, identity/anatomy, planted-foot contact and loop quality require real visual review; hashes and differences are not artistic approval.']}
print(json.dumps(report))
