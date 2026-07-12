"""Single-date ETL pipeline orchestration."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .extract.downloader import download_udiff_zip
from .load.upsert import upsert_option_rows
from .transform.enrich import enrich_row
from .transform.parser import parse_udiff_zip
from .transform.schema import OptionRow


def run_pipeline_for_date(trade_date: date, config: dict, session) -> int:
    zip_path = download_udiff_zip(
        trade_date=trade_date,
        output_dir=Path(config["paths"]["raw_dir"]),
        base_url=config["nse"]["base_url"],
    )
    raw_rows = parse_udiff_zip(zip_path)
    records = [enrich_row(OptionRow.from_raw(row)) for row in raw_rows]
    return upsert_option_rows(session, records)
