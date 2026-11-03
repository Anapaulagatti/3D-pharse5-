# Historical scene tests — not current gameplay acceptance

These tests exercise the rejected V10 scene and its old controller, not the approved current canonical Phaser world. Phase3BD explicitly retires that scene and its build entry. Preserve these tests as historical source for recoverable Git checkpoint d54117c0; do not run them against the current world or report their old PASS as current evidence.

Current tests/e2e exercise actual canonical world movement, all26NPCs,12avatars,24cosmetics,3priorquests and new farm/shop mechanics. Cleanup/current-world tests replace old start-page coverage. No timeout, collision or art standard is weakened to make old tests pass.
