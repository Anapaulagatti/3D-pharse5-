from pathlib import Path
import json,re,shutil
R=Path.cwd();D=R/'docs/phase3bd'
full=json.loads((R/'.cache/phase3bd-full/e2e-results.json').read_text());follow=json.loads((R/'.cache/phase3bd-regression-followup/e2e-results.json').read_text());target=json.loads((R/'.cache/phase3bd-targeted/e2e-results.json').read_text());zone=json.loads((R/'.cache/phase3bd-zone-final/e2e-results.json').read_text())
assert re.search(r'Tests\s+199 passed', (R/'.cache/phase3bd-unit-batched.log').read_text())
assert follow['stats']['expected']==15 and follow['stats']['unexpected']==1 and follow['stats']['skipped']==0,follow['stats']
assert zone['stats']['expected']==3 and zone['stats']['unexpected']==0 and zone['stats']['skipped']==0,zone['stats']
assert target['stats']['expected']==6 and target['stats']['unexpected']==0
for name in ['GAMEPLAY_QA.json','PROTECTED_AUDIT.json','ASSET_CONTRACT.json','BROWSER_PERFORMANCE.json','NATIVE_RENDERING.json']:
 assert json.loads((D/name).read_text())['status'].startswith('PASS'),name
checks=[
('Typecheck / assets / lint / formatting / production build','PASS','Fresh local commands; unchanged1900kB bundle-size advisory retained. CI configured, remote CI not executed.'),
('Unit tests','PASS','199/199 across28files. Offline growth/invalid actions/funds/full bags/stock/double harvest/receipt rollback/migration/world cleanup covered.'),
('Initial full active E2E regression','FAIL',f"{full['stats']['expected']} PASS / {full['stats']['unexpected']} FAIL / {full['stats']['skipped']} skipped. Original result retained; see HISTORICAL_FAILURES.md."),
('Isolated motion / six-identity follow-up','PASS','12/12 locomotion runs (6actors×2) and2/2 six-identity complete dialogue runs. Follow-up total15PASS/1FAIL because worker retained the obsolete zone metadata assertion; original report retained.'),
('Corrected inactive-zone lifecycle follow-up','PASS','Fresh3/3 with every physical/animation/conversation/history field frozen, bounded textures/actors, reentry/despawn and oneplayer. Only derived time-based activity metadata may follow DailyLife clock. No scheduler/gameplay changes.'),
('New canonical/marker/shop/mobile targeted E2E','PASS','6/6 independently; same6also PASS in initial full run. Legacy query/direct URL/reload requests only canonical world;3actual QA approaches; shop replay;667x375 joystick farming.'),
('Two NEW actual packaged quest loops','PASS','Nayeon radish till/plant/water/grow/harvest; Minseo buy/scallion/grow/harvest/sell; wrong→different→correct; reload, one reward,37coins/40gameXP. Eight real control legs, no teleport/state/time completion override.'),
('Three previous actual quest loops','PASS','Fresh isolated real Phaser delivery/orchard/practice-tray completion, wrong/different/right, reward receipts/reload; no old evidence count reuse.'),
('Protected assets and roster/cosmetics','PASS','10462 retained source/runtime files unchanged;26NPC/12player catalogs;24active cosmetics/39native variants exact,4head items remain retired in current play. Historical snapshots retain their original bytes.'),
('Canonical build/source/ZIP transport guard','PASS','585allowlisted assets;416confirmed rejected files git rm,183required donor files moved byte-exact out of public,128exceptions retained. Source/artifact/hash/CItransport guards. Final ZIP CRC/extraction/launch proof is separate.'),
('Native rendering/performance','PASS','5actual native canvas crops: zoom1/nearest/integer camera/one player. No sprite or ground resampling; runtime texture keys unique and NPC cap4. Estimates are not GPU hardware measurements.'),
('New art/provenance','PASS','6original16x20crop frames and exact128x96approved-source Jeju postcard crop; no new image-generation/provider/third-party artwork/audio/font.'),
('Public exposure / artistic/curriculum approval','NOT TESTED','New exact public approval PENDING; owner gameplay/art review needed. Korean content PENDING_HUMAN_REVIEW. No public upload/deployment/main merge.'),
('Physical Android/iPhone / hardware GPU','NOT TESTED','Desktop Chromium + mobile browser emulation only; no physical performance certificate.'),
('Spatial/source decisions','WARN','Bakery deferred, station8px strip retained with prior eastern route, uncertain oldGate3 source classified/excluded rather than indiscriminately deleted. Historical commits not erased.'),
]
qa={'status':'READY_FOR_OWNER_REVIEW / INITIAL_REGRESSION_WARNINGS_RETAINED','summary':'Functional private Phase3BD farm/shop/twoquest slice; 26preservedNPC/12players/24cosmetics/5quests; canonical world unchanged. No public release. Read initial failures and follow-up separately.','checks':[dict(check=c,status=s,evidence=e)for c,s,e in checks],'initialFullRegression':full['stats'],'regressionFollowup':follow['stats'],'correctedZoneFollowup':zone['stats'],'targeted':target['stats'],'unitTests':199,'learningMode':'LOCAL_DEMO','educationalReview':'PENDING_HUMAN_REVIEW','ads':'DISABLED','physicalDevices':'NOT TESTED','publicExposure':'PENDING_EXACT_OWNER_APPROVAL'}
(D/'QA_RESULT.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
(D/'QA.md').write_text('# Phase3BD QA\n\n'+qa['status']+'\n\n| Check | Status | Evidence |\n|---|---|---|\n'+'\n'.join(f'|{c}|{s}|{e}|'for c,s,e in checks)+'\n\nThese are separate runs; not an invented clean combined79-test result. Twelve rejected-world-only cases are archived with their old controller. Six current-world/economy cases added; active discovery66. No tests suppressed, no timeout increases, no animation heuristics reduced.\n')
for name,report in [('FULL_REGRESSION_RESULT.json',full),('REGRESSION_FOLLOWUP_RESULT.json',follow),('ZONE_FOLLOWUP_RESULT.json',zone)]:
 (D/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(qa['status'], full['stats'],follow['stats'])
