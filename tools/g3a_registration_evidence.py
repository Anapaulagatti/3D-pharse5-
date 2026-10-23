from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-corrections';p=json.loads((D/'registration-proposal.json').read_text());plan=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
canvas=Image.new('RGB',(1680,1040),'#17242e');d=ImageDraw.Draw(canvas);scale=.18
for i in range(2):
 ox,oy=60+i*830,60
 def rect(r,color,width=2):x,y,w,h=r;d.rectangle((ox+x*scale,oy+y*scale,ox+(x+w)*scale,oy+(y+h)*scale),outline=color,width=width)
 for r in plan['land']:x,y,w,h=r;d.rectangle((ox+x*scale,oy+y*scale,ox+(x+w)*scale,oy+(y+h)*scale),fill='#3d514d')
 for path in plan['paths']:d.line([(ox+x*scale,oy+y*scale) for x,y in path['points']],fill='#657068',width=2)
 for b in plan['buildings']:rect(b['rect'],'#a0a2a0')
 rect([0,0,4352,4864],'white')
 d.text((ox,20),'CURRENT: rigid district' if not i else 'PROPOSED: native individual registration / NOT APPROVED',fill='white',font=font)
 if not i:rect([-225.5,1913,3184,1214],'#ff7878',3);rect([2238.5,2180,720,720],'#ffce70',3);d.text((ox,950),'West overflow225.5px; protected station anchor unchanged',fill='white',font=font)
 else:
  for s in p['buildings']:
   rect(s['collision'],'#ffce70' if s['id']=='station' else '#7ce7ba',3)
   x,y=s['worldEntry'];d.ellipse((ox+x*scale-3,oy+y*scale-3,ox+x*scale+3,oy+y*scale+3),fill='#ffeeae');d.text((ox+s['collision'][0]*scale,oy+s['collision'][1]*scale-18),s['id'],font=font,fill='white')
  for path in p['connectingRoutes']:d.line([(ox+x*scale,oy+y*scale)for x,y in path['points']],fill='#ffe1a0',width=2)
  d.text((ox,950),'Green: candidate footprints; yellow: protected station / new routes',font=font,fill='white')
d.text((20,995),'No approved plan, canvas, station anchor or source artwork changed. Bakery and convenience are UNASSIGNED candidate plots.',font=font,fill='white');canvas.save(D/'CURRENT_VS_PROPOSED.png',optimize=True)
# Compare footprints at the same scale; no invented bakery protected slot.
im=Image.new('RGB',(1500,720),'#17242e');d=ImageDraw.Draw(im)
for i,s in enumerate(p['buildings']):
 ox=20+(i%3)*500;oy=40+(i//3)*350;r=s['collision'];d.text((ox,oy-25),s['id']+' / contact footprint '+str(r[2:]),font=font,fill='white')
 reserve=next((b['rect'] for b in plan['buildings'] if b['id']==s['reservation']),None)
 if reserve:d.rectangle((ox,oy,ox+reserve[2]*.45,oy+reserve[3]*.45),outline='#999999',width=3)
 else:d.text((ox,oy+240),'No protected building reservation',fill='#ffce70',font=font)
 d.rectangle((ox,oy,ox+r[2]*.45,oy+r[3]*.45),outline='#7ce7ba',width=2)
 d.text((ox,oy+270),'Grey: existing slot; green: native candidate',font=font,fill='white')
im.save(D/'FOOTPRINT_COMPARISON.png',optimize=True)
rows=['| Building | Source plate entrance | Legacy rigid world (invalid group) | Candidate entrance | Reservation status |','| --- | --- | --- | --- | --- |']
for s in p['buildings']:
 a=s['sourceEntry'];old=[a[0]-225.5,a[1]+1913];rows.append(f"| {s['id']} | {a} | {old} | {s['worldEntry']} | {s['reservation'] or 'NEW UNASSIGNED PROPOSAL'} |")
(D/'ENTRANCE_COORDINATES.md').write_text('# Entrance registration comparison\n\nThe legacy rigid group is diagnostic only and cannot fit the canvas. Original source plate coordinates remain immutable.\n\n'+'\n'.join(rows)+'\n')
print('Registration diagrams and entrance comparison ready')

# Report physical and visual conflicts separately; the latter cannot be hidden by footprint-only checks.
def hit(a,b):
 x,y=max(a[0],b[0]),max(a[1],b[1]);right,bottom=min(a[0]+a[2],b[0]+b[2]),min(a[1]+a[3],b[1]+b[3]);return [x,y,right-x,bottom-y] if right>x and bottom>y else None
conflicts=[]
for s in p['buildings']:
 x,y=s['rasterOrigin'];a,b,c,e=s['sourceRect'];visual=[x,y,c-a,e-b]
 for b in plan['buildings']:
  if b['id']==s['reservation']:continue
  contact=hit(s['collision'],b['rect']);projection=hit(visual,b['rect'])
  if contact or projection:conflicts.append(dict(candidate=s['id'],approved=b['id'],contactIntersection=contact,visualEnvelopeIntersection=projection))
(D/'spatial-conflicts.json').write_text(json.dumps({'protectedContactIntersections':p['protectedStructureIntersections'],'projectionIntersections':conflicts,'note':'Conservative rectangular projection envelopes. They are not new physical building collisions or permissions to move approved structures.'},indent=2)+'\n')
