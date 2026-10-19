"""Review boards from actual engine captures, with exact native-pixel QA."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import json, hashlib
import numpy as np

R = Path(__file__).resolve().parents[1]
D = R / 'docs/v6-path-fix'
Q = D / 'quality'
font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def ft(n):
    return ImageFont.truetype(font,n)


def board(path, panels, titles, footer):
    w = max(im.width for im in panels)
    h = max(im.height for im in panels)
    out = Image.new('RGB',(len(panels)*(w+20)+20,h+130),'#17342e')
    draw = ImageDraw.Draw(out)
    for i,(im,title) in enumerate(zip(panels,titles)):
        x = 20+i*(w+20)
        draw.text((x,12),title,font=ft(19),fill='#f6e1b5')
        out.paste(im,(x,45))
    for i,line in enumerate(footer):
        draw.text((20,h+58+i*23),line,font=ft(16),fill='#dfebdb')
    out.save(path)


before = Image.open(Q/'before/full-map-native.png').convert('RGB')
after = Image.open(Q/'after/full-map-native.png').convert('RGB')
assert before.size == after.size == (4352,5312)
after.save(D/'V6_FIXED_OVERVIEW.png')
after.resize((2176,2656),Image.Resampling.NEAREST).save(D/'V6_FIXED_OVERVIEW_WEB.png')
after.resize((1088,1328),Image.Resampling.NEAREST).save(D/'V6_FIXED_OVERVIEW_SMALL.png')
board(D/'PATHS_FULL_BEFORE_AFTER.png',[before.resize((1088,1328),Image.Resampling.NEAREST),after.resize((1088,1328),Image.Resampling.NEAREST)],['BEFORE / VERIFIED V6','AFTER / PATH-ONLY FIX'],['Actual native Phaser full-world frames, integer-quarter overview.','Same4352x5312world,497placements and552colliders; native crops are separate.'])

for name,box in [
    ('museum-join',(2432,1504,2944,2144)),
    ('civic-join',(1920,1856,2432,2688)),
    ('station',(1728,2720,2816,3312)),
    ('retail-terminal',(1440,3328,3104,3808)),
    ('park',(3072,3008,4288,3664)),
    ('waterfront',(2368,3648,3104,3968)),
    ('island',(1600,4160,2944,5152)),
]:
    board(D/f'PATHS_{name.upper().replace("-","_")}_BEFORE_AFTER.png',[before.crop(box),after.crop(box)],['BEFORE / 1:1 WORLD CROP','AFTER / 1:1 WORLD CROP'],['Unscaled crops from real Phaser full-world frames; no filtering or repainting.',f'World box{box}; overview camera zoom1. Gameplay-camera PNGs in quality/after/.'])

pre = json.loads((Q/'before/captures.json').read_text())
post = json.loads((Q/'after/captures.json').read_text())
comparison = []
for renderer in ['canvas','webgl']:
    v4 = Image.open(Q/f'before/v4-{renderer}-native-1x-native.png').convert('RGB')
    v6 = Image.open(Q/f'before/v6-{renderer}-native-1x-native.png').convert('RGB')
    fixed = Image.open(Q/f'after/v6-{renderer}-native-1x-native.png').convert('RGB')
    assert ImageChops.difference(v4,v6).getbbox() is None
    assert ImageChops.difference(v6,fixed).getbbox() is None
    comparison.append({'renderer':renderer,'nativeSize':list(v4.size),'pose':[1568,1292],'camera':[1056,848,1],'viewport':[1440,1140],'DPR':1,'V4vsV6ChangedPixels':0,'beforeVsFixedUnchangedHeritagePixels':0})
    crop = (240,160,560,400)
    board(D/f'SHARPNESS_{renderer.upper()}_COMPARISON.png',[im.crop(crop).resize((640,480),Image.Resampling.NEAREST)for im in [v4,v6,fixed]],['V4 / SAME CAMERA','V6 BEFORE / SAME CAMERA','V6 FIXED / SAME CAMERA'],['Actual identical native320x240region, enlarged exactly2x with NEAREST for inspection.','Zero changed pixels in full1024x768native frames. No sharpening/contrast enhancement.'])

draws = []
for phase,data in [('before',pre),('after',post)]:
    for s in data['displays']:
        counts = {'nearest':0,'smoothed':0}
        for key,values in s.get('textureDraws',{}).items():
            if key != '[canvas]':
                for k in counts:
                    counts[k] += values[k]
        if s['renderer']=='Canvas':
            assert counts['nearest']>0 and counts['smoothed']==0
        else:
            assert s['filters'] and set(s['filters'])=={'9728'}
        assert s['rect']['width']==s['canvas'][0] and s['rect']['height']==s['canvas'][1]
        assert s['css']['imageRendering']=='pixelated'
        # Compare an unobstructed region of the REAL browser screenshot with
        # exact replicated canvas pixels, rather than relying on CSS settings.
        a=np.array(Image.open(Q/f'{phase}/{s["name"]}-native.png').convert('RGB'))
        b=np.array(Image.open(Q/f'{phase}/{s["name"]}-browser.png').convert('RGB'))
        dpr=s['dpr']; x,y=int(np.floor(s['rect']['x']*dpr+.5)),int(np.floor(s['rect']['y']*dpr+.5))
        box=(336,160,464,224)if 'mobile'in s['name']else(360,160,620,300)
        l,t,r,bot=box; native=a[t:bot,l:r]
        expected=np.repeat(np.repeat(native,dpr,axis=0),dpr,axis=1)
        actual=b[y+t*dpr:y+bot*dpr,x+l*dpr:x+r*dpr]
        # Settings overlay intentionally covers zoom demonstration screenshots.
        covered='zoom-'in s['name']
        same=expected.shape==actual.shape and np.array_equal(expected,actual)
        if not covered:
            assert same,(phase,s['name'],'Physical browser pixels differ from nearest native pixels')
        draws.append({'phase':phase,'name':s['name'],'renderer':s['renderer'],'DPR':dpr,'zoom':s['requestedZoom'],'canvas':s['canvas'],'CSSOrigin':[s['rect']['x'],s['rect']['y']],'assetDraws':counts,'textureFilters':s['filters'],'browserPixelPatchEqualsNearestNative':same if not covered else 'Not compared: settings overlay covers this patch','postRenderContextSmoothing':s.get('postRenderSmoothing'),'postRenderStateIsNotAssetDrawState':True})

report={'status':'PASS','comparisons':comparison,'drawAndDisplayEvidence':draws,'runtimeChanges':'None: matched captures demonstrated no V6-specific blur; all assets remain native, texture drawing uses nearest filtering, movement/camera code unchanged.','exportFinding':'Original1088x1328overview is a4:1nearest downsample of4352x5312. It discards detail and may be rescaled again by viewers; it is not a1:1gameplay sample. New web overview is integer2:1, full resolution and1:1PNG crops are also supplied.','limitations':['Zoom0.5necessarily drops detail and is not the native sharpness acceptance view.','WebGL measured in cloud SwiftShader; no physical phone/Safari/hardwareGPU claim.','Unchanged northern test crop is chosen to isolate rendering from intentional path-art changes.']}
(Q/'sharpness-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'matchedRendererComparisons':len(comparison),'displayChecks':len(draws),'nativeOverview':[4352,5312],'webOverview':[2176,2656]}))
