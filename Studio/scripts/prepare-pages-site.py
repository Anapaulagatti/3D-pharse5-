#!/usr/bin/env python3
"""Stage only the approved saved v0.3 HTML; never rebuild art or the app."""
import argparse
import hashlib
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description="Prepare the approved two-file GitHub Pages artifact")
parser.add_argument("--output", default=str(root / "_site"))
args = parser.parse_args()
# Pin the reviewed artifact. Future art changes require their own release approval.
approved_sha = "0ce49e58b26baa3802bc6e22fa4cab91d7181232e0069adcedd4f9353270c2d6"
info = json.loads((root / "showcase-v0.3/build-info.json").read_text())
html = (root / "showcase-v0.3/index.html").read_bytes()
if info["asset_version"] != "0.3.0" or len(html) != info["file_bytes"] or hashlib.sha256(html).hexdigest() != info["checksum_sha256"] or info["checksum_sha256"] != approved_sha:
    raise SystemExit("Approved v0.3 HTML integrity check failed")
text = html.decode("utf-8")
patterns = [
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"AKIA[0-9A-Z]{16}", r"ghp_[A-Za-z0-9]{36}",
    r"github_pat_[A-Za-z0-9_]{60,}", r"sk-(?:proj-)?[A-Za-z0-9_-]{40,}",
]
if any(re.search(pattern, text) for pattern in patterns):
    raise SystemExit("Credential-like material detected in the proposed public HTML; inspect locally")
if 'id="studio-dependency-licenses"' not in text:
    raise SystemExit("Bundled dependency license notices are missing")
if re.search(r'<script\b[^>]*\bsrc=|<link\b[^>]*\brel="stylesheet"|sourceMappingURL=', text, re.I):
    raise SystemExit("Public artifact must remain self-contained; external bundle or source map found")
site = pathlib.Path(args.output).resolve()
# Fail closed if a reused artifact directory contains extra/private files.
# Do not delete or copy existing files to make that check pass.
site.mkdir(parents=True, exist_ok=True)
expected = {"index.html", ".nojekyll"}
if any(path.name not in expected or path.is_symlink() or not path.is_file() for path in site.iterdir()):
    raise SystemExit("Output directory contains unexpected files; use a fresh output directory")
(site / "index.html").write_bytes(html)
(site / ".nojekyll").write_bytes(b"")
assert {path.name for path in site.iterdir()} == expected
print("Staged approved v0.3 HTML and .nojekyll only; no source/private files or build/model regeneration")
print(f"HTML bytes: {len(html)}; SHA-256: {info['checksum_sha256']}")
