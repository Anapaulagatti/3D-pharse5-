from pathlib import Path
import re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';source=(R/'docs/phase2c/DEVICE_REVIEW.html').read_text();source=source.replace('Phase2C','Phase3A').replace("phase:'2C'","phase:'3A'").replace('phase2c-device-report','phase3a-device-report');source=source.replace("const checks=['Landscape safe areas and44px controls','All12 gallery and category scrolling','Default/customized front,right,back walk and run','Glasses,hat,hair and garment occlusion','Save,rename,delete,apply,cancel and reload presets','World position,visited markers and progress retained','Joystick isolation and return to gameplay','60character switches and100cosmetic preview/apply','Resource counts,visible smoothness and thermal behavior']", "const checks=['Landscape safe areas,readable Korean/Vietnamese and44px controls','All14 NPCs across7home zones','Four-direction NPC idle/walk,greetings and occupation gestures','Proximity target,E/touch,choices,next,close and activity return','12zoneexit/entrycycles and60actual dialogues','Original12players/28cosmetics/Studio/presets preserved','Worldposition,realvisitedmarkers andprogress retained','Joystick isolation and preserved ScenicTour','Continuous mainland-to-Jeju bridgeA exploration','Observed cadence,memory,thermal behavior and stability']");assert'All14 NPCs'in source;(D/'DEVICE_REVIEW.html').write_text(source)
(D/'DEVICE_REVIEW.md').write_text('''# Physical-device handoff

Android Chrome: NOT TESTED. iPhone Safari: NOT TESTED. Hardware GPU,thermal and sustained memory acceptance: NOT TESTED.

1. Extract PHASE3A_LIVING_NPC_WORLD_REVIEW.zip. Run `python3 start_review.py` and open REVIEW.html. The compiled game is local/offline; some large full recordings link to the immutable checkpoint. For your own LAN device use explicit `--lan` and the host LAN IP/port4378; no public deployment is required.
2. On the actual device record model,OS/browser version,viewport,DPR,checkpoint and ZIP SHA256. Record genuine screen video and native screenshots.
3. Visit all7regions/all14residents. Verify contextual place/role,visibility,actual paths,four-direction idle/walk,work gestures and greetings. Approach from supported public directions. Entrances/plots/bridges/docks must stay clear.
4. Test E where a keyboard is available and touch interaction. Read Korean/Vietnamese,select both branches,advance,close/escape,return to movement. Verify joystick isolation,44px targets and both landscape safe areas.
5. Repeat12zoneexit/entrycycles and60dialogues. Check one player,no duplicates/orphans,bounded NPC textures,world position,visited markers,existing Studio/cosmetics/preferences and reload. Traverse the approved northern Jeju bridgeA continuously. No other route is certified merely by unchanged artwork.
6. Test ScenicTour and Return without changing player position. Observe actual cadence,thermal behavior,browser reloads and memory. Atlas width×height×4 is an ownership estimate,not measured totalGPU memory.
7. Open DEVICE_REVIEW.html,enter observed PASS/FAIL/WARN and evidence filenames,leave unrun checks NOT TESTED,then export local JSON. The form requires an evidence entry before accepting PASS. Reports are human-entered and do not authenticate evidence or send data to any server.

Desktop Chromium and SwiftShader are technical smoke evidence only. They cannot certify physical Safari/Android or hardware performance. Phase3B remains locked.
''')
print('NPC-specific physical-device checklist/localJSON export created; original Phase2C handoff unchanged')
