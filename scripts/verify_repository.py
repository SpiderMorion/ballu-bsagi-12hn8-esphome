#!/usr/bin/env python3
"""Fail-closed source-only repository audit."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "NOTICE.md", "LICENSE.md", "requirements.txt",
    "SOURCE-MANIFEST.json", "patches/upstream-to-production.patch",
    "ballu-bsagi-12hn8.yaml", "secrets.example.yaml",
    "AC-Hisense/components/ac_hi/__init__.py",
    "AC-Hisense/components/ac_hi/climate.py",
    "AC-Hisense/components/ac_hi/ac_hi.h",
    "AC-Hisense/components/ac_hi/ac_hi.cpp",
    "AC-Hisense/components/ac_hi/kelon168_protocol.h",
    "AC-Hisense/components/ac_hi/kelon168_protocol.cpp",
    ".github/workflows/build.yml",
}
FORBIDDEN_DIRS = {".git", ".venv", "venv", ".esphome", ".pio", ".platformio", "__pycache__", "build", "dist"}
FORBIDDEN_SUFFIXES = {".bin", ".elf", ".map", ".o", ".a", ".pyc", ".pyo"}
SECRET_PATTERNS = {
    "private key": re.compile(rb"BEGIN [A-Z ]*PRIVATE KEY"),
    "GitHub token": re.compile(rb"gh[opusr]_[A-Za-z0-9_]{20,}"),
    "Home Assistant bearer token": re.compile(rb"eyJ[a-zA-Z0-9_-]{30,}\.eyJ"),
}

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument("--allow-local-secrets",action="store_true");args=ap.parse_args()
    missing=sorted(p for p in REQUIRED if not (ROOT/p).is_file())
    if missing: fail(f"missing required files: {missing}")
    files=[]
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT)
        if any(part in FORBIDDEN_DIRS for part in rel.parts): continue
        if p.is_symlink(): fail(f"symlink is not allowed: {rel}")
        if p.is_file(): files.append(p)
    bad=[str(p.relative_to(ROOT)) for p in files if p.suffix.lower() in FORBIDDEN_SUFFIXES]
    if bad: fail(f"compiled artifacts present: {bad}")
    local=ROOT/"secrets.yaml"
    if local.exists() and not args.allow_local_secrets: fail("secrets.yaml must not be present for release audit")
    for p in files:
        if p == local: continue
        data=p.read_bytes()
        for name,pattern in SECRET_PATTERNS.items():
            if pattern.search(data): fail(f"{name} pattern in {p.relative_to(ROOT)}")
    yaml=(ROOT/"ballu-bsagi-12hn8.yaml").read_text()
    required_yaml=["board: esp32dev","baud_rate: 9600","tx_pin: GPIO16","rx_pin: GPIO17","baud_rate: 0","reboot_timeout: 0s","path: AC-Hisense/components"]
    for text in required_yaml:
        if text not in yaml: fail(f"required YAML invariant missing: {text}")
    readme=(ROOT/"README.md").read_text()
    for text in ["## Архитектура","## Схема подключения","## Первичная прошивка ESP32","## Интеграция с Home Assistant","## Протокол и принцип работы"]:
        if text not in readme: fail(f"README contract missing: {text}")
    for target in re.findall(r"\[[^]]+\]\((?!https?://|#)([^)]+)\)", readme):
        if not (ROOT / target).exists(): fail(f"broken local README link: {target}")
    manifest=json.loads((ROOT/"SOURCE-MANIFEST.json").read_text())
    if manifest.get("upstream_commit") != "424f65aba9db997fc48bb37f377bc9a72507a8f7":
        fail("unexpected upstream commit in manifest")
    for item in manifest.get("files", []):
        p=ROOT/item["path"]
        if not p.is_file(): fail(f"manifest member missing: {item['path']}")
        if p.stat().st_size != item["size"]: fail(f"manifest size mismatch: {item['path']}")
        if hashlib.sha256(p.read_bytes()).hexdigest() != item["sha256"]:
            fail(f"manifest hash mismatch: {item['path']}")
    manifest_paths={item["path"] for item in manifest.get("files", [])}
    release_paths={p.relative_to(ROOT).as_posix() for p in files if p.name not in {"SOURCE-MANIFEST.json", "secrets.yaml"}}
    if manifest_paths != release_paths:
        fail(f"manifest member set mismatch: missing={sorted(release_paths-manifest_paths)}, extra={sorted(manifest_paths-release_paths)}")
    print(f"PASS: source-only audit, {len(files)} files checked")

if __name__ == "__main__": main()
