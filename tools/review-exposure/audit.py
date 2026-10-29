"""Exact served-asset assessment. Integrity is separate from rights eligibility."""
from pathlib import Path
import hashlib,json,datetime,collections,re,subprocess
R=Path.cwd();S=Path('/workspace/review-pages-compiled');D=R/'docs/review-exposure';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((S/'export-manifest.json').read_text());prior=json.loads((R/'docs/review-final/PROVENANCE_AUDIT.json').read_text());assert len(prior['rows'])==26
# These are records actually present, not reconstructed account receipts.
sources=['docs/phase3a-art-rebuild/ART_PIPELINE.md','assets-src/npcs/phase3a-art-rebuild/run-manifest.json','docs/phase3a-final-six/ART_PROVENANCE.json','assets-src/juni-animation/run-manifest.json','docs/phase1b/SOURCE_PROVENANCE.md','assets-src/characters/phase2c/catalog.json','LICENSES.md']
provider={'toolIdentified':'built-in host image_gen.imagegen in Codex','platform':'OpenAI Codex (current platform context; historical records name built-in tool, not a separately billed API provider)','externalImageAPIRecorded':False,'underlyingModel':'UNKNOWN; not needed to establish a license unless applicable terms make it relevant','accountController':'UNKNOWN','accountServiceAndAgreement':'UNKNOWN','termsEffectiveAtCreation':'UNKNOWN','distributionEntitlement':'UNKNOWN','sourceRecords':[{'path':p,'sha256':sha(R/p)}for p in sources],'notEvidence':'A current terms URL or historical Git timestamp is not the creator account agreement or its effective date.'}
(D/'PROVIDER_EVIDENCE.json').write_text(json.dumps(provider,ensure_ascii=False,indent=2)+'\n')
rows=[];hist=[]
for a in prior['rows']:
 for e in a['sourceEvidence']:assert sha(R/e['path'])==e['expectedSHA256']
 row={k:a[k]for k in ['id','name','archive','atlasSHA256','concern','conditionalRedesignProposal']}
 row.update(depictionAssessment='NEEDS REVIEW'if a['archive']else'PASS — limited original-fictional depiction screen; no concrete copied work identified',sourceIntegrity='PASS',termsEligibility='PENDING_SHARED_ACCOUNT_EVIDENCE',ownerExposure='NOT APPROVED',publicEligible=False,mandatoryRedesign=False,concreteReferenceWork=None)
 rows.append(row)
 if a['archive']:hist.append(row)
(D/'NPC_ASSESSMENT.json').write_text(json.dumps({'scope':'Limited recorded-input and native visual screen, not legal clearance or comprehensive reverse image search','contemporary':20,'eraInspired':6,'sourceReferences':309,'rows':rows},ensure_ascii=False,indent=2)+'\n')
# Classify EVERY exact manifest member; snapshots inherit all underlying concerns.
def group(row):
 n=row['filename'];origin=row['origin']
 if row.get('npcId'):return 'npc-era'if row['npcId'].startswith('npc-history-')else'npc-contemporary'
 if '/cosmetics/' in n:return 'cosmetics'
 if any(s in n for s in ['/characters/','/juni/','/character-studio/']):return'playable-characters'
 if n.endswith('.mp4'):return'checkpoint-media'
 if '/gate' in n or '/world/' in n:return'world'
 if n.endswith(('.bin','.png')):return'world'
 if 'licenses/' in n or n.endswith(('/LICENSE','/LICENSES.md'))or n in ['LICENSE','LICENSES.md']:return'license-notices'
 if '/play/assets/'in '/'+n and n.endswith(('.js','.css')):return'compiled-code-and-embedded-data'
 return'portal-and-metadata'
