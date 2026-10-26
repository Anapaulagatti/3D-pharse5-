"""Phase2A native own-layer production extended only into the Phase2B namespace."""
from pathlib import Path
import importlib.util,sys,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2b';D=R/'docs/phase2b'
spec=importlib.util.spec_from_file_location('approved_native_authoring',R/'tools/phase2a/art.py')
art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art);art.S=S;art.D=D
IDS=['sori','jiwon','nari','taeyang','yuna','hyunwoo']
def opposing_profile(parts,cfg,phase,action='walk'):
    """New identities only: near arm opposes the near leg, not the same phase.
    Accepted original tooling/art remains untouched. Lower-limb IK and root are
    reused; only the extracted native forearm is projected with opposite phase.
    """
    import animate,math
    # The preserved function draws limbs/body; supply no forearms for that pass.
    out=approved_profile({k:v for k,v in parts.items()if 'forearm'not in k},cfg,phase,action)
    t=phase*math.tau;run=action=='run';bob=round(-abs(math.sin(t))*(2 if run else 1))
    if action=='idle':bob=-round((1-math.cos(t))/2)
    for side in ['L','R']:
        if side+'forearm'not in parts:continue
        a,b,c=cfg['arms'][side];swing=-math.cos(t+(0 if side=='L'else math.pi))
        elbow=[b[0],b[1]+bob];wrist=[c[0]+round(swing*(7 if run else 4)),c[1]+bob-round(abs(swing)*2)]
        if action=='idle':wrist=[c[0],c[1]+bob]
        art.bone(out,parts[side+'forearm'],b,c,elbow,wrist)
    return out
import animate
approved_profile=animate.render_side
animate.render_side=opposing_profile
def build(id):
    assert id in IDS
    art.prepare(id);art.rig(id)
    cfg=json.loads((S/id/'rig.json').read_text());im=Image.open(S/id/'native/front.png').convert('RGBA');parts={n:art.layer(im,poly)for n,poly in cfg['front']['masks'].items()}
    poses=[art.front(parts,cfg['front'],p)for p in art.T['walk-front']]
    assert len({q.tobytes()for q in poses})==8
    for q in poses:
        bb=q.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112
    board=Image.new('RGBA',(768,112),(29,28,36,255))
    for i,q in enumerate(poses):board.alpha_composite(q,(96*i,0))
    board.save(D/f'{id}-first-walk-native.png')
    (S/id/'first-walk-gate.json').write_text(json.dumps({'identity':id,'distinctFrames':8,'native':[96,112],'anchor':[48,100],'motion':'Exact same-index approved Juni front-walk landmarks','sourceSHA256':hashlib.sha256((S/id/'turnaround-source.png').read_bytes()).hexdigest(),'stage':'Native first-walk bounds/phase validation before full pack export; actual Phaser gate still required'},indent=2)+'\n')
    art.finish(id)
if __name__=='__main__':build(sys.argv[1])
