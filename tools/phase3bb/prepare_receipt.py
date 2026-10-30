"""Prepare, never approve, the exact new public payload and existing workflow profile."""
from pathlib import Path
import json,copy,hashlib,subprocess
R=Path.cwd();D=R/'docs/phase3bb-hotfix';C=Path('/workspace/review-pages-destination');proof=json.loads((D/'PUBLIC_CANDIDATE_PROOF.json').read_text());old=json.loads((C/'approved-releases/current.approved.json').read_text());q=copy.deepcopy(old)
q.update(schemaVersion=2,profile='phase3bb-fictional26',purpose='PREVIEW_PUBLIC_EXPOSURE ONLY; new targeted hotfix,26fictional actors and explicitly listed review evidence; not commercial certification',manifestSHA256=proof['manifestSHA256'],artifactCommit=proof['artifactCommit'],decision='PENDING',approvedBy='',approvedAt='',snapshotManifests=proof['snapshots'])
q.pop('ownerDecision',None);q.pop('approvalScope',None)
for k in ['ownerStatement','authorization','publicationLimits','reviewedCandidate']:
 if k in q:q.pop(k)
for k in ['approvalDateLocal','approvalTimezone','approvalSource','timeBasis','exposureManifestSHA256']:
 q.pop(k,None)
q['excluded']={'unverifiedHistoricalBiographies':True,'realCelebrityPhotosVoicesLogos':True,'rawSourceMastersPromptsPrivateAudits':True,'oldPrivate26Videos':True}
q['missingEvidence']=['One exact owner public-preview decision on this new manifest, including six previously excluded fictional-era depictions, revised head cosmetics and new evidence films']
q['readiness']='READY_FOR_EXACT_OWNER_REVIEW; NOT APPROVED OR DEPLOYED'
q['exposureRecordDigestScope']='New exact immutable payload in PUBLIC_CANDIDATE_PROOF.json; old20 approval is not reused.'
q['approvalRequiredReason']='Previous owner receipt binds only bb2c88af/20674e77/20actors; cannot be silently reused for revised assets, six excluded era depictions or new gameplay evidence.'
q['creationTermsReview']['coveredGroups']=['npc-contemporary','npc-fictional-era','world','playable-characters','cosmetics']
q['creationTermsReview']['specificChecks']['identifiablePeople']='20 existing fictional depictions unchanged; six original era-inspired fictional actors assessed in consolidated RIGHTS_AND_SIX.md. No specific copied artwork or identifiable commercial performer established by limited source review; royal/costume/student associations remain disclosed, not certified absent. Exact owner public exposure decision PENDING.'
q['creationTermsReview']['specificChecks']['voiceOutput']='New gameplay review movies contain video only; ffprobe must confirm no audio/ChatGPT Voice output. No real voices, celebrity images, logos or song lyrics added.'
cat=json.loads((R/proof['candidate']/'catalog.json').read_text());q['npcReviews']={}
for row in cat['npcs']:
 q['npcReviews'][row['id']]={'publicName':row['name'],'decision':'PENDING','unresolvedSpecificConcern':False,'depictionReview':'docs/phase3bb-hotfix/RIGHTS_AND_SIX.md'if row['archive']else'docs/review-terms/TERMS_REVIEW.json + unchanged protected native atlas','exposureJustification':'Original fictional public identity; no particular copied third-party work established in inspected records; same owner-confirmed generation terms. Limited screening is not legal/commercial certification.','remainingQualification':'Era/royal/costume association disclosed; owner must review actual depiction in consolidated gallery.'if row['archive']else'No changes to this approved contemporary NPC source pixels.'}
for key in q['groups']:
 q['groups'][key]['decision']='PENDING'
 q['groups'][key]['justification']='Exact new payload requires consolidated owner approval; canonical original artwork preserved, no legal or device certification.'
q['groups']['checkpoint-media']['justification']='Six NEW actual Phaser gameplay videos only, explicitly enumerated in exact manifest; no old private26 or archival videos. No audio stream.'
q['releaseLimitations']=['No source-main merge or productionv0.5 change','No Phase3B-C/D','No commercial legal certification','Physical Android/iPhone/GPU NOT TESTED','Use same review Pages HTTPS URL only after exact approval and protected environment review','Retain approved20 snapshot unchanged']
(D/'PUBLIC_APPROVAL_PENDING.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
(C/'review-candidates/phase3bb-fictional26.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
config=json.loads((C/'review-source.json').read_text());source=proof['sourceCommit']
if source not in config['acceptedBuildSourceCommits']:config['acceptedBuildSourceCommits'].append(source)
config['releaseProfiles']['phase3bb-fictional26']={'manifestSHA256':proof['manifestSHA256'],'npcIds':proof['npcIds'],'artworkEligibility':'DOCUMENTED_PUBLIC_DISPLAY_TERMS','evidenceBasis':'Owner-supplied official Output terms + existing limited depiction review; exact new exposure decision PENDING; no legal/commercial certification','sourceCommit':source,'newScope':['six canonical fictional-era depictions','native head cosmetic revisions','new actual gameplay evidence'],'physicalDevices':'NOT TESTED'}
(C/'review-source.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print('Prepared PENDING exact26 receipt; old approved receipt left unchanged; no art pushed or deployment triggered')
