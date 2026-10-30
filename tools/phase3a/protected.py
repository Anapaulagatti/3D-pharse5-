"""Full accepted Phase2C preservation plus exact removable additive NPC integration."""
from pathlib import Path
import json,hashlib,re,os,difflib
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase3bb'))
from amendments import historical_bytes
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';q=json.loads((D/'approved-baseline.json').read_text());bad=[]
for p,h in q['files'].items():
 if hashlib.sha256(historical_bytes(p,h)).hexdigest()!=h:bad.append(p)
assert not bad,bad
source=historical_bytes('src/gate3/main.ts').decode();pattern=r'^[ \t]*// PHASE3A BEGIN ([\w-]+)\n.*?^[ \t]*// PHASE3A END \1\n';blocks=list(re.finditer(pattern,source,re.M|re.S));assert[len(blocks),len(set(b.group(1)for b in blocks))]==[6,6],'Exactly6additive NPC hooks expected';stripped=re.sub(pattern,'',source,flags=re.M|re.S);original=(D/'approved-main.ts.txt').read_text();assert stripped==original,'Protected scene changed outside NPC hooks:\n'+''.join(list(difflib.unified_diff(original.splitlines(True),stripped.splitlines(True)))[:35]);result={'status':'PASS','approvedCommit':q['approvedCommit'],'frozenAssetFiles':len(q['files']),'baseAtlases':q['baseAtlases'],'changed':bad,'approvedSceneOutsideAdditiveHooks':'Historical baseline identical; exact Phase3BB amendments checked separately','additiveHooks':[{'name':b.group(1),'sha256':hashlib.sha256(b.group().encode()).hexdigest(),'lines':len(b.group().splitlines())}for b in blocks],'playerMovement':'Phase3BB explicit actual-travel facing/camera amendment; atlas unchanged','worldCollision':'UNCHANGED','StudioAnd28Cosmetics':'28 stable IDs; additive Phase3BB head-patch revisions; old assets unchanged','humanPhase3AArtApproval':'PENDING'};tmp=D/('protected-'+str(os.getpid())+'.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(D/'protected-audit.json');print('PASS',len(q['files']),'acceptedfiles;sceneoutside6NPC hooks byte-identical')
