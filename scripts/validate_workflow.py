#!/usr/bin/env python3
"""Validasi statis workflow n8n di repo ini (dipakai juga oleh CI).

Pemeriksaan:
  1. JSON valid dan nama node unik
  2. Semua koneksi menunjuk node yang ada
  3. Credential tidak memuat ID instance (id harus kosong)
  4. Tidak ada ID spreadsheet nyata (harus placeholder GANTI_SHEET_ID)
  5. Tidak ada pola rahasia (token Discord/Google/Groq/Gemini)
  6. Sintaks JavaScript di node Code (butuh Node.js; dilewati bila tidak ada)
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = sorted((ROOT / "workflows").glob("*.json"))

SECRET_PATTERNS = {
    "token Discord": re.compile(r"[A-Za-z0-9_-]{23,28}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}"),
    "API key Google": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "API key Groq": re.compile(r"gsk_[A-Za-z0-9]{20,}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "URL webhook Discord": re.compile(r"discord(?:app)?\.com/api(?:/v\d+)?/webhooks/\d+/[A-Za-z0-9_-]{20,}"),
}


def check(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")
    try:
        wf = json.loads(raw)
    except json.JSONDecodeError as e:
        return [f"JSON tidak valid: {e}"]

    names = [n["name"] for n in wf["nodes"]]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        errors.append(f"Nama node dobel: {sorted(dup)}")

    for src, outputs in wf["connections"].items():
        if src not in names:
            errors.append(f"Koneksi dari node yang tidak ada: {src}")
        for _type, branches in outputs.items():
            for branch in branches:
                for link in branch:
                    if link["node"] not in names:
                        errors.append(f"Koneksi {src} -> {link['node']} (node tidak ada)")

    for n in wf["nodes"]:
        for cred_type, cred in (n.get("credentials") or {}).items():
            if cred.get("id"):
                errors.append(f"Node '{n['name']}': credential {cred_type} masih berisi id instance")

    if re.search(r"/spreadsheets/d/[A-Za-z0-9_-]{30,}", raw):
        errors.append("Ditemukan URL spreadsheet nyata; gunakan placeholder GANTI_SHEET_ID")
    for n in wf["nodes"]:
        doc = (n["parameters"].get("documentId") or {}).get("value")
        if doc and doc != "GANTI_SHEET_ID":
            errors.append(f"Node '{n['name']}': documentId bukan placeholder ({doc[:8]}...)")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(raw):
            errors.append(f"Terindikasi {label} di dalam file")

    node_bin = shutil.which("node")
    if node_bin:
        for n in wf["nodes"]:
            if n["type"] == "n8n-nodes-base.code":
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                    f.write("(function($, $input, $json, $now){\n" + n["parameters"]["jsCode"] + "\n})")
                    tmp = f.name
                res = subprocess.run([node_bin, "--check", tmp], capture_output=True, text=True)
                if res.returncode != 0:
                    errors.append(f"Node Code '{n['name']}': sintaks JS salah: {res.stderr.strip().splitlines()[-1]}")
    else:
        print("  (Node.js tidak ditemukan, cek sintaks JS dilewati)")
    return errors


def main() -> int:
    if not WORKFLOWS:
        print("Tidak ada file di workflows/")
        return 1
    failed = False
    for path in WORKFLOWS:
        errs = check(path)
        status = "OK " if not errs else "GAGAL"
        print(f"[{status}] {path.relative_to(ROOT)}")
        for e in errs:
            print(f"   - {e}")
        failed |= bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
