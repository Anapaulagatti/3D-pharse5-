"""Data-only promotion of native-inspected complete packs; no engine changes."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2b'
identities=[('sori','소리','Sori','Cô bạn yêu âm nhạc, mang nhịp điệu vui tươi đến những con phố mới.',['lavender','cream','plum'],'Lavender raglan bomber, tailored shorts, long socks and musical brooch'),('jiwon','지원','Jiwon','Người bạn mê sách trầm tĩnh, luôn tò mò về những câu chuyện quanh mình.',['navy','beige','warm-white'],'Cable-knit academic vest, rolled white shirt and book brooch'),('nari','나리','Nari','Cô bạn yêu cây cỏ, thích khám phá khu vườn và những con đường tự nhiên.',['sage','yellow','cream'],'Gardener field vest, yellow shirt, practical trousers and botanical pin'),('taeyang','태양','Taeyang','Nhà thám hiểm thể thao đầy năng lượng và tự tin.',['amber','dark-blue','cream'],'Athletic amber windbreaker, navy trekking trousers and adventure shoes'),('yuna','유나','Yuna','Cô nghệ sĩ trẻ tinh nghịch, tìm cảm hứng từ những màu sắc của thành phố.',['dusty-pink','cream','denim'],'Creative pink utility jacket, denim culottes and paintbrush brooch'),('hyunwoo','현우','Hyunwoo','Người bạn đường ấm áp và đáng tin, luôn sẵn sàng cho chuyến đi mới.',['olive','brown','light-beige'],'Outdoor olive jacket, brown hiking trousers and compact backpack')]
imports=[];rows=[]
for id,ko,vi,description,palette,outfit in identities:
 p=S/id/'native-validation.json'
 if not p.exists():continue
 assert (S/id/'internal-native-review.json').exists(),f'Inspect native art first: {id}'
 q=json.loads(p.read_text());assert q['frameCount']==112 and len(q['clips'])==34
 imports.append(f'import {id}Clips from "../../assets-src/characters/phase2b/{id}/clips.json";')
 rows.append(dict(id=id,names={'ko':ko,'vi':vi},description=description,preview=f'assets/characters/{id}/preview-native.png',native={'width':96,'height':112,'anchor':[48,100]},collision={'policy':'shared-world-native-contact','model':'swept-point-plus-native-mask','footprint':'approved-native-envelope'},movement={'walkSpeed':60,'runSpeed':100,'walkStride':44,'runStride':64},cosmetics={'palette':palette,'outfit':outfit,'tags':['original-design','phase2b-review','default-only']},availability={'status':'playable','unlock':'free','reason':'Complete independent native pack, internal native art/phase gate inspected; actual Phaser wave evidence required; final human artistic acceptance pending'},assets={'key':f'character-{id}','texture':f'assets/characters/{id}/atlas.png','atlas':f'assets/characters/{id}/atlas.json'},animations=f'CLIP_{id}'))
s=json.dumps(rows,ensure_ascii=False,indent=2)
for row in rows:s=s.replace(json.dumps(row['animations']),'{ ...'+row['id']+'Clips, \"social-front\": '+row['id']+'Clips[\"wave-front\"] }')
(R/'src/characters/phase2bCharacters.ts').write_text('\n'.join(imports)+'\nimport type { CharacterDefinition } from "./types";\n/** Complete native review candidates. Future slots are removed by existing registry promotion. */\nexport const phase2bCharacters: CharacterDefinition[] = '+s+';\n')
print('Native-inspected complete registrations:',[r['id']for r in rows])
