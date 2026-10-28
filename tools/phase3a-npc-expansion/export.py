"""Only approved-scope legacy derived visual replacements, after strict native audit."""
from pathlib import Path
import json,hashlib,shutil,sys
from audit import protect,actor
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion'
for id in sys.argv[1:]:
 p=S/id;report=actor(id);assert not report['errors'],report['errors'];out=R/f'public/assets/npcs/phase3a/npc-{id}'
 for a,b in [('candidate-atlas.png','atlas.png'),('candidate-preview-native.png','preview-native.png')]:shutil.copyfile(p/a,out/b)
 provenance={'art_source':'host_image','route':'builtin image_gen.imagegen','identity':(p/'identity.txt').read_text().strip(),'sources':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in[p/'master-source.png',p/'turnaround-source.png',p/'rig.json',p/'native-finish.json']},'sourceOwnedLayers':44,'nativeCells':104,'cell':[96,112],'anchor':[48,100],'runtimeAtlasJSON':'UNCHANGED original approved frame contract','primaryCharacterArt':'Own independent source illustration; no procedural body or copied player pixels','movement':'Juni numerical landmarks only; own grounded-retargeted shoes, own masks and cloth','humanArtApproval':'PENDING','qa':report['status']};(out/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n');print(id,'exported derived visuals only')
protect()
