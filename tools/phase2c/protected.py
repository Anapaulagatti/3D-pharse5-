from core import *
import subprocess
m=json.loads((D/'approved-baseline.json').read_text());bad=[]
for p,h in m['files'].items():
 if sha(R/p)!=h:bad.append(p)
assert not bad,bad
# Explicitly permit only Studio/cosmetic extension code; game/camera/controller
# and identity registrations stay byte-identical to the human-approved commit.
allowed={'appearance.ts','appearanceTypes.ts','AppearanceRenderer.ts','preferences.ts','CharacterSelection.ts','selection.css','studioI18n.ts'};src=[]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',m['approvedCommit'],'src'],text=True).splitlines():
 if p.startswith('src/characters/')and Path(p).name in allowed:continue
 old=subprocess.check_output(['git','show',m['approvedCommit']+':'+p]);assert (R/p).read_bytes()==old,p;src.append(p)
q={'status':'PASS','baseAtlases':m['baseAtlases'],'frozenAssetFiles':len(m['files']),'changed':bad,'unchangedRuntimeFiles':src,'approval':m['approvedCommit'],'walkFrontAndWalkRight':'EXACT APPROVED PIXELS','defaultRestoration':'Immutable original atlas; no re-export','humanPhase2CApproval':'PENDING'};(D/'protected-audit.json').write_text(json.dumps(q,indent=2)+'\n');print('PASS',len(m['files']),'frozenartfiles,12atlases,',len(src),'protectedruntimefiles')
