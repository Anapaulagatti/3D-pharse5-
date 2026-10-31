from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bc';m=json.loads((D/'PROTECTED_BASELINE.json').read_text());bad=[]
for name,digest in m['files'].items():
 p=R/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:bad.append(name)
report={'status':'PASS'if not bad else'FAIL','base':m['base'],'files':len(m['files']),'changed':bad,'allExistingNPCPlayerWorldCosmeticArt':'BYTE IDENTICAL'if not bad else'CHANGED','allowedAdditions':['two derived bridge collision .bin files; original masks immutable','reversible quest indicators drawn as separate gameplay objects; no base pixel writes'],'runtimeCodeAmendments':'AUTHORIZED_AMENDMENTS.json exact before/after hashes; old checks reconstruct old code only after matching successor pin. Current behavior checked independently.','publicRollbackArtifact':'74235a6e7075b77840d2e9fdf36dce678288cd05'}
(D/'PROTECTED_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');assert not bad,bad;print(report['files'],'unchanged protected files')
