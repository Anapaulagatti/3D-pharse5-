"""Read-only public authoritative source retrieval; no images copied into game."""
from pathlib import Path
from urllib.request import urlopen,Request
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,re,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion/research';D.mkdir(exist_ok=True)
URLS={
'sejong':'https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n305800',
'jang-yeongsil':'https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n310300',
'shin-saimdang':'https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_30&levelId=kc_n306500',
'yi-sunsin':'https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_n309000',
'early-korea-index':'https://contents.history.go.kr/front/newEh/list.do?code=eh_age_30&type=eh_ty_010',
'han-kang':'https://www.nobelprize.org/prizes/literature/2024/han/facts/',
'bts':'https://ibighit.com/bts/eng/profile/',
'son-heungmin':'https://www.lafc.com/players/heung-min-son/',
'faker':'https://www.t1.gg/teams/league-of-legends',
'iu':'https://edam-ent.com/html/sub03/sub03_0301.php',
'yoo-jaesuk':'https://programs.sbs.co.kr/enter/runningman/cast/70100',
'aks-historical-encyclopedia':'https://encykorea.aks.ac.kr/',
'independence-hall':'https://www.i815.or.kr/',
'korea-publicity-policy':'https://www.korea.kr/news/policyNewsView.do?newsId=148903034'}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t in ['p','div','li','h1','h2','h3','br','tr']:self.out.append('\n')
 def handle_data(self,s):
  if not self.skip:self.out.append(s)
def fetch(pair):
 id,url=pair;record={'id':id,'requestedURL':url,'checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifiedClaims':[]}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 (educational game fact-check)'}),timeout=35)as r:
   data=r.read();record.update(status=r.status,finalURL=r.url,contentSHA256=hashlib.sha256(data).hexdigest());charset=r.headers.get_content_charset()or'utf-8'
  text=data.decode(charset,errors='replace');parser=Text();parser.feed(text);plain=re.sub(r'[ \t]+',' ',''.join(parser.out));plain=re.sub(r'\n\s*\n+','\n\n',plain).strip();(D/f'{id}.txt').write_text(plain);record.update(textFile=f'{id}.txt',bytes=len(data),retrieval='retrieved; human/claim review still required')
 except Exception as e:record.update(status='NOT VERIFIED',error=str(e))
 (D/f'{id}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(id,record['status'],flush=True);return record
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6)as pool:records=list(pool.map(fetch,URLS.items()))
 (D/'retrieval-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
