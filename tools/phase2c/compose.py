from core import *
import itertools
class Composer:
 def __init__(self):
  self.catalog=json.loads((S/'catalog.json').read_text());self.items={i['id']:i for i in self.catalog['items']};self.cache={};self.bases={}
 def patch(self,v):
  key=v['paint']
  if key not in self.cache:self.cache[key]=decode(v)
  return self.cache[key]
 def base(self,id):
  if id not in self.bases:self.bases[id]=load(id)
  return self.bases[id]
 def variants(self,id,ids):
  selected=[self.items[i]for i in ids];out=[next(v for v in i['variants']if v['characterId']==id)for i in selected if i['category']!='accessory'];inter=[i for i in self.catalog.get('interactions',[])if i['characterId']==id and all(x in ids for x in i['requiresItemIds'])];out +=[i['patch']for i in inter if i['applyPhase']=='before-accessories'];out +=[next(v for v in i['variants']if v['characterId']==id)for i in selected if i['category']=='accessory'];out +=[i['patch']for i in inter if i['applyPhase']=='after-accessories'];return out
 def render(self,id,ids,name):
  im=self.base(id)[name].copy()
  for v in self.variants(id,ids):im=apply(im,self.patch(v)[name])
  return im
 def allLooks(self,id):
  get=lambda cat:[None]+[i['id']for i in self.catalog['items']if i['category']==cat and id in i['compatibility']['characterIds']]
  accessories=[x for x in get('accessory')if x]
  for h,o,acc in itertools.product(get('hairstyle'),get('outfit'),[tuple(a)for n in range(len(accessories)+1)for a in itertools.combinations(accessories,n)]):
   ids=[v for v in [h,o,*acc]if v]
   if any(set(self.items[i]['compatibility'].get('excludes',[]))&set(ids)for i in ids):continue
   yield ids
