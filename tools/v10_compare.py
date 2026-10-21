"""Diagnostic only; old southern input is read AFTER independently committing V10.
Output never feeds the planner, build or runtime.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from v10_plan import sample_points
R=Path(__file__).resolve().parents[1];D=R/'docs/v10-city';S=R/'assets-src/v10-city'
old=json.loads((R/'assets-src/v9-world/plan/city.json').read_text());new=json.loads((S/'plan/city.json').read_text())
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';font=lambda n:ImageFont.truetype(F,n)
W,H=4352,6144;SCALE=0.2;pw,ph=round(W*SCALE),round((H-2240)*SCALE)
def roadmask(plan,legacy):
    im=Image.new('1',(W//16,(H-2240)//16));d=ImageDraw.Draw(im)
    for r in plan['roads']:
        pts=r['points']if legacy else sample_points(r)
        d.line([(round(x/16),round((y-2240)/16))for x,y in pts],fill=1,width=max(1,round(r['width']/16)),joint='curve')
    return np.array(im,dtype=bool)
def plotmask(plan,legacy):
    im=Image.new('1',(W//16,(H-2240)//16));d=ImageDraw.Draw(im)
    for p in plan['plots']:
        if legacy:x,y,x2,y2=p['bounds']
        else:x,y,w,h=p['rect'];x2,y2=x+w,y+h
        d.rectangle((x//16,(y-2240)//16,x2//16,(y2-2240)//16),fill=1)
    return np.array(im,dtype=bool)
def drawpanel(plan,legacy):
    im=Image.new('RGB',(pw,ph),'#e7ebe4');d=ImageDraw.Draw(im)
    pt=lambda p:(round(p[0]*SCALE),round((p[1]-2240)*SCALE))
    for r in plan['roads']:d.line([pt(p)for p in (r['points']if legacy else sample_points(r))],fill='#879dab',width=max(1,round(r['width']*SCALE)),joint='curve')
    for p in plan['plots']:
        if legacy:x,y,x2,y2=p['bounds']
        else:x,y,w,h=p['rect'];x2,y2=x+w,y+h
        d.rectangle((pt((x,y)),pt((x2,y2))),outline='#273e4a',fill='#b3c2c1',width=1)
    return im
roadsA,roadsB=roadmask(old,True),roadmask(new,False);plotsA,plotsB=plotmask(old,True),plotmask(new,False)
iou=lambda a,b:float(np.logical_and(a,b).sum()/np.logical_or(a,b).sum())
metrics=dict(method='Same absolute origin/scale; 16px raster of road envelopes and plot bounds. V9 curves use stored control-point polylines; a planning comparison, not a pixel-art comparison.',v10InitialIndependentPlanCommit='eea64e4',v10PlanSha256=hashlib.sha256((S/'plan/city.json').read_bytes()).hexdigest(),roadEnvelopeIoU=iou(roadsA,roadsB),plotEnvelopeIoU=iou(plotsA,plotsB),copiedRoadArrays=sum(a['points']==b['points'] for a in old['roads'] for b in new['roads']),copiedPlotRectangles=sum(a['bounds']==[b['rect'][0],b['rect'][1],b['rect'][0]+b['rect'][2],b['rect'][1]+b['rect'][3]]for a in old['plots']for b in new['plots']),approval='USER_VISUAL_REVIEW_REQUIRED')
out=Image.new('RGB',(pw*3+128,ph+240),'#f4f1e8');q=ImageDraw.Draw(out)
q.text((32,24),'V9 → V10 / ABSOLUTE GEOMETRY COMPARISON',font=font(28),fill='#243e4e')
q.text((32,68),'Roads + plots only. Same origin, no translation/rotation/normalization. Protected north excluded.',font=font(18),fill='#526c7b')
for i,(p,legacy,title)in enumerate([(old,True,'V9 / REJECTED'),(new,False,'V10 / PROPOSED')]):
    x=32+i*(pw+32);q.text((x,112),title,font=font(20),fill='#243e4e');out.paste(drawpanel(p,legacy),(x,152))
overlay=np.full((*roadsA.shape,3),236,dtype=np.uint8);overlay[roadsA]=[203,132,86];overlay[roadsB]=[73,139,154];overlay[roadsA&roadsB]=[96,76,115]
x=32+2*(pw+32);q.text((x,112),'OVERLAY / ORANGE V9 · TEAL V10',font=font(20),fill='#243e4e');out.paste(Image.fromarray(overlay).resize((pw,ph),Image.Resampling.NEAREST),(x,152))
q.text((32,out.height-58),f"Road overlap {metrics['roadEnvelopeIoU']:.1%} · Plot overlap {metrics['plotEnvelopeIoU']:.1%} · Identical road arrays {metrics['copiedRoadArrays']} · Identical plot bounds {metrics['copiedPlotRectangles']}",font=font(18),fill='#243e4e')
q.text((32,out.height-30),'Geometry metrics do not grant visual acceptance. V9 control polylines approximate curved road envelopes.',font=font(16),fill='#526c7b')
out.save(D/'V9_V10_GEOMETRY_COMPARISON.png');(D/'geometry-comparison.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics))
