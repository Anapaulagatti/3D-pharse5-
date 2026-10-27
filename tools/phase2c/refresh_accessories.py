from designs import *
c=json.loads((S/'catalog.json').read_text())
for style in range(6):
 new=make('accessory',style,PAIRS[style]);old=next(i for i in c['items']if i['id']==new['id']);old['variants']=new['variants']
(S/'catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');print('12newaccessoryvariants refreshed for native foreground hand ownership; bases/outfits/hair unchanged')
