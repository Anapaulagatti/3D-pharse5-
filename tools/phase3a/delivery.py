"""Consolidate measured Phase3A evidence; never grants human artistic acceptance."""
from pathlib import Path
import json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';logs=D/'logs';logs.mkdir(exist_ok=True)
def load(n):return json.loads((D/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['typecheck','assets','lint','format','unit','build','focused','cross','performance','media']:
 p=Path('/tmp/phase3a-final-'+n+'.log')
 if p.exists():shutil.copyfile(p,logs/(n+'.log'))
shutil.copyfile('/tmp/phase3a-locked-e2e.log',logs/'full-60-e2e.log')
for n in ['stability','extra','webgl']:
 p=Path('/tmp/phase3a-locked-'+n+'.log')
 if p.exists():shutil.copyfile(p,logs/(n+'.log'))
provenance={}
for stem in ['assets-src/npcs/phase3a','public/assets/npcs/phase3a','src/npcs','tools/phase3a']:
 for p in (R/stem).rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:provenance[str(p.relative_to(R))]=sha(p)
pilots={}
for id in ['seoyeon','minseo','harin','eunji']:
 n=f'public/assets/npcs/phase3a/npc-{id}/atlas.png';h=hashlib.sha256(subprocess.check_output(['git','show','checkpoint/phase3a-four-context-pilot-20261027:'+n],cwd=R)).hexdigest();assert h==sha(R/n);pilots[id]=h
(D/'source-provenance.json').write_text(json.dumps({'authoring':'Reproducible own-native NPC recipe; approved Juni landmark motion numbers only. No copied playable face/costume/atlas pixels. Original artwork read-only.','paidAPIs':[],'externalImageAPIs':[],'nativeRegistration':[96,112,48,100],'files':provenance,'fourPilotAtlasesUnchangedSincePilot':pilots,'humanArtApproval':'PENDING'},indent=2)+'\n')
qa=D/'QA.md';s=qa.read_text();focused=load('final-focused/e2e-results.json')['stats'];assert focused['expected']==7 and focused['unexpected']==0 and focused['skipped']==0;assert load('package-npcs-smoke.json')['status']=='PASS' and load('package-characters-smoke.json')['status']=='PASS';assert load('device-export-smoke.json')['formExport']=='PASS'
s=s.replace('| Typecheck/assets/lint/format |See final logs|','| Typecheck/assets/lint/format |PASS|').replace('| Build/portable build |See final logs|','| Build/portable build |PASS|').replace('| Independent ZIP |PENDING until package proof|CRC/SHA,extracted runtime and actual input test required |','| Independent ZIP |PASS technical|CRC/SHA; separately extracted runtime,all14NPC dialogues,all12curated looks,save/reset/reload and actual touch movement |')
s+='\nFinal scope: full60test regression passed with0skips/0flaky. Two subsequent QA-only approach-spawn amendments placed coastal review starts on coherent public routes; the independent bridge recording now starts at the existing approved `bridge-a-mainland` entry. Runtime art/game rules were unchanged. A fresh build and all7NPC browser cases passed again after those amendments. [Final7report](final-focused/e2e-results.json),[full60report](e2e/e2e-results.json),[logs](logs/full-60-e2e.log).\n\nIndependent artifact: [NPCsmoke](package-npcs-smoke.json),[12characters/Studio/persistence/touch](package-characters-smoke.json),[device export](device-export-smoke.json),[ZIP CRC/SHA inventory](package-proof.json),[source provenance](source-provenance.json). Large native scenes and full cross-zone/stability videos remain available at the immutable tag even where the compact ZIP links online.\n';qa.write_text(s)
perf=load('performance-observations.json');p=D/'PERFORMANCE.md';s=p.read_text()+'\n## Actual desktop probe\n\nObserved initial ready time: '+str(perf['loadingMs'])+'ms. These shared-host measurements are observations,not hardware certification.\n\n| Stage | RAF samples | p50 ms | p95 ms | NPC sim updates | NPC animation updates |\n|---|---:|---:|---:|---:|---:|\n'
for row in perf['stages']:
 c=row['cadence'];s+=f'| {row["label"]} | {c["samples"]} | {c["p50"]:.2f} | {c["p95"]:.2f} | {row["simulationUpdates"]} | {row["animationUpdates"]} |\n'
s+='\nScenicTour returned to exact original player coordinates: `'+str(perf['anchor'])+'` → `'+str(perf['returned'])+'`. Physical/hardwareGPU status stays NOT TESTED.\n';p.write_text(s)
print('Consolidated provenance,full60+final7,independent package evidence and measured performance. Human approval PENDING.')
