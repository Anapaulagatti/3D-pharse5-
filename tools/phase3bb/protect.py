from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[2]; D=R/'docs/phase3bb-hotfix'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=D/'BASELINE.json'
if '--freeze' in sys.argv:
 assert not p.exists()
 old=json.loads((R/'docs/phase3b-a/BASELINE.json').read_text())['files']
 paths=[n for n in old if n.startswith(('public/assets/','assets-src/characters/','assets-src/npcs/','src/npcs/','src/engine/JuniMotion','src/characters/'))]
 p.write_text(json.dumps({'base':'ddd52849566fb3c1734570d6ff8562fbf7ef4026','files':{n:sha(R/n) for n in paths}},indent=2)+'\n')
 print('Frozen',len(paths));sys.exit()
old=json.loads(p.read_text())['files']; changes=[{'path':n,'before':s,'after':sha(R/n)} for n,s in old.items() if sha(R/n)!=s]
allowed={'assets-src/characters/phase2c/catalog.json'}
unexpected=[c for c in changes if c['path'] not in allowed]
q={'status':'PASS' if not unexpected else 'FAIL','checked':len(old),'changes':changes,'unexpected':unexpected,'baseAtlasesAndWorld':'UNCHANGED' if not unexpected else 'CHECK','physicalDevices':'NOT TESTED'}
(D/'PROTECTED_AUDIT.json').write_text(json.dumps(q,indent=2)+'\n'); print(q['status'],len(old),'files;',len(changes),'authorized catalog edits');assert not unexpected
