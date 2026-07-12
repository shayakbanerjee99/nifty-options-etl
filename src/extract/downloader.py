"""Download UDiFF files for a trade date."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .nse_client import NSEClient


def _udiff_filename(trade_date: date) -> str:
    return f"fo{trade_date.strftime('%d%b%Y').upper()}bhav.csv.zip"


def build_udiff_url(base_url: str, trade_date: date) -> str:
    month = trade_date.strftime("%b").upper()
    return f"{base_url}/{trade_date.year}/{month}/{_udiff_filename(trade_date)}"


def download_udiff_zip(
    trade_date: date,
    output_dir: str | Path,
    base_url: str,
    client: NSEClient | None = None,
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    client = client or NSEClient()
    content = client.get(build_udiff_url(base_url, trade_date))

    destination = output_path / _udiff_filename(trade_date)
    destination.write_bytes(content)
    return destination
