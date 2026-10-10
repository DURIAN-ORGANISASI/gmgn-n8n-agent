#!/usr/bin/env python3
"""Ganti placeholder GANTI_SHEET_ID di workflow dengan ID Google Spreadsheet-mu.

Pemakaian:
  python scripts/set_sheet_id.py <ID_ATAU_URL_SPREADSHEET>
  python scripts/set_sheet_id.py https://docs.google.com/spreadsheets/d/XXXX/edit -o dist/workflow.json

Hasil default: dist/gmgn-ai-agent.json (folder dist/ diabaikan git, jadi ID-mu tidak ikut ter-commit).
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = "GANTI_SHEET_ID"
ROOT = Path(__file__).resolve().parent.parent


def extract_id(value: str) -> str:
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", value)
    sheet_id = m.group(1) if m else value.strip()
    if not re.fullmatch(r"[a-zA-Z0-9_-]{20,}", sheet_id):
        raise SystemExit(f"ID spreadsheet tidak valid: {value!r}")
    return sheet_id


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", help="ID atau URL Google Spreadsheet")
    ap.add_argument("-i", "--input", default=str(ROOT / "workflows" / "gmgn-ai-agent.json"))
    ap.add_argument("-o", "--output", default=str(ROOT / "dist" / "gmgn-ai-agent.json"))
    args = ap.parse_args()

    sheet_id = extract_id(args.sheet)
    src = Path(args.input).read_text(encoding="utf-8")
    count = src.count(PLACEHOLDER)
    if count == 0:
        raise SystemExit(f"Placeholder {PLACEHOLDER} tidak ditemukan di {args.input}")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(src.replace(PLACEHOLDER, sheet_id), encoding="utf-8")
    print(f"OK: {count} node diperbarui -> {out}")
    print("Selanjutnya: import file itu di n8n (Workflows > ... > Import from file), lalu pilih credential.")


if __name__ == "__main__":
    sys.exit(main())
