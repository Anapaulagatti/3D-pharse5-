"""Original bilingual learning teasers in additive sidecars; original14graphs remain immutable."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion'
WORDS={
'seoyeon':'궁궐:cung điện|지붕:mái nhà|기둥:cột|마당:sân|문:cửa|계단:bậc thang',
'daehyun':'길:đường|안내:hướng dẫn|입구:lối vào|천천히:chậm rãi|오른쪽:bên phải|왼쪽:bên trái',
'minseo':'카페:quán cà phê|차:trà|컵:cốc|따뜻하다:ấm|가게:cửa hàng|쉬다:nghỉ',
'jiho':'책:sách|책장:giá sách|읽다:đọc|이야기:câu chuyện|조용하다:yên tĩnh|찾다:tìm',
'eunji':'역:nhà ga|표:vé|승강장:sân ga|기차:tàu hỏa|기다리다:chờ|안전:an toàn',
'junho':'시간:thời gian|출발:khởi hành|도착:đến nơi|여행:chuyến đi|지도:bản đồ|준비:chuẩn bị',
'harin':'귤:quýt|나무:cây|바다:biển|돌:đá|길:lối đi|집:nhà',
'seojun':'문화:văn hóa|현무암:đá basalt|마을:làng|풍경:phong cảnh|걷다:đi bộ|보다:ngắm',
'nayeon':'밭:ruộng|씨앗:hạt giống|물:nước|잎:lá|햇빛:ánh nắng|자라다:lớn lên',
'cheolsu':'봄:mùa xuân|흙:đất|뿌리:rễ|심다:trồng|작다:nhỏ|기다리다:chờ',
'yejin':'산:núi|숲:rừng|길:đường|지도:bản đồ|쉬다:nghỉ|천천히:chậm rãi',
'sungmin':'놀이공원:khu vui chơi|줄:hàng|입구:lối vào|표:vé|차례:lượt|기다리다:chờ',
'donghae':'배:thuyền|밧줄:dây thừng|항구:cảng|바람:gió|파도:sóng|방향:phương hướng',
'soobin':'안내:hướng dẫn|여객선:phà|시간표:lịch trình|줄:hàng|출발:khởi hành|안전:an toàn',
'modern-daon':'노래:bài hát|음악:âm nhạc|연습:luyện tập|박자:nhịp|듣다:nghe|함께:cùng nhau',
'modern-miram':'축구:bóng đá|공:quả bóng|팀:đội|운동:vận động|쉬다:nghỉ|천천히:chậm rãi',
'modern-geonu':'게임:trò chơi|팀:đội|전략:chiến thuật|협력:hợp tác|연습:luyện tập|휴식:nghỉ ngơi',
'modern-seorin':'연극:kịch|무대:sân khấu|대본:kịch bản|목소리:giọng nói|이야기:câu chuyện|연습:luyện tập',
'modern-haru':'인사:chào hỏi|소개:giới thiệu|행사:sự kiện|함께:cùng nhau|듣다:nghe|이야기:câu chuyện',
'modern-yeori':'책:sách|작가:tác giả|문장:câu|글쓰기:viết văn|읽다:đọc|모임:buổi gặp'}
LINES={
'seoyeon':('기둥과 지붕을 보세요. 마당에서는 천천히 걸어요.','Hãy ngắm những cây cột và mái nhà. Mình đi thong thả trong sân nhé.'),
'daehyun':('입구를 찾으세요? 길을 천천히 안내해 드릴게요.','Bạn đang tìm lối vào à? Tôi sẽ thong thả chỉ đường cho bạn.'),
'minseo':('따뜻한 차 한 잔을 마시며 쉬어 가세요.','Bạn hãy nghỉ chân và thưởng thức một tách trà ấm nhé.'),
'jiho':('어떤 이야기를 좋아하세요? 책장에서 함께 찾아봐요.','Bạn thích câu chuyện như thế nào? Mình cùng tìm trên giá sách nhé.'),
'eunji':('기차를 기다릴 때는 안전을 먼저 생각해 주세요.','Khi đợi tàu, bạn hãy chú ý an toàn trước nhé.'),
'junho':('출발 시간과 도착 시간을 미리 확인해요.','Mình kiểm tra trước giờ khởi hành và giờ đến nhé.'),
'harin':('귤나무를 보고 바다 쪽 풍경도 즐겨 보세요.','Bạn hãy ngắm cây quýt và thưởng thức cả cảnh hướng ra biển nhé.'),
'seojun':('마을의 돌과 현무암을 살펴보세요. 풍경을 보며 걸어요.','Bạn hãy quan sát những viên đá và đá basalt trong làng. Mình vừa đi vừa ngắm cảnh nhé.'),
'nayeon':('씨앗이 자라려면 물과 햇빛이 필요해요.','Để hạt giống lớn lên thì cần có nước và ánh nắng.'),
'cheolsu':('작은 씨앗을 흙에 심고 천천히 기다려요.','Mình gieo hạt nhỏ xuống đất rồi kiên nhẫn chờ nhé.'),
'yejin':('지도를 확인하고 숲길에서 천천히 걸어요.','Mình xem bản đồ rồi thong thả đi trên đường rừng nhé.'),
'sungmin':('입구에서 줄을 서고 차례를 기다려 주세요.','Bạn hãy xếp hàng ở lối vào và chờ đến lượt nhé.'),
'donghae':('항구에서는 바람과 파도를 살펴보세요.','Ở cảng, bạn hãy quan sát gió và sóng nhé.'),
'soobin':('여객선의 출발 시간은 시간표에서 확인해 주세요.','Bạn hãy xem giờ khởi hành của phà trên bảng lịch trình nhé.'),
'modern-daon':('음악을 들으며 박자를 천천히 느껴 보세요. 저는 노래를 연습하러 왔어요.','Bạn hãy nghe nhạc và từ từ cảm nhận nhịp nhé. Tôi đến đây để luyện hát.'),
'modern-miram':('저는 축구를 가르쳐요. 팀과 함께 운동하고 쉬는 시간도 챙겨요.','Tôi dạy bóng đá. Mình vận động cùng đội và cũng nhớ dành thời gian nghỉ nhé.'),
'modern-geonu':('게임에서는 팀의 협력이 중요해요. 연습할 때 휴식도 필요해요.','Trong trò chơi, sự hợp tác của cả đội rất quan trọng. Khi luyện tập cũng cần nghỉ ngơi.'),
'modern-seorin':('저는 연극을 해요. 대본을 읽고 목소리를 천천히 연습해요.','Tôi diễn kịch. Tôi đọc kịch bản rồi thong thả luyện giọng.'),
'modern-haru':('문화 행사에서 사람들의 이야기를 들어요. 함께 인사해 볼까요?','Tôi lắng nghe câu chuyện của mọi người tại các sự kiện văn hóa. Mình cùng thử chào hỏi nhé?'),
'modern-yeori':('저는 글을 쓰고 책 모임에 가요. 마음에 드는 문장을 함께 읽어 봐요.','Tôi viết văn và tham gia câu lạc bộ sách. Mình cùng đọc một câu bạn yêu thích nhé.')}
old=json.load(open(R/'assets-src/npcs/phase3a/registry.json'))['npcs'];modern=json.load(open(S/'modern-definitions.json'))['npcs'];nodes=[];extensions=[];learning=[]
def node(n,id,ko,vi,hint,choices=None,next=None):return {'id':id,'npcId':n['id'],'content':{'ko':ko,'vi':vi},'hint':{'ko':'함께 말해 봐요','vi':hint},'choices':choices or[],'next':next,'conditions':[],'futureQuestHook':None,'lessonTopicTags':n['future']['learningTopicTags']+['beginner-korean','conversation-teaser']}
for n in old+modern:
 id=n['id'][4:];vocab=[dict(zip(['ko','vi'],w.split(':')))for w in WORDS[id].split('|')];ko,vi=LINES[id];wordsHint=' · '.join(v['ko']+' = '+v['vi']for v in vocab[:3]);practiceHint=' · '.join(v['ko']+' = '+v['vi']for v in vocab[3:]);learning.append({'npcId':n['id'],'topicCount':4,'vocabulary':vocab,'authenticatedLessonProgress':False,'contentStatus':'Original fictional/contextual language teaser; human language review pending'})
 if n in old:
  choices=[{'id':'words','label':{'ko':'직업 이야기를 들려주세요.','vi':'Nói về công việc'},'next':n['id']+'-exp-words'},{'id':'practice','label':{'ko':'한국어로 말해 볼까요?','vi':'Thử nói tiếng Hàn'},'next':n['id']+'-exp-practice'}];extensions.append({'npcId':n['id'],'rootId':n['dialogueId'],'choices':choices});nodes.append(node(n,choices[0]['next'],ko,vi,wordsHint));nodes.append(node(n,choices[1]['next'],'천천히 말해도 괜찮아요. 모르는 말이 있으면 다시 물어보세요.','Bạn cứ nói chậm cũng được. Nếu có từ chưa hiểu, bạn hãy hỏi lại nhé.',practiceHint))
 else:
  choices=[{'id':key,'label':{'ko':k,'vi':v},'next':n['id']+'-'+key}for key,k,v in [('place','여기에는 왜 왔어요?','Bạn đến đây làm gì?'),('work','어떤 일을 해요?','Nói về công việc'),('words','새 단어를 알려주세요.','Từ vựng nhỏ'),('practice','함께 말해 볼까요?','Thử nói cùng nhau')]];nodes.append(node(n,n['dialogueId'],'안녕하세요. 저는 '+n['names']['ko']+('이에요'if(ord(n['names']['ko'][-1])-0xAC00)%28 else'예요')+'. 잠깐 이야기 나눌까요?','Xin chào, tôi là '+n['names']['vi']+'. Mình trò chuyện một lát nhé?', 'Khách văn hóa hư cấu · Không đại diện hay bảo chứng cho người thật.',choices));nodes.append(node(n,n['id']+'-place','잠시 이곳에 들렀어요. 주변을 천천히 둘러보고 있어요.','Tôi đang ghé nơi này một lát và thong thả ngắm xung quanh.',wordsHint,next=n['id']+'-work'));nodes.append(node(n,n['id']+'-work',ko,vi,wordsHint));nodes.append(node(n,n['id']+'-words','오늘은 이 단어들을 함께 읽어 봐요.','Hôm nay mình cùng đọc những từ này nhé.',wordsHint,next=n['id']+'-practice'));nodes.append(node(n,n['id']+'-practice','천천히 말해도 괜찮아요. 좋아하는 것을 한국어로 소개해 보세요.','Bạn cứ nói chậm cũng được. Hãy thử giới thiệu điều mình thích bằng tiếng Hàn nhé.',practiceHint))
(S/'dialogue-additions.json').write_text(json.dumps({'schemaVersion':1,'rootExtensions':extensions,'nodes':nodes,'learning':learning},ensure_ascii=False,indent=2)+'\n');print(len(nodes),'additive nodes;',len(learning),'six-word bilingual sets; original graphs unchanged')
