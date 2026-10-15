# Reusable cloud setup

`bash tools/setup.sh` actually executed PASS: Node/Pillow checks, valid-package reuse, source/art validation, typecheck/lint/formatter,5unit tests, production build and3native browser flows. QA uses ignored .cache/setup-qa; it does not regenerate artwork or replace accepted screenshots. Preconditions retained in this environment: Node24+, Python withPillow12.3.0 and Chromium. Fresh remote clone npm ci/checks/build also verified.

Cloud configuration install_script should run `bash /workspace/3D-pharse5-/tools/setup.sh`; start_skill should read persistent records and start root `npm run dev`, not removed3D preview/Studio scripts. The saved repository declaration must identify the exact verified pixel checkpoint at mount_path3D-pharse5-. No worktree, force/reset, token or new network domains needed.

Environment draft saving/snapshot publication and public website publication are separate. Draft persistence does not itself restart services or prove a fresh task restored. Existing live v0.5 must remain unchanged. At Gate2, do not start Gate3 without user's explicit pixel art choice.
