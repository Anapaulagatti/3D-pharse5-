"""Stage owner-requested historical candidates; never change old NPCs."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-final-six';D=R/'docs/phase3a-final-six'
ROWS=[
('seondeok','Nữ vương Seondeok','선덕여왕','Silla','632–647 (reign, owner anchor)','npc-seoyeon','E0028652',['나라','역사','왕','문화']),
('sejong','Vua Sejong','세종대왕','Joseon đầu kỳ','1397–1450; reign1418–1450 (owner anchor)','npc-seoyeon','E0029857',['글자','한글','책','배우다']),
('jang','Jang Yeong-sil','장영실','Joseon đầu kỳ','Birth/death years unknown; not invented','npc-jiho','E0048697',['시간','시계','과학','만들다']),
('saimdang','Shin Saimdang','신사임당','Joseon','1504–1551 (owner anchor)','npc-jiho','E0033037',['그림','꽃','색','그리다']),
('yi','Đô đốc Yi Sun-sin','이순신','Joseon','1545–1598 (owner anchor)','npc-donghae','E0044900',['바다','배','지도','방향']),
('yu','Yu Gwan-sun','유관순','Phong trào độc lập thế kỷ XX','1902–1920;1919 (owner anchor)','npc-jiho','614',['독립','역사','학생','기억하다'])]
old=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs'];defs=[];meta=[];claims=[];nodes=[]
gloss={'나라':'đất nước','역사':'lịch sử','왕':'vua','문화':'văn hóa','글자':'chữ viết','한글':'chữ Hangeul','책':'sách','배우다':'học','시간':'thời gian','시계':'đồng hồ','과학':'khoa học','만들다':'làm, chế tạo','그림':'tranh','꽃':'hoa','색':'màu sắc','그리다':'vẽ','바다':'biển','배':'thuyền','지도':'bản đồ','방향':'phương hướng','독립':'độc lập','학생':'học sinh','기억하다':'ghi nhớ'}
for key,vi,ko,era,dates,host,article,words in ROWS:
 id='npc-history-'+key;n=copy.deepcopy(next(x for x in old if x['id']==host));n.update(id=id,names={'ko':ko,'vi':vi},occupation='Bản thử mỹ thuật · '+era+' (theo đề bài, chưa kiểm chứng)',idleBehavior='archive-art',dialogueId=id+'-welcome');n['assets']={'texture':f'assets/npcs/phase3a/{id}/atlas.png','atlas':f'assets/npcs/phase3a/{id}/atlas.json','key':id};n['future']={'questProviderId':None,'shopProviderId':None,'learningTopicTags':['history-archive',key]};defs.append(n)
 url='https://search.i815.or.kr/dictionary/detail/print.do?id=614' if key=='yu' else 'https://encykorea.aks.ac.kr/Article/'+article
 meta.append({'id':id,'hostResidentId':host,'era':era,'chronologyOrder':len(meta),'dateProposal':dates,'dateStatus':'UNVERIFIED owner starting anchor','sourceURL':url,'sourceStatus':'UNVERIFIED','reconstructionNotice':{'ko':'교육용 재구성 미술 시안입니다. 역사와 복식 자료는 아직 검증되지 않았습니다. 실제 인물의 발언이 아닙니다.','vi':'Bản thử mỹ thuật tái hiện phục vụ giáo dục. Tư liệu lịch sử và trang phục chưa được kiểm chứng. Đây không phải lời nói thật của nhân vật.'},'vocabulary':[{'ko':w,'vi':gloss[w]}for w in words]})
 for cid,ck,cv in [('identity',ko,vi),('period',era,era),('dates',dates,dates),('attire','복식 재구성','Trang phục tái hiện')]:claims.append({'figureId':id,'claimId':id+'-'+cid,'koreanWording':ck,'vietnameseWording':cv,'sourceURL':url,'publisher':'Independence Hall of Korea'if key=='yu'else'Academy of Korean Studies','pageTitle':None,'retrievedAt':None,'supportingExcerpt':None,'status':'UNVERIFIED','confidence':'Not independently inspected; owner-provided starting anchor only','rightsNotes':'No source images copied. Independently illustrated costume is speculative; no authenticated portrait claim.'})
 def node(suffix,k,v,next=None,hint=None):return {'id':id+'-'+suffix,'npcId':id,'content':{'ko':k,'vi':v},'hint':{'ko':'미술 시안 · 역사 사실 검증 대기','vi':hint or 'Bản thử mỹ thuật · đang chờ kiểm chứng lịch sử'},'choices':[],'next':id+'-'+next if next else None,'conditions':['always'],'futureQuestHook':None,'lessonTopicTags':['history-archive',key]}
 nodes.append(node('welcome','안녕하세요. 이 화면은 역사 이야기의 미술 시안입니다.','Xin chào! Đây là bản thử mỹ thuật cho mục câu chuyện lịch sử.','notice'))
 nodes.append(node('notice',meta[-1]['reconstructionNotice']['ko'],meta[-1]['reconstructionNotice']['vi'],'words'))
 nodes.append(node('words','한국어 낱말을 함께 살펴보세요.','Cùng xem một vài từ tiếng Hàn nhé.','art',' · '.join(w+' = '+gloss[w]for w in words)))
 nodes.append(node('art','앞모습과 뒷모습, 옆모습의 움직임을 살펴보세요.','Bạn có thể quan sát chuyển động từ phía trước, phía sau và hai bên.','sources'))
 nodes.append(node('sources','검증된 자료를 확보한 뒤 역사 설명을 제공합니다.','Phần giới thiệu lịch sử sẽ được bổ sung sau khi kiểm chứng được tư liệu.','return'))
 nodes.append(node('return','둘러봐 주셔서 감사합니다. 원래 세계로 돌아가세요.','Cảm ơn bạn đã xem. Hãy trở lại thế giới hiện tại nhé.'))
(S/'definitions.json').write_text(json.dumps({'schemaVersion':1,'status':'ART_REVIEW_ONLY_SOURCE_BLOCKED','npcs':defs},ensure_ascii=False,indent=2)+'\n')
(S/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');(S/'dialogues.json').write_text(json.dumps({'nodes':nodes,'verifiedHistoricalBiographies':0,'purpose':'Neutral art-review narrator/vocabulary only, not completed historical educational dialogue'},ensure_ascii=False,indent=2)+'\n')
(D/'SOURCE_EVIDENCE.json').write_text(json.dumps({'verifiedClaims':0,'claims':claims,'retrievalEvidence':['research/retrieval-attempts.json','research/browser-retrieval.json'],'status':'SOURCE BLOCKED; do not enable production archives'},ensure_ascii=False,indent=2)+'\n')
print('Staged six exact IDs and neutral review-only dialogue, not verified historical content')
