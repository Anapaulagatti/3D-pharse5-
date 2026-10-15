# Verified recovery — never rewrite tags or history

The pre-cleanup game and complete historical3D project have immutable annotated tags on origin. Both were freshly cloned via HTTPS and every tracked file was read and SHA256-hashed. See current/recovery-verification.json.

```sh
git clone --branch recovery/pixel-before-anim-cleanup-20261015 --single-branch https://github.com/Anapaulagatti/3D-pharse5-.git pixel-recovery
git -C pixel-recovery rev-parse HEAD
# 3b62e9b772e9d1e542d13b951ba67a0744c38c35 — 5948 files

git clone --branch recovery/historical-3d-20261015 --single-branch https://github.com/Anapaulagatti/3D-pharse5-.git historical-3d
git -C historical-3d rev-parse HEAD
# f1f13f2b4aebcc2659d94cde84800cef17ad7a4e — 2738 files
```

Use a separate directory for recovery; do not reset the active checkout or force-push. Tags preserve sources, all prior experiments, old reports/packages and approved3D assets without retaining them in the active tree. Existing archive branches/tags are also preserved. Deleted files remain in Git history, so full-history clone size does not shrink; a shallow clone of the cleaned tip does.

The public Pages site is a separately deployed workflow artifact, not a live rendering of main. No unfinished2D publication is authorized. Main promotion requires no pages-writing workflow at the new tip and unchanged public HTML; otherwise stop for publication approval.
