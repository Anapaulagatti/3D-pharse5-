from designs import *
import copy,sys
manifest_path=S/'catalog.json';c=json.loads(manifest_path.read_text());stage=sys.argv[1]if len(sys.argv)>1 else'pilot'
styles=[0]if stage=='pilot'else list(range(6));c['items']=[i for i in c['items']if not i['id'].startswith('kr-')];c['presets']=[p for p in c['presets']if not p['id'].startswith('fashion-')];c['interactions']=[i for i in c.get('interactions',[])if not i['id'].startswith('fashion-')]
for style in styles:
 for category in ['hairstyle','outfit','accessory']:c['items'].append(make(category,style,PAIRS[style]))
 for id in PAIRS[style]:c['presets'].append({'id':'fashion-'+id,'name':id.title()+' · '+NAMES['outfit'][style][1],'appearance':{'schemaVersion':2,'characterId':id,'hairstyleId':'kr-'+NAMES['hairstyle'][style][0],'outfitId':'kr-'+NAMES['outfit'][style][0],'accessoryIds':['kr-'+NAMES['accessory'][style][0]]}})
# Explicit slot exclusions; no unsupported universal variants.
for item in c['items']:
 if item['id']=='kr-garden-hat':item['compatibility']['excludes']=['doyun-swept-quiff','doyun-curly-crop']
# Reapply authored long hair ownership after garment paint, then accessories.
for hair in [i for i in c['items']if i['category']=='hairstyle'and i['id'].startswith('kr-')]:
 for hv in hair['variants']:
  id=hv['characterId'];base=load(id);patch=decode(hv)
  for outfititem in [i for i in c['items']if i['category']=='outfit'and id in i['compatibility']['characterIds']]:
   iid='fashion-'+hair['id']+'-'+outfititem['id']+'-'+id
   c['interactions'].append({'id':iid,'characterId':id,'requiresItemIds':[hair['id'],outfititem['id']],'applyPhase':'before-accessories','patch':save(iid,id,patch,apply(base['idle-front-0'],patch['idle-front-0']),'Explicit hair/garment ownership replay; original face and foreground hands remain untouched')})
manifest_path.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');print(stage,'catalog',len(c['items']),'items',len(c['presets']),'presets')
