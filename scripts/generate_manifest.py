#!/usr/bin/env python3
"""Generate SOURCE-MANIFEST.json from the clean release source tree."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED_DIRS={".git",".venv","venv",".esphome",".pio",".platformio","__pycache__","build","dist"}
files=[]
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.name in {"SOURCE-MANIFEST.json","secrets.yaml"}:
        continue
    rel=p.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        continue
    files.append({"path":rel.as_posix(),"size":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={
    "project":"ballu-bsagi-12hn8-esphome",
    "visibility":"private",
    "upstream_url":"https://github.com/Druidblack/AC-Hisense",
    "upstream_commit":"424f65aba9db997fc48bb37f377bc9a72507a8f7",
    "esphome":"2026.6.5",
    "files":files,
}
(ROOT/"SOURCE-MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
print(f"Wrote manifest for {len(files)} files")
