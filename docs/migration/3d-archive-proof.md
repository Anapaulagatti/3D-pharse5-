# Verified 3D recovery

Archive SHA: `f1f13f2b4aebcc2659d94cde84800cef17ad7a4e`.

- Branch `archive/3d-final-before-pixel-v3-20261015`
- Annotated tag `checkpoint/3d-before-pixel-v3-20261015` (peeled SHA matched via independent git ls-remote).
- Fresh HTTPS remote clone completed; all 2,738 working-tree file SHA256 values matched. No LFS objects used. JSON contains every path/hash/size and ignored duplicate audit. No active QA/server process was present at migration preflight.
- Includes approved Blender/GLBs/textures, v0.5 release and complete unfinished v0.6 sources, concepts, packages and failed/successful partial QA. v0.6 was not released/finally verified.
- No history rewrite or force push. Current branch removal is recorded in deletion-manifest.json. Old public v0.5 is not replaced.

## Restore in a separate directory

```sh
git clone --branch archive/3d-final-before-pixel-v3-20261015 https://github.com/Anapaulagatti/3D-pharse5-.git Korean-Arena-3D-recovery
cd Korean-Arena-3D-recovery
git rev-parse HEAD
# must equal f1f13f2b4aebcc2659d94cde84800cef17ad7a4e
cd preview
npm ci
```

The fresh-clone file restore was executed; reinstalling the old 3D toolchain was not needed or repeated. Do not reset the pixel branch to restore the old project.