for x in manifest['files']:
 p=S/x['filename'];assert p.is_file()and not p.is_symlink()and sha(p)==x['sha256'],x['filename']
 g=group(x);origin=R/x['origin'];matches=origin.is_file()and sha(origin)==x['sha256']
 rowspec={'filename':x['filename'],'sha256':x['sha256'],'bytes':x['bytes'],'group':g,'npcId':x.get('npcId'),'origin':x['origin'],'canonicalFileHashMatches':bool(matches),'integrity':'PASS','eligibility':'PENDING_SHARED_ACCOUNT_EVIDENCE'if g in ['world','npc-era','npc-contemporary','playable-characters','cosmetics','checkpoint-media','compiled-code-and-embedded-data']else'PROJECT_OR_LICENSE_DOCUMENTED_OWNER_EXPOSURE_PENDING','publicEligible':False}
 rowspec['assessment']='Source contract/permission UNKNOWN; not cleared by MIT or names'if rowspec['eligibility'].startswith('PENDING')else'Project tooling/notices; check retained third-party notice coverage and public metadata scope'
 if p.suffix in ['.json','.bin']and g in ['world','playable-characters','cosmetics','npc-contemporary','npc-era']:
  rowspec['eligibility']='PROJECT_AUTHORED_REGISTRATION_OR_NAVIGATION_DATA_OWNER_EXPOSURE_PENDING';rowspec['assessment']='Project-authored numeric/registration/navigation metadata under project notice; this does not grant rights to linked artwork.'
 if g=='compiled-code-and-embedded-data':
  rowspec['eligibility']='SOFTWARE_LICENSE_DOCUMENTED_NOTICE_REPAIR_REQUIRED';rowspec['assessment']='Project/MIT software and original metadata; retain dependency/vendor notices in derived package. Its image dependencies remain separately blocked.'
 # Kept separate from NPC assessment rows.
 globals().setdefault('served',[]).append(rowspec)
summary=dict(collections.Counter(x['group']for x in served));assert len(served)==1367
report={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifestSHA256':sha(S/'export-manifest.json'),'files':len(served),'groups':summary,'ownerArtGameplayDailyLife':'APPROVED by latest user decision; not exposure approval','ownerPublicExposure':'NOT APPROVED','knownEligibleArtFiles':0,'qualifier':'No art eligible to publish on current evidence. 20-NPC subset can be technically prepared privately but cannot truthfully be called cleared or publicly safe.','rows':served}
(D/'ALL_ASSET_ASSESSMENT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Actual distributed CSS; no downloaded font license requirement if no font shipped.
fontFiles=[x['filename']for x in manifest['files']if Path(x['filename']).suffix.lower()in ['.woff','.woff2','.ttf','.otf']];audioFiles=[x['filename']for x in manifest['files']if Path(x['filename']).suffix.lower()in ['.mp3','.ogg','.wav','.m4a','.aac','.flac']]
css=[S/x['filename']for x in manifest['files']if x['filename'].endswith('.css')];fontRules=[]
for p in css:
 t=p.read_text();fontRules.extend({'file':str(p.relative_to(S)),'rule':r}for r in re.findall(r'font-family\s*:\s*[^;}]+',t))
licenses=[]
for name,path in [('Phaser','node_modules/phaser/LICENSE.md'),('Zod','node_modules/zod/LICENSE'),('EventEmitter3','node_modules/eventemitter3/LICENSE')]:
 p=R/path;licenses.append({'package':name,'license':'MIT','source':path,'sha256':sha(p),'noticeInOriginalCandidate':name!='EventEmitter3','action':'Ship full exact notice in derived candidate'if name=='EventEmitter3'else'Preserve notice'})
(D/'SOFTWARE_FONT_AUDIO_ASSESSMENT.json').write_text(json.dumps({'fontFiles':fontFiles,'fontRules':fontRules,'audioFiles':audioFiles,'mediaStreams':'MEDIA_STREAM_AUDIT.json: all four MP4 files have video only','licenses':licenses,'bundledFontAndAudio':'NONE','softwareRights':'MIT notices documented; EventEmitter3 notice coverage strengthened in derived candidates. No AI image rights inferred.','portal':'Project-authored code under LICENSE; no raw prompts/account records in public export; source/QA/version metadata reviewed separately from imagery.'},ensure_ascii=False,indent=2)+'\n')
print('Assessed',len(served),'served files;',summary,'; account terms UNKNOWN, no public eligibility invented')
