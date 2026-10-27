from designs import *
c=json.loads((S/'catalog.json').read_text());new=make('outfit',1,PAIRS[1]);old=next(i for i in c['items']if i['id']==new['id']);old['variants']=new['variants'];(S/'catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');print('Festival skirt now occludes lifted shoes behind fabric; grounded soles stay preserved; only2 outfit variants changed')
