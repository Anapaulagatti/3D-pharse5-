"""Reuse the existing compiled game; apply only targeted scene assets/catalog and review documents."""
from pathlib import Path
import zipfile,json,hashlib,shutil,re,posixpath,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25-station-planters';P=R/'public/assets/gate2';source=R/'docs/gate25-device-review/GATE25_DEVICE_REVIEW.zip';sha=lambda b:hashlib.sha256(b).hexdigest();sourceReceipt=json.loads((R/'docs/gate25-device-review/package.json').read_text());assert sha(source.read_bytes())==sourceReceipt['sha256'];assert not subprocess.check_output(['git','diff','868aa60','--','src'],cwd=R,text=True)
with zipfile.ZipFile(source)as z:
 assert z.testzip()is None;game={n:z.read(n)for n in z.namelist()if n.startswith('3D-pharse5-/')and not n.endswith('/')};launcher=z.read('start.py').decode().replace('scene=district-refinement','scene=district-planter-repair')
old={n:sha(b)for n,b in game.items()};catalog='3D-pharse5-/assets/gate2/catalog.json';game[catalog]=(P/'catalog.json').read_bytes();added=[]
for p in sorted((P/'district-planter-repair').iterdir()):
 if p.is_file():name='3D-pharse5-/assets/gate2/district-planter-repair/'+p.name;assert name not in game;game[name]=p.read_bytes();added.append(name)
changed=[n for n,h in old.items()if sha(game[n])!=h];assert changed==[catalog]
data=dict(game);data['start.py']=launcher.encode();data['README.txt']=b'''TWO STATION PLANTERS / HUMAN VISUAL REVIEW PENDING / GATE3 LOCKED
Run python3 start.py and open the printed local URL; current scene is district-planter-repair.
For a private phone review on the same trusted Wi-Fi use python3 start.py --lan and your computer's LAN IP. No public deployment.
Only two station planters and associated local underpainting/shadows/foot reservations were repaired. The existing compiled application and other scene assets are preserved.
Compare actual native PNGs, both before/after crops, frontage with Juni and collision video at:
https://github.com/Anapaulagatti/3D-pharse5-/blob/art-gate/gate2-three-slices/docs/gate25-station-planters/README.md
Native arrow/WASD and mobile joystick; Scenic/Overview/Return retained.
Previous approval was qualified by the planter defect; this candidate is NOT artistically approved. Android Chrome/iPhone Safari physical validation NOT TESTED.
Stop for direct human visual approval. No Gate3, full-world production, merge or deployment.
'''
report=(D/'REPORT.md').read_text();base='https://github.com/Anapaulagatti/3D-pharse5-/blob/art-gate/gate2-three-slices/'
report=re.sub(r'\]\(([^)]+)\)',lambda m:']('+base+posixpath.normpath('docs/gate25-station-planters/'+m.group(1))+')'if not m.group(1).startswith(('http','#'))else m.group(0),report);data['REPORT.md']=report.encode()
for n in ['asset-proof.json','sampling-and-alpha.json','preservation.json','browser-qa.json']:data[n]=(D/n).read_bytes()
manifest=[dict(path=n,bytes=len(b),sha256=sha(b))for n,b in sorted(data.items())];data['MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode();out=D/'GATE25_STATION_PLANTERS_REVIEW.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6)as z:
 for n,b in sorted(data.items()):z.writestr(n,b)
ex=R/'.cache/gate25-station-planters/extracted'
if ex.exists():shutil.rmtree(ex)
with zipfile.ZipFile(out)as z:assert z.testzip()is None;z.extractall(ex)
for f in manifest:assert sha((ex/f['path']).read_bytes())==f['sha256']
(D/'package.json').write_text(json.dumps(dict(path=str(out.relative_to(R)),bytes=out.stat().st_size,sha256=sha(out.read_bytes()),crc='PASS',manifest='PASS',noFrontendRebuild=True,existingRuntimeFiles=len(old),changedExistingRuntimeFiles=changed,newSceneFiles=added,allOtherRuntimeFilesIdentical=True,sourceArchiveUnchanged=sha(source.read_bytes())==sourceReceipt['sha256']),indent=2)+'\n');print('PASS review ZIP / CRC+manifest / only catalog +5 targeted scene files / frozen application reused')
