from pathlib import Path
import json
D=Path('docs/phase3b-a');p=D/'ACTUAL_PHASER_EVIDENCE.json';q=json.loads(p.read_text())
def snapshot(s):
 if not isinstance(s,dict):return s
 if 'npcs'in s:return {'world':{k:v for k,v in s['world'].items()if k in ['x','y','scene','characterId','playerSprites','frame','visited']},'npcs':snapshot(s['npcs'])}
 if 'actors'not in s:return s
 return {k:s[k]for k in ['clock','active','rendered','limit','assets','target','dialogue','historyArtSelected','catalogTotal']if k in s}|{'actors':[{k:a[k]for k in ['id','zone','position','direction','state','frame','activity','nativeScale','sampling','visible']if k in a}for a in s['actors']]}
for row in q['rows']:
 for key in ['samples','trace']:
  if key in row:row[key]=[snapshot(s)for s in row[key]]
q['evidenceProjection']='Actual captured values only; redundant inactive-record copies and FSM histories omitted. No samples or positions synthesized.';p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('Evidence bytes',p.stat().st_size)
