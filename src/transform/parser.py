"""Parse NSE UDiFF zip content and keep NIFTY OPTIDX rows."""

from __future__ import annotations

import csv
from io import StringIO, TextIOWrapper
from pathlib import Path
from zipfile import ZipFile


def parse_udiff_zip(zip_path: str | Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    with ZipFile(zip_path) as archive:
        for member_name in archive.namelist():
            with archive.open(member_name) as member:
                wrapper = TextIOWrapper(member, encoding="utf-8")
                reader = csv.DictReader(wrapper)
                for row in reader:
                    if row.get("INSTRUMENT") == "OPTIDX" and row.get("SYMBOL") == "NIFTY":
                        records.append(row)
    return records


def parse_udiff_text(raw_csv: str) -> list[dict[str, str]]:
    reader = csv.DictReader(StringIO(raw_csv))
    return [
        row
        for row in reader
        if row.get("INSTRUMENT") == "OPTIDX" and row.get("SYMBOL") == "NIFTY"
    ]
