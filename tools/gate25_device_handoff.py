"""Prepare documentation-only real-device handoff from the immutable approved ZIP. No build."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,shutil
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25-device-review';approved='868aa60acce297253c555f994ecac60276a830b3';tag='checkpoint/gate25-refinement-approved-20261022';original=R/'docs/gate25-refinement/GATE25_COMPOSITION_PLAYABLE.zip';expected='9390ec40ad0b7f8d1e6b6d50eff91862dd0261c3e2ce87276ea3ca7a1b3a50c5';sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(original.read_bytes())==expected
assert subprocess.check_output(['git','rev-parse',tag+'^{}'],cwd=R,text=True).strip()==approved
assert not subprocess.check_output(['git','diff',approved,'--','src','public','assets-src'],cwd=R,text=True)
checkpoint=dict(approvedCommit=approved,approvedTree=subprocess.check_output(['git','rev-parse',approved+'^{tree}'],cwd=R,text=True).strip(),annotatedTag=tag,tagObject=subprocess.check_output(['git','rev-parse','refs/tags/'+tag],cwd=R,text=True).strip(),approvalDate='2026-10-22',approvalTimezone='Asia/Saigon',scope='ARTISTIC_REFINEMENT_OF_CURRENT_DISTRICT_PROTOTYPE_ONLY',artisticStatus='HUMAN_APPROVED',physicalAndroidChrome='NOT TESTED',physicalIPhoneSafari='NOT TESTED',gate3='LOCKED',originalPackage=dict(path=str(original.relative_to(R)),bytes=original.stat().st_size,sha256=expected),sourceAndRuntimeChanged=False,merge=False,publicDeployment=False)
(D/'checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
with zipfile.ZipFile(original)as z:
 assert z.testzip()is None;data={n:z.read(n)for n in z.namelist()if not n.endswith('/')};oldmanifest=json.loads(data['MANIFEST.json'])
 for f in oldmanifest:assert sha(data[f['path']])==f['sha256'],f['path']
runtime={n:sha(b)for n,b in data.items()if n.startswith('3D-pharse5-/')};launcher=sha(data['start.py'])
# Existing native game, assets, historical scenes and launch script remain identical.
data['README.txt']=b'''GATE 2.5 HUMAN-APPROVED VISUAL PROTOTYPE / PHYSICAL DEVICE REVIEW ONLY
Gate3 LOCKED. Android Chrome NOT TESTED; iPhone Safari NOT TESTED.
Extract, run python3 start.py --lan on a computer; use its LAN IP on phones on the same trusted Wi-Fi. Stop with Ctrl-C. No public deployment.
Open http://COMPUTER_LAN_IP:8065/3D-pharse5-/gate2-review.html?scene=district-refinement
Frozen game files and picker labels are unchanged; approval is recorded in APPROVAL.md and CHECKPOINT.json.
Read DEVICE_CHECKLIST.md, fill DEVICE_REPORT_ANDROID.json / DEVICE_REPORT_IPHONE.json.
Options(...) > Export test report downloads JSON. Record real device model/OS/browser; attach exported files and actual screenshots/screen recordings. No physical PASS without evidence.
This handoff does not authorize fixes, Gate3, full-world production, main merge, deployment or large expansion. Stop and wait for explicit authorization.
'''
data['REPORT.md']=b'''# Handoff status

The district artistic refinement prototype is human-approved. See APPROVAL.md and CHECKPOINT.json. Game files and start.py are byte-identical to the approved archive; only handoff documentation/metadata/templates/manifest change.

Android Chrome: NOT TESTED. iPhone Safari: NOT TESTED. Automated desktop export/package smoke checks do not establish physical acceptance. Follow DEVICE_CHECKLIST.md and attach actual device evidence to the report templates.

Gate3 LOCKED. No full-world production, merge, deployment or large expansion is authorized. Stop after handoff and wait for explicit Gate3 authorization.
'''
for name in ['DEVICE_CHECKLIST.md','DEVICE_REPORT_ANDROID.json','DEVICE_REPORT_IPHONE.json']:data[name]=(D/name).read_bytes()
data['MOBILE_CHECKLIST.md']=data['DEVICE_CHECKLIST.md'];data['DEVICE_TESTING.md']=data['DEVICE_CHECKLIST.md'];data['APPROVAL.md']=(R/'docs/current/GATE25_REFINEMENT_APPROVAL.md').read_bytes();data['CHECKPOINT.json']=(D/'checkpoint.json').read_bytes()
for n,h in runtime.items():assert sha(data[n])==h
assert sha(data['start.py'])==launcher
manifest=[dict(path=n,bytes=len(b),sha256=sha(b))for n,b in sorted(data.items())if n!='MANIFEST.json'];data['MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
archive=D/'GATE25_DEVICE_REVIEW.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,6)as z:
 for n,b in sorted(data.items()):z.writestr(n,b)
ex=R/'.cache/gate25-device-review/extracted'
if ex.exists():shutil.rmtree(ex)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None;z.extractall(ex)
for row in manifest:assert sha((ex/row['path']).read_bytes())==row['sha256']
assert sha(original.read_bytes())==expected
(D/'package.json').write_text(json.dumps(dict(path=str(archive.relative_to(R)),bytes=archive.stat().st_size,sha256=sha(archive.read_bytes()),crc='PASS',manifest='PASS',originalApprovedZipUnchanged=True,approvedRuntimeFiles=len(runtime),allRuntimeFilesByteIdentical=True,startPyByteIdentical=True,noRebuild=True,onlyDocumentationMetadataTemplatesChanged=True,runtimeFiles=runtime),indent=2)+'\n')
print('PASS approved checkpoint / original ZIP immutable /',len(runtime),'runtime files + launcher identical / new ZIP CRC and manifest')
