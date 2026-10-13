#!/usr/bin/env python3
"""Package verified, existing HTML for local HTTP viewing and static hosting."""
import hashlib
import json
import pathlib
import zipfile

root = pathlib.Path(__file__).resolve().parents[2]
showcase = root / "showcase"
info = json.loads((showcase / "build-info.json").read_text())
html = (showcase / "index.html").read_bytes()
if len(html) != info["file_bytes"] or hashlib.sha256(html).hexdigest() != info["checksum_sha256"]:
    raise SystemExit("Saved index.html differs from build-info.json; do not package unverified HTML")
downloads = root / "downloads"
downloads.mkdir(exist_ok=True)
local = downloads / "showcase-v0.2-http.zip"
static = downloads / "showcase-v0.2-static.zip"
with zipfile.ZipFile(local, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name in ["index.html", "start.py", "START_WINDOWS.cmd", "README.md", "DEPLOYMENT.md", "build-info.json"]:
        archive.write(showcase / name, f"Korean-Arena-Showcase-v0.2/{name}")
with zipfile.ZipFile(static, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    archive.write(showcase / "index.html", "index.html")
    archive.writestr(".nojekyll", "")
packages = []
for package in [local, static]:
    data = package.read_bytes()
    packages.append({"file": str(package.relative_to(root)), "file_bytes": len(data), "checksum_sha256": hashlib.sha256(data).hexdigest()})
    print(f"Saved {package.relative_to(root)} ({len(data):,} bytes)")
(downloads / "package-manifest.json").write_text(json.dumps({
    "version": "0.2.0", "html_sha256": info["checksum_sha256"], "packages": packages,
    "public_deployment": "Not published; explicit user approval required",
}, indent=2) + "\n")
