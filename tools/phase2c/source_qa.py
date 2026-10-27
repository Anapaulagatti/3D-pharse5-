from compose import *
import collections
c=Composer();cat=c.catalog;assert len(cat['items'])==28;old=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());assert set(i['id']for i in old['items'])<=set(c.items);assert len(c.items)==28;rows=[];total=0
for item in cat['items']:
 assert item['availability']['status']=='free-review';assert set(item['compatibility']['characterIds'])=={v['characterId']for v in item['variants']}
 for v in item['variants']:
  id=v['characterId'];assert v['baseAtlasSHA256']==B[id];patch=c.patch(v);base=c.base(id);assert set(patch)==set(base),(item['id'],id,'missingframe');m=json.loads((R/'public'/v['mapping']).read_text());assert m['baseAtlasSHA256']==B[id];bounds=[]
  for name,(p,e)in patch.items():
   assert p.size==e.size==(96,112);assert set(np.unique(np.array(p)[:,:,3]))<={0,255};assert set(np.unique(np.array(e)[:,:,3]))<={0,255};out=apply(base[name],(p,e));bb=out.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112,(item['id'],id,name,bb);bounds.append(bb)
  rows.append({'item':item['id'],'character':id,'frames':len(patch),'headFootRegistration':[96,112,48,100],'baseHash':B[id],'explicitHiddenFrames':sum(v is None for v in m['frames'].values()),'decodedPatchBytes':Image.open(R/'public'/v['paint']).width*Image.open(R/'public'/v['paint']).height*8});total+=len(patch)
curated=[p for p in cat['presets']if p['id'].startswith('fashion-')];assert len(curated)==12;assert {p['appearance']['characterId']for p in curated}==set(B)
# Exhaustive within each actor's AUTHORED compatibility, ephemeral cells only.
# No permutations are shipped/preloaded or retained as runtime atlases.
combos=[]
for id in B:
 looks=list(c.allLooks(id));n=0
 for ids in looks:
  for name,base in c.base(id).items():
   out=c.render(id,ids,name);assert out.getbbox(),(id,ids,name);assert out.size==(96,112);n+=1
 combos.append({'character':id,'validCombinations':len(looks),'framesChecked':n});print(id,len(looks),n,flush=True)
q={'items':28,'existingItemsRetained':10,'newUniqueDesigns':18,'variants':rows,'variantFrames':total,'combinations':combos,'combinationFrames':sum(r['framesChecked']for r in combos),'baseAtlases':'Immutable; protected-audit.json','limitations':'Offline structural/ownership QA, not human art approval. Actual Phaser readbacks and gameplay are separate. Back glasses and occluded props may intentionally map null.','thresholds':'No historical Forge threshold changed','physicalDevices':'NOT TESTED'};(D/'source-qa.json').write_text(json.dumps(q,indent=2)+'\n');print('PASS28items,46nativevariants,',total,'registeredframes; exhaustivecombinations',q['combinationFrames'])
