from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd';base=json.loads((D/'BASELINE.json').read_text());cleanup=json.loads((R/'docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json').read_text());deleted={r['path']for r in cleanup['removed']};moves={r['from']:r for r in cleanup['archiveMoves']};bad=[];count=0
# All pre-existing artwork/source assets that were NOT expressly rejected stay exact.
for name,row in base['files'].items():
 if not name.startswith(('assets-src/','public/assets/')):continue
 if name in deleted:continue
 p=R/(moves[name]['to']if name in moves else name)
 if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(name)
 count+=1
codes=0
for name,row in base['files'].items():
 if not name.startswith(('src/characters/','src/npcs/','src/gate3/','src/world-gate1/','src/game/'))or name in ['src/npcs/manager.ts','src/gate3/main.ts']:continue
 if hashlib.sha256((R/name).read_bytes()).hexdigest()!=row['sha256']:bad.append(name)
 codes+=1
assert not bad,bad
proof={'status':'PASS','base':base['base'],'unchangedRetainedSourceAndRuntimeFiles':count,'unchangedProtectedCodeFiles':codes,'explicitAdditiveIntegrationCode':['src/gate3/main.ts','src/npcs/manager.ts'],'changedApprovedArt':bad,'explicitRejectedDeletions':len(deleted),'byteIdenticalSourceArchiveMoves':len(moves),'newArt':['assets-src/farming/phase3bd/crops.png:6original16x20pixel frames','assets-src/farming/phase3bd/postcard.png:exact native crop of already approved Jeju bridge ground'],'newArtProvenance':['assets-src/farming/phase3bd/PROVENANCE.json','assets-src/farming/phase3bd/POSTCARD_PROVENANCE.json'],'worldGeometryCameraNPCAndAvatarPixels':'UNCHANGED;3QAonlyapproachaliases versioned in source, no original manifest/target overwrite','sourceRollback':base['base'],'compiledRollback':base['rollbackArtifact'],'livePagesUnchanged':base['liveArtifactUnchanged']}
(D/'PROTECTED_AUDIT.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS',count,'retained source/runtime files unchanged;',len(moves),'moves byte-exact')
