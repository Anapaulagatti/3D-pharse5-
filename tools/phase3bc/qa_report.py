from pathlib import Path
import json,re
R=Path.cwd();D=R/'docs/phase3bc'
report=json.loads((R/'.cache/browser/e2e-results.json').read_text());stats=report['stats'];assert stats['expected']>=70 and stats['skipped']==0 and stats['unexpected']<=1,stats
unit=(R/'.cache/phase3bc-unit-final.log').read_text();assert re.search(r'Tests\s+181 passed',unit)
for path,term in [('.cache/phase3bc-types-final.log','error TS'),('.cache/phase3bc-lint-final.log','error'),('.cache/phase3bc-format-final.log','[warn]')]:assert term not in (R/path).read_text(),path
checks=[
 {'check':'Typecheck / assets / lint / formatting / production build','status':'PASS','evidence':'Current commands completed; build uses canonical rights gate. Build bundle-size advisory retained.'},
 {'check':'Unit tests','status':'PASS','evidence':'181 fresh tests; quest order, invalid references, atomic reward receipts, wrong-answer rotation, reload and retired equipment.'},
 {'check':'Full regression command','status':'WARN'if stats['unexpected']else'PASS','evidence':f'{stats["expected"]} passed / {stats["unexpected"]} failed / {stats["skipped"]} skipped. Obsolete removed-hat expectation retained as FAIL in original report, not relabeled.'},
 {'check':'Updated wardrobe/Studio follow-up','status':'PASS','evidence':'14/14 actual browser tests, including the replacement retired-hat test and unaffected accessory persistence/preview/cache.'},
 {'check':'New12-character legacy equipment + mobile question + local collision E2E','status':'PASS','evidence':'3/3 browser tests; all12 actors walk/run/idle without retired equipment;667x375 touch wrong/right answer and close; source data/controls preserved.'},
 {'check':'Three actual in-world quest loops','status':'PASS','evidence':'Actual isolated packaged Phaser: accept, world interaction, return/recipient, wrong→different question→correct, reward, reload. No teleport or UI-only completion.'},
 {'check':'Nine actual navigation sequences','status':'PASS','evidence':'Palace,retail,station,farm,coast,Namsan,amusement,JejuA,JejuB. Actual held WASD/Shift over canonical floor; no collision override by driver.'},
 {'check':'Native renderer','status':'PASS','evidence':'5 genuine POST_RENDER native canvas PNGs, zoom1, nearest sampling, integer camera, one player. No art processing.'},
 {'check':'Approved asset preservation','status':'PASS','evidence':'9180 prior world/player/NPC/cosmetic/source files SHA256 unchanged; old masks preserved; two new derived collision chunks only.'},
 {'check':'26 NPC identities/interactions/Daily Life','status':'PASS','evidence':'Fresh full-suite resident14/visitor6/archive6 real movements/dialogues, population bounds, schedule interruption/resume and identity checks.'},
 {'check':'Legacy blocked/scenery markers','status':'WARN','evidence':'Jeju3500,3610 planted edge; old3180,4020 ferry marker off deck; palace-west1740,1090 in retained garden. Metadata not silently moved. See collision review.'},
 {'check':'Korean educational approval / gameplay artistic approval','status':'NOT TESTED','evidence':'Original beginner KO/VI data awaits human review. Local demo only, no website history/proficiency/account sync.'},
 {'check':'Real Android/iPhone / hardware GPU','status':'NOT TESTED','evidence':'Desktop Chromium and mobile emulation only; no physical-device or hardware performance certification.'},
 {'check':'New public exposure / Pages update','status':'NOT TESTED','evidence':'Not authorized yet for changed manifest. Existing live26 Pages/v0.5 unchanged; no deployment performed.'},
]
qa={'status':'PASS TARGETED TECHNICAL QA / WARN LEGACY REGRESSION EXPECTATION / HUMAN REVIEW PENDING','summary':'Three actual packaged Phaser quests,9 real route sequences,24active cosmetics,26 preserved NPCs,12players,local-demo learning and atomic local rewards. Existing public26 unchanged. Read exact counts, limitations and retained failures.','checks':checks,'fullRegression':stats,'learningMode':'LOCAL_DEMO','ads':'DISABLED','physicalDevices':'NOT TESTED'}
(D/'QA_RESULT.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
lines=['# Phase3BC QA','',qa['status'],'','| Check | Status | Evidence |','|---|---|---|']+[f'| {r["check"]} | {r["status"]} | {r["evidence"]} |'for r in checks]
lines+=['','The former72-test discovery is retained exactly. Updated14-test wardrobe/Studio and3-test Phase3BC cases pass separately; this is not a claim of one clean75-test run. See HISTORICAL_FAILURES.md.','', 'Protected source artwork, original atlases, gait, camera math, save keys, world geometry and all existing checkpoints remain recoverable. New collision ownership is explicit and local. No full farming/economy/shop/real ad integration, main merge, public deployment or Phase3B-D.']
(D/'QA.md').write_text('\n'.join(lines)+'\n')
(D/'FULL_REGRESSION_STATS.json').write_text(json.dumps(stats,indent=2)+'\n')
print(qa['status'],stats)
