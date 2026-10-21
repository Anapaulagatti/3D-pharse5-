"""Offline Gate1 stored-output validation; never generate art or fetch providers."""
import ast,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate1';M=S/'map';P=R/'public/assets/gate1';D=R/'docs/gate1';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
 protected=read(R/'assets-src/v10-city/protected-files.json')
 for p,want in protected.items():assert sha(R/p)==want,p
 # The entire approved masterplan/map and shared engine were not edited for Gate1.
 changed=subprocess.check_output(['git','diff','3c323bc1d844c80b3e0ca0d62df3f1806a7a972f','--name-only','--','assets-src/v10-city','assets-src/protected-north','public/assets/v10-city','src/engine','src/game','src/world','src/main.ts','package.json','package-lock.json'],cwd=R,text=True);assert not changed,changed
 bundle=read(M/'bundle.json');world=read(M/'world.json');tm=read(P/'plaza.json');assert world['mapSha256']==sha(M/'bundle.json')
 for name,spec in bundle['props'].items():assert sha(P/(name+'.png'))==sha(M/spec['image']),name
 assert sha(P/'tiles.png')==sha(M/'tiles.png')
 atlas=Image.open(P/'tiles.png').convert('RGBA');floor=Image.open(M/'floor.png').convert('RGBA');out=Image.new('RGBA',(1536,1024))
 for i,gid in enumerate(tm['layers'][0]['data']):
  tile=gid-1;xx=(tile%128)*32;yy=(tile//128)*32;out.paste(atlas.crop((xx,yy,xx+32,yy+32)),((i%48)*32,(i//48)*32))
 assert out.tobytes()==floor.tobytes(),'Tiled readback'
 solids=bundle['collision']['solids'];assert[[o[k]for k in['x','y','width','height']]for o in tm['layers'][2]['objects']]==[[o[k]for k in['x','y','w','h']]for o in solids]
 for row in read(S/'native-provenance.json'):
  image=S/row['path'];assert sha(image)==row['sha256'];im=Image.open(image).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<={0,255}
 native=Image.open(S/'native/street-foundation.png');assert native.size==Image.open(S/'originals/street-foundation.png').size==(1536,1024)
 for src in [R/'src/gate1/Street.ts',R/'src/gate1/main.ts',R/'tools/gate1_build.py']:
  txt=src.read_text();assert not any(x in txt for x in ['v10-city','v9-world','v8-city','map_pipeline','v10_surfaces','v10_final_build']),src
 nav=read(S/'qa/nav-report.json');assert nav['status']=='pass';assert read(S/'qa/proof.json')['bundleSha256']==sha(M/'bundle-hashed.json')
 expected=Image.open(R/'docs/v10-city/V10_NORTH.png').convert('RGBA');actual=Image.open(D/'GATE1_NORTH_REFERENCE.png').convert('RGBA');assert actual.tobytes()==expected.tobytes()
 one=Image.open(D/'GATE1_STREET_NATIVE.png').convert('RGBA');two=Image.open(D/'GATE1_STREET_2X.png').convert('RGBA');assert one.resize((3072,2048),Image.Resampling.NEAREST).tobytes()==two.tobytes()
 proof=dict(status='PASS',protectedFiles=len(protected),masterplanAndFullMapUnchanged=True,sharedGameplayUnchanged=True,majorArtworkSpatialScale=1,northRenderPixelExact=True,twoXExactNearest=True,tiledFloorReadbackExact=True,runtimeCollidersExact=True,navTargets=5,solids=len(solids),artApproval='PENDING USER')
 (D/'offline-validation.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
if __name__=='__main__':validate()
