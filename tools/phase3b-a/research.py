from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
import json,datetime,hashlib,re
urls=[('Korean unfair competition statute','https://law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1025179229'),('KIPO statement requested 2026-03-05','https://www.kipo.go.kr/ko/kpoBultnDetail.do?aprchId=BUT0000029&keyword=&menuCd=SCD0200618&ntatcSeq=20800&pageIndex=&searchCondition=&sysCd=SCD02'),('KIPRIS','https://www.kipris.or.kr/'),('KCC AI-assisted works registration guidance','https://www.copyright.or.kr/eng/doc/etc_pdf/Guide_to_Copyright_Registration_for_Generative_AI-Assisted_Works.pdf'),('MCST copyright FAQ','https://www.mcst.go.kr/site/s_policy/copyright/netizen/netizen02.jsp'),('Provider terms','https://openai.com/policies/terms-of-use/'),('Provider service terms','https://openai.com/policies/service-terms/')]
def get(row):
 title,url=row;q={'evidenceId':'official-'+str(urls.index(row)+1),'titleRequested':title,'url':url,'attemptedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'termsAtCreation':'UNKNOWN','permissionEstablished':False}
 try:
  with urlopen(Request(url,headers={'User-Agent':'KoreanArena-ProvenanceReview/1.0'}),timeout=12)as r:
   b=r.read(2000000);q.update(httpStatus=r.status,contentType=r.headers.get('Content-Type'),sha256=hashlib.sha256(b).hexdigest())
   if 'pdf' in(r.headers.get('Content-Type')or''):q.update(status='BINARY_RETRIEVED_NOT_TEXT_VERIFIED',supportingExcerpt=None)
   else:
    text=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',b.decode('utf-8',errors='replace'))).strip();q.update(status='CURRENT_TEXT_INSPECTED_NOT_CREATION_TERMS',supportingExcerpt=text[:350],claimLimit='Does not establish original account/model/plan terms or depiction permission')
 except Exception as e:q.update(status='TRANSPORT_FAILED_NOT_RIGHTS_DENIAL',error=str(e),supportingExcerpt=None)
 return q
with ThreadPoolExecutor(max_workers=5)as pool:rows=list(pool.map(get,urls))
Path('docs/phase3b-a/OFFICIAL_SOURCE_EVIDENCE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print([(q['evidenceId'],q['status'])for q in rows])
