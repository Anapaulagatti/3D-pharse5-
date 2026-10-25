"""Native texel extraction/registration only, no image filters/resampling."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/palace-cleanup-v1';spec=json.loads((S/'scope.json').read_text());base=Image.open(S/'before-authoring-context.png').convert('RGBA');approach=Image.open(S/'approaches-authored.png').convert('RGBA');facade=Image.open(S/'facade-authored.png').convert('RGBA');branch=Image.open(S/'right-connection-authored.png').convert('RGBA')
for src in [approach,facade,branch]:assert src.size==(1536,1024)
layer=Image.new('RGBA',base.size);layer.paste(approach,(-7,512));mask=Image.new('L',base.size);d=ImageDraw.Draw(mask)
for key in ['axis','axis-gateway']:d.polygon([(x-1400,y-320)for x,y in spec['polygons'][key]],fill=255)
base.paste(layer,(0,0),mask)
for key in ['facade-left','facade-right']:
 p=spec['polygons'][key];x=min(i[0]for i in p);y=min(i[1]for i in p);rx=max(i[0]for i in p)+1;ry=max(i[1]for i in p)+1;base.paste(facade.crop((x-1400,y-200,rx-1400,ry-200)),(x-1400,y-320))
branchLayer=Image.new('RGBA',base.size);branchLayer.paste(branch,(188,380));mask=Image.new('L',base.size);d=ImageDraw.Draw(mask);d.polygon([(x-1400,y-320)for x,y in spec['polygons']['right-access']],fill=255);base.paste(branchLayer,(0,0),mask)
# Right gate lantern is in front of the new branch floor. Preserve its complete
# native silhouette rather than letting a floor patch clip its upper cap.
pier=[(742,622),(734,635),(721,646),(714,652),(714,659),(722,666),(724,683),(723,689),(718,695),(718,759),(715,764),(715,777),(763,777),(763,764),(761,759),(761,695),(757,689),(758,666),(766,660),(767,652),(754,646),(748,635)]
poly=[(x-7,y+512)for x,y in pier];mask=Image.new('L',base.size);ImageDraw.Draw(mask).polygon(poly,fill=255);base.paste(layer,(0,0),mask);mask.save(S/'right-gate-foreground-mask.png');base.save(S/'local-repair-authored.png')
(S/'native-assembly.json').write_text(json.dumps({'sourceSizes':[1536,1024],'placements':{'approaches':[1393,832],'facade':[1400,200],'branch':[1588,700]},'ceremonialSourceCenterX':655,'registeredAxisX':2048,'resampling':'NONE; integer native texels','rightGateForegroundPolygonInSource':pier,'sourceScale':1,'compoundScopeMask':'edit-scope-mask.png','preservedLeftPublicLane':[1855,1370,1984,1437]},indent=2)+'\n')
